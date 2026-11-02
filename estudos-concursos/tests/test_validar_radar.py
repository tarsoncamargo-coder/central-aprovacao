"""Regressões do contrato de descoberta e integridade do Radar."""
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / 'estudos-concursos/scripts/validar_radar.py'


class RadarTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(SCRIPT.is_file(), 'Validador automático ainda não implementado')
        spec = importlib.util.spec_from_file_location('validar_radar', SCRIPT)
        self.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.module)
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        shutil.copytree(ROOT / '.agents', self.root / '.agents')
        shutil.copytree(ROOT / 'estudos-concursos', self.root / 'estudos-concursos',
                        ignore=shutil.ignore_patterns('__pycache__'))

    def test_catalogo_completo_valido(self):
        self.assertEqual(self.module.validate(self.root), [])

    def test_skill_ausente_e_detectada(self):
        shutil.rmtree(self.root / '.agents/skills/professor-de-concursos')
        self.assertTrue(self.module.validate(self.root))

    def test_nome_incompativel_e_detectado(self):
        path = self.root / '.agents/skills/professor-de-concursos/SKILL.md'
        path.write_text(path.read_text().replace('name: professor-de-concursos', 'name: outro'))
        self.assertTrue(self.module.validate(self.root))

    def test_invocacao_implicita_desativada_e_detectada(self):
        path = self.root / '.agents/skills/professor-de-concursos/agents/openai.yaml'
        path.write_text(path.read_text().replace('allow_implicit_invocation: true',
                                                 'allow_implicit_invocation: false'))
        self.assertTrue(self.module.validate(self.root))

    def test_prompt_removido_e_detectado(self):
        path = self.root / 'estudos-concursos/PROMPTS_PRONTOS.md'
        path.write_text('\n'.join(line for line in path.read_text().splitlines()
                                  if not line.startswith('10. ')))
        self.assertTrue(self.module.validate(self.root))

    def test_link_quebrado_e_detectado(self):
        path = self.root / 'estudos-concursos/README.md'
        path.write_text(path.read_text() + '\n[Quebrado](nao-existe.md)\n')
        self.assertTrue(self.module.validate(self.root))

    def test_prompt_sem_rota_e_detectado(self):
        path = self.root / 'estudos-concursos/catalogo.json'
        catalog = json.loads(path.read_text())
        catalog['prompts']['PROMPTS_PRONTOS.md'].pop()
        path.write_text(json.dumps(catalog))
        self.assertTrue(self.module.validate(self.root))

    def test_rota_para_skill_inexistente_e_detectada(self):
        path = self.root / 'estudos-concursos/catalogo.json'
        catalog = json.loads(path.read_text())
        catalog['prompts']['PROMPTS_PRONTOS.md'][0]['skills'] = ['nao-existe']
        path.write_text(json.dumps(catalog))
        self.assertTrue(self.module.validate(self.root))


if __name__ == '__main__':
    unittest.main()
