// Notícias do dia via Google Notícias (RSS), sem IA. Atualiza uma vez por dia (horário de Brasília) e guarda no Upstash.
import { ok, deny } from "../lib/auth.js";
import * as kv from "../lib/kv.js";
const Q = {
  moda: ["streetwear Brasil", "moda cristã marca", "marca de roupa Instagram Reels"],
  negocios: ["Mercado Livre vendedores", "Black Friday 2026 e-commerce", "inteligência artificial vendas online"],
  infantil: ["YouTube infantil conteúdo", "animação infantil série"],
};
const LIM = { moda: 4, negocios: 4, infantil: 3 };
const dec = (s) => s.replace(/<!\[CDATA\[|\]\]>/g, "").replace(/&amp;/g, "&").replace(/&quot;/g, '"').replace(/&#39;/g, "'").replace(/&lt;/g, "<").replace(/&gt;/g, ">").trim();
async function feed(q) {
  const r = await fetch("https://news.google.com/rss/search?" + new URLSearchParams({ q: q + " when:3d", hl: "pt-BR", gl: "BR", ceid: "BR:pt-419" }));
  if (!r.ok) return [];
  const x = await r.text();
  return [...x.matchAll(/<item>([\s\S]*?)<\/item>/g)].slice(0, 3).map(([, it]) => {
    const g = (t) => dec((it.match(new RegExp(`<${t}[^>]*>([\\s\\S]*?)</${t}>`)) || [])[1] || "");
    const fonte = g("source"); let titulo = g("title");
    if (fonte && titulo.endsWith(" - " + fonte)) titulo = titulo.slice(0, -(fonte.length + 3));
    return { titulo, url: g("link"), fonte, resumo: new Date(g("pubDate")).toLocaleDateString("pt-BR", { day: "2-digit", month: "2-digit" }) + " · busca: " + q };
  });
}
export async function GET(req) {
  if (!ok(req)) return deny();
  const hoje = new Date().toLocaleDateString("pt-BR", { timeZone: "America/Sao_Paulo" });
  const ia = kv.ready() ? await kv.get("nexus:briefing_ia").catch(() => null) : null;
  if (ia?.data === hoje) return Response.json({ ...ia, fonte: "Briefing do Nexus (IA)" });
  if (kv.ready()) { const c = await kv.get("nexus:briefing").catch(() => null); if (c?.data === hoje) return Response.json(c); }
  const out = { data: hoje, insights: [], alertas: [], fonte: "Google Notícias" };
  for (const [k, qs] of Object.entries(Q)) {
    const seen = new Set(), list = [];
    for (const items of await Promise.all(qs.map(feed))) for (const it of items) if (it.titulo && !seen.has(it.titulo)) { seen.add(it.titulo); list.push(it); }
    out[k] = list.slice(0, LIM[k]);
  }
  if (kv.ready()) await kv.set("nexus:briefing", out).catch(() => {});
  return Response.json(out);
}
