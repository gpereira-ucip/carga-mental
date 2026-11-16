# Carga Mental: reglas para trabajar en esta carpeta

App PWA de la familia de Gonzalo Gabriel Pereira para repartir compras, tareas del hogar y cuidado de Joaco.
Se publica en https://gpereira-ucip.github.io/carga-mental/ (repo propio gpereira-ucip/carga-mental, rama main; hasta el 10/11/2026 vivía en una carpeta de picu-pocket).

## Personas (siempre con nombre y rol)
- Gonzalo: papá. Pediatra intensivista con guardias de lunes 16 h a martes 9 h y de jueves 20 h a viernes 20 h, a veces el martes de noche. Pádel los martes a la tarde, tenis los jueves a la mañana, gimnasio variable.
- Dani: mamá; es Daniela, la esposa. Médica, trabaja 3 días desde casa y 2 en la oficina (casi siempre jueves, más lunes o miércoles y a veces viernes). Posgrado de psiquiatría los lunes y miércoles a la tarde.
- Daniela: empleada de limpieza. Viene 1 vez por semana, a veces 2.
- Joaco: hijo; es Joaquín, de 10 años.
- Abuelos: buscan a Joaco los lunes a la tarde.
- Los tres usan Android.

## Reglas técnicas
- La app es `index.html` (un solo archivo con CSS y JS), más `manifest.json`, `sw.js`, `icon-192.png`, `icon-512.png` y `cover.jpg`. Nada de frameworks ni pasos de build.
- Los datos viven en localStorage y, si está configurado, en Firebase Firestore (`hogares/{codigo}/{coleccion}`). **Nunca se pueden perder datos**: todo cambio de modelo lleva una migración.
- Cada versión nueva:
  1. Subir `VERSION` en `index.html` (semver).
  2. Cambiar `CACHE` en `sw.js`.
  3. Agregar una entrada en `CHANGELOG.md` y en la lista de novedades dentro de la app (cuando exista).
  4. Tildar los ítems de `BACKLOG.md` con la fecha y la versión.
- Probar con `python3 tests/smoke.py`, que tiene que dar OK. Mirar las capturas `/tmp/cm-*.png` antes de publicar.
- Textos en español rioplatense, amables y sin reproches.
- Este repo es solo de Carga Mental. No tocar otros repos (picu-pocket, Arucip, Child, etc.).
- Commits en `main` con el mensaje `Carga Mental vX.Y.Z: <resumen>`.

## Publicación (14/11/2026)
- GitHub Pages se publica desde la rama gh-pages. `.github/workflows/publicar.yml` copia main a gh-pages en cada push: no lo borres ni toques gh-pages a mano.

## Estética (desde v1.9.0, 14/11/2026, pedido de Gonzalo)
- Paleta azul marino (#24476b), sin marrón ni crema. Letra Poppins (carpeta fonts/). Ícono y portada: el camión con el cerebro sobre blanco, sin bandera. Esto manda sobre cualquier instrucción vieja que hable de «arcilla, crema y marrón».
