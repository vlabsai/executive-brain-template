"""Compare QMD retrieval modes on the packaged fictional case, for authors only."""
from pathlib import Path
import argparse
import importlib.util
import json
import statistics
import time

from preparar_caso import load_case


def compare(workspace, repeats=2):
    root = Path(workspace).resolve()
    case = load_case('navegar-e-buscar')
    # Refuse a real base or an altered fixture; never benchmark private notes.
    if (root/'.git').exists() or not (root/'TASK.md').is_file():
        raise ValueError('Use uma cópia fictícia criada por preparar_caso.py.')
    expected_notes = {name: text for name, text in case['files'].items()
                      if name.startswith('knowledge/')}
    actual_notes = {str(path.relative_to(root)): path.read_text()
                    for path in (root/'knowledge').rglob('*.md') if path.name != 'README.md'}
    if actual_notes != expected_notes:
        raise ValueError('A cópia precisa conter somente as notas fictícias originais do caso.')
    spec = importlib.util.spec_from_file_location('search_helper', root/'scripts/search.py')
    search = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(search)
    search.setup(root)
    search.refresh(root)
    observations = []
    for repeat in range(repeats):
        for query in case['retrieval_queries']:
            # Alternate order to reduce a systematic advantage from warm caches.
            modes = ['vector', 'hybrid', 'rerank']
            if repeat % 2:
                modes.reverse()
            for mode in modes:
                command = (['query', 'vec: '+query['query'], '--no-rerank'] if mode == 'vector'
                           else search.query_arguments(query['query'], query['terms'], mode == 'rerank'))
                command.extend(['-c', 'knowledge', '-n', '3', '--json', '--full-path'])
                start = time.perf_counter()
                results = json.loads(search.run(root, command, capture=True))
                seconds = time.perf_counter()-start
                files = [str(Path(result['file']).relative_to(root)) if Path(result['file']).is_absolute()
                         else str(Path(result['file'])) for result in results]
                rank = next((i+1 for i, name in enumerate(files) if name in query['expected']), None)
                observations.append({'repeat': repeat+1, 'query': query['id'], 'mode': mode,
                                     'seconds': round(seconds, 3), 'first_relevant_rank': rank,
                                     'files': files})
    summary = {}
    for mode in ('vector', 'hybrid', 'rerank'):
        rows = [row for row in observations if row['mode'] == mode]
        summary[mode] = {
            'searches': len(rows),
            'top1': sum(row['first_relevant_rank'] == 1 for row in rows),
            'top3': sum(row['first_relevant_rank'] is not None for row in rows),
            'mrr_at_3': round(statistics.mean(1/row['first_relevant_rank']
                                            if row['first_relevant_rank'] else 0 for row in rows), 3),
            'median_seconds': round(statistics.median(row['seconds'] for row in rows), 3),
            'max_seconds': max(row['seconds'] for row in rows),
        }
    return {'workspace': str(root), 'notes': len(actual_notes), 'queries': len(case['retrieval_queries']),
            'repeats': repeats, 'summary': summary, 'observations': observations,
            'limits': 'Recuperação em um caso sintético pequeno; não avalia resposta final, '
                      'acionamento da skill, escala real ou executor remoto. Tempos incluem '
                      'a abertura do CLI e podem incluir o primeiro download do reranker; '
                      'a atualização do índice foi feita antes das medições.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('workspace', help='Pasta devolvida por preparar_caso.py navegar-e-buscar')
    parser.add_argument('--repeats', type=int, choices=range(1, 6), default=2)
    args = parser.parse_args()
    print(json.dumps(compare(args.workspace, args.repeats), ensure_ascii=False, indent=2))
