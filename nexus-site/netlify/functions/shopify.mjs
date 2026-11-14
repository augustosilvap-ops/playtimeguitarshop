// Pedidos da RUAH (Shopify Admin GraphQL). Precisa de SHOPIFY_STORE e SHOPIFY_TOKEN (escopo read_orders).
import { ok, deny } from "../lib/auth.mjs";
const Q = `{ ordersCount { count } orders(first: 50, sortKey: CREATED_AT, reverse: true) { nodes {
  name createdAt displayFinancialStatus displayFulfillmentStatus totalPriceSet { shopMoney { amount } } } } }`;
export default async (req) => {
  if (!ok(req)) return deny();
  const store = Netlify.env.get("SHOPIFY_STORE"), token = Netlify.env.get("SHOPIFY_TOKEN");
  if (!store || !token) return Response.json({ error: "Shopify não configurada" }, { status: 503 });
  const r = await fetch(`https://${store}/admin/api/2026-07/graphql.json`, {
    method: "POST", headers: { "Content-Type": "application/json", "X-Shopify-Access-Token": token },
    body: JSON.stringify({ query: Q }),
  });
  const j = await r.json().catch(() => null);
  if (!r.ok || !j?.data) return Response.json({ error: "Falha na Shopify", detail: j?.errors ?? r.status }, { status: 502 });
  const orders = j.data.orders.nodes.map((o) => ({
    name: o.name, createdAt: o.createdAt, totalPrice: o.totalPriceSet.shopMoney.amount,
    financialStatus: o.displayFinancialStatus, fulfillmentStatus: o.displayFulfillmentStatus,
  }));
  return Response.json({ orders, totalCount: j.data.ordersCount?.count ?? orders.length });
};
export const config = { path: "/api/shopify" };
