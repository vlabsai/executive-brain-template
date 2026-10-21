"""Validate template integrity, or configuration readiness with --configured."""
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
import argparse
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ('brain-context', 'brain-curate', 'brain-query', 'brain-briefing', 'brain-automate')
REQUIRED = ['AGENTS.md', 'START_HERE.md', 'profile/overview.md', 'sources/catalog.md',
            'inbox/README.md', 'knowledge/README.md', 'commitments/source-map.md',
            'routines/answer-from-base.md', 'routines/curate-inbox.md',
            'routines/daily-briefing.md', 'routines/setup-automation.md',
            'runs/README.md', 'quality/acceptance.md', 'quality/query-checks.md',
            'templates/source-note.md', 'templates/run-log.md', 'quality/workflow-checks.md']


def validate(configured=False, root=ROOT):
    root = Path(root).resolve()
    errors = [f'Missing {name}' for name in REQUIRED if not (root/name).is_file()]
    for name in SKILLS:
        folder = root/'.agents/skills'/name
        manifest = folder/'SKILL.md'
        if not manifest.is_file() or not (folder/'agents/openai.yaml').is_file():
            errors.append(f'Missing skill or UI metadata: {name}')
            continue
        header = re.match(r'\A---\n(.*?)\n---\n', manifest.read_text(), re.S)
        if not header or not re.search(r'^name: '+re.escape(name)+r'$', header[1], re.M) or not re.search(r'^description: .+', header[1], re.M):
            errors.append(f'Invalid skill metadata: {name}')
        if '[TODO' in manifest.read_text():
            errors.append(f'Unfinished skill scaffold: {name}')
    for path in root.rglob('*.md'):
        if '.git' in path.parts:
            continue
        for target in re.findall(r'\]\(([^)]+)\)', path.read_text()):
            if target.startswith(('https://', '#', 'mailto:')):
                continue
            resolved = (path.parent/target.split('#')[0]).resolve()
            if not resolved.is_relative_to(root) or not resolved.exists():
                errors.append(f'Invalid local link in {path.relative_to(root)}: {target}')
    try:
        brain = json.loads((root/'config/brain.json').read_text())
        registry = json.loads((root/'config/sources.json').read_text())
        sources = registry['sources']
    except (OSError, ValueError, KeyError) as exc:
        return errors+[f'Invalid configuration: {exc}']
    if not isinstance(brain, dict):
        return errors+['brain configuration must be an object']
    if brain.get('schema_version') != 1 or brain.get('state') not in ('template', 'configured'):
        errors.append('Invalid brain schema version or state')
    if brain.get('automation_state') not in ('not_configured', 'scheduled', 'observed'):
        errors.append('Invalid automation state')
    if not isinstance(sources, list):
        return errors+['sources must be a list']
    valid_sources = [s for s in sources if isinstance(s, dict)]
    ids = set()
    for source in sources:
        required = ['id', 'type', 'purpose', 'locator', 'authority', 'refresh', 'enabled', 'authorized', 'access_verified_at']
        if not isinstance(source, dict) or any(key not in source for key in required):
            errors.append('Source is missing required fields')
            continue
        sid = source['id']
        if not isinstance(sid, str) or not re.fullmatch(r'[A-Za-z0-9_-]+', sid) or sid in ids:
            errors.append('Source IDs must be unique, nonempty identifiers')
        ids.add(str(sid))
        if source['type'] not in ('document', 'meeting', 'message', 'calendar', 'tasks'):
            errors.append(f'Invalid source type: {sid}')
        if type(source['enabled']) is not bool or type(source['authorized']) is not bool:
            errors.append(f'Source flags must be booleans: {sid}')
        if source['enabled']:
            if source['authorized'] is not True or not all(source[key] for key in ['purpose', 'locator', 'authority', 'refresh']):
                errors.append(f'Enabled source lacks permission or context: {sid}')
            try:
                datetime.fromisoformat(source['access_verified_at'])
            except (ValueError, TypeError):
                errors.append(f'Enabled source needs a real ISO access date: {sid}')
    for key, kind in [('calendar_source_id', 'calendar'), ('tasks_source_id', 'tasks')]:
        if brain.get(key) is not None and not any(s.get('id') == brain[key] and s.get('type') == kind and s.get('enabled') is True for s in valid_sources):
            errors.append(f'{key} must reference an enabled {kind} source')
    if brain.get('timezone'):
        try:
            ZoneInfo(brain['timezone'])
        except (ZoneInfoNotFoundError, TypeError):
            errors.append('Invalid IANA timezone')
    if configured:
        if brain.get('state') != 'configured':
            errors.append('Project is still a template')
        for key in ('project_name', 'executive_goal', 'timezone'):
            if not brain.get(key):
                errors.append(f'Configure {key}')
        if not any(s.get('enabled') is True for s in valid_sources):
            errors.append('Configure at least one authorized source with verified access')
    return errors


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--configured', action='store_true')
    errors = validate(parser.parse_args().configured)
    for error in errors:
        print('ERROR:', error)
    if errors:
        sys.exit(1)
    print('Configuration structure valid.' if '--configured' in sys.argv else 'Template structure valid; runtime access is not tested.')
