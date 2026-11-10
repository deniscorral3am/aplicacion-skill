# Aplicación · tu app para la App Store con Claude y el plugin oficial de Apple

Apple ya tiene un plugin oficial para Claude Code: Claude compila tu app en Xcode, la abre en el simulador, la prueba
y la arregla él solo. Esta skill lo junta con el plan de 5 pasos de Greg Isenberg para sacar una app que cobra.

| Paso | Qué hace |
|---|---|
| 1 | Busca apps que facturan mucho pero tienen menos de 3,5 estrellas (Appfigures o el ranking público de Apple) |
| 2 | Lee sus reseñas y te saca las 5 quejas que más se repiten. Si se quejan del precio pero pagan, hay demanda; si se quejan de fallos, ahí entras tú |
| 3 | Construye contigo la app en Xcode con el plugin de Apple, la prueba en el simulador y la arregla hasta que quede bien |
| 4 | Le monta la suscripción con el paywall justo después de resolverle el problema al usuario, nunca nada más instalar |
| 5 | Te deja los guiones de vídeo, quién los graba (tú, creadores o clones de IA) y cómo meterle dinero al que funcione |

Hecha por Denis Corral · [Sell Your AI](https://sellyourai.io)

## Instalación

```bash
git clone https://github.com/deniscorral3am/aplicacion-skill ~/.claude/skills/aplicacion
```

Abre Claude Code y escribe `/aplicacion`.

¿Sin instalar nada? Copia el prompt de [`PROMPT.md`](PROMPT.md) y pégalo en Claude Code.

## Qué necesitas

- Un **Mac** con la última versión de **Xcode** (gratis en la Mac App Store).
- [Claude Code](https://claude.com/claude-code) con tu cuenta de Claude.
- El plugin oficial de Apple, que se instala desde Claude Code: `/plugin install xcode@claude-plugins-official`.
- Opcional: cuenta de [Appfigures](https://appfigures.com) para ver ingresos estimados (sin ella, la skill usa el
  ranking público de Apple).
- Para **publicar** (no para construir ni probar): la cuenta de desarrollador de Apple, 99 €/año.

## Bueno saber

- El ranking público de Apple dice qué apps facturan más, no cuánto. Las cifras en euros son de Appfigures o Sensor
  Tower, y son estimaciones.
- La skill no copia la app de nadie: resuelve el mismo problema, mejor.
- El plan sale de este hilo de Greg Isenberg: x.com/gregisenberg/status/2119229734563271124

## Licencia

MIT
