// Tarefas, aprovações e briefing (Netlify Blobs, loja "nexus").
import { getStore } from "@netlify/blobs";
import { ok, deny } from "../lib/auth.mjs";
const KEYS = new Set(["estado/tarefas", "aprovacoes", "briefing/hoje"]);
export default async (req) => {
  if (!ok(req)) return deny();
  const u = new URL(req.url), k = u.searchParams.get("k"), id = u.searchParams.get("id");
  if (!KEYS.has(k)) return Response.json({ error: "chave inválida" }, { status: 400 });
  const store = getStore({ name: "nexus", consistency: "strong" });
  if (req.method === "GET") return Response.json((await store.get(k, { type: "json" })) ?? null);
  if (req.method === "PUT") {
    const body = await req.json();
    if (k === "aprovacoes" && id) {
      const cur = (await store.get(k, { type: "json" })) ?? {};
      cur[id] = body; await store.setJSON(k, cur);
    } else await store.setJSON(k, body);
    return Response.json({ ok: true });
  }
  return new Response("Method not allowed", { status: 405 });
};
export const config = { path: "/api/state" };
