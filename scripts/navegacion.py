# -*- coding: utf-8 -*-
"""Genera la cabecera y el menu movil en todas las paginas.

La navegacion se define UNA VEZ aqui abajo. Al ejecutar el script, se
reescribe el <header> y el panel movil de todos los .html del proyecto.

Asi, con veinticuatro paginas, cambiar el menu es tocar un sitio y
ejecutar:   python scripts/navegacion.py

Las entradas con 'pendiente': True no se pintan todavia. Cuando la pagina
este escrita, se quita esa marca y aparece en las veinticuatro a la vez.
"""
import io, os, re, glob
import sys

# La consola de Windows usa cp1252 y revienta con tildes y simbolos.
# Esto fuerza UTF-8 en la salida; si no se puede, sustituye en vez de fallar.
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass


RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------- LA NAVEGACION
# ('Rotulo', 'fichero.html' o None si es solo un grupo, [hijos], pendiente)
NAV = [
    {'rotulo': 'La mesa', 'hijos': [
        {'rotulo': 'Carta',                  'url': 'carta.html'},
        {'rotulo': 'Menú degustación',       'url': 'menu-degustacion.html'},
        {'rotulo': 'Las ocho provincias',    'url': 'provincias.html',
         'tambien': ['provincia-jaen.html', 'provincia-malaga.html',
                     'provincia-granada.html', 'provincia-cadiz.html',
                     'provincia-cordoba.html', 'provincia-sevilla.html',
                     'provincia-huelva.html', 'provincia-almeria.html']},
        {'rotulo': 'El olivar y el aceite',  'url': 'aceite.html',      'pendiente': True},
        {'rotulo': 'El chef',                'url': 'chef.html'},
    ]},
    {'rotulo': 'La casa', 'hijos': [
        {'rotulo': 'El restaurante',         'url': 'restaurante.html'},
        {'rotulo': 'La experiencia',         'url': 'experiencia.html'},
        {'rotulo': 'El tablao',              'url': 'flamenco.html'},
        {'rotulo': 'Piezas de la Alhambra',  'url': 'alhambra.html',    'pendiente': True},
        {'rotulo': 'Historia',               'url': 'historia.html'},
        {'rotulo': 'Galería',                'url': 'galeria.html'},
    ]},
    {'rotulo': 'Eventos',    'url': 'eventos.html'},
    {'rotulo': 'El Camino',  'url': 'camino-primitivo.html', 'icono': 'concha'},
    {'rotulo': 'Contacto',   'url': 'contacto.html'},
]

RESERVAS = 'reservas.html'
WA = ('https://wa.me/34621153815?text=Hola%2C%20me%20gustar%C3%ADa%20consultar'
      '%20disponibilidad%20para%20reservar%20en%20La%20Taranta.')
TEL = '+34984265252'
TEL_TXT = '984 26 52 52'


# La concha de vieira, el simbolo del Camino. Va delante del rotulo de las
# entradas que llevan 'icono': 'concha'.
CONCHA = ('<svg class="nav__concha" viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
          '<path d="M12 21 8.4 18.2C5 16.6 3 13.2 3 9.6 5.4 6.6 8.5 5 12 5s6.6 1.6 9 4.6c0 3.6-2 7-5.4 8.6Z"/>'
          '<path d="M12 21V6M12 21 7.4 7.6M12 21l4.6-13.4M12 21 4.4 11M12 21l7.6-10"/></svg>')


def rotulo(it):
    return (CONCHA if it.get('icono') == 'concha' else '') + it['rotulo']


def visibles(items):
    return [i for i in items if not i.get('pendiente')]


def ident(texto):
    """Un id estable a partir del rotulo, para enlazar boton y desplegable."""
    base = texto.lower()
    for a, b in (('á','a'),('é','e'),('í','i'),('ó','o'),('ú','u'),('ñ','n'),(' ','-')):
        base = base.replace(a, b)
    return 'nav-' + re.sub(r'[^a-z0-9-]', '', base)


# --------------------------------------------------------------- LA CABECERA
def cabecera(actual):
    filas = []
    for it in visibles(NAV):
        hijos = visibles(it.get('hijos') or [])
        if not it.get('hijos'):
            aqui = ' aria-current="page"' if it.get('url') == actual else ''
            filas.append('      <a href="%s"%s>%s</a>' % (it['url'], aqui, rotulo(it)))
            continue
        if not hijos:
            continue
        dentro = any(h['url'] == actual or actual in (h.get('tambien') or [])
                     for h in hijos)
        gid = ident(it['rotulo'])
        enlaces = '\n'.join(
            '          <a href="%s"%s>%s</a>' %
            (h['url'],
             ' aria-current="page"' if h['url'] == actual else
             (' data-rama="si"' if actual in (h.get('tambien') or []) else ''),
             h['rotulo'])
            for h in hijos)
        filas.append(
            '      <div class="nav__grupo">\n'
            '        <button type="button" class="nav__boton"%s aria-expanded="false" aria-controls="%s">\n'
            '          %s<span class="nav__flecha" aria-hidden="true"></span>\n'
            '        </button>\n'
            '        <div class="nav__panel" id="%s">\n'
            '%s\n'
            '        </div>\n'
            '      </div>'
            % (' data-dentro="si"' if dentro else '', gid, it['rotulo'], gid, enlaces))

    return (
        '<header class="cabecera">\n'
        '  <div class="cabecera__int">\n'
        '    <a class="marca" href="index.html" aria-label="La Taranta, ir a la portada">\n'
        '      <img src="assets/logo/logo-marfil.png" width="949" height="433" '
        'alt="La Taranta · Andalucía en el corazón de Asturias">\n'
        '    </a>\n'
        '    <nav class="nav" aria-label="Navegación principal">\n'
        + '\n'.join(filas) + '\n'
        '    </nav>\n'
        '    <a class="boton boton--cabecera" href="%s">Reservar mesa</a>\n'
        '    <button class="hamburguesa" type="button" aria-label="Abrir el menú" '
        'aria-expanded="false" aria-controls="menu-movil">\n'
        '      <span></span><span></span><span></span>\n'
        '    </button>\n'
        '  </div>\n'
        '</header>' % RESERVAS)


# ------------------------------------------------------------- EL MENU MOVIL
def movil(actual):
    bloques = []
    for it in visibles(NAV):
        hijos = visibles(it.get('hijos') or [])
        if not it.get('hijos'):
            aqui = ' aria-current="page"' if it.get('url') == actual else ''
            bloques.append('    <a class="menu-movil__suelto" href="%s"%s>%s</a>'
                           % (it['url'], aqui, rotulo(it)))
            continue
        if not hijos:
            continue
        enlaces = '\n'.join(
            '      <a href="%s"%s>%s</a>' %
            (h['url'],
             ' aria-current="page"' if h['url'] == actual else
             (' data-rama="si"' if actual in (h.get('tambien') or []) else ''),
             h['rotulo'])
            for h in hijos)
        bloques.append(
            '    <div class="menu-movil__grupo">\n'
            '      <p class="menu-movil__titulo">%s</p>\n'
            '%s\n'
            '    </div>' % (it['rotulo'], enlaces))

    aqui_res = ' aria-current="page"' if actual == RESERVAS else ''
    return (
        '<div class="menu-movil" id="menu-movil">\n'
        '  <nav aria-label="Navegación móvil">\n'
        + '\n'.join(bloques) + '\n'
        '    <a class="menu-movil__suelto" href="%s"%s>Reservar mesa</a>\n'
        '  </nav>\n'
        '  <div class="menu-movil__pie">\n'
        '    <a class="boton" href="%s">Reservar mesa</a>\n'
        '    <a class="boton boton--wa" href="%s" target="_blank" rel="noopener">WhatsApp</a>\n'
        '    <a class="boton boton--fantasma" href="tel:%s">Llamar %s</a>\n'
        '  </div>\n'
        '</div>' % (RESERVAS, aqui_res, RESERVAS, WA, TEL, TEL_TXT))


# -------------------------------------------------------------------- APLICAR
def aplicar():
    os.chdir(RAIZ)
    tocadas = 0
    for p in sorted(glob.glob('*.html')):
        s = io.open(p, encoding='utf-8').read()
        o = s

        s, n1 = re.subn(r'<header class="cabecera">.*?</header>',
                        lambda m: cabecera(p), s, count=1, flags=re.S)
        if n1 == 0:
            # Pagina recien generada: aun no tiene cabecera, se pone tras <body>
            s, n1 = re.subn(r'<body>\n',
                            lambda m: '<body>\n' + cabecera(p) + '\n',
                            s, count=1)

        s, n2 = re.subn(r'<div class="menu-movil" id="menu-movil">.*?\n</div>',
                        lambda m: movil(p), s, count=1, flags=re.S)
        if n2 == 0:
            s, n2 = re.subn(r'</header>\n',
                            lambda m: '</header>\n' + movil(p) + '\n',
                            s, count=1)

        if n1 == 0:
            print('  !! no se pudo poner la cabecera:', p)
        if n2 == 0:
            print('  !! no se pudo poner el menu movil:', p)
        if s != o:
            io.open(p, 'w', encoding='utf-8', newline='').write(s)
            tocadas += 1

    pend = []
    for it in NAV:
        if it.get('pendiente'):
            pend.append(it['rotulo'])
        for h in it.get('hijos') or []:
            if h.get('pendiente'):
                pend.append(h['rotulo'])

    print('paginas actualizadas:', tocadas)
    if pend:
        print('todavia sin escribir (no salen en el menu):')
        for x in pend:
            print('   ·', x)


if __name__ == '__main__':
    aplicar()
