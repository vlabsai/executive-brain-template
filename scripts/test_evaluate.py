"""Check isolation, artifact integrity and honest evaluation states."""
from pathlib import Path
import json
import shutil
import tempfile
import unittest
from evaluate import ROOT, prepare, check


class EvaluationTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)

    def test_private_client_data_and_expected_answers_are_not_copied(self):
        source=self.root/'source'
        shutil.copytree(ROOT,source,ignore=shutil.ignore_patterns('.git','__pycache__','.local'))
        for name in ('profile/overview.md','config/brain.json','config/sources.json'):
            (source/name).write_text('PRIVATE_CLIENT_CANARY')
        workspace=prepare('contexto-inicial',self.root/'run',source)
        self.assertFalse(any('PRIVATE_CLIENT_CANARY' in p.read_text() for p in workspace.rglob('*') if p.is_file()))
        self.assertFalse((workspace/'evals').exists())
        self.assertFalse((workspace/'manifest.json').exists())
        self.assertTrue((workspace/'.agents/skills/brain-context/SKILL.md').is_file())

    def test_preparation_alone_does_not_pass(self):
        prepare('consulta-sem-orcamento',self.root/'run')
        self.assertEqual(check(self.root/'run')['status'],'failed')

    def test_artifacts_without_review_remain_pending(self):
        w=prepare('prazo-em-conflito',self.root/'run')
        (w/'inbox/atualizacao-proposta.md').write_text('Synthetic proposal for validator test')
        (w/'runs/curadoria-do-exercicio.md').write_text('Synthetic record for validator test')
        self.assertEqual(check(self.root/'run')['status'],'pending_review')
        (w/'knowledge/projects/alfa.md').write_text('The confirmed note was overwritten')
        result=check(self.root/'run')
        self.assertEqual(result['status'],'failed')
        self.assertTrue(any(not x['passed'] and x['check']=='unchanged' for x in result['automated']))

    def test_rubric_cannot_be_used_as_passing_execution_evidence(self):
        prepare('consulta-sem-orcamento',self.root/'run')
        manifest=json.loads((self.root/'run/manifest.json').read_text())
        review=dict(reviewer='Synthetic judge fixture',criteria=[dict(id=k,status='pass',reason='Fixture',evidence=['manifest.json']) for k,_ in manifest['expected']['rubric']])
        path=self.root/'run/review.json';path.write_text(json.dumps(review))
        with self.assertRaises(ValueError):check(self.root/'run',path)

    def test_existing_run_cannot_be_replaced(self):
        prepare('contexto-inicial',self.root/'run')
        with self.assertRaises(ValueError):prepare('contexto-inicial',self.root/'run')


if __name__=='__main__':unittest.main()
