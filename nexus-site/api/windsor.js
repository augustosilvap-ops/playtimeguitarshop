// Meta Ads e Instagram via API da Windsor. Precisa de WINDSOR_API_KEY.
// As contas do Instagram são separadas pelo nome (a API REST usa IDs diferentes dos do conector).
import { ok, deny } from "../lib/auth.js";
const ACC = { "17841452465952355": "ruahwear_", "17841407424879500": "augustosilva.p" };
async function pull(c, key, fields, preset) {
  const q = new URLSearchParams({ api_key: key, fields: fields.join(",") });
  if (preset) q.set("date_preset", preset);
  const r = await fetch(`https://connectors.windsor.ai/${c}?${q}`);
  const j = await r.json().catch(() => null);
  if (!r.ok || !j || !Array.isArray(j.data)) throw new Error(`windsor ${r.status}`);
  return j.data;
}
export async function GET(req) {
  if (!ok(req)) return deny();
  const key = process.env.WINDSOR_API_KEY;
  if (!key) return Response.json({ error: "Windsor não configurada" }, { status: 503 });
  const u = new URL(req.url), c = u.searchParams.get("c");
  if (!["facebook", "instagram"].includes(c)) return Response.json({ error: "conector inválido" }, { status: 400 });
  const fields = (u.searchParams.get("fields") || "").split(",").filter(Boolean);
  const preset = u.searchParams.get("preset") || "";
  const name = ACC[u.searchParams.get("acc")] || null;
  const want = name && !fields.includes("account_name") ? [...fields, "account_name"] : fields;
  const presets = preset ? [preset, preset.replace(/T$/, "")].filter((v, i, a) => a.indexOf(v) === i) : [""];
  let data = null, err = null;
  for (const p of presets) { try { data = await pull(c, key, want, p); break; } catch (e) { err = e; } }
  if (!data) return Response.json({ error: "Falha na Windsor", detail: String(err?.message) }, { status: 502 });
  if (name) data = data.filter((r) => !r.account_name || r.account_name === name);
  return Response.json({ status: "done", data });
}
