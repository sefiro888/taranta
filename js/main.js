/* =========================================================================
   LA TARANTA - Comportamiento general
   Sin dependencias externas. Funciona abriendo los archivos en local.
   ========================================================================= */
(function () {
  'use strict';

  /* ------------------------------------------------ Cabecera solida al bajar */
  var cabecera = document.querySelector('.cabecera');
  var ultimoScroll = 0;

  function alScroll() {
    var y = window.pageYOffset || document.documentElement.scrollTop;
    if (cabecera) cabecera.classList.toggle('es-solida', y > 60);
    ultimoScroll = y;
  }
  alScroll();
  window.addEventListener('scroll', alScroll, { passive: true });

  /* ------------------------------------------------------------ Menu movil */
  var boton = document.querySelector('.hamburguesa');
  var panel = document.getElementById('menu-movil');

  function cerrarMenu() {
    if (!panel || !boton) return;
    panel.classList.remove('es-abierto');
    boton.setAttribute('aria-expanded', 'false');
    document.body.style.overflow = '';
  }

  if (boton && panel) {
    boton.addEventListener('click', function () {
      var abierto = panel.classList.toggle('es-abierto');
      boton.setAttribute('aria-expanded', abierto ? 'true' : 'false');
      document.body.style.overflow = abierto ? 'hidden' : '';
      if (abierto) {
        var primero = panel.querySelector('a');
        if (primero) primero.focus({ preventScroll: true });
      }
    });
    panel.addEventListener('click', function (e) {
      if (e.target.closest('a')) cerrarMenu();
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && panel.classList.contains('es-abierto')) {
        cerrarMenu();
        boton.focus();
      }
    });
  }

  /* --------------------------------------------- Aparicion suave al entrar */
  var revelables = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && revelables.length) {
    var obs = new IntersectionObserver(function (entradas) {
      entradas.forEach(function (e) {
        if (e.isIntersecting) {
          e.target.classList.add('es-visible');
          obs.unobserve(e.target);
        }
      });
    }, { threshold: 0.02, rootMargin: '0px 0px 180px 0px' });
    revelables.forEach(function (el) { obs.observe(el); });
  } else {
    revelables.forEach(function (el) { el.classList.add('es-visible'); });
  }

  /* Red de seguridad: nada puede quedarse invisible. Cualquier bloque que ya
     haya pasado por pantalla se muestra aunque el observador no lo detectase. */
  function rescatarOcultos() {
    document.querySelectorAll('.reveal:not(.es-visible)').forEach(function (el) {
      if (el.getBoundingClientRect().top < window.innerHeight + 60) {
        el.classList.add('es-visible');
      }
    });
  }
  var rescate;
  window.addEventListener('scroll', function () {
    clearTimeout(rescate);
    rescate = setTimeout(rescatarOcultos, 400);
  }, { passive: true });
  window.addEventListener('load', function () { setTimeout(rescatarOcultos, 1200); });
  window.addEventListener('resize', rescatarOcultos, { passive: true });

  /* ---------------------- Botones flotantes discretos mientras se hace scroll */
  var flotantes = document.querySelector('.flotantes');
  var temporizador;
  if (flotantes) {
    window.addEventListener('scroll', function () {
      flotantes.classList.add('es-discreto');
      clearTimeout(temporizador);
      temporizador = setTimeout(function () { flotantes.classList.remove('es-discreto'); }, 550);
    }, { passive: true });
  }

  /* ------------------------------------------------------------ Ano actual */
  var anos = document.querySelectorAll('[data-ano]');
  var ano = new Date().getFullYear();
  anos.forEach(function (el) { el.textContent = ano; });

  /* ------------------------------- Enlaces internos con cabecera fija */
  document.addEventListener('click', function (e) {
    var a = e.target.closest('a[href^="#"]');
    if (!a) return;
    var id = a.getAttribute('href');
    if (id.length < 2) return;
    var destino = document.querySelector(id);
    if (!destino) return;
    e.preventDefault();
    var alto = cabecera ? cabecera.offsetHeight : 0;
    var y = destino.getBoundingClientRect().top + window.pageYOffset - alto - 16;
    window.scrollTo({ top: y, behavior: 'smooth' });
    destino.setAttribute('tabindex', '-1');
    destino.focus({ preventScroll: true });
  });

  /* ------------------------------------ Aviso: demo sin envio a servidor */
  window.LT = window.LT || {};
  window.LT.telefono = '+34984265252';
  window.LT.whatsapp = '34621153815';
  window.LT.mensajeWA = 'Hola, me gustaría consultar disponibilidad para reservar en La Taranta.';
}());
