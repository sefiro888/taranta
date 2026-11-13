# -*- coding: utf-8 -*-
"""Reconstruye el sitio entero, en el orden correcto, y lo revisa.

ESTE ES EL COMANDO QUE HAY QUE EJECUTAR DESPUES DE CUALQUIER CAMBIO:

    python scripts/construir.py

Hace, por este orden:

  1. provincias.py   las nueve paginas de provincias
  2. navegacion.py   la cabecera y el menu movil en todas
  3. sitemap.py      sitemap.xml y robots.txt
  4. cache.py        las firmas ?v= de los CSS y JS
  5. una revision    enlaces rotos, imagenes que faltan, avisos

El orden importa: navegacion.py tiene que correr DESPUES de provincias.py,
porque las paginas nuevas no tienen cabecera hasta que pasa por ellas. Y
cache.py va el ultimo, cuando ya nadie va a tocar un .css o un .js.

Es idempotente: ejecutarlo dos veces seguidas no cambia nada.
"""
import io, os, re, sys, glob, subprocess

# La consola de Windows usa cp1252 y revienta con tildes y simbolos.
# Esto fuerza UTF-8 en la salida; si no se puede, sustituye en vez de fallar.
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass


RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AQUI = os.path.dirname(os.path.abspath(__file__))


def paso(n, titulo, script):
    print()
    print('── %d · %s' % (n, titulo))
    r = subprocess.run([sys.executable, '-I', os.path.join(AQUI, script)],
                       capture_output=True, text=True, encoding='utf-8', errors='replace')
    for linea in (r.stdout or '').strip().splitlines():
        print('   ' + linea)
    if r.returncode != 0:
        print('   ERROR:')
        for linea in (r.stderr or '').strip().splitlines()[-12:]:
            print('   ' + linea)
        sys.exit('\nFallo en %s. No sigo.' % script)


def revisar():
    """Lo que puede estar roto y no se ve hasta que lo ve un cliente."""
    os.chdir(RAIZ)
    print()
    print('── 5 · Revisión')

    paginas = sorted(glob.glob('*.html'))
    rotos, faltan, sin_firma = set(), set(), set()

    for p in paginas:
        s = io.open(p, encoding='utf-8').read()
        for r in re.findall(r'href="([a-z0-9-]+\.html)"', s):
            if not os.path.exists(r):
                rotos.add((p, r))
        for r in re.findall(r'(assets/[A-Za-z0-9_./-]+\.(?:jpg|png|webp|svg|pdf))', s):
            if not os.path.exists(r):
                faltan.add((p, r))
        for r in re.findall(r'(?:css|js|data)/[A-Za-z0-9_-]+\.(?:css|js)(?!\?v=)', s):
            sin_firma.add((p, r))
        if '<header class="cabecera">' not in s:
            rotos.add((p, 'SIN CABECERA'))
        if 'id="menu-movil"' not in s:
            rotos.add((p, 'SIN MENU MOVIL'))

    # La carta pide siempre la version -sm: si falta, sale rota
    datos = io.open('data/menu-data.js', encoding='utf-8').read()
    carta_rota = [i.replace('.jpg', '-sm.jpg') for i in re.findall(r"img:\s*'([^']+)'", datos)
                  if not os.path.exists(i.replace('.jpg', '-sm.jpg'))]

    print('   páginas:                 %d' % len(paginas))
    print('   enlaces rotos:           %d' % len(rotos))
    print('   imágenes que faltan:     %d' % len(faltan))
    print('   fotos de carta sin -sm:  %d' % len(carta_rota))
    print('   referencias sin firma:   %d' % len(sin_firma))

    mal = False
    for etiqueta, conjunto in [('ENLACE ROTO', rotos), ('IMAGEN QUE FALTA', faltan),
                               ('SIN FIRMA', sin_firma)]:
        for a, b in sorted(conjunto):
            print('   ⚠️  %s · %s → %s' % (etiqueta, a, b))
            mal = True
    for x in carta_rota:
        print('   ⚠️  FOTO DE CARTA ROTA · %s' % x)
        mal = True

    peso = sum(os.path.getsize(x) for x in glob.glob('assets/images/*')) / 1048576
    print('   peso de assets/images:   %.1f MB' % peso)
    if peso > 10:
        print('   ℹ️  Pendiente: pasar las imágenes a formatos modernos')

    print()
    print('   ✅ Todo correcto.' if not mal else '   ❌ Hay cosas que arreglar, arriba.')
    return not mal


if __name__ == '__main__':
    print('Reconstruyendo La Taranta')
    paso(1, 'Páginas de provincias', 'provincias.py')
    paso(2, 'Navegación', 'navegacion.py')
    paso(3, 'Sitemap y robots', 'sitemap.py')
    paso(4, 'Firmas de caché', 'cache.py')
    ok = revisar()
    print()
    print('Para verlo:  python .claude/servidor-demo.py   →  http://localhost:8123')
    sys.exit(0 if ok else 1)
