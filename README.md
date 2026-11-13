# La Taranta · Oviedo

**Andalucía en el corazón de Asturias**

Web del restaurante **La Taranta**, alta cocina andaluza con tablao flamenco en
el centro de Oviedo. Calle Rosal, 22-24.

🔗 **https://www.latarantaoviedo.com**

---

## Cómo verlo en local

Abre `index.html` con doble clic: funciona sin servidor. O, para que todo se
comporte igual que en producción:

```bash
python .claude/servidor-demo.py
```

Y visita `http://localhost:8123`.

---

## Cómo está hecho

HTML, CSS y JavaScript plano. **Sin framework, sin dependencias y sin paso de
compilación.** Se publica tal cual.

Lo único que hace falta para trabajar en él es Python 3 (y Pillow, si se tocan
imágenes), que se usa para tres generadores que evitan mantener a mano la
cabecera y el pie de veintidós páginas.

| | |
|---|---|
| Páginas | 22 |
| Alojamiento | GitHub Pages, rama `main` |
| Reservas | Widget de Tableo |
| Analítica | Ninguna. No se rastrea a nadie |

### Estructura

```
├── index.html              Portada
├── carta.html              Las tres cartas, con filtros y buscador
├── menu-degustacion.html   Los nueve pases y el mapa interactivo
├── provincias.html         Índice de las ocho provincias
├── provincia-*.html        Una ficha por provincia
├── restaurante.html        Los cuatro espacios
├── experiencia.html        Cómo es una visita
├── flamenco.html           El tablao
├── chef.html               José Ignacio López Gómez
├── historia.html           El origen de la casa
├── galeria.html            Fotografías y vídeo
├── eventos.html            Grupos y eventos
├── reservas.html           Reserva en línea
├── contacto.html           Datos, horarios y cómo llegar
├── politica-privacidad.html
│
├── css/        Sistema visual y adaptación a pantallas
├── js/         Un fichero por pieza, sin dependencias
├── data/       menu-data.js, fuente única de la carta
├── assets/     Imágenes, logotipos y las cartas en PDF
└── scripts/    Generadores de navegación, provincias y sitemap
```

### Los generadores

La navegación está definida **una sola vez**, en `scripts/navegacion.py`. Al
ejecutarlo, reescribe la cabecera y el menú móvil de todas las páginas.

```bash
python scripts/construir.py
```

Ese único comando regenera las páginas de provincias, la cabecera de las
veintidós, el sitemap y las firmas de caché de los CSS y JS, **y después revisa
el resultado**: enlaces rotos, imágenes que faltan, fotos sin su versión
pequeña. Es idempotente y devuelve error si encuentra algo mal.

Requisitos: Python 3. Y Pillow (`pip install pillow`) solo si se tocan
imágenes.

---

## Privacidad

La web **no instala cookies propias, ni analítica, ni publicidad.**

Incrusta tres servicios de terceros —Tableo, Google Maps y YouTube— y **ninguno
se carga por su cuenta**: los iframes no llevan `src` hasta que el visitante
acepta, y el vídeo no descarga nada hasta que se pulsa el play. Si se rechaza,
la página sigue siendo útil y ofrece la alternativa.

Las tipografías todavía se sirven desde Google Fonts. No instalan cookies, pero
Google recibe la dirección IP del visitante; está previsto alojarlas en el
propio servidor.

---

## Accesibilidad

- Navegación completa con teclado, incluidos los desplegables del menú
- `aria-current` en la página activa y `aria-expanded` en lo que se abre
- Texto alternativo en todas las imágenes de contenido
- Se respeta `prefers-reduced-motion`
- Contrastes comprobados sobre los fondos oscuros de la casa

---

## Para continuar el trabajo

Lee **[CLAUDE.md](CLAUDE.md)**. Recoge las convenciones, cómo funcionan los
generadores, qué no se puede romper, los errores que ya se cometieron y lo que
queda pendiente.

---

## Créditos

Diseño y desarrollo: **Bernardo Fernández**.

Fotografías, cartas y textos de marca: La Taranta · GALIANDA, S.L.
El mapa de Andalucía deriva del archivo «Provincias de Andalucía» de Wikimedia
Commons, CC BY-SA 3.0, simplificado y redibujado.
Tipografías Cormorant Garamond y Jost, SIL Open Font License.
