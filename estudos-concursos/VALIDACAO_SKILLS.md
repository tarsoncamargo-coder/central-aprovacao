# Validação das skills e automação — 02/11/2026

## Descoberta real no Codex

Executado Codex CLI 0.163.0, app-server via stdio, método skills/list, em uma cópia local dos arquivos desta branch. Resultado: 13 skills do repositório habilitadas, zero erros de leitura. A consulta não chama um modelo nem exige uma chave de API. A descoberta foi executada antes e repetida depois da inclusão de agents/openai.yaml, com o mesmo resultado.

Cada uma das 13 skills possui agents/openai.yaml com allow_implicit_invocation: true, nome de apresentação e prompt padrão. A seleção implícita é permitida e orientada pelo pedido e pela descrição; não significa executar todas as skills a cada mensagem. As instruções locais de [AGENTS.md](AGENTS.md) orientam a seleção no diretório de estudos. A documentação oficial consultada foi https://developers.openai.com/codex/skills, em 02/11/2026.

## Testes funcionais controlados

Três agentes independentes leram os SKILL.md e executaram os cenários abaixo. Os dados de concurso e respostas do candidato usados nos testes são sintéticos ou fornecidos para o teste. Não representam provas oficiais nem progresso real do usuário.

| Skill | Cenário e resultado observado | Resultado |
|---|---|---|
| professor-de-concursos | Aula de interpretação com três objetivos, dois exemplos, três perguntas; resposta simulada confundiu avaliação com encerramento; correção explicou a extrapolação e encerrou com síntese de cinco linhas. | PASS |
| simulados-e-bancas | Três itens autorais; gabarito em etapa posterior às respostas simuladas B/B/A; correção B/C/A: 2 acertos, 1 erro, 0 brancos, 66,7%; amostra pequena sinalizada. | PASS |
| revisao-e-memorizacao | Três flashcards atômicos, recuperação ativa e revisões D+1/3/7/14/30 adaptáveis aos erros; nenhuma alegação de progresso real. | PASS |
| diagnostico-de-desempenho | Português 6/10 e 8/10: 14/20=70%; Matemática 4/10 e 5/10: 9/20=45%; total 23/40=57,5%; erros/brancos e causas não inventados; plano de sete dias. | PASS |
| planejador-inteligente | Grade de sete dias, seis sessões de 120 minutos, pausas, correção e revisão; 720 minutos totais; alternativa para dia perdido sem dobrar carga. | PASS |
| analista-de-editais | Edital sintético: 10 itens de Português peso2 e 10 de Matemática peso1; 30 pontos; remuneração e retificações ausentes sinalizadas; referências às seções fornecidas. | PASS |
| legislacao-atualizada | Diploma e artigo não identificados; recusou afirmar vigência; entregou checklist e cinco questões autorais sobre verificação, sem inventar norma. | PASS |
| rastreador-provas-oficiais | Pedido sem órgão, cargo ou ano: solicitou identificadores, separou artefatos, não inventou PDFs nem alegou consulta; explicou limites de repositório de terceiros. | PASS |
| auditoria-gabaritos-provas | Fixture A preliminar 1B/2C/3A e final 1B/2anulada/3D: identificou anulação e retificação; versão B ausente impediu pareamento e cálculo real. | PASS |
| engenharia-reversa-vunesp | Alfa A com três itens e B permutada: um conjunto de três, não seis; rejeitou fixture como evidência Vunesp; não inventou frequência histórica. | PASS |
| matriz-cobranca-edital | PT01/PT02/MAT01: 1/3 cada na fixture; PT03 não examinado permaneceu sem frequência, não zero; peso oficial separado de prioridade pedagógica. | PASS |
| laboratorio-distratores | Alguns → todos identificado como generalização indevida; treino autoral sem respostas antecipadas; item anulado sem motivo não recebeu justificativa inventada. | PASS |
| plano-adaptativo-pos-prova | Fixture PT02 2/10, MAT01 6/10, PT01 8/10: priorização provisória, seis dias de 120min, redação e revisão; metas explícitas e preservação de histórico. | PASS |

## Verificações reproduzíveis

Na raiz do repositório:

```sh
python3 -m pip install -r estudos-concursos/requirements-validacao.txt
python3 estudos-concursos/scripts/validar_radar.py
python3 -m unittest discover -s estudos-concursos/tests -v
python3 estudos-concursos/scripts/verificar_descoberta_codex.py
```

O último comando exige Codex CLI instalado; os demais exigem Python 3.12 e a dependência declarada. Resultado local: validador OK para 13 skills e 22 prompts, 16/16 testes de regressão aprovados e descoberta real com ok=true, total=13, errors=[]. O workflow radar-skills executa automaticamente validação e regressões em alterações relevantes. A checagem de descoberta real é local e não é confundida com o validador estrutural do CI.

## Alcance

Os 13 testes controlados e a descoberta local foram executados. Eles não certificam todas as saídas futuras de um modelo. Consulta de norma real, download de provas, correspondência entre versões e acesso a fontes oficiais dependem dos documentos e da conectividade de cada tarefa. Registrar ausência de evidência é o comportamento correto, não uma pendência de instalação da skill. A presença nesta branch não instala skills em outras conversas ou ambientes que não carreguem o repositório.
