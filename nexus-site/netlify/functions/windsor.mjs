// Meta Ads e Instagram via API da Windsor. Precisa de WINDSOR_API_KEY.
import { ok, deny } from "../lib/auth.mjs";
const ALLOWED = new Set(["facebook", "instagram"]);
export default async (req) => {
  if (!ok(req)) return deny();
  const key = Netlify.env.get("WINDSOR_API_KEY");
  if (!key) return Response.json({ error: "Windsor não configurada" }, { status: 503 });
  const u = new URL(req.url), c = u.searchParams.get("c");
  if (!ALLOWED.has(c)) return Response.json({ error: "conector inválido" }, { status: 400 });
  const q = new URLSearchParams({ api_key: key, fields: u.searchParams.get("fields") || "" });
  const preset = u.searchParams.get("preset"); if (preset) q.set("date_preset", preset);
  const acc = u.searchParams.get("acc"); if (acc) q.set("select_accounts", `${c}__${acc}`);
  const r = await fetch(`https://connectors.windsor.ai/${c}?${q}`);
  const j = await r.json().catch(() => null);
  if (!r.ok || !j) return Response.json({ error: "Falha na Windsor", detail: r.status }, { status: 502 });
  return Response.json({ status: "done", data: j.data ?? [] });
};
export const config = { path: "/api/windsor" };
