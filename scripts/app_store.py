#!/usr/bin/env python3
"""Datos públicos de la App Store para /aplicacion (sin claves, sin dependencias).

Usa solo lo que Apple publica gratis:
  - Ranking de las que más facturan por categoría (feed RSS «top grossing» de iTunes).
  - Ficha de cada app (API de búsqueda de iTunes: nota media, nº de valoraciones, última versión).
  - Reseñas recientes (feed RSS de reseñas: hasta 10 páginas de 50 por país).

Ojo: Apple NO da lo que factura cada app en euros. El ranking dice quién factura más, no cuánto.
Para la cifra estimada hace falta Appfigures o Sensor Tower.

Uso:
  python3 app_store.py buscar  --categoria utilidades --pais es [--max-nota 3.5] [--top 100]
  python3 app_store.py ficha   --id 1510944943 [--pais es]
  python3 app_store.py resenas --id 1510944943 [--pais es,us] [--paginas 10] [--max-estrellas 2] --salida resenas.json
  python3 app_store.py categorias
"""
import argparse
import json
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone

CATEGORIAS = {
    "utilidades": 6002, "productividad": 6007, "negocios": 6000, "salud": 6013,
    "educacion": 6017, "estilo-de-vida": 6012, "finanzas": 6015, "foto-y-video": 6008,
    "medicina": 6020, "musica": 6011, "comida": 6023, "viajes": 6003, "deportes": 6004,
    "navegacion": 6010, "tiempo": 6001, "libros": 6018, "redes-sociales": 6005,
    "compras": 6024, "diseno": 6027, "desarrolladores": 6026, "referencia": 6006,
    "noticias": 6009, "entretenimiento": 6016,
}
UA = {"User-Agent": "Mozilla/5.0 (Macintosh) app-research/1.0"}


def _get(url: str):
    for intento in range(3):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception as e:  # noqa: BLE001
            if intento == 2:
                raise SystemExit(f"No he podido leer {url}: {e}")
            time.sleep(2 * (intento + 1))


def ficha(ids, pais):
    out = []
    for i in range(0, len(ids), 150):
        q = ",".join(str(x) for x in ids[i:i + 150])
        d = _get(f"https://itunes.apple.com/lookup?id={q}&country={pais}&entity=software")
        out += d.get("results", [])
    hoy = datetime.now(timezone.utc)
    res = []
    for r in out:
        ult = r.get("currentVersionReleaseDate")
        dias = None
        if ult:
            dias = (hoy - datetime.fromisoformat(ult.replace("Z", "+00:00"))).days
        res.append({
            "id": r.get("trackId"), "nombre": r.get("trackName"), "empresa": r.get("sellerName"),
            "nota": round(r["averageUserRating"], 2) if r.get("averageUserRating") is not None else None,
            "valoraciones": r.get("userRatingCount"), "precio": r.get("formattedPrice"),
            "categoria": r.get("primaryGenreName"), "dias_sin_actualizar": dias,
            "version": r.get("version"), "url": r.get("trackViewUrl"),
        })
    return res


def buscar(categoria, pais, top, max_nota):
    gid = CATEGORIAS.get(categoria)
    if gid is None and str(categoria).isdigit():
        gid = int(categoria)
    if gid is None:
        raise SystemExit(f"Categoría desconocida: {categoria}. Mira: python3 app_store.py categorias")
    d = _get(f"https://itunes.apple.com/{pais}/rss/topgrossingapplications/limit={min(top, 100)}/genre={gid}/json")
    entradas = d.get("feed", {}).get("entry", [])
    if isinstance(entradas, dict):
        entradas = [entradas]
    ids = [int(e["id"]["attributes"]["im:id"]) for e in entradas]
    puesto = {app_id: n + 1 for n, app_id in enumerate(ids)}
    fichas = ficha(ids, pais)
    for f in fichas:
        f["puesto_facturacion"] = puesto.get(f["id"])
    fichas.sort(key=lambda f: f["puesto_facturacion"] or 999)
    candidatas = [f for f in fichas if f["nota"] is not None and f["nota"] < max_nota]
    return {"categoria": categoria, "pais": pais, "analizadas": len(fichas),
            "candidatas": candidatas, "todas": fichas}


def resenas(app_id, paises, paginas, max_estrellas):
    todas = []
    for pais in paises:
        for p in range(1, paginas + 1):
            url = f"https://itunes.apple.com/{pais}/rss/customerreviews/page={p}/id={app_id}/sortby=mostrecent/json"
            try:
                d = _get(url)
            except SystemExit:
                break
            ent = d.get("feed", {}).get("entry", [])
            if isinstance(ent, dict):
                ent = [ent]
            ent = [e for e in ent if "im:rating" in e]
            if not ent:
                break
            for e in ent:
                todas.append({
                    "pais": pais, "estrellas": int(e["im:rating"]["label"]),
                    "titulo": e.get("title", {}).get("label", ""),
                    "texto": e.get("content", {}).get("label", ""),
                    "version": e.get("im:version", {}).get("label", ""),
                    "fecha": e.get("updated", {}).get("label", ""),
                })
            time.sleep(0.5)
    malas = [r for r in todas if r["estrellas"] <= max_estrellas]
    reparto = {s: sum(1 for r in todas if r["estrellas"] == s) for s in range(1, 6)}
    return {"id": app_id, "total": len(todas), "reparto_estrellas": reparto,
            "malas": len(malas), "resenas_malas": malas, "resenas": todas}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("buscar")
    b.add_argument("--categoria", default="utilidades")
    b.add_argument("--pais", default="es")
    b.add_argument("--top", type=int, default=100)
    b.add_argument("--max-nota", type=float, default=3.5)
    f = sub.add_parser("ficha")
    f.add_argument("--id", required=True)
    f.add_argument("--pais", default="es")
    r = sub.add_parser("resenas")
    r.add_argument("--id", required=True)
    r.add_argument("--pais", default="es", help="uno o varios, separados por comas (es,us,mx)")
    r.add_argument("--paginas", type=int, default=10)
    r.add_argument("--max-estrellas", type=int, default=2)
    r.add_argument("--salida")
    sub.add_parser("categorias")
    a = ap.parse_args()

    if a.cmd == "categorias":
        out = CATEGORIAS
    elif a.cmd == "buscar":
        out = buscar(a.categoria, a.pais, a.top, a.max_nota)
    elif a.cmd == "ficha":
        out = ficha([x.strip() for x in a.id.split(",")], a.pais)
    else:
        out = resenas(a.id, [p.strip() for p in a.pais.split(",")], a.paginas, a.max_estrellas)

    texto = json.dumps(out, ensure_ascii=False, indent=2)
    if getattr(a, "salida", None):
        with open(a.salida, "w", encoding="utf-8") as fh:
            fh.write(texto)
        resumen = {k: v for k, v in out.items() if k not in ("resenas", "resenas_malas")}
        print(json.dumps(resumen, ensure_ascii=False, indent=2))
        print(f"Guardado en {a.salida}", file=sys.stderr)
    else:
        print(texto)


if __name__ == "__main__":
    main()
