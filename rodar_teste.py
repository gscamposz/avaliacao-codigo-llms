import json
import sys
import types
import unittest
from pathlib import Path

id_tarefa, caminho_resposta = sys.argv[1:]
base = Path(__file__).with_name("ClassEval_data.json")
tarefas = json.loads(base.read_text(encoding="utf-8-sig"))
tarefa = next(item for item in tarefas if item["task_id"] == id_tarefa)

resposta = Path(caminho_resposta)
modulo = types.ModuleType("avaliacao_classeval")

exec(compile(resposta.read_text(encoding="utf-8-sig"), str(resposta), "exec"),
     modulo.__dict__)
exec(compile(tarefa["test"], f"{id_tarefa}_testes_oficiais.py", "exec"),
     modulo.__dict__)

suite = unittest.defaultTestLoader.loadTestsFromModule(modulo)
if not suite.countTestCases():
    raise SystemExit("Nenhum teste foi encontrado.")

resultado = unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(0 if resultado.wasSuccessful() else 1)