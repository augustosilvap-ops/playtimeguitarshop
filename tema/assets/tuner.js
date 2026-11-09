/*
 * Playtime — Afinador cromático no navegador (Web Audio API, autocorrelação).
 * Nada é gravado nem enviado: o áudio do microfone é analisado só no aparelho.
 */
(function () {
  var root = document.querySelector('[data-tuner]');
  if (!root) return;
  var NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'];
  var PT = { C: 'Dó', 'C#': 'Dó#', D: 'Ré', 'D#': 'Ré#', E: 'Mi', F: 'Fá', 'F#': 'Fá#', G: 'Sol', 'G#': 'Sol#', A: 'Lá', 'A#': 'Lá#', B: 'Si' };
  var PRESETS = {
    guitarra: [['E', 2], ['A', 2], ['D', 3], ['G', 3], ['B', 3], ['E', 4]],
    baixo: [['E', 1], ['A', 1], ['D', 2], ['G', 2]],
    dropd: [['D', 2], ['A', 2], ['D', 3], ['G', 3], ['B', 3], ['E', 4]]
  };
  var noteEl = root.querySelector('[data-note]');
  var freqEl = root.querySelector('[data-freq]');
  var statusEl = root.querySelector('[data-status]');
  var needle = root.querySelector('.tuner__needle');
  var startBtn = root.querySelector('[data-start]');
  var stringsEl = root.querySelector('.tuner__strings');
  var preset = 'guitarra';
  var ctx, analyser, buf, raf, stream, smooth = 0;

  function freqOf(name, oct) { var n = NOTES.indexOf(name) + (oct + 1) * 12; return 440 * Math.pow(2, (n - 69) / 12); }

  function renderStrings() {
    stringsEl.innerHTML = '';
    PRESETS[preset].forEach(function (s) {
      var b = document.createElement('button');
      b.type = 'button';
      b.textContent = s[0];
      b.setAttribute('aria-label', 'Corda ' + PT[s[0]] + ' (' + freqOf(s[0], s[1]).toFixed(2).replace('.', ',') + ' Hz)');
      b.dataset.freq = freqOf(s[0], s[1]);
      b.addEventListener('click', function () { playRef(parseFloat(b.dataset.freq)); });
      stringsEl.appendChild(b);
    });
  }

  function playRef(f) {
    var c = ctx || new (window.AudioContext || window.webkitAudioContext)();
    ctx = c;
    var o = c.createOscillator(), g = c.createGain();
    o.type = 'triangle'; o.frequency.value = f;
    g.gain.setValueAtTime(0.0001, c.currentTime);
    g.gain.exponentialRampToValueAtTime(0.25, c.currentTime + 0.02);
    g.gain.exponentialRampToValueAtTime(0.0001, c.currentTime + 2.2);
    o.connect(g).connect(c.destination); o.start(); o.stop(c.currentTime + 2.3);
  }

  function autoCorrelate(b, rate) {
    var size = b.length, rms = 0, i;
    for (i = 0; i < size; i++) rms += b[i] * b[i];
    rms = Math.sqrt(rms / size);
    if (rms < 0.01) return -1;
    var r1 = 0, r2 = size - 1, th = 0.2;
    for (i = 0; i < size / 2; i++) if (Math.abs(b[i]) < th) { r1 = i; break; }
    for (i = 1; i < size / 2; i++) if (Math.abs(b[size - i]) < th) { r2 = size - i; break; }
    b = b.slice(r1, r2); size = b.length;
    var c = new Array(size).fill(0);
    for (i = 0; i < size; i++) for (var j = 0; j < size - i; j++) c[i] += b[j] * b[j + i];
    var d = 0; while (c[d] > c[d + 1]) d++;
    var max = -1, pos = -1;
    for (i = d; i < size; i++) if (c[i] > max) { max = c[i]; pos = i; }
    var T0 = pos, x1 = c[T0 - 1], x2 = c[T0], x3 = c[T0 + 1];
    var a = (x1 + x3 - 2 * x2) / 2, bb = (x3 - x1) / 2;
    if (a) T0 = T0 - bb / (2 * a);
    return rate / T0;
  }

  function tick() {
    analyser.getFloatTimeDomainData(buf);
    var f = autoCorrelate(buf, ctx.sampleRate);
    if (f > 25 && f < 1500) {
      var n = 12 * Math.log2(f / 440) + 69;
      var r = Math.round(n);
      var cents = Math.round((n - r) * 100);
      smooth = smooth * 0.7 + cents * 0.3;
      var name = NOTES[(r % 12 + 12) % 12];
      noteEl.textContent = name;
      noteEl.setAttribute('aria-label', PT[name]);
      freqEl.textContent = f.toFixed(1).replace('.', ',') + ' Hz · ' + (cents > 0 ? '+' : '') + cents + ' cents';
      needle.style.transform = 'rotate(' + Math.max(-50, Math.min(50, smooth)) * 0.9 + 'deg)';
      var inTune = Math.abs(cents) <= 4;
      statusEl.textContent = inTune ? 'Afinado' : (cents < 0 ? 'Abaixo — aperte a tarraxa' : 'Acima — afrouxe a tarraxa');
      statusEl.classList.toggle('is-in', inTune);
      Array.prototype.forEach.call(stringsEl.children, function (b) {
        b.classList.toggle('is-target', Math.abs(12 * Math.log2(f / parseFloat(b.dataset.freq))) < 0.5);
      });
    }
    raf = requestAnimationFrame(tick);
  }

  startBtn.addEventListener('click', function () {
    if (stream) { stop(); return; }
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) { statusEl.textContent = 'Seu navegador não permite usar o microfone.'; return; }
    navigator.mediaDevices.getUserMedia({ audio: { echoCancellation: false, noiseSuppression: false, autoGainControl: false } }).then(function (s) {
      stream = s;
      ctx = ctx || new (window.AudioContext || window.webkitAudioContext)();
      var src = ctx.createMediaStreamSource(s);
      analyser = ctx.createAnalyser(); analyser.fftSize = 2048;
      buf = new Float32Array(analyser.fftSize);
      src.connect(analyser);
      startBtn.textContent = 'Parar afinador';
      statusEl.textContent = 'Toque uma corda solta';
      tick();
    }).catch(function () { statusEl.textContent = 'Permita o acesso ao microfone para afinar.'; });
  });

  function stop() {
    cancelAnimationFrame(raf);
    stream.getTracks().forEach(function (t) { t.stop(); });
    stream = null;
    startBtn.textContent = 'Ativar microfone';
    statusEl.textContent = '';
  }

  Array.prototype.forEach.call(root.querySelectorAll('.tuner__presets button'), function (b) {
    b.addEventListener('click', function () {
      preset = b.dataset.preset;
      Array.prototype.forEach.call(root.querySelectorAll('.tuner__presets button'), function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
      renderStrings();
    });
  });
  renderStrings();
})();
