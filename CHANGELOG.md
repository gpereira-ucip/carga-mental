# Novedades de Carga Mental

## v1.8.0 — 2026-11-14
- Modo «Estoy en el negocio» (ítem 28): cada negocio con pendientes tiene el botón «🛒 Estoy en el negocio», que abre una hoja con letra grande, solo con lo que falta comprar (agrupado por categoría si hay varias) y un contador «Faltan N de M». Tocar un producto lo tacha (y vuelve a tocar para destacharlo); «Terminé» registra como comprados los tachados —con historial, frecuencia aprendida, confeti si no queda nada y «Deshacer»— y deja el resto en la lista. «Seguir después» cierra sin perder lo tachado.
- Lo tachado se guarda en el teléfono (`cm_shop`) hasta tocar «Terminé», por si se cierra la app a mitad de compra; no cambia los datos de la familia: SCHEMA sigue en 3, sin migración.
- Pruebas: datos de v1.7.0 intactos, pendientes mostrados, letra y filas ≥ 44 px, tachado y contador, persistencia tras recargar, destachar, «Terminé» (solo tachados, historial) y su deshacer, 390 px en claro y oscuro. Se actualizó 28/100 en pruebas anteriores.

## v1.7.0 — 2026-11-13
- Aviso anticipado (ítem 27): en Compras, cada negocio muestra arriba «Por acabarse» con los productos al día que, según su «cada X días» y la última compra, se terminan en 2 días o menos («se acaba mañana», «se acaba en 2 días»). El botón «Anotar» los pasa a la lista antes de que falten, con «Deshacer». En «Habituales» esos productos llevan la misma etiqueta.
- Solo se avisa de productos que se reponen cada 4 días o más (con frecuencias más cortas estarían siempre «por acabarse»). No toca ningún dato: no cambia SCHEMA (sigue en 3) ni hay migración.
- Pruebas: cálculo de días restantes (límites, lista, sin compra, frecuencia corta), tarjeta y etiqueta, «Anotar» y su deshacer, y 390 px en claro y oscuro. Se actualizó el texto 27/100 de las pruebas anteriores.

## v1.6.0 — 2026-11-12
- Frecuencia aprendida (ítem 26): al registrar una compra, la app promedia los intervalos reales entre las últimas compras del producto (hasta 6 intervalos; hacen falta al menos 3 compras; las del mismo día cuentan una sola vez) y ajusta sola el «cada X días». Cuando lo cambia avisa en el mismo cartel («Agua: ahora cada 5 días (antes 7)») y «Deshacer» devuelve también la frecuencia. «Compré todo» cuenta cuántos productos se ajustaron.
- En el formulario del producto: opción «Que se ajuste solo con las compras reales» (tildada de fábrica), el promedio calculado («Según las últimas 4 compras, lo reponen cada 5 días») y un botón «Usar X días» si difiere. Escribir el número a mano destilda la opción y lo deja fijo. En «Habituales», los productos cuya frecuencia viene del promedio llevan la etiqueta «aprendido».
- Estructura de datos: SCHEMA pasa a 3. La migración 3 solo agrega `auto: true` a cada producto (no cambia ninguna frecuencia: recién se ajusta con la próxima compra); antes guarda la copia `cm_backup_v2`. Un producto sin el campo (de un teléfono con versión vieja) se trata como `auto` prendido.
- El cartel de aviso ahora usa todo el ancho disponible cuando el texto es largo.
- Pruebas: migración desde v1.5.0 (nada cambia salvo `auto`, copia idéntica), cálculo del promedio (pocas compras, mismo día, tope de 6 intervalos, mínimo 1 día), ajuste con aviso y deshacer, producto fijo que no se toca, formulario, «Compré todo» y 390 px en claro y oscuro.

## v1.5.0 — 2026-11-11
- Cantidad y unidad por producto (ítem 21): en el formulario del producto hay «Cantidad» (acepta coma: 1,5) y «Unidad» (unidades, kg, g, L, ml, docenas, paquetes, cajas, botellas, latas, bolsas, rollos, atados). Se muestra al lado del nombre («Agua · 6 L»), en el buscador y en la lista que se manda por WhatsApp («• Agua: 6 L»). El campo «Detalle» queda para marca o variedad; las notas que ya estaban no se tocan.
- Categorías dentro de cada negocio (ítem 22): frescos, almacén, bebidas, limpieza, papeles y otros. La app la elige sola según el nombre (se puede cambiar en el formulario) y agrupa con un título cada categoría, tanto en la lista como en «Habituales»; si un negocio tiene una sola categoría no muestra títulos.
- Buscador con alta rápida (ítem 23): arriba de Compras, busca en todos los negocios sin importar mayúsculas ni acentos (también en el detalle), sin redibujar la pantalla para no perder el teclado. Cada resultado tiene «Se acaba» o avisa que ya está en la lista; si no existe, ofrece anotarlo como producto nuevo en el negocio que elijas (Enter lo anota en el negocio filtrado o en el súper). Con «Deshacer».
- Anotar por voz (ítem 24): botón de micrófono al lado del buscador. Usa el reconocimiento de voz del navegador (es-AR) y entiende frases como «leche, dos kilos de tomate y papel higiénico», «un kilo y medio de carne» o «media docena de huevos»: separa productos, cantidades y unidades, reconoce los que ya existen y muestra una revisión para destildar antes de anotar. Si el navegador no escucha, se puede dictar con el micrófono del teclado en el mismo cuadro. Con «Deshacer».
- Historial de compras por producto (ítem 25): cada compra (tilde o «Compré todo») guarda quién, cuándo y cuánto, hasta 30 por producto; se ve en «Historial de compras» dentro del producto. «Deshacer» también saca la compra del historial.
- Estructura de datos: SCHEMA pasa a 2. La migración 2 agrega a cada producto `cat`, `qty`, `unit` e `hist` (si había una última compra, queda como primer renglón del historial) sin tocar nada más; antes guarda la copia `cm_backup_v1`. Los datos que bajan de la nube o de una copia vieja se completan igual.
- Pruebas: migración desde v1.4.0 (nada cambia salvo los campos nuevos, copia idéntica), categorías de los productos de fábrica, formulario de cantidad, historial y su deshacer, buscador (foco, acentos, Enter, alta rápida), 8 frases dictadas, flujo de voz con reconocimiento simulado y sin él, accesibilidad de las pantallas nuevas en claro, oscuro y letra grande, y 390 px.

## v1.4.0 — 2026-11-10
- Accesibilidad (ítem 16): todos los botones, chips, tildes y campos miden al menos 44 px; las tildes de compras e indicaciones tienen un área de toque de 44×44 (`.chk`); la manija de las hojas también. Cada botón, campo y fila tocable tiene nombre para lectores de pantalla (p. ej. «Comprado: Agua», «Sacar Agua de la lista») y las filas que se tocan se pueden usar con teclado (`role=button`, Enter/Espacio). Las hojas reciben el foco al abrirse, se nombran con su título y devuelven el foco al cerrarse; las etiquetas de los formularios quedan asociadas a su campo. Nuevo «Tamaño de letra: Normal / Grande» en ⚙ Ajustes → Apariencia (`cm_big`, se aplica antes de pintar). Contraste AA verificado en más pares (etiquetas sobre arcilla, globito rojo, botón de Dani, avatares) en claro y oscuro.
- Deshacer (ítem 17): los avisos de anotar, comprar, «Compré todo», pedido habitual, sacar de la lista, tareas hechas, ciclos completos, mochila, indicaciones hechas/borradas/limpiadas y borrados de productos, tareas y controles traen «Deshacer» durante 6,5 s. Restaura el estado anterior (también en la nube) y saca el movimiento de «Últimos movimientos».
- Botón «+» flotante (ítem 18): en Hoy abre «¿Qué querés sumar?» (compra, tarea, control de salud, mensaje); en Compras anota un producto en el negocio elegido; en Casa crea una tarea; en Joaco carga un control de salud. No aparece en Mensajes ni en la vista de Daniela.
- Anillos de progreso (ítem 19): en Hoy, «Cómo va el día» con compras (compradas hoy / pendientes), tareas que se repiten (hechas hoy / que tocan) y mochila de Joaco; se animan al entrar a la pestaña y se pintan en verde al completarse.
- Textos (ítem 20): revisión de mensajes de error y estados para que suenen amables y sin reproches («Ese archivo no parece una copia de Carga Mental», «ya pasó el turno: cargá el nuevo», «No se pudo sincronizar por ahora»…); el estado de sincronización y el permiso de avisos ya no muestran palabras en inglés.
- Sin cambios en la estructura de datos (SCHEMA sigue en 1); una clave nueva de preferencias del teléfono (`cm_big`).
- Pruebas: datos de v1.3.0 intactos, auditoría de 44 px / nombres / teclado en todas las pestañas y hojas (claro, oscuro y letra grande), deshacer de cada acción, botón + por pestaña, anillos, foco de las hojas y letra grande en las 5 pestañas a 390 px.

## v1.3.0 — 2026-11-10
- Barra inferior (ítem 11): indicador tipo píldora que se desliza a la pestaña activa y globitos con la cantidad de pendientes por sección (Hoy: lo tuyo; Compras: productos en lista o vencidos; Casa: tareas que tocan o ciclos empezados; Joaco: mochila incompleta y controles por vencer; Mensajes: sin leer, con `cm_read`; Daniela: indicaciones pendientes). Lectores de pantalla leen «, N pendientes».
- Tilde animada y festejo (ítem 12): la tilde/etapa/fila recién marcada hace un salto con brillo; papelitos de confeti al completar un ciclo, la mochila, la lista de un negocio («Compré todo» o el último producto) y todas las indicaciones de Daniela. Respeta «reducir movimiento» del teléfono.
- Vibración corta (ítem 13): 15 ms al marcar, patrón corto al festejar; se apaga en ⚙ Ajustes → Apariencia (`cm_vib`).
- Hojas modales (ítem 14): entran deslizando, tienen manija arriba y se cierran tirando hacia abajo (si están arriba de todo) o con Escape; no se arrastra desde campos de texto.
- Estados vacíos ilustrados (ítem 15) en Te toca, Últimos movimientos, cada negocio, tareas que se repiten, indicaciones y comidas de Daniela, salud de Joaco y mensajes.
- Sin cambios en la estructura de datos (SCHEMA sigue en 1); solo dos claves nuevas de preferencias del teléfono.
- Pruebas: globitos, indicador, mensajes sin leer, confeti, vibración, cerrar la hoja deslizando (toques reales por CDP), estados vacíos y migración desde v1.2.0.

## v1.2.0 — 2026-11-09
- Sistema de diseño (ítem 6): tokens de color en tono arcilla, espacios (`--s1…--s6`), radios (`--r1…--r4`) y sombras (`--sh1`, `--sh2`); ya no quedan colores sueltos en la interfaz.
- Tipografía (ítem 7): pila del sistema (Roboto en Android), escala `--fs-xs…--fs-2xl`, pesos y títulos con jerarquía; números tabulares en contadores.
- Íconos SVG propios (ítem 8) en la barra inferior, el botón de ajustes y los títulos de cada sección (los íconos de negocios y tareas siguen siendo los que eligió la familia).
- Avatares (ítem 9): círculo con inicial y color por persona (G, D, Da, J, Ab; «Ambos» = G+D superpuestos) en Hoy, Compras, Casa, la semana de Joaco, mensajes y ajustes.
- Modo oscuro (ítem 10): automático según el teléfono y manual en ⚙ Ajustes → Apariencia; se aplica antes de pintar (sin parpadeo) y cambia el color de la barra del teléfono.
- Pruebas: contraste AA (4.5:1) de los pares de colores principales en claro y oscuro, íconos, avatares y tema manual.

## v1.1.0 — 2026-11-09
- Pantalla «Novedades y progreso» (ítem 1): versión, cambios de cada día y barra X/100; se abre sola la primera vez que se entra a una versión nueva. Acceso desde Hoy, Ajustes y la vista de Daniela.
- Pruebas automáticas ampliadas (ítem 2): usuario nuevo, compras, etapas, tareas que se repiten, indicaciones, mochila, mensajes, ajustes, atajos, vista de Daniela, migración, importación, errores de consola y ancho de 390 px.
- Migraciones de datos versionadas (ítem 3): `SCHEMA` + `MIGRATIONS`; antes de migrar se guarda copia en `cm_backup_v{n}`; también se migran las copias importadas y se completan campos al bajar de la nube.
- Botón «Instalar app» con `beforeinstallprompt` y guía para Android (ítem 4).
- Accesos directos del ícono (ítem 5): «Anotar compra», «Mensajes» y «Hoy» (`?go=…`); el service worker sirve la página guardada aunque la dirección tenga `?go=`.

## v1.0.0 — 2026-11-09
- Primera versión publicada: compras por negocio con alertas, tareas por etapas, semana de Joaco según las guardias, mochila, salud, indicaciones para Daniela y mensajes.
- Portada e ícono con el camión de la carga mental.
- Plan de 100 mejoras en BACKLOG.md.
