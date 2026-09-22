/* =========================================================================
   LA TARANTA - Formularios (reservas, eventos, contacto, flamenco)
   -------------------------------------------------------------------------
   DEMO: ningun formulario envia datos a un servidor. Al validarse
   correctamente se muestra un mensaje de confirmacion y se ofrece continuar
   por WhatsApp o por telefono. Antes de publicar habra que conectar el
   formulario con el correo o el sistema de reservas del restaurante.
   ========================================================================= */
(function () {
  'use strict';

  var WA = (window.LT && window.LT.whatsapp) || '34621153815';

  function texto(el) { return (el.value || '').trim(); }

  function marcarError(campo, mensaje) {
    var cont = campo.closest('.campo') || campo.parentNode;
    cont.classList.add('campo--error');
    var hueco = cont.querySelector('.campo__error');
    if (hueco) hueco.textContent = mensaje;
    campo.setAttribute('aria-invalid', 'true');
  }

  function limpiarError(campo) {
    var cont = campo.closest('.campo') || campo.parentNode;
    cont.classList.remove('campo--error');
    var hueco = cont.querySelector('.campo__error');
    if (hueco) hueco.textContent = '';
    campo.removeAttribute('aria-invalid');
  }

  function validarCampo(campo) {
    var v = texto(campo);
    var tipo = campo.getAttribute('type');

    if (campo.hasAttribute('required')) {
      if (campo.type === 'checkbox' && !campo.checked) {
        marcarError(campo, 'Es necesario aceptar para continuar.');
        return false;
      }
      if (campo.type !== 'checkbox' && !v) {
        marcarError(campo, 'Este campo es obligatorio.');
        return false;
      }
    }
    if (tipo === 'email' && v && !/^[^\s@]+@[^\s@]+\.[a-z]{2,}$/i.test(v)) {
      marcarError(campo, 'Revise el correo electrónico.');
      return false;
    }
    if (tipo === 'tel' && v && !/^[+0-9()\s.-]{9,20}$/.test(v)) {
      marcarError(campo, 'Revise el número de teléfono.');
      return false;
    }
    if (campo.name === 'personas' && v && (isNaN(v) || Number(v) < 1)) {
      marcarError(campo, 'Indique al menos una persona.');
      return false;
    }
    if (tipo === 'date' && v) {
      var hoy = new Date(); hoy.setHours(0, 0, 0, 0);
      if (new Date(v + 'T00:00:00') < hoy) {
        marcarError(campo, 'Elija una fecha a partir de hoy.');
        return false;
      }
    }
    limpiarError(campo);
    return true;
  }

  function mensajeWhatsApp(form) {
    var d = new FormData(form);
    var tipo = form.getAttribute('data-form') || 'consulta';
    var lineas = [];

    if (tipo === 'reserva') {
      lineas.push('Hola, me gustaría consultar disponibilidad para reservar en La Taranta.');
      if (d.get('fecha')) lineas.push('Fecha: ' + d.get('fecha'));
      if (d.get('hora')) lineas.push('Hora: ' + d.get('hora'));
      if (d.get('personas')) lineas.push('Personas: ' + d.get('personas'));
      if (d.get('espacio')) lineas.push('Zona: ' + d.get('espacio'));
    } else if (tipo === 'evento') {
      lineas.push('Hola, me gustaría información para un evento en La Taranta.');
      if (d.get('tipo')) lineas.push('Tipo de evento: ' + d.get('tipo'));
      if (d.get('fecha')) lineas.push('Fecha prevista: ' + d.get('fecha'));
      if (d.get('personas')) lineas.push('Asistentes: ' + d.get('personas'));
    } else if (tipo === 'flamenco') {
      lineas.push('Hola, me gustaría información sobre el flamenco en La Taranta.');
    } else {
      lineas.push('Hola, me gustaría hacerles una consulta.');
    }

    if (d.get('nombre')) lineas.push('Nombre: ' + d.get('nombre'));
    if (d.get('mensaje')) lineas.push('Mensaje: ' + d.get('mensaje'));

    return 'https://wa.me/' + WA + '?text=' + encodeURIComponent(lineas.join('\n'));
  }

  document.querySelectorAll('form[data-form]').forEach(function (form) {
    var campos = Array.prototype.slice.call(form.querySelectorAll('input, select, textarea'));
    var exito = form.parentNode.querySelector('[data-form-exito]');

    campos.forEach(function (c) {
      c.addEventListener('blur', function () { if (texto(c) || c.hasAttribute('required')) validarCampo(c); });
      c.addEventListener('input', function () {
        var cont = c.closest('.campo');
        if (cont && cont.classList.contains('campo--error')) validarCampo(c);
      });
    });

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var valido = true;
      var primerFallo = null;

      campos.forEach(function (c) {
        if (!validarCampo(c)) {
          valido = false;
          if (!primerFallo) primerFallo = c;
        }
      });

      if (!valido) {
        if (primerFallo) primerFallo.focus();
        return;
      }

      var enlace = mensajeWhatsApp(form);
      if (exito) {
        var boton = exito.querySelector('[data-wa]');
        if (boton) boton.setAttribute('href', enlace);
        exito.classList.add('es-visible');
        exito.setAttribute('tabindex', '-1');
        exito.focus({ preventScroll: true });
        exito.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
      form.reset();
    });
  });

  /* ---------------------- Enlaces de WhatsApp con mensaje predefinido */
  document.querySelectorAll('[data-wa-simple]').forEach(function (a) {
    var msg = a.getAttribute('data-wa-simple') ||
      'Hola, me gustaría consultar disponibilidad para reservar en La Taranta.';
    a.setAttribute('href', 'https://wa.me/' + WA + '?text=' + encodeURIComponent(msg));
  });


  /* ------------------ Widget de reservas (Tableo): ajuste de altura
     Si el widget comunica su altura por postMessage, el marco se adapta.
     Si no lo hace, se queda con la altura definida en el CSS.             */
  var marcoReserva = document.querySelector('.widget-reserva iframe');
  if (marcoReserva) {
    /* Aviso de carga mientras el sistema de reservas se descarga */
    var cargando = document.querySelector('[data-widget-cargando]');
    if (cargando) {
      var listo = function () { cargando.classList.add('es-listo'); };
      marcoReserva.addEventListener('load', listo);
      setTimeout(listo, 9000);  // por si el evento no llegase
    }

    window.addEventListener('message', function (e) {
      var host = '';
      try { host = new URL(e.origin).hostname; } catch (err) { return; }
      if (!/(^|\.)tableo\.com$/.test(host)) return;

      var alto = null;
      var d = e.data;
      if (typeof d === 'number') alto = d;
      else if (typeof d === 'string' && /^\d+$/.test(d)) alto = parseInt(d, 10);
      else if (d && typeof d === 'object') alto = d.height || d.iframeHeight || (d.payload && d.payload.height);

      if (alto && alto > 400 && alto < 3000) marcoReserva.style.height = alto + 'px';
    });

    /* Los botones flotantes se apartan mientras el widget esta en pantalla:
       no deben taparle ningun control al que esta reservando. */
    var flotantes = document.querySelector('.flotantes');
    var caja = marcoReserva.closest('.widget-reserva');
    if (flotantes && caja && 'IntersectionObserver' in window) {
      var niveles = [];
      for (var i = 0; i <= 20; i++) niveles.push(i / 20);
      new IntersectionObserver(function (entradas) {
        entradas.forEach(function (e) {
          // Solo se apartan cuando el widget ocupa buena parte de la pantalla,
          // que es cuando el visitante esta realmente reservando.
          var cubre = e.intersectionRect.height / window.innerHeight;
          flotantes.classList.toggle('es-oculto', e.isIntersecting && cubre > 0.45);
        });
      }, { threshold: niveles }).observe(caja);
    }
  }

  /* ----------------- Fecha minima = hoy en los selectores de fecha */
  var hoy = new Date();
  var iso = hoy.getFullYear() + '-' +
    String(hoy.getMonth() + 1).padStart(2, '0') + '-' +
    String(hoy.getDate()).padStart(2, '0');
  document.querySelectorAll('input[type="date"]').forEach(function (i) {
    if (!i.getAttribute('min')) i.setAttribute('min', iso);
  });
}());
