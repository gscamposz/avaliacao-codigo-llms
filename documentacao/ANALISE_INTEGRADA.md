# Análise integrada — resultados funcionais e estáticos

Revisão 2 baseada no snapshot de entradas d997a313306b52b6c03a8c7ee48cbb8afa8da41c.
Este documento consolida a análise descritiva. O relatório acadêmico e o roteiro da apresentação foram preparados na etapa final autorizada pelo autor e estão em documentacao/.

## Amostra e coleta

Foram selecionadas 30 tarefas do ClassEval e coletada uma resposta por tarefa em cada modelo, totalizando 90 respostas.
ChatGPT e Gemini foram acessados pelo navegador. Qwen3 8B foi executado localmente pelo Ollama com tag qwen3:8b, conforme confirmado pelo autor e pelos registros locais.
O autor informou GPT-6 para o ChatGPT e o período de coleta de 9 a 21 de novembro de 2026. Não há snapshot técnico independente do ChatGPT nem variante específica do Gemini. Datas individuais das conversas não foram preservadas. Consulte COLETA_MODELOS.md.
O piloto Calculator/VendingMachine é separado desta amostra e não entra nos totais.

## Resultados funcionais

| Modelo | Aprovados/executados | Falhas | Erros nos testes | Não executados | Tarefas com suíte inteira aprovada |
|---|---:|---:|---:|---:|---:|
| ChatGPT | 610/668 | 52 | 6 | 0 | 14/30 |
| Gemini | 596/668 | 51 | 21 | 0 | 12/30 |
| Qwen3 8B | 285/623 | 21 | 317 | 45 | 8/30 |

Cada modelo tem 668 testes previstos. Cada teste tem peso igual no total de testes, mas o número de testes varia entre tarefas. A contagem de tarefas inteiramente aprovadas dá peso igual a cada tarefa.
Os 45 testes não executados do Qwen3 pertencem a duas respostas que falham no carregamento. Elas permanecem no universo de 30 tarefas.

| Modelo | Aprovação entre testes executados | Aprovados sobre 668 previstos |
|---|---:|---:|
| ChatGPT | 91.32% | 91.32% |
| Gemini | 89.22% | 89.22% |
| Qwen3 8B | 45.75% | 42.66% |

O segundo percentual mantém a base de 668 e representa a parcela de aprovações demonstradas. Ele não converte automaticamente testes não executados em falhas de asserção.

## Métricas estáticas

| Modelo | Sintaxe após preparação | Contrato estrutural completo | NOM total | NPM total | CC média por método |
|---|---:|---:|---:|---:|---:|
| ChatGPT | 30/30 | 30/30 | 152 | 122 | 3.65 |
| Gemini | 30/30 | 29/30 | 153 | 123 | 3.72 |
| Qwen3 8B | 29/30 | 14/30 | 115 | 92 | 2.63 |

NOM inclui os métodos declarados diretamente nas classes e seus construtores. NPM conta os métodos cujos nomes não começam com underscore, segundo a convenção operacional adotada. CC é calculada com Radon 6.0.1.
O contrato estrutural verifica classe e assinaturas. A tabela detalhada informa o método ausente ou alterado. Essas verificações não analisam o comportamento das implementações.

ChatGPT teve todas as classes e assinaturas preservadas, mas só 14 tarefas passaram em toda a suíte.
Gemini teve 29 contratos completos e 12 tarefas totalmente aprovadas. A resposta da tarefa 5 declara init, confirmado pelo autor como presente no original, e não inicializa o objeto como o teste exige.
Qwen3 teve 14 contratos completos, várias classes renomeadas e respostas parciais. Sua CC média menor acompanha um conjunto com menos métodos, por isso a média global não demonstra superioridade.

## Contrato estrutural versus teste funcional

| Modelo | Contrato completo e suíte toda aprovada | Contrato completo com falha ou erro funcional |
|---|---:|---:|
| ChatGPT | 14 | 16 |
| Gemini | 12 | 17 |
| Qwen3 8B | 8 | 6 |

Esses cruzamentos foram calculados por tarefa em resultados_integrados.csv.
Ter todas as assinaturas não é suficiente para aprovar a suíte. Casos com métodos faltando ou nomes de classe diferentes podem falhar antes de testar a lógica interna.

## Comparação com tarefas pareadas

A comparação estática adicional em Metricas_Estaticas_ClassEval/tabelas/comparacao_pareada.csv usa as mesmas 13 tarefas com contrato completo nos três modelos.
As médias das CC médias por classe foram 2,74 para ChatGPT, 3,20 para Gemini e 2,67 para Qwen3 8B.
Esse recorte controla o conjunto de tarefas, mas é selecionado por completude do contrato e não representa a amostra inteira.
As diferenças são descritivas. Uma geração por tarefa não sustenta inferências gerais de superioridade dos produtos.

## Revisão de formatação e confirmação do original

As respostas TXT permanecem preservadas. As cópias executáveis recebem remoção de cercas e recuperação do recuo conforme o manifesto.
Para as tarefas 5 e 71 do Gemini, foram comparados todos os caracteres não brancos após remover cercas. A recuperação preservou essa sequência de caracteres.
A tarefa 71 passou nos 16 testes. A tarefa 5 teve 15 erros de instanciação. O usuário confirmou def init(self, text) na conversa original, encerrando a dúvida sobre possível perda de underscores nesse nome.
Outras perdas de formatação na exportação não foram atribuídas automaticamente ao modelo.

## Controle do benchmark e interpretação

Foram executadas as 30 soluções de referência. O controle passou em 667 de 668 testes, com uma falha de calendário dependente de datas.
Na tarefa CalendarUtil, os resultados completos desta execução foram

- Referência ClassEval — 28/29 testes aprovados, 1 falhas e 0 erros.
- ChatGPT — 24/29 testes aprovados, 5 falhas e 0 erros.
- Gemini — 19/29 testes aprovados, 10 falhas e 0 erros.
- Qwen3 8B — 0/29 testes aprovados, 0 falhas e 29 erros.

A falha que existe também na referência deve ser destacada na discussão. Os números oficiais foram preservados, sem corrigir as asserções para favorecer um modelo.
Há descrição inconsistente no exemplo de apply_operator do piloto, que não integra estas 30 tarefas.
Jogos aleatórios foram executados com random.seed(0), e outra semente pode alterar resultados. A execução utilizou Python/Linux, enquanto a coleta do Ollama ocorreu no Windows.

## Limitações a levar para o trabalho final

- Seleção intencional de 30 tarefas e uma geração por tarefa.
- Possível exposição dos modelos ao benchmark público durante treinamento não investigada.
- Identificação GPT-6 declarada pelo autor, sem snapshot técnico; Gemini sem variante registrada.
- Formatação dos arquivos exportados pode diferir da resposta visível no navegador.
- Cobertura de testes e ambiguidades do benchmark limitam a interpretação de aprovações.
- Estruturas predefinidas das tarefas influenciam NOM e NPM.
- Métodos incompletos, classes renomeadas e falhas de carregamento alteram os conjuntos usados nas médias.
- As configurações efetivas completas do Ollama não estão contidas nos JSON de resposta.
- Retomadas após timeout não correspondem a novas amostras independentes no desenho atual.

## Reprodução e arquivos

Execute na raiz do repositório

    python Testes_Funcionais_ClassEval/evaluate.py
    python Metricas_Estaticas_ClassEval/atualizar_entradas.py
    python Metricas_Estaticas_ClassEval/calcular_metricas.py
    python Metricas_Estaticas_ClassEval/gerar_relatorio.py
    python documentacao/gerar_analise_integrada.py

O cálculo estático exige as dependências em Metricas_Estaticas_ClassEval/requirements.txt, e o gráfico usa requisitos_figura.txt.
Os scripts validam hashes e totais antes de gerar as tabelas. Os resultados funcionais incluem baseline, enquanto o resumo integrado contém só os três modelos.
Para conferir a revisão funcional, consulte resultados/gemini/preparados e Testes_Funcionais_ClassEval/gemini.
Os arquivos CHECKSUMS.json são regenerados após alterações nos pacotes.

## Referências metodológicas

- ClassEval — https://github.com/FudanSELab/ClassEval
- Radon — https://radon.readthedocs.io/en/latest/intro.html
- API Radon — https://radon.readthedocs.io/en/latest/api.html
- Python AST — https://docs.python.org/3/library/ast.html
- PEP 8 — https://peps.python.org/pep-0008/

## Documentação final

O texto acadêmico, as justificativas, o roteiro de 10 minutos, o README e o checklist foram preparados. O autor ainda deve revisar os materiais, ensaiar e entregar ao professor.
Etapa final autorizada pelo autor. Nenhuma resposta original foi corrigida funcionalmente nesta finalização.
