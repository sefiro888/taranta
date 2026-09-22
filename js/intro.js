/* =========================================================================
   LA TARANTA - Umbral de entrada
   -------------------------------------------------------------------------
   Cortina que se muestra UNA sola vez por sesion, solo en la portada:
   el arco se dibuja, aparece el logotipo y la frase, y despues se abre.

   Reglas de cortesia:
   - Se salta con un toque, con Esc o con el boton "Entrar".
   - No se muestra si el visitante pide reducir el movimiento.
   - No se muestra si ya se vio en esta sesion ni al volver atras.
   - Si el JS falla, no aparece: el atributo hidden solo se quita desde aqui.
   ========================================================================= */
(function () {
  'use strict';

  var umbral = document.getElementById('umbral');
  if (!umbral) return;

  var yaVista = false;
  try { yaVista = sessionStorage.getItem('lt-umbral') === '1'; } catch (e) {}

  var sinMovimiento = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  if (yaVista || sinMovimiento) {
    umbral.remove();
    return;
  }

  /* Cada trazo se anima segun su longitud real, para que el dibujo
     salga parejo aunque los paths tengan tamanos distintos. */
  umbral.querySelectorAll('.umbral__arco .trazos path, .umbral__arco .trazos line').forEach(function (t) {
    var largo = 0;
    try { largo = Math.ceil(t.getTotalLength()); } catch (e) { largo = 900; }
    if (largo > 0) {
      t.style.strokeDasharray = largo;
      t.style.strokeDashoffset = largo;
    }
  });

  /* A partir de aqui si se muestra */
  var foco = document.activeElement;
  umbral.hidden = false;
  document.body.classList.add('con-umbral');
  try { sessionStorage.setItem('lt-umbral', '1'); } catch (e) {}

  var cerrado = false;
  var temporizador;

  function cerrar() {
    if (cerrado) return;
    cerrado = true;
    clearTimeout(temporizador);
    umbral.classList.add('es-abierto');
    document.body.classList.remove('con-umbral');
    document.removeEventListener('keydown', alPulsar);
    setTimeout(function () {
      umbral.remove();
      if (foco && foco.focus) foco.focus({ preventScroll: true });
    }, 1100);
  }

  function alPulsar(e) {
    if (e.key === 'Escape' || e.key === 'Enter' || e.key === ' ') cerrar();
  }

  umbral.addEventListener('click', cerrar);
  document.addEventListener('keydown', alPulsar);

  /* Se abre solo cuando termina la secuencia */
  temporizador = setTimeout(cerrar, 4200);

  /* Salvaguarda: si algo fallase en la secuencia, la cortina no se queda
     puesta mas de seis segundos en ningun caso. */
  setTimeout(cerrar, 6000);
}());
