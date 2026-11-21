# Testes funcionais — ClassEval

## Escopo e versão
Foram avaliadas as 90 respostas das 30 tarefas selecionadas.
Repositório https://github.com/gscamposz/avaliacao-codigo-llms
Commit f4c7ecd69986cc6d987611e253ef4d05be30b0bc
Ambiente Python 3.12.14 em Linux. Cada tarefa executada em processo separado, diretório temporário, timeout de 15 segundos e random.seed(0).
A suíte utiliza os testes oficiais presentes no ClassEval_data.json deste commit. As soluções de referência foram executadas para controle.
O repositório remoto não foi alterado.

## Resultados após extração e ajustes de formatação

| Modelo | Testes aprovados/executados | Falhas de asserção | Erros nos testes | Arquivos sem carregamento | Tarefas com suíte inteira aprovada |
|---|---:|---:|---:|---:|---:|
| chatgpt | 610/668 | 52 | 6 | 0 | 14/30 |
| gemini | 580/637 | 51 | 6 | 2 | 11/30 |
| qwen3_8b | 285/623 | 21 | 317 | 2 | 8/30 |

O conjunto contém 668 testes por modelo. Os denominadores menores indicam testes que não chegaram a executar devido a falha no carregamento, e não devem ser usados como ranking direto.
Códigos sem classe mas com funções foram submetidos à suíte e geraram os respectivos erros de atributos ou nomes.

## Preparação documentada
Respostas originais preservadas em originais/. Cada entrada em results.csv registra SHA-256 do texto, situação e transformação aplicada.
ChatGPT e Qwen3 tiveram extração dos blocos Python quando havia Markdown. Blocos de saída sem etiqueta Python foram descartados quando existiam blocos Python explícitos.
No Gemini foram removidas cercas e restaurados o recuo comum da classe e quebras do cabeçalho. As cópias executadas estão nas pastas por modelo. Nenhuma implementação de método foi corrigida.
Os resultados representam o código extraído/normalizado, e não necessariamente o texto bruto pronto para execução. Problemas de transferência e formatação não podem ser atribuídos com certeza ao modelo apenas pelos TXT recebidos.

## Pendências de carregamento
- Gemini ClassEval_5 — cabeçalho concatenado com import e construtor escrito como init. Não foi renomeado para __init__, pois isso alteraria a implementação. Conferir resposta na conversa original.
- Gemini ClassEval_71 — indentação irregular em vários níveis. A normalização comum não resolve. Conferir ou restaurar apenas a formatação da resposta original e executar novamente.
- Qwen3 ClassEval_42 — resposta parcial com trechos e exemplos sem classe completa, erro de sintaxe ao carregar o código extraído.
- Qwen3 ClassEval_58 — trecho que utiliza self no nível do módulo, gerando NameError ao carregar.

Os dois casos do Gemini precisam de confirmação de fidelidade à resposta original para encerrar completamente a avaliação funcional dessas tarefas.

## Controle do benchmark
A solução de referência passou em 667/668 testes com seed 0. A exceção é CalendarUtil, test_get_upcoming_events_5, que falha também na referência e depende de datas. A falha deve ser interpretada com ressalva e não como evidência exclusiva de defeito no modelo.
Uma primeira execução sem semente fixa também apresentou uma falha de MinesweeperGame na referência. A execução final usa seed 0 para todos os modelos. Jogos aleatórios podem produzir outros resultados com outras sementes.
O campo test_classes de Words2Numbers contém espaço extra em um nome. O carregador remove espaços nas extremidades dos nomes, sem alterar os corpos ou asserções dos testes.
As tarefas com referência aprovada fornecem uma verificação do carregador, mas testes oficiais ainda podem conter ambiguidades.
O script antigo rodar_teste.py do repositório não foi alterado.

## Arquivos
- results.csv e results.json — resultados individuais das 90 respostas e das 30 soluções de referência.
- pastas de modelos — cópias executadas e log detalhado por tarefa.
- baseline/ — controle com soluções de referência.
- originais/ — respostas originais usadas.
- evaluate.py — procedimento reproduzível. Defina CLASSEVAL_REPO para a pasta do repositório e execute com Python. As saídas são escritas na pasta do script.

## Próxima etapa
A análise de métricas estáticas não foi iniciada. Depende da autorização do usuário.
