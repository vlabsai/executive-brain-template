"""Check framework boundaries and isolated fictional examples."""
from pathlib import Path
import json
import shutil
import tempfile
import unittest

from validate import ROOT, validate, validate_notes, evaluation_module

evaluations = evaluation_module()
prepare = evaluations.prepare


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

    def test_note_check_accepts_links_and_detects_missing_target(self):
        note = self.root/'knowledge/check.md'
        source = self.root/'inbox/source with spaces.txt'
        source.write_text('Fictional source')
        note.write_text('---\nid: stable-note\ndomains: [example]\n---\n[Source](../inbox/source%20with%20spaces.txt)\n')
        self.assertEqual(validate_notes(self.root), [])
        source.unlink()
        self.assertTrue(any('Invalid local link' in e for e in validate_notes(self.root)))

    def test_note_check_detects_missing_and_duplicate_identity(self):
        first = self.root/'knowledge/check.md'
        first.write_text('# Note without identity\n')
        self.assertTrue(any('Missing note id' in e for e in validate_notes(self.root)))
        first.write_text('---\nid: stable-note\ndomains: [example]\n---\n# Fictional note\n')
        second = self.root/'knowledge/other.md'
        second.write_text(first.read_text())
        self.assertTrue(any('Duplicate note id' in e for e in validate_notes(self.root)))

    def test_note_check_preserves_identity_after_move_and_blocks_escaped_link(self):
        first = self.root/'knowledge/check.md'
        first.write_text('---\nid: stable-note\ndomains: [example]\n---\n# Fictional note\n')
        first.rename(self.root/'knowledge/projetos/moved.md')
        self.assertEqual(validate_notes(self.root), [])
        outside = Path(self.temp.name)/'outside.md'
        outside.write_text('Outside the Brain')
        moved = self.root/'knowledge/projetos/moved.md'
        moved.write_text(moved.read_text()+'\n[Outside](../../../outside.md)\n')
        self.assertTrue(any('Invalid local link' in e for e in validate_notes(self.root)))

    def test_example_does_not_copy_personal_context_or_notes(self):
        (self.root/'knowledge').mkdir(exist_ok=True)
        (self.root/'knowledge/perfil.md').write_text('PRIVATE_CLIENT_CANARY')
        (self.root/'knowledge/private.md').write_text('PRIVATE_CLIENT_CANARY')
        (self.root/'knowledge/private-company').mkdir()
        (self.root/'knowledge/private-company/README.md').write_text('PRIVATE_CLIENT_CANARY')
        (self.root/'.local').mkdir(exist_ok=True)
        (self.root/'.local/private.txt').write_text('PRIVATE_CLIENT_CANARY')
        target = prepare('montar-contexto', Path(self.temp.name)/'example', self.root)
        self.assertFalse(any('PRIVATE_CLIENT_CANARY' in p.read_text() for p in target.rglob('*') if p.is_file()))
        self.assertFalse((target/'evals').exists())
        self.assertFalse((target/'.agents/skills/brain-evaluate').exists())
        self.assertTrue((target/'.agents/skills/brain-onboarding/SKILL.md').is_file())
        self.assertTrue((target/'inbox/README.md').is_file())
        self.assertTrue((target/'knowledge/README.md').is_file())
        self.assertTrue((target/'knowledge/empresas/README.md').is_file())
        self.assertFalse((target/'.local').exists())
        self.assertFalse((target/'knowledge/private-company').exists())
        self.assertFalse((target/'contexto.md').exists())
        self.assertFalse((target/'knowledge/perfil.md').exists())
        self.assertTrue((target/'inbox/relato-inicial.md').is_file())

    def test_existing_attempt_is_preserved(self):
        target = Path(self.temp.name)/'example'
        prepare('montar-contexto', target, self.root)
        with self.assertRaises(FileExistsError):
            prepare('montar-contexto', target, self.root)

    def test_conversation_case_starts_empty_and_keeps_operator_replies_outside_executor(self):
        target = prepare('conversar-contexto', Path(self.temp.name)/'conversation', self.root)
        case = evaluations.load_case('conversar-contexto', self.root)
        self.assertEqual(case['files'], {})
        self.assertFalse((target/'knowledge/perfil.md').exists())
        self.assertFalse((target/'inbox/perfil-proposto.md').exists())
        self.assertFalse((target/'inbox/relato-inicial.md').exists())
        task = (target/'TASK.md').read_text()
        self.assertIn(case['prompt'], task)
        self.assertTrue(all(reply not in task for reply in case['author_replies']))

    def test_each_example_carries_its_human_checkpoints(self):
        for path in evaluations.case_paths(self.root):
            name = path.stem
            target = prepare(name, Path(self.temp.name)/name, self.root)
            case = evaluations.load_case(name, self.root)
            task = (target/'TASK.md').read_text()
            self.assertTrue(all(point in task for point in case['checks']))

    def test_example_cannot_write_outside_its_working_folder(self):
        path = self.root/'.agents/skills/brain-evaluate/assets/montar-contexto.json'
        case = json.loads(path.read_text())
        case['files'] = {'../outside.md': 'Unexpected write'}
        path.write_text(json.dumps(case))
        self.assertTrue(validate(self.root))
        with self.assertRaises(ValueError):
            prepare('montar-contexto', Path(self.temp.name)/'example', self.root)
        self.assertFalse((Path(self.temp.name)/'outside.md').exists())

    def test_new_case_needs_no_code_registration_or_context_specific_paths(self):
        skill = self.root/'.agents/skills/outro-fluxo'
        skill.mkdir()
        (skill/'SKILL.md').write_text('---\nname: outro-fluxo\ndescription: Another workflow.\n---\nRead the supplied example.\n')
        path = self.root/'.agents/skills/brain-evaluate/assets/outro-fluxo.json'
        path.write_text(json.dumps(dict(title='Another flow', skill='outro-fluxo', prompt='Read the fictional document.', files={'documents/example.txt':'Synthetic input'}, checks=['Uses the supplied source.'])))
        self.assertEqual(validate(self.root), [])
        target = prepare('outro-fluxo', Path(self.temp.name)/'new-example', self.root)
        self.assertEqual((target/'documents/example.txt').read_text(), 'Synthetic input')
        self.assertTrue((target/'.agents/skills/outro-fluxo/SKILL.md').is_file())


if __name__ == '__main__':
    unittest.main()
