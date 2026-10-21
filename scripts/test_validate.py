"""Exercise source-readiness boundaries using isolated synthetic copies."""
from pathlib import Path
import json
import shutil
import tempfile
import unittest

from validate import ROOT, validate


class ReadinessTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)/'brain'
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns('.git', '__pycache__', '.local'))

    def write(self, name, value):
        (self.root/name).write_text(json.dumps(value))

    def source(self, **changes):
        item = dict(id='S01', type='document', purpose='Synthetic test', locator='inbox/test.md',
                    authority='Project facts', refresh='Review origin on changes',
                    enabled=True, authorized=True, access_verified_at='2026-10-21T10:00:00-03:00')
        item.update(changes)
        self.write('config/sources.json', dict(schema_version=1, sources=[item]))

    def test_empty_template_is_valid_but_not_ready(self):
        self.assertEqual(validate(root=self.root), [])
        self.assertTrue(validate(configured=True, root=self.root))

    def test_enabled_source_needs_permission_and_observed_read(self):
        self.source(authorized=False, access_verified_at='')
        errors = validate(root=self.root)
        self.assertTrue(any('permission' in e for e in errors))
        self.assertTrue(any('access date' in e for e in errors))

    def test_calendar_cannot_point_to_document_source(self):
        self.source()
        brain = json.loads((self.root/'config/brain.json').read_text())
        brain['calendar_source_id'] = 'S01'
        self.write('config/brain.json', brain)
        self.assertTrue(any('enabled calendar' in e for e in validate(root=self.root)))

    def test_configured_snapshot_passes_structure_without_claiming_live_access(self):
        self.source()
        brain = json.loads((self.root/'config/brain.json').read_text())
        brain.update(state='configured', project_name='Synthetic', executive_goal='Find decisions', timezone='America/Sao_Paulo')
        self.write('config/brain.json', brain)
        self.assertEqual(validate(configured=True, root=self.root), [])

    def test_skill_reference_cannot_escape_client_repository(self):
        manifest = self.root/'.agents/skills/brain-query/SKILL.md'
        manifest.write_text(manifest.read_text()+'\n[Outside](../../../../outside.md)\n')
        self.assertTrue(any('Invalid local link' in e for e in validate(root=self.root)))


if __name__ == '__main__':
    unittest.main()
