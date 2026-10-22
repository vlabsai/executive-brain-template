"""Check the framework; optionally check note identities and local links."""
from pathlib import Path
import argparse
import importlib.util
import json
import re
import sys
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ('start-executive-project', 'brain-curate', 'brain-query', 'brain-evaluate')
REQUIRED = ('AGENTS.md', 'README.md', 'inbox/README.md', 'knowledge/README.md',
            *('knowledge/'+name+'/README.md' for name in
              ('empresas', 'pessoas', 'projetos', 'reunioes', 'temas')))


def local_link_errors(path, root):
    if not path.resolve().is_relative_to(root):
        return [f'File outside project: {path.relative_to(root)}']
    errors = []
    prose = re.sub(r'```.*?```|`[^`\n]*`', '', path.read_text(), flags=re.S)
    for target in re.findall(r'\]\(([^)]+)\)', prose):
        if target.startswith(('https://', 'http://', '#', 'mailto:')):
            continue
        resolved = (path.parent/unquote(target.split('#')[0].strip('<>'))).resolve()
        if not resolved.is_relative_to(root) or not resolved.exists():
            errors.append(f'Invalid local link in {path.relative_to(root)}: {target}')
    return errors


def validate_notes(root=ROOT):
    """Check mechanical integrity, without approving facts, domains or sources."""
    root = Path(root).resolve()
    errors, identities = [], {}
    for path in sorted((root/'knowledge').rglob('*.md')):
        if path.name == 'README.md':
            continue
        if not path.resolve().is_relative_to(root):
            errors.append(f'Note outside project: {path.relative_to(root)}')
            continue
        header = re.match(r'\A---\n(.*?)\n---(?:\n|$)', path.read_text(), re.S)
        identity = re.search(r'^id:[ \t]*([^\n]+)$', header[1], re.M) if header else None
        value = identity[1].strip().strip('\"\'') if identity else ''
        if not value:
            errors.append(f'Missing note id: {path.relative_to(root)}')
        elif value in identities:
            errors.append(f'Duplicate note id: {path.relative_to(root)} and {identities[value]}')
        else:
            identities[value] = path.relative_to(root)
        errors.extend(local_link_errors(path, root))
    return errors


def evaluation_module(root=ROOT):
    path = Path(root)/'.agents/skills/brain-evaluate/scripts/preparar_caso.py'
    spec = importlib.util.spec_from_file_location('evaluation_cases', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate(root=ROOT):
    root = Path(root).resolve()
    configurations = ('.obsidian/app.json', '.obsidian/core-plugins.json', '.obsidian/graph.json')
    resources = ('scripts/search.py', '.agents/skills/brain-query/references/search.md', *configurations)
    errors = [f'Missing {name}' for name in (*REQUIRED, *resources) if not (root/name).is_file()]
    for name in configurations:
        if (root/name).is_file():
            try:
                json.loads((root/name).read_text())
            except json.JSONDecodeError as exc:
                errors.append(f'Invalid vault configuration {name}: {exc}')
    documents = [root/name for name in REQUIRED]
    documents.append(root/'.agents/skills/brain-query/references/search.md')
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
        errors.extend(local_link_errors(path, root))
    try:
        evaluations = evaluation_module(root)
        paths = evaluations.case_paths(root)
        if not paths:
            errors.append('Evaluation skill needs a packaged example')
        for path in paths:
            try:
                evaluations.load_case(path.stem, root)
            except (OSError, ValueError, KeyError, TypeError) as exc:
                errors.append(f'Invalid example {path.stem}: {exc}')
    except OSError as exc:
        errors.append(f'Missing evaluation preparer: {exc}')
    return errors


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--notes', action='store_true', help='Also check ids and local links in knowledge/.')
    args = parser.parse_args()
    errors = validate()
    if args.notes:
        errors.extend(validate_notes())
    for error in errors:
        print('ERROR:', error)
    if errors:
        sys.exit(1)
    print('Framework'+(' and note integrity' if args.notes else '')+' valid. Facts, domains, model behavior and operational access are not tested.')
