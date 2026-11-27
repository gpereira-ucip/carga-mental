# Novedades de Carga Mental

## v1.29.0 — 2026-11-27
- Ítem 46 del plan: subtareas. Las tareas que se repiten y las de una sola vez tienen debajo un botón «＋ Subtareas» que abre una hoja para armar los pasos (con Enter o «Agregar paso»; «✕» quita uno). Los pasos se ven en la lista como círculos que se tildan con un toque, y el botón pasa a «Editar subtareas · 2/3». Al tildar el último paso aparece un aviso con confeti para tocar «Hecho» (no se cierra sola). En las tareas que se repiten, «Hecho» destilda los pasos para la próxima vuelta.
- Estructura de datos: sin migración (SCHEMA sigue en 7). `subs` ([{id, text, done}]) es un campo opcional de la tarea; si falta, la tarea es como antes.
- Pruebas: datos intactos al abrir, rechazo de pasos vacíos, alta con Enter, pasos en Casa, tildar, aviso de «todos listos», reinicio con «Hecho», quitar, botones ≥ 44 px, datos ajenos intactos y 390 px en claro y oscuro. Pruebas viejas adaptadas a 46/100.

## v1.28.0 — 2026-11-27
- Pedido de Gonzalo (27/11): mejorar la estética y que la app sea más intuitiva, con mejores botones. Jerarquía clara: «Hecho» es un botón azul lleno con tilde ✓ (acción principal); los botones comunes son pastillas tonales; «+ Nueva tarea» y «+ Tarea de una vez» ocupan todo el ancho con borde punteado; «✕» es un botón redondo discreto que se pone rojo al pasar; «Cancelar» es un botón liso. Todos se hunden un poco al tocarlos (se desactiva si el sistema pide menos movimiento). En las hojas, «Guardar»/«Crear» son más grandes y quedan fijos abajo aunque haya que desplazarse.
- Estructura de datos: sin cambios (solo estilos y clases).
- Pruebas: «Hecho» con clase `ok` y tilde, botón de agregar a todo el ancho, botones de la hoja fijos y ≥ 44 px, 390 px sin desborde. Todas las pruebas anteriores siguen en OK.

## v1.27.0 — 2026-11-27
- Ítem 45 del plan: tareas de una sola vez con fecha límite. Al crear una tarea hay un tipo nuevo, «Una sola vez (con fecha límite)», con fecha opcional. En Casa aparecen en «Para hacer una vez», ordenadas por fecha (las sin fecha al final) con «vence en 2 días», «vence hoy» o «venció hace 1 día»; las hechas quedan en un desplegable «Hechas» (las últimas 10). Tocar el nombre abre una hoja para cambiar texto y fecha; «Hecho» las cierra (con «Deshacer») y «✕» las borra (con «Deshacer», sin cartel de confirmación). En Hoy y en el numerito de Casa aparecen solo cuando faltan 3 días o menos, o ya venció; las sin fecha no molestan en Hoy.
- Estructura de datos: sin migración (SCHEMA sigue en 7). Es un tipo nuevo de tarea (`kind: 'once'`, con `due` opcional y `done` / `doneBy`); las tareas existentes no se tocan.
- Pruebas: datos intactos al abrir, alta con y sin fecha, textos de vencimiento, orden, qué aparece en Hoy, hecho y deshacer, edición, borrado, botones ≥ 44 px, datos ajenos intactos, persistencia al recargar y 390 px en claro y oscuro. Pruebas viejas adaptadas a 45/100.

## v1.26.0 — 2026-11-27
- Ítem 44 del plan: tareas que se repiten en días fijos de la semana (por ejemplo lunes, miércoles y viernes). Al crear una tarea hay un tipo nuevo «Se repite en días fijos de la semana» con siete botones de día; en Casa se ve «lunes, miércoles y viernes» en vez de «cada X días». Esos días la tarea figura como «toca» (en Casa, en Hoy y en el numerito de Casa) y, si queda sin hacer, sigue pendiente hasta que alguien toque «Hecho». Tocando el nombre de cualquier tarea que se repite se abre una hoja para pasarla a días fijos o volver a «cada X días» (con «Deshacer»).
- Estructura de datos: sin migración (SCHEMA sigue en 7). `days` ([0-6], 0 = domingo) es un campo opcional de la tarea; si falta, la tarea funciona exactamente como antes.
- Pruebas: datos intactos al abrir, lógica de «toca» con fechas simuladas (hoy toca, ya hecha, olvidada de un día anterior, hoy no toca, tarea de siempre), texto de días, alta con y sin días elegidos, edición en ambos sentidos, botones ≥ 44 px, datos ajenos intactos y 390 px en claro y oscuro. Pruebas viejas adaptadas a 44/100.

## v1.25.0 — 2026-11-27
- Pedido de Gonzalo: «Ropa de la semana» de Joaco. En la pestaña Joaco, arriba de la mochila, hay un dibujo de lunes a viernes con la ropa de cada día: gimnasia (remera amarilla, pantalón bordó, zapatillas blancas) o uniforme de calle (chomba crema con cuello bordó, pantalón gris, zapatillas negras). Tocar un día cambia entre gimnasia y uniforme, con «Deshacer». «Editar» permite cambiar nombres, prendas, colores, chomba o remera y las fechas de inicio y fin de clases, para el año que viene. En Hoy aparece «Ropa de mañana» cuando mañana hay clases (no en fin de semana, feriado ni fuera de las fechas de clases).
- Estructura de datos: sin migración (SCHEMA sigue en 7). El documento `checks.uniforme` se crea recién al editar; mientras no existe se usan los valores de fábrica, así que no se toca ningún dato guardado.
- Pruebas: datos intactos al abrir, dibujo de la semana en Joaco, cambio de un día, Hoy con la ropa de mañana y 390 px en claro y oscuro.

## v1.24.0 — 2026-11-27
- Ítem 43 del plan: la ropa de Joaco va aparte. En Casa, dentro de «Tareas diarias», hay una tarea nueva «Ropa de Joaco» (🎽) con tres etapas: Uniforme, Educación física y En la mochila, para dejar todo listo para el día. En Hoy aparece qué falta apenas se empieza (y suma al numerito de Casa). Cada etapa lleva quién y cuándo, festejo al cerrar el ciclo y «Deshacer». Se puede borrar como cualquier tarea propia.
- Estructura de datos: SCHEMA pasa a 7. La migración 7 solo suma la tarea `t_ropajoaco` (una sola vez, marca `checks.m7`, que viaja a la nube; si se borra, no revive) y antes guarda la copia `cm_backup_v6`. No toca nada más.
- Pruebas: migración desde el esquema 6 con copia idéntica y datos intactos, la tarea en Casa y en Hoy, etapas independientes de la ropa del lavarropas, cierre del ciclo, que no reviva al borrarla y 390 px en claro y oscuro. Pruebas viejas adaptadas al esquema 7 y a 43/100.

## v1.23.0 — 2026-11-26
- Ítem 42 del plan: la ropa admite varias cargas a la vez. En Casa, la tarea «Ropa (lavarropas)» tiene «+ Otra carga»: cada carga extra tiene sus propias etapas (Lavar, Colgar, Doblar, Guardar), se completa por separado (con festejo y «Deshacer») y se puede quitar. En Hoy aparece qué falta de cada carga y el numerito de Casa las cuenta. La carga 1 sigue siendo la de siempre.
- Estructura de datos: sin cambios (SCHEMA sigue en 6, sin migración): `more` ([{id, cur}]) es un campo opcional de la tarea; si falta, hay una sola carga como antes.
- Pruebas: datos intactos al abrir, sumar cargas, etapas independientes, Hoy, completar una carga sin tocar la otra, quitar y deshacer, y 390 px en claro y oscuro.

## v1.22.0 — 2026-11-24
- Ítem 41 del plan: en Hoy hay una tarjeta «Lavavajillas» con el estado según las etapas ya marcadas: «Vacío y guardado», «Cargando: falta encenderlo» o «Limpio, falta guardar», más un botón para marcar la etapa que sigue (si no hay ciclo en curso muestra cuándo fue el último). La tarjeta se oculta si la tarea del lavavajillas no existe.
- Estructura de datos: sin cambios (SCHEMA sigue en 6, sin migración): se calcula con los datos que ya tiene la tarea.
- Pruebas: los tres estados, el botón avanza y cierra el ciclo, datos intactos y 390 px en claro y oscuro.

## v1.21.0 — 2026-11-23
- Ítem 40 del plan: nota de calidad y dónde comprarlo. Al editar un producto hay dos campos opcionales: «Nota de calidad» (por ejemplo «gallinas alimentadas a maíz, yema bien naranja») y «Dónde comprarlo» (por ejemplo «el naturista de la esquina»). Se ven en la lista de compras con ⭐ y 📍, el buscador los encuentra (y los muestra en los resultados) y la nota de calidad viaja entre corchetes en el mensaje al negocio. Los huevos de un hogar nuevo arrancan con «Gallinas alimentadas a maíz»; a los hogares existentes no se les cambia nada: cada uno la carga cuando quiera.
- Estructura de datos: sin cambios (SCHEMA sigue en 6, sin migración): `qual` y `where` son campos opcionales del producto; si faltan o se vacían, el producto se ve igual que antes.
- Pruebas: datos intactos al abrir, sin migración nueva, guardar y quitar calidad/lugar, que se vean en la lista y en el buscador, que viajen en el mensaje, el huevo de arranque y 390 px en claro y oscuro. Pruebas viejas adaptadas a 40/100.

## v1.20.1 — 2026-11-22
- Pedido de Gonzalo: los turnos médicos («Sacar turno…», «Turno … el día…») salen de «Te toca» en Hoy y del numerito de la pestaña Joaco; siguen en el desplegable «Turnos médicos», que muestra cuántos hay para revisar.
- Estructura de datos: sin cambios.

## v1.20.0 — 2026-11-22
- Pedido de Gonzalo (22/11), fuera del plan de 100 mejoras:
  - Casa reordenada en «Tareas diarias» (lavavajillas, ropa con lavarropas, sacar la basura), «Orden de la casa» (orden de la cocina y orden de las habitaciones, separados) y «Otras tareas que se repiten». Las tareas nuevas eligen sección.
  - Sale «Fertilizar el limonero» (nadie la hace).
  - «Turnos médicos y odontología de Joaco» sale de «Quién se encarga de qué» y pasa a un desplegable «Turnos médicos» en la pestaña Joaco, con todos los controles y quién se encarga. Se suma Fonoaudiología (frecuencia según indicación).
  - Calendario de feriados (pestaña Joaco): mes con los feriados marcados, próximo feriado y aviso en Hoy el día anterior. Regla de Gonzalo: si el feriado cae en su día de guardia lo trabaja, y si cae lunes es guardia de 24 h. Ese día la semana de Joaco muestra «Feriado» en lugar de lleva/busca. Fuente: calendario oficial 2026 (Ley 27.399, Res. 164/2025); 2027 solo con los inamovibles, falta sumar trasladables y no laborables cuando se publiquen.
  - Estética: encabezado con degradé y bordes redondeados, tarjetas sin borde con sombra suave, títulos con ícono, botones redondeados, barra inferior flotante.
- Estructura de datos: SCHEMA 6 con migración (copia previa en cm_backup_v5). Agrega `grp` a las tareas, borra `t_fert`, renombra «Orden general» y «Ropa» solo si conservan el nombre original, y suma «Orden de las habitaciones», «Sacar la basura» y Fonoaudiología. Corre una sola vez por hogar (marca `checks.m6`, que viaja a la nube).

## v1.19.0 — 2026-11-22
- Marca o variedad preferida y foto (ítem 39): al editar un producto hay un campo «Marca o variedad preferida» y una foto opcional («📷 Agregar foto», con cámara o galería; se achica sola a 160 px y JPEG, unos pocos KB). La marca se ve junto al nombre en las listas, la encuentra el buscador y viaja en el mensaje al negocio («Leche — La Serenísima entera: 2 L»); la foto aparece como miniatura en la lista de compras. «Quitar foto» la borra. El campo «Detalle» sigue existiendo para presentación o comentarios.
- Estructura de datos: sin cambios (SCHEMA sigue en 5, sin migración): `brand` y `photo` son campos opcionales del producto; si faltan, el producto se ve igual que antes.
- Pruebas: datos intactos al abrir, guardar marca y foto (JPEG liviano), vista previa, miniatura ≥ 44 px y marca en la lista, búsqueda por marca, marca en el mensaje, quitar foto y marca, botones ≥ 44 px y 390 px en claro y oscuro. Pruebas viejas adaptadas a 39/100.

## v1.18.0 — 2026-11-21
- Compartir de más formas (ítem 38): «📲 Mandar lista» de cada negocio y «Mandar indicaciones» a Daniela abren una hoja con el mensaje y tres botones: «WhatsApp» (igual que antes, directo a quien corresponde), «Compartir…» (menú nativo de Android vía Web Share; solo aparece si el navegador lo permite) y «Copiar texto» (portapapeles, con respaldo para navegadores viejos). Cancelar el menú nativo no da error.
- Estructura de datos: sin cambios (SCHEMA sigue en 5, sin migración).
- Pruebas: la hoja muestra el texto, WhatsApp abre wa.me con el mensaje, Compartir… llama a navigator.share con el mismo texto, Copiar deja el texto en el portapapeles, sin Web Share no aparece el botón, indicaciones a Daniela, botones ≥ 44 px y 390 px en claro y oscuro.

## v1.17.0 — 2026-11-20
- Snacks de Joaco (ítem 37): en la pestaña Joaco, tarjeta «🍎 Snacks de la semana» con el snack de lunes a viernes. «Armar rotación» reparte las opciones en orden para que no se repita el mismo dos días seguidos, y la próxima vez sigue desde donde quedó (también entre semanas). Tocar un día permite elegir de la lista, escribir otro o dejarlo sin elegir; «Opciones» edita la lista (sin repetidas). Todo lleva «Deshacer». Las opciones de arranque (fruta, yogur, frutos secos, galletitas de arroz, barrita de cereal) son ideas comunes y se cambian a gusto; no son indicaciones médicas.
- Estructura de datos: sin cambios (SCHEMA sigue en 5, sin migración): `checks.snacks` ({opts, plan, cur}) es un documento opcional que recién se crea al usar la tarjeta; si falta, se leen las opciones por defecto.
- Pruebas: datos intactos al abrir, sin documento hasta usarlo, rotación sin repetidos seguidos y continuidad entre semanas, deshacer, validación de lista vacía y duplicados, elegir/escribir/vaciar un día, botón ≥ 44 px y 390 px en claro y oscuro. Pruebas viejas adaptadas a 37/100.

## v1.16.0 — 2026-11-20
- Ideas y antojos (ítem 36): al final de Compras (con el filtro «Todos») hay una tarjeta «💡 Ideas y antojos» para lo que no es urgente. Se anota con el campito y «Sumar» (o Enter); tocar una idea la edita; «A la lista» abre una hoja para elegir el negocio y la pasa a la lista de compras (si el producto ya existe ahí, lo reutiliza); «✕» la borra. Todo lleva «Deshacer». Las ideas no cuentan como pendientes ni aparecen en «Hoy».
- Estructura de datos: SCHEMA pasa a 5. La migración 5 solo agrega la colección `ideas` (vacía) y antes guarda la copia `cm_backup_v4`; no toca productos, negocios ni plantillas. Se sincroniza con la nube como las demás colecciones.
- Pruebas: migración desde esquema 4 (solo se suma `ideas`, copia idéntica), tarjeta vacía, alta (con botón y con Enter, rechaza vacías), edición, pasar a la lista y su deshacer, borrar y deshacer, botón ≥ 44 px, ideas que no cuentan como pendientes y 390 px en claro y oscuro. Las pruebas viejas se adaptaron al esquema 5 y a 36/100.

## v1.15.0 — 2026-11-19
- «No había» (ítem 35): en la lista de cada negocio, cada producto tiene «🚫 No había». Se abre una hoja para dejar una nota opcional («tenían solo el grande») y, si se quiere, pasar el producto a otro negocio para reintentar ahí (queda en la lista del nuevo negocio). El producto muestra «No había en <negocio> (fecha): nota» para que nadie lo busque de nuevo en el mismo lugar; «Quitar marca» la saca y todo lleva «Deshacer». Al comprarlo o sacarlo de la lista, la marca se limpia sola.
- Estructura de datos: sin cambios (SCHEMA sigue en 4, sin migración): `miss` ({at, by, from, note}) es un campo opcional del producto; si falta, no hubo faltante.
- Pruebas: datos intactos al abrir, lectura de `miss`, nota sin mover el producto, pasarlo a otro negocio, quitar la marca, limpieza al comprar, botón ≥ 44 px y 390 px en claro y oscuro.

## v1.14.0 — 2026-11-18
- «Lo traigo yo» (ítem 34): en la lista de cada negocio, cada producto tiene «🙋 Lo traigo». Queda «Lo trae Gonzalo/Dani» en el producto y a esa persona le aparece en «Hoy» (en «Te toca») «Lo traés vos: …». «Ya no» lo libera y «Cambiar» lo toma otra persona. Si quien toca es Daniela u otra persona, se abre una hoja para elegir quién lo trae. Al comprarlo o sacarlo de la lista, el responsable se limpia solo; lleva «Deshacer».
- Estructura de datos: sin cambios (SCHEMA sigue en 4, sin migración): `bring` es un campo opcional del producto; si falta, nadie lo trae.
- Pruebas: datos intactos al abrir, asignar, mostrar en Compras y en Hoy, liberar, cambiar, hoja para otros usuarios, limpieza al comprar y al sacar de la lista, botón ≥ 44 px y 390 px en claro y oscuro.


## v1.13.0 — 2026-11-17
- Día fijo de pedido (ítem 33): cada negocio tiene «📅 Día de pedido», con los siete días de la semana o «Sin día fijo». El negocio muestra «Se pide los domingos» y, el día anterior y el mismo día, aparece «Mañana/Hoy es el día de pedir en <negocio>» en «Hoy» (en «Te toca» de quien se encarga, con cuántos productos hay anotados) y una etiqueta en la tarjeta. No se cargó ningún día de fábrica: lo elige la familia.
- Estructura de datos: sin cambios (SCHEMA sigue en 4, sin migración): `orderDay` es un campo opcional del negocio (0 = domingo … 6 = sábado); si falta, no hay día fijo. Se sincroniza con el negocio.
- Pruebas: validación de `orderDay`, días que faltan, guardar, recordatorio de mañana y de hoy, que no aparezca fuera de fecha, quitar el día, chips ≥ 44 px y 390 px en claro y oscuro. Los recordatorios con la app cerrada quedan para el ítem 91/92.

## v1.12.1 — 2026-11-16
- Links a la web de cada negocio (ítem 32): en Compras, cada negocio muestra «🌐 Abrir web» (abre en otra pestaña) y «✎ Enlace» para cambiarlo o quitarlo; si no tiene, «🔗 Poner web». MercadoLibre trae por defecto https://www.mercadolibre.com.ar/. Pendiente de Gonzalo: cargar el enlace de Berardi y del súper desde la app (no se inventaron direcciones). Solo se aceptan enlaces http/https; se guarda en el negocio y se sincroniza.
- Estructura de datos: sin cambios (SCHEMA sigue en 4, sin migración): `url` es un campo opcional del negocio.
- Pruebas: datos intactos al abrir, validación de enlaces (rechaza javascript: y texto suelto), guardar, link con rel noopener y ≥ 44 px, quitar, valor por defecto de MercadoLibre y 390 px en claro y oscuro. Paleta azul marino y Poppins sin cambios.

## v1.12.0 — 2026-11-17
- Plantillas de pedido (ítem 31): cada negocio tiene el botón «📋 Plantillas» con pedidos armados de antemano. De fábrica: «Súper semanal» (los productos del súper que se reponen cada 7 días o menos), «MercadoLibre mensual» y «Berardi quincenal» (todos los productos de cada uno). «Armar pedido» pasa a la lista los productos de la plantilla que todavía no estaban, avisa cuántos anotó y tiene «Deshacer». Se pueden editar (nombre y productos), borrar (con «Deshacer»), crear nuevas y guardar la lista actual de un negocio como plantilla.
- Estructura de datos: SCHEMA pasa a 4. La migración 4 solo agrega la colección `tpls` (plantillas de fábrica armadas con los productos que ya existen); no toca productos ni negocios, y antes guarda la copia `cm_backup_v3`. Una plantilla borrada no reaparece al sincronizar. Se sincroniza con la nube como las demás colecciones.
- Pruebas: migración desde v1.11.0 (nada cambia salvo `tpls`, copia idéntica), plantillas de fábrica coherentes, armar pedido y su deshacer, crear desde la lista, validación de nombre (sin alterar la plantilla guardada), borrar y deshacer, que una borrada no reaparezca, y 390 px en claro y oscuro. Las pruebas viejas se adaptaron al esquema 4 y a 31/100.
## v1.11.0 — 2026-11-16
- Gasto mensual por negocio (ítem 30): al final de Compras (con el filtro «Todos») aparece «Gasto de <mes>» con el total y lo gastado en cada negocio, con barras proporcionales y de mayor a menor. Suma los precios guardados en el historial de compras (los que quedan al marcar algo como comprado con precio cargado). Las flechas ‹ › cambian de mes; si hubo compras sin precio, avisa cuántas no se suman.
- Estructura de datos: sin cambios (SCHEMA sigue en 3, sin migración); solo lee el historial existente.
- Pruebas: datos de v1.10.0 intactos, suma por negocio y mes (mes anterior, compras sin precio, otro año), tarjeta, navegación de meses y 390 px en claro y oscuro.

## v1.10.0 — 2026-11-15
- Precios y total estimado (ítem 29): cada producto tiene «Precio del último pedido» (para la cantidad indicada; acepta 1500, 1.500 o 1.234,50). En cada negocio, arriba de la lista, aparece «Total estimado: $X» con la suma de lo pendiente y, si faltan precios, «N de M con precio»; el mismo total se ve en el modo «Estoy en el negocio». Al marcar algo como comprado, el precio queda en su historial. En la lista, cada producto muestra su precio.
- Estructura de datos: sin cambios (SCHEMA sigue en 3, sin migración): `price` es un campo opcional que, si falta, se lee como «sin precio». Los datos guardados no se tocan.
- Pruebas: datos de v1.9.1 intactos al abrir, lectura de precios (con puntos y coma) y formato de pesos, total parcial y completo, total en modo negocio, precio en el historial y su deshacer, borrar el precio, y 390 px en claro y oscuro.
## v1.9.1 — 2026-11-14
- Sombra de la barra inferior sin tono marrón.

## v1.9.0 — 2026-11-14
- Portada nueva (pedido de Gonzalo): el camión sin bandera sobre fondo blanco, como el ícono; el título va como texto.
- Paleta sin marrón: azul marino (#24476b) en claro y oscuro. Tipografía Poppins incluida en la app (carpeta fonts/, solo letras latinas) para que funcione sin conexión.
- Teléfonos para WhatsApp en ⚙ Ajustes (solo en el dispositivo; nunca en el repo). La lista de un comercio se manda directo al responsable y las indicaciones a Daniela. También se pueden cargar con un enlace `#tel=`.

## v1.8.2 — 2026-11-14
- Ícono más nítido (pedido de Gonzalo): sin restos del palo ni de la bandera, fondo blanco limpio y mejor definición.

## v1.8.1 — 2026-11-14
- Ícono nuevo (pedido de Gonzalo): el camión con el cerebro sobre fondo blanco, sin la bandera blanca. Se sacó el ícono «maskable» para que Android no lo recorte.

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
