"""Métricas estáticas reproduzíveis. Não executa código dos modelos."""
import ast
import csv
import hashlib
import importlib.metadata
import json
import platform
import re
import statistics
from pathlib import Path

from radon.complexity import cc_rank, cc_visit
from radon.raw import analyze

BASE = Path(__file__).resolve().parent
METHOD_TYPES = (ast.FunctionDef, ast.AsyncFunctionDef)


def direct_methods(cls):
    return [node for node in cls.body if isinstance(node, METHOD_TYPES)]


def signature(method):
    """Compara nomes/tipos de parâmetros, defaults e static/classmethod; ignora anotações."""
    args = method.args
    default = lambda node: ast.dump(node, include_attributes=False) if node else None
    return {
        "kind": type(method).__name__,
        "posonly": [a.arg for a in args.posonlyargs],
        "positional": [a.arg for a in args.args],
        "vararg": args.vararg.arg if args.vararg else None,
        "kwonly": [a.arg for a in args.kwonlyargs],
        "kwarg": args.kwarg.arg if args.kwarg else None,
        "defaults": [default(a) for a in args.defaults],
        "kw_defaults": [default(a) for a in args.kw_defaults],
        "binding": sorted(
            d.id for d in method.decorator_list
            if isinstance(d, ast.Name) and d.id in {"staticmethod", "classmethod"}
        ),
    }


def stub(method):
    body = method.body
    if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant) and isinstance(body[0].value.value, str):
        body = body[1:]
    if not body:
        return True
    return all(
        isinstance(n, ast.Pass)
        or isinstance(n, ast.Expr) and isinstance(n.value, ast.Constant) and n.value.value is Ellipsis
        or isinstance(n, ast.Raise) and (
            isinstance(n.exc, ast.Name) and n.exc.id == "NotImplementedError"
            or isinstance(n.exc, ast.Call) and isinstance(n.exc.func, ast.Name) and n.exc.func.id == "NotImplementedError"
        )
        for n in body
    )


def mean(values):
    return statistics.mean(values) if values else None


def write_csv(path, rows):
    if not rows:
        return
    keys = list(dict.fromkeys(k for row in rows for k in row))
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=keys)
        writer.writeheader()
        writer.writerows(rows)


def measure():
    tasks = {t["task_id"]: t for t in json.loads((BASE / "entradas/especificacoes.json").read_text())}
    manifest = json.loads((BASE / "entradas/manifesto_funcional.json").read_text())
    files, classes, methods, contracts = [], [], [], []
    for original in manifest:
        model, tid = original["model"], original["task"]
        path = BASE / "entradas/normalizados" / model / (tid + ".py")
        code = path.read_text(encoding="utf-8")
        try:
            specification_tree = ast.parse(tasks[tid]["skeleton"])
            if not any(isinstance(n, ast.ClassDef) for n in specification_tree.body):
                raise SyntaxError("Classe dentro de string literal no esqueleto")
            contract_source = "AST do esqueleto"
        except SyntaxError:
            # Só as linhas de assinatura, sem reparar descrições defeituosas do benchmark.
            headers = re.findall(r"(?m)^    (?:async )?def [^\n]+:", tasks[tid]["skeleton"])
            specification_tree = ast.parse("class " + tasks[tid]["class_name"] + ":\n" + "\n".join(h + "\n        pass" for h in headers))
            contract_source = "linhas de assinatura do esqueleto (docstrings inválidas)"
        expected = next(n for n in specification_tree.body if isinstance(n, ast.ClassDef))
        expected_methods = direct_methods(expected)
        expected_names = {m.name for m in expected_methods}
        raw_path = BASE / "entradas/originais" / model / (tid + "_resposta.txt")
        raw_ok = None
        if raw_path.exists():
            try:
                ast.parse(raw_path.read_text(encoding="utf-8-sig"))
                raw_ok = True
            except SyntaxError:
                raw_ok = False
        row = {
            "modelo": model, "tarefa": tid, "classe_esperada": expected.name,
            "sintaxe_bruta_valida": raw_ok,
            "sintaxe_normalizada_valida": False, "erro_sintaxe": "",
            "sha256_normalizado_bytes": hashlib.sha256(path.read_bytes()).hexdigest(),
            "ajustes": original["normalization"],
            "testes_executados": original["run"], "testes_aprovados": original["passed"],
            "status_funcional": original["status"],
            "metodos_esperados": len(expected_methods), "fonte_contrato": contract_source,
        }
        assert row["sha256_normalizado_bytes"] == original["sha256_normalizado_bytes"]
        try:
            tree = ast.parse(code)
        except SyntaxError as error:
            row.update(erro_sintaxe=f"linha {error.lineno}: {error.msg}",
                       classe_esperada_presente=None,
                       metodos_esperados_encontrados=None,
                       assinaturas_preservadas=None)
            files.append(row)
            continue
        row["sintaxe_normalizada_valida"] = True
        declared = [n for n in tree.body if isinstance(n, ast.ClassDef)]
        found = [n for n in declared if n.name == expected.name]
        present = bool(found)
        actual = direct_methods(found[-1]) if found else []
        by_name = {m.name: m for m in actual}
        count_present = len(expected_names & by_name.keys())
        exact = sum(name in by_name and signature(m) == signature(by_name[name]) for name, m in ((m.name, m) for m in expected_methods))
        row.update(
            classe_esperada_presente=present,
            metodos_esperados_encontrados=count_present,
            assinaturas_preservadas=exact,
            cobertura_nomes=count_present / len(expected_methods) if expected_methods else 1.0,
            cobertura_assinaturas=exact / len(expected_methods) if expected_methods else 1.0,
            contrato_completo=present and exact == len(expected_methods),
        )
        for method in expected_methods:
            actual_method = by_name.get(method.name)
            contracts.append({
                "modelo": model, "tarefa": tid, "classe": expected.name,
                "metodo": method.name, "presente": actual_method is not None,
                "assinatura_preservada": actual_method is not None and signature(method) == signature(actual_method),
                "assinatura_esperada": json.dumps(signature(method), ensure_ascii=False),
                "assinatura_encontrada": json.dumps(signature(actual_method), ensure_ascii=False) if actual_method else "",
            })
        complexity_blocks = cc_visit(code)
        radon_classes = {(b.name, b.lineno): b for b in complexity_blocks if hasattr(b, "methods")}
        task_cc = []
        for cls in declared:
            declared_methods = direct_methods(cls)
            radon_class = radon_classes[(cls.name, cls.lineno)]
            blocks = {(m.name, m.lineno): m for m in radon_class.methods}
            cc = []
            for method in declared_methods:
                block = blocks.get((method.name, method.lineno))
                if block is None:
                    raise RuntimeError(f"Método ausente no Radon: {model}/{tid}/{method.name}")
                cc.append(block.complexity)
                methods.append({
                    "modelo": model, "tarefa": tid, "classe": cls.name,
                    "classe_esperada": cls.name == expected.name,
                    "metodo": method.name, "linha": method.lineno,
                    "publico_convencao": not method.name.startswith("_"),
                    "especial_dunder": method.name.startswith("__") and method.name.endswith("__"),
                    "cc": block.complexity, "faixa_radon": cc_rank(block.complexity),
                    "stub": stub(method),
                })
            task_cc.extend(cc)
            classes.append({
                "modelo": model, "tarefa": tid, "classe": cls.name,
                "classe_esperada": cls.name == expected.name,
                "nom": len(declared_methods),
                "nom_sem_init": sum(m.name != "__init__" for m in declared_methods),
                "npm": sum(not m.name.startswith("_") for m in declared_methods),
                "metodos_especiais": sum(m.name.startswith("__") and m.name.endswith("__") for m in declared_methods),
                "nomes_duplicados": len(declared_methods) - len({m.name for m in declared_methods}),
                "wmc_cc": sum(cc), "cc_media": mean(cc), "cc_max": max(cc) if cc else None,
            })
        raw = analyze(code)
        task_classes = [c for c in classes if c["modelo"] == model and c["tarefa"] == tid]
        expected_metric = next((c for c in reversed(task_classes) if c["classe_esperada"]), {})
        row.update(
            classes_declaradas=len(declared),
            funcoes_nivel_modulo=sum(isinstance(n, METHOD_TYPES) for n in tree.body),
            nom_total=sum(c["nom"] for c in task_classes),
            npm_total=sum(c["npm"] for c in task_classes),
            nom_classe_esperada=expected_metric.get("nom"),
            npm_classe_esperada=expected_metric.get("npm"),
            cc_media_metodos=mean(task_cc),
            cc_max_metodos=max(task_cc) if task_cc else None,
            wmc_total=sum(task_cc) if task_cc else None,
            sloc=raw.sloc,
        )
        files.append(row)
    return files, classes, methods, contracts


def summarize(files, classes, methods):
    rows = []
    for model in ["chatgpt", "gemini", "qwen3_8b", "baseline"]:
        ff = [r for r in files if r["modelo"] == model]
        cc = [r for r in classes if r["modelo"] == model]
        mm = [r for r in methods if r["modelo"] == model]
        row = {
            "modelo": model, "arquivos": len(ff),
            "sintaxe_bruta_valida": sum(r["sintaxe_bruta_valida"] is True for r in ff) if model != "baseline" else None,
            "sintaxe_normalizada_valida": sum(r["sintaxe_normalizada_valida"] for r in ff),
            "arquivos_com_classe_esperada": sum(r.get("classe_esperada_presente") is True for r in ff),
            "contrato_completo": sum(r.get("contrato_completo") is True for r in ff),
            "classes_declaradas": len(cc),
            "nom_total": sum(r["nom"] for r in cc),
            "npm_total": sum(r["npm"] for r in cc),
            "cc_media_ponderada_metodos": mean([r["cc"] for r in mm]),
            "cc_mediana_metodos": statistics.median([r["cc"] for r in mm]) if mm else None,
            "cc_max_metodos": max([r["cc"] for r in mm], default=None),
            "metodos_cc_maior_10": sum(r["cc"] > 10 for r in mm),
            "metodos_stub": sum(r["stub"] for r in mm),
            "metodos_esperados_total": sum(r["metodos_esperados"] for r in ff),
            "metodos_esperados_encontrados_em_analisaveis": sum(r.get("metodos_esperados_encontrados") or 0 for r in ff),
        }
        rows.append(row)
    # Pareamento entre modelos: mesma tarefa e contrato completo nos três.
    model_names = ["chatgpt", "gemini", "qwen3_8b"]
    common = sorted(
        set.intersection(*[
            {r["tarefa"] for r in files if r["modelo"] == model and r.get("contrato_completo")}
            for model in model_names
        ]),
        key=lambda name: int(name.split("_")[-1]),
    )
    paired = []
    for model in model_names:
        ff = [r for r in files if r["modelo"] == model and r["tarefa"] in common]
        cc = [r for r in classes if r["modelo"] == model and r["classe_esperada"] and r["tarefa"] in common]
        paired.append({
            "modelo": model, "tarefas": len(common),
            "ids": ";".join(common),
            "nom_media_por_classe": mean([r["nom"] for r in cc]),
            "npm_media_por_classe": mean([r["npm"] for r in cc]),
            "wmc_media_por_classe": mean([r["wmc_cc"] for r in cc]),
            "cc_media_das_medias_por_classe": mean([r["cc_media"] for r in cc]),
        })
    return rows, paired


def verify_counting():
    example = """class Sample:
    def __init__(self):
        self.x = 0
    @staticmethod
    def public(x):
        if x and x > 1:
            return x
        return 0
    def _private(self):
        pass
    async def other(self):
        return 1
"""
    cls = ast.parse(example).body[0]
    assert len(direct_methods(cls)) == 4
    assert sum(not m.name.startswith("_") for m in direct_methods(cls)) == 2
    block = next(b for b in cc_visit(example) if hasattr(b, "methods"))
    assert next(m.complexity for m in block.methods if m.name == "public") == 3
    assert stub(direct_methods(cls)[2])
    assert not stub(direct_methods(cls)[0])
    assert signature(direct_methods(cls)[1])["binding"] == ["staticmethod"]


if __name__ == "__main__":
    verify_counting()
    ff, cc, mm, contracts = measure()
    summary, paired = summarize(ff, cc, mm)
    output = BASE / "tabelas"
    output.mkdir(exist_ok=True)
    for name, rows in [
        ("por_arquivo", ff), ("por_classe", cc), ("por_metodo", mm),
        ("assinaturas", contracts), ("resumo_modelos", summary), ("comparacao_pareada", paired),
    ]:
        write_csv(output / (name + ".csv"), rows)
        (output / (name + ".json")).write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")
    (output / "ambiente.json").write_text(json.dumps({
        "python": platform.python_version(), "platform": platform.platform(),
        "radon": importlib.metadata.version("radon"),
        "commit": "f4c7ecd69986cc6d987611e253ef4d05be30b0bc",
        "verificacao_contagem": "aprovada",
    }, indent=2), encoding="utf-8")
    print(json.dumps({"resumo": summary, "pareada": paired}, indent=2, ensure_ascii=False))
