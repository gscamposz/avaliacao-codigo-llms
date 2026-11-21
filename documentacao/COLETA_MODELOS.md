# Metadados da coleta

Formas de acesso confirmadas por Gustavo Silva Campos em 21/11/2026.

| Identificação no experimento | Forma de acesso | Identificador técnico comprovado |
|---|---|---|
| ChatGPT | Navegador | Modelo/versão selecionado não informado |
| Gemini | Navegador no piloto e na coleta principal | Modelo/versão selecionado não informado |
| Qwen3 8B | Ollama local | qwen3:8b em 30 registros JSON |

Os nomes ChatGPT e Gemini identificam os produtos utilizados. A interface de acesso não permite deduzir o identificador ou versão do modelo selecionado.

## Evidências do Ollama

Os 30 registros resultados/qwen3_8b/ClassEval_*_registro.json identificam qwen3:8b.
created_at varia de 2026-11-21T02:00:22.2377211Z a 2026-11-21T20:56:46.0396562Z. No horário de Brasília, o intervalo corresponde a 20/11/2026 às 23:00 até 21/11/2026 às 17:56. São timestamps de conclusão gravados pela API.
Os registros comprovam o tag, mas não contêm o digest do modelo, a versão do servidor Ollama ou as configurações completas de geração.

O comando de coleta compartilhado na conversa enviava model, prompt e stream=false, com timeout de 3600 segundos. Ele fazia uma requisição independente por tarefa. A confirmação de que todos os arquivos foram gerados exatamente com esse comando depende dos registros locais do autor.

## Informações ainda a completar

- Nome do modelo selecionado no ChatGPT e no Gemini, conforme a interface no momento da coleta.
- Datas da coleta pelo navegador.
- Caso disponível, versão efetiva do Ollama durante a coleta, digest e parâmetros do modelo.
- Histórico de retomadas. erros.log registra dois timeouts em ClassEval_65, e os arquivos finais dessa tarefa estão presentes.

A ausência dessas informações foi registrada sem estimar versões. A revisão 2 incorpora os resultados reexecutados e mantém as informações desconhecidas explicitamente identificadas.

## Confirmação adicional

O autor confirmou que a resposta original de ClassEval_5 do Gemini contém def init(self, text), conforme o TXT versionado. As cópias executáveis preservam esse nome.
