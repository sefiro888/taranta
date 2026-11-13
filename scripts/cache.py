# -*- coding: utf-8 -*-
"""Regenera las firmas de cache de los CSS, JS y datos.

Cada referencia lleva ?v=<hash>, con los ocho primeros caracteres del MD5 del
fichero. Si no se regenera despues de tocar un .css o un .js, los navegadores
siguen sirviendo la version vieja y el cambio no se ve.

Es el paso que mas se olvida. Por eso tiene su propio comando y por eso
`construir.py` lo llama siempre al final.

Uso:  python scripts/cache.py
"""
import io, os, re, glob, hashlib
import sys

# La consola de Windows usa cp1252 y revienta con tildes y simbolos.
# Esto fuerza UTF-8 en la salida; si no se puede, sustituye en vez de fallar.
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass


RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATRON = re.compile(r'((?:css|js|data)/[A-Za-z0-9_-]+\.(?:css|js))(\?v=[0-9a-f]{8})?')


def firmas():
    return {r.replace(os.sep, '/'): hashlib.md5(io.open(r, 'rb').read()).hexdigest()[:8]
            for r in glob.glob('css/*.css') + glob.glob('js/*.js') + glob.glob('data/*.js')}


def aplicar():
    os.chdir(RAIZ)
    h = firmas()
    tocadas, refs = 0, 0

    def rep(m):
        nonlocal refs
        ruta = m.group(1)
        if ruta not in h:
            print('  !! referencia a un fichero que no existe:', ruta)
            return m.group(0)
        refs += 1
        return ruta + '?v=' + h[ruta]

    for p in sorted(glob.glob('*.html')):
        s = io.open(p, encoding='utf-8').read()
        n = PATRON.sub(rep, s)
        if n != s:
            io.open(p, 'w', encoding='utf-8', newline='').write(n)
            tocadas += 1

    print('firmas: %d referencias en %d paginas (%d reescritas)'
          % (refs, len(glob.glob('*.html')), tocadas))
    return tocadas


if __name__ == '__main__':
    aplicar()
