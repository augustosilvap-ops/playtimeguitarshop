// Token assinado com HMAC (NEXUS_SECRET), válido por 30 dias.
import { createHmac, timingSafeEqual } from "node:crypto";
const secret = () => process.env.NEXUS_SECRET || "";
const sign = (s) => createHmac("sha256", secret()).update(s).digest("base64url");
export const issue = () => { const exp = String(Date.now() + 30 * 864e5); return `${exp}.${sign(exp)}`; };
export function ok(req) {
  if (!secret()) return false;
  const [exp, sig] = (req.headers.get("authorization") || "").replace(/^Bearer /, "").split(".");
  if (!exp || !sig || Number(exp) < Date.now()) return false;
  const a = Buffer.from(sig), b = Buffer.from(sign(exp));
  return a.length === b.length && timingSafeEqual(a, b);
}
export const deny = () => Response.json({ error: "login" }, { status: 401 });
