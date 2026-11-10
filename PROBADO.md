# Qué está comprobado

- 10/11/2026: el plugin `xcode` está en el marketplace oficial de Anthropic (`anthropics/claude-plugins-official`,
  `.claude-plugin/marketplace.json`, PR #6338 fusionado el 6/11/2026), autor «Apple Inc.», con fuente
  `xcrun agent plugin path --plugin-format claude`. Su descripción: compilar, ejecutar y probar esquemas, vistas
  previas de SwiftUI, simuladores y dispositivos, registros de compilación y documentación de Apple.
- 10/11/2026: el plan sale del hilo de Greg Isenberg del 8/11/2026 (x.com/gregisenberg/status/2119229734563271124).
- `scripts/app_store.py` probado en macOS con Python 3.9: ranking «top grossing» por categoría (máx. 100), ficha por la
  API de búsqueda de iTunes y reseñas por el feed RSS (50 por página, hasta 10 páginas por país).
- `scripts/comprobar.sh` probado en macOS.

## Sin probar todavía

- La instalación del plugin y el ciclo compilar → simulador → arreglar en un Mac con Xcode 27: el Mac donde se escribió
  la skill no tenía Xcode. Los comandos salen del marketplace oficial; el permiso que pide Xcode la primera vez, de un
  artículo de Classmethod sobre las skills de Xcode 27.
- Los filtros exactos de Appfigures (qué enseña el plan gratis) pueden cambiar.
