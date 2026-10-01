# Central de Aprovação V7

PWA gratuita preparada para GitHub Pages.

## Novidade da V7
Login e sincronização opcional entre celular e computador usando Supabase.

### Continua funcionando offline/local
A Central não depende do Supabase para abrir, estudar ou registrar dados. Sem login, usa o armazenamento do navegador.

### Com login
- criar conta por e-mail e senha;
- enviar dados para a nuvem;
- baixar dados da nuvem;
- sincronização automática após alterações;
- comparação entre versão local e versão em nuvem;
- RLS no banco para cada usuário acessar somente os próprios dados.

## Arquivos novos
- `config.js` — Project URL e anon/public key (opcionais).
- `supabase-setup.sql` — cria tabela e políticas RLS.
- `CONFIGURAR-SUPABASE.md` — guia passo a passo.

## Segurança
Nunca use `service_role` em código de navegador. Use somente a chave anon/public e mantenha RLS habilitado.

## Estrutura de estudos
Permanece igual à V6:
Curso → Matéria → Módulo → Aula/Material → Questões → Revisão → Simulado.
