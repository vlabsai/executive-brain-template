"""Check onboarding reuse, failure boundaries and isolation without network access."""
from pathlib import Path
import json
import tempfile
import unittest
from unittest.mock import patch

import search


class OnboardingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='brain onboarding ')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root/'knowledge').mkdir()
        self.note = self.root/'knowledge/accepted.md'
        self.note.write_text('PRIVATE_ACCEPTED_NOTE')
        self.addCleanup(patch.stopall)
        patch.object(search, 'prerequisites', side_effect=lambda: []).start()

    def resources(self):
        state = self.root/'.local/search'
        package = state/'node_modules/@tobilu/qmd/package.json'
        package.parent.mkdir(parents=True, exist_ok=True)
        package.write_text(json.dumps({'version': search.VERSION}))
        cli = state/'node_modules/.bin/qmd'
        cli.parent.mkdir(parents=True, exist_ok=True)
        cli.write_text('fixture, not executed')
        model = state/'cache/qmd/models'/search.MODEL_FILE
        model.parent.mkdir(parents=True, exist_ok=True)
        with model.open('wb') as output:
            output.write(b'GGUF')
            output.seek(search.MODEL_BYTES-1)
            output.write(b'\0')
        (state/'index.sqlite').write_bytes(b'SQLite format 3\0')
        search.configure(self.root)
        return model

    def test_ready_resources_skip_install_download_and_probe(self):
        model = self.resources()
        before = model.stat().st_mtime_ns
        with patch.object(search.subprocess, 'run') as process, patch.object(search, 'verify_search') as probe:
            result = search.setup(self.root)
        self.assertTrue(result['ready'])
        self.assertFalse(result['prepared_now'])
        process.assert_not_called()
        probe.assert_not_called()
        self.assertEqual(model.stat().st_mtime_ns, before)
        self.assertEqual(self.note.read_text(), 'PRIVATE_ACCEPTED_NOTE')

    def test_truncated_model_cannot_be_reported_ready(self):
        model = self.resources()
        model.write_bytes(b'GGUF')
        result = search.readiness(self.root)
        self.assertFalse(result['ready'])
        self.assertIn('Modelo de embeddings completo', result['pending'])

    def test_dependency_failure_does_not_install_or_mutate_notes(self):
        with patch.object(search, 'prerequisites', return_value=['Node 22 ou superior']), patch.object(search.subprocess, 'run') as process:
            with self.assertRaisesRegex(RuntimeError, 'Pré-requisitos pendentes'):
                search.setup(self.root)
        process.assert_not_called()
        self.assertEqual(self.note.read_text(), 'PRIVATE_ACCEPTED_NOTE')

    def test_failed_probe_does_not_index_real_notes_or_declare_ready(self):
        with patch.object(search, 'installed', return_value=True), patch.object(search, 'verify_search', side_effect=RuntimeError('Model unavailable')), patch.object(search, 'refresh') as refresh:
            with self.assertRaisesRegex(RuntimeError, 'Model unavailable'):
                search.setup(self.root)
        refresh.assert_not_called()
        self.assertFalse(search.readiness(self.root)['ready'])
        self.assertEqual(self.note.read_text(), 'PRIVATE_ACCEPTED_NOTE')

    def test_probe_uses_temporary_notes_and_cleans_up_on_bad_result(self):
        environments = []
        def fake_run(root, arguments, **options):
            env = options['env']
            environments.append(env)
            config = json.loads((Path(env['QMD_CONFIG_DIR'])/'brain.yml').read_text())
            notes = Path(config['collections']['knowledge']['path'])
            self.assertNotEqual(notes, self.root/'knowledge')
            self.assertTrue((notes/'verificacao.md').is_file())
            self.assertFalse((notes/'accepted.md').exists())
            return '[{"file":"qmd://knowledge/wrong.md"}]' if options.get('capture') else None
        with patch.object(search, 'run', side_effect=fake_run):
            with self.assertRaisesRegex(RuntimeError, 'não recuperou'):
                search.verify_search(self.root)
        self.assertTrue(environments)
        for env in environments:
            self.assertTrue(Path(env['INDEX_PATH']).is_relative_to(self.root/'.local/search'))
            self.assertEqual(env['XDG_CACHE_HOME'], str(self.root/'.local/search/cache'))
        self.assertFalse(list((self.root/'.local/search').glob('onboarding-*')))
        self.assertEqual(self.note.read_text(), 'PRIVATE_ACCEPTED_NOTE')

    def test_explicit_verification_runs_with_existing_resources(self):
        self.resources()
        with patch.object(search, 'verify_search') as probe, patch.object(search, 'refresh'):
            result = search.setup(self.root, verify=True)
        probe.assert_called_once_with(self.root)
        self.assertTrue(result['probe_executed'])

    def test_fresh_preparation_installs_only_pinned_qmd_with_local_cache(self):
        installs = []
        def install(arguments, **options):
            installs.append((arguments, options))
            self.resources()
        with patch.object(search.subprocess, 'run', side_effect=install), patch.object(search, 'verify_search') as probe, patch.object(search, 'refresh'):
            result = search.setup(self.root)
        self.assertTrue(result['ready'])
        self.assertEqual(len(installs), 1)
        arguments, options = installs[0]
        self.assertIn('@tobilu/qmd@'+search.VERSION, arguments)
        self.assertEqual(options['env']['npm_config_cache'], str(self.root/'.local/search/npm-cache'))
        probe.assert_called_once_with(self.root)

    def test_failed_real_index_after_probe_stays_pending(self):
        self.resources()
        with patch.object(search, 'verify_search'), patch.object(search, 'refresh', side_effect=RuntimeError('Index failed')):
            with self.assertRaisesRegex(RuntimeError, 'Index failed'):
                search.setup(self.root, verify=True)
        self.assertEqual(self.note.read_text(), 'PRIVATE_ACCEPTED_NOTE')


if __name__ == '__main__':
    unittest.main()
