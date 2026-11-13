/* =========================================================
   MARCELA CÓRDOBA — script.js
   ========================================================= */
(function () {
  'use strict';
  var CFG = window.MC_CONFIG || {};

  /* ---------- Fuente del lead (primera visita de la sesión) ---------- */
  function safeGet(k) { try { return sessionStorage.getItem(k); } catch (e) { return null; } }
  function safeSet(k, v) { try { sessionStorage.setItem(k, v); } catch (e) {} }
  (function captureSource() {
    if (safeGet('mc_source')) return;
    var p = new URLSearchParams(location.search);
    var utm = ['utm_source', 'utm_medium', 'utm_campaign'].map(function (k) { return p.get(k); }).filter(Boolean).join(' / ');
    var ref = document.referrer && document.referrer.indexOf(location.host) === -1 ? document.referrer : '';
    safeSet('mc_source', utm || ref || 'directo');
    safeSet('mc_landing', location.pathname);
  })();

  /* ---------- Analítica (solo si hay IDs en config.js) ---------- */
  if (CFG.ga4Id) {
    var g = document.createElement('script');
    g.async = true; g.src = 'https://www.googletagmanager.com/gtag/js?id=' + CFG.ga4Id;
    document.head.appendChild(g);
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { dataLayer.push(arguments); };
    gtag('js', new Date()); gtag('config', CFG.ga4Id);
  }
  if (CFG.metaPixelId) {
    !function (f, b, e, v, n, t, s) { if (f.fbq) return; n = f.fbq = function () { n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments) }; if (!f._fbq) f._fbq = n; n.push = n; n.loaded = !0; n.version = '2.0'; n.queue = []; t = b.createElement(e); t.async = !0; t.src = v; s = b.getElementsByTagName(e)[0]; s.parentNode.insertBefore(t, s) }(window, document, 'script', 'https://connect.facebook.net/en_US/fbevents.js');
    fbq('init', CFG.metaPixelId); fbq('track', 'PageView');
  }
  function track(name, data) {
    if (window.gtag) gtag('event', name, data || {});
    if (window.fbq && name === 'generate_lead') fbq('track', 'Lead', data || {});
  }

  /* ---------- Navegación ---------- */
  var nav = document.getElementById('nav');
  var burger = document.getElementById('burger');
  function onScroll() { nav.classList.toggle('scrolled', window.scrollY > 12); }
  window.addEventListener('scroll', onScroll, { passive: true }); onScroll();

  burger.addEventListener('click', function () {
    var open = nav.classList.toggle('menu-open');
    burger.setAttribute('aria-expanded', open);
    document.body.style.overflow = open ? 'hidden' : '';
  });
  document.querySelectorAll('.has-sub > .nav-link').forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      e.preventDefault();
      var li = btn.parentElement, open = li.classList.toggle('open');
      btn.setAttribute('aria-expanded', open);
    });
  });
  document.addEventListener('click', function (e) {
    document.querySelectorAll('.has-sub.open').forEach(function (li) {
      if (!li.contains(e.target) && window.innerWidth > 900) { li.classList.remove('open'); li.firstElementChild.setAttribute('aria-expanded', 'false'); }
    });
  });
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    document.querySelectorAll('.has-sub.open').forEach(function (li) { li.classList.remove('open'); });
    if (nav.classList.contains('menu-open')) burger.click();
  });
  document.querySelectorAll('.nav-menu a').forEach(function (a) {
    a.addEventListener('click', function () {
      if (nav.classList.contains('menu-open')) { nav.classList.remove('menu-open'); burger.setAttribute('aria-expanded', 'false'); document.body.style.overflow = ''; }
    });
  });

  /* ---------- Contacto desde config ---------- */
  document.querySelectorAll('[data-wa]').forEach(function (a) {
    if (!CFG.whatsapp) { a.closest('[data-wa-wrap]') ? a.closest('[data-wa-wrap]').remove() : a.remove(); return; }
    a.href = 'https://wa.me/' + CFG.whatsapp + '?text=' + encodeURIComponent('Hola Marcela, quiero dar el primer paso.');
  });
  document.querySelectorAll('[data-phone]').forEach(function (el) { el.textContent = CFG.phoneLabel || ''; });
  document.querySelectorAll('[data-email]').forEach(function (el) {
    if (!CFG.email) { (el.closest('[data-email-wrap]') || el).remove(); return; }
    el.textContent = CFG.email;
    var link = el.tagName === 'A' ? el : el.closest('a'); if (link) link.href = 'mailto:' + CFG.email;
  });

  /* ---------- Revelado al hacer scroll ---------- */
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    document.querySelectorAll('.reveal').forEach(function (el) { io.observe(el); });
  } else {
    document.querySelectorAll('.reveal').forEach(function (el) { el.classList.add('in'); });
  }

  /* ---------- Barra CTA fija en móvil ---------- */
  var mcta = document.querySelector('.mobile-cta');
  if (mcta) {
    document.body.classList.add('has-mobile-cta');
    var hero = document.querySelector('.hero');
    var forms = document.querySelectorAll('.form-section, .footer');
    var heroGone = false, formVisible = false;
    function upd() { mcta.classList.toggle('show', heroGone && !formVisible); }
    new IntersectionObserver(function (en) { heroGone = !en[0].isIntersecting; upd(); }).observe(hero);
    var vis = new Set();
    var fo = new IntersectionObserver(function (en) {
      en.forEach(function (e) { e.isIntersecting ? vis.add(e.target) : vis.delete(e.target); });
      formVisible = vis.size > 0; upd();
    });
    forms.forEach(function (f) { fo.observe(f); });
  }

  /* ---------- Formularios de leads ---------- */
  function pad(n) { return n < 10 ? '0' + n : n; }
  function nowLocal() { var d = new Date(); return d.getFullYear() + '-' + pad(d.getMonth() + 1) + '-' + pad(d.getDate()) + ' ' + pad(d.getHours()) + ':' + pad(d.getMinutes()); }

  document.querySelectorAll('form.lead-form').forEach(function (form) {
    var card = form.closest('.form-card');
    var success = card.querySelector('.form-success');
    var errorBox = form.querySelector('.form-error');
    var btn = form.querySelector('button[type="submit"]');

    form.addEventListener('input', function (e) {
      var f = e.target.closest('.field'); if (f) f.classList.remove('invalid');
    });

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      errorBox.classList.remove('show');

      // Validación propia (mensajes claros, también para grupos de opciones)
      var firstBad = null;
      form.querySelectorAll('[required]').forEach(function (el) {
        var ok = el.type === 'checkbox' ? el.checked : (el.type === 'radio' ? !!form.querySelector('[name="' + el.name + '"]:checked') : el.checkValidity());
        var field = el.closest('.field') || el.closest('.consent');
        if (!ok) { if (field) field.classList.add('invalid'); firstBad = firstBad || el; }
      });
      if (firstBad) {
        errorBox.textContent = 'Revisa los campos marcados con * para continuar.';
        errorBox.classList.add('show');
        var det = firstBad.closest('details'); if (det) det.open = true;
        firstBad.focus({ preventScroll: true });
        firstBad.scrollIntoView({ behavior: 'smooth', block: 'center' });
        return;
      }

      var fd = new FormData(form);
      if (fd.get('botcheck')) return;
      var service = form.dataset.service;
      fd.set('servicio_de_interes', service);
      fd.set('pagina_de_origen', location.pathname);
      fd.set('fuente', safeGet('mc_source') || 'directo');
      fd.set('pagina_de_entrada', safeGet('mc_landing') || location.pathname);
      fd.set('fecha', nowLocal());

      var data = {};
      fd.forEach(function (v, k) { if (k === 'botcheck') return; data[k] = data[k] ? data[k] + ', ' + v : v; });

      var payload = Object.assign({}, data, {
        access_key: CFG.web3formsKey,
        subject: 'Nuevo lead web — ' + service,
        from_name: 'Web Marcela Córdoba',
        replyto: data.correo || ''
      });

      btn.disabled = true;
      var label = btn.textContent; btn.textContent = 'Enviando…';

      var jobs = [];
      jobs.push(fetch('https://api.web3forms.com/submit', {
        method: 'POST', headers: { 'Content-Type': 'application/json', Accept: 'application/json' }, body: JSON.stringify(payload)
      }).then(function (r) { return r.json(); }).then(function (j) { if (!j.success) throw new Error(j.message || 'error'); }));

      if (CFG.crmWebhook) {
        // No bloquea la confirmación si el CRM falla: el lead ya llegó por correo
        fetch(CFG.crmWebhook, { method: 'POST', mode: 'no-cors', headers: { 'Content-Type': 'text/plain' }, body: JSON.stringify(data), keepalive: true }).catch(function () {});
      }

      Promise.all(jobs).then(function () {
        form.style.display = 'none';
        success.classList.add('show');
        card.scrollIntoView({ behavior: 'smooth', block: 'center' });
        track('generate_lead', { servicio: service });
      }).catch(function () {
        btn.disabled = false; btn.textContent = label;
        errorBox.innerHTML = 'No pudimos enviar tu solicitud. Intenta de nuevo o escríbenos por <a href="#" data-wa-inline>WhatsApp</a>.';
        var w = errorBox.querySelector('[data-wa-inline]');
        if (CFG.whatsapp) w.href = 'https://wa.me/' + CFG.whatsapp; else w.replaceWith('nuestros canales de contacto');
        errorBox.classList.add('show');
      });
    });
  });

  /* ---------- Galería (lightbox) ---------- */
  var lb = document.getElementById('lightbox');
  if (lb) {
    var items = Array.prototype.slice.call(document.querySelectorAll('.gallery button'));
    var img = lb.querySelector('img'), cur = 0;
    function show(i) { cur = (i + items.length) % items.length; var s = items[cur].querySelector('img'); img.src = s.src; img.alt = s.alt; }
    items.forEach(function (b, i) { b.addEventListener('click', function () { show(i); lb.classList.add('open'); document.body.style.overflow = 'hidden'; lb.querySelector('.lb-close').focus(); }); });
    function close() { lb.classList.remove('open'); document.body.style.overflow = ''; items[cur].focus(); }
    lb.querySelector('.lb-close').addEventListener('click', close);
    lb.querySelector('.lb-prev').addEventListener('click', function () { show(cur - 1); });
    lb.querySelector('.lb-next').addEventListener('click', function () { show(cur + 1); });
    lb.addEventListener('click', function (e) { if (e.target === lb) close(); });
    document.addEventListener('keydown', function (e) {
      if (!lb.classList.contains('open')) return;
      if (e.key === 'Escape') close(); if (e.key === 'ArrowLeft') show(cur - 1); if (e.key === 'ArrowRight') show(cur + 1);
    });
  }

  /* ---------- Solo un video a la vez ---------- */
  var vids = document.querySelectorAll('video');
  vids.forEach(function (v) { v.addEventListener('play', function () { vids.forEach(function (o) { if (o !== v) o.pause(); }); }); });

  var y = document.getElementById('year'); if (y) y.textContent = new Date().getFullYear();
})();
