"""Prepare a small fictional example, without copying the executive's content."""
from pathlib import Path
import argparse
import json
import shutil
import uuid

ROOT = Path(__file__).resolve().parents[1]
CASES = ('contexto-inicial', 'prazo-em-conflito', 'consulta-sem-orcamento')


def prepare(case_name, destination=None, root=ROOT):
    root = Path(root).resolve()
    if case_name not in CASES:
        raise ValueError('Unknown example')
    case = json.loads((root/'evals'/(case_name+'.json')).read_text())
    # Validate file destinations before creating anything.
    for name in case['files']:
        path = Path(name)
        if not path.parts or path.is_absolute() or '..' in path.parts or path.parts[0] not in ('inbox', 'knowledge'):
            raise ValueError('Example source must stay in inbox or knowledge')
    target = Path(destination).resolve() if destination else root/'.local/ensaios'/(case_name+'-'+uuid.uuid4().hex[:8])
    target.mkdir(parents=True, exist_ok=False)
    shutil.copyfile(root/'AGENTS.md', target/'AGENTS.md')
    shutil.copytree(root/'.agents/skills', target/'.agents/skills')
    seeds = {
        'README.md': '# Ensaio fictício\n\nLeia TASK.md. Use apenas os dados fictícios desta pasta.\n',
        'TASK.md': '# '+case['title']+'\n\n'+case['prompt']+'\n\nTrabalhe somente nesta pasta. Mostre os arquivos realmente salvos ou a resposta da consulta. A pessoa fará a conferência; não dê uma nota automática ao próprio resultado.\n\n## Conferência humana\n\n'+''.join('- '+point+'\n' for point in case['checks']),
    }
    for folder in ('inbox', 'knowledge'):
        (target/folder).mkdir()
    for name, text in (seeds | case['files']).items():
        path = target/name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
    return target


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('case', choices=CASES)
    parser.add_argument('--destination')
    args = parser.parse_args()
    print(prepare(args.case, args.destination))
