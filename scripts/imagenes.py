# -*- coding: utf-8 -*-
"""Herramientas de imagen del proyecto.

La web espera DOS ficheros por cada foto:

    nombre.jpg      lado largo 1600 px   (la grande)
    nombre-sm.jpg   lado largo  900 px   (la que se carga primero)

`js/carta.js` pide SIEMPRE la version -sm. Si falta, en la carta sale una
imagen rota. Ya paso una vez. Por eso este script genera las dos a la vez
y nunca una sola.

Necesita Pillow:  pip install pillow

USO
---
  python scripts/imagenes.py importar <origen> <nombre-destino>
      Mete una foto en assets/images/ con las dos medidas.
      Acepta jpg, png, webp y avif.

  python scripts/imagenes.py revisar
      Avisa de fotos sin su -sm, de referencias rotas y de fotos
      que no usa nadie.

  python scripts/imagenes.py hoja <carpeta> [salida.jpg]
      Hoja de contacto numerada para mirar muchas fotos de golpe.
      Imprescindible antes de elegir: los nombres de fichero mienten.
"""
import io, os, re, sys, glob, math

# La consola de Windows usa cp1252 y revienta con tildes y simbolos.
# Esto fuerza UTF-8 en la salida; si no se puede, sustituye en vez de fallar.
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass


try:
    from PIL import Image, ImageOps, ImageDraw
except ImportError:
    sys.exit('Falta Pillow:  pip install pillow')
try:
    import pillow_avif  # noqa  (para leer .avif, opcional)
except ImportError:
    pass

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEST = 'assets/images'
GRANDE, PEQUENA = 1600, 900
CALIDAD = 85


def _guardar(im, ruta, lado):
    copia = im.copy()
    copia.thumbnail((lado, lado), Image.LANCZOS)
    copia.save(ruta, 'JPEG', quality=CALIDAD, optimize=True, progressive=True)
    return copia.size, os.path.getsize(ruta) // 1024


def importar(origen, nombre):
    """Una foto nueva, en sus dos medidas."""
    os.chdir(RAIZ)
    nombre = re.sub(r'\.jpe?g$', '', nombre, flags=re.I)
    if not re.match(r'^[a-z0-9-]+$', nombre):
        sys.exit('El nombre solo puede llevar minusculas, numeros y guiones: ' + nombre)
    if not os.path.exists(origen):
        sys.exit('No existe: ' + origen)

    im = ImageOps.exif_transpose(Image.open(origen)).convert('RGB')
    g = '%s/%s.jpg' % (DEST, nombre)
    p = '%s/%s-sm.jpg' % (DEST, nombre)
    tg, kg = _guardar(im, g, GRANDE)
    tp, kp = _guardar(im, p, PEQUENA)
    print('%-34s %-10s %4d KB' % (g, '%dx%d' % tg, kg))
    print('%-34s %-10s %4d KB' % (p, '%dx%d' % tp, kp))
    print()
    print('Para usarla:')
    print('  · en la carta      data/menu-data.js   img: \'%s/%s.jpg\'' % (DEST, nombre))
    print('  · en la galeria    galeria.html        src=-sm  data-grande=la grande')
    print('  · en una provincia scripts/provincias.py  campo foto')


def revisar():
    """Lo que puede estar roto sin que se note hasta que un cliente lo ve."""
    os.chdir(RAIZ)
    grandes = sorted(x.replace(os.sep, '/') for x in glob.glob(DEST + '/*.jpg')
                     if '-sm.' not in x)

    # 1. Fotos sin su version pequena (las de compartir no la necesitan)
    sin = [x for x in grandes
           if not os.path.exists(x.replace('.jpg', '-sm.jpg'))
           and 'compartir' not in x]
    print('Sin version -sm:', len(sin))
    for x in sin:
        print('   ', x)

    # 2. Lo que la carta pide y no existe  <- el fallo clasico
    datos = io.open('data/menu-data.js', encoding='utf-8').read()
    rotas = []
    for img in re.findall(r"img:\s*'([^']+)'", datos):
        chica = img.replace('.jpg', '-sm.jpg')
        if not os.path.exists(chica):
            rotas.append(chica)
    print()
    print('Fotos de la carta sin su -sm (saldrian rotas):', len(rotas))
    for x in rotas:
        print('   ', x)

    # 3. Referencias a ficheros que no existen
    faltan = set()
    for p in glob.glob('*.html') + glob.glob('js/*.js') + glob.glob('data/*.js'):
        s = io.open(p, encoding='utf-8').read()
        for r in re.findall(r'(assets/[A-Za-z0-9_./-]+\.(?:jpg|png|webp|svg|pdf))', s):
            if not os.path.exists(r):
                faltan.add((p, r))
    print()
    print('Referencias rotas:', len(faltan))
    for p, r in sorted(faltan):
        print('    %s -> %s' % (p, r))

    # 4. Fotos que no usa nadie
    usadas = set()
    for p in glob.glob('*.html') + glob.glob('js/*.js') + glob.glob('data/*.js') \
            + glob.glob('scripts/*.py'):
        s = io.open(p, encoding='utf-8').read()
        for r in re.findall(r'([A-Za-z0-9_-]+)\.jpg', s):
            usadas.add(r.replace('-sm', ''))
    huerfanas = [x for x in grandes
                 if os.path.basename(x)[:-4] not in usadas]
    print()
    print('Fotos que no usa ninguna pagina:', len(huerfanas))
    for x in huerfanas:
        print('   ', x)

    peso = sum(os.path.getsize(x) for x in glob.glob(DEST + '/*')) / 1048576
    print()
    print('Peso total de assets/images: %.1f MB' % peso)


def hoja(carpeta, salida=None):
    """Hoja de contacto. Mirar las fotos antes de elegir, siempre."""
    os.chdir(RAIZ)
    ext = ('.jpg', '.jpeg', '.png', '.webp', '.avif')
    fotos = sorted(os.path.join(r, f)
                   for r, _, fs in os.walk(carpeta) for f in fs
                   if f.lower().endswith(ext))
    if not fotos:
        sys.exit('No hay imagenes en ' + carpeta)

    C, COLS = 300, 6
    filas = math.ceil(len(fotos) / COLS)
    lienzo = Image.new('RGB', (COLS * C, filas * (C + 24)), (26, 24, 20))
    d = ImageDraw.Draw(lienzo)
    for i, ruta in enumerate(fotos):
        try:
            im = ImageOps.fit(ImageOps.exif_transpose(Image.open(ruta)).convert('RGB'),
                              (C - 8, C - 8), Image.LANCZOS)
        except Exception as e:
            print('  no se pudo leer', ruta, e)
            continue
        x, y = (i % COLS) * C, (i // COLS) * (C + 24)
        lienzo.paste(im, (x + 4, y + 4))
        d.text((x + 6, y + C + 3), '%d  %s' % (i + 1, os.path.basename(ruta)[:34]),
               fill=(224, 208, 170))

    salida = salida or 'hoja-contacto.jpg'
    lienzo.save(salida, quality=86)
    print('%s  ·  %d fotos' % (salida, len(fotos)))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    orden = sys.argv[1]
    if orden == 'importar' and len(sys.argv) == 4:
        importar(sys.argv[2], sys.argv[3])
    elif orden == 'revisar':
        revisar()
    elif orden == 'hoja' and len(sys.argv) >= 3:
        hoja(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)
    else:
        sys.exit(__doc__)
