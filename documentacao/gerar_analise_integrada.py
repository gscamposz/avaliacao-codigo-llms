"""Atualiza relatórios e tabelas integradas a partir das execuções e métricas."""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "documentacao"
FUNCTIONAL = ROOT / "Testes_Funcionais_ClassEval"
STATIC = ROOT / "Metricas_Estaticas_ClassEval"
MODELS = ["chatgpt", "gemini", "qwen3_8b"]
LABELS = {"chatgpt": "ChatGPT", "gemini": "Gemini", "qwen3_8b": "Qwen3 8B"}
functional = json.loads((FUNCTIONAL / "results.json").read_text())
metrics = json.loads((STATIC / "tabelas/por_arquivo.json").read_text())
static_summary = {
    item["modelo"]: item
    for item in json.loads((STATIC / "tabelas/resumo_modelos.json").read_text())
}
lookup = {(item["modelo"], item["tarefa"]): item for item in metrics}
expected_tests = {item["task"]: item["run"] for item in functional if item["model"] == "baseline"}
assert len(expected_tests) == 30 and sum(expected_tests.values()) == 668
summary = []
joined = []
for model in MODELS:
    rows = [item for item in functional if item["model"] == model]
    assert len(rows) == 30
    entry = {
        "modelo": model,
        "testes_previstos": sum(expected_tests[item["task"]] for item in rows),
        "testes_executados": sum(item["run"] for item in rows),
        "aprovados": sum(item["passed"] for item in rows),
        "falhas": sum(item["failures"] for item in rows),
        "erros": sum(item["errors"] for item in rows),
        "arquivos_sem_carregar": sum(item["status"] != "tested" for item in rows),
        "tarefas_aprovadas": sum(item["status"] == "tested" and item["run"] > 0 and item["failures"] == item["errors"] == 0 for item in rows),
    }
    entry["testes_nao_executados"] = entry["testes_previstos"] - entry["testes_executados"]
    entry["proporcao_aprovados_entre_executados"] = entry["aprovados"] / entry["testes_executados"]
    entry["aprovados_sobre_previstos"] = entry["aprovados"] / entry["testes_previstos"]
    assert entry["aprovados"] + entry["falhas"] + entry["erros"] == entry["testes_executados"]
    summary.append(entry)
    for item in rows:
        metric = lookup[(model, item["task"])]
        joined.append({
            "modelo": model, "tarefa": item["task"],
            "status_funcional": item["status"],
            "testes_previstos": expected_tests[item["task"]],
            "testes_executados": item["run"], "testes_aprovados": item["passed"],
            "falhas": item["failures"], "erros": item["errors"],
            "sintaxe_normalizada_valida": metric["sintaxe_normalizada_valida"],
            "classe_esperada_presente": metric.get("classe_esperada_presente"),
            "contrato_completo": metric.get("contrato_completo"),
            "nom_total": metric.get("nom_total"), "npm_total": metric.get("npm_total"),
            "cc_media": metric.get("cc_media_metodos"), "cc_max": metric.get("cc_max_metodos"),
            "ajustes": metric["ajustes"],
        })
for name, rows in [("resumo_integrado", summary), ("resultados_integrados", joined)]:
    (DOC / (name + ".json")).write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    with (DOC / (name + ".csv")).open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

table = "\n".join(
    f"| {LABELS[r['modelo']]} | {r['aprovados']}/{r['testes_executados']} | "
    f"{r['falhas']} | {r['erros']} | {r['testes_nao_executados']} | "
    f"{r['tarefas_aprovadas']}/30 |"
    for r in summary
)
environment = json.loads((FUNCTIONAL / "ambiente.json").read_text())
functional_report = f"""# Testes funcionais — revisão 2

Entradas versionadas no commit {environment['snapshot_entradas']}.
Nesta revisão foram reexecutadas as 90 respostas e as 30 soluções de referência.

## Procedimento

Execução em Python/Linux, com um processo e diretório temporário por tarefa, semente random 0 e timeout de 15 segundos por processo.
As asserções e os corpos dos testes oficiais em ClassEval_data.json foram preservados. O carregador retira espaços nas extremidades dos nomes em test_classes, por causa de um espaço extra nos metadados de Words2Numbers.
As respostas originais permanecem em resultados/ e originais/. As cópias executadas e logs estão nas pastas dos modelos deste pacote.

## Resultados

| Modelo | Aprovados/executados | Falhas | Erros nos testes | Testes não executados | Tarefas com suíte inteira aprovada |
|---|---:|---:|---:|---:|---:|
{table}

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
Esta revisão documenta os resultados funcionais e estáticos. A documentação acadêmica final autorizada encontra-se em documentacao/.
"""
(FUNCTIONAL / "RELATORIO.md").write_text(functional_report, encoding="utf-8")

static_table = "\n".join(
    f"| {LABELS[model]} | {static_summary[model]['sintaxe_normalizada_valida']}/30 | "
    f"{static_summary[model]['contrato_completo']}/30 | "
    f"{static_summary[model]['nom_total']} | {static_summary[model]['npm_total']} | "
    f"{static_summary[model]['cc_media_ponderada_metodos']:.2f} |"
    for model in MODELS
)
percentage_table = "\n".join(
    f"| {LABELS[r['modelo']]} | {100*r['proporcao_aprovados_entre_executados']:.2f}% | "
    f"{100*r['aprovados_sobre_previstos']:.2f}% |"
    for r in summary
)
structural_fail = {
    model: sum(
        item["modelo"] == model and item["contrato_completo"] is True
        and (item["status_funcional"] != "tested" or item["falhas"] + item["erros"] > 0)
        for item in joined
    )
    for model in MODELS
}
contract_pass = {
    model: sum(
        item["modelo"] == model and item["contrato_completo"] is True
        and item["status_funcional"] == "tested" and item["falhas"] == item["erros"] == 0
        for item in joined
    )
    for model in MODELS
}
cross_table = "\n".join(
    f"| {LABELS[m]} | {contract_pass[m]} | {structural_fail[m]} |"
    for m in MODELS
)
calendar = [item for item in functional if item["task"] == "ClassEval_17"]
calendar_detail = "\n".join(
    f"- {LABELS.get(r['model'], 'Referência ClassEval')} — "
    f"{r['passed']}/{r['run']} testes aprovados, {r['failures']} falhas e {r['errors']} erros."
    for r in calendar
)
integrated = f"""# Análise integrada — resultados funcionais e estáticos

Revisão 2 baseada no snapshot de entradas {environment['snapshot_entradas']}.
Este documento consolida a análise descritiva. O relatório acadêmico e o roteiro da apresentação foram preparados na etapa final autorizada pelo autor e estão em documentacao/.

## Amostra e coleta

Foram selecionadas 30 tarefas do ClassEval e coletada uma resposta por tarefa em cada modelo, totalizando 90 respostas.
ChatGPT e Gemini foram acessados pelo navegador. Qwen3 8B foi executado localmente pelo Ollama com tag qwen3:8b, conforme confirmado pelo autor e pelos registros locais.
O autor informou GPT-6 para o ChatGPT e o período de coleta de 9 a 21 de novembro de 2026. Não há snapshot técnico independente do ChatGPT nem variante específica do Gemini. Datas individuais das conversas não foram preservadas. Consulte COLETA_MODELOS.md.
O piloto Calculator/VendingMachine é separado desta amostra e não entra nos totais.

## Resultados funcionais

| Modelo | Aprovados/executados | Falhas | Erros nos testes | Não executados | Tarefas com suíte inteira aprovada |
|---|---:|---:|---:|---:|---:|
{table}

Cada modelo tem 668 testes previstos. Cada teste tem peso igual no total de testes, mas o número de testes varia entre tarefas. A contagem de tarefas inteiramente aprovadas dá peso igual a cada tarefa.
Os 45 testes não executados do Qwen3 pertencem a duas respostas que falham no carregamento. Elas permanecem no universo de 30 tarefas.

| Modelo | Aprovação entre testes executados | Aprovados sobre 668 previstos |
|---|---:|---:|
{percentage_table}

O segundo percentual mantém a base de 668 e representa a parcela de aprovações demonstradas. Ele não converte automaticamente testes não executados em falhas de asserção.

## Métricas estáticas

| Modelo | Sintaxe após preparação | Contrato estrutural completo | NOM total | NPM total | CC média por método |
|---|---:|---:|---:|---:|---:|
{static_table}

NOM inclui os métodos declarados diretamente nas classes e seus construtores. NPM conta os métodos cujos nomes não começam com underscore, segundo a convenção operacional adotada. CC é calculada com Radon 6.0.1.
O contrato estrutural verifica classe e assinaturas. A tabela detalhada informa o método ausente ou alterado. Essas verificações não analisam o comportamento das implementações.

ChatGPT teve todas as classes e assinaturas preservadas, mas só 14 tarefas passaram em toda a suíte.
Gemini teve 29 contratos completos e 12 tarefas totalmente aprovadas. A resposta da tarefa 5 declara init, confirmado pelo autor como presente no original, e não inicializa o objeto como o teste exige.
Qwen3 teve 14 contratos completos, várias classes renomeadas e respostas parciais. Sua CC média menor acompanha um conjunto com menos métodos, por isso a média global não demonstra superioridade.

## Contrato estrutural versus teste funcional

| Modelo | Contrato completo e suíte toda aprovada | Contrato completo com falha ou erro funcional |
|---|---:|---:|
{cross_table}

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

{calendar_detail}

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
"""
(DOC / "ANALISE_INTEGRADA.md").write_text(integrated, encoding="utf-8")
print(json.dumps(summary, ensure_ascii=False, indent=2))
