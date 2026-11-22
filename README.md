# ClassEval LLM Comparison

Projeto acadêmico da disciplina de Desenvolvimento Orientado a Objetos (DOO), do curso de Sistemas de Informação.

O estudo compara códigos Python gerados por ChatGPT, Gemini e Qwen3 8B a partir de 30 tarefas do benchmark ClassEval.

## Objetivo

Analisar como diferentes modelos de linguagem implementam classes Python, considerando o atendimento às especificações, a correção funcional e as características estruturais dos códigos.

## Escopo

- 30 tarefas selecionadas do ClassEval.
- 3 modelos de linguagem.
- 1 resposta por tarefa e modelo.
- 90 respostas na avaliação principal.
- 2 tarefas adicionais para o piloto.

## Modelos

| Modelo | Ambiente |
|---|---|
| ChatGPT (GPT-6 informado pelo autor) | Navegador |
| Gemini | Navegador, no piloto e na coleta principal |
| Qwen3 8B | Ollama local — `qwen3:8b` |

Coleta realizada entre 9 e 21 de novembro de 2026, conforme relato do autor. ChatGPT foi identificado pelo autor como GPT-6, sem snapshot técnico preservado. Gemini permanece sem variante específica registrada. O tag qwen3:8b consta nos 30 registros do Ollama. Consulte [os metadados da coleta](documentacao/COLETA_MODELOS.md) e [a revisão das tarefas 5 e 71 do Gemini](documentacao/REVISAO_GEMINI_5_71.md).

## Metodologia

1. Selecionar 30 especificações de classes Python do ClassEval.
2. Preparar um template de prompt zero-shot.
3. Validar o procedimento em duas tarefas de piloto.
4. Enviar o mesmo prompt de cada tarefa aos três modelos.
5. Preservar a primeira resposta de cada geração.
6. Executar os testes oficiais do ClassEval.
7. Aplicar métricas estáticas e comparar os resultados.

Cada tarefa é enviada em uma conversa nova ou em uma requisição independente.

## Prompt utilizado

```text
Complete a classe Python 3 a partir do esqueleto fornecido.

Implemente todos os métodos conforme as descrições e os exemplos do esqueleto.
Preserve o nome da classe, os nomes dos métodos e suas assinaturas.
Use apenas a biblioteca padrão do Python.
Retorne somente o código completo, incluindo os imports necessários, sem Markdown ou explicações.

ESPECIFICAÇÃO:
[esqueleto original da tarefa]
```

## Organização dos arquivos

| Caminho | Conteúdo |
|---|---|
| `01_utilitarios/` | 10 especificações de utilitários e processamento de dados |
| `02_regras_de_negocio/` | 10 especificações de regras de negócio |
| `03_jogos_e_simulacoes/` | 10 especificações de jogos e simulações |
| `prompts/` | 30 prompts completos da avaliação principal |
| `piloto/` | Especificações, respostas e logs do piloto |
| `resultados/` | Respostas da avaliação principal, organizadas por modelo |
| `ClassEval_data.json` | Dados oficiais do benchmark, incluindo testes |
| `rodar_teste.py` | Script para executar os testes de uma tarefa |

As respostas principais ficam em resultados/chatgpt, resultados/gemini e resultados/qwen3_8b. Somente Qwen3 utilizou a API local; os demais foram acessados pelo navegador.

## Preservação das respostas

Os arquivos `.txt` armazenam as respostas originais.

A preparação de cópias `.py` para análise deve ser documentada. Ajustes de formatação, como remover cercas Markdown ou reconstruir a indentação perdida na transferência, são registrados separadamente.

Alterações na lógica devem ser mantidas como versões corrigidas e avaliadas separadamente das respostas originais.

## Avaliação

### Testes funcionais

Os testes são obtidos do campo `test` do arquivo oficial `ClassEval_data.json`.

Para executar uma tarefa:

```powershell
py .\rodar_teste.py ClassEval_94 '.\piloto\respostas\chatGPT\ClassEval_94_resposta_chatGPT.py'
```

São registrados o número de testes executados, aprovações, falhas e erros.

### Análise estática concluída

- AST — inspeção da estrutura, das classes e das assinaturas.
- Complexidade ciclomática por método.
- NOM — quantidade de métodos por classe.
- NPM — quantidade de métodos públicos por classe.

As regras e os resultados estão em [Metricas_Estaticas_ClassEval](Metricas_Estaticas_ClassEval/RELATORIO_METRICAS.md). NOM inclui construtores e métodos diretos; NPM conta nomes sem prefixo underscore. CC é calculada com Radon 6.0.1. Métricas ausentes por erro de sintaxe não são convertidas em zero.

## Resultados da avaliação principal

| Modelo | Aprovados/previstos | Falhas | Erros | Não executados | Tarefas integralmente aprovadas |
|---|---:|---:|---:|---:|---:|
| ChatGPT | 610/668 (91,32%) | 52 | 6 | 0 | 14/30 |
| Gemini | 596/668 (89,22%) | 51 | 21 | 0 | 12/30 |
| Qwen3 8B | 285/668 (42,66%) | 21 | 317 | 45 | 8/30 |

Qwen3 executou 623 testes, com 45,75% de aprovação entre os executados. Os 45 não executados pertencem a duas respostas com falha de carregamento. O controle ClassEval aprovou 667/668 testes, com uma falha de calendário dependente de datas. Uma resposta por tarefa não permite uma classificação geral dos modelos.

| Modelo | Contrato completo | NOM total | NPM total | CC média por método |
|---|---:|---:|---:|---:|
| ChatGPT | 30/30 | 152 | 122 | 3,65 |
| Gemini | 29/30 | 153 | 123 | 3,72 |
| Qwen3 8B | 14/30 | 115 | 92 | 2,63 |

A CC menor do Qwen3 acompanha menor completude e não demonstra superioridade. [Análise integrada](documentacao/ANALISE_INTEGRADA.md) e [dados por tarefa](documentacao/resultados_integrados.csv).

## Reprodução

O protocolo consolidado utiliza Python 3.12.14 em Linux, semente 0 e timeout de 15 segundos por tarefa. Para reproduzir, use uma cópia de trabalho: os scripts atualizam resultados e logs locais. No Windows, prefira WSL para aproximar o ambiente registrado.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r Metricas_Estaticas_ClassEval/requirements.txt
python -m pip install -r Metricas_Estaticas_ClassEval/requisitos_figura.txt
python Testes_Funcionais_ClassEval/evaluate.py
python Metricas_Estaticas_ClassEval/atualizar_entradas.py
python Metricas_Estaticas_ClassEval/calcular_metricas.py
python Metricas_Estaticas_ClassEval/gerar_relatorio.py
python documentacao/gerar_analise_integrada.py
```

O comando python3.12 deve apontar à instalação 3.12 disponível; a execução arquivada utilizou 3.12.14. Mudanças de ambiente, data e dependências podem afetar a reprodução. Consulte o [guia detalhado](documentacao/GUIA_REPRODUCAO.md). Reexecutar a avaliação dos arquivos existentes não equivale a reproduzir a geração pelos modelos.

## Documentação final

- [Ficha de coleta e modelos](documentacao/COLETA_MODELOS.md)
- [Relatório acadêmico em texto](documentacao/TRABALHO_ACADEMICO.md)
- [Roteiro de apresentação de 10 minutos](documentacao/ROTEIRO_APRESENTACAO.md)
- [Checklist de entrega](documentacao/CHECKLIST_FINAL.md)

Os arquivos Word, PDF e PowerPoint são entregues separadamente ao autor. As 90 respostas originais e seus resultados permanecem preservados.

## Resultados do piloto

Foram utilizadas as tarefas `ClassEval_16` (`Calculator`) e `ClassEval_94` (`VendingMachine`).

| Modelo | Calculator | VendingMachine | Total de testes aprovados |
|---|---:|---:|---:|
| ChatGPT | 18/19 | 24/27 | 42/46 — 91,3% |
| Gemini | 18/19 | 27/27 | 45/46 — 97,8% |
| Qwen3 8B | 5/19 | 27/27 | 32/46 — 69,6% |

As cópias executáveis do Gemini receberam ajustes de formatação. Os resultados foram obtidos nas execuções locais do piloto.

Esses percentuais representam a proporção de testes aprovados nas duas tarefas. A amostra é pequena e os resultados não estabelecem uma classificação geral dos modelos.

Foi identificada uma inconsistência no exemplo de `apply_operator` da tarefa `Calculator`: o exemplo mostra uma pilha de operadores diferente da esperada pelos testes oficiais. A divergência é documentada como limitação do piloto, separado da amostra principal.

## Estado do projeto

- [x] Seleção das 30 tarefas.
- [x] Preparação dos prompts.
- [x] Execução do piloto.
- [x] Conclusão das 90 gerações.
- [x] Testes funcionais da avaliação principal.
- [x] Análise estática.
- [x] Consolidação dos resultados e relatório.

## Limitações

- A seleção das tarefas é intencional e não representa todo o ClassEval.
- Uma única geração por tarefa não caracteriza a variabilidade dos modelos.
- Interfaces e configurações diferentes podem influenciar os resultados.
- Aprovação nos testes não garante ausência de defeitos.
- Métricas de complexidade devem ser interpretadas junto à completude e à correção funcional.
- O ClassEval é público, e uma possível exposição dos modelos às tarefas durante o treinamento não foi investigada.

## Fonte e atribuição

Du, X. et al. *ClassEval: A Manually-Crafted Benchmark for Evaluating LLMs on Class-level Code Generation*. 2023.

- Repositório — https://github.com/FudanSELab/ClassEval
- Artigo — https://arxiv.org/abs/2308.01861

Os dados do ClassEval são distribuídos sob CC BY-NC 4.0. O código do repositório original utiliza a licença MIT. As condições dos materiais de origem devem ser preservadas na redistribuição.

## Autor

Gustavo Silva Campos  
Sistemas de Informação — DOO
