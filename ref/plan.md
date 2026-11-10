# El plan de 5 pasos, con detalle

Sale del hilo de Greg Isenberg del 8/11/2026 («now that apple put xcode inside claude code, here's how i'd find, build
and grow an iOS app with AI agents», x.com/gregisenberg/status/2119229734563271124), adaptado a España y a Claude Code.
Lo que va entre corchetes es opcional.

## 1. Encontrar la app (dinero + gente enfadada)

- **Appfigures** (o Sensor Tower) → Top Apps / Explorer → categoría aburrida (utilidades, productividad, herramientas de
  un oficio) → ordenar por ingresos → quedarse con las de **menos de 3,5 estrellas**.
  Las estimaciones de ingresos y algunos filtros de Appfigures piden plan de pago; el plan gratis enseña Top Apps.
- **Sin Appfigures:** `scripts/app_store.py buscar` saca las 100 que más facturan de una categoría en un país (ranking
  público de Apple) con su nota y los días sin actualizar. Te dice quién factura más, no cuánto.
- Puntos extra:
  - la primera de la lista lleva **6 meses o más sin actualizarse**;
  - las palabras clave por las que sale tienen **poca dificultad y mucho dinero** (Appfigures → Keywords);
  - la fila «También te puede gustar» de su ficha: cada app ahí es otro mercado que mirar.

## 2. Leer sus reseñas (dónde entras tú)

- Bajar todas las reseñas posibles de las 5-20 candidatas: `scripts/app_store.py resenas` (feed público de Apple, hasta
  500 por país) [o `facundoolano/app-store-scraper` en Node para más volumen].
- Agrupar las de 1 y 2 estrellas en **las 5 quejas que más se repiten**, con frases literales de usuarios y cuántas veces
  sale cada una.
- Cómo leerlo:
  - **Se quejan del precio pero siguen pagando** → hay demanda. Bien.
  - **Se quejan de fallos, cuelgues, anuncios, pasos de más** → ahí entras tú. Mejor todavía.
  - Elegir la app donde las quejas son **del producto, no del precio**.
- Buscar en Reddit «alternative to <app>»: cada hilo es una lista de gente esperándote.

## 3. Construirla con el plugin oficial de Apple

- **Claude Code + el plugin «xcode» de Apple** (marketplace oficial de Anthropic, autor «Apple Inc.»):
  compila, ejecuta y prueba los esquemas, dibuja las vistas previas de SwiftUI, maneja simuladores y dispositivos,
  lee los registros de compilación y busca en la documentación de Apple.
  `/plugin install xcode@claude-plugins-official` (necesita la última versión de Xcode en el Mac).
- [XcodeBuildMCP (`cameroncooke/XcodeBuildMCP`, hoy en github.com/getsentry/MobileBuildMCP) e `ios-simulator-mcp` (joshuayoes) para que toque,
  deslice y haga capturas como un usuario.]
- Las 5 quejas van a `quejas.md`: **cada pantalla se comprueba contra esa lista** antes de darla por buena.
- IA dentro de la app con los Foundation Models de Apple (en el propio iPhone, coste de inferencia 0 €).
- App Intents para que Siri y los agentes puedan usarla.
- Botón «Importar desde <competidor>»: que cambiarse cueste 10 segundos.
- Probar: cada flujo del que se quejaban, en varios tamaños de pantalla, antes de cada compilación. Si al competidor
  le cuesta 6 toques, a la tuya 2. [Maestro para tests de flujos, Sentry para fallos, TelemetryDeck para analítica.]
- TestFlight a 20 personas de esos hilos de Reddit antes de lanzar.

## 4. Cobrar cuando ya le has resuelto el problema

- Suscripción con StoreKit 2 (lo nativo de Apple) o RevenueCat (suscripciones e ingresos recurrentes)
  [Superwall para probar paywalls sin sacar versión nueva].
- **El paywall sale justo después de la primera victoria, nunca al abrir la app.** La primera victoria = el momento en
  que la app hace lo que la del competidor no hacía bien.
- Anual por defecto con 3 días de prueba; semanal como ancla de precio.
- Ofertas de recuperación (win-back) para quien cancela.
- Ficha de la App Store: cada captura contesta una queja («sin anuncios», «funciona sin conexión», «cancela cuando
  quieras»). Prueba A/B de capturas con Product Page Optimization de App Store Connect. Ficha en 10 idiomas.
- Pedir valoración justo después de una victoria (el aviso nativo de Apple), nunca después de un error.

## 5. Contenido y anuncios

- Vídeos que enseñan **qué resuelve la app** (el problema, la pantalla, el resultado):
  - grabándolos tú;
  - pagando a creadores pequeños del nicho (base mensual + extra por visitas);
  - con clones de IA (HeyGen, Arcads) cuando necesitas muchas variaciones de uno que funciona.
- Banco de ganchos: los 100 que mejor funcionan en tu nicho, cada semana. Lo que pierde a la gente en 3 s, fuera.
- Cuentas sin cara con carruseles 3 veces al día: problema, captura, resultado.
- **Cuando un vídeo orgánico despega, le metes dinero** (TikTok Spark Ads, anuncios de Instagram con ese mismo vídeo)
  en vez de hacer anuncios nuevos.
- Un código de oferta de Apple por creador para saber quién trae cada suscriptor.
- Apple Ads con el nombre del competidor.
