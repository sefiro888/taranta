/* =========================================================================
   LA TARANTA - La arqueria: los cuatro espacios de la casa
   -------------------------------------------------------------------------
   Cuatro vanos de arco nazari, uno por espacio. Al pasar el cursor o tocar,
   el vano se ilumina, los demas se atenuan y el panel cuenta la zona.
   No representa la distribucion real del local: es una composicion visual.
   ========================================================================= */
(function () {
  'use strict';

  var raiz = document.querySelector('[data-arqueria]');
  if (!raiz) return;

  var ESPACIOS = [
    { id: 'el-patio', nombre: 'El Patio', orden: 'I',
      titular: 'Donde empieza el día',
      texto: 'Azulejo sevillano, plantas y tragaluz. Molletes de Antequera con AOVE temprano, tapas y vermut en la barra.',
      img: 'assets/images/barra-azulejos.jpg',
      alt: 'Barra de La Taranta con frente de azulejos andaluces',
      enlace: 'restaurante.html#el-patio', cta: 'Ver El Patio' },
    { id: 'el-cortijo', nombre: 'El Cortijo', orden: 'II',
      titular: 'El comedor de mantel largo',
      texto: 'Lámparas granadinas, tejas centenarias y un panorama de olivar. Aquí se sirven la carta de autor y el menú degustación.',
      img: 'assets/images/comedor-flores.jpg',
      alt: 'Comedor principal El Cortijo, con arcos y flores',
      enlace: 'restaurante.html#el-cortijo', cta: 'Ver El Cortijo' },
    { id: 'la-bodega', nombre: 'La Bodega', orden: 'III',
      titular: 'La sala que se cierra',
      texto: 'Arcos, columnas y barricas. Comidas de empresa, celebraciones y presentaciones con acceso de servicio propio.',
      img: 'assets/images/arcos-barricas.jpg',
      alt: 'La Bodega: arcos, columnas y barricas',
      enlace: 'eventos.html', cta: 'Organizar un evento' },
    { id: 'el-tablao', nombre: 'El Tablao', orden: 'IV',
      titular: 'Donde suena el compás',
      texto: 'Escenario de madera, sillas de enea y el mirador de arcos al fondo. El flamenco estuvo en los planos desde el principio.',
      img: 'assets/images/tablao.jpg',
      alt: 'El Tablao: escenario de madera y arcos andaluces',
      enlace: 'flamenco.html', cta: 'El flamenco en casa' }
  ];

  var activo = 0;

  /* ------------------------------------------------------------ Montaje */
  var vanos = document.createElement('div');
  vanos.className = 'arqueria__vanos';
  vanos.setAttribute('role', 'tablist');
  vanos.setAttribute('aria-label', 'Los cuatro espacios de La Taranta');

  ESPACIOS.forEach(function (e, i) {
    var b = document.createElement('button');
    b.type = 'button';
    b.className = 'vano';
    b.setAttribute('role', 'tab');
    b.setAttribute('id', 'vano-' + e.id);
    b.setAttribute('aria-controls', 'panel-arqueria');
    b.setAttribute('aria-selected', i === 0 ? 'true' : 'false');
    b.innerHTML =
      '<span class="vano__arco"><img src="' + e.img.replace('.jpg', '-sm.jpg') + '" alt="' + e.alt + '" loading="lazy"></span>' +
      '<span class="vano__pie"><i>' + e.orden + '</i><b>' + e.nombre + '</b></span>';
    b.addEventListener('mouseenter', function () {
      if (window.matchMedia('(hover: hover)').matches) elegir(i);
    });
    b.addEventListener('focus', function () { elegir(i); });
    b.addEventListener('click', function () { elegir(i, true); });
    vanos.appendChild(b);
  });

  var panel = document.createElement('div');
  panel.className = 'arqueria__panel';
  panel.id = 'panel-arqueria';
  panel.setAttribute('role', 'tabpanel');
  panel.setAttribute('aria-live', 'polite');

  raiz.appendChild(vanos);
  raiz.appendChild(panel);

  /* ------------------------------------------------------------ Estado */
  function elegir(i, desplazar) {
    activo = i;
    var botones = vanos.querySelectorAll('.vano');
    botones.forEach(function (b, k) {
      b.classList.toggle('es-activo', k === i);
      b.setAttribute('aria-selected', k === i ? 'true' : 'false');
    });
    vanos.classList.add('tiene-activo');

    var e = ESPACIOS[i];
    panel.innerHTML =
      '<p class="arqueria__orden">Espacio ' + e.orden + ' de IV</p>' +
      '<h3>' + e.nombre + '</h3>' +
      '<p class="arqueria__titular">' + e.titular + '</p>' +
      '<p class="arqueria__texto">' + e.texto + '</p>' +
      '<a class="enlace-fino" href="' + e.enlace + '">' + e.cta + '</a>';

    if (desplazar && window.matchMedia('(max-width: 768px)').matches) {
      var y = panel.getBoundingClientRect().top + window.pageYOffset - 120;
      window.scrollTo({ top: y, behavior: 'smooth' });
    }
  }

  vanos.addEventListener('keydown', function (e) {
    if (e.key !== 'ArrowRight' && e.key !== 'ArrowLeft') return;
    e.preventDefault();
    var siguiente = (activo + (e.key === 'ArrowRight' ? 1 : -1) + ESPACIOS.length) % ESPACIOS.length;
    vanos.querySelectorAll('.vano')[siguiente].focus();
  });

  elegir(0);
}());
