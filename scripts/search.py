"""Run the pinned QMD CLI with a private, rebuildable index for this copy."""
from pathlib import Path
import argparse
import json
import os
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
VERSION = '2.8.3'


def environment(root):
    state = root/'.local/search'
    env = os.environ.copy()
    # Explicit --index prevents adoption of an unrelated parent .qmd project.
    env['INDEX_PATH'] = str(state/'index.sqlite')
    env['QMD_CONFIG_DIR'] = str(state/'config')
    env['XDG_CACHE_HOME'] = str(state/'cache')
    # The tested defaults, not a model override inherited from another project.
    for name in ('QMD_EMBED_MODEL', 'QMD_GENERATE_MODEL', 'QMD_RERANK_MODEL'):
        env.pop(name, None)
    return env


def configure(root):
    directory = root/'.local/search/config'
    directory.mkdir(parents=True, exist_ok=True)
    config = {'collections': {'knowledge': {
        'path': str(root/'knowledge'), 'pattern': '**/*.md',
        'ignore': ['README.md', '**/README.md'],
        'context': {'/': 'Conhecimento revisado do executivo; confira a nota atual e sua origem.'},
    }}}
    # JSON is valid YAML; no Python dependency or second registry is needed.
    (directory/'brain.yml').write_text(json.dumps(config, ensure_ascii=False, indent=2)+'\n')


def run(root, arguments, maintenance=False):
    executable = root/'.local/search/node_modules/.bin/qmd'
    if not executable.is_file():
        raise RuntimeError('Busca não preparada. Execute: python3 scripts/search.py setup')
    result = subprocess.run([str(executable), '--index', 'brain', *arguments],
                            cwd=root, env=environment(root),
                            stdout=sys.stderr if maintenance else None)
    if result.returncode:
        raise RuntimeError(f'QMD falhou ({result.returncode}); não use resultados antigos.')


def refresh(root, semantic=True):
    # Do not return cached content when scanning or embedding fails.
    run(root, ['update'], maintenance=True)
    if semantic:
        run(root, ['embed'], maintenance=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('setup', 'update', 'status', 'search', 'lexical'))
    parser.add_argument('query', nargs='?')
    parser.add_argument('-n', type=int, default=5)
    args = parser.parse_args()
    if args.action in ('search', 'lexical') and not args.query:
        parser.error('Informe a pergunta ou os termos de busca.')
    try:
        if args.action == 'setup':
            subprocess.run(['npm', 'install', '--prefix', str(ROOT/'.local/search'),
                            f'@tobilu/qmd@{VERSION}', '--save-exact', '--no-fund', '--no-audit'],
                           cwd=ROOT, check=True, stdout=sys.stderr)
        configure(ROOT)
        if args.action in ('setup', 'update'):
            refresh(ROOT)
        elif args.action == 'status':
            run(ROOT, ['status'])
        else:
            semantic = args.action == 'search'
            refresh(ROOT, semantic)
            # vsearch in 2.8.3 also loads the expansion LLM. A typed vector
            # query avoids that download and reranking for this small path.
            query = 'vec: '+args.query.replace('\n', ' ') if semantic else args.query
            command = ['query', query, '--no-rerank'] if semantic else ['search', query]
            run(ROOT, [*command, '-c', 'knowledge', '-n', str(args.n),
                       '--json', '--full-path'])
    except (OSError, RuntimeError, subprocess.CalledProcessError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
