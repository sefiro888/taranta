/* =========================================================================
   LA TARANTA - Cartas digitales: tres cartas, filtros, buscador y ficha
   Los datos viven en data/menu-data.js
   ========================================================================= */
(function () {
  'use strict';

  var raiz = document.querySelector('[data-carta]');
  if (!raiz || !window.MENU_DATA) return;

  var D = window.MENU_DATA;
  var CARTAS = window.CARTAS || [{ id: 'autor', nombre: 'Carta' }];
  var selectorCartas = document.querySelector('[data-cartas]');
  var contenedorFiltros = document.querySelector('[data-carta-filtros]');
  var buscador = document.querySelector('[data-carta-buscador]');
  var vacia = document.querySelector('[data-carta-vacia]');

  var cartaActiva = CARTAS[0].id;
  var filtroActivo = 'todo';
  var textoBusqueda = '';

  function euros(n) { return n.toFixed(2).replace('.', ',') + ' €'; }
  function esc(t) { return String(t).replace(/"/g, '&quot;'); }

  /* --------------------------------------------------------- Precio HTML */
  function precioHTML(p) {
    if (p.precioMedia) {
      return '<p class="plato__precio">' + euros(p.precio) +
        '<small>entera · media ' + euros(p.precioMedia) + '</small></p>';
    }
    return '<p class="plato__precio">' + euros(p.precio) +
      (p.unidad ? '<small>por ' + p.unidad + '</small>' : '') + '</p>';
  }

  /* Iconos de linea, uno por seccion (se dibujan en dorado sobre la banda oscura) */
  var ICONOS = {
    molletes: '<path d="M6 29c0-8 8-14 18-14s18 6 18 14c0 4-3 6-6 6H12c-3 0-6-2-6-6Z"/><path d="M16 21l3 7M24 19l2 9M32 21l-1 7"/>',
    tortillas: '<circle cx="24" cy="24" r="17"/><path d="M12 21c3-4 8-6 12-6s9 2 12 6"/><path d="M14 31c3 2 6 3 10 3s7-1 10-3"/><circle cx="24" cy="24" r="1.2"/>',
    raciones: '<circle cx="24" cy="24" r="17"/><circle cx="24" cy="24" r="11.5"/><circle cx="19" cy="24" r="3.6"/><circle cx="29.5" cy="24" r="3.6"/>',
    alacena: '<path d="M20 5h8v8l4 6v22a2 2 0 0 1-2 2H18a2 2 0 0 1-2-2V19l4-6V5Z"/><path d="M16 27h16M16 35h16"/><path d="M22 9h4"/>',
    frios: '<path d="M24 5v38M7.5 14.5l33 19M7.5 33.5l33-19"/><path d="M20 8l4 4 4-4M20 40l4-4 4 4"/>',
    calientes: '<path d="M24 4c2 8 11 11 11 22a11 11 0 0 1-22 0c0-5 3-8 5-10 0 4 2 6 4 6 0-6-1-11 2-18Z"/><path d="M24 40a5 5 0 0 1-5-5c0-3 3-5 5-8 2 3 5 5 5 8a5 5 0 0 1-5 5Z"/>',
    arroces: '<ellipse cx="24" cy="27" rx="17" ry="8"/><path d="M7 27H2M41 27h5"/><circle cx="16" cy="26" r="1"/><circle cx="23" cy="29" r="1"/><circle cx="30" cy="26" r="1"/><circle cx="26" cy="23.5" r="1"/><path d="M18 14c0-3 3-3 3-6M26 14c0-3 3-3 3-6"/>',
    lonja: '<path d="M4 24c6-9 16-12 24-9 3 1 6 4 8 9-2 5-5 8-8 9-8 3-18 0-24-9Z"/><path d="M36 24l8-8v16l-8-8Z"/><circle cx="14" cy="22" r="1.3"/><path d="M20 17c2 4 2 10 0 14"/>',
    carnes: '<path d="M7 21c0-8 8-12 17-12 8 0 14 4 16 9 2 7-2 15-11 18-10 3-22-1-22-15Z"/><path d="M15 21h18M24 21v13"/><path d="M12 17c2-2 4-3 7-4"/>',
    postres: '<path d="M16 23l8 20 8-20"/><path d="M13 23a11 11 0 1 1 22 0Z"/><path d="M19 29l4 6M25 27l3 7"/>'
  };
  function iconoHTML(id) {
    return ICONOS[id] ? '<svg class="carta-grupo__icono" viewBox="0 0 48 48" aria-hidden="true" focusable="false">' + ICONOS[id] + '</svg>' : '';
  }

  /* ------------------------------------------------------------- Render */
  function pintar() {
    var html = '';
    var ROMANOS = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X'];
    var orden = {};
    D.categorias.forEach(function (cat) {
      var platos = D.platos.filter(function (p) { return p.cat === cat.id; });
      if (!platos.length) return;
      var carta = cat.carta || 'autor';
      orden[carta] = (orden[carta] || 0) + 1;

      html += '<section class="carta-grupo reveal" data-grupo="' + cat.id + '" data-carta-grupo="' +
        carta + '" id="cat-' + cat.id + '">' +
        '<header class="carta-grupo__cab">' +
        '<div class="carta-grupo__tit">' +
        iconoHTML(cat.id) +
        '<p class="kicker">' + cat.kicker + '</p>' +
        '<h2>' + cat.nombre + '</h2>' +
        '<span class="carta-grupo__adorno" aria-hidden="true"></span>' +
        '<p class="carta-grupo__texto">' + cat.texto + '</p>' +
        '</div>' +
        '<span class="carta-grupo__num" aria-hidden="true">' + ROMANOS[orden[carta] - 1] + '</span>' +
        '</header><div class="platos">';

      platos.forEach(function (p) {
        var busca = (p.nombre + ' ' + (p.desc || '')).toLowerCase();
        var clases = 'plato' + (p.destacado ? ' plato--destacado' : '');
        html += '<article class="' + clases + '" data-plato="' + p.id + '" data-busca="' +
          esc(busca) + '" data-cat="' + p.cat + '">';

        html += '<div class="plato__cab"><h3 class="plato__nombre">' + p.nombre + '</h3>' +
          '<span class="plato__guia" aria-hidden="true"></span>' + precioHTML(p) + '</div>';
        if (p.desc) html += '<p class="plato__desc">' + p.desc + '</p>';

        var etiquetas = [];
        if (p.unidades) etiquetas.push('<span class="etiqueta">' + p.unidades + '</span>');
        if (p.minimo) etiquetas.push('<span class="etiqueta etiqueta--aviso">M&iacute;nimo ' + p.minimo + ' personas</span>');
        if (p.espera) etiquetas.push('<span class="etiqueta etiqueta--aviso">Elaboraci&oacute;n: ' + p.espera + '</span>');
        if (p.destacado) etiquetas.push('<span class="etiqueta etiqueta--destacado">Recomendado de la casa</span>');
        if (p.nota) etiquetas.push('<span class="etiqueta">' + p.nota + '</span>');
        if (etiquetas.length) html += '<div class="plato__etiquetas">' + etiquetas.join('') + '</div>';

        html += '</article>';
      });

      html += '</div></section>';
    });
    raiz.innerHTML = html;
    observarReveal();
  }

  /* ------------------------------------------------- Selector de cartas */
  if (selectorCartas) {
    var h = '';
    CARTAS.forEach(function (c, i) {
      h += '<button class="carta-pestana' + (i === 0 ? ' es-activa' : '') + '" data-carta-id="' + c.id +
        '" aria-pressed="' + (i === 0 ? 'true' : 'false') + '">' +
        '<span>' + c.nombre + '</span><small>' + c.titular + '</small></button>';
    });
    selectorCartas.innerHTML = h;

    selectorCartas.addEventListener('click', function (e) {
      var b = e.target.closest('.carta-pestana');
      if (!b) return;
      cartaActiva = b.getAttribute('data-carta-id');
      selectorCartas.querySelectorAll('.carta-pestana').forEach(function (o) {
        var on = o === b;
        o.classList.toggle('es-activa', on);
        o.setAttribute('aria-pressed', on ? 'true' : 'false');
      });
      filtroActivo = 'todo';
      pintarFiltros();
      aplicar();
      var intro = document.querySelector('[data-carta-intro]');
      if (intro) {
        var c = CARTAS.filter(function (x) { return x.id === cartaActiva; })[0];
        if (c) intro.textContent = c.texto;
      }
    });
  }

  /* ------------------------------------------------------------ Filtros */
  function pintarFiltros() {
    if (!contenedorFiltros) return;
    var cats = D.categorias.filter(function (c) { return (c.carta || 'autor') === cartaActiva; });
    var b = '<button class="filtro es-activo" data-filtro="todo" aria-pressed="true">Todo</button>';
    cats.forEach(function (c) {
      b += '<button class="filtro" data-filtro="' + c.id + '" aria-pressed="false">' +
        c.nombre.replace('Siempre queda hueco para…', 'Postres') + '</button>';
    });
    contenedorFiltros.innerHTML = b;
    contenedorFiltros.hidden = cats.length < 2;
  }

  function aplicar() {
    var visibles = 0;
    D.categorias.forEach(function (cat) {
      var grupo = raiz.querySelector('[data-grupo="' + cat.id + '"]');
      if (!grupo) return;
      var deEstaCarta = (cat.carta || 'autor') === cartaActiva;
      var enGrupo = 0;
      grupo.querySelectorAll('.plato').forEach(function (art) {
        var okCat = filtroActivo === 'todo' || art.getAttribute('data-cat') === filtroActivo;
        var okTxt = !textoBusqueda || art.getAttribute('data-busca').indexOf(textoBusqueda) !== -1;
        var ok = deEstaCarta && okCat && okTxt;
        art.classList.toggle('plato--oculto', !ok);
        if (ok) enGrupo++;
      });
      grupo.hidden = enGrupo === 0;
      visibles += enGrupo;
    });
    if (vacia) vacia.hidden = visibles > 0;
  }

  if (contenedorFiltros) {
    contenedorFiltros.addEventListener('click', function (e) {
      var b = e.target.closest('.filtro');
      if (!b) return;
      contenedorFiltros.querySelectorAll('.filtro').forEach(function (o) {
        o.classList.toggle('es-activo', o === b);
        o.setAttribute('aria-pressed', o === b ? 'true' : 'false');
      });
      filtroActivo = b.getAttribute('data-filtro');
      aplicar();
    });
  }

  if (buscador) {
    buscador.addEventListener('input', function () {
      textoBusqueda = buscador.value.trim().toLowerCase();
      /* La busqueda mira en todas las cartas */
      if (textoBusqueda) {
        var enc = D.platos.filter(function (p) {
          return (p.nombre + ' ' + (p.desc || '')).toLowerCase().indexOf(textoBusqueda) !== -1;
        });
        if (enc.length) {
          var cat = D.categorias.filter(function (c) { return c.id === enc[0].cat; })[0];
          var destino = cat ? (cat.carta || 'autor') : cartaActiva;
          if (destino !== cartaActiva && selectorCartas) {
            var pest = selectorCartas.querySelector('[data-carta-id="' + destino + '"]');
            if (pest) pest.click();
          }
        }
      }
      aplicar();
    });
  }

  /* -------------------------------------------------- Ficha del plato */
  var ficha = document.createElement('div');
  ficha.className = 'ficha-plato';
  ficha.setAttribute('role', 'dialog');
  ficha.setAttribute('aria-modal', 'true');
  ficha.setAttribute('aria-label', 'Detalle del plato');
  ficha.innerHTML =
    '<div class="ficha-plato__caja">' +
      '<button class="ficha-plato__cerrar" type="button" aria-label="Cerrar">&times;</button>' +
      '<div class="ficha-plato__foto"><img alt=""></div>' +
      '<div class="ficha-plato__texto">' +
        '<p class="kicker" data-ficha-cat></p>' +
        '<h3 data-ficha-nombre></h3>' +
        '<p class="lead" data-ficha-desc></p>' +
        '<p class="apunte" data-ficha-apunte hidden></p>' +
        '<p class="ficha-plato__precio" data-ficha-precio></p>' +
        '<div class="ficha-plato__etiquetas" data-ficha-etiquetas></div>' +
        '<div class="acciones" style="margin-top:1.6rem">' +
          '<a class="boton" href="reservas.html">Reservar mesa</a>' +
          '<a class="boton boton--wa" data-ficha-wa href="#" target="_blank" rel="noopener">Preguntar por WhatsApp</a>' +
        '</div>' +
        '<p class="pie-foto" data-ficha-credito></p>' +
      '</div>' +
    '</div>';
  document.body.appendChild(ficha);

  var focoPrevio = null;

  function abrirFicha(id) {
    var p = D.platos.filter(function (x) { return x.id === id; })[0];
    if (!p) return;
    var cat = D.categorias.filter(function (c) { return c.id === p.cat; })[0];

    ficha.querySelector('img').src = p.img;
    ficha.querySelector('img').alt = p.alt || p.nombre;
    ficha.querySelector('[data-ficha-cat]').textContent = cat ? cat.nombre : '';
    ficha.querySelector('[data-ficha-nombre]').textContent = p.nombre;
    ficha.querySelector('[data-ficha-desc]').textContent = p.desc || '';
    var ap = ficha.querySelector('[data-ficha-apunte]');
    ap.textContent = p.apunte || '';
    ap.hidden = !p.apunte;
    ficha.querySelector('[data-ficha-precio]').innerHTML =
      p.precioMedia ? euros(p.precio) + ' <small>ración entera</small> · ' + euros(p.precioMedia) + ' <small>media</small>'
                    : euros(p.precio) + (p.unidad ? ' <small>por ' + p.unidad + '</small>' : '');

    var et = [];
    if (p.unidades) et.push('<span class="etiqueta">' + p.unidades + '</span>');
    if (p.minimo) et.push('<span class="etiqueta etiqueta--aviso">Mínimo ' + p.minimo + ' personas</span>');
    if (p.espera) et.push('<span class="etiqueta etiqueta--aviso">Elaboración: ' + p.espera + '</span>');
    if (p.destacado) et.push('<span class="etiqueta etiqueta--destacado">Recomendado</span>');
    ficha.querySelector('[data-ficha-etiquetas]').innerHTML = et.join('');

    ficha.querySelector('[data-ficha-credito]').textContent =
      'Fotografía publicada por La Taranta en su Instagram';

    var msg = 'Hola, me gustaría preguntar por el plato «' + p.nombre + '» de La Taranta.';
    ficha.querySelector('[data-ficha-wa]').href =
      'https://wa.me/34621153815?text=' + encodeURIComponent(msg);

    focoPrevio = document.activeElement;
    ficha.classList.add('es-abierta');
    document.body.style.overflow = 'hidden';
    ficha.querySelector('.ficha-plato__cerrar').focus();
  }

  function cerrarFicha() {
    ficha.classList.remove('es-abierta');
    document.body.style.overflow = '';
    if (focoPrevio) focoPrevio.focus();
  }

  raiz.addEventListener('click', function (e) {
    var b = e.target.closest('[data-ver]');
    if (b) abrirFicha(b.getAttribute('data-ver'));
  });
  ficha.querySelector('.ficha-plato__cerrar').addEventListener('click', cerrarFicha);
  ficha.addEventListener('click', function (e) { if (e.target === ficha) cerrarFicha(); });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && ficha.classList.contains('es-abierta')) cerrarFicha();
  });

  /* ----------------------------------------------- Aparicion progresiva */
  function observarReveal() {
    if ('IntersectionObserver' in window) {
      var obs = new IntersectionObserver(function (ent) {
        ent.forEach(function (e) {
          if (e.isIntersecting) { e.target.classList.add('es-visible'); obs.unobserve(e.target); }
        });
      }, { threshold: 0.02, rootMargin: '0px 0px 180px 0px' });
      raiz.querySelectorAll('.reveal').forEach(function (el) { obs.observe(el); });
    } else {
      raiz.querySelectorAll('.reveal').forEach(function (el) { el.classList.add('es-visible'); });
    }
  }

  /* ------------------------------------------------------------ Arranque */
  pintar();
  pintarFiltros();
  aplicar();
}());
