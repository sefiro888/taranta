/* =========================================================================
   LA TARANTA - Grupos del menu

   El desplegable ya abre solo con CSS, al pasar por encima y al llegar
   con el teclado. Esto anade lo que el CSS no puede:

   · En tactil, el primer toque abre el grupo en vez de no hacer nada.
   · Escape lo cierra.
   · Un clic fuera lo cierra.
   · Solo un grupo abierto a la vez.
   ========================================================================= */
(function () {
  'use strict';

  var grupos = Array.prototype.slice.call(document.querySelectorAll('.nav__grupo'));
  if (!grupos.length) return;

  function cerrarTodos(menos) {
    grupos.forEach(function (g) {
      if (g === menos) return;
      var b = g.querySelector('.nav__boton');
      if (b) b.setAttribute('aria-expanded', 'false');
    });
  }

  grupos.forEach(function (grupo) {
    var boton = grupo.querySelector('.nav__boton');
    if (!boton) return;

    boton.addEventListener('click', function (e) {
      e.preventDefault();
      var abierto = boton.getAttribute('aria-expanded') === 'true';
      cerrarTodos(grupo);
      boton.setAttribute('aria-expanded', abierto ? 'false' : 'true');
    });

    /* Al salir con el tabulador del ultimo enlace, se cierra */
    grupo.addEventListener('focusout', function (e) {
      if (!grupo.contains(e.relatedTarget)) {
        boton.setAttribute('aria-expanded', 'false');
      }
    });
  });

  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    var abierto = document.querySelector('.nav__boton[aria-expanded="true"]');
    if (!abierto) return;
    abierto.setAttribute('aria-expanded', 'false');
    abierto.focus();
  });

  document.addEventListener('click', function (e) {
    if (e.target.closest && e.target.closest('.nav__grupo')) return;
    cerrarTodos(null);
  });
}());
