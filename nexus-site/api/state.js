// Tarefas, aprovações e briefing (Upstash Redis).
import { ok, deny } from "../lib/auth.js";
import * as kv from "../lib/kv.js";
const SEED = {"estado/tarefas": {"ruah": [{"texto": "Enviar os pedidos pagos que aguardam envio", "feito": false}, {"texto": "Comparar métricas da home antes/depois do tema", "feito": false}, {"texto": "Prévia do combo \"Leve 2 por R$ 269,90\" (17/11)", "feito": false}, {"texto": "Revisar menções a \"25/11\" no fluxo Founders", "feito": false}, {"texto": "Falar com especialista sobre o registro no INPI", "feito": false}], "aug": [{"texto": "Testar os 6 fluxos do Manychat", "feito": false}, {"texto": "Aprovar e publicar os posts 01–06 (16 e 17/11)", "feito": false}, {"texto": "Produzir os posts 07–21", "feito": false}], "ml": [{"texto": "Exportar planilhas de vendas e anúncios do Mercado Livre", "feito": false}, {"texto": "Ativar o programa Decola", "feito": false}, {"texto": "Confirmar se a B2Drop sincroniza preço e estoque", "feito": false}, {"texto": "Escolher os 20–30 anúncios prioritários", "feito": false}], "pq": [{"texto": "Revisar o EP01 \"Bem-vindos ao Reino\"", "feito": false}, {"texto": "Fechar a ficha visual dos 4 personagens", "feito": false}, {"texto": "Montar a grade de Shorts da semana", "feito": false}, {"texto": "Enviar os arquivos do Drive para o projeto", "feito": false}], "s360": [{"texto": "Confirmar VPS regularizada e n8n no ar", "feito": false}, {"texto": "Rotacionar chaves (Asaas, Anthropic, Evolution) e mover para credenciais do n8n", "feito": false}, {"texto": "Inbound: ignorar sessões em modo monitoramento", "feito": false}, {"texto": "Reconectar números da Nicolle e validar o maturador", "feito": false}, {"texto": "Webhook da Evolution nas instâncias novas", "feito": false}, {"texto": "Subir CRM no Netlify e hospedar a landing page v2", "feito": false}, {"texto": "Corrigir loop da Evolution e certificado do domínio", "feito": false}], "bro": [{"texto": "Enviar o contexto da Brothers Supply", "feito": false}, {"texto": "Definir canais e prioridades", "feito": false}]}};
const KEYS = new Set(["estado/tarefas", "aprovacoes", "briefing/hoje"]);
const pre = (req) => {
  if (!ok(req)) return deny();
  if (!kv.ready()) return Response.json({ error: "Armazenamento não configurado" }, { status: 503 });
  const k = new URL(req.url).searchParams.get("k");
  if (!KEYS.has(k)) return Response.json({ error: "chave inválida" }, { status: 400 });
  return null;
};
export async function GET(req) {
  const e = pre(req); if (e) return e;
  const k = new URL(req.url).searchParams.get("k");
  let v = await kv.get("nexus:" + k);
  if (v == null && SEED[k]) { v = SEED[k]; await kv.set("nexus:" + k, v); }
  return Response.json(v);
}
export async function PUT(req) {
  const e = pre(req); if (e) return e;
  const u = new URL(req.url), k = "nexus:" + u.searchParams.get("k"), id = u.searchParams.get("id"), body = await req.json();
  if (u.searchParams.get("k") === "aprovacoes" && id) { const cur = (await kv.get(k)) ?? {}; cur[id] = body; await kv.set(k, cur); }
  else await kv.set(k, body);
  return Response.json({ ok: true });
}
