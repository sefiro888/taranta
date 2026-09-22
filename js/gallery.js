/* =========================================================================
   LA TARANTA - Galeria: filtros + lightbox accesible
   ========================================================================= */
(function () {
  'use strict';

  var galeria = document.querySelector('[data-galeria]');
  if (!galeria) return;

  var figuras = Array.prototype.slice.call(galeria.querySelectorAll('figure'));
  var filtros = document.querySelectorAll('[data-filtro-galeria]');
  var vacio = document.querySelector('[data-galeria-vacia]');

  /* ---------------------------------------------------------- Filtrado */
  function filtrar(clave) {
    var visibles = 0;
    figuras.forEach(function (f) {
      var cats = (f.getAttribute('data-cat') || '').split(' ');
      var ok = clave === 'todo' || cats.indexOf(clave) !== -1;
      f.classList.toggle('es-oculta', !ok);
      if (ok) visibles++;
    });
    if (vacio) vacio.hidden = visibles > 0;
  }

  filtros.forEach(function (b) {
    b.addEventListener('click', function () {
      filtros.forEach(function (o) {
        o.classList.toggle('es-activo', o === b);
        o.setAttribute('aria-pressed', o === b ? 'true' : 'false');
      });
      filtrar(b.getAttribute('data-filtro-galeria'));
    });
  });

  /* ---------------------------------------------------------- Lightbox */
  var caja = document.createElement('div');
  caja.className = 'lightbox';
  caja.setAttribute('role', 'dialog');
  caja.setAttribute('aria-modal', 'true');
  caja.setAttribute('aria-label', 'Imagen ampliada');
  caja.innerHTML =
    '<button class="lightbox__cerrar" type="button" aria-label="Cerrar (Esc)">&times;</button>' +
    '<button class="lightbox__ant" type="button" aria-label="Anterior (flecha izquierda)">&#8249;</button>' +
    '<button class="lightbox__sig" type="button" aria-label="Siguiente (flecha derecha)">&#8250;</button>' +
    '<figure class="lightbox__fig"><img alt=""><figcaption></figcaption></figure>' +
    '<p class="lightbox__contador"></p>';
  document.body.appendChild(caja);

  var lbImg = caja.querySelector('img');
  var lbCap = caja.querySelector('figcaption');
  var lbCont = caja.querySelector('.lightbox__contador');
  var indice = 0;
  var ultimoFoco = null;

  function visibles() {
    return figuras.filter(function (f) { return !f.classList.contains('es-oculta'); });
  }

  function pintar() {
    var lista = visibles();
    if (!lista.length) return;
    indice = (indice + lista.length) % lista.length;
    var fig = lista[indice];
    var img = fig.querySelector('img');
    var cap = fig.querySelector('figcaption');
    lbImg.src = img.getAttribute('data-grande') || img.src;
    lbImg.alt = img.alt || '';
    lbCap.textContent = cap ? cap.textContent : img.alt;
    lbCont.textContent = (indice + 1) + ' / ' + lista.length;
  }

  function abrir(fig) {
    var lista = visibles();
    indice = lista.indexOf(fig);
    if (indice < 0) indice = 0;
    ultimoFoco = document.activeElement;
    pintar();
    caja.classList.add('es-abierto');
    document.body.style.overflow = 'hidden';
    caja.querySelector('.lightbox__cerrar').focus();
  }

  function cerrar() {
    caja.classList.remove('es-abierto');
    document.body.style.overflow = '';
    lbImg.removeAttribute('src');
    if (ultimoFoco) ultimoFoco.focus();
  }

  figuras.forEach(function (f) {
    f.setAttribute('tabindex', '0');
    f.setAttribute('role', 'button');
    var img = f.querySelector('img');
    f.setAttribute('aria-label', 'Ampliar imagen: ' + (img ? img.alt : ''));
    f.addEventListener('click', function () { abrir(f); });
    f.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); abrir(f); }
    });
  });

  caja.querySelector('.lightbox__cerrar').addEventListener('click', cerrar);
  caja.querySelector('.lightbox__ant').addEventListener('click', function () { indice--; pintar(); });
  caja.querySelector('.lightbox__sig').addEventListener('click', function () { indice++; pintar(); });
  caja.addEventListener('click', function (e) { if (e.target === caja) cerrar(); });

  document.addEventListener('keydown', function (e) {
    if (!caja.classList.contains('es-abierto')) return;
    if (e.key === 'Escape') cerrar();
    if (e.key === 'ArrowRight') { indice++; pintar(); }
    if (e.key === 'ArrowLeft') { indice--; pintar(); }
    if (e.key === 'Tab') {
      var foco = caja.querySelectorAll('button');
      var primero = foco[0], ultimo = foco[foco.length - 1];
      if (e.shiftKey && document.activeElement === primero) { e.preventDefault(); ultimo.focus(); }
      else if (!e.shiftKey && document.activeElement === ultimo) { e.preventDefault(); primero.focus(); }
    }
  });

  /* Deslizar en tactil */
  var x0 = null;
  caja.addEventListener('touchstart', function (e) { x0 = e.changedTouches[0].clientX; }, { passive: true });
  caja.addEventListener('touchend', function (e) {
    if (x0 === null) return;
    var dx = e.changedTouches[0].clientX - x0;
    if (Math.abs(dx) > 45) { indice += dx < 0 ? 1 : -1; pintar(); }
    x0 = null;
  }, { passive: true });
}());
