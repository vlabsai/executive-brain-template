"""Check framework boundaries and isolated fictional examples."""
from pathlib import Path
import json
import shutil
import tempfile
import unittest

from validate import ROOT, validate
from ensaio import prepare


class FrameworkTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)/'brain'
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns('.git', '.local', '__pycache__'))

    def test_starting_framework_is_valid(self):
        self.assertEqual(validate(self.root), [])

    def test_missing_required_skill_is_detected(self):
        (self.root/'.agents/skills/brain-query/SKILL.md').unlink()
        self.assertTrue(any('Missing skill' in e for e in validate(self.root)))

    def test_raw_sources_and_executive_notes_do_not_break_framework_checks(self):
        for name in ('.local/raw/source.md', 'inbox/source.md', 'knowledge/note.md', 'knowledge/perfil.md'):
            path = self.root/name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('[Original reference](missing-export.md)')
        self.assertEqual(validate(self.root), [])

    def test_broken_framework_reference_is_detected(self):
        path = self.root/'README.md'
        path.write_text(path.read_text()+'\n[Missing](missing.md)\n')
        self.assertTrue(any('Invalid local link' in e for e in validate(self.root)))

    def test_skill_reference_cannot_escape_project(self):
        path = self.root/'.agents/skills/brain-query/SKILL.md'
        path.write_text(path.read_text()+'\n[Outside](../../../../outside.md)\n')
        self.assertTrue(any('Invalid local link' in e for e in validate(self.root)))

    def test_example_does_not_copy_personal_context_or_notes(self):
        (self.root/'knowledge').mkdir()
        (self.root/'knowledge/perfil.md').write_text('PRIVATE_CLIENT_CANARY')
        (self.root/'knowledge/private.md').write_text('PRIVATE_CLIENT_CANARY')
        target = prepare('contexto-inicial', Path(self.temp.name)/'example', self.root)
        self.assertFalse(any('PRIVATE_CLIENT_CANARY' in p.read_text() for p in target.rglob('*') if p.is_file()))
        self.assertFalse((target/'evals').exists())
        self.assertFalse((target/'contexto.md').exists())
        self.assertFalse((target/'knowledge/perfil.md').exists())
        self.assertTrue((target/'inbox/relato-inicial.md').is_file())

    def test_existing_attempt_is_preserved(self):
        target = Path(self.temp.name)/'example'
        prepare('contexto-inicial', target, self.root)
        with self.assertRaises(FileExistsError):
            prepare('contexto-inicial', target, self.root)

    def test_each_example_carries_its_human_checkpoints(self):
        for name in ('contexto-inicial', 'prazo-em-conflito', 'consulta-sem-orcamento'):
            target = prepare(name, Path(self.temp.name)/name, self.root)
            case = json.loads((self.root/'evals'/(name+'.json')).read_text())
            task = (target/'TASK.md').read_text()
            self.assertTrue(all(point in task for point in case['checks']))

    def test_example_cannot_write_outside_its_working_folder(self):
        path = self.root/'evals/contexto-inicial.json'
        case = json.loads(path.read_text())
        case['files'] = {'../outside.md': 'Unexpected write'}
        path.write_text(json.dumps(case))
        self.assertTrue(validate(self.root))
        with self.assertRaises(ValueError):
            prepare('contexto-inicial', Path(self.temp.name)/'example', self.root)
        self.assertFalse((Path(self.temp.name)/'outside.md').exists())


if __name__ == '__main__':
    unittest.main()
