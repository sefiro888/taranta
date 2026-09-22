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

  /* ------------------------------------------------------------- Render */
  function pintar() {
    var html = '';
    D.categorias.forEach(function (cat) {
      var platos = D.platos.filter(function (p) { return p.cat === cat.id; });
      if (!platos.length) return;

      html += '<section class="carta-grupo reveal" data-grupo="' + cat.id + '" data-carta-grupo="' +
        (cat.carta || 'autor') + '" id="cat-' + cat.id + '">' +
        '<header class="carta-grupo__cab">' +
        '<p class="kicker">' + cat.kicker + '</p>' +
        '<h2>' + cat.nombre + '</h2>' +
        '<p>' + cat.texto + '</p>' +
        '</header><div class="platos">';

      platos.forEach(function (p) {
        var busca = (p.nombre + ' ' + (p.desc || '')).toLowerCase();
        var clases = 'plato' + (p.img ? ' plato--con-foto' : '');
        html += '<article class="' + clases + '" data-plato="' + p.id + '" data-busca="' +
          esc(busca) + '" data-cat="' + p.cat + '">';

        if (p.img) {
          html += '<button class="plato__foto" type="button" data-ver="' + p.id +
            '" aria-label="Ver la fotografía de ' + esc(p.nombre) + '">' +
            '<img src="' + p.img.replace('.jpg', '-sm.jpg') + '" alt="' + esc(p.alt || p.nombre) + '" loading="lazy"></button>';
        }

        html += '<h3 class="plato__nombre">' + p.nombre + '</h3>' + precioHTML(p);
        if (p.desc) html += '<p class="plato__desc">' + p.desc + '</p>';

        var etiquetas = [];
        if (p.unidades) etiquetas.push('<span class="etiqueta">' + p.unidades + '</span>');
        if (p.minimo) etiquetas.push('<span class="etiqueta etiqueta--aviso">Mínimo ' + p.minimo + ' personas</span>');
        if (p.espera) etiquetas.push('<span class="etiqueta etiqueta--aviso">Elaboración: ' + p.espera + '</span>');
        if (p.destacado) etiquetas.push('<span class="etiqueta etiqueta--destacado">Recomendado</span>');
        if (p.img) etiquetas.push('<button class="etiqueta etiqueta--ver" type="button" data-ver="' + p.id + '">Ver el plato</button>');
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
