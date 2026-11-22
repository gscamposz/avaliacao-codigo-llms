# Guia de reprodução da avaliação

A reprodução utiliza os arquivos já coletados. Nenhuma chamada a ChatGPT, Gemini ou Ollama é necessária para executar os testes e calcular as métricas. O snapshot de evidência do relatório é f7a439fc46299f5379a2587ba9f70ee2968917eb. As alterações posteriores da etapa final documentam o trabalho e os metadados informados pelo autor.

## Ambiente

A execução consolidada utilizou Python 3.12.14 em Linux, Radon 6.0.1, semente random 0 e timeout de 15 segundos por tarefa. A figura do pacote estático usa Matplotlib 3.10.8. As respostas foram coletadas entre 9 e 21 de novembro de 2026. As versões dos serviços remotos não são integralmente reproduzíveis.

No Windows, WSL aproxima o ambiente Linux utilizado. Os comandos abaixo pressupõem Git e uma instalação Python 3.12 disponível. Use uma cópia separada: os scripts sobrescrevem resultados e logs locais. Os testes executam o código dos arquivos candidatos; não acrescente código desconhecido à avaliação.

## Obtenção e execução

```bash
git clone https://github.com/gscamposz/avaliacao-codigo-llms.git
cd avaliacao-codigo-llms
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

Para consultar os artefatos exatamente como estavam no snapshot de evidência, após clonar use `git checkout f7a439fc46299f5379a2587ba9f70ee2968917eb`. Nesse snapshot, os textos de metadados ainda não incluem as confirmações finais do autor. A atualização posterior não altera as 90 respostas nem os resultados arquivados.

## O que conferir

- `Testes_Funcionais_ClassEval/results.json`: resultados por tarefa e modelo, incluindo controle baseline.
- `Testes_Funcionais_ClassEval/ambiente.json`: Python, semente, timeout e hash da base.
- `Metricas_Estaticas_ClassEval/tabelas/`: métricas por método, classe e arquivo, além do recorte pareado.
- `documentacao/resultados_integrados.csv`: cruzamento funcional e estrutural.
- `documentacao/resumo_integrado.csv`: totais por modelo.
- `documentacao/REVISAO_GEMINI_5_71.md`: recuperação de formatação e confirmação de init na tarefa 5.

Totais arquivados: ChatGPT 610/668 aprovados; Gemini 596/668; Qwen3 285/623 executados e 45 não executados. Referência 667/668. Um teste de calendário depende da data, e casos aleatórios dependem da semente. Divergências de execução devem ser investigadas no log individual e no ambiente, sem editar as asserções para reproduzir artificialmente um total.

## Integridade

Os arquivos CHECKSUMS.json registram os pacotes arquivados. Uma nova execução pode mudar logs, versões de ambiente e arquivos gerados; hashes antigos deixam de representar os novos bytes. Os scripts de sincronização verificam os hashes das respostas de entrada. Para auditar o snapshot original, utilize o commit fixado. Não publique resultados de uma reexecução como se fossem os números históricos sem identificar o ambiente e a data.

## Limites

A reprodução do processamento não reproduz a coleta: os modelos podem gerar outras respostas. O relatório utiliza uma única resposta preservada por tarefa. Não há medição comparável de custo, energia ou tempo entre os três modelos. As 90 respostas originais não devem receber correções de lógica durante uma tentativa de reproduzir os resultados.
