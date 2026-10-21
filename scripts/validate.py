"""Check maintained framework files without traversing the executive's notes."""
from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ('start-executive-project', 'brain-curate', 'brain-query')
CASES = ('contexto-inicial', 'prazo-em-conflito', 'consulta-sem-orcamento')
REQUIRED = ('AGENTS.md', 'README.md', 'evals/README.md')


def validate(root=ROOT):
    root = Path(root).resolve()
    errors = [f'Missing {name}' for name in REQUIRED if not (root/name).is_file()]
    documents = [root/name for name in REQUIRED]
    for name in SKILLS:
        folder = root/'.agents/skills'/name
        manifest = folder/'SKILL.md'
        documents.append(manifest)
        if not manifest.is_file() or not (folder/'agents/openai.yaml').is_file():
            errors.append(f'Missing skill or UI metadata: {name}')
            continue
        text = manifest.read_text()
        header = re.match(r'\A---\n(.*?)\n---\n', text, re.S)
        if not header or not re.search(r'^name: '+re.escape(name)+r'$', header[1], re.M) or not re.search(r'^description: .+', header[1], re.M):
            errors.append(f'Invalid skill metadata: {name}')
        if '[TODO' in text:
            errors.append(f'Unfinished skill scaffold: {name}')
    for path in documents:
        if not path.is_file():
            continue
        if not path.resolve().is_relative_to(root):
            errors.append(f'Instruction outside project: {path.relative_to(root)}')
            continue
        for target in re.findall(r'\]\(([^)]+)\)', path.read_text()):
            if target.startswith(('https://', 'http://', '#', 'mailto:')):
                continue
            resolved = (path.parent/target.split('#')[0]).resolve()
            if not resolved.is_relative_to(root) or not resolved.exists():
                errors.append(f'Invalid local link in {path.relative_to(root)}: {target}')
    for name in CASES:
        try:
            case = json.loads((root/'evals'/(name+'.json')).read_text())
            if case['skill'] not in SKILLS or len(case['checks']) != 3 or not case['prompt'] or not case['files']:
                raise ValueError('Invalid example')
            for target in case['files']:
                path = Path(target)
                if not path.parts or '..' in path.parts or path.is_absolute() or path.parts[0] not in ('inbox', 'knowledge'):
                    raise ValueError('Example source must stay in inbox or knowledge')
        except (OSError, ValueError, KeyError, TypeError) as exc:
            errors.append(f'Invalid example {name}: {exc}')
    return errors


if __name__ == '__main__':
    errors = validate()
    for error in errors:
        print('ERROR:', error)
    if errors:
        sys.exit(1)
    print('Framework structure valid. Sources, model behavior and operational access are not tested.')
