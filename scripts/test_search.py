"""Check search isolation and fail-closed updates without downloading models."""
from pathlib import Path
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest


class SearchTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='brain search ')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        (self.root/'scripts').mkdir()
        (self.root/'knowledge').mkdir()
        shutil.copyfile(Path(__file__).with_name('search.py'), self.root/'scripts/search.py')
        cli = self.root/'.local/search/node_modules/.bin/qmd'
        cli.parent.mkdir(parents=True)
        cli.write_text('#!'+sys.executable+'''\nimport json, os, sys
from pathlib import Path
root = Path.cwd()
with (root/'calls.jsonl').open('a') as log:
    log.write(json.dumps({'args': sys.argv[1:], 'index': os.environ['INDEX_PATH'], 'config': os.environ['QMD_CONFIG_DIR']})+'\\n')
if sys.argv[3] == os.environ.get('FAIL_STAGE'):
    sys.exit(7)
if sys.argv[3] in ('query', 'search'):
    print('[]')
''')
        cli.chmod(0o755)

    def invoke(self, stage='', action='search', query='atendimento entre equipes', extra=()):
        env = os.environ.copy()
        env.update(FAIL_STAGE=stage, INDEX_PATH='/unrelated/private.sqlite', QMD_CONFIG_DIR='/unrelated/config')
        result = subprocess.run([sys.executable, 'scripts/search.py', action, query, *extra],
                                cwd=self.root, env=env, text=True, capture_output=True)
        calls = [json.loads(line) for line in (self.root/'calls.jsonl').read_text().splitlines()]
        return result, calls

    def test_query_uses_only_this_copy_and_accepted_knowledge(self):
        result, calls = self.invoke()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), [])
        self.assertTrue(all(call['index'] == str(self.root/'.local/search/index.sqlite') for call in calls))
        self.assertTrue(all(call['config'] == str(self.root/'.local/search/config') for call in calls))
        config = json.loads((self.root/'.local/search/config/brain.yml').read_text())
        self.assertEqual(set(config['collections']), {'knowledge'})
        self.assertEqual(config['collections']['knowledge']['path'], str(self.root/'knowledge'))
        self.assertIn('**/README.md', config['collections']['knowledge']['ignore'])
        command = calls[-1]['args']
        self.assertEqual(command[2], 'query')
        self.assertEqual(command[3], 'lex: atendimento entre equipes\nvec: atendimento entre equipes')
        self.assertIn('--no-rerank', command)

    def test_hybrid_preserves_exact_terms_and_full_semantic_question(self):
        result, calls = self.invoke(query='O que ficou decidido?\nE quem conduz?',
                                    extra=('--terms', '"DEC-0742" Atlas'))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(calls[-1]['args'][3],
                         'lex: "DEC-0742" Atlas\nvec: O que ficou decidido? E quem conduz?')
        command = calls[-1]['args']
        self.assertEqual(command[command.index('--intent')+1], 'O que ficou decidido? E quem conduz?')

    def test_explicit_reranking_keeps_both_retrieval_backends(self):
        result, calls = self.invoke(extra=('--rerank',))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn('--no-rerank', calls[-1]['args'])
        self.assertIn('lex:', calls[-1]['args'][3])
        self.assertIn('vec:', calls[-1]['args'][3])

    def test_lexical_lookup_does_not_require_vector_generation(self):
        result, calls = self.invoke(action='lexical', query='CT-8821')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual([call['args'][2] for call in calls], ['update', 'search'])

    def test_failed_scan_prevents_embedding_and_query(self):
        result, calls = self.invoke('update')
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual([call['args'][2] for call in calls], ['update'])
        self.assertEqual(result.stdout, '')

    def test_failed_embedding_prevents_query(self):
        result, calls = self.invoke('embed')
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual([call['args'][2] for call in calls], ['update', 'embed'])
        self.assertEqual(result.stdout, '')

    def test_failed_reranking_does_not_retry_without_reranking(self):
        result, calls = self.invoke('query', extra=('--rerank',))
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual([call['args'][2] for call in calls], ['update', 'embed', 'query'])
        self.assertEqual(result.stdout, '')


if __name__ == '__main__':
    unittest.main()
