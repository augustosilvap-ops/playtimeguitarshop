import { timingSafeEqual } from "node:crypto";
import { issue } from "../lib/auth.js";
export async function POST(req) {
  const pass = process.env.NEXUS_PASSWORD || "";
  const { password = "" } = await req.json().catch(() => ({}));
  const a = Buffer.from(String(password)), b = Buffer.from(pass);
  if (!pass || a.length !== b.length || !timingSafeEqual(a, b)) {
    await new Promise((r) => setTimeout(r, 800));
    return Response.json({ error: "Senha incorreta" }, { status: 401 });
  }
  return Response.json({ token: issue() });
}
