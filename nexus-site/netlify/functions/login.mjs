import { timingSafeEqual } from "node:crypto";
import { issue } from "../lib/auth.mjs";
export default async (req) => {
  if (req.method !== "POST") return new Response("Method not allowed", { status: 405 });
  const pass = Netlify.env.get("NEXUS_PASSWORD") || "";
  const { password = "" } = await req.json().catch(() => ({}));
  const a = Buffer.from(String(password)), b = Buffer.from(pass);
  if (!pass || a.length !== b.length || !timingSafeEqual(a, b)) {
    await new Promise((r) => setTimeout(r, 800));
    return Response.json({ error: "Senha incorreta" }, { status: 401 });
  }
  return Response.json({ token: issue() });
};
export const config = { path: "/api/login" };
