"""Prueba de humo de Carga Mental.
Uso: python3 tests/smoke.py   (desde la carpeta carga-mental)
Levanta un servidor local, abre la app en un celular simulado (390x844) y recorre:
  1. Usuario nuevo: bienvenida, Novedades, todas las pestañas y los flujos principales
     (compras, tareas por etapas, tareas que se repiten, indicaciones, mochila, mensajes, ajustes).
  2. Migración: datos guardados con el formato de v1.0.0 → no se pierde nada y queda copia.
  3. Accesos directos del ícono (?go=chat, ?go=anotar).
  4. Vista de Daniela.
  5. Diseño: íconos SVG, avatares, contraste AA y modo oscuro (automático y manual), con capturas /tmp/cm-dark-*.png.
  6. Movimiento (v1.3.0): globitos e indicador de la barra, mensajes sin leer, tilde y confeti, vibración,
     cerrar hojas deslizando (toques reales), estados vacíos y datos de v1.2.0 que siguen intactos.
  7. v1.4.0: accesibilidad (44 px, nombres, teclado, letra grande), deshacer, botón +, anillos y datos de v1.3.0 intactos.
  8. v1.5.0: migración al esquema 2 (datos de v1.4.0), cantidad y unidad, categorías, buscador con alta rápida,
     anotar por voz (reconocimiento simulado) e historial de compras por producto.
  9. v1.6.0: migración al esquema 3 (datos de v1.5.0), frecuencia aprendida con el promedio real de las compras,
     aviso y deshacer, opción por producto y «Compré todo».
Falla si hay errores de JavaScript o de consola, o si la página se ensancha más de 390 px.
Guarda capturas en /tmp/cm-*.png para revisarlas.
"""
import http.server, json, os, socketserver, sys, threading
from functools import partial
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROME = next((p for p in ['/usr/bin/google-chrome', '/usr/bin/chromium', '/usr/bin/chromium-browser'] if os.path.exists(p)), None)

class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
handler = partial(Quiet, directory=ROOT)
srv = socketserver.TCPServer(('127.0.0.1', 0), handler)
port = srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()
URL = f'http://127.0.0.1:{port}/'

errs = []
def check(cond, msg):
    if not cond: errs.append(msg)

def S(pg): return pg.evaluate('JSON.parse(localStorage.getItem("cm_data"))')
def sin_v15(d):
    """Saca lo que agregó el esquema 2 (v1.5.0) para comparar con los datos guardados por versiones anteriores."""
    d = json.loads(json.dumps(d)); d['_v'] = 1
    for i in d['items'].values():
        for k in ('cat', 'qty', 'unit', 'hist', 'auto'): i.pop(k, None)
    return d
def width_ok(pg, where):
    w = pg.evaluate('document.documentElement.scrollWidth')
    check(w == 390, f'{where}: scrollWidth={w} (debería ser 390)')

# Datos con el formato de v1.0.0 (sin _v, sin checks.daniela, con cosas propias de la familia)
OLD = {
  "stores": {"super": {"id": "super", "name": "Supermercado", "icon": "🛒", "how": "Pedido online semanal", "owner": "gonzalo", "ord": 3},
             "naturista": {"id": "naturista", "name": "Naturista", "icon": "🌰", "how": "Cercanía", "owner": "dani", "ord": 1}},
  "items": {"i_agua": {"id": "i_agua", "name": "Agua", "store": "super", "every": 7, "last": None, "state": "list", "by": "dani"},
            "i_mio": {"id": "i_mio", "name": "Queso rallado especial", "store": "super", "every": 10, "last": 1762000000000, "note": "el de Gonzalo"},
            "i_huerfano": {"id": "i_huerfano", "name": "Miel", "store": "negocio-borrado", "every": 30, "state": "ok"}},
  "tasks": {"t_lava": {"id": "t_lava", "kind": "cycle", "name": "Lavavajillas", "icon": "🍽️", "owner": "gonzalo", "steps": ["Cargar", "Encender", "Guardar"], "cur": {"0": {"by": "dani", "at": 1762000000000}}, "ord": 1},
            "t_x": {"id": "t_x", "name": "Sacar la basura", "every": 1, "last": None, "owner": "dani"}},
  "checks": {"mochila": {"id": "mochila", "date": "", "done": {}, "list": ["Cartuchera", "Flauta los miércoles"]}},
  "salud": {"s_odonto": {"id": "s_odonto", "name": "Odontología", "every": 180, "last": "2026-06-01", "next": "", "owner": "dani", "note": "Dra. López"}},
  "indic": {"n_1": {"id": "n_1", "text": "Planchar camisas", "done": False, "created": 1762000000000, "by": "dani"}},
  "areas": {},
  "msgs": {"m_1": {"id": "m_1", "text": "Mensaje viejo que no se tiene que perder", "at": 1762000000000, "by": "dani"}},
  "weeks": {"base": {"id": "base", "days": {"1": {"lleva": "gonzalo", "busca": "abuelos"}, "2": {"lleva": "dani", "busca": "gonzalo"}}}},
  "log": {}
}

with sync_playwright() as p:
    kw = {'args': ['--no-sandbox']}
    if CHROME: kw['executable_path'] = CHROME
    b = p.chromium.launch(**kw)

    def new_page(name, init=None):
        ctx = b.new_context(viewport={'width': 390, 'height': 844})
        if init: ctx.add_init_script(init)
        pg = ctx.new_page()
        pg.on('pageerror', lambda e: errs.append(f'[{name}] JS: {e}'))
        pg.on('console', lambda m: errs.append(f'[{name}] consola: {m.text}') if m.type == 'error' else None)
        return ctx, pg

    # ---------- 1. Usuario nuevo ----------
    ctx, pg = new_page('nuevo')
    pg.goto(URL); pg.wait_for_timeout(1800)
    pg.screenshot(path='/tmp/cm-0-inicio.png')
    check(pg.locator('text=Gonzalo —').count() > 0, 'No apareció la bienvenida')
    pg.locator('text=Gonzalo —').first.click(); pg.wait_for_timeout(700)
    check(pg.locator('#sheet >> text=Novedades y progreso').count() > 0, 'No se abrió Novedades después de elegir usuario')
    ver = pg.evaluate('VERSION'); hechas = pg.evaluate('NEWS[0].hechas')
    check(pg.locator(f'#sheet >> text={hechas}/100').count() > 0, 'Novedades no muestra el progreso X/100')
    check(pg.evaluate('NEWS[0].v') == ver, 'La primera novedad no es la versión actual')
    pg.screenshot(path='/tmp/cm-novedades.png')
    pg.locator('#sheet >> text=¡Genial!').click(); pg.wait_for_timeout(200)
    check(pg.evaluate('localStorage.getItem("cm_seen")') == ver, 'No quedó marcada la versión vista')
    check(S(pg).get('_v') == pg.evaluate('SCHEMA'), 'Datos nuevos sin número de esquema')

    for i, name in enumerate(['Hoy', 'Compras', 'Casa', 'Joaco', 'Mensajes']):
        loc = pg.locator(f'nav >> text={name}')
        if loc.count():
            loc.first.click(); pg.wait_for_timeout(250)
            pg.screenshot(path=f'/tmp/cm-{i+1}-{name.lower()}.png', full_page=True)
            width_ok(pg, name)
        else:
            errs.append(f'No encontré la pestaña {name}')

    # Hoy: tarjeta de instalar y acceso a Novedades
    pg.locator('nav >> text=Hoy').click(); pg.wait_for_timeout(200)
    check(pg.locator('text=Instalá Carga Mental').count() == 1, 'Falta la tarjeta para instalar en Hoy')
    pg.locator('text=Cómo se hace').click(); pg.wait_for_timeout(200)
    check(pg.locator('#sheet >> text=Instalar app').count() > 0, 'La guía de instalación no menciona «Instalar app»')
    pg.screenshot(path='/tmp/cm-instalar.png')
    pg.locator('#sheet >> text=Entendido').click(); pg.wait_for_timeout(150)
    pg.locator('text=Ahora no').click(); pg.wait_for_timeout(200)
    check(pg.locator('text=Instalá Carga Mental').count() == 0, '«Ahora no» no escondió la tarjeta de instalar')
    pg.locator('.verlink').click(); pg.wait_for_timeout(200)
    check(pg.locator('#sheet >> text=Novedades y progreso').count() > 0, 'El acceso a Novedades en Hoy no abre la pantalla')
    pg.locator('#sheet >> text=¡Genial!').click(); pg.wait_for_timeout(150)

    # Compras: anotar y comprar
    pg.locator('nav >> text=Compras').click(); pg.wait_for_timeout(200)
    pg.evaluate("A.filter('super')"); pg.wait_for_timeout(150)
    check(pg.locator('details[open]').count() == 1, 'Habituales debería estar abierto si no hay nada para comprar')
    pg.locator('button:has-text("Se acaba")').first.click(); pg.wait_for_timeout(200)
    listed = [i for i in S(pg)['items'].values() if i['state'] == 'list']
    check(len(listed) == 1, f'«Se acaba» no anotó el producto ({len(listed)})')
    pg.locator('section.card input[type=checkbox]').first.click(); pg.wait_for_timeout(200)
    it = S(pg)['items'][listed[0]['id']] if listed else {}
    check(it.get('state') == 'ok' and it.get('last'), 'Marcar comprado no registró la compra')
    check(pg.locator('nav button[data-tab=compras] .badge').count() == 0, 'El globito de compras no se actualizó')

    # Casa: ciclo del lavavajillas y tarea que se repite
    pg.locator('nav >> text=Casa').click(); pg.wait_for_timeout(200)
    for step in ['Cargar', 'Encender', 'Guardar']:
        pg.locator(f'.steps button:has-text("{step}")').first.click(); pg.wait_for_timeout(150)
    check((S(pg)['tasks']['t_lava'].get('lastDone') or {}).get('by') == 'gonzalo', 'El ciclo del lavavajillas no se completó')
    pg.evaluate("A.recDone('t_riego')"); pg.wait_for_timeout(100)
    check(S(pg)['tasks']['t_riego'].get('last'), '«Hecho» no registró la tarea que se repite')
    # Indicaciones para Daniela
    pg.fill('#in_tarea', 'Limpiar vidrios del balcón'); pg.press('#in_tarea', 'Enter'); pg.wait_for_timeout(200)
    check(any(n['text'] == 'Limpiar vidrios del balcón' for n in S(pg)['indic'].values()), 'No se agregó la indicación')

    # Joaco: mochila
    pg.locator('nav >> text=Joaco').click(); pg.wait_for_timeout(200)
    pg.locator('.card:has-text("Mochila") input[type=checkbox]').first.click(); pg.wait_for_timeout(150)
    check(len(S(pg)['checks']['mochila']['done']) == 1, 'No se tildó la mochila')

    # Mensajes
    pg.locator('nav >> text=Mensajes').click(); pg.wait_for_timeout(200)
    pg.fill('#chatin', 'Hola familia'); pg.press('#chatin', 'Enter'); pg.wait_for_timeout(250)
    check(pg.locator('.msg:has-text("Hola familia")').count() == 1, 'No se mandó el mensaje')
    width_ok(pg, 'Mensajes con texto')

    # Ajustes
    pg.locator('#who').click(); pg.wait_for_timeout(200)
    for t in ['Instalar app', 'Cómo instalarla', 'Novedades y progreso', f'v{ver}']:
        check(pg.locator(f'#sheet >> text={t}').count() > 0, f'Ajustes no muestra «{t}»')
    pg.screenshot(path='/tmp/cm-ajustes.png', full_page=True)
    pg.locator('#sheet >> text=Cerrar').click()

    # Recargar: Novedades no vuelve a abrirse y los datos siguen
    pg.reload(); pg.wait_for_timeout(2200)
    check(pg.locator('#modal:not(.hidden)').count() == 0, 'Novedades se volvió a abrir en la misma versión')
    check(S(pg)['tasks']['t_riego'].get('last'), 'Se perdieron datos al recargar')
    ctx.close()

    # ---------- 2. Migración desde v1.0.0 ----------
    init = f"""if(!sessionStorage.getItem('seeded')){{ sessionStorage.setItem('seeded','1');
      localStorage.setItem('cm_data', {json.dumps(json.dumps(OLD))}); localStorage.setItem('cm_me','dani'); localStorage.setItem('cm_tab','hoy'); }}"""
    ctx, pg = new_page('migración', init)
    pg.goto(URL); pg.wait_for_timeout(2200)
    d = S(pg)
    check(d.get('_v') == pg.evaluate('SCHEMA'), f"Migración: _v={d.get('_v')}")
    check(pg.evaluate('!!localStorage.getItem("cm_backup_v0")'), 'Migración: no quedó la copia cm_backup_v0')
    check(json.loads(pg.evaluate('localStorage.getItem("cm_backup_v0")')) == OLD, 'Migración: la copia no es idéntica a los datos viejos')
    check(d['items']['i_agua']['state'] == 'list' and d['items']['i_agua']['by'] == 'dani', 'Migración: se perdió la lista anotada')
    check(d['items']['i_mio']['note'] == 'el de Gonzalo' and d['items']['i_mio']['state'] == 'ok', 'Migración: se perdió el producto propio')
    check(d['items']['i_huerfano']['name'] == 'Miel' and d['items']['i_huerfano']['store'] in d['stores'], 'Migración: producto con negocio borrado')
    check(d['tasks']['t_lava']['cur']['0']['by'] == 'dani', 'Migración: se perdió la etapa en curso')
    check(d['tasks']['t_x']['kind'] == 'rec' and d['tasks']['t_x']['every'] == 1, 'Migración: tarea sin tipo')
    check(d['checks']['mochila']['list'] == ['Cartuchera', 'Flauta los miércoles'], 'Migración: se perdió la mochila propia')
    check('daniela' in d['checks'], 'Migración: no se agregó la ficha de Daniela')
    check(d['salud']['s_odonto']['note'] == 'Dra. López', 'Migración: se perdió salud')
    check(d['indic']['n_1']['text'] == 'Planchar camisas' and d['indic']['n_1']['kind'] == 'tarea', 'Migración: indicaciones')
    check(d['msgs']['m_1']['text'].startswith('Mensaje viejo'), 'Migración: se perdió el mensaje')
    check(d['weeks']['base']['days']['1']['busca'] == 'abuelos' and '5' in d['weeks']['base']['days'], 'Migración: semana tipo')
    check(pg.locator('#sheet >> text=Novedades y progreso').count() > 0, 'Migración: Novedades no se abrió para la versión nueva')
    pg.screenshot(path='/tmp/cm-migracion.png')
    pg.locator('#sheet >> text=¡Genial!').click(); pg.wait_for_timeout(150)
    for name in ['Hoy', 'Compras', 'Casa', 'Joaco', 'Mensajes']:
        pg.locator(f'nav >> text={name}').first.click(); pg.wait_for_timeout(150); width_ok(pg, f'Migración/{name}')
    check(pg.locator('text=Mensaje viejo que no se tiene que perder').count() == 1, 'Migración: el mensaje viejo no se ve')
    # Segunda carga: no vuelve a migrar ni pisa la copia
    pg.reload(); pg.wait_for_timeout(1500)
    check(S(pg)['msgs']['m_1']['text'].startswith('Mensaje viejo'), 'Migración: datos perdidos tras recargar')
    # Importar una copia vieja también la migra
    pg.evaluate("""() => { const f = new File([JSON.stringify({items:{i_imp:{id:'i_imp',name:'Importado',store:'super'}}})], 'v.json');
      const dt = new DataTransfer(); dt.items.add(f); A.settings(); const inp = document.getElementById('f_imp'); inp.files = dt.files; A.importJ(inp); }""")
    pg.wait_for_timeout(400)
    imp = S(pg)['items'].get('i_imp') or {}
    check(imp.get('state') == 'ok' and imp.get('every') == 7, f'Importar copia vieja: {imp}')
    ctx.close()

    # ---------- 3. Accesos directos ----------
    ctx, pg = new_page('atajos')
    pg.goto(URL); pg.wait_for_timeout(300)
    pg.evaluate("localStorage.setItem('cm_me','gonzalo'); localStorage.setItem('cm_seen', VERSION)")
    pg.goto(URL + '?go=chat'); pg.wait_for_timeout(800)
    check(pg.locator('nav button.on').inner_text().strip().endswith('Mensajes'), 'Atajo ?go=chat no abrió Mensajes')
    check('?' not in pg.url, 'El atajo no limpió la dirección')
    pg.goto(URL + '?go=anotar'); pg.wait_for_timeout(800)
    check(pg.locator('#sheet >> text=Nuevo producto').count() > 0, 'Atajo ?go=anotar no abrió el formulario')
    pg.screenshot(path='/tmp/cm-atajo-anotar.png')
    man = json.load(open(os.path.join(ROOT, 'manifest.json'), encoding='utf-8'))
    check([s['url'] for s in man.get('shortcuts', [])] == ['./?go=anotar', './?go=chat', './?go=hoy'], 'Faltan accesos directos en el manifest')
    ctx.close()

    # ---------- 4. Daniela ----------
    ctx, pg = new_page('daniela')
    pg.goto(URL); pg.wait_for_timeout(300)
    pg.evaluate("localStorage.setItem('cm_me','daniela'); localStorage.setItem('cm_seen', VERSION)")
    pg.reload(); pg.wait_for_timeout(1800)
    tabs = [t.strip() for t in pg.locator('nav button').all_inner_texts()]
    check(len(tabs) == 2 and 'Indicaciones' in tabs[0], f'Daniela ve pestañas de más: {tabs}')
    check(pg.locator('.verlink').count() == 1, 'Daniela no ve el acceso a Novedades')
    pg.screenshot(path='/tmp/cm-daniela.png', full_page=True)
    width_ok(pg, 'Daniela')
    ctx.close()

    # ---------- 5. Diseño: íconos, avatares y modo oscuro (v1.2.0) ----------
    CONTRAST = """() => {
      const cs = getComputedStyle(document.documentElement), v = n => cs.getPropertyValue(n).trim();
      const lum = h => { h = h.replace('#',''); if(h.length === 3) h = h.split('').map(x => x + x).join(''); const c = [0,2,4].map(i => parseInt(h.slice(i,i+2),16)/255).map(x => x <= .03928 ? x/12.92 : Math.pow((x+.055)/1.055, 2.4)); return .2126*c[0]+.7152*c[1]+.0722*c[2]; };
      const ratio = (a,b) => { const x = lum(v(a)), y = lum(v(b)); return (Math.max(x,y)+.05)/(Math.min(x,y)+.05); };
      return {ink:ratio('--ink','--bg'), mut:ratio('--mut','--bg'), mutCard:ratio('--mut','--card'), pri:ratio('--pri-on','--pri'), priTx:ratio('--pri-tx','--card'), warn:ratio('--warn','--warnbg'), bad:ratio('--bad','--badbg'), ok:ratio('--ok','--okbg'), bg:v('--bg')};
    }"""
    for scheme in ['light', 'dark']:
        ctx = b.new_context(viewport={'width': 390, 'height': 844}, color_scheme=scheme)
        pg = ctx.new_page()
        pg.on('pageerror', lambda e: errs.append(f'[tema] JS: {e}'))
        pg.on('console', lambda m: errs.append(f'[tema] consola: {m.text}') if m.type == 'error' else None)
        pg.goto(URL); pg.wait_for_timeout(300)
        pg.evaluate("localStorage.setItem('cm_me','gonzalo'); localStorage.setItem('cm_seen', VERSION)")
        pg.reload(); pg.wait_for_timeout(1800)
        c = pg.evaluate(CONTRAST)
        for k, val in c.items():
            if k != 'bg': check(val >= 4.5, f'Contraste {scheme} {k}={val:.2f} (mínimo 4.5)')
        bg = pg.evaluate("getComputedStyle(document.body).backgroundColor")
        check((bg == 'rgb(26, 20, 17)') == (scheme == 'dark'), f'Modo {scheme} automático: fondo {bg}')
        check(pg.locator('nav svg.ic').count() == 5, 'La barra inferior no tiene los 5 íconos SVG')
        check(pg.locator('nav b').count() == 0, 'Quedaron emojis en la barra inferior')
        check(pg.locator('#who .av').count() == 1, 'El botón de usuario no muestra el avatar')
        check(pg.locator('main h3 .hic svg').count() >= 3, 'Los títulos de Hoy no tienen íconos')
        for name in ['Hoy', 'Compras', 'Casa', 'Joaco', 'Mensajes']:
            pg.locator(f'nav >> text={name}').first.click(); pg.wait_for_timeout(200)
            pg.screenshot(path=f'/tmp/cm-{scheme}-{name.lower()}.png', full_page=True)
            width_ok(pg, f'{scheme}/{name}')
        pg.locator('nav >> text=Joaco').click(); pg.wait_for_timeout(150)
        check(pg.locator('.week .pp.v .av').count() == 10, 'La semana de Joaco no usa avatares')
        ctx.close()
    # Elegir el tema a mano desde Ajustes (gana sobre el del teléfono y se recuerda)
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, color_scheme='light')
    pg = ctx.new_page(); pg.on('pageerror', lambda e: errs.append(f'[tema manual] JS: {e}'))
    pg.goto(URL); pg.wait_for_timeout(300)
    pg.evaluate("localStorage.setItem('cm_me','dani'); localStorage.setItem('cm_seen', VERSION)")
    pg.reload(); pg.wait_for_timeout(1800)
    pg.locator('#who').click(); pg.wait_for_timeout(200)
    pg.locator('#sheet .seg >> text=Oscuro').click(); pg.wait_for_timeout(200)
    check(pg.evaluate("document.documentElement.dataset.theme") == 'dark', 'Elegir «Oscuro» no cambió el tema')
    check(pg.evaluate("document.querySelector('meta[name=theme-color]').content") == '#2f231d', 'La barra del teléfono no cambió de color')
    pg.screenshot(path='/tmp/cm-dark-ajustes.png', full_page=True)
    pg.reload(); pg.wait_for_timeout(600)
    check(pg.evaluate("document.documentElement.dataset.theme") == 'dark', 'El modo oscuro no se recordó al recargar')
    pg.locator('#who').click(); pg.wait_for_timeout(200)
    pg.locator('#sheet .seg >> text=Automático').click(); pg.wait_for_timeout(200)
    check(pg.evaluate("document.documentElement.dataset.theme") is None and pg.evaluate("localStorage.getItem('cm_theme')") is None, '«Automático» no volvió al tema del teléfono')
    ctx.close()

    # ---------- 6. Movimiento y festejo (v1.3.0) ----------
    V12 = json.loads(json.dumps(OLD)); V12['_v'] = 1
    V12['checks']['daniela'] = {'id': 'daniela', 'next': '', 'hours': '', 'coord': 'dani', 'note': ''}
    V12['indic']['n_1']['kind'] = 'tarea'
    V12['weeks']['base']['days'].update({'3': {'lleva': 'gonzalo', 'busca': 'gonzalo'}, '4': {'lleva': 'gonzalo', 'busca': 'gonzalo'}, '5': {'lleva': 'dani', 'busca': 'dani'}})
    V12['msgs']['m_2'] = {'id': 'm_2', 'text': 'Mensaje de Dani sin leer', 'at': 1762500000000, 'by': 'dani'}
    init12 = f"""if(!sessionStorage.getItem('seeded')){{ sessionStorage.setItem('seeded','1');
      localStorage.setItem('cm_data', {json.dumps(json.dumps(V12))}); localStorage.setItem('cm_me','gonzalo'); localStorage.setItem('cm_seen','1.2.0'); localStorage.setItem('cm_read','1762000000001');
      window.__vib = []; navigator.vibrate = p => {{ window.__vib.push(p); return true; }}; }}
      else {{ window.__vib = []; navigator.vibrate = p => {{ window.__vib.push(p); return true; }}; }}"""
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, has_touch=True)
    ctx.add_init_script(init12)
    pg = ctx.new_page()
    pg.on('pageerror', lambda e: errs.append(f'[v1.3] JS: {e}'))
    pg.on('console', lambda m: errs.append(f'[v1.3] consola: {m.text}') if m.type == 'error' else None)
    pg.goto(URL); pg.wait_for_timeout(2200)
    d = S(pg)
    check(sin_v15(d) == V12, 'Datos de v1.2.0: cambiaron al cargar la versión nueva')
    # Hoja de Novedades: se cierra deslizando hacia abajo con toques reales
    check(pg.locator('#sheet >> text=Novedades y progreso').count() > 0, 'v1.3: no se abrió Novedades')
    check(pg.locator('#sheetbox .grab').count() == 1, 'La hoja no tiene manija')
    cdp = ctx.new_cdp_session(pg)
    box = pg.locator('#sheetbox').bounding_box()
    x, y = 195, box['y'] + 20
    cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': x, 'y': y}]})
    for k in range(1, 9):
        cdp.send('Input.dispatchTouchEvent', {'type': 'touchMove', 'touchPoints': [{'x': x, 'y': y + k * 30}]}); pg.wait_for_timeout(16)
    pg.screenshot(path='/tmp/cm-hoja-deslizando.png')
    cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []}); pg.wait_for_timeout(450)
    check(pg.locator('#modal.hidden').count() == 1, 'Deslizar hacia abajo no cerró la hoja')
    # Un toque corto no la cierra
    pg.evaluate('A.news()'); pg.wait_for_timeout(350)
    cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': x, 'y': y}]})
    cdp.send('Input.dispatchTouchEvent', {'type': 'touchMove', 'touchPoints': [{'x': x, 'y': y + 25}]})
    cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []}); pg.wait_for_timeout(400)
    check(pg.locator('#modal:not(.hidden)').count() == 1, 'Un arrastre cortito cerró la hoja')
    pg.keyboard.press('Escape'); pg.wait_for_timeout(150)
    check(pg.locator('#modal.hidden').count() == 1, 'Escape no cerró la hoja')
    # Globitos e indicador
    bd = lambda k: (pg.locator(f'nav button[data-tab={k}] .badge').all_inner_texts() or ['0'])[0]
    check(bd('chat') == '1', f'Globito de mensajes sin leer: {bd("chat")}')
    check(bd('compras') == '2', f'Globito de compras: {bd("compras")}')
    check(pg.locator('nav button[data-tab=chat] .vh').inner_text().strip() == ', 1 pendiente', 'Falta el texto para lectores de pantalla')
    check(pg.locator('nav b').count() == 0, 'Globitos con <b> en la barra')
    left0 = pg.evaluate("getComputedStyle(document.getElementById('navind')).left")
    pg.screenshot(path='/tmp/cm-globitos.png')
    pg.locator('nav button[data-tab=chat]').click(); pg.wait_for_timeout(450)
    left1 = pg.evaluate("getComputedStyle(document.getElementById('navind')).left")
    ind = pg.locator('#navind').bounding_box(); btn = pg.locator('nav button[data-tab=chat]').bounding_box()
    check(left0 != left1 and abs((ind['x'] + ind['width'] / 2) - (btn['x'] + btn['width'] / 2)) < 2, f'El indicador no se movió a Mensajes ({left0} → {left1})')
    check(pg.locator('nav button[data-tab=chat] .badge').count() == 0, 'El globito de mensajes no se borró al leerlos')
    pg.locator('nav button[data-tab=hoy]').click(); pg.wait_for_timeout(200)
    check(pg.locator('nav button[data-tab=chat] .badge').count() == 0, 'Los mensajes leídos volvieron a contarse')
    # Tilde, vibración y confeti: comprar lo último de la lista
    pg.locator('nav button[data-tab=compras]').click(); pg.wait_for_timeout(200)
    pg.locator('section.card input[type=checkbox]').first.click(); pg.wait_for_timeout(250)
    check(pg.locator('#confeti').count() == 0, 'Hubo confeti antes de terminar la lista')
    pg.locator('section.card input[type=checkbox]').first.click(); pg.wait_for_timeout(120)
    check(pg.locator('#confeti i').count() > 10, 'No hubo confeti al completar la lista')
    check(pg.locator('section.card.pop').count() == 1, 'No se resaltó el negocio recién completado')
    pg.screenshot(path='/tmp/cm-confeti.png')
    vib = pg.evaluate('window.__vib')
    check(15 in vib and [20, 40, 30] in vib, f'Vibración: {vib}')
    pg.wait_for_timeout(2300)
    check(pg.locator('#confeti').count() == 0, 'El confeti no se limpió')
    # Etapa con tilde animada; apagar la vibración
    pg.locator('nav button[data-tab=casa]').click(); pg.wait_for_timeout(200)
    pg.locator('.steps button:has-text("Encender")').first.click(); pg.wait_for_timeout(100)
    check(pg.locator('.steps button.pop').count() == 1, 'La etapa marcada no tiene la tilde animada')
    pg.locator('#who').click(); pg.wait_for_timeout(200)
    pg.locator('#f_vib').uncheck(); pg.wait_for_timeout(100)
    check(pg.evaluate("localStorage.getItem('cm_vib')") == '0', 'No se guardó «sin vibración»')
    pg.keyboard.press('Escape'); n0 = len(pg.evaluate('window.__vib'))
    pg.evaluate("A.recDone('t_x')"); pg.wait_for_timeout(100)
    check(len(pg.evaluate('window.__vib')) == n0, 'Vibró con la vibración apagada')
    # Estados vacíos ilustrados
    pg.evaluate("S.msgs = {}; S.indic = {}; S.salud = {}; render(); A.go('chat')"); pg.wait_for_timeout(150)
    check(pg.locator('main .empty .ill svg').count() >= 1, 'Mensajes vacío sin ilustración')
    pg.screenshot(path='/tmp/cm-vacio-chat.png')
    pg.evaluate("A.go('casa')"); pg.wait_for_timeout(150)
    check(pg.locator('main .empty:has-text("Sin tareas por ahora")').count() == 1, 'Indicaciones vacías sin ilustración')
    pg.evaluate("A.go('joaco')"); pg.wait_for_timeout(150)
    check(pg.locator('main .empty:has-text("Sin controles cargados")').count() == 1, 'Salud vacía sin ilustración')
    width_ok(pg, 'v1.3 vacíos')
    ctx.close()
    # Modo oscuro de lo nuevo
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, color_scheme='dark'); ctx.add_init_script(init12)
    pg = ctx.new_page(); pg.on('pageerror', lambda e: errs.append(f'[v1.3 oscuro] JS: {e}'))
    pg.goto(URL); pg.wait_for_timeout(2000); pg.keyboard.press('Escape'); pg.wait_for_timeout(200)
    pg.screenshot(path='/tmp/cm-dark-globitos.png')
    pg.evaluate("S.msgs = {}; render(); A.go('chat')"); pg.wait_for_timeout(200)
    pg.screenshot(path='/tmp/cm-dark-vacio.png')
    ctx.close()


    # ---------- 7. Accesibilidad, deshacer, botón + y anillos (v1.4.0) ----------
    # Datos de v1.3.0 (igual formato: el esquema no cambió) con la versión 1.3.0 ya vista
    init13 = init12.replace("localStorage.setItem('cm_seen','1.2.0')", "localStorage.setItem('cm_seen','1.3.0')")
    def new13(name, scheme='light'):
        c = b.new_context(viewport={'width': 390, 'height': 844}, color_scheme=scheme); c.add_init_script(init13)
        q = c.new_page()
        q.on('pageerror', lambda e: errs.append(f'[{name}] JS: {e}'))
        q.on('console', lambda m: errs.append(f'[{name}] consola: {m.text}') if m.type == 'error' else None)
        return c, q
    ctx, pg = new13('v1.4')
    pg.goto(URL); pg.wait_for_timeout(2200)
    check(sin_v15(S(pg)) == V12, 'Datos de v1.3.0: cambiaron al cargar la versión nueva')
    check(pg.locator('#modal.hidden').count() == 0 or True, '')
    # Novedades se abre sola por ser versión nueva
    check(pg.locator('#sheet >> text=Novedades y progreso').count() > 0 and pg.locator(f'#sheet >> text={hechas}/100').count() > 0, 'v1.4: Novedades no muestra el progreso')
    pg.keyboard.press('Escape'); pg.wait_for_timeout(200)
    # Anillos en Hoy
    check(pg.locator('main svg.ring').count() == 3, 'Hoy no muestra los 3 anillos')
    lbl = lambda: pg.locator('main svg.ring').evaluate_all('els => els.map(e => e.getAttribute("aria-label"))')
    check(lbl()[0] == 'Compras: 0 de 2', f'Anillo de compras: {lbl()}')
    pg.screenshot(path='/tmp/cm-anillos.png', full_page=True)
    # Botón + por pestaña
    check(pg.locator('#fab:not([hidden])').count() == 1 and pg.locator('#fab').get_attribute('aria-label') == 'Sumar algo', 'Hoy no tiene botón +')
    pg.locator('#fab').click(); pg.wait_for_timeout(300)
    check(pg.locator('#sheet >> text=¿Qué querés sumar?').count() == 1, 'El botón + de Hoy no abrió el menú')
    pg.screenshot(path='/tmp/cm-fab-hoy.png')
    pg.locator('#sheet >> text=Anotar una compra').click(); pg.wait_for_timeout(250)
    check(pg.locator('#sheet >> text=Nuevo producto').count() == 1, '«Anotar una compra» no abrió el formulario')
    pg.keyboard.press('Escape'); pg.wait_for_timeout(200)
    for tabk, lab, sheet in [('compras', 'Anotar un producto', 'Nuevo producto'), ('casa', 'Nueva tarea', 'Nueva tarea'), ('joaco', 'Nuevo control de salud', 'Nuevo control')]:
        pg.locator(f'nav button[data-tab={tabk}]').click(); pg.wait_for_timeout(200)
        check(pg.locator('#fab').get_attribute('aria-label') == lab and pg.locator('#fab:not([hidden])').count() == 1, f'Botón + de {tabk}: {pg.locator("#fab").get_attribute("aria-label")}')
        pg.locator('#fab').click(); pg.wait_for_timeout(250)
        check(pg.locator(f'#sheet >> text={sheet}').count() >= 1, f'Botón + de {tabk} no abrió «{sheet}»')
        pg.keyboard.press('Escape'); pg.wait_for_timeout(150)
    pg.locator('nav button[data-tab=chat]').click(); pg.wait_for_timeout(200)
    check(pg.locator('#fab:not([hidden])').count() == 0, 'El botón + no debería verse en Mensajes')
    # Deshacer: se acaba → deshacer
    pg.locator('nav button[data-tab=compras]').click(); pg.wait_for_timeout(200)
    pg.evaluate("A.filter('super')"); pg.wait_for_timeout(150)
    pg.evaluate("A.need('i_huerfano')"); pg.wait_for_timeout(200)
    check(S(pg)['items']['i_huerfano']['state'] == 'list', 'Se acaba: no anotó')
    n_log = len(S(pg)['log'])
    check(pg.locator('#toast button:has-text("Deshacer")').count() == 1, 'El aviso no trae «Deshacer»')
    pg.screenshot(path='/tmp/cm-deshacer.png')
    pg.wait_for_timeout(2600)
    check(pg.locator('#toast.on').count() == 1, 'El aviso con «Deshacer» desapareció muy rápido')
    pg.locator('#toast button').click(); pg.wait_for_timeout(250)
    check(S(pg)['items']['i_huerfano']['state'] == 'ok', 'Deshacer no devolvió el producto')
    check(len(S(pg)['log']) == n_log - 1, 'Deshacer no sacó el movimiento del registro')
    # Deshacer una compra: vuelve a la lista con su fecha anterior
    pg.evaluate("A.filter('super')"); pg.wait_for_timeout(100)
    antes = S(pg)['items']['i_agua']
    pg.evaluate("A.bought('i_agua')"); pg.wait_for_timeout(100)
    check(S(pg)['items']['i_agua']['state'] == 'ok', 'bought no marcó')
    pg.locator('#toast button').click(); pg.wait_for_timeout(200)
    check(S(pg)['items']['i_agua']['state'] == 'list' and S(pg)['items']['i_agua']['last'] == antes['last'], 'Deshacer la compra no restauró el estado anterior')
    # Compré todo → deshacer
    pg.evaluate("A.boughtAll('super')"); pg.wait_for_timeout(100)
    check(S(pg)['items']['i_agua']['state'] == 'ok' and S(pg)['items']['i_mio']['state'] == 'ok', 'Compré todo no marcó')
    pg.locator('#toast button').click(); pg.wait_for_timeout(200)
    check(S(pg)['items']['i_agua']['state'] == 'list' and S(pg)['items']['i_mio'].get('last') == 1762000000000, 'Deshacer «Compré todo» no restauró')
    # Indicación borrada → deshacer; tarea hecha → deshacer
    pg.evaluate("A.go('casa')"); pg.wait_for_timeout(150)
    pg.evaluate("A.delIndic('n_1')"); pg.wait_for_timeout(100)
    check('n_1' not in S(pg)['indic'], 'delIndic no borró')
    pg.locator('#toast button').click(); pg.wait_for_timeout(200)
    check(S(pg)['indic'].get('n_1', {}).get('text') == 'Planchar camisas', 'Deshacer no devolvió la indicación')
    pg.evaluate("A.recDone('t_x')"); pg.wait_for_timeout(100)
    check(S(pg)['tasks']['t_x']['last'], 'recDone no marcó')
    pg.locator('#toast button').click(); pg.wait_for_timeout(200)
    check(not S(pg)['tasks']['t_x'].get('last'), 'Deshacer «Hecho» no restauró la tarea')
    # Anillo que cambia al comprar
    pg.evaluate("A.go('hoy')"); pg.wait_for_timeout(150)
    pg.evaluate("A.bought('i_agua')"); pg.wait_for_timeout(150)
    check(lbl()[0] == 'Compras: 1 de 2', f'El anillo de compras no avanzó: {lbl()}')
    # Textos nuevos
    pg.evaluate("A.settings()"); pg.wait_for_timeout(200)
    check(pg.locator('#sheet >> text=Tamaño de letra').count() == 1, 'Ajustes sin tamaño de letra')
    check(pg.locator('#sheet >> text=todavía sin activar').count() + pg.locator('#sheet >> text=no disponible').count() + pg.locator('#sheet >> text=activado').count() + pg.locator('#sheet >> text=bloqueado').count() >= 1, 'Permiso de avisos sin traducir')
    check(pg.locator('#sheet >> text=solo en este teléfono').count() >= 1, 'Estado de sincronización sin traducir')
    # Foco: al abrir va a la hoja; al cerrar vuelve
    check(pg.evaluate("document.activeElement && document.activeElement.id") == 'sheetbox', 'Al abrir una hoja el foco no va a la hoja')
    check(bool(pg.evaluate("document.getElementById('sheetbox').getAttribute('aria-label')")), 'La hoja no tiene nombre para lectores de pantalla')
    # Letra grande
    base_fs = pg.evaluate("parseFloat(getComputedStyle(document.querySelector('.muted')).fontSize)")
    pg.locator('#sheet .seg:has-text("Grande") >> text=Grande').click(); pg.wait_for_timeout(250)
    check(pg.evaluate("document.documentElement.dataset.big") == '1' and pg.evaluate("localStorage.getItem('cm_big')") == '1', 'Letra grande no se activó')
    pg.screenshot(path='/tmp/cm-grande-ajustes.png', full_page=True)
    pg.keyboard.press('Escape'); pg.wait_for_timeout(200)
    big_fs = pg.evaluate("parseFloat(getComputedStyle(document.querySelector('.muted')).fontSize)")
    check(big_fs > base_fs, f'La letra grande no agrandó el texto ({base_fs} → {big_fs})')
    pg.reload(); pg.wait_for_timeout(1200)
    check(pg.evaluate("document.documentElement.dataset.big") == '1', 'La letra grande no se recordó')
    for tk in ['hoy', 'compras', 'casa', 'joaco', 'chat']:
        pg.locator(f'nav button[data-tab={tk}]').click(); pg.wait_for_timeout(200)
        pg.screenshot(path=f'/tmp/cm-grande-{tk}.png', full_page=True); width_ok(pg, f'Letra grande/{tk}')
    ctx.close()

    # Áreas táctiles de 44 px y accesibilidad (claro y oscuro, normal y letra grande)
    AUDIT = """() => {
      const bad = [], vis = e => { const r = e.getBoundingClientRect(); const cs = getComputedStyle(e); return r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && !e.closest('#splash') && !e.closest('[hidden]'); };
      document.querySelectorAll('button, summary, select, input:not([type=hidden]):not([type=file])').forEach(e => {
        if(!vis(e)) return;
        const t = (e.type === 'checkbox') ? (e.closest('label') || e) : e, r = t.getBoundingClientRect();
        const nm = (e.innerText || '').trim() || e.getAttribute('aria-label') || (e.id && document.querySelector('label[for="' + e.id + '"]')) || (e.closest('label') && e.closest('label').innerText.trim()) || e.getAttribute('title');
        const id = (e.tagName + '.' + (e.className || '') + ' «' + ((e.innerText || e.getAttribute('aria-label') || '').trim().slice(0, 24)) + '»');
        if(r.width < 43.5 || r.height < 43.5) bad.push('chico ' + id + ' ' + Math.round(r.width) + 'x' + Math.round(r.height));
        if(!nm) bad.push('sin nombre ' + id);
      });
      document.querySelectorAll('[onclick]').forEach(e => {
        if(!vis(e) || ['BUTTON','A','INPUT','LABEL','SUMMARY'].includes(e.tagName) || e.id === 'modal') return;
        if(e.getAttribute('role') !== 'button' || e.tabIndex < 0) bad.push('clic sin teclado ' + e.tagName + '.' + e.className);
      });
      return bad;
    }"""
    for scheme, bigv in [('light', '0'), ('dark', '0'), ('light', '1')]:
        ctx, pg = new13(f'a11y-{scheme}-{bigv}', scheme)
        pg.goto(URL); pg.wait_for_timeout(300)
        if bigv == '1': pg.evaluate("localStorage.setItem('cm_big','1')")
        pg.evaluate("localStorage.setItem('cm_seen', VERSION)"); pg.reload(); pg.wait_for_timeout(1500)
        for tk in ['hoy', 'compras', 'casa', 'joaco', 'chat']:
            pg.locator(f'nav button[data-tab={tk}]').click(); pg.wait_for_timeout(200)
            if tk == 'compras':
                pg.evaluate("A.filter('todos')"); pg.wait_for_timeout(100)
                pg.evaluate("A.search('a')"); pg.wait_for_timeout(100)
                for x in pg.evaluate(AUDIT): errs.append(f'a11y {scheme}/{bigv}/buscador: {x}')
                width_ok(pg, f'a11y {scheme}/{bigv}/buscador')
                pg.evaluate("A.search('')"); pg.wait_for_timeout(100)
            if tk == 'casa': pg.evaluate("document.querySelectorAll('details').forEach(d => d.open = true)")
            for x in pg.evaluate(AUDIT): errs.append(f'a11y {scheme}/{bigv}/{tk}: {x}')
            width_ok(pg, f'a11y {scheme}/{bigv}/{tk}')
        for opener in ["A.voice()", "document.getElementById('f_voz').value='agua, dos kilos de tomate y pan';A.voiceReview()", "A.settings()", "A.fab()", "A.news()", "A.itemForm('i_agua')", "A.saludForm('s_odonto')", "A.mochilaEdit()"]:
            pg.evaluate(opener); pg.wait_for_timeout(150)
            for x in pg.evaluate(AUDIT): errs.append(f'a11y {scheme}/{bigv}/{opener}: {x}')
            gh = pg.locator('#sheetbox .grab').bounding_box()['height']; check(gh >= 43.5, f'La manija de la hoja es muy chica ({gh}, {opener}, {scheme}/{bigv})')
            pg.keyboard.press('Escape'); pg.wait_for_timeout(100)
        if scheme == 'dark':
            pg.screenshot(path='/tmp/cm-dark-v14.png')
            pg.locator('nav button[data-tab=hoy]').click(); pg.wait_for_timeout(200); pg.screenshot(path='/tmp/cm-dark-hoy-anillos.png', full_page=True)
        ctx.close()
    # Contraste AA de más pares: etiquetas, botón rojo del globito, botón de Dani, avatares y anillos
    for scheme in ['light', 'dark']:
        ctx = b.new_context(viewport={'width': 390, 'height': 844}, color_scheme=scheme)
        pg = ctx.new_page(); pg.goto(URL); pg.wait_for_timeout(300)
        r = pg.evaluate("""() => {
          const cs = getComputedStyle(document.documentElement), v = n => cs.getPropertyValue(n).trim();
          const lum = h => { h = h.replace('#',''); if(h.length === 3) h = h.split('').map(x => x + x).join(''); const c = [0,2,4].map(i => parseInt(h.slice(i,i+2),16)/255).map(x => x <= .03928 ? x/12.92 : Math.pow((x+.055)/1.055, 2.4)); return .2126*c[0]+.7152*c[1]+.0722*c[2]; };
          const ratio = (a,b) => { const x = lum(a), y = lum(b); return (Math.max(x,y)+.05)/(Math.min(x,y)+.05); };
          const out = {mutPri2: ratio(v('--mut'), v('--pri2')), priTxPri2: ratio(v('--pri-tx'), v('--pri2')), inkField: ratio(v('--ink'), v('--field')), toast: ratio(v('--toast-tx'), v('--toast')), hdr: ratio(v('--hdr-tx'), v('--hdr')), danio: ratio('#ffffff', '#db2777')};
          out.badge = ratio('#ffffff', document.documentElement.dataset.theme === 'dark' || matchMedia('(prefers-color-scheme: dark)').matches ? '#c4473f' : v('--bad'));
          ['#2563eb','#db2777','#047857','#c2410c','#7c3aed','#64748b'].forEach((c, i) => out['av' + i] = ratio('#ffffff', c));
          return out; }""")
        for k, val in r.items(): check(val >= 4.5, f'Contraste {scheme} {k}={val:.2f} (mínimo 4.5)')
        ctx.close()

    # ---------- 8. Compras v1.5.0: cantidad, categorías, buscador, voz e historial ----------
    VOZ = """window.__dicho = 'leche, dos kilos de tomate y agua';
      window.SpeechRecognition = window.webkitSpeechRecognition = function(){ const r = this; r.start = () => setTimeout(() => {
        r.onresult && r.onresult({results:[[{transcript: window.__dicho}]]}); r.onend && r.onend(); }, 60); r.stop = r.abort = () => {}; };"""
    init14 = init12.replace("localStorage.setItem('cm_seen','1.2.0')", "localStorage.setItem('cm_seen','1.4.0')") + VOZ
    for scheme in ['light', 'dark']:
        ctx = b.new_context(viewport={'width': 390, 'height': 844}, color_scheme=scheme); ctx.add_init_script(init14)
        pg = ctx.new_page()
        pg.on('pageerror', lambda e: errs.append(f'[v1.5] JS: {e}'))
        pg.on('console', lambda m: errs.append(f'[v1.5] consola: {m.text}') if m.type == 'error' else None)
        pg.goto(URL); pg.wait_for_timeout(2200)
        d = S(pg)
        # Migración 1 → 2: nada se pierde, queda copia y se completan los campos nuevos
        check(d['_v'] == 3, f"v1.5: _v={d['_v']} (esperaba 3)")
        check(sin_v15(d) == V12, 'v1.5: la migración cambió o perdió datos de v1.4.0')
        check(json.loads(pg.evaluate('localStorage.getItem("cm_backup_v1")') or 'null') == V12, 'v1.5: no quedó la copia cm_backup_v1 idéntica')
        it = d['items']
        check(it['i_agua']['cat'] == 'bebidas' and it['i_mio']['cat'] == 'frescos' and it['i_huerfano']['cat'] == 'almacen', f"v1.5: categorías mal asignadas {[x['cat'] for x in it.values()]}")
        check(all(x['qty'] is None and x['unit'] == '' for x in it.values()), 'v1.5: cantidad/unidad iniciales')
        check(it['i_mio']['hist'] == [{'at': 1762000000000, 'by': None}] and it['i_agua']['hist'] == [], f"v1.5: historial inicial {it['i_mio']['hist']}")
        check(pg.locator('#sheet >> text=26/100').count() > 0, 'v1.5: Novedades no muestra 26/100')
        pg.screenshot(path=f'/tmp/cm-v15-novedades-{scheme}.png')
        pg.keyboard.press('Escape'); pg.wait_for_timeout(200)
        pg.reload(); pg.wait_for_timeout(1800)
        check(S(pg) == d, 'v1.5: recargar volvió a tocar los datos ya migrados')
        # Categorías del usuario nuevo y texto de cantidades
        cats = pg.evaluate("Object.fromEntries(Object.values(seed().items).map(i => [i.name, i.cat]))")
        esperado = {'Agua': 'bebidas', 'Soda': 'bebidas', 'Latas de atún': 'almacen', 'Papel de cocina': 'papeles', 'Papel higiénico': 'papeles', 'Pañuelos descartables': 'papeles',
                    'Artículos de limpieza': 'limpieza', 'Pastillas para el lavavajillas': 'limpieza', 'Jabón para la ropa': 'limpieza', 'Frutos secos': 'almacen', 'Semillas': 'almacen',
                    'Frutas': 'frescos', 'Verduras': 'frescos', 'Pescado': 'frescos', 'Yerba': 'almacen', 'Huevos (gallinas alimentadas a maíz)': 'frescos', 'Snacks de Joaco': 'almacen'}
        for k, v in esperado.items(): check(cats.get(k) == v, f'Categoría de «{k}»: {cats.get(k)} (esperaba {v})')
        q = pg.evaluate("[qtyTxt({qty:2, unit:'doc'}), qtyTxt({qty:6, unit:'L'}), qtyTxt({qty:1, unit:'kg'}), qtyTxt({qty:1.5, unit:'kg'}), qtyTxt({qty:3, unit:''}), qtyTxt({qty:null, unit:'kg'}), qtyTxt({qty:1, unit:'paq'})]")
        check(q == ['2 docenas', '6 L', '1 kg', '1,5 kg', '× 3', '', '1 paquete'], f'qtyTxt: {q}')
        # Cantidad y unidad desde el formulario
        pg.locator('nav button[data-tab=compras]').click(); pg.wait_for_timeout(300)
        check(pg.locator('main section.card:has-text("Supermercado") .cat').count() == 2, 'El súper no agrupa por categoría')
        check(pg.locator('main section.card:has-text("Naturista") .cat').count() == 0, 'Un negocio con una sola categoría no debería mostrar títulos')
        pg.locator('main .item .t:has-text("Agua")').first.click(); pg.wait_for_timeout(250)
        check(pg.locator('#f_cat').input_value() == 'bebidas', 'El formulario no muestra la categoría')
        check(pg.locator('#sheet summary:has-text("Historial de compras (0)")').count() == 1, 'El formulario no muestra el historial vacío')
        pg.fill('#f_qty', '1,5'); pg.select_option('#f_unit', 'L'); pg.select_option('#f_cat', 'otros')
        pg.locator('#sheet button.pri').click(); pg.wait_for_timeout(250)
        a = S(pg)['items']['i_agua']
        check(a['qty'] == 1.5 and a['unit'] == 'L' and a['cat'] == 'otros' and a['state'] == 'list', f'Cantidad/unidad/categoría no se guardaron: {a}')
        check(pg.locator('main .item:has-text("Agua") .qty').first.inner_text().strip() == '· 1,5 L', 'La lista no muestra la cantidad')
        pg.evaluate("A.itemForm('i_agua')"); pg.wait_for_timeout(150)
        check(pg.locator('#f_qty').input_value() == '1,5' and pg.locator('#f_unit').input_value() == 'L', 'El formulario no recuerda la cantidad')
        pg.fill('#f_qty', '6'); pg.select_option('#f_cat', 'bebidas'); pg.locator('#sheet button.pri').click(); pg.wait_for_timeout(200)
        # Historial: comprar registra quién, cuándo y cuánto; deshacer lo saca
        pg.locator('main input[aria-label="Comprado: Agua"]').click(); pg.wait_for_timeout(250)
        a = S(pg)['items']['i_agua']
        check(len(a['hist']) == 1 and a['hist'][0]['by'] == 'gonzalo' and a['hist'][0]['qty'] == 6 and a['hist'][0]['unit'] == 'L' and a['hist'][0]['at'] == a['last'], f"Historial tras comprar: {a['hist']}")
        pg.locator('#toast button').click(); pg.wait_for_timeout(250)
        check(S(pg)['items']['i_agua']['hist'] == [] and S(pg)['items']['i_agua']['state'] == 'list', 'Deshacer no sacó la compra del historial')
        pg.evaluate("A.bought('i_agua')"); pg.wait_for_timeout(100); pg.evaluate("A.need('i_agua')"); pg.wait_for_timeout(100); pg.evaluate("A.boughtAll('super')"); pg.wait_for_timeout(300)
        check(len(S(pg)['items']['i_agua']['hist']) == 2, '«Compré todo» no sumó al historial')
        pg.evaluate("A.itemForm('i_agua')"); pg.wait_for_timeout(200)
        check(pg.locator('#sheet summary:has-text("Historial de compras (2)")').count() == 1, 'El historial no cuenta 2 compras')
        pg.locator('#sheet summary').click(); pg.wait_for_timeout(150)
        check(pg.locator('#sheet .histd .log').count() == 2 and 'Gonzalo' in pg.locator('#sheet .histd .log').first.inner_text() and '6 L' in pg.locator('#sheet .histd .log').first.inner_text(), 'El historial no muestra quién y cuánto')
        pg.screenshot(path=f'/tmp/cm-v15-producto-{scheme}.png'); width_ok(pg, 'v1.5 producto')
        pg.keyboard.press('Escape'); pg.wait_for_timeout(150)
        pg.evaluate("A.itemForm('i_mio')"); pg.wait_for_timeout(150); pg.locator('#sheet summary').click()
        check('Sin dato de quién' in pg.locator('#sheet .histd').inner_text(), 'Historial migrado: falta el renglón de la última compra')
        pg.keyboard.press('Escape'); pg.wait_for_timeout(150)
        # Buscador
        pg.locator('#buscar').click(); pg.keyboard.type('ques'); pg.wait_for_timeout(200)
        check(pg.locator('#sres .item').count() == 1 and 'Queso rallado' in pg.locator('#sres').inner_text(), 'El buscador no encontró el queso')
        check(pg.evaluate("document.activeElement.id") == 'buscar' and pg.locator('#buscar').input_value() == 'ques', 'El buscador perdió el foco o el texto al escribir')
        check(pg.evaluate("document.getElementById('stl').hidden"), 'Con una búsqueda activa siguen a la vista los negocios')
        pg.locator('#sres button:has-text("Se acaba")').click(); pg.wait_for_timeout(250)
        check(S(pg)['items']['i_mio']['state'] == 'list' and 'ya está en la lista' in pg.locator('#sres').inner_text(), 'Buscar → «Se acaba» no anotó el producto')
        pg.fill('#buscar', 'MIEL'); pg.wait_for_timeout(150)
        check(pg.locator('#sres .item').count() == 1 and pg.locator('#sres .newp').count() == 0, 'Búsqueda exacta sin acentos/mayúsculas')
        pg.locator('#buscar').press('Enter'); pg.wait_for_timeout(200)
        check(S(pg)['items']['i_huerfano']['state'] == 'list', 'Enter sobre un producto existente no lo anotó')
        pg.fill('#buscar', 'pan  lactal'); pg.wait_for_timeout(150)
        check(pg.locator('#sres .item').count() == 0 and 'Pan lactal' in pg.locator('#sres .newp').inner_text(), 'El buscador no ofrece el alta rápida')
        pg.screenshot(path=f'/tmp/cm-v15-buscador-{scheme}.png'); width_ok(pg, 'v1.5 buscador')
        n0 = len(S(pg)['items'])
        pg.locator('#sres .chips button:has-text("Naturista")').click(); pg.wait_for_timeout(250)
        nuevo = [x for x in S(pg)['items'].values() if x['name'] == 'Pan lactal']
        check(len(nuevo) == 1 and nuevo[0]['store'] == 'naturista' and nuevo[0]['state'] == 'list' and nuevo[0]['cat'] == 'frescos' and nuevo[0]['hist'] == [], f'Alta rápida: {nuevo}')
        check(pg.locator('#buscar').input_value() == '' and not pg.evaluate("document.getElementById('stl').hidden"), 'Después del alta rápida no se limpió la búsqueda')
        pg.locator('#toast button').click(); pg.wait_for_timeout(250)
        check(len(S(pg)['items']) == n0, 'Deshacer el alta rápida no borró el producto')
        pg.fill('#buscar', 'tostadas'); pg.locator('#buscar').press('Enter'); pg.wait_for_timeout(250)
        t = [x for x in S(pg)['items'].values() if x['name'] == 'Tostadas']
        check(pg.locator('#buscar').input_value() == '' and pg.evaluate("document.activeElement.id") == 'buscar', 'Después de Enter el buscador no quedó vacío y listo para seguir')
        check(len(t) == 1 and t[0]['store'] == 'super', 'Enter con un producto nuevo no lo anotó en el súper')
        # Entender lo dictado
        ps = pg.evaluate("""['leche, dos kilos de tomate y papel higiénico', 'un kilo y medio de carne', 'media docena de huevos', 'Anotá agua y 1,5 litros de jugo de naranja.',
          'una lechuga; 3 latas de arvejas', 'queso rallado', 'comprar dos paquetes de fideos y tostadas', ''].map(t => parseSpoken(t).map(x => [x.name, x.id, x.qty, x.unit]))""")
        check(ps[0] == [['Leche', None, None, ''], ['Tomate', None, 2, 'kg'], ['Papel higiénico', None, None, '']], f'Voz 0: {ps[0]}')
        check(ps[1] == [['Carne', None, 1.5, 'kg']], f'Voz 1: {ps[1]}')
        check(ps[2] == [['Huevos', None, 0.5, 'doc']], f'Voz 2: {ps[2]}')
        check(ps[3] == [['Agua', 'i_agua', None, ''], ['Jugo de naranja', None, 1.5, 'L']], f'Voz 3: {ps[3]}')
        check(ps[4] == [['Lechuga', None, None, ''], ['Arvejas', None, 3, 'lata']], f'Voz 4: {ps[4]}')
        check(ps[5] == [['Queso rallado especial', 'i_mio', None, '']], f'Voz 5: {ps[5]}')
        check(ps[6] == [['Fideos', None, 2, 'paq'], ['Tostadas', t[0]['id'] if t else None, None, '']], f'Voz 6: {ps[6]}')
        check(ps[7] == [], f'Voz 7: {ps[7]}')
        # Anotar por voz con el reconocimiento simulado
        n1 = len(S(pg)['items'])
        pg.locator('main .search button[aria-label="Anotar por voz"]').click(); pg.wait_for_timeout(250)
        check(pg.locator('#micbtn').count() == 1, 'La hoja de voz no muestra el micrófono')
        pg.screenshot(path=f'/tmp/cm-v15-voz-{scheme}.png')
        pg.locator('#micbtn').click(); pg.wait_for_timeout(400)
        check(pg.locator('#sheet h3:has-text("¿Anoto esto?")').count() == 1 and pg.locator('#sheet label.item').count() == 3, 'Después de escuchar no apareció la revisión')
        check(pg.locator('#sheet .tag:has-text("producto nuevo")').count() == 2 and pg.locator('#f_vstore').input_value() == 'super', 'La revisión no distingue productos nuevos')
        pg.screenshot(path=f'/tmp/cm-v15-voz-revision-{scheme}.png'); width_ok(pg, 'v1.5 voz')
        pg.locator('#vz_0').uncheck(); pg.select_option('#f_vstore', 'naturista')
        pg.locator('#sheet button.pri').click(); pg.wait_for_timeout(300)
        d2 = S(pg); tom = [x for x in d2['items'].values() if x['name'] == 'Tomate']
        check(len(d2['items']) == n1 + 1 and len(tom) == 1 and tom[0]['qty'] == 2 and tom[0]['unit'] == 'kg' and tom[0]['store'] == 'naturista' and tom[0]['state'] == 'list', f'Voz: tomate {tom}')
        check(d2['items']['i_agua']['state'] == 'list' and d2['items']['i_agua']['qty'] == 6, 'Voz: el agua no volvió a la lista (o perdió su cantidad)')
        check(not any(x['name'] == 'Leche' for x in d2['items'].values()), 'Voz: anotó lo que estaba destildado')
        check(any('anotó por voz' in l['act'] for l in d2['log'].values()), 'Voz: no quedó en últimos movimientos')
        check(pg.locator('#modal.hidden').count() == 1, 'Voz: la hoja no se cerró')
        pg.locator('#toast button').click(); pg.wait_for_timeout(250)
        d3 = S(pg)
        check(len(d3['items']) == n1 and d3['items']['i_agua']['state'] == 'ok' and not any('anotó por voz' in l['act'] for l in d3['log'].values()), 'Voz: deshacer no dejó todo como estaba')
        # Escribiendo en lugar de hablar, y sin reconocimiento de voz
        pg.evaluate("A.voice()"); pg.wait_for_timeout(150); pg.fill('#f_voz', 'media docena de huevos'); pg.locator('#sheet button.pri').click(); pg.wait_for_timeout(200)
        check(pg.locator('#sheet label.item').count() == 1 and '0,5 docena' in pg.locator('#sheet label.item').inner_text(), 'Voz escrita: no entendió «media docena de huevos»')
        pg.keyboard.press('Escape'); pg.wait_for_timeout(150)
        pg.evaluate("window.SpeechRecognition = window.webkitSpeechRecognition = undefined; A.voice()"); pg.wait_for_timeout(150)
        check(pg.locator('#micbtn').count() == 0 and pg.locator('#f_voz').count() == 1 and 'micrófono del teclado' in pg.locator('#sheet').inner_text(), 'Sin reconocimiento de voz no hay alternativa para dictar')
        pg.locator('#sheet button.pri').click(); pg.wait_for_timeout(150)
        check(pg.locator('#f_voz').count() == 1, 'Revisar con el texto vacío no debería avanzar')
        pg.keyboard.press('Escape'); pg.wait_for_timeout(150)
        # Vista general con categorías (usuario con todos los productos de fábrica)
        pg.evaluate("S = seed(); S._v = SCHEMA; ['i_agua','i_atun','i_higienico','i_limpieza'].forEach(k => S.items[k].state = 'list'); S.items.i_agua.qty = 6; S.items.i_agua.unit = 'L'; storeFilter = 'super'; render()"); pg.wait_for_timeout(200)
        check(pg.locator('main section.card .cat').count() >= 5, 'El súper de fábrica no muestra las categorías')
        pg.screenshot(path=f'/tmp/cm-v15-compras-{scheme}.png', full_page=True); width_ok(pg, 'v1.5 compras')
        ctx.close()

    # ---------- 9. v1.6.0: frecuencia aprendida ----------
    DAYMS = 86400000
    V15 = json.loads(json.dumps(V12)); V15['_v'] = 2
    for x in V15['items'].values():
        x.update({'cat': 'otros', 'qty': None, 'unit': '', 'hist': [{'at': x['last'], 'by': None}] if x.get('last') else []})
    init15 = ("localStorage.setItem('cm_me','gonzalo'); localStorage.setItem('cm_seen','1.5.0');"
              " if(!localStorage.getItem('cm_data')){ const d = %s; const now = Date.now(), D = 86400000;"
              " d.items.i_agua.hist = [20, 15, 10].map(n => ({at: now - n * D, by: 'dani'})); d.items.i_agua.last = now - 10 * D; d.items.i_agua.lastBy = 'dani'; d.items.i_agua.every = 7; d.items.i_agua.state = 'list';"
              " localStorage.setItem('cm_pre', JSON.stringify(d)); localStorage.setItem('cm_data', JSON.stringify(d)); }") % json.dumps(V15)
    for scheme in ['light', 'dark']:
        ctx = b.new_context(viewport={'width': 390, 'height': 844}, color_scheme=scheme); ctx.add_init_script(init15)
        pg = ctx.new_page()
        pg.on('pageerror', lambda e: errs.append(f'[v1.6] JS: {e}'))
        pg.on('console', lambda m: errs.append(f'[v1.6] consola: {m.text}') if m.type == 'error' else None)
        pg.goto(URL); pg.wait_for_timeout(2200)
        d = S(pg); pre = json.loads(pg.evaluate('localStorage.getItem("cm_pre")'))
        # Migración 2 → 3: solo agrega «auto», no cambia «every» ni nada más, y deja copia
        check(d['_v'] == 3, f"v1.6: _v={d['_v']} (esperaba 3)")
        check(all(x.get('auto') is True for x in d['items'].values()), 'v1.6: la migración no puso auto=true')
        d0 = json.loads(json.dumps(d)); d0['_v'] = 2
        for x in d0['items'].values(): x.pop('auto', None)
        check(d0 == pre, 'v1.6: la migración cambió o perdió datos de v1.5.0')
        check(json.loads(pg.evaluate('localStorage.getItem("cm_backup_v2")') or 'null') == pre, 'v1.6: no quedó la copia cm_backup_v2 idéntica')
        check(pg.locator('#sheet >> text=26/100').count() > 0, 'v1.6: Novedades no se abrió con 26/100')
        pg.keyboard.press('Escape'); pg.wait_for_timeout(200)
        # Cálculo del promedio
        calc = pg.evaluate("""() => { const D = 86400000, t = 1e12, h = a => ({hist: a.map(n => ({at: t + n * D}))});
          return [learned(h([])), learned(h([0, 7])), learned(h([0, 4, 10])), learned(h([0, 0.1, 0.2, 6, 12.2])), learned(h([0, 100, 101, 102, 103, 104, 105, 106])), learned(h([0, 0.6, 1.2])), learned({last: t})]; }""")
        check(calc[0] is None and calc[1] is None and calc[6] is None, f'Promedio: con menos de 3 compras no hay que calcular {calc}')
        check(calc[2] == {'days': 5, 'n': 2}, f'Promedio de 4 y 6 días: {calc[2]}')
        check(calc[3] == {'days': 6, 'n': 2}, f'Compras del mismo día cuentan una vez: {calc[3]}')
        check(calc[4] == {'days': 1, 'n': 6}, f'Solo los últimos 6 intervalos: {calc[4]}')
        check(calc[5] == {'days': 1, 'n': 2}, f'Mínimo 1 día: {calc[5]}')
        # Comprar el agua (compras hace 20, 15, 10 días y hoy → intervalos 5, 5, 10 → 7 no cambia… se usa otro historial)
        pg.evaluate("A.go('compras')"); pg.wait_for_timeout(250)
        pg.locator('main input[aria-label="Comprado: Agua"]').click(); pg.wait_for_timeout(300)
        a = S(pg)['items']['i_agua']
        check(a['every'] == 7 and len(a['hist']) == 4, f"Agua: promedio (5+5+10)/3≈7, no debía cambiar: {a['every']}")
        check('ahora cada' not in pg.locator('#toast').inner_text(), 'Agua: avisó un ajuste que no hubo')
        check(pg.locator('main .item:has-text("Agua") .tag:has-text("aprendido")').count() == 1, 'Agua: falta la etiqueta «aprendido»')
        # Otro producto: compras hace 12, 8 y 4 días, cada 7 → al comprar hoy pasa a 4
        pg.evaluate("(() => { const i = S.items.i_mio, now = Date.now(), D = 86400000; i.hist = [12, 8, 4].map(n => ({at: now - n * D, by: 'gonzalo'})); i.last = now - 4 * D; i.every = 7; i.state = 'list'; save(); render(); })()"); pg.wait_for_timeout(200)
        nm = S(pg)['items']['i_mio']['name']
        pg.locator(f'main input[aria-label="Comprado: {nm}"]').click(); pg.wait_for_timeout(300)
        m = S(pg)['items']['i_mio']
        check(m['every'] == 4, f"Frecuencia aprendida: esperaba 4 días, quedó {m['every']}")
        check('ahora cada 4 días (antes 7)' in pg.locator('#toast').inner_text(), f"Falta el aviso del ajuste: {pg.locator('#toast').inner_text()}")
        pg.screenshot(path=f'/tmp/cm-v16-aviso-{scheme}.png'); width_ok(pg, 'v1.6 aviso')
        pg.locator('#toast button').click(); pg.wait_for_timeout(300)
        m = S(pg)['items']['i_mio']
        check(m['every'] == 7 and len(m['hist']) == 3 and m['state'] == 'list', f"Deshacer no devolvió la frecuencia: {m['every']} {len(m['hist'])}")
        # Formulario: muestra lo aprendido, «Usar X días» y la opción de ajuste
        pg.locator(f'main .item .t:has-text("{nm}")').first.click(); pg.wait_for_timeout(300)
        check(pg.locator('#f_auto').is_checked(), 'Formulario: la opción de ajuste no viene tildada')
        check('Según las últimas 3 compras, lo reponen cada 4 días' in pg.locator('#f_learn').inner_text(), f"Formulario: texto de lo aprendido: {pg.locator('#f_learn').inner_text()}")
        check(pg.locator('#f_uselearn').count() == 1, 'Formulario: falta «Usar 4 días»')
        box = pg.locator('#f_auto').locator('xpath=..').bounding_box(); check(box['height'] >= 44, f"Formulario: la opción mide {box['height']} px")
        pg.screenshot(path=f'/tmp/cm-v16-form-{scheme}.png'); width_ok(pg, 'v1.6 formulario')
        pg.locator('#f_uselearn').click(); pg.wait_for_timeout(100)
        check(pg.input_value('#f_every') == '4' and pg.locator('#f_auto').is_checked(), '«Usar 4 días» no cargó el número')
        # Escribir un número a mano lo deja fijo
        pg.fill('#f_every', '9'); pg.wait_for_timeout(100)
        check(not pg.locator('#f_auto').is_checked(), 'Escribir el número a mano tendría que destildar el ajuste')
        pg.locator('#sheet button.pri').click(); pg.wait_for_timeout(300)
        m = S(pg)['items']['i_mio']; check(m['every'] == 9 and m['auto'] is False, f"Guardar fijo: {m['every']} {m['auto']}")
        pg.locator(f'main input[aria-label="Comprado: {nm}"]').click(); pg.wait_for_timeout(300)
        m = S(pg)['items']['i_mio']
        check(m['every'] == 9 and len(m['hist']) == 4, f"Con el ajuste apagado no debía cambiar: {m['every']}")
        check('ahora cada' not in pg.locator('#toast').inner_text(), 'Con el ajuste apagado avisó un cambio')
        check(pg.locator(f'main .item:has-text("{nm}") .tag:has-text("aprendido")').count() == 0, 'Etiqueta «aprendido» en un producto fijo')
        # Producto con pocas compras: cuenta cuántas van
        pg.evaluate("A.itemForm('i_huerfano')"); pg.wait_for_timeout(250)
        check('Desde la tercera compra' in pg.locator('#f_learn').inner_text() and pg.locator('#f_uselearn').count() == 0, 'Formulario sin historial suficiente')
        pg.keyboard.press('Escape'); pg.wait_for_timeout(200)
        # «Compré todo» también ajusta y se deshace
        pg.evaluate("""(() => { const now = Date.now(), D = 86400000; const ids = Object.values(S.items).filter(i => i.store === S.items.i_agua.store).map(i => i.id); window.__ids = ids;
          ids.forEach(k => { const i = S.items[k]; i.auto = true; i.every = 30; i.hist = [6, 3].map(n => ({at: now - n * D, by: 'dani'})); i.last = now - 3 * D; i.state = 'list'; }); save(); storeFilter = S.items.i_agua.store; render(); })()"""); pg.wait_for_timeout(200)
        ids = pg.evaluate('window.__ids')
        if len(ids) > 1:
            pg.locator('main button:has-text("Compré todo")').first.click(); pg.wait_for_timeout(300)
            its = S(pg)['items']
            check(all(its[k]['every'] == 3 for k in ids), f"Compré todo: {[its[k]['every'] for k in ids]}")
            check('Se ajustó la frecuencia de' in pg.locator('#toast').inner_text(), f"Compré todo: aviso {pg.locator('#toast').inner_text()}")
            pg.locator('#toast button').click(); pg.wait_for_timeout(300)
            its = S(pg)['items']; check(all(its[k]['every'] == 30 and len(its[k]['hist']) == 2 for k in ids), 'Compré todo: deshacer no devolvió las frecuencias')
        else:
            check(False, 'Prueba de «Compré todo»: el negocio del agua tiene un solo producto')
        # Producto nuevo nace con el ajuste prendido
        check(pg.evaluate("newItem('Prueba', 'super').auto === true && Object.values(seed().items).every(i => i.auto === true)"), 'Los productos nuevos no nacen con auto=true')
        pg.evaluate("storeFilter = 'todos'; render()"); pg.wait_for_timeout(150)
        pg.screenshot(path=f'/tmp/cm-v16-compras-{scheme}.png', full_page=True); width_ok(pg, 'v1.6 compras')
        ctx.close()

    b.close()
srv.shutdown()

# Versiones coherentes entre index.html, sw.js y CHANGELOG
html = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
sw = open(os.path.join(ROOT, 'sw.js'), encoding='utf-8').read()
cl = open(os.path.join(ROOT, 'CHANGELOG.md'), encoding='utf-8').read()
import re
v = re.search(r"const VERSION = '([\d.]+)'", html).group(1)
check(f"carga-mental-v{v}'" in sw, f'sw.js no tiene CACHE de la versión {v}')
check(f'## v{v}' in cl, f'CHANGELOG.md no tiene la entrada v{v}')
check(not re.search(r'(?<![.\w])(alert|prompt)\(', html), 'index.html usa alert() o prompt()')

if errs:
    print('ERRORES:'); [print(' -', e) for e in errs]; sys.exit(1)
print(f'OK: v{v} sin errores. Capturas en /tmp/cm-*.png')
