/* =========================================================================
   LA TARANTA - El poema del azulejo
   Texto en data/menu-data.js (window.POEMA), transcrito del panel ceramico.
   Las estrofas se revelan al entrar en pantalla, como quien lee despacio.
   ========================================================================= */
(function () {
  'use strict';

  var destino = document.querySelector('[data-poema]');
  if (!destino || !window.POEMA) return;

  var P = window.POEMA;
  var completo = destino.getAttribute('data-poema') !== 'breve';

  var estrofas = completo ? P.estrofas : [P.estrofas[0]];
  var html = '';

  estrofas.forEach(function (versos) {
    /* La clase 'reveal' hace que la red de seguridad de main.js tambien las cubra */
    html += '<p class="poema__estrofa reveal">' + versos.join('<br>') + '</p>';
  });

  if (completo) {
    html += '<p class="poema__firma reveal"><b>' + P.autora + '</b>' + P.oficio + ' · ' + P.lugar + '</p>';
  }

  destino.innerHTML = html;

  var partes = destino.querySelectorAll('.poema__estrofa, .poema__firma');
  if ('IntersectionObserver' in window) {
    var obs = new IntersectionObserver(function (entradas) {
      entradas.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('es-visible'); obs.unobserve(e.target); }
      });
    }, { threshold: 0.15, rootMargin: '0px 0px -40px 0px' });
    partes.forEach(function (el) { obs.observe(el); });
  } else {
    partes.forEach(function (el) { el.classList.add('es-visible'); });
  }
}());
