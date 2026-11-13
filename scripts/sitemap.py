# -*- coding: utf-8 -*-
"""Genera sitemap.xml y robots.txt a partir de las paginas que existen.

Asi no hay que acordarse de anadir cada pagina nueva a mano.

Uso:  python scripts/sitemap.py
"""
import io, os, glob, datetime
import sys

# La consola de Windows usa cp1252 y revienta con tildes y simbolos.
# Esto fuerza UTF-8 en la salida; si no se puede, sustituye en vez de fallar.
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass


RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOM = 'https://www.latarantaoviedo.com'

# Importancia relativa. Lo que no este aqui usa el valor por defecto.
PRIO = {
    'index.html': '1.0',
    'carta.html': '0.9', 'menu-degustacion.html': '0.9', 'reservas.html': '0.9',
    'restaurante.html': '0.8', 'experiencia.html': '0.8', 'flamenco.html': '0.8',
    'provincias.html': '0.8', 'camino-primitivo.html': '0.8',
    'chef.html': '0.7', 'historia.html': '0.7', 'eventos.html': '0.7',
    'galeria.html': '0.6', 'contacto.html': '0.6',
    'politica-privacidad.html': '0.2',
}
POR_DEFECTO = '0.6'   # las fichas de provincia y lo que venga


def generar():
    os.chdir(RAIZ)
    fecha = datetime.date.today().isoformat()
    paginas = sorted(glob.glob('*.html'),
                     key=lambda p: (-float(PRIO.get(p, POR_DEFECTO)), p))

    filas = []
    for p in paginas:
        url = DOM + '/' + ('' if p == 'index.html' else p)
        filas.append('  <url>\n'
                     '    <loc>%s</loc>\n'
                     '    <lastmod>%s</lastmod>\n'
                     '    <priority>%s</priority>\n'
                     '  </url>' % (url, fecha, PRIO.get(p, POR_DEFECTO)))

    io.open('sitemap.xml', 'w', encoding='utf-8', newline='\n').write(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + '\n'.join(filas) + '\n</urlset>\n')

    io.open('robots.txt', 'w', encoding='utf-8', newline='\n').write(
        '# La Taranta · Oviedo\n'
        'User-agent: *\n'
        'Allow: /\n'
        '\n'
        'Sitemap: %s/sitemap.xml\n' % DOM)

    print('sitemap.xml con', len(filas), 'paginas')
    print('robots.txt')


if __name__ == '__main__':
    generar()
