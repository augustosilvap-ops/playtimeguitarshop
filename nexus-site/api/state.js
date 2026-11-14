// Tarefas, aprovações e briefing (Upstash Redis).
import { ok, deny } from "../lib/auth.js";
import * as kv from "../lib/kv.js";
const KEYS = new Set(["estado/tarefas", "aprovacoes", "briefing/hoje"]);
const pre = (req) => {
  if (!ok(req)) return deny();
  if (!kv.ready()) return Response.json({ error: "Armazenamento não configurado" }, { status: 503 });
  const k = new URL(req.url).searchParams.get("k");
  if (!KEYS.has(k)) return Response.json({ error: "chave inválida" }, { status: 400 });
  return null;
};
export async function GET(req) {
  const e = pre(req); if (e) return e;
  return Response.json(await kv.get("nexus:" + new URL(req.url).searchParams.get("k")));
}
export async function PUT(req) {
  const e = pre(req); if (e) return e;
  const u = new URL(req.url), k = "nexus:" + u.searchParams.get("k"), id = u.searchParams.get("id"), body = await req.json();
  if (u.searchParams.get("k") === "aprovacoes" && id) { const cur = (await kv.get(k)) ?? {}; cur[id] = body; await kv.set(k, cur); }
  else await kv.set(k, body);
  return Response.json({ ok: true });
}
