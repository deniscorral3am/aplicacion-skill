---
name: aplicacion
description: Te lleva de cero a una app de iPhone que cobra, con el plan de 5 pasos de Greg Isenberg y el plugin oficial de Apple para Claude (Xcode dentro de Claude Code). Busca apps que facturan mucho pero tienen menos de 3,5 estrellas, lee sus reseñas y te saca las 5 quejas que más se repiten, construye contigo una app mejor en Xcode (la compila, la prueba en el simulador y la arregla sola), le monta la suscripción con el paywall justo después de resolverle el problema al usuario y te deja el plan de contenido y anuncios. Úsala cuando digan /aplicacion, «comenta APLICACIÓN», «quiero hacer una app», «app para la App Store con Claude», «plugin de Apple para Claude», «Xcode con Claude» o «el plan de Greg Isenberg».
---

# /aplicacion: una app para la App Store con Claude y el plugin oficial de Apple

Al terminar, el usuario tiene: la app elegida con datos (factura y la gente está enfadada), las 5 quejas de sus
reseñas, una app suya en Xcode que resuelve esas quejas y funciona en el simulador, la suscripción con el paywall en
su sitio y el plan de contenido para venderla.

Habla en español, cercano, corto y sin tecnicismos. Una pregunta cada vez. Nunca pidas contraseñas ni claves en el chat.
El detalle del método está en `ref/plan.md`. Todo lo del usuario se guarda en `~/Apps/<nombre-de-la-app>/`.

## Paso 0. Comprobar el ordenador

```bash
bash ~/.claude/skills/aplicacion/scripts/comprobar.sh
```

- **Hace falta un Mac.** Las apps de iPhone se hacen con Xcode y Xcode solo existe en Mac. Si no tiene Mac, díselo
  claro: puede hacer los pasos 1, 2 y 5 (investigar, quejas y contenido) y dejar la construcción para cuando lo tenga.
- **Xcode, la última versión** (gratis en la Mac App Store). Que lo abra una vez y acepte la licencia.
- **El plugin oficial de Apple para Claude.** Está en el marketplace oficial de Anthropic, con «Apple Inc.» de autor.
  Dile que escriba en Claude Code:

  ```
  /plugin install xcode@claude-plugins-official
  ```

  El plugin no se descarga de internet: Claude Code lo coge del propio Xcode del Mac
  (`xcrun agent plugin path --plugin-format claude`). Si da error, casi siempre es que su Xcode es antiguo.
  Después, que reinicie Claude Code. Con el proyecto abierto en Xcode, la primera vez Xcode pide permiso para que el
  agente lo use: que diga que sí.
- Para **publicar** en la App Store hace falta la cuenta de desarrollador de Apple (Apple Developer Program, 99 €/año).
  Para construir y probar en el simulador, no. Díselo ahora para que no se lleve la sorpresa al final.

## Paso 1. Encontrar la app (factura mucho y tiene menos de 3,5 estrellas)

Pregunta (una tanda corta): qué categoría le tira (si no sabe: **utilidades** o **productividad**, son aburridas y
pagan), en qué país quiere vender (por defecto `es` y `us`) y si tiene cuenta de **Appfigures** o Sensor Tower.

- **Con Appfigures:** que abra Top Apps / Explorer, categoría elegida, ordene por ingresos y te pegue (o te pase
  captura de) las que tengan menos de 3,5 estrellas con su ingreso estimado. Las estimaciones de ingresos suelen
  pedir plan de pago: si no las ve, usa el plan B.
- **Plan B, sin cuenta** (lo haces tú):

  ```bash
  python3 ~/.claude/skills/aplicacion/scripts/app_store.py buscar --categoria utilidades --pais es
  python3 ~/.claude/skills/aplicacion/scripts/app_store.py buscar --categoria utilidades --pais us
  ```

  Saca las 100 que más facturan de esa categoría (ranking público de Apple) con su nota, nº de valoraciones y días
  sin actualizar, y separa las de menos de 3,5. Si salen pocas, prueba otra categoría (`... categorias`) o sube a
  `--max-nota 3.8` y dilo.
- Ordena las candidatas: más arriba en facturación, peor nota, más valoraciones (= más gente usándola) y **6 meses o
  más sin actualizarse** (puntos extra). Enséñale una tabla con las 5 mejores y recomiéndale 2-3 para el paso 2.
- Nunca digas cuánto factura una app si no viene de Appfigures o Sensor Tower: el ranking de Apple dice quién factura
  más, no cuánto.

Guarda la tabla en `~/Apps/investigacion/candidatas.md`.

## Paso 2. Leer sus reseñas y sacar las 5 quejas

Para cada candidata:

```bash
python3 ~/.claude/skills/aplicacion/scripts/app_store.py resenas --id <ID> --pais es,us --salida ~/Apps/investigacion/<id>.json
```

Lee las reseñas de 1 y 2 estrellas (`resenas_malas`) y agrúpalas en **las 5 quejas que más se repiten**, cada una con
cuántas veces sale y 2 frases literales de usuarios. Clasifica cada queja:

- **Precio** («es carísima», «me cobraron sin avisar»): si se quejan del precio pero pagan, hay demanda.
- **Producto** (fallos, cuelgues, anuncios, pasos de más, le falta algo): **ahí entras tú**.

Elige con él la app donde **las quejas son del producto, no del precio**. Mira también en Reddit si hay hilos
«alternative to <app>» (con la búsqueda web) y apúntalos: son los primeros que la van a probar.

Rellena `plantillas/quejas.md` y guárdalo en `~/Apps/<nombre>/quejas.md`, con «la primera victoria»: el momento exacto
en que el usuario ve que tu app sí le funciona. Enséñaselo y que lo apruebe antes de construir.

## Paso 3. Construir la app con el plugin de Apple (y que se pruebe sola)

1. Pregúntale el nombre (o propón 5 con gancho) y crea el proyecto en `~/Apps/<nombre>/` (SwiftUI, iOS). Que lo abra en
   Xcode para que el plugin pueda trabajar con él.
2. Construye **solo lo que resuelve las 5 quejas** y el flujo principal. Nada de extras. Si al competidor le cuesta 6
   toques, a la tuya 2. Si tiene sentido, botón «Importar desde <competidor>» para que cambiarse cueste 10 segundos.
3. El ciclo, con las herramientas del plugin de Xcode, hasta que quede bien:
   compilar → abrir en el simulador → recorrer cada flujo del que se quejaban → mirar las vistas previas y los
   registros → arreglar → volver a compilar. Haz capturas del simulador y enséñaselas.
4. Antes de dar una pantalla por buena, márcala en `quejas.md` («Comprobado»). Si no resuelve su queja, no está lista.
5. Si quiere IA dentro de la app: los Foundation Models de Apple (corren en el iPhone, sin coste por uso).
6. Cuando funcione entera: TestFlight a 10-20 personas (las de Reddit, sus seguidores) antes de lanzar. Esto ya pide la
   cuenta de desarrollador.

Si el plugin no aparece o no responde: `/plugin` para ver si está instalado, Xcode abierto con el proyecto, y que
acepte el permiso de Xcode. Si sigue sin ir, puedes compilar con `xcodebuild` y el simulador con `xcrun simctl`.

## Paso 4. Cobrar, pero cuando ya le has resuelto el problema

- Suscripción con **StoreKit 2** (lo de Apple, sin terceros) o **RevenueCat** (más fácil de medir y de cambiar
  precios). Pregúntale cuál; si no sabe, StoreKit 2 para empezar.
- **El paywall sale justo después de la primera victoria, nunca nada más instalar.** Primero le resuelves el problema;
  luego le cobras por seguir teniéndolo resuelto.
- Anual por defecto con 3 días de prueba; semanal como ancla de precio. Ofertas de recuperación para quien cancela.
- La ficha de la App Store: cada captura contesta una de las 5 quejas («sin anuncios», «funciona sin conexión»,
  «cancela cuando quieras»). Pide la valoración justo después de una victoria, nunca después de un error.
- Escribe la ficha (nombre, subtítulo, descripción, palabras clave) en español e inglés; si quiere, en 10 idiomas.

No inventes precios de la competencia: si no los ve en la ficha, pregúntale o déjalo como hueco.

## Paso 5. Contenido y anuncios

Déjale en `~/Apps/<nombre>/contenido.md`:

- **10 guiones de vídeo corto** (gancho de 3 s, el problema con las palabras de las reseñas, la app resolviéndolo en
  pantalla, el resultado). Que enseñen **qué resuelve**, no la app por dentro.
- **Quién los graba**, según su tiempo y su dinero: él mismo, creadores pequeños del nicho (base mensual + extra por
  visitas, un código de oferta de Apple por creador para saber quién trae cada suscriptor) o clones de IA (HeyGen,
  Arcads) cuando un vídeo funciona y quiere muchas variaciones.
- **Dónde:** TikTok, Reels y Shorts. Cuentas sin cara con carruseles: problema, captura, resultado.
- **Anuncios:** no hace anuncios nuevos. **Al vídeo orgánico que despega le mete dinero** (TikTok Spark Ads o
  promocionarlo en Instagram) y Apple Ads con el nombre del competidor.

## Al terminar

Resumen corto: la app elegida y por qué, las 5 quejas, dónde está el proyecto, qué funciona ya en el simulador, cómo
cobra y los 3 primeros vídeos que grabaría. Y el siguiente paso concreto (TestFlight, cuenta de desarrollador o enviar
a revisión de Apple).

## Reglas

- **No inventes datos:** ni ingresos, ni descargas, ni notas. Lo estimado va marcado como estimado y con su fuente.
- No copies la app del competidor (ni su nombre, ni sus textos, ni su diseño): resuelve lo mismo, mejor.
- Nada de reseñas falsas ni trucos contra las normas de la App Store: Apple rechaza la app o cierra la cuenta.
- Si algo del plugin de Apple no funciona como dice aquí, dilo y sigue con `xcodebuild`: no te inventes comandos.
