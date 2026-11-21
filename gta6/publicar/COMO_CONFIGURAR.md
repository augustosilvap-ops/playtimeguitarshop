# YouTube e TikTok automáticos · como configurar (uma vez só)

O GitHub publica sozinho, a cada 30 minutos, os vídeos da fila (`gta6/publicacao`) que chegaram no horário.
Custo zero. Nenhuma chave passa pelo chat: você cola direto no GitHub.

---

## Parte 1 · YouTube (≈ 15 min)

1. Acesse **console.cloud.google.com** com a conta Google dona do canal **Caos Insano BR** → **Novo projeto** → nome `Caos Insano`.
2. Menu **APIs e serviços → Biblioteca** → procure **YouTube Data API v3** → **Ativar**.
3. **Google Auth Platform → Branding / Tela de consentimento OAuth**: tipo **Externo**, nome `Caos Insano`, seu e-mail de suporte e de contato → salvar.
   - Em **Público-alvo**, clique em **Publicar app** (status "Em produção"). Se ficar em "Teste", a autorização expira a cada 7 dias.
4. **Clientes → Criar cliente** → tipo **Aplicativo da Web** → em **URIs de redirecionamento autorizados** coloque
   `https://developers.google.com/oauthplayground` → **Criar**. Copie o **ID do cliente** e a **Chave secreta** (guarde só para o passo 6).
5. Abra **developers.google.com/oauthplayground**:
   - engrenagem ⚙️ (canto direito) → marque **Use your own OAuth credentials** → cole o ID do cliente e a chave secreta;
   - no campo "Input your own scopes" digite `https://www.googleapis.com/auth/youtube.upload` → **Authorize APIs**;
   - entre com a conta e **escolha o canal Caos Insano BR** → aceite (pode aparecer "app não verificado" → Avançado → continuar);
   - clique em **Exchange authorization code for tokens** → copie o **Refresh token**.
6. No GitHub: repositório **playtimeguitarshop → Settings → Secrets and variables → Actions → New repository secret**. Crie 3:
   | Nome | Valor |
   |---|---|
   | `YT_CLIENT_ID` | ID do cliente |
   | `YT_CLIENT_SECRET` | Chave secreta |
   | `YT_REFRESH_TOKEN` | Refresh token |
7. Teste: aba **Actions → "Caos Insano · YouTube e TikTok" → Run workflow**. Depois me avise que eu confiro o resultado.

**Privado até a auditoria.** Projetos novos do Google só podem subir vídeo como **privado**. Enquanto isso, abra o YouTube Studio e troque para **Público** (1 toque).
Para liberar: formulário **"YouTube API Services – Audit and Quota Extension Form"** (gratuito; eu preencho o texto com você). Quando aprovarem:
**Settings → Secrets and variables → Actions → aba Variables → New variable** `YT_PRIVACIDADE` = `public`.

Limite grátis: ~6 envios por dia (cota de 10.000 unidades; cada envio usa 1.600).

---

## Parte 2 · TikTok (≈ 15 min + aprovação do TikTok)

1. **developers.tiktok.com** → entre com a conta do TikTok → **Manage apps → Connect an app** → nome `Caos Insano`.
2. Em **Products**, adicione **Login Kit** e **Content Posting API**. Em **Scopes**, marque `video.upload`.
3. Em **Login Kit → Redirect URI**, coloque `https://nexusautomatic.vercel.app/tiktok` → **Submit for review** (o TikTok revisa o app; o sandbox já funciona para a sua conta).
4. Copie **Client key** e **Client secret**. Abra no navegador (troque `SUA_CLIENT_KEY`):
   ```
   https://www.tiktok.com/v2/auth/authorize/?client_key=SUA_CLIENT_KEY&scope=user.info.basic,video.upload&response_type=code&redirect_uri=https%3A%2F%2Fnexusautomatic.vercel.app%2Ftiktok&state=caos
   ```
   Autorize. A página seguinte pode dar erro 404 — tudo bem: copie da barra de endereço o valor de `code=` (até antes do `&`).
5. No **terminal do seu computador** (Mac: app Terminal · Windows: PowerShell), rode trocando os 3 valores:
   ```
   curl -X POST https://open.tiktokapis.com/v2/oauth/token/ -H "Content-Type: application/x-www-form-urlencoded" -d "client_key=SUA_CLIENT_KEY&client_secret=SEU_CLIENT_SECRET&code=SEU_CODE&grant_type=authorization_code&redirect_uri=https://nexusautomatic.vercel.app/tiktok"
   ```
   Copie o valor de `"refresh_token"` da resposta (vale 1 ano).
6. No GitHub, crie mais 3 secrets: `TT_CLIENT_KEY`, `TT_CLIENT_SECRET`, `TT_REFRESH_TOKEN`.

**Rascunho até a aprovação.** Sem aprovação do TikTok, o vídeo chega na sua **caixa de entrada do TikTok como rascunho** — abre, confere a legenda (está no `PACOTE_UPLOAD.md`) e publica.

---

## Como funciona depois
- O agente 6 grava em cada pacote da fila: `publicar_em`, `arquivo`, `yt` (título, descrição, tags) e `tt` (legenda).
- O GitHub Actions (`.github/workflows/caos_publicar.yml`) roda às :07 e :37 de cada hora, envia o que venceu e guarda o resultado na branch `caos-status` (não mexe na `main`).
- Vídeo com mais de 6 h de atraso não é enviado (evita enxurrada). Se um envio falhar, ele **não** é repetido sozinho (evita duplicado) — eu vejo no status e te aviso.
