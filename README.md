# La Taranta · Demostración web

**Andalucía en el corazón de Asturias**
Demostración de diseño y desarrollo preparada para presentar una propuesta al restaurante
La Taranta (calle Rosal, 22-24, Oviedo). No es la web oficial del restaurante.

Para verla: abra `index.html` en el navegador (funciona sin servidor), o ejecute
`python .claude/servidor-demo.py` y visite `http://localhost:8123`.
En línea: **https://sefiro888.github.io/taranta/**

**Antes de la reunión con el restaurante, lea [PARA-LA-REUNION.md](PARA-LA-REUNION.md)**:
recoge el guion de lo que enseñar, las preguntas que hacer, los 15 datos a confirmar, los
3 permisos que hay que pedir, el material que debe aportar el cliente y el catálogo
completo de 75 mejoras con su estado.

---

## 1. Estructura de archivos

```
flamecontaranta/
├── PARA-LA-REUNION.md         Guion, preguntas, datos a confirmar, material que
│                              debe aportar el cliente y las 75 mejoras posibles
├── index.html                 Portada (foto del patio con los geranios)
├── experiencia.html           La visita, en nueve momentos
├── carta.html                 Carta digital con filtros y buscador
├── menu-degustacion.html      Las ocho provincias + mapa interactivo
├── restaurante.html           El Patio · El Cortijo · La Bodega · El Tablao
├── flamenco.html              El tablao y formulario de consulta
├── eventos.html               Página comercial de eventos y grupos
├── galeria.html               Galería filtrable con lightbox
├── reservas.html              Formulario, horarios, mapa e info de grupos
├── historia.html              Origen, nombre, cocina, casa y oficios
├── contacto.html              Datos, horarios, cómo llegar, FAQ y formulario
├── politica-privacidad.html   Aviso legal, privacidad y créditos
│
├── css/styles.css             Sistema visual completo
├── css/responsive.css         Adaptación a 1440 / 1180 / 1024 / 768 / 520 / 380 px
│
├── js/main.js                 Cabecera, menú móvil, animaciones, flotantes
├── js/mapa-andalucia.js       Mapa SVG interactivo + listado de pases
├── js/carta.js                Render de la carta, filtros y búsqueda
├── js/gallery.js              Filtros de galería y lightbox accesible
├── js/reservas.js             Validación de formularios y enlaces de WhatsApp
│
├── data/menu-data.js          Carta, provincias y menú degustación (fuente única)
│
├── assets/logo/               Logotipo real en sus distintas versiones
├── assets/images/             Fotografías optimizadas (1800 px y 900 px)
│
├── extras/umbral/             Umbral de entrada, retirado de la web pero guardado
│                              (arco polilobulado, su generador, CSS y JS)
├── logo.jpg                   Archivo original del cliente (sin modificar)
├── _material-original/        Descargas originales sin procesar (no forman parte de la web)
└── .claude/servidor-demo.py   Servidor local opcional para previsualizar
```

## 2. El logotipo

Se ha usado **el logotipo real facilitado** (`logo.jpg`), sin rediseñarlo ni sustituirlo.
A partir de él se generaron, respetando forma y proporciones:

| Archivo | Uso |
|---|---|
| `logo-marfil.png` | Cabecera, pie y portada sobre fondos oscuros |
| `logo-oliva.png` | Versión para fondos claros |
| `logo-arena.png` | Variante auxiliar |
| `isotipo-oliva/marfil/dorado.png` | Separadores ornamentales y detalles |
| `favicon-32/180/512.png`, `favicon.ico` | Icono del navegador y de móvil |

El color de marca se ha muestreado del propio archivo: **#7E7824** (el brief indicaba
#807A18; se ha usado el valor exacto del logotipo). El resto de la paleta sigue el brief:
oliva oscuro #4E5428, carbón #171511, marfil #F4EBDD, arena #D8C7A6, terracota #A64F32,
dorado envejecido #B59A55, granate #542B26 y marrón madera #3A2B20.

## 3. Funcionalidades

- **Mapa interactivo de Andalucía** en SVG, con las ocho provincias reales: hover e
  iluminación en escritorio, toque y botones de provincia en móvil, panel con el pase
  correspondiente, navegación anterior/siguiente, teclado (Tab, Enter, flechas) y
  `aria-label` por provincia.
- **Tres cartas en una**: Desayunos (molletes de Antequera y tortillas), Raciones y
  barra (con precio de media y entera) y Carta de autor. Selector de carta, filtros por
  categoría y buscador que salta solo a la carta donde está el plato. Etiquetas de
  «mínimo 2 personas», tiempo de elaboración y unidades (`/persona`, `/kg`, `/unidad`).
- **Ficha ampliada de plato**: los platos cuya fotografía identificó el propio
  restaurante en Instagram se abren a pantalla completa con la foto, el precio y acceso
  directo a reservar o preguntar por WhatsApp.
- **El poema del azulejo** (`flamenco.html#poema`): el poema que cuelga en la pared del
  restaurante, transcrito y revelado estrofa a estrofa, junto a la foto del panel.
- **La arquería** (`restaurante.html`): los cuatro espacios en cuatro vanos de arco
  nazarí. Al pasar el cursor o tocar uno, se ilumina, los demás se atenúan y el panel
  cuenta la zona. Es una composición visual, no un plano de la distribución real.
- **La trayectoria del chef** en `historia.html`: los cuatro galardones de José Ignacio
  López presentados como piezas, y **La alacena** en `carta.html`: el AOVE de marca
  propia y la bodega de referencias andaluzas.
- **Menú degustación** con los nueve pases y el mapa como hilo conductor, encabezado por
  una **ficha de la experiencia** servida desde `data/menu-data.js`: precio (75,00 €),
  nueve pases, recorrido de Jaén a Almería, 48 horas de antelación y maridaje de vinos del
  sur. Los tres campos que siguen sin confirmar —duración, mínimo de comensales y días
  disponibles— aparecen con línea de puntos, listos para rellenar con el restaurante.
  Cada pase lleva además su nombre oficial: «Simplemente Jaén», «Málaga la bella»,
  «De chirigotas por Cádiz»…
- **Galería** con filtros (espacios, cocina, tablao, detalles), lightbox con teclado
  (flechas y `Esc`), gesto de deslizar en táctil, contador y foco atrapado.
- **Reserva en línea real**: el widget de **Tableo** del propio restaurante, incrustado en
  `reservas.html#reservar` con los colores de la casa (fondo marfil, campos arena, botón
  oliva, tipografía Jost). Reserva con confirmación inmediata, no una simulación. Incluye
  aviso de carga mientras se descarga y ajuste automático de altura si el widget lo
  comunica. Los botones flotantes se apartan mientras el widget ocupa la pantalla para no
  taparle ningún control a quien está reservando.
- **Formularios validados** en eventos, flamenco y contacto, más el de consulta para
  grupos y menú degustación en reservas, con mensajes de error en español, casilla de
  privacidad sin premarcar y confirmación visible.
- **WhatsApp** con mensaje predefinido (`https://wa.me/34621153815`) y, en los
  formularios, mensaje compuesto automáticamente con los datos introducidos.
- **Barra fija de reserva en móvil** (Reservar · WhatsApp · Llamar) y, en escritorio,
  botón flotante de WhatsApp que se atenúa al hacer scroll para no tapar contenido.
- **Cenefa de lacería** dibujada a partir del alicatado real de la barra del local, usada
  como remate de sección y como textura de fondo.
- Fundido corto de entrada en cada página.
- **Recursos versionados**: cada hoja de estilo, script y archivo de datos se enlaza con
  `?v=<huella del archivo>`, así que al publicar un cambio el navegador descarga la
  versión nueva en lugar de servir la que tiene guardada.
- Cabecera fija que se compacta, menú móvil a pantalla completa, animaciones de entrada
  suaves (desactivadas si el sistema pide menos movimiento), enlace «saltar al contenido»,
  metaetiquetas y Open Graph por página, datos estructurados `Restaurant` en la portada,
  favicon, textos alternativos en todas las imágenes y hoja de estilos de impresión.

## 4. La portada: una foto para cada pantalla

La portada usa `<picture>` para servir **dos fotografías distintas** según el dispositivo:

| | Fotografía | Archivos | Por qué |
|---|---|---|---|
| Móvil (≤768 px) | El patio de los geranios | `portada-patio-sm/med.jpg` | Su original es de 1000×1000 px: en vertical se ve nítida y es la más viva |
| Escritorio (≥769 px) | Sala con la yesería y el panel del poema | `portada-sala-med/.jpg` | Recorte panorámico de un original de 3024×4032 px: en 1440 px va 1:1, sin ampliar |

Comprobado que en ambos casos la imagen servida tiene, como mínimo, tantos píxeles como
los que ocupa en pantalla. Si en el futuro el restaurante facilita **el original en alta
de la foto de los geranios**, esa puede volver también al escritorio: es la más atractiva
de las dos, y solo se descartó ahí por resolución.

## 5. Imágenes utilizadas

**Del Instagram oficial (@la_tarantaoviedo)** — 24 fotografías descargadas en su máxima
resolución pública. Once de ellas proceden de las publicaciones que indicó el cliente e
incluyen platos **identificados por el propio pie de la publicación**: tabla de quesos
andaluces, mollejas de cordero, falsa aceituna con anchoa del Cantábrico, calamares a la
andaluza, arroz negro y falsa trufa de Jaén. Además, el cuadro de Euliser Polanco, la
escalera de la buganvilla y el rincón de arcos. Primer lote:
`plato-arroz-negro`, `plato-falsa-trufa-jaen`, `plato-flamenquin`, `postre-taranta`,
`plato-autor`, `plato-pescado`, `salon-arcos-flores`, `comedor-flores`, `barra-azulejos`,
`rincon-toro`, `barricas-vermut`, `rincon-yeseria`, `bodega-barril`.

Dos de ellas están identificadas con certeza por la publicación de la que proceden:
el **arroz negro de gamba roja** y la **falsa trufa de paté de perdiz** (pase de Jaén).

**De prensa local (MiOviedo, reportajes de apertura)** — 10 fotografías:
`tablao`, `escalera-barra`, `arcos-barricas`, `arco-nazari`, `artesonado`, `fachada`,
`mural-bodega`, `olivos-escultura`, `yeseria-sala`, `arcos-obra`.

**No se ha utilizado ninguna imagen de banco de imágenes.** Todo lo que se ve en la web
es del restaurante. Lo que faltaba (patio con fuente, flamenco en directo, desayunos) no
se ha inventado con fotografías genéricas: se ha resuelto con las fotos reales
disponibles y con recursos gráficos propios (arcos, cenefas y ornamentos en SVG).

Las fotografías de prensa deberán sustituirse por material propio o contar con
autorización expresa antes de publicar.

## 6. Datos pendientes de confirmar con el restaurante

1. **Precios y denominaciones de la carta** (marcados como provisionales en la web y en
   `data/menu-data.js`). Incluye la grafía de «cuarrécano» y «plácton».
2. **Horarios**: los publicados proceden de la información pública del restaurante.
3. **Menú degustación**: ya no está pendiente en lo esencial. El restaurante facilitó los
   nombres oficiales de los nueve pases, el precio (75,00 € por persona), la antelación de
   reserva (48 horas) y el maridaje (vinos del sur: finos, manzanillas, olorosos y
   amontillados). Quedan por confirmar **duración aproximada, mínimo de comensales y días
   en que se sirve**.
4. **Calendario de flamenco**: no se ha inventado ninguna fecha ni artista.
5. **Escuela de flamenco**: no está confirmada, por lo que no aparece.
6. **Eventos**: aforos, menús de grupo, precios y condiciones de reserva.
7. **Correo electrónico** de contacto para el aviso legal.
   *(La razón social ya no está pendiente: GALIANDA, S.L., CIF B-70950597, tomada del pie
   de la carta. Queda por confirmar el domicilio social a efectos legales.)*
   *(El sistema de reservas tampoco está pendiente: es el widget real de Tableo.)*
11. **El poema en azulejo**: confirmar con el restaurante que se cuenta con la
   autorización de su autora, Virginia A. M., para reproducirlo en la web.
12. **Desayunos y raciones**: confirmar precios y si el dulce del día mantiene el
   formato de 0,50 €/unidad.
8. **Alérgenos**: no se incluye tabla; la web remite a la sala.
9. **Equipo de sala y cocina**, y distribución exacta de plantas (la prensa ofrece dos
   versiones distintas, así que no se afirma ninguna).
10. **Aparcamientos y líneas de autobús** concretos.

No se han inventado testimonios, premios, reseñas ni actuaciones. Los datos históricos
(edificio de 1799, apertura en marzo de 2025, trayectoria del chef José Ignacio López y
del propietario Juan Carlos Revert, artesanos y artistas) proceden de la prensa local.

## 7. Pruebas realizadas

- Las 12 páginas cargan sin errores de consola y sin recursos rotos (comprobación
  automática de todos los enlaces, imágenes, hojas de estilo y scripts).
- Sin desbordamiento horizontal a 375, 768 y 1280 px.
- Mapa: selección por clic, por chips de provincia y por teclado; panel sincronizado.
- Carta: 31 platos en 7 categorías, filtros y buscador.
- Galería: filtrado, apertura de lightbox, navegación y contador.
- Formularios: envío vacío (6 errores marcados), teléfono inválido detectado, envío
  correcto con mensaje de éxito y enlace de WhatsApp compuesto.
- Widget de Tableo: carga correctamente en escritorio y en móvil (375 px), sin
  desbordamiento horizontal, y los botones flotantes se apartan solo mientras ocupa
  pantalla (comprobado arriba, sobre el widget y al pie de la página).
- Menú móvil: apertura, cierre con `Esc` y bloqueo del scroll de fondo.
- Logotipo comprobado sobre fondo claro y oscuro, sin deformación (proporción original).
- Animaciones de entrada: comprobado con scroll rápido (saltos de 1400 px) que **ningún
  bloque queda invisible**; hay una red de seguridad que rescata cualquiera que se quedase
  atrás.

## 8. Posibles mejoras cuando el proyecto siga adelante

- Sesión fotográfica propia: patio con fuente, tablao en actuación, desayunos y equipo.
- Conectar los formularios de eventos y contacto al correo del restaurante, y añadir
  aviso de cookies que cargue Tableo y Google Maps solo tras el consentimiento.
- Carta en PDF descargable e información de alérgenos.
- Agenda de actuaciones flamencas con fechas reales y venta anticipada.
- Versión en inglés y ficha de Google Business enlazada.
- Formatos WebP/AVIF y `srcset` para afinar aún más la carga (ahora todas las imágenes
  son JPG optimizado en dos tamaños: 1800 px y 900 px).
- Fotografía propia del patio con la fuente y de una actuación en el tablao: son los dos
  huecos que quedan sin imagen real.
- Página de prensa con los reportajes publicados y dosier descargable.
