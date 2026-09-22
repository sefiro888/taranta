# -*- coding: utf-8 -*-
"""
Arco polilobulado del local: lóbulos festoneados en el intradós, enjutas
con ataurique, alfiz con friso y columnas cilíndricas con capitel y basa.
Todo calculado: los lóbulos se reparten sobre la curva base del arco.
"""
import math

W, H = 420, 470
CX = 210
SUELO = 470
CY = 196          # centro de la circunferencia del arco (arriba: columnas largas)
R_INT = 104       # radio del borde interior del arco
GROSOR = 34       # grosor de la rosca
R_EXT = R_INT + GROSOR
N_LOBULOS = 11    # impar: uno centrado en la clave
A_INI = 158       # ángulo de arranque (grados)
A_FIN = 382       # ángulo final; >360 para que sea herradura


def pt(cx, cy, r, grados):
    a = math.radians(grados)
    return (cx + r * math.cos(a), cy + r * math.sin(a))


def festón(r, invertido=False):
    """Cadena de lóbulos sobre la circunferencia de radio r."""
    pasos = [A_INI + (A_FIN - A_INI) * i / N_LOBULOS for i in range(N_LOBULOS + 1)]
    if invertido:
        pasos = list(reversed(pasos))
    puntos = [pt(CX, CY, r, g) for g in pasos]
    # radio de cada lóbulo: media cuerda entre dos puntos consecutivos
    cuerda = math.dist(puntos[0], puntos[1])
    rl = cuerda / 2 * 1.02
    d = ''
    for i in range(1, len(puntos)):
        x, y = puntos[i]
        # sweep 0 = el lóbulo abomba hacia el centro del vano
        d += ' A%.1f %.1f 0 0 %d %.1f %.1f' % (rl, rl, 1 if invertido else 0, x, y)
    return puntos[0], puntos[-1], d


# --- intradós y extradós, ambos festoneados ---
i0, i1, D_INT = festón(R_INT)
e0, e1, D_EXT = festón(R_EXT)
e1r, e0r, D_EXT_INV = festón(R_EXT, invertido=True)

# jambas: bajan desde el arranque del arco hasta el suelo
JAMBA_IZQ_X, JAMBA_DER_X = i0[0], i1[0]
EXT_IZQ_X, EXT_DER_X = e0[0], e1[0]

# la rosca es un trazo grueso sobre el festón medio: así sigue los lóbulos
R_MEDIO = R_INT + GROSOR / 2
m0, m1, D_MED = festón(R_MEDIO)
ROSCA = ('M%.1f %.1f L%.1f %.1f' % (m0[0], SUELO, m0[0], m0[1]) + D_MED +
         ' L%.1f %.1f' % (m1[0], SUELO))

# vano: el hueco interior, para la luz y el recorte
VANO = ('M%.1f %.1f' % (i0[0], SUELO) + ' L%.1f %.1f' % i0 + D_INT +
        ' L%.1f %.1f' % (i1[0], SUELO) + ' Z')

# alfiz
ALF_X0, ALF_X1, ALF_Y = 26, 394, 44
BANDA_ALF = 30
ALFIZ = ('M%d %d L%d %d L%d %d L%d %d Z M%d %d L%d %d L%d %d L%d %d Z'
         % (ALF_X0, SUELO, ALF_X0, ALF_Y, ALF_X1, ALF_Y, ALF_X1, SUELO,
            ALF_X0 + BANDA_ALF, SUELO, ALF_X0 + BANDA_ALF, ALF_Y + BANDA_ALF,
            ALF_X1 - BANDA_ALF, ALF_Y + BANDA_ALF, ALF_X1 - BANDA_ALF, SUELO))

# enjutas: lo que queda entre el extradós y el interior del alfiz
ENJUTAS = ('M%d %d L%d %d L%d %d L%d %d Z '
           % (ALF_X0 + BANDA_ALF, SUELO, ALF_X0 + BANDA_ALF, ALF_Y + BANDA_ALF,
              ALF_X1 - BANDA_ALF, ALF_Y + BANDA_ALF, ALF_X1 - BANDA_ALF, SUELO)
           + 'M%.1f %.1f' % (e0[0], SUELO) + ' L%.1f %.1f' % e0 + D_EXT +
           ' L%.1f %.1f' % (e1[0], SUELO) + ' Z')
# el vano llega hasta el borde interior de la rosca
VANO = ('M%.1f %.1f' % (i0[0], SUELO) + ' L%.1f %.1f' % i0 + D_INT +
        ' L%.1f %.1f' % (i1[0], SUELO) + ' Z')

# --- columnas ---
COL_R = 17
COL_IZQ = e0[0] - 2
COL_DER = e1[0] + 2
# el capitel arranca donde muere el extradós del arco
COL_TOP = round(max(e0[1], e1[1])) + 4


def ataurique():
    """Patrón vegetal: roleos con palmetas, al modo del ataurique tallado."""
    p = []
    for dx, dy in [(0, 0), (26, 26)]:
        p.append('<path d="M%d %d c 6 -9 16 -9 21 0 c 5 9 -5 16 -11 11 c -5 -4 -2 -12 4 -12"/>' % (dx + 2, dy + 20))
        p.append('<path d="M%d %d c -6 -9 -16 -9 -21 0 c -5 9 5 16 11 11 c 5 -4 2 -12 -4 -12"/>' % (dx + 24, dy + 6))
        p.append('<path d="M%d %d q 7 -8 14 0 q -7 6 -14 0z"/>' % (dx + 5, dy + 3))
        p.append('<path d="M%d %d q 7 8 14 0 q -7 -6 -14 0z"/>' % (dx + 8, dy + 23))
    return ''.join(p)


SVG = '''<svg class="umbral__arco" viewBox="0 0 {W} {H}" aria-hidden="true" focusable="false">
  <defs>
    <linearGradient id="yeso" x1="0" y1="0" x2=".3" y2="1">
      <stop offset="0" stop-color="#F3E9D6"/>
      <stop offset=".4" stop-color="#DCCBA8"/>
      <stop offset="1" stop-color="#A08D6B"/>
    </linearGradient>
    <linearGradient id="yesoArco" x1="0" y1="0" x2=".25" y2="1">
      <stop offset="0" stop-color="#FBF5E8"/>
      <stop offset=".45" stop-color="#EDE0C6"/>
      <stop offset="1" stop-color="#C0AC86"/>
    </linearGradient>
    <linearGradient id="yesoFriso" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#D3C4A2"/>
      <stop offset="1" stop-color="#8E7C5C"/>
    </linearGradient>
    <linearGradient id="fusteCol" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#8E7F62"/>
      <stop offset=".22" stop-color="#EFE7D6"/>
      <stop offset=".55" stop-color="#D9CCB2"/>
      <stop offset="1" stop-color="#8A7A5D"/>
    </linearGradient>
    <radialGradient id="luz" cx=".5" cy=".6" r=".85">
      <stop offset="0" stop-color="#C08F55" stop-opacity=".5"/>
      <stop offset=".45" stop-color="#8A6338" stop-opacity=".34"/>
      <stop offset="1" stop-color="#211C15" stop-opacity=".08"/>
    </radialGradient>
    <radialGradient id="sombraLogo" cx=".5" cy=".5" r=".5">
      <stop offset="0" stop-color="#140F0A" stop-opacity=".5"/>
      <stop offset="1" stop-color="#140F0A" stop-opacity="0"/>
    </radialGradient>
    <pattern id="ataurique" width="26" height="26" patternUnits="userSpaceOnUse">
      <g fill="none" stroke="#7A6845" stroke-width=".85" opacity=".62">{ATAURIQUE}</g>
    </pattern>
    <filter id="relieve" x="-15%" y="-15%" width="130%" height="130%">
      <feDropShadow dx="1.4" dy="2" stdDeviation="1.3" flood-color="#0B0A08" flood-opacity=".55"/>
    </filter>
  </defs>

  <!-- luz del vano -->
  <g class="cap cap--luz"><path d="{VANO}" fill="url(#luz)"/></g>
  <g class="cap cap--sombraLogo"><ellipse cx="{CX}" cy="{LOGO_CY}" rx="100" ry="58" fill="url(#sombraLogo)"/></g>

  <!-- enjutas y alfiz, tallados -->
  <g class="cap cap--alfiz" filter="url(#relieve)">
    <path d="{ENJUTAS}" fill="url(#yesoFriso)" fill-rule="evenodd"/>
    <path d="{ENJUTAS}" fill="url(#ataurique)" fill-rule="evenodd"/>
    <path d="{ALFIZ}" fill="url(#yesoFriso)" fill-rule="evenodd"/>
    <path d="{ALFIZ}" fill="url(#ataurique)" fill-rule="evenodd"/>
  </g>

  <!-- la rosca festoneada: trazo grueso que sigue los lóbulos -->
  <g class="cap cap--arco" filter="url(#relieve)">
    <path d="{ROSCA}" fill="none" stroke="url(#yesoArco)" stroke-width="{GROSOR}" stroke-linejoin="round" stroke-linecap="butt"/>
    <path d="{ROSCA}" fill="none" stroke="url(#ataurique)" stroke-width="{GROSOR}" stroke-linejoin="round" stroke-linecap="butt"/>
    <path d="M{INT_IZQ_X} {SUELO} L{I0X} {I0Y}{D_INT} L{INT_DER_X} {SUELO}" fill="none" stroke="#C6A863" stroke-width="1.5" stroke-opacity=".85" stroke-linejoin="round"/>
    <path d="M{EXT_IZQ_X} {SUELO} L{E0X} {E0Y}{D_EXT} L{EXT_DER_X} {SUELO}" fill="none" stroke="#C6A863" stroke-width="1.5" stroke-opacity=".7" stroke-linejoin="round"/>
  </g>

  <!-- columnas: fuste, capitel y basa -->
  <g class="cap cap--columnas" filter="url(#relieve)">
    <rect x="{COL_IZQ_X}" y="{COL_TOP}" width="{COL_W}" height="{COL_H}" fill="url(#fusteCol)"/>
    <rect x="{COL_DER_X}" y="{COL_TOP}" width="{COL_W}" height="{COL_H}" fill="url(#fusteCol)"/>
    <rect x="{CAP_IZQ_X}" y="{CAP_Y}" width="{CAP_W}" height="26" rx="2" fill="url(#yeso)"/>
    <rect x="{CAP_DER_X}" y="{CAP_Y}" width="{CAP_W}" height="26" rx="2" fill="url(#yeso)"/>
    <rect x="{CAP_IZQ_X}" y="{CAP_Y}" width="{CAP_W}" height="26" rx="2" fill="url(#ataurique)"/>
    <rect x="{CAP_DER_X}" y="{CAP_Y}" width="{CAP_W}" height="26" rx="2" fill="url(#ataurique)"/>
    <rect x="{CAP_IZQ_X}" y="{BASA_Y}" width="{CAP_W}" height="14" rx="2" fill="url(#yeso)"/>
    <rect x="{CAP_DER_X}" y="{BASA_Y}" width="{CAP_W}" height="14" rx="2" fill="url(#yeso)"/>
  </g>

  <!-- contornos, que son los que se dibujan primero -->
  <g class="trazos" fill="none" stroke="#C9AE69" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round">
    <path class="t1" d="M{EXT_IZQ_X} {SUELO} L{E0X} {E0Y}{D_EXT} L{EXT_DER_X} {SUELO}"/>
    <path class="t2" d="M{INT_IZQ_X} {SUELO} L{I0X} {I0Y}{D_INT} L{INT_DER_X} {SUELO}"/>
    <path class="t3" d="M{ALF_X0} {SUELO} L{ALF_X0} {ALF_Y} L{ALF_X1} {ALF_Y} L{ALF_X1} {SUELO}"/>
    <path class="t3" d="M{ALF_IN0} {SUELO} L{ALF_IN0} {ALF_IN_Y} L{ALF_IN1} {ALF_IN_Y} L{ALF_IN1} {SUELO}"/>
  </g>
</svg>'''

rep = {
    '{W}': W, '{H}': H, '{CX}': CX, '{SUELO}': SUELO,
    '{VANO}': VANO, '{ROSCA}': ROSCA, '{ALFIZ}': ALFIZ, '{ENJUTAS}': ENJUTAS,
    '{ATAURIQUE}': ataurique(),
    '{D_EXT}': D_EXT, '{D_INT}': D_INT,
    '{E0X}': '%.1f' % e0[0], '{E0Y}': '%.1f' % e0[1],
    '{I0X}': '%.1f' % i0[0], '{I0Y}': '%.1f' % i0[1],
    '{EXT_IZQ_X}': '%.1f' % e0[0], '{EXT_DER_X}': '%.1f' % e1[0],
    '{INT_IZQ_X}': '%.1f' % i0[0], '{INT_DER_X}': '%.1f' % i1[0],
    '{ALF_X0}': ALF_X0, '{ALF_X1}': ALF_X1, '{ALF_Y}': ALF_Y,
    '{ALF_IN0}': ALF_X0 + BANDA_ALF, '{ALF_IN1}': ALF_X1 - BANDA_ALF,
    '{ALF_IN_Y}': ALF_Y + BANDA_ALF,
    '{LOGO_CY}': '%.0f' % (235 + 235 * 0.40),
    '{GROSOR}': GROSOR, '{MEDIO_GROSOR}': GROSOR / 2,
    '{COL_IZQ_X}': '%.1f' % (e0[0] - COL_R), '{COL_DER_X}': '%.1f' % (e1[0] - COL_R),
    '{COL_W}': COL_R * 2, '{COL_TOP}': COL_TOP, '{COL_H}': SUELO - COL_TOP,
    '{CAP_IZQ_X}': '%.1f' % (e0[0] - COL_R - 5), '{CAP_DER_X}': '%.1f' % (e1[0] - COL_R - 5),
    '{CAP_W}': COL_R * 2 + 10, '{CAP_Y}': COL_TOP - 26, '{BASA_Y}': SUELO - 14,
}
for k, v in rep.items():
    SVG = SVG.replace(k, str(v))

open('arco2_generado.svg', 'w', encoding='utf-8').write(SVG)

# zona del vano libre de lóbulos: por debajo del arranque del intradós
LIBRE_Y0 = max(i0[1], i1[1])
LIBRE_ALTO = SUELO - LIBRE_Y0
LOGO_CY = LIBRE_Y0 + LIBRE_ALTO * 0.40
ANCHO_VANO = i1[0] - i0[0]

print('zona libre del vano: y de %.0f a %d (%.0f px de alto)' % (LIBRE_Y0, SUELO, LIBRE_ALTO))
print('logotipo -> top: %.1f%%   ancho maximo: %.0f%% del svg'
      % (LOGO_CY / H * 100, ANCHO_VANO * 0.78 / W * 100))
print('lóbulos:', N_LOBULOS)
print('arranque izq x=%.1f  der x=%.1f  (eje %d)' % (i0[0], i1[0], CX))
print('simetría intradós:', abs((i0[0] + i1[0]) / 2 - CX) < 0.5)
print('simetría extradós:', abs((e0[0] + e1[0]) / 2 - CX) < 0.5)
print('bytes', len(SVG))
