// Diagnóstico das conexões (sem mostrar chaves).
import { ok, deny } from "../lib/auth.js";
import * as kv from "../lib/kv.js";
const cut = (s) => String(s).slice(0, 300);
export async function GET(req) {
  if (!ok(req)) return deny();
  const out = {
    variaveis: {
      SHOPIFY_STORE: !!process.env.SHOPIFY_STORE,
      SHOPIFY_CLIENT_ID: !!process.env.SHOPIFY_CLIENT_ID, SHOPIFY_CLIENT_SECRET: !!process.env.SHOPIFY_CLIENT_SECRET, SHOPIFY_TOKEN: !!process.env.SHOPIFY_TOKEN,
      WINDSOR_API_KEY: !!process.env.WINDSOR_API_KEY,
      banco_upstash: kv.ready(),
    },
  };
  if (kv.ready()) {
    try { await kv.set("nexus:ping", { em: Date.now() }); out.banco = (await kv.get("nexus:ping")) ? "ok" : "leitura vazia"; }
    catch (e) { out.banco = "erro: " + cut(e.message); }
  } else out.banco = "não conectado (crie o Upstash Redis em Storage e conecte ao projeto)";
  const key = process.env.WINDSOR_API_KEY;
  if (key) {
    for (const [nome, c, f] of [["meta", "facebook", "campaign,spend,impressions,clicks"], ["instagram", "instagram", "account_name,account_id,followers_count"]]) {
      try {
        const r = await fetch(`https://connectors.windsor.ai/${c}?` + new URLSearchParams({ api_key: key, fields: f, date_preset: "last_7d" }));
        const t = await r.text();
        out["windsor_" + nome] = { http: r.status, inicio: cut(t) };
      } catch (e) { out["windsor_" + nome] = "erro: " + cut(e.message); }
    }
  } else out.windsor = "WINDSOR_API_KEY não configurada";
  return Response.json(out);
}
