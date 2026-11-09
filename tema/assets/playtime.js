/* Playtime — interações do tema (sem dependências) */
(function () {
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var money = function (v) { return 'R$ ' + Number(v).toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 }); };

  /* ---------- menu mobile ---------- */
  function menu() {
    var btn = $('.menu-toggle'), nav = $('.site-nav');
    if (!btn || !nav) return;
    btn.addEventListener('click', function () {
      var open = nav.classList.toggle('is-open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      document.body.style.overflow = open ? 'hidden' : '';
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('is-open')) { btn.click(); btn.focus(); }
    });
  }

  /* ---------- revelação ao rolar ---------- */
  function reveal() {
    var els = $$('[data-reveal]');
    if (reduce || !('IntersectionObserver' in window)) { els.forEach(function (e) { e.classList.add('is-in'); }); return; }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('is-in'); io.unobserve(en.target); } });
    }, { threshold: 0.15, rootMargin: '0px 0px -40px 0px' });
    els.forEach(function (e) { io.observe(e); });
  }

  /* ---------- adicionar ao carrinho sem recarregar ---------- */
  function cart() {
    $$('form[data-ajax-cart]').forEach(function (form) {
      form.addEventListener('submit', function (e) {
        if (!window.fetch) return;
        e.preventDefault();
        var btn = form.querySelector('[type="submit"]');
        var label = btn ? btn.innerHTML : '';
        if (btn) { btn.disabled = true; btn.textContent = 'Adicionando…'; }
        fetch((window.Shopify && Shopify.routes ? Shopify.routes.root : '/') + 'cart/add.js', {
          method: 'POST', headers: { 'Accept': 'application/json' }, body: new FormData(form)
        }).then(function (r) { return r.json().then(function (j) { if (!r.ok) throw j; return j; }); })
          .then(function () { return fetch((window.Shopify && Shopify.routes ? Shopify.routes.root : '/') + 'cart.js').then(function (r) { return r.json(); }); })
          .then(function (c) {
            $$('[data-cart-count]').forEach(function (el) { el.textContent = c.item_count; el.hidden = c.item_count === 0; });
            if (btn) { btn.textContent = 'Adicionado ao carrinho'; }
            setTimeout(function () { if (btn) { btn.disabled = false; btn.innerHTML = label; } }, 2200);
          })
          .catch(function (err) {
            if (btn) { btn.disabled = false; btn.innerHTML = label; }
            var msg = form.querySelector('[data-cart-error]');
            if (msg) { msg.textContent = (err && err.description) || 'Não foi possível adicionar. Tente novamente.'; msg.hidden = false; }
          });
      });
    });
    $$('[data-qty]').forEach(function (wrap) {
      var input = wrap.querySelector('input');
      wrap.addEventListener('click', function (e) {
        var b = e.target.closest('button'); if (!b) return;
        var v = Math.max(1, (parseInt(input.value, 10) || 1) + (b.dataset.step === 'up' ? 1 : -1));
        input.value = v;
      });
    });
  }

  /* ---------- índice do guia (Clínica) ---------- */
  function toc() {
    var links = $$('.guide__toc a');
    if (!links.length || !('IntersectionObserver' in window)) return;
    var map = {};
    links.forEach(function (a) { var id = a.getAttribute('href').slice(1); var t = document.getElementById(id); if (t) map[id] = a; });
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { links.forEach(function (l) { l.classList.remove('is-active'); }); var a = map[en.target.id]; if (a) a.classList.add('is-active'); }
      });
    }, { rootMargin: '-30% 0px -60% 0px' });
    Object.keys(map).forEach(function (id) { io.observe(document.getElementById(id)); });
  }

  /* ---------- "Ouça esta peça" ---------- */
  function sound() {
    $$('[data-sound-demo]').forEach(function (box) {
      var audio = new Audio();
      audio.preload = 'none';
      var bars = $$('.sound-demo__wave i', box);
      var btns = $$('.sound-demo__tracks button', box);
      var play = $('[data-sound-play]', box);
      var status = $('[data-sound-status]', box);
      function paint() {
        var p = audio.duration ? audio.currentTime / audio.duration : 0;
        var n = Math.round(p * bars.length);
        bars.forEach(function (b, i) { b.classList.toggle('is-played', i < n); });
        if (!audio.paused) requestAnimationFrame(paint);
      }
      function select(btn) {
        btns.forEach(function (b) { b.setAttribute('aria-pressed', b === btn ? 'true' : 'false'); });
        audio.src = btn.getAttribute('data-src');
        audio.play().then(function () { play.textContent = 'Pausar'; status.textContent = 'Tocando: ' + btn.textContent; paint(); }).catch(function () {});
      }
      btns.forEach(function (b) { b.addEventListener('click', function () { select(b); }); });
      play.addEventListener('click', function () {
        if (!audio.src) { if (btns[0]) select(btns[0]); return; }
        if (audio.paused) { audio.play(); play.textContent = 'Pausar'; paint(); } else { audio.pause(); play.textContent = 'Ouvir'; }
      });
      audio.addEventListener('ended', function () { play.textContent = 'Ouvir'; status.textContent = ''; });
    });
  }

  /* ---------- visualizador 360° (arrastar) ---------- */
  function viewer360() {
    $$('[data-viewer360]').forEach(function (v) {
      var img = $('img', v);
      var srcs = JSON.parse(v.getAttribute('data-frames') || '[]');
      if (srcs.length < 2) return;
      srcs.forEach(function (s) { var i = new Image(); i.src = s; });
      var idx = 0, startX = null, startIdx = 0;
      function show(i) { idx = (i % srcs.length + srcs.length) % srcs.length; img.src = srcs[idx]; }
      v.addEventListener('pointerdown', function (e) { startX = e.clientX; startIdx = idx; v.setPointerCapture(e.pointerId); });
      v.addEventListener('pointermove', function (e) { if (startX === null) return; show(startIdx + Math.round((e.clientX - startX) / 12)); });
      v.addEventListener('pointerup', function () { startX = null; });
      v.addEventListener('keydown', function (e) { if (e.key === 'ArrowLeft') show(idx - 1); if (e.key === 'ArrowRight') show(idx + 1); });
    });
  }

  /* ---------- pré-avaliação de troca ---------- */
  function tradeIn() {
    var form = $('[data-trade-in]');
    if (!form) return;
    var out = $('[data-estimate]', form.parentNode) || $('[data-estimate]');
    var factor = { 'impecavel': [0.68, 0.78], 'otimo': [0.58, 0.68], 'bom': [0.46, 0.58], 'regular': [0.32, 0.46] };
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var fd = new FormData(form);
      var ref = parseFloat(String(fd.get('referencia') || '').replace(/\./g, '').replace(',', '.'));
      var cond = fd.get('condicao') || 'bom';
      var f = factor[cond] || factor.bom;
      if (fd.get('case') === 'sim') f = [f[0] + 0.02, f[1] + 0.02];
      if (fd.get('modificado') === 'sim') f = [f[0] - 0.04, f[1] - 0.02];
      var text = 'Olá, Playtime! Quero avaliar meu instrumento para troca:%0A' +
        '• Tipo: ' + encodeURIComponent(fd.get('tipo') || '') + '%0A' +
        '• Marca/modelo: ' + encodeURIComponent((fd.get('marca') || '') + ' ' + (fd.get('modelo') || '')) + '%0A' +
        '• Ano: ' + encodeURIComponent(fd.get('ano') || '-') + '%0A' +
        '• Estado: ' + encodeURIComponent(cond) + '%0A' +
        '• Case original: ' + encodeURIComponent(fd.get('case') || '-') + '%0A' +
        '• Modificações: ' + encodeURIComponent(fd.get('modificado') || '-') + '%0A' +
        '• Interesse: ' + encodeURIComponent(fd.get('interesse') || '-');
      var wa = out.getAttribute('data-whatsapp');
      var range = $('[data-estimate-range]', out), link = $('[data-estimate-link]', out);
      if (ref > 0) {
        range.textContent = money(Math.round(ref * f[0] / 50) * 50) + ' a ' + money(Math.round(ref * f[1] / 50) * 50);
      } else {
        range.textContent = 'Informe o valor de referência para ver a faixa';
      }
      link.href = 'https://wa.me/' + wa + '?text=' + text;
      out.hidden = false;
      out.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'center' });
    });
  }

  /* ---------- vídeos: pausa quando sai da tela / respeita movimento reduzido ---------- */
  function videos() {
    var vids = $$('.media-frame video, video[data-autoplay]');
    if (!vids.length) return;
    if (reduce) { vids.forEach(function (v) { v.removeAttribute('autoplay'); v.pause(); v.controls = true; }); return; }
    if (!('IntersectionObserver' in window)) return;
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { var p = en.target.play(); if (p && p.catch) p.catch(function () {}); } else en.target.pause(); });
    }, { threshold: 0.2 });
    vids.forEach(function (v) { io.observe(v); });
  }

  function boot() { menu(); reveal(); cart(); toc(); sound(); viewer360(); tradeIn(); videos(); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
  document.addEventListener('shopify:section:load', function () { reveal(); videos(); viewer360(); sound(); });
})();
