/*
 * Playtime — hero com rolagem cinematográfica.
 * Adaptação do runtime do ScrollCraft (frames em canvas controlados pela rolagem)
 * para funcionar como uma seção do Shopify: o canvas fica "preso" (sticky) apenas
 * enquanto a seção está na tela, e o progresso é calculado dentro da seção.
 * Mantém as regras do motor original: pré-carregamento por quadros-chave (a cada 5),
 * escala "cover", DPR limitado a 2, conjunto mobile separado e um único rAF por vez.
 */
(function () {
  function framePath(tpl, idx) {
    var s = String(idx);
    while (s.length < 4) s = '0' + s;
    return tpl.replace('0000', s);
  }

  function init(root) {
    var canvas = root.querySelector('.scroll-hero__canvas');
    var stage = root.querySelector('.scroll-hero__stage');
    if (!canvas || !stage) return;
    var ctx = canvas.getContext('2d');
    var steps = Array.prototype.slice.call(root.querySelectorAll('.scroll-hero__step'));
    var dots = Array.prototype.slice.call(root.querySelectorAll('.scroll-hero__progress span'));
    var hint = root.querySelector('.scroll-hero__hint');

    var desktopTpl = root.getAttribute('data-frames') || '';
    var mobileTpl = root.getAttribute('data-frames-mobile') || '';
    var desktopCount = parseInt(root.getAttribute('data-count'), 10) || 0;
    var mobileCount = parseInt(root.getAttribute('data-count-mobile'), 10) || 0;
    var hasMobile = !!(mobileTpl && mobileCount);
    var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    // Altura da pista: soma das alturas de cada passo (como no scrollcraft.json)
    var heights = steps.map(function (s) { return parseInt(s.getAttribute('data-scroll'), 10) || 1200; });
    var total = heights.reduce(function (a, b) { return a + b; }, 0);
    root.style.height = 'calc(100vh + ' + total + 'px)';
    var bounds = [];
    var acc = 0;
    heights.forEach(function (h) { bounds.push([acc / total, (acc + h) / total]); acc += h; });

    var mq = window.matchMedia('(max-width: 767px)');
    var isMobile = hasMobile && mq.matches;
    var desktopImages = new Array(desktopCount);
    var mobileImages = hasMobile ? new Array(mobileCount) : null;
    var currentFrame = 0;
    var activeStep = -1;

    function frameCount() { return isMobile ? mobileCount : desktopCount; }
    function images() { return (isMobile && mobileImages) ? mobileImages : desktopImages; }

    function resize() {
      var dpr = Math.min(window.devicePixelRatio || 1, 2);
      var w = stage.clientWidth, h = stage.clientHeight;
      canvas.width = Math.max(1, Math.round(w * dpr));
      canvas.height = Math.max(1, Math.round(h * dpr));
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      draw(currentFrame);
    }

    function draw(i) {
      var img = images()[i];
      if (!img || !img.complete || !img.naturalWidth || !img.naturalHeight) return;
      var w = stage.clientWidth, h = stage.clientHeight;
      var s = Math.max(w / img.naturalWidth, h / img.naturalHeight);
      var dw = img.naturalWidth * s, dh = img.naturalHeight * s;
      ctx.clearRect(0, 0, w, h);
      ctx.drawImage(img, (w - dw) / 2, (h - dh) / 2, dw, dh);
    }

    function preloadSet(count, tpl, target) {
      if (!count || !tpl) return;
      var STEP = 5, keys = [], settled = 0;
      for (var i = 0; i < count; i += STEP) keys.push(i);
      function one(idx, after) {
        var img = new Image();
        img.decoding = 'async';
        img.src = framePath(tpl, idx);
        img.onload = function () { target[idx] = img; if (idx === currentFrame) draw(idx); if (after) after(); };
        img.onerror = function () { if (after) after(); };
      }
      keys.forEach(function (k) {
        one(k, function () {
          settled++;
          if (settled === keys.length) for (var j = 0; j < count; j++) if (j % STEP) one(j);
        });
      });
    }

    var loaded = { d: false, m: false };
    function preload() {
      if (isMobile) { if (!loaded.m) { preloadSet(mobileCount, mobileTpl, mobileImages); loaded.m = true; } }
      else if (!loaded.d) { preloadSet(desktopCount, desktopTpl, desktopImages); loaded.d = true; }
    }

    function setStep(i) {
      if (i === activeStep) return;
      activeStep = i;
      steps.forEach(function (s, n) {
        var on = n === i;
        s.classList.toggle('is-active', on);
        s.setAttribute('aria-hidden', on ? 'false' : 'true');
        Array.prototype.forEach.call(s.querySelectorAll('a, button'), function (el) { el.tabIndex = on ? 0 : -1; });
      });
      dots.forEach(function (d, n) { d.classList.toggle('is-on', n <= i); });
    }

    var raf = 0;
    function update() {
      raf = 0;
      var rect = root.getBoundingClientRect();
      var track = root.offsetHeight - window.innerHeight;
      var p = track > 0 ? -rect.top / track : 0;
      p = Math.min(1, Math.max(0, p));
      var last = frameCount() - 1;
      var idx = last > 0 ? Math.round((reduce ? 0 : p) * last) : 0;
      if (idx !== currentFrame) { currentFrame = idx; draw(idx); }
      var step = 0;
      for (var i = 0; i < bounds.length; i++) if (p >= bounds[i][0]) step = i;
      setStep(step);
      if (hint) hint.style.opacity = p > 0.02 ? '0' : '1';
    }
    function onScroll() { if (!raf) raf = requestAnimationFrame(update); }

    if (hasMobile) {
      mq.addEventListener('change', function (e) { isMobile = e.matches; preload(); currentFrame = -1; resize(); onScroll(); });
    }

    // Só começa a baixar os quadros quando a seção está perto da tela
    if ('IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (entries) {
        if (entries[0].isIntersecting) { preload(); io.disconnect(); }
      }, { rootMargin: '200px' });
      io.observe(root);
    } else { preload(); }

    window.addEventListener('resize', resize, { passive: true });
    window.addEventListener('scroll', onScroll, { passive: true });
    resize();
    update();
  }

  function boot() { Array.prototype.forEach.call(document.querySelectorAll('[data-scroll-hero]'), init); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
  document.addEventListener('shopify:section:load', boot);
})();
