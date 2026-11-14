// Ponte: o Nexus foi escrito para rodar dentro do Claude (window.claude.use).
// Aqui, fora do Claude, cada capacidade é atendida pelas funções do próprio site.
(() => {
  const TK = "nexus_token";
  const tok = () => { try { return localStorage.getItem(TK) || ""; } catch { return ""; } };
  window.nexusLogout = () => { try { localStorage.removeItem(TK); } catch {} location.reload(); };
  async function api(path, opts = {}) {
    const r = await fetch(path, { ...opts, headers: { "Content-Type": "application/json", Authorization: "Bearer " + tok(), ...(opts.headers || {}) } });
    if (r.status === 401) { showLogin(); throw { code: "not_granted" }; }
    if (!r.ok) throw { code: "server_unavailable", status: r.status };
    return r.json();
  }
  function showLogin() {
    if (document.getElementById("nxLogin")) return;
    const d = document.createElement("div"); d.id = "nxLogin";
    d.innerHTML = `<form><svg viewBox="0 0 64 64" width="64" height="64"><g fill="none" stroke="#38D6FF" stroke-width="2.2"><path d="M32 4 56 18v28L32 60 8 46V18z"/></g><path d="M24 42V22l16 20V22" fill="none" stroke="#fff" stroke-width="3.2" stroke-linejoin="round" stroke-linecap="round"/></svg>
      <h1>NEXUS</h1><p>Digite sua senha para entrar</p><label for="nxPass" style="position:absolute;left:-9999px">Senha</label><input id="nxPass" type="password" autocomplete="current-password" placeholder="Senha" required>
      <button type="submit">Entrar</button><small id="nxErr"></small></form>`;
    document.body.appendChild(d);
    d.querySelector("form").addEventListener("submit", async (e) => {
      e.preventDefault(); const err = d.querySelector("#nxErr"); err.textContent = "Entrando…";
      const r = await fetch("/api/login", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ password: d.querySelector("#nxPass").value }) });
      const j = await r.json().catch(() => ({}));
      if (j.token) { try { localStorage.setItem(TK, j.token); } catch {} location.reload(); } else err.textContent = j.error || "Não foi possível entrar.";
    });
    setTimeout(() => d.querySelector("#nxPass").focus(), 50);
  }
  if (!tok()) document.addEventListener("DOMContentLoaded", showLogin);

  const endpoint = (server, input) => {
    if (server === "Shopify") return "/api/shopify";
    if (server === "Windsor_ai") {
      const q = new URLSearchParams({ c: input.connector, fields: (input.fields || []).join(",") });
      if (input.date_preset) q.set("preset", input.date_preset);
      if (input.accounts?.[0]) q.set("acc", input.accounts[0]);
      return "/api/windsor?" + q;
    }
    return null;
  };
  const mcp = {
    watchTool(server, tool, input, handler, opts = {}) {
      const url = endpoint(server, input); if (!url) return () => {};
      const run = () => api(url).then((payload) => handler({ type: "data", result: { payload, cache: { storedAt: Date.now() } } }))
        .catch((error) => handler({ type: "error", error }));
      run(); const id = setInterval(run, opts.refetchInterval || 300000); return () => clearInterval(id);
    },
    invalidate: async () => {}, listTools: async () => ({ servers: [] }),
    callTool: async () => { throw { code: "not_granted" }; },
  };
  const poll = (k, toSnap, cb, err) => {
    const run = () => api("/api/state?k=" + encodeURIComponent(k)).then((j) => cb(toSnap(j))).catch((e) => err && err(e));
    run(); const id = setInterval(run, 30000); return () => clearInterval(id);
  };
  const db = {
    doc: (k) => ({
      onSnapshot: (cb, err) => poll(k, (j) => ({ exists: j != null, data: () => j ?? undefined }), cb, err),
      set: (obj) => api("/api/state?k=" + encodeURIComponent(k), { method: "PUT", body: JSON.stringify(obj) }),
    }),
    collection: (k) => ({
      onSnapshot: (cb, err) => poll(k, (j) => ({ docs: Object.entries(j || {}).map(([id, d]) => ({ id, data: () => d })) }), cb, err),
      doc: (id) => ({ set: (obj) => api(`/api/state?k=${encodeURIComponent(k)}&id=${encodeURIComponent(id)}`, { method: "PUT", body: JSON.stringify(obj) }) }),
    }),
  };
  const tts = "speechSynthesis" in window ? {
    speak: (text) => new Promise((res) => { const u = new SpeechSynthesisUtterance(text); u.lang = "pt-BR"; u.onend = res; u.onerror = res; speechSynthesis.speak(u); }),
    stop: () => speechSynthesis.cancel(),
  } : null;
  let dictation = null;
  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (SR) {
    const rec = new SR(); rec.lang = "pt-BR"; rec.interimResults = true; rec.continuous = false;
    const hs = { p: () => {}, f: () => {}, s: () => {} };
    rec.onresult = (e) => { for (let i = e.resultIndex; i < e.results.length; i++) { const t = e.results[i][0].transcript; e.results[i].isFinal ? hs.f({ text: t }) : hs.p({ text: t }); } };
    rec.onstart = () => hs.s({ state: "listening" }); rec.onend = () => hs.s({ state: "idle", reason: "stopped" });
    dictation = { start: async () => rec.start(), stop: async () => rec.stop(), onPartial: (f) => (hs.p = f), onFinal: (f) => (hs.f = f), onState: (f) => (hs.s = f) };
  }
  const caps = { mcp, db, tts, dictation, sample: null, user: null, permissions: null };
  window.claude = { use: async (n) => (tok() ? caps[n] ?? null : null) };
})();
