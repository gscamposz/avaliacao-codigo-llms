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
| ChatGPT | Navegador |
| Gemini | Navegador no piloto, com API prevista para a coleta principal |
| Qwen3 8B | Ollama local — `qwen3:8b` |

Os identificadores exatos dos modelos, as datas e as configurações utilizadas devem ser registrados durante a coleta.

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

Respostas coletadas via API podem ficar em subpastas identificadas pelo provedor e pelo modelo.

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

### Análise estática planejada

- AST — inspeção da estrutura, das classes e das assinaturas.
- Complexidade ciclomática por método.
- NOM — quantidade de métodos por classe.
- NPM — quantidade de métodos públicos por classe.

As ferramentas, fontes e regras de contagem serão documentadas antes da análise principal. Em Python, a contagem de métodos públicos seguirá uma convenção explicitamente definida.

## Resultados do piloto

Foram utilizadas as tarefas `ClassEval_16` (`Calculator`) e `ClassEval_94` (`VendingMachine`).

| Modelo | Calculator | VendingMachine | Total de testes aprovados |
|---|---:|---:|---:|
| ChatGPT | 18/19 | 24/27 | 42/46 — 91,3% |
| Gemini | 18/19 | 27/27 | 45/46 — 97,8% |
| Qwen3 8B | 5/19 | 27/27 | 32/46 — 69,6% |

As cópias executáveis do Gemini receberam ajustes de formatação. Os resultados foram obtidos nas execuções locais do piloto.

Esses percentuais representam a proporção de testes aprovados nas duas tarefas. A amostra é pequena e os resultados não estabelecem uma classificação geral dos modelos.

Foi identificada uma inconsistência no exemplo de `apply_operator` da tarefa `Calculator`: o exemplo mostra uma pilha de operadores diferente da esperada pelos testes oficiais. A divergência será discutida na análise.

## Estado do projeto

- [x] Seleção das 30 tarefas.
- [x] Preparação dos prompts.
- [x] Execução do piloto.
- [ ] Conclusão das 90 gerações.
- [ ] Testes funcionais da avaliação principal.
- [ ] Análise estática.
- [ ] Consolidação dos resultados e relatório.

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
