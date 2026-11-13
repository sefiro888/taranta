# -*- coding: utf-8 -*-
"""Genera las tarjetas de compartir: una por pagina, 1200x630.

Son las que enseñan WhatsApp, Facebook y Google al pegar un enlace. Foto de
fondo, degradado, un velo suave detras del logotipo y el filete dorado.

Por debajo de 300 KB o WhatsApp no genera miniatura. Las actuales andan por
los 100 KB.

Al anadir una pagina nueva, se anade aqui su linea y se ejecuta:
    python scripts/compartir.py
Y luego hay que apuntar la og:image de esa pagina a la imagen nueva.

Necesita Pillow.
"""
import os
import sys
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PIL import Image, ImageOps, ImageDraw, ImageFilter

# La consola de Windows usa cp1252 y revienta con tildes y simbolos.
# Esto fuerza UTF-8 en la salida; si no se puede, sustituye en vez de fallar.
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass


ANCHO, ALTO = 1200, 630
LOGO = 'assets/logo/logo-marfil.png'          # marca + claim
ISO  = 'assets/logo/isotipo-marfil.png'       # solo el simbolo

# destino -> (foto, tamano del logo, usar logo completo)
PAGINAS = [
    ('compartir',              'tablao.jpg',                 0.46, True),
    ('compartir-degustacion',  'plato-falsa-trufa-jaen.jpg', 0.40, True),
    ('compartir-carta',        'cocina-emplatado.jpg',       0.40, True),
    ('compartir-flamenco',     'tablao-logo-suelo.jpg',      0.42, True),
    ('compartir-restaurante',  'salon-arcos-flores.jpg',     0.42, True),
    ('compartir-chef',         'chef-jose-ignacio.jpg',      0.38, True),
    ('compartir-galeria',      'comedor-artesonado.jpg',     0.42, True),
    ('compartir-historia',     'pasillo-arco-herradura.jpg', 0.42, True),
    ('compartir-eventos',      'arcos-barricas.jpg',         0.42, True),
    ('compartir-reservas',     'comedor-mesas-vestidas.jpg', 0.42, True),
    ('compartir-contacto',     'entrada-rosal.jpg',          0.42, True),
    ('compartir-experiencia',  'comedor-arcos-pintura.jpg',  0.42, True),
    ('compartir-camino',       'entrada-rosal.jpg',          0.42, True),
]


def degradado(w, h):
    """Oscurece arriba y abajo, deja el centro respirar."""
    capa = Image.new('L', (1, h), 0)
    px = capa.load()
    for y in range(h):
        t = y / (h - 1)
        if t < 0.42:
            v = 150 - (150 - 70) * (t / 0.42)        # arriba: 150 -> 70
        else:
            u = (t - 0.42) / 0.58
            v = 70 + (205 - 70) * (u ** 1.5)          # abajo: 70 -> 205
        px[0, y] = int(v)
    return capa.resize((w, h))


mascara = degradado(ANCHO, ALTO)
negro = Image.new('RGB', (ANCHO, ALTO), (18, 16, 13))

for nombre, foto, escala, completo in PAGINAS:
    ruta = 'assets/images/' + foto
    if not os.path.exists(ruta):
        print('!! falta', ruta)
        continue

    base = ImageOps.exif_transpose(Image.open(ruta)).convert('RGB')
    base = ImageOps.fit(base, (ANCHO, ALTO), Image.LANCZOS, centering=(0.5, 0.42))

    # Un punto de desenfoque para que el logotipo despegue del fondo
    base = base.filter(ImageFilter.GaussianBlur(0.6))
    base = Image.composite(negro, base, mascara)

    # Velo suave detras del logotipo: sobre una columna clara el nombre
    # se perdia. Es una elipse muy difuminada, no se nota como mancha.
    velo = Image.new('L', (ANCHO, ALTO), 0)
    dv = ImageDraw.Draw(velo)
    dv.ellipse([int(ANCHO * 0.10), int(ALTO * 0.20),
                int(ANCHO * 0.90), int(ALTO * 0.86)], fill=118)
    velo = velo.filter(ImageFilter.GaussianBlur(90))
    base = Image.composite(negro, base, velo)

    logo = Image.open(LOGO if completo else ISO).convert('RGBA')
    lw = int(ANCHO * escala)
    lh = int(logo.height * lw / logo.width)
    logo = logo.resize((lw, lh), Image.LANCZOS)

    # Sombra suave bajo el logotipo
    sombra = Image.new('RGBA', (lw + 60, lh + 60), (0, 0, 0, 0))
    sombra.paste(logo, (30, 30), logo)
    sombra = sombra.filter(ImageFilter.GaussianBlur(14))
    alpha = sombra.split()[3].point(lambda a: int(a * 0.55))
    oscura = Image.new('RGBA', sombra.size, (0, 0, 0, 255))
    oscura.putalpha(alpha)

    x = (ANCHO - lw) // 2
    y = int(ALTO * 0.5 - lh / 2)
    base.paste(oscura, (x - 30, y - 30 + 6), oscura)
    base.paste(logo, (x, y), logo)

    # Filete dorado fino, como el de la web
    d = ImageDraw.Draw(base, 'RGBA')
    d.rectangle([18, 18, ANCHO - 19, ALTO - 19], outline=(181, 154, 85, 150), width=1)

    salida = 'assets/images/%s.jpg' % nombre
    base.save(salida, 'JPEG', quality=86, optimize=True, progressive=True)
    print('%-28s %s  %d KB' % (salida, base.size, os.path.getsize(salida) // 1024))
