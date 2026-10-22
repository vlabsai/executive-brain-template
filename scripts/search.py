"""Run the pinned QMD CLI with a private, rebuildable index for this copy."""
from pathlib import Path
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
VERSION = '2.8.3'
MODEL_FILE = 'hf_ggml-org_embeddinggemma-300M-Q8_0.gguf'
MODEL_BYTES = 333590944


def environment(root):
    state = root/'.local/search'
    env = os.environ.copy()
    # Explicit --index prevents adoption of an unrelated parent .qmd project.
    env['INDEX_PATH'] = str(state/'index.sqlite')
    env['QMD_CONFIG_DIR'] = str(state/'config')
    env['XDG_CACHE_HOME'] = str(state/'cache')
    env['npm_config_cache'] = str(state/'npm-cache')
    # The tested defaults, not a model override inherited from another project.
    for name in ('QMD_EMBED_MODEL', 'QMD_GENERATE_MODEL', 'QMD_RERANK_MODEL'):
        env.pop(name, None)
    return env


def configure(root, directory=None, knowledge=None):
    directory = directory or root/'.local/search/config'
    directory.mkdir(parents=True, exist_ok=True)
    config = {'collections': {'knowledge': {
        'path': str(knowledge or root/'knowledge'), 'pattern': '**/*.md',
        'ignore': ['README.md', '**/README.md'],
        'context': {'/': 'Conhecimento revisado; confira a nota atual e sua origem.'},
    }}}
    # JSON is valid YAML; no Python dependency or second registry is needed.
    (directory/'brain.yml').write_text(json.dumps(config, ensure_ascii=False, indent=2)+'\n')


def run(root, arguments, maintenance=False, env=None, capture=False):
    executable = root/'.local/search/node_modules/.bin/qmd'
    if not executable.is_file():
        raise RuntimeError('Busca não preparada. Execute: python3 scripts/search.py setup')
    result = subprocess.run([str(executable), '--index', 'brain', *arguments],
                            cwd=root, env=env or environment(root), text=True,
                            stdout=subprocess.PIPE if capture else sys.stderr if maintenance else None)
    if result.returncode:
        raise RuntimeError(f'QMD falhou ({result.returncode}); não use resultados antigos.')
    return result.stdout


def refresh(root, semantic=True):
    # Do not return cached content when scanning or embedding fails.
    run(root, ['update'], maintenance=True)
    if semantic:
        run(root, ['embed'], maintenance=True)


def prerequisites():
    errors = []
    if sys.version_info < (3, 10):
        errors.append('Python 3.10 ou superior')
    if not shutil.which('node'):
        errors.append('Node 22 ou superior')
    else:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        try:
            major = int(result.stdout.strip().removeprefix('v').split('.')[0])
        except ValueError:
            major = 0
        if result.returncode or major < 22:
            errors.append('Node 22 ou superior')
    if not shutil.which('npm'):
        errors.append('npm')
    return errors


def installed(root):
    state = root/'.local/search'
    try:
        version = json.loads((state/'node_modules/@tobilu/qmd/package.json').read_text())['version']
        return version == VERSION and (state/'node_modules/.bin/qmd').is_file()
    except (OSError, ValueError, KeyError):
        return False


def readiness(root):
    """Read actual local resources; do not maintain a separate ready flag."""
    issues = prerequisites()
    state = root/'.local/search'
    if not installed(root):
        issues.append('QMD '+VERSION)
    model = state/'cache/qmd/models'/MODEL_FILE
    try:
        with model.open('rb') as source:
            valid = source.read(4) == b'GGUF' and model.stat().st_size == MODEL_BYTES
    except OSError:
        valid = False
    if not valid:
        issues.append('Modelo de embeddings completo')
    try:
        with (state/'index.sqlite').open('rb') as source:
            indexed = source.read(16) == b'SQLite format 3\x00'
    except OSError:
        indexed = False
    if not indexed or not (state/'config/brain.yml').is_file():
        issues.append('Índice e configuração desta cópia')
    return {'ready': not issues, 'pending': issues}


def verify_search(root):
    """Load/download the embedding model and exercise retrieval outside real notes."""
    state = root/'.local/search'
    state.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='onboarding-', dir=state) as temporary:
        probe = Path(temporary)
        notes = probe/'knowledge'
        notes.mkdir()
        (notes/'verificacao.md').write_text('# Verificação fictícia\n\nLia revisará o protótipo de exemplo. Registro temporário de teste, sem compromisso real.\n')
        configure(root, probe/'config', notes)
        env = environment(root)
        env['INDEX_PATH'] = str(probe/'index.sqlite')
        env['QMD_CONFIG_DIR'] = str(probe/'config')
        run(root, ['update'], maintenance=True, env=env)
        run(root, ['embed'], maintenance=True, env=env)
        output = run(root, ['query', 'vec: Quem fará a revisão do protótipo de exemplo?',
                            '--no-rerank', '-c', 'knowledge', '-n', '1', '--json', '--full-path'],
                     capture=True, env=env)
        results = json.loads(output)
        if not isinstance(results, list) or not any(str(item.get('file', '')).endswith('/verificacao.md') for item in results if isinstance(item, dict)):
            raise RuntimeError('A busca de verificação não recuperou o registro fictício; onboarding pendente.')


def setup(root, verify=False):
    state = readiness(root)
    if state['ready'] and not verify:
        # Configuration is derived and follows this checkout after moves.
        configure(root)
        return {**state, 'prepared_now': False, 'probe_executed': False}
    missing = prerequisites()
    if missing:
        raise RuntimeError('Pré-requisitos pendentes: '+', '.join(missing)+'. Prepare-os neste executor antes de continuar.')
    if not installed(root):
        subprocess.run(['npm', 'install', '--prefix', str(root/'.local/search'),
                        f'@tobilu/qmd@{VERSION}', '--save-exact', '--no-fund', '--no-audit'],
                       cwd=root, env=environment(root), check=True, stdout=sys.stderr)
    configure(root)
    verify_search(root)
    refresh(root)
    state = readiness(root)
    if not state['ready']:
        raise RuntimeError('Onboarding pendente: '+', '.join(state['pending']))
    return {**state, 'prepared_now': True, 'probe_executed': True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('setup', 'check', 'update', 'status', 'search', 'lexical'))
    parser.add_argument('query', nargs='?')
    parser.add_argument('-n', type=int, default=5)
    parser.add_argument('--verify', action='store_true', help='Repeat the temporary retrieval test during setup.')
    args = parser.parse_args()
    if args.action in ('search', 'lexical') and not args.query:
        parser.error('Informe a pergunta ou os termos de busca.')
    try:
        if args.action == 'check':
            state = readiness(ROOT)
            print(json.dumps(state, ensure_ascii=False))
            return 0 if state['ready'] else 1
        if args.action == 'setup':
            print(json.dumps(setup(ROOT, args.verify), ensure_ascii=False))
            return 0
        configure(ROOT)
        if args.action == 'update':
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
