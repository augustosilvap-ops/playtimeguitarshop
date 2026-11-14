// Pedidos da RUAH. Credenciais (variáveis da Vercel):
//  - SHOPIFY_STORE (ex.: qxsiyw-54.myshopify.com)
//  - SHOPIFY_CLIENT_ID + SHOPIFY_CLIENT_SECRET (app do novo painel de desenvolvedor; token pedido pelo servidor, vale ~24h)
//  - ou SHOPIFY_TOKEN (token fixo de app antigo)
// Escopo necessário: read_orders. Nomes de clientes não são retornados.
import { ok, deny } from "../lib/auth.js";
const Q = `{ ordersCount { count } orders(first: 50, sortKey: CREATED_AT, reverse: true) { nodes {
  name createdAt displayFinancialStatus displayFulfillmentStatus totalPriceSet { shopMoney { amount } } } } }`;
let cached = { token: null, exp: 0 };
async function accessToken(store) {
  const fixed = process.env.SHOPIFY_TOKEN;
  if (fixed) return fixed;
  const id = process.env.SHOPIFY_CLIENT_ID, secret = process.env.SHOPIFY_CLIENT_SECRET;
  if (!id || !secret) return null;
  if (cached.token && cached.exp > Date.now() + 60e3) return cached.token;
  const r = await fetch(`https://${store}/admin/oauth/access_token`, {
    method: "POST", headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({ grant_type: "client_credentials", client_id: id, client_secret: secret }),
  });
  const j = await r.json().catch(() => null);
  if (!r.ok || !j?.access_token) throw new Error(`token ${r.status}: ${JSON.stringify(j)?.slice(0, 200)}`);
  cached = { token: j.access_token, exp: Date.now() + (Number(j.expires_in) || 3600) * 1000 };
  return cached.token;
}
export async function GET(req) {
  if (!ok(req)) return deny();
  const store = process.env.SHOPIFY_STORE;
  let token;
  try { token = store && (await accessToken(store)); }
  catch (e) { return Response.json({ error: "Falha ao autenticar na Shopify", detail: String(e.message) }, { status: 502 }); }
  if (!token) return Response.json({ error: "Shopify não configurada" }, { status: 503 });
  const r = await fetch(`https://${store}/admin/api/2026-07/graphql.json`, {
    method: "POST", headers: { "Content-Type": "application/json", "X-Shopify-Access-Token": token }, body: JSON.stringify({ query: Q }) });
  const j = await r.json().catch(() => null);
  if (!r.ok || !j?.data) return Response.json({ error: "Falha na Shopify", detail: j?.errors ?? r.status }, { status: 502 });
  const orders = j.data.orders.nodes.map((o) => ({ name: o.name, createdAt: o.createdAt, totalPrice: o.totalPriceSet.shopMoney.amount,
    financialStatus: o.displayFinancialStatus, fulfillmentStatus: o.displayFulfillmentStatus }));
  return Response.json({ orders, totalCount: j.data.ordersCount?.count ?? orders.length });
}
