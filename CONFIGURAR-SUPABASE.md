# Configurar login e sincronização — Central de Aprovação V7

A V7 funciona normalmente sem Supabase. O Supabase só é necessário para sincronizar celular e computador.

## 1. Criar projeto
1. Entre em https://supabase.com
2. Crie uma conta gratuita.
3. Clique em **New project**.
4. Escolha um nome, por exemplo `central-aprovacao`.
5. Defina uma senha do banco e guarde-a.
6. Aguarde o projeto ficar pronto.

## 2. Criar a tabela
1. No menu do projeto, abra **SQL Editor**.
2. Clique em **New query**.
3. Copie todo o conteúdo do arquivo `supabase-setup.sql`.
4. Cole no editor.
5. Clique em **Run**.

## 3. Pegar Project URL e anon/public key
1. No Supabase, abra **Project Settings / API** (a nomenclatura pode variar).
2. Copie a **Project URL**.
3. Copie a chave **anon/public**.
4. NUNCA use a chave `service_role` no navegador.

## 4. Colocar na Central
Você tem duas opções.

### Opção A — configurar dentro da própria Central
1. Abra a Central.
2. Vá em **☁️ Conta & Sync**.
3. Cole Project URL e anon/public key.
4. Clique em **Salvar configuração**.

Essa opção salva a configuração somente no aparelho atual.

### Opção B — configurar no GitHub para todos os seus aparelhos
1. Edite o arquivo `config.js`.
2. Preencha:
```js
window.CENTRAL_SUPABASE = {
  url: "https://SEU-PROJETO.supabase.co",
  anonKey: "SUA_CHAVE_ANON_PUBLIC"
};
```
3. Commit/push no GitHub.
4. Aguarde o GitHub Pages atualizar.

A chave anon/public pode ser exposta no frontend quando RLS está corretamente habilitado. A segurança dos dados depende das políticas RLS criadas pelo SQL.

## 5. Criar sua conta
1. Na Central, abra **☁️ Conta & Sync**.
2. Informe seu e-mail e uma senha.
3. Clique em **Criar conta**.
4. Se o Supabase exigir confirmação de e-mail, confirme.
5. Depois faça login.

## 6. Como a sincronização funciona
- Sem login: salva no `localStorage`.
- Com login: mudanças são enviadas automaticamente após alguns segundos.
- Ao entrar em outro aparelho, a Central compara a data local e a data da nuvem.
- Você também tem botões **Enviar para nuvem** e **Baixar da nuvem**.
- O botão **Exportar** continua sendo recomendado como backup.
