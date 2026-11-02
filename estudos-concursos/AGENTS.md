# Operação automática do Radar de Estudos

Estas instruções se aplicam ao diretório estudos-concursos. As 13 skills ficam em ../.agents/skills e podem ser selecionadas implicitamente pelo Codex em qualquer diretório deste repositório. Todas permitem invocação implícita em agents/openai.yaml.

## Seleção pelo pedido

Em pedidos de estudo neste diretório, escolha as skills pelo objetivo e leia os respectivos SKILL.md antes de responder. Não exija que o candidato escreva o nome da skill nem copie um prompt. Consulte [catalogo.json](catalogo.json) para a correspondência de cada um dos 22 prompts com suas skills; os arquivos PROMPTS são exemplos reutilizáveis, não tarefas a executar em lote.

| Pedido | Skill |
|---|---|
| Edital, requisitos ou pesos | analista-de-editais |
| Cronograma ou ciclo | planejador-inteligente |
| Aula ou explicação | professor-de-concursos |
| Simulado ou bateria de questões | simulados-e-bancas |
| Flashcards ou revisão | revisao-e-memorizacao |
| Resultados ou caderno de erros | diagnostico-de-desempenho |
| Lei, vigência ou artigo | legislacao-atualizada |
| Localizar provas e gabaritos | rastreador-provas-oficiais |
| Versões, anulações ou retificações de gabarito | auditoria-gabaritos-provas |
| Padrões Vunesp | engenharia-reversa-vunesp |
| Cruzar questões com tópicos do edital | matriz-cobranca-edital |
| Alternativas incorretas e pegadinhas | laboratorio-distratores |
| Replanejar após prova/simulado com 12h semanais | plano-adaptativo-pos-prova |

Combine skills quando necessário. Para outra banca, use as skills gerais e provas identificadas; não apresente engenharia-reversa-vunesp como análise específica de outra organizadora. Declare hipóteses quando faltar banca, edital ou rotina. Quando faltarem documentos essenciais, produza a parte possível e identifique os dados necessários. Não invente provas, legislação vigente, progresso ou fontes. Corrija respostas após o treino, preservando o raciocínio do candidato e o histórico fornecido.

## Manutenção

Ao alterar skills ou prompts, atualize catalogo.json e execute:

```sh
python3 -m pip install -r estudos-concursos/requirements-validacao.txt
python3 estudos-concursos/scripts/validar_radar.py
python3 -m unittest discover -s estudos-concursos/tests -v
```

Execute esses comandos a partir da raiz do repositório. O workflow radar-skills valida o contrato a cada alteração relevante. Isso não substitui testes pedagógicos nem consulta de fontes oficiais.

Preserve o isolamento: não modificar o AGENTS.md principal, NinjaScript, robôs, Laranjinha, Larry, Fusion ou Risk Desk. Não fazer merge na main sem autorização explícita.
