/* =========================================================================
   LA TARANTA - Video con fachada (sin cookies hasta que se pulsa)

   El iframe de YouTube NO se inserta al cargar la pagina. Solo cuando la
   persona pulsa el boton. Asi no se descarga nada de Google ni se deja
   ninguna cookie sin que medie una accion voluntaria, que es lo que pide
   el articulo 22.2 de la LSSI.

   Se usa youtube-nocookie.com, que es el dominio sin cookies publicitarias.
   ========================================================================= */
(function () {
  'use strict';

  var cajas = document.querySelectorAll('[data-video]');
  if (!cajas.length) return;

  Array.prototype.forEach.call(cajas, function (caja) {
    var id = caja.getAttribute('data-video');
    if (!id || !/^[A-Za-z0-9_-]{6,20}$/.test(id)) return;

    var boton = caja.querySelector('[data-video-play]');
    if (!boton) return;

    boton.addEventListener('click', function () {
      var marco = document.createElement('iframe');
      marco.src = 'https://www.youtube-nocookie.com/embed/' + id +
                  '?autoplay=1&rel=0&modestbranding=1&hl=es';
      marco.title = caja.getAttribute('data-video-titulo') || 'Vídeo';
      marco.setAttribute('allow',
        'accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture');
      marco.setAttribute('allowfullscreen', '');
      marco.setAttribute('referrerpolicy', 'strict-origin-when-cross-origin');
      marco.loading = 'eager';

      caja.innerHTML = '';
      caja.appendChild(marco);
      caja.classList.add('es-reproduciendo');
      marco.focus();
    });
  });
}());
