# Roteiro da apresentação

Gustavo Silva Campos. Tempo planejado: 10 minutos. Limite total: 15 minutos, com margem de até cinco minutos para perguntas ou esclarecimentos. O slide de referências pode permanecer aberto durante as perguntas.

## Slide 1 — Avaliação de código Python gerado por modelos de linguagem

Tempo: 00:00 a 00:35 (35 segundos).

Boa noite. Este trabalho compara implementações de classes Python produzidas pelo ChatGPT, pelo Gemini e pelo Qwen3 8B local. A avaliação utiliza trinta tarefas do ClassEval e noventa respostas. O foco é verificar se essas classes atendem aos testes e preservam a estrutura solicitada. A coleta ocorreu entre nove e vinte e um de novembro de dois mil e vinte e seis. Vou apresentar o desenho do experimento, os resultados e os limites da comparação.

## Slide 2 — A pergunta do trabalho

Tempo: 00:35 a 01:20 (45 segundos).

A pergunta central é como os modelos diferem em correção funcional, preservação das assinaturas e complexidade. Uma resposta pode parecer organizada e ainda falhar ao compartilhar estado entre os métodos. Por isso, o estudo combina testes com análise estática. Avalio os artefatos efetivamente coletados, sem afirmar que uma única resposta caracteriza toda a capacidade de um modelo. O resultado deve ajudar a entender o que precisa ser conferido antes de utilizar esse código.

## Slide 3 — Trinta tarefas com comportamentos diferentes

Tempo: 01:20 a 02:10 (50 segundos).

Escolhi trinta tarefas organizadas em três grupos de dez. Utilitários trabalham transformações de dados, regras de negócio mantêm registros e jogos exigem transições de estado. Essa organização oferece diversidade dentro do volume viável para revisão. O ClassEval já fornece esqueletos e testes, o que favorece uma comparação comum. A seleção é intencional e não representa estatisticamente todo o benchmark. Calculator e VendingMachine foram usados apenas no piloto e ficaram fora das trinta tarefas principais. Fonte: Du et al., 2023, https://arxiv.org/abs/2308.01861.

## Slide 4 — Modelos e condições de coleta

Tempo: 02:10 a 03:00 (50 segundos).

Os modelos foram escolhidos pela viabilidade de acesso. ChatGPT e Gemini foram utilizados pelo navegador, enquanto o Qwen3 foi executado no Ollama local, permitindo processar os prompts em lote. GPT-6 é a identificação que informei para o ChatGPT, sem um snapshot técnico preservado. Para o Gemini, mantenho apenas o nome do produto. O Qwen3 está identificado nos trinta registros como qwen3:8b. A execução local levou quase vinte horas, conforme meu relato. Isso não é uma comparação de velocidade com os serviços do navegador.

## Slide 5 — Mesmo template para cada tarefa

Tempo: 03:00 a 03:50 (50 segundos).

O prompt pede a implementação integral da classe, preservando nomes e assinaturas e utilizando somente a biblioteca padrão. O mesmo template acompanha o esqueleto de cada tarefa. A abordagem é zero-shot no sentido de não acrescentar uma solução resolvida de outra tarefa. Os exemplos das docstrings continuam presentes como parte da especificação. Python foi mantido porque já é a linguagem do benchmark, evitando variação causada por tradução. O piloto verificou o funcionamento do procedimento, mas não provou que esse prompt é o melhor possível. Fonte: Brown et al., 2020, https://arxiv.org/abs/2005.14165.

## Slide 6 — Avaliação funcional e estática

Tempo: 03:50 a 04:45 (55 segundos).

Os testes oficiais foram executados em Python 3.12.14, em Linux, com subprocesso por tarefa, semente aleatória zero e limite de quinze segundos. Além dos testes, a AST verificou sintaxe e contrato estrutural. NOM conta métodos declarados, incluindo construtores. NPM conta nomes que não começam com underscore, uma convenção explícita para Python. A complexidade ciclomática descreve decisões internas. Essas dimensões se complementam: ter assinatura correta não garante comportamento correto, e complexidade menor não significa automaticamente código melhor. Fontes: documentação Python e Radon, https://radon.readthedocs.io/en/latest/intro.html.

## Slide 7 — Aprovações sobre os 668 testes previstos

Tempo: 04:45 a 05:55 (70 segundos).

Neste gráfico todos os modelos usam a mesma base de seiscentos e sessenta e oito testes previstos. ChatGPT aprovou seiscentos e dez, Gemini quinhentos e noventa e seis e Qwen3 duzentos e oitenta e cinco. A diferença entre ChatGPT e Gemini é de quatorze testes, cerca de dois vírgula dez pontos percentuais. O Qwen3 executou somente seiscentos e vinte e três casos: quarenta e cinco não executaram por falhas de carregamento de duas respostas. Entre os testes que executaram, sua aprovação foi de quarenta e cinco vírgula setenta e cinco por cento. Exibir a base prevista evita ocultar essas ausências. Fonte: resultados integrados do repositório, snapshot f7a439f.

## Slide 8 — Aprovar testes não equivale a concluir a classe

Tempo: 05:55 a 06:45 (50 segundos).

Quando cada tarefa recebe o mesmo peso, o resultado muda de perspectiva. ChatGPT aprovou integralmente quatorze tarefas, Gemini doze e Qwen3 oito. Uma classe pode acertar quase todos os casos e ainda exigir correção antes de ser utilizada. O número de testes varia entre tarefas; por isso, a taxa de aprovação por teste e a taxa de classes inteiramente aprovadas respondem a perguntas diferentes. Esses números mostram a necessidade de revisar os casos que falharam, mesmo quando o percentual agregado parece alto. Fonte: resultados integrados do repositório.

## Slide 9 — Complexidade precisa ser lida com a completude

Tempo: 06:45 a 07:45 (60 segundos).

A tabela mostra que ChatGPT preservou todos os contratos e Gemini preservou vinte e nove. Qwen3 preservou quatorze. Sua média de complexidade foi menor, mas foram contabilizados menos métodos e ocorreram omissões e nomes divergentes. Portanto, essa média não demonstra superioridade. Também comparei treze tarefas com contrato completo nos três modelos. Nesse recorte, as médias por classe foram dois vírgula setenta e quatro, três vírgula vinte e dois vírgula sessenta e sete. É uma análise complementar selecionada por completude, e não uma prova de diferença estatística. Fonte: tabelas estáticas do repositório.

## Slide 10 — Falhas e limites que precisam acompanhar os números

Tempo: 07:45 a 08:50 (65 segundos).

Alguns casos explicam os resultados. No Gemini, a tarefa cinco possui init em vez de __init__, confirmado na resposta original, e isso gera quinze erros de instanciação. O nome foi preservado. Duas respostas do Qwen3 não carregaram, deixando quarenta e cinco testes sem execução. A própria referência do ClassEval aprovou seiscentos e sessenta e sete de seiscentos e sessenta e oito casos: existe uma falha de calendário dependente de datas. Mantive o resultado oficial e documentei o problema. As conclusões também são limitadas pela seleção intencional, por uma geração por tarefa e pela ausência de parâmetros completos das interfaces.

## Slide 11 — A revisão precisa combinar comportamento e estrutura

Tempo: 08:50 a 09:50 (60 segundos).

Concluo que o ChatGPT apresentou mais aprovações no conjunto coletado, seguido do Gemini e do Qwen3 local. A conclusão principal, porém, é sobre avaliação: precisamos combinar comportamento e estrutura. Mesmo com todas as assinaturas, o ChatGPT apresentou problemas em dezesseis tarefas. A menor complexidade do Qwen3 acompanhou várias implementações incompletas. Para trabalhos futuros, recomendo várias gerações por tarefa, registro técnico das versões e parâmetros e análise sob outras sementes. Para utilizar qualquer uma dessas respostas, o caminho é conferir a interface, executar os testes e revisar as falhas. Obrigado.

## Slide 12 — Referências e material de apoio

Tempo: 09:50 a 10:00 (10 segundos).

As referências completas, as noventa respostas, os scripts e os resultados detalhados constam no relatório e no repositório. Este slide pode permanecer aberto durante as perguntas. O roteiro totaliza dez minutos, com até cinco minutos de margem para esclarecimentos. Fontes: https://arxiv.org/abs/2308.01861; https://arxiv.org/abs/2005.14165; https://arxiv.org/abs/2505.09388; https://docs.python.org/3.12/; https://radon.readthedocs.io/en/latest/intro.html; https://github.com/gscamposz/avaliacao-codigo-llms.

## Perguntas prováveis

Por que não corrigir as respostas que falharam? Porque o objeto da comparação é a resposta coletada. Uma versão corrigida exigiria avaliação separada.

Por que o Qwen3 tem CC menor? A população contém menos métodos e contratos incompletos. A métrica isolada não mede correção.

O ChatGPT é sempre melhor? Não. Ele obteve mais aprovações nesta coleta, com uma resposta por tarefa e configurações incompletamente controladas.

Por que usar o denominador 668 para Qwen3? Para mostrar a parcela de aprovações demonstradas sobre o mesmo conjunto previsto, mantendo os 45 casos não executados explicitamente separados.

Por que os exemplos das docstrings não tornam o prompt few-shot? Eles descrevem o comportamento da própria tarefa. Não foi acrescentada uma demonstração completa de outra solução.

O que significa o erro da referência? O conjunto de testes também tem limitações. A falha dependente de datas foi mantida e discutida, sem modificar as asserções depois de observar os modelos.
