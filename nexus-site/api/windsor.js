// Meta Ads e Instagram via API da Windsor. Precisa de WINDSOR_API_KEY.
import { ok, deny } from "../lib/auth.js";
export async function GET(req) {
  if (!ok(req)) return deny();
  const key = process.env.WINDSOR_API_KEY;
  if (!key) return Response.json({ error: "Windsor não configurada" }, { status: 503 });
  const u = new URL(req.url), c = u.searchParams.get("c");
  if (!["facebook", "instagram"].includes(c)) return Response.json({ error: "conector inválido" }, { status: 400 });
  const q = new URLSearchParams({ api_key: key, fields: u.searchParams.get("fields") || "" });
  const preset = u.searchParams.get("preset"); if (preset) q.set("date_preset", preset);
  const acc = u.searchParams.get("acc"); if (acc) q.set("select_accounts", `${c}__${acc}`);
  const r = await fetch(`https://connectors.windsor.ai/${c}?${q}`);
  const j = await r.json().catch(() => null);
  if (!r.ok || !j) return Response.json({ error: "Falha na Windsor", detail: r.status }, { status: 502 });
  return Response.json({ status: "done", data: j.data ?? [] });
}
