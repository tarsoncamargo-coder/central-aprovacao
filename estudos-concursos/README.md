# Radar de Estudos — Concursos

13 Agent Skills e 22 prompts para concursos brasileiros, com prioridade para nível médio, fontes oficiais gratuitas e prática com feedback.

## Comece aqui

- [10 prompts de estudo](PROMPTS_PRONTOS.md): planejamento, aulas, simulados, revisão, editais, legislação e diagnóstico.
- [12 prompts de engenharia reversa](PROMPTS_ENGENHARIA_REVERSA.md): provas anteriores, auditoria, Vunesp/TJSP, distratores e plano adaptativo.
- Substitua os campos entre colchetes antes de usar um prompt.
- Informe banca, cargo, edital, assunto e tempo disponível quando souber. Na ausência desses dados, peça uma versão-base com hipóteses declaradas.

## Catálogo das 13 skills

| Skill | Quando usar |
|---|---|
| [analista-de-editais](../.agents/skills/analista-de-editais/SKILL.md) | Extrair requisitos, datas, disciplinas e pesos de editais e retificações. |
| [auditoria-gabaritos-provas](../.agents/skills/auditoria-gabaritos-provas/SKILL.md) | Conferir versões, gabaritos definitivos, anulações e retificações. |
| [diagnostico-de-desempenho](../.agents/skills/diagnostico-de-desempenho/SKILL.md) | Analisar registros de questões e simulados e priorizar correções. |
| [engenharia-reversa-vunesp](../.agents/skills/engenharia-reversa-vunesp/SKILL.md) | Analisar padrões em questões conferidas e comparar com o edital. |
| [laboratorio-distratores](../.agents/skills/laboratorio-distratores/SKILL.md) | Entender alternativas incorretas e treinar erros típicos. |
| [legislacao-atualizada](../.agents/skills/legislacao-atualizada/SKILL.md) | Estudar normas com fontes oficiais e verificação de vigência. |
| [matriz-cobranca-edital](../.agents/skills/matriz-cobranca-edital/SKILL.md) | Relacionar questões verificadas aos tópicos do edital. |
| [planejador-inteligente](../.agents/skills/planejador-inteligente/SKILL.md) | Montar ciclos e planos de estudo conforme rotina e edital. |
| [plano-adaptativo-pos-prova](../.agents/skills/plano-adaptativo-pos-prova/SKILL.md) | Recalibrar 12 horas semanais com edital e desempenho real. |
| [professor-de-concursos](../.agents/skills/professor-de-concursos/SKILL.md) | Aprender com mini-aula, exemplos resolvidos e recuperação ativa. |
| [rastreador-provas-oficiais](../.agents/skills/rastreador-provas-oficiais/SKILL.md) | Localizar provas e gabaritos e registrar sua verificação. |
| [revisao-e-memorizacao](../.agents/skills/revisao-e-memorizacao/SKILL.md) | Criar flashcards, testes de lembrança e revisão espaçada. |
| [simulados-e-bancas](../.agents/skills/simulados-e-bancas/SKILL.md) | Resolver simulados autorais por assunto e estilo de banca. |

## Uso no Codex

1. Abra o repositório `central-aprovacao` na branch `feat/radar-de-estudos-skills`.
2. Inicie uma sessão no diretório do repositório para permitir a descoberta de `.agents/skills/<nome>/SKILL.md`.
3. Consulte o catálogo de skills da sessão. Se houver suporte à chamada por nome, use, por exemplo, `$professor-de-concursos`.
4. Se a skill não aparecer, solicite explicitamente a leitura do arquivo e a aplicação das instruções. A leitura manual permite usar o método, mas não comprova descoberta automática.

Exemplo que funciona por leitura explícita:

> Leia .agents/skills/professor-de-concursos/SKILL.md e siga suas instruções. Ensine interpretação de texto para concurso de nível médio, sem banca definida. Apresente dois exemplos resolvidos e três perguntas de treino, sem antecipar o gabarito. Depois das minhas respostas, analise meu raciocínio.

## Uso nesta conversa ou em outra conversa do ChatGPT

Os prompts podem ser copiados diretamente. Para aplicar integralmente uma skill, forneça o conteúdo do respectivo SKILL.md ou peça sua leitura no GitHub quando houver acesso ao repositório. Somente escrever "ative" não instala nem garante o carregamento automático da skill.

Exemplo com acesso ao GitHub:

> No repositório tarsoncamargo-coder/central-aprovacao, branch feat/radar-de-estudos-skills, leia .agents/skills/professor-de-concursos/SKILL.md e aplique suas instruções em uma aula de interpretação de texto para nível médio. Use exemplos autorais e aguarde minhas respostas antes de corrigir o treino.

Para começar a análise de provas:

> Na mesma branch, leia .agents/skills/rastreador-provas-oficiais/SKILL.md e aplique suas instruções. Localize provas e gabaritos de [BANCA], [ÓRGÃO], [CARGO], entre [ANO INICIAL] e [ANO FINAL]. Informe URLs, aplicação, versão e status de verificação.

## Sequência recomendada

- Estudo: analista-de-editais → planejador-inteligente → professor-de-concursos → simulados-e-bancas → diagnostico-de-desempenho → revisao-e-memorizacao.
- Provas anteriores: rastreador-provas-oficiais → auditoria-gabaritos-provas → engenharia-reversa-vunesp → matriz-cobranca-edital → laboratorio-distratores → plano-adaptativo-pos-prova.
- Use legislacao-atualizada quando o conteúdo exigir confronto com a norma vigente.

## Dados necessários e limites

- Editais: forneça o documento oficial e as retificações ou permita sua localização.
- Análise histórica: exige cadernos identificados, versões e gabaritos conferidos. Dados ausentes devem ser sinalizados; frequência observada não garante cobrança futura.
- Diagnóstico: forneça suas respostas ou registros. Nenhuma skill presume acesso ao seu histórico.
- Plano adaptativo: a base é 2 horas por dia, 6 dias por semana; declare sua disponibilidade se precisar de adaptação.
- Questões autorais devem ser identificadas como tais; não são questões oficiais.
- Legislação exige fonte e data de verificação; se não houver acesso, a vigência deve ser marcada como não confirmada.

## Estado de verificação

Em 02/11/2026, foram conferidos os 13 arquivos SKILL.md: todos apresentam metadados name e description, com nome correspondente à pasta. Os dois arquivos de prompts totalizam 22 entradas numeradas (10 + 12).

A skill professor-de-concursos foi demonstrada em uma aula de interpretação de texto. A correção interativa depende das respostas do candidato. As outras 12 skills ainda não passaram por testes completos de execução; a conferência estrutural não equivale a validação funcional. A descoberta automática depende do ambiente e deve ser confirmada na sessão do Codex.

## Isolamento

Esta branch no repositório central-aprovacao é experimental. Não modificar NinjaScript, robôs, Laranjinha, Larry, Fusion, Risk Desk ou o AGENTS.md principal. Não fazer merge na main sem aprovação.
