"""Prepare isolated synthetic skill exercises and check their actual artifacts."""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
RUNTIME_FILES = ['AGENTS.md', 'START_HERE.md', 'sources/catalog.md', 'inbox/README.md',
                 'knowledge/README.md', 'runs/README.md', 'commitments/source-map.md',
                 'quality/acceptance.md', 'quality/query-checks.md', 'quality/workflow-checks.md',
                 'scripts/validate.py']
RUNTIME_DIRS = ['.agents/skills', 'routines', 'templates']


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def under(root, name):
    path = (root/name).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError(f'Path escapes workspace: {name}')
    return path


def prepare(case_name, destination, root=ROOT):
    case = under(root/'evals/cases', case_name)
    inputs = json.loads((case/'input.json').read_text())
    expected = json.loads((case/'expected.json').read_text())
    destination = Path(destination).resolve()
    if destination.exists():
        raise ValueError('Choose a new run directory; existing results are preserved')
    workspace = destination/'workspace'
    workspace.mkdir(parents=True)
    for name in RUNTIME_FILES:
        target = under(workspace, name);target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(root/name, target)
    for name in RUNTIME_DIRS:
        shutil.copytree(root/name, workspace/name)
    # Never copy a client's profile, knowledge, sources, configuration or runs.
    seeds = {
        'README.md': '# Ensaio fictício isolado\n\nLeia TASK.md e AGENTS.md. Todos os dados desta pasta são sintéticos.\n',
        'profile/overview.md': '# Contexto do executivo\n\nEstado: a preencher neste ensaio fictício.\n',
        'config/brain.json': json.dumps(dict(schema_version=1,state='template',project_name='',executive_goal='',timezone='',calendar_source_id=None,tasks_source_id=None,automation_state='not_configured'),indent=2)+'\n',
        'config/sources.json': '{"schema_version": 1, "sources": []}\n',
    }
    for name, text in (seeds | inputs['files']).items():
        target = under(workspace, name);target.parent.mkdir(parents=True, exist_ok=True);target.write_text(text)
    task = '# Ensaio da mentoria\n\n'+inputs['lesson']+'\n\n'+inputs['prompt']+'\n\nUse somente esta pasta e os dados fictícios fornecidos. Não envie mensagens, crie repositórios remotos ou configure agendamentos. Registre apenas ações e perguntas realmente realizadas. Ao concluir, mostre os arquivos que salvou.\n'
    (workspace/'TASK.md').write_text(task)
    baseline = {str(p.relative_to(workspace)):digest(p) for p in workspace.rglob('*') if p.is_file()}
    manifest = dict(case=case_name,lesson=inputs['lesson'],skill=inputs['skill'],baseline=baseline,expected=expected)
    (destination/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    rubric = '\n'.join(f'- {key}: {criterion}' for key,criterion in expected['rubric'])
    judge = '# Revisão em outra sessão\n\nAbra esta pasta de execução como projeto de revisão. A execução usa somente workspace/; o gabarito fica fora dela.\n\nLeia manifest.json, a conversa real da execução quando disponível e os arquivos produzidos em workspace/. Compare o resultado com as fontes, sem corrigir os arquivos do executor. Não aceite um relato de sucesso como prova da ação.\n\n'+rubric+'\n\nSalve review.json com este formato: {"reviewer":"identificação da sessão ou pessoa", "criteria":[{"id":"identificador acima", "status":"pass|fail|needs_evidence", "evidence":["workspace/caminho-do-arquivo"], "reason":"evidência e motivo"}]}. Use needs_evidence quando faltar a conversa ou prova suficiente. Não marque pass sem suporte concreto.\n'
    (destination/'REVIEW.md').write_text(judge)
    return workspace


def check(run, review=None):
    run = Path(run).resolve();workspace = run/'workspace'
    manifest = json.loads((run/'manifest.json').read_text())
    checks = []
    for rule in manifest['expected']['checks']:
        path = under(workspace, rule['path']);kind=rule['kind'];passed=False
        if kind == 'exists':passed=path.is_file() and bool(path.read_text().strip())
        elif kind == 'unchanged':passed=path.is_file() and digest(path)==manifest['baseline'].get(rule['path'])
        elif kind == 'modified':passed=path.is_file() and digest(path)!=manifest['baseline'].get(rule['path']) and bool(path.read_text().strip())
        elif kind == 'json_equal':
            try:passed=json.loads(path.read_text()).get(rule['field'])==rule['value']
            except (OSError,ValueError,AttributeError):passed=False
        else:raise ValueError(f'Unknown check: {kind}')
        checks.append(dict(check=kind,path=rule['path'],passed=passed))
    expected_ids = {item[0] for item in manifest['expected']['rubric']}
    semantic = []
    if review:
        data=json.loads(Path(review).read_text())
        if not data.get('reviewer'):raise ValueError('Review needs a reviewer identity')
        entries=data.get('criteria',[])
        if len(entries)!=len(expected_ids) or {x['id'] for x in entries}!=expected_ids:
            raise ValueError('Review must address each criterion exactly once')
        for entry in entries:
            if entry['status'] not in ('pass','fail','needs_evidence') or not entry.get('reason'):
                raise ValueError('Invalid review status or missing rationale')
            if entry['status']=='pass':
                if not entry.get('evidence') or not all(under(run,name).is_file() for name in entry['evidence']):
                    raise ValueError('Passing criteria need existing evidence within the run')
                if any(name in ('manifest.json','REVIEW.md','review.json','report.json') for name in entry['evidence']):
                    raise ValueError('The rubric or self-score is not execution evidence')
        semantic=entries
    failed = any(not x['passed'] for x in checks) or any(x['status']=='fail' for x in semantic)
    complete = len(semantic)==len(expected_ids) and all(x['status']=='pass' for x in semantic)
    status = 'failed' if failed else ('accepted' if complete else 'pending_review')
    report=dict(case=manifest['case'],lesson=manifest['lesson'],status=status,automated=checks,review=semantic,limitation='Artifact checks do not prove semantic correctness or independent execution. Review the real conversation when a criterion depends on interaction.')
    (run/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    return report


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);sub=parser.add_subparsers(dest='command',required=True)
    p=sub.add_parser('prepare');p.add_argument('case');p.add_argument('--destination',required=True)
    p=sub.add_parser('check');p.add_argument('run');p.add_argument('--review')
    args=parser.parse_args()
    try:
        if args.command=='prepare':print('Open this folder in a separate execution session:',prepare(args.case,args.destination))
        else:
            result=check(args.run,args.review);print(json.dumps(result,ensure_ascii=False,indent=2));sys.exit(0 if result['status']=='accepted' else 1)
    except (OSError,ValueError,KeyError) as exc:parser.exit(2,str(exc)+'\n')
