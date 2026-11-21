"""Sincroniza entradas estáticas com a última execução funcional do repositório."""
import hashlib
import json
import shutil
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROOT = BASE.parent
FUNCTIONAL = ROOT / "Testes_Funcionais_ClassEval"
rows = json.loads((FUNCTIONAL / "results.json").read_text(encoding="utf-8"))
for row in rows:
    model, task = row["model"], row["task"]
    source = FUNCTIONAL / model / (task + ".py")
    destination = BASE / "entradas/normalizados" / model / source.name
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)
    row["sha256_normalizado_bytes"] = hashlib.sha256(destination.read_bytes()).hexdigest()
    if model != "baseline":
        raw = ROOT / "resultados" / model / (task + "_resposta.txt")
        text_hash = hashlib.sha256(raw.read_text(encoding="utf-8-sig").encode()).hexdigest()
        if text_hash != row["sha256_original"]:
            raise ValueError(f"O TXT mudou após a execução funcional: {model}/{task}")
        original = BASE / "entradas/originais" / model / raw.name
        original.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(raw, original)
(BASE / "entradas/manifesto_funcional.json").write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")
environment = json.loads((FUNCTIONAL / "ambiente.json").read_text())
(BASE / "entradas/proveniencia.json").write_text(json.dumps(environment, indent=2, ensure_ascii=False), encoding="utf-8")
print("Entradas sincronizadas e hashes conferidos.")
