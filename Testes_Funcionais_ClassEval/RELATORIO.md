# Testes funcionais — revisão 2

Entradas versionadas no commit d997a313306b52b6c03a8c7ee48cbb8afa8da41c.
Nesta revisão foram reexecutadas as 90 respostas e as 30 soluções de referência.

## Procedimento

Execução em Python/Linux, com um processo e diretório temporário por tarefa, semente random 0 e timeout de 15 segundos por processo.
As asserções e os corpos dos testes oficiais em ClassEval_data.json foram preservados. O carregador retira espaços nas extremidades dos nomes em test_classes, por causa de um espaço extra nos metadados de Words2Numbers.
As respostas originais permanecem em resultados/ e originais/. As cópias executadas e logs estão nas pastas dos modelos deste pacote.

## Resultados

| Modelo | Aprovados/executados | Falhas | Erros nos testes | Testes não executados | Tarefas com suíte inteira aprovada |
|---|---:|---:|---:|---:|---:|
| ChatGPT | 610/668 | 52 | 6 | 0 | 14/30 |
| Gemini | 596/668 | 51 | 21 | 0 | 12/30 |
| Qwen3 8B | 285/623 | 21 | 317 | 45 | 8/30 |

Há 668 testes previstos por modelo. Para Qwen3, 45 deles não executaram porque as tarefas 42 e 58 falham ao carregar. Testes não executados não são apresentados como erros de asserção.
Os percentuais sobre testes executados são condicionais à execução. A tabela integrada também fornece aprovados sobre os 668 testes previstos para manter o denominador explícito.

## Atualização Gemini

ClassEval_71 passou nos 16 testes após recuperar o recuo.
ClassEval_5 passou a carregar, mas os 15 testes produziram TypeError ao criar AutomaticGuitarSimulator com um argumento.
O autor confirmou def init(self, text) na resposta original do Gemini. Não se inseriu __init__.
As duas cópias preservam todos os caracteres não brancos dos originais, após remover linhas de cercas Markdown.

## Controle e limitações

A solução de referência passou em 667 dos 668 testes. CalendarUtil.test_get_upcoming_events_5 falha também na referência e depende de datas históricas.
Em uma execução exploratória anterior sem semente fixa, ocorreu também uma falha de MinesweeperGame na referência. Os resultados publicados desta revisão usam seed 0.
Aprovação nos testes descreve a suíte e a execução, sem provar correção universal. O resultado é sensível à cobertura, a requisitos ambíguos e à aleatoriedade.
Os registros de ambiente, o hash do JSON oficial e o snapshot estão em ambiente.json.

## Reprodução

Na raiz do repositório, execute

    python Testes_Funcionais_ClassEval/evaluate.py

O script usa a raiz atual por padrão. CLASSEVAL_REPO permite escolher outra cópia do repositório.
Os arquivos de saída são gravados na pasta do script.
resultados/gemini/preparados contém as recuperações explícitas de formatação usadas para as tarefas 5 e 71.
Os logs suplementares em revisao_gemini pertencem à primeira verificação dessas cópias. As pastas gemini/ e results.json contêm a nova rodada completa.

## Integração

Consulte ../documentacao/ANALISE_INTEGRADA.md e os CSV/JSON associados.
Esta revisão atualiza os resultados funcionais e estáticos. A finalização do texto acadêmico e a apresentação aguardam a autorização do autor.
