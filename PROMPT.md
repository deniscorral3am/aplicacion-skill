# El prompt

Ábrelo en Claude Code (en tu Mac, con Xcode instalado) y pega todo lo que hay dentro del recuadro.
Si prefieres la versión completa, instala la skill (`README.md`) y escribe `/aplicacion`.

```
Quiero sacar una app de iPhone a la App Store que cobre por suscripción, siguiendo este plan de 5 pasos. Hazlo
conmigo paso a paso, en español, corto y sin tecnicismos, y pregúntame una sola cosa cada vez. No inventes datos
(ingresos, descargas, notas): si algo es estimado, dilo y di de dónde sale.

PASO 0 · PREPARAR EL MAC
- Comprueba que tengo Xcode (xcodebuild -version) y que trae el plugin para Claude
  (xcrun agent plugin path --plugin-format claude). Si no, dime que actualice Xcode desde la Mac App Store.
- Dime que escriba /plugin install xcode@claude-plugins-official (el plugin oficial de Apple para Claude Code) y que
  reinicie Claude Code. Comprueba después que tienes sus herramientas (compilar, simulador, vistas previas).
- Avísame de que para construir y probar no pago nada, pero para publicar hace falta la cuenta de desarrollador de
  Apple (99 €/año).

PASO 1 · ENCONTRAR LA APP
- Pregúntame categoría (si no sé: utilidades o productividad), país (es y us) y si tengo Appfigures.
- Si tengo Appfigures: que ordene por ingresos y te pase las de menos de 3,5 estrellas.
- Si no: usa el ranking público de Apple de las que más facturan por categoría
  (https://itunes.apple.com/<pais>/rss/topgrossingapplications/limit=100/genre=<id>/json; utilidades = 6002,
  productividad = 6007) y la API de búsqueda (https://itunes.apple.com/lookup?id=<ids>&country=<pais>) para sacar
  la nota, el nº de valoraciones y la fecha de la última versión. Ojo: ese ranking dice quién factura más, no cuánto.
- Quédate con las de menos de 3,5 estrellas, ordénalas (más arriba en facturación, peor nota, más valoraciones,
  6 meses o más sin actualizar) y enséñame las 5 mejores en una tabla.

PASO 2 · LAS 5 QUEJAS
- Baja las reseñas de las 2-3 que elija (feed público:
  https://itunes.apple.com/<pais>/rss/customerreviews/page=<1-10>/id=<id>/sortby=mostrecent/json).
- Agrupa las de 1 y 2 estrellas en las 5 quejas que más se repiten, con cuántas veces salen y frases literales.
- Separa quejas de precio (si se quejan del precio pero pagan, hay demanda) y de producto (fallos, anuncios, pasos de
  más: ahí entro yo). Elegimos la app donde las quejas son del producto.
- Busca en Reddit «alternative to <app>» y apunta los hilos.
- Guárdalo en ~/Apps/<nombre>/quejas.md con «la primera victoria»: el momento en que el usuario ve que mi app sí le
  funciona. Enséñamelo y espera mi OK.

PASO 3 · CONSTRUIRLA CON EL PLUGIN DE APPLE
- Crea el proyecto (SwiftUI, iOS) en ~/Apps/<nombre>/ y dime que lo abra en Xcode.
- Construye solo lo que resuelve las 5 quejas y el flujo principal, con menos toques que el competidor.
- Con el plugin de Xcode: compila, ábrela en el simulador, recorre cada flujo del que se quejaban, mira las vistas
  previas y los registros, arregla y vuelve a compilar, hasta que quede perfecta. Enséñame capturas.
- No des una pantalla por buena si no resuelve su queja: márcala en quejas.md.

PASO 4 · COBRAR CUANDO YA LE HAS RESUELTO EL PROBLEMA
- Suscripción con StoreKit 2 (o RevenueCat si te lo pido).
- El paywall sale justo después de la primera victoria, nunca nada más instalar.
- Anual por defecto con 3 días de prueba y semanal como ancla de precio.
- Escribe la ficha de la App Store: cada captura contesta una queja. Pide la valoración justo después de una
  victoria, nunca después de un error.

PASO 5 · CONTENIDO Y ANUNCIOS
- Escríbeme 10 guiones de vídeo corto que enseñen qué resuelve la app (gancho, el problema con las palabras de las
  reseñas, la app resolviéndolo, el resultado).
- Dime quién los graba según mi tiempo y mi dinero: yo, creadores pequeños pagados (con un código de oferta de Apple
  cada uno) o clones de IA.
- Y el plan de anuncios: al vídeo orgánico que funcione le metemos dinero en vez de hacer anuncios nuevos.

Empieza por el paso 0.
```
