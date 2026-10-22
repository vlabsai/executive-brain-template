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

    def invoke(self, stage=''):
        env = os.environ.copy()
        env.update(FAIL_STAGE=stage, INDEX_PATH='/unrelated/private.sqlite', QMD_CONFIG_DIR='/unrelated/config')
        result = subprocess.run([sys.executable, 'scripts/search.py', 'search', 'atendimento entre equipes'],
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


if __name__ == '__main__':
    unittest.main()
