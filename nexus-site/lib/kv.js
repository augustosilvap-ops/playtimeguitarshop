// Armazenamento: Upstash Redis (integração gratuita da Vercel), via REST.
const URL_ = () => process.env.KV_REST_API_URL || process.env.UPSTASH_REDIS_REST_URL;
const TOKEN = () => process.env.KV_REST_API_TOKEN || process.env.UPSTASH_REDIS_REST_TOKEN;
export const ready = () => !!(URL_() && TOKEN());
export async function get(key) {
  const r = await fetch(`${URL_()}/get/${encodeURIComponent(key)}`, { headers: { Authorization: `Bearer ${TOKEN()}` } });
  const j = await r.json(); return j.result ? JSON.parse(j.result) : null;
}
export async function set(key, value) {
  const r = await fetch(`${URL_()}/set/${encodeURIComponent(key)}`, { method: "POST", headers: { Authorization: `Bearer ${TOKEN()}` }, body: JSON.stringify(value) });
  if (!r.ok) throw new Error("kv " + r.status);
}
