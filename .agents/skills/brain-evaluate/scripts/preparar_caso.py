"""Prepare any packaged evaluation case in an isolated local workspace."""
from pathlib import Path
import argparse
import json
import re
import shutil
import uuid

SKILL_DIR = Path(__file__).resolve().parents[1]
ROOT = SKILL_DIR.parents[2]


def case_paths(root=ROOT):
    return sorted((Path(root)/'.agents/skills/brain-evaluate/assets').glob('*.json'))


def load_case(name, root=ROOT):
    if not re.fullmatch(r'[a-z0-9][a-z0-9_-]*', name):
        raise ValueError('Invalid case name')
    root = Path(root).resolve()
    case = json.loads((root/'.agents/skills/brain-evaluate/assets'/(name+'.json')).read_text())
    if not isinstance(case, dict):
        raise ValueError('A case must be a JSON object')
    if any(not isinstance(case.get(key), str) or not case[key].strip() for key in ('title', 'skill', 'prompt')):
        raise ValueError('A case needs title, skill and prompt')
    if not re.fullmatch(r'[a-z0-9][a-z0-9-]*', case['skill']) or not (root/'.agents/skills'/case['skill']/'SKILL.md').is_file():
        raise ValueError('The evaluated skill must exist in this project')
    if not isinstance(case.get('checks'), list) or not case['checks'] or not all(isinstance(c, str) and c.strip() for c in case['checks']):
        raise ValueError('A case needs human checkpoints')
    if not isinstance(case.get('files'), dict) or not case['files']:
        raise ValueError('A case needs fictional source files')
    for name, text in case['files'].items():
        path = Path(name)
        if not path.parts or path.is_absolute() or '..' in path.parts or path.parts[0] in ('.git', '.agents') or name in ('AGENTS.md', 'README.md', 'TASK.md') or not isinstance(text, str):
            raise ValueError('Source files must stay inside the workspace and preserve its instructions')
    return case


def prepare(name, destination=None, root=ROOT):
    root = Path(root).resolve()
    case = load_case(name, root)
    target = Path(destination).resolve() if destination else root/'.local/ensaios'/(name+'-'+uuid.uuid4().hex[:8])
    target.mkdir(parents=True, exist_ok=False)
    shutil.copyfile(root/'AGENTS.md', target/'AGENTS.md')
    skill_path = Path('.agents/skills')/case['skill']
    shutil.copytree(root/skill_path, target/skill_path)
    for folder in ('inbox', 'knowledge'):
        (target/folder).mkdir()
        shutil.copyfile(root/folder/'README.md', target/folder/'README.md')
    seeds = {
        'README.md': '# Ensaio fictício\n\nLeia TASK.md. Use somente os dados fictícios desta pasta.\n',
        'TASK.md': '# '+case['title']+'\n\n'+case['prompt']+'\n\nTrabalhe somente nesta pasta. Mostre o resultado realmente produzido. A conferência é humana; não dê uma nota automática ao próprio resultado.\n\n## Pontos de conferência\n\n'+''.join('- '+point+'\n' for point in case['checks']),
    }
    for filename, text in (seeds | case['files']).items():
        path = target/filename
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
    return target


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('case', nargs='?')
    parser.add_argument('--list', action='store_true')
    parser.add_argument('--destination')
    args = parser.parse_args()
    try:
        if args.list:
            print('\n'.join(path.stem+': '+load_case(path.stem)['title'] for path in case_paths()))
        elif args.case:
            print(prepare(args.case, args.destination))
        else:
            parser.error('Choose a case or use --list')
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.exit(2, str(exc)+'\n')
