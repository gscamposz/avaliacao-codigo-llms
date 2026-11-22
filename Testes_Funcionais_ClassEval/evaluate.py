import os,ast,csv,hashlib,io,json,re,subprocess,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(os.environ.get('CLASSEVAL_REPO', str(Path.cwd())))
OUT=Path(__file__).parent
def normalize(text,model):
    notes=[]
    if model=='gemini':
        code=re.sub(r'^\s*```(?:python|py)?\s*$','',text,flags=re.M)
        if code!=text:notes.append('removed Markdown fence lines')
        # Split the joined class/docstring/method header, preserving all tokens.
        code=re.sub(r'(class \w+:)\s*("""[^\n]*?""")\s*(?=def )',r'\1\n\2\n',code)
        m=re.search(r'(?m)^(?:@staticmethod\s*\n)?def \w+\(',code)
        if m:
            head=code[:m.start()]
            body=code[m.start():]
            head_lines=head.splitlines()
            code='\n'.join(l if l.startswith(('class ','import ','from ')) or not l.strip() else '    '+l for l in head_lines)+'\n'
            code+='\n'.join('    '+l if l.strip() else '' for l in body.splitlines())
            notes.append('restored class indentation and header line breaks')
        return code,notes
    try:ast.parse(text);return text,notes
    except SyntaxError:pass
    blocks=re.findall(r'(?ms)^[ \t]*```(?:python|py)?[ \t]*\n(.*?)^[ \t]*```[ \t]*$',text)
    labelled=re.findall(r'(?ms)^[ \t]*```(?:python|py)[ \t]*\n(.*?)^[ \t]*```[ \t]*$',text)
    if labelled:blocks=labelled
    if blocks:
        return '\n\n'.join(blocks),['extracted fenced code blocks without changing code']
    return text,notes
def worker(payload,output):
    d=json.loads(Path(payload).read_text())
    import random
    random.seed(0)
    module={'__name__':'candidate_module'}
    result={'status':'not_run','run':0,'failures':0,'errors':0,'passed':0}
    log=io.StringIO()
    try:
        exec(compile(d['code'],'candidate.py','exec'),module)
        exec(compile(d['test'],'official_tests.py','exec'),module)
        suite=unittest.TestSuite()
        for name in d['test_classes']:
            suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(module[name.strip()]))
        r=unittest.TextTestRunner(stream=log,verbosity=2).run(suite)
        result.update(status='tested',run=r.testsRun,failures=len(r.failures),errors=len(r.errors),passed=r.testsRun-len(r.failures)-len(r.errors))
    except BaseException:
        import traceback
        result['status']='load_error'
        log.write(traceback.format_exc())
    result['log']=log.getvalue()
    Path(output).write_text(json.dumps(result))
if len(sys.argv)>1 and sys.argv[1]=='--worker':
    worker(sys.argv[2],sys.argv[3]);sys.exit()
data={d['task_id']:d for d in json.loads((ROOT/'ClassEval_data.json').read_text())}
rows=[]
for model in ['baseline','chatgpt','gemini','qwen3_8b']:
    paths=sorted((ROOT/'resultados/chatgpt' if model=='baseline' else ROOT/'resultados'/model).glob('*_resposta.txt'))
    for file in paths:
        tid=re.match(r'ClassEval_\d+',file.name)[0];task=data[tid]
        text=task['solution_code'] if model=='baseline' else file.read_text(encoding='utf-8-sig')
        code,notes=normalize(text,model)
        prepared = ROOT / 'resultados' / model / 'preparados' / (tid + '.py')
        if model == 'gemini' and tid in {'ClassEval_5', 'ClassEval_71'} and prepared.exists():
            code = prepared.read_text(encoding='utf-8')
            unfenced = re.sub(r'^\s*```(?:python)?[ \t]*$', '', text, flags=re.M)
            if re.sub(r'\s', '', unfenced) != re.sub(r'\s', '', code):
                raise ValueError(f'A preparação alterou caracteres não brancos: {tid}')
            notes = ['restored whitespace and removed fence lines; verified nonwhitespace equality']
        dest=OUT/model;dest.mkdir(exist_ok=True)
        (dest/(tid+'.py')).write_text(code)
        raw_valid=True
        try:ast.parse(text)
        except SyntaxError:raw_valid=False
        row={'model':model,'task':tid,'class':task['class_name'],'raw_syntax_valid':raw_valid,'normalization':'; '.join(notes),'sha256_original':hashlib.sha256(text.encode()).hexdigest()}
        try:
            tree=ast.parse(code)
            present=any(isinstance(n,ast.ClassDef) and n.name==task['class_name'] for n in tree.body)
            row['expected_class_present']=present
        except SyntaxError:row['expected_class_present']=False
        with tempfile.TemporaryDirectory() as tmp:
            payload=Path(tmp)/'input.json';output=Path(tmp)/'output.json'
            payload.write_text(json.dumps({'code':code,'test':task['test'],'test_classes':task['test_classes']}))
            try:
                p=subprocess.run([sys.executable,str(Path(__file__).resolve()),'--worker',str(payload),str(output)],cwd=tmp,capture_output=True,text=True,timeout=15)
                result=json.loads(output.read_text()) if output.exists() else {'status':'process_error','run':0,'passed':0,'failures':0,'errors':0,'log':p.stderr}
            except subprocess.TimeoutExpired:
                result={'status':'timeout','run':0,'passed':0,'failures':0,'errors':0,'log':'15 second execution timeout'}
        (dest/(tid+'.log')).write_text(result.pop('log'))
        row.update(result);rows.append(row)
    print(model,[(r['status'],r['task']) for r in rows if r['model']==model and r['status']!='tested'],flush=True)
(OUT/'ambiente.json').write_text(json.dumps({
    'snapshot_entradas': subprocess.check_output(['git', '-C', str(ROOT), 'rev-parse', 'HEAD'], text=True).strip(),
    'python': sys.version,
    'semente_random': 0,
    'timeout_por_tarefa_segundos': 15,
    'arquivo_testes_sha256': hashlib.sha256((ROOT/'ClassEval_data.json').read_bytes()).hexdigest(),
}, indent=2))
(OUT/'results.json').write_text(json.dumps(rows,indent=2,ensure_ascii=False))
with (OUT/'results.csv').open('w') as f:
    w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
for m in ['baseline','chatgpt','gemini','qwen3_8b']:
    rr=[r for r in rows if r['model']==m]
    print(m,'passed',sum(r['passed'] for r in rr),'run',sum(r['run'] for r in rr),'full',sum(r['status']=='tested' and r['run']>0 and r['failures']==r['errors']==0 for r in rr),'load',sum(r['status']!='tested' for r in rr))
