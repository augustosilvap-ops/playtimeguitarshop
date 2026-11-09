/* Playtime — frete pelo CEP, comparador, medida do braço, procedência e consultoria (sem dependências) */
(function () {
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var root = (window.Shopify && Shopify.routes && Shopify.routes.root) || '/';
  var brl = function (v) { return 'R$ ' + Number(v).toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 }); };
  var num = function (v) { return Number(v).toLocaleString('pt-BR', { minimumFractionDigits: 1, maximumFractionDigits: 1 }); };
  var store = {
    get: function (k, d) { try { var v = localStorage.getItem(k); return v ? JSON.parse(v) : d; } catch (e) { return d; } },
    set: function (k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }
  };
  var sleep = function (ms) { return new Promise(function (r) { setTimeout(r, ms); }); };
  var esc = function (s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };

  /* ---------------------------------------------------------------- frete */
  function maskCep(input) {
    input.addEventListener('input', function () {
      var d = input.value.replace(/\D/g, '').slice(0, 8);
      input.value = d.length > 5 ? d.slice(0, 5) + '-' + d.slice(5) : d;
    });
  }

  function lookupCep(d) {
    return fetch('https://viacep.com.br/ws/' + d + '/json/').then(function (r) { return r.json(); }).then(function (a) {
      if (!a || a.erro) throw new Error('cep');
      return a;
    });
  }

  function fetchRates(variant, cep, uf, inCart) {
    var params = new URLSearchParams({ 'shipping_address[zip]': cep, 'shipping_address[country]': 'Brazil', 'shipping_address[province]': uf });
    var added = null;
    var json = function (r) { return r.json(); };
    return fetch(root + 'cart.js').then(json).then(function (cart) {
      var has = cart.items.some(function (i) { return String(i.variant_id) === String(variant); });
      if (inCart || has || !variant) return null;
      // Peça ainda fora do carrinho: entra por alguns segundos só para a Shopify calcular, e sai logo depois.
      return fetch(root + 'cart/add.js', {
        method: 'POST', headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify({ items: [{ id: Number(variant), quantity: 1, properties: { _estimativa_frete: '1' } }] })
      }).then(json).then(function (r) { added = r.items && r.items[0] && r.items[0].key; });
    }).then(function () {
      return fetch(root + 'cart/prepare_shipping_rates.json?' + params, { method: 'POST' });
    }).then(function () {
      var tries = 0;
      function poll() {
        return fetch(root + 'cart/async_shipping_rates.json?' + params).then(function (r) {
          if (r.status === 200) return r.json();
          return null;
        }).then(function (j) {
          if (j && j.shipping_rates) return j.shipping_rates;
          if (++tries > 12) throw new Error('timeout');
          return sleep(700).then(poll);
        });
      }
      return poll();
    }).finally(function () {
      if (added) return fetch(root + 'cart/change.js', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ id: added, quantity: 0 }) });
    });
  }

  function days(rate) {
    var d = rate.delivery_days;
    if (d && d.length) { var a = d[0], b = d[d.length - 1]; return a === b ? a + ' dias úteis' : a + ' a ' + b + ' dias úteis'; }
    return '';
  }

  function renderRates(out, addr, rates) {
    if (!rates.length) { out.innerHTML = '<p class="ship__msg">Ainda não temos entrega automática para esse CEP. Fale com a gente no WhatsApp que a gente cota.</p>'; return; }
    rates.sort(function (a, b) { return parseFloat(a.price) - parseFloat(b.price); });
    out.innerHTML = '<p class="ship__place">' + esc(addr.localidade) + '/' + esc(addr.uf) + (addr.bairro ? ' · ' + esc(addr.bairro) : '') + '</p><ul class="ship__list">' +
      rates.map(function (r) {
        var p = parseFloat(r.price);
        return '<li><span class="ship__name">' + esc(r.presentment_name || r.name) + '<small>' + days(r) + '</small></span><strong>' + (p === 0 ? 'Grátis' : brl(p)) + '</strong></li>';
      }).join('') + '</ul><p class="ship__note">Com seguro e embalagem reforçada. O prazo conta a partir da regulagem e do envio.</p>';
  }

  function shipping() {
    $$('[data-ship]').forEach(function (box) {
      if (box.dataset.ready) return; box.dataset.ready = '1';
      var form = $('form', box), input = $('input', box), out = $('[data-ship-out]', box);
      maskCep(input);
      var saved = store.get('pt-cep', '');
      if (saved) input.value = saved;
      form.addEventListener('submit', function (e) {
        e.preventDefault();
        var d = input.value.replace(/\D/g, '');
        if (d.length !== 8) { out.innerHTML = '<p class="ship__msg ship__msg--err">Digite os 8 números do CEP.</p>'; input.focus(); return; }
        var cep = d.slice(0, 5) + '-' + d.slice(5);
        store.set('pt-cep', cep);
        var btn = $('button', form); btn.disabled = true;
        out.innerHTML = '<p class="ship__msg"><span class="ship__spin" aria-hidden="true"></span>Calculando…</p>';
        var demo = box.hasAttribute('data-demo');
        lookupCep(d).catch(function () { if (demo) return { localidade: 'Curitiba', uf: 'PR', bairro: '' }; throw new Error('cep'); }).then(function (addr) {
          if (demo) return sleep(700).then(function () { renderRates(out, addr, JSON.parse(box.getAttribute('data-demo'))); });
          return fetchRates(box.dataset.variant, cep, addr.uf, box.hasAttribute('data-in-cart')).then(function (rates) { renderRates(out, addr, rates); });
        }).catch(function (err) {
          out.innerHTML = '<p class="ship__msg ship__msg--err">' + (err && err.message === 'cep' ? 'Não encontramos esse CEP. Confira os números.' : 'Não foi possível calcular agora. Tente de novo ou fale com a gente no WhatsApp.') + '</p>';
        }).finally(function () { btn.disabled = false; });
      });
    });
  }

  /* ---------------------------------------------------------- comparador */
  var MAX = 3, KEY = 'pt-compare';
  function list() { return store.get(KEY, []); }
  function save(l) { store.set(KEY, l); sync(); }
  function toggle(item) {
    var l = list(), i = l.findIndex(function (x) { return x.handle === item.handle; });
    if (i >= 0) l.splice(i, 1);
    else if (l.length >= MAX) { toast('Dá para comparar até 3 peças. Tire uma para incluir esta.'); return; }
    else l.push(item);
    save(l);
  }
  function toast(msg) {
    var t = $('.pt-toast') || document.body.appendChild(Object.assign(document.createElement('div'), { className: 'pt-toast', role: 'status' }));
    t.textContent = msg; t.classList.add('is-on');
    clearTimeout(t._t); t._t = setTimeout(function () { t.classList.remove('is-on'); }, 2800);
  }
  function compareUrl() { return document.body.getAttribute('data-compare-url') || (root + 'pages/comparar'); }
  function sync() {
    var l = list();
    $$('[data-compare-toggle]').forEach(function (b) {
      var on = l.some(function (x) { return x.handle === b.dataset.handle; });
      b.setAttribute('aria-pressed', on ? 'true' : 'false');
      b.classList.toggle('is-on', on);
      var lab = $('[data-compare-label]', b) || b;
      lab.textContent = on ? 'Na comparação (' + l.length + '/3)' : (b.dataset.short ? 'Comparar' : 'Adicionar à comparação');
    });
    var bar = $('.compare-bar');
    if (!l.length) { if (bar) bar.classList.remove('is-on'); return; }
    if (!bar) {
      bar = document.createElement('div'); bar.className = 'compare-bar'; bar.setAttribute('role', 'region'); bar.setAttribute('aria-label', 'Comparação');
      document.body.appendChild(bar);
      bar.addEventListener('click', function (e) {
        var rm = e.target.closest('[data-compare-rm]');
        if (rm) { save(list().filter(function (x) { return x.handle !== rm.dataset.compareRm; })); }
        if (e.target.closest('[data-compare-clear]')) save([]);
      });
    }
    var slots = '';
    for (var i = 0; i < MAX; i++) {
      var x = l[i];
      slots += x ? '<div class="compare-bar__slot"><img src="' + esc(x.image) + '" alt=""><span>' + esc(x.title) + '</span><button type="button" data-compare-rm="' + esc(x.handle) + '" aria-label="Tirar ' + esc(x.title) + ' da comparação">×</button></div>'
                 : '<div class="compare-bar__slot compare-bar__slot--empty">+ peça</div>';
    }
    bar.innerHTML = '<div class="container compare-bar__inner"><div class="compare-bar__slots">' + slots + '</div><div class="compare-bar__actions"><button type="button" class="compare-bar__clear" data-compare-clear>Limpar</button><a class="btn btn--gold" href="' + compareUrl() + '"' + (l.length < 2 ? ' aria-disabled="true"' : '') + '>Comparar ' + l.length + '</a></div></div>';
    requestAnimationFrame(function () { bar.classList.add('is-on'); });
  }
  function compareButtons() {
    document.addEventListener('click', function (e) {
      var b = e.target.closest('[data-compare-toggle]');
      if (!b) return;
      e.preventDefault(); e.stopPropagation();
      toggle({ handle: b.dataset.handle, title: b.dataset.title, image: b.dataset.image });
    });
    sync();
  }

  function comparePage() {
    var box = $('[data-compare-page]');
    if (!box) return;
    var l = list();
    var empty = $('[data-compare-empty]', box), table = $('[data-compare-table]', box);
    if (l.length < 2) { empty.hidden = false; table.innerHTML = ''; return; }
    empty.hidden = true;
    table.innerHTML = '<p class="muted">Carregando…</p>';
    var get = function (h) {
      if (window.PT_COMPARE_DATA) return Promise.resolve(window.PT_COMPARE_DATA[h]);
      return fetch(root + 'products/' + encodeURIComponent(h) + '?view=comparar').then(function (r) { return r.text(); }).then(function (t) { return JSON.parse(t); });
    };
    Promise.all(l.map(function (x) { return get(x.handle).catch(function () { return null; }); })).then(function (items) {
      items = items.filter(Boolean);
      if (items.length < 2) { empty.hidden = false; table.innerHTML = ''; return; }
      var labels = items[0].specs.map(function (s) { return s.label; });
      var head = '<tr><th scope="col"><span class="visually-hidden">Característica</span></th>' + items.map(function (p) {
        return '<th scope="col"><a class="cmp__prod" href="' + esc(p.url) + '"><img src="' + esc(p.image) + '" alt="" loading="lazy"><span class="product-card__brand">' + esc(p.vendor) + '</span><strong>' + esc(p.title) + '</strong><span class="cmp__price">' + esc(p.price) + '</span></a>' +
          '<button type="button" class="cmp__rm" data-cmp-rm="' + esc(p.handle) + '">Tirar</button></th>';
      }).join('') + '</tr>';
      var rows = labels.map(function (lab, i) {
        var vals = items.map(function (p) { return (p.specs[i] && p.specs[i].value) || ''; });
        if (!vals.some(Boolean)) return '';
        var diff = vals.filter(Boolean).some(function (v) { return v !== vals.filter(Boolean)[0]; });
        return '<tr class="' + (diff ? 'is-diff' : '') + '"><th scope="row">' + esc(lab) + '</th>' + vals.map(function (v) { return '<td>' + (v ? esc(v) : '<span class="muted">—</span>') + '</td>'; }).join('') + '</tr>';
      }).join('');
      if (!rows) rows = '<tr><td colspan="' + (items.length + 1) + '" class="muted">Essas peças ainda não têm ficha técnica cadastrada. Veja a descrição de cada uma.</td></tr>';
      table.innerHTML = '<div class="cmp__scroll"><table class="cmp"><thead>' + head + '</thead><tbody>' + rows + '</tbody></table></div><p class="field__help">Linhas destacadas mostram onde as peças são diferentes.</p>';
    });
    if (box.dataset.ready) return; box.dataset.ready = '1';
    box.addEventListener('click', function (e) {
      var rm = e.target.closest('[data-cmp-rm]');
      if (rm) { save(list().filter(function (x) { return x.handle !== rm.dataset.cmpRm; })); comparePage(); }
    });
  }

  /* ------------------------------------------------------ medida do braço */
  function neck() {
    $$('[data-neck]').forEach(function (box) {
      if (box.dataset.ready) return; box.dataset.ready = '1';
      var out = $('[data-neck-out]', box);
      var refs = { e1: parseFloat(box.dataset.e1), e12: parseFloat(box.dataset.e12) };
      var names = { e1: '1ª casa', e12: '12ª casa' };
      function run() {
        var html = '';
        $$('[data-neck-in]', box).forEach(function (inp) {
          var k = inp.dataset.neckIn, mine = parseFloat(inp.value.replace(',', '.')), ref = refs[k];
          if (!(mine > 5 && mine < 40) || !ref) return;
          var d = ref - mine, abs = Math.abs(d);
          var txt = abs < 0.25 ? 'praticamente igual ao seu' : num(abs) + ' mm ' + (d < 0 ? 'mais fino' : 'mais grosso') + ' que o seu';
          var max = Math.max(ref, mine) * 1.08;
          html += '<div class="neck__row"><p><strong>' + names[k] + ':</strong> este braço é ' + txt + '.</p>' +
            '<div class="neck__bar"><span>Este</span><i style="--w:' + (ref / max * 100).toFixed(1) + '%"></i><b>' + num(ref) + ' mm</b></div>' +
            '<div class="neck__bar neck__bar--mine"><span>O seu</span><i style="--w:' + (mine / max * 100).toFixed(1) + '%"></i><b>' + num(mine) + ' mm</b></div></div>';
        });
        out.innerHTML = html;
      }
      $$('[data-neck-in]', box).forEach(function (i) { i.addEventListener('input', run); });
    });
  }

  /* -------------------------------------------------- copiar nº de série */
  function copySerial() {
    document.addEventListener('click', function (e) {
      var b = e.target.closest('[data-copy-btn]');
      if (!b) return;
      var v = $('[data-copy]', b.parentNode).getAttribute('data-copy');
      var done = function () { b.textContent = 'Copiado'; setTimeout(function () { b.textContent = 'Copiar'; }, 1800); };
      if (navigator.clipboard) navigator.clipboard.writeText(v).then(done, done); else done();
    });
  }

  /* --------------------------------------------------------- consultoria */
  function consult() {
    var form = $('[data-consult]');
    if (!form) return;
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var fd = new FormData(form);
      var name = (fd.get('nome') || '').trim();
      if (!name) { var n = form.querySelector('[name="nome"]'); n.focus(); n.setAttribute('aria-invalid', 'true'); return; }
      var lines = [
        'Olá, Playtime! Quero agendar uma consultoria por vídeo.',
        '• Nome: ' + name,
        '• Toco: ' + (fd.getAll('toca').join(', ') || '-'),
        '• Nível: ' + (fd.get('nivel') || '-'),
        '• Procuro: ' + (fd.get('procura') || '-'),
        '• Orçamento: ' + (fd.get('orcamento') || '-'),
        '• Melhor horário: ' + (fd.get('dia') || '-') + ', ' + (fd.get('hora') || '-'),
        '• Formato: ' + (fd.get('formato') || '-')
      ];
      var wa = form.getAttribute('data-whatsapp');
      var url = 'https://wa.me/' + wa + '?text=' + encodeURIComponent(lines.join('\n'));
      var ok = $('[data-consult-ok]');
      if (ok) { ok.hidden = false; $('a', ok).href = url; ok.scrollIntoView({ behavior: 'smooth', block: 'center' }); }
      window.open(url, '_blank', 'noopener');
    });
  }

  function boot() { shipping(); compareButtons(); comparePage(); neck(); copySerial(); consult(); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
  document.addEventListener('shopify:section:load', function () { shipping(); sync(); comparePage(); neck(); });
  window.PlaytimeExtras = { sync: sync, comparePage: comparePage };
})();
