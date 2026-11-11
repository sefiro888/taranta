/* =========================================================================
   LA TARANTA - Consentimiento de cookies

   Bloquea de verdad: los iframes de terceros no llevan src al cargar la
   pagina, sino data-cookie-src. Nada se descarga de Google ni de Tableo
   hasta que la persona acepta. Eso es lo que pide el articulo 22.2 de la
   LSSI: consentimiento previo, no un cartel encima de algo ya cargado.

   Si rechaza, en el hueco del iframe queda un aviso con la alternativa
   (telefono, WhatsApp, enlace al mapa), para que la pagina siga sirviendo.

   La decision se guarda en localStorage durante 180 dias. No se envia a
   ningun sitio ni identifica a nadie.
   ========================================================================= */
(function () {
  'use strict';

  var CLAVE = 'lt-cookies';
  var DIAS = 180;

  /* ------------------------------------------------- Lectura y escritura */
  function leer() {
    try {
      var bruto = window.localStorage.getItem(CLAVE);
      if (!bruto) return null;
      var d = JSON.parse(bruto);
      if (!d || typeof d.acepta !== 'boolean' || !d.fecha) return null;
      if (Date.now() - d.fecha > DIAS * 864e5) return null;
      return d;
    } catch (e) {
      return null;
    }
  }

  function guardar(acepta) {
    try {
      window.localStorage.setItem(CLAVE, JSON.stringify({
        acepta: acepta, fecha: Date.now(), v: 1
      }));
    } catch (e) { /* navegacion privada: vale, se volvera a preguntar */ }
  }

  /* ------------------------------------------------------ Los incrustados */
  function marcos() {
    return document.querySelectorAll('[data-cookie-src]');
  }

  function cargar() {
    Array.prototype.forEach.call(marcos(), function (hueco) {
      if (hueco.dataset.cookieCargado === 'si') return;
      var marco = document.createElement('iframe');
      marco.src = hueco.getAttribute('data-cookie-src');
      marco.title = hueco.getAttribute('data-cookie-titulo') || '';
      marco.loading = 'lazy';
      marco.setAttribute('referrerpolicy', 'no-referrer-when-downgrade');
      var clase = hueco.getAttribute('data-cookie-clase');
      if (clase) marco.className = clase;
      hueco.innerHTML = '';
      hueco.appendChild(marco);
      hueco.dataset.cookieCargado = 'si';
      hueco.classList.add('es-cargado');
    });
    document.dispatchEvent(new CustomEvent('lt:terceros-cargados'));
  }

  function rechazar() {
    /* Fuera cualquier "cargando...", este dentro del hueco o sea una capa
       superpuesta como la del widget de reservas: si no, se queda girando
       para siempre sobre algo que nunca va a llegar. */
    Array.prototype.forEach.call(
      document.querySelectorAll('[data-cookie-espera]'),
      function (espera) { espera.hidden = true; espera.remove(); });

    Array.prototype.forEach.call(marcos(), function (hueco) {
      if (hueco.dataset.cookieCargado === 'si') return;
      var aviso = hueco.querySelector('[data-cookie-aviso]');
      if (aviso) aviso.hidden = false;
      hueco.classList.add('es-rechazado');
    });
  }

  /* ------------------------------------------------------------- El cartel */
  function cartel() {
    var caja = document.createElement('div');
    caja.className = 'cookies';
    caja.setAttribute('role', 'dialog');
    caja.setAttribute('aria-modal', 'false');
    caja.setAttribute('aria-labelledby', 'cookies-titulo');
    caja.innerHTML =
      '<div class="cookies__int">' +
      '<div class="cookies__texto">' +
      '<p class="cookies__titulo" id="cookies-titulo">Cookies de terceros</p>' +
      '<p>Para enseñarle el mapa y el sistema de reservas tenemos que cargar ' +
      '<b>Google Maps</b> y <b>Tableo</b>, que instalan cookies propias. ' +
      'No usamos analítica ni publicidad. ' +
      '<a href="politica-privacidad.html#cookies">Más detalle</a>.</p>' +
      '</div>' +
      '<div class="cookies__botones">' +
      '<button type="button" class="boton boton--fantasma" data-cookies-no>Solo lo imprescindible</button>' +
      '<button type="button" class="boton" data-cookies-si>Aceptar</button>' +
      '</div>' +
      '</div>';
    document.body.appendChild(caja);

    requestAnimationFrame(function () { caja.classList.add('es-visible'); });

    function cerrar(acepta) {
      guardar(acepta);
      caja.classList.remove('es-visible');
      window.setTimeout(function () { caja.remove(); }, 320);
      if (acepta) cargar(); else rechazar();
    }

    caja.querySelector('[data-cookies-si]').addEventListener('click', function () { cerrar(true); });
    caja.querySelector('[data-cookies-no]').addEventListener('click', function () { cerrar(false); });
  }

  /* --------------------------------------------------------------- Arranque */
  function arrancar() {
    var d = leer();
    if (d && d.acepta) { cargar(); return; }
    if (d && !d.acepta) { rechazar(); return; }
    /* Sin decision todavia: se pregunta en cualquier pagina, aunque esa
       pagina no lleve ningun incrustado. Asi la decision ya esta tomada
       cuando llegue a reservas, y el enlace "Cookies" del pie funciona
       desde donde sea. */
    cartel();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', arrancar);
  } else {
    arrancar();
  }

  /* Enlace del pie para volver a decidir: <a data-cookies-cambiar> */
  document.addEventListener('click', function (e) {
    var a = e.target.closest ? e.target.closest('[data-cookies-cambiar]') : null;
    if (!a) return;
    e.preventDefault();
    try { window.localStorage.removeItem(CLAVE); } catch (err) { /* nada */ }
    window.location.reload();
  });
}());
