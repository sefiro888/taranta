# Umbral de entrada (retirado)

Cortina de bienvenida con el **arco polilobulado** del restaurante: se dibujan los
contornos, entran las capas de yesería y ataurique, aparece el logotipo dentro del vano
y las dos hojas se abren dejando ver la portada.

Está **fuera de la web** desde el 23 de septiembre de 2026, a petición del cliente.
Todo el trabajo queda aquí guardado y funcionando; volver a activarlo son cuatro pasos.

## Qué hay en esta carpeta

| Archivo | Qué es |
|---|---|
| `arco-polilobulado.svg` | El arco terminado: once lóbulos, moldura festoneada con filete dorado, enjutas y alfiz con ataurique, columnas con capitel y basa |
| `generador-arco.py` | El programa que lo dibuja. La geometría se calcula: reparte los lóbulos sobre la curva, coloca el capitel donde muere el extradós y mide la zona del vano libre para situar el logotipo |
| `umbral.html` | El bloque de la portada, con el SVG ya incrustado |
| `umbral.css` | Los estilos: secuencia de dibujo, capas, apertura de las hojas |
| `intro.js` | El comportamiento: una vez por sesión, saltable con un toque o `Esc`, invisible con «reducir movimiento» activado |

## Para volver a activarlo

1. Pegar el contenido de `umbral.css` al principio de `css/styles.css`, antes del bloque
   `2. BASE/RESET`.
2. Mover `intro.js` a `js/intro.js`.
3. Pegar el contenido de `umbral.html` en `index.html`, justo antes de
   `<section class="hero">`.
4. Añadir `<script src="js/intro.js"></script>` antes del resto de scripts de la portada.

## Para cambiar el arco

`python generador-arco.py` vuelve a dibujarlo y escribe `arco2_generado.svg`. Los
parámetros están arriba del archivo:

- `N_LOBULOS` — número de lóbulos (impar, para que uno quede centrado en la clave)
- `R_INT`, `GROSOR` — radio del vano y grosor de la moldura
- `A_INI`, `A_FIN` — ángulos de arranque; con `A_FIN > 360` el arco es de herradura
- `CY` — sube o baja el arco, y con él la altura de las columnas

Al ejecutarlo imprime dónde queda la zona libre del vano y qué posición y tamaño debe
tener el logotipo, que es lo que hay que poner en `.umbral__logo` del CSS.
