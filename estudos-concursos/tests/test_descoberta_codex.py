"""Contrato da descoberta real de skills pelo Codex app-server."""
import copy
import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / 'estudos-concursos/scripts/verificar_descoberta_codex.py'


class DiscoveryTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(SCRIPT.is_file(), 'Verificação de descoberta ainda não implementada')
        spec = importlib.util.spec_from_file_location('verificar_descoberta_codex', SCRIPT)
        self.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.module)
        self.root = Path('/tmp/radar-repo')
        self.names = ['professor-de-concursos']
        self.result = {'data': [{
            'cwd': str(self.root), 'errors': [], 'skills': [{
                'name': self.names[0], 'enabled': True, 'scope': 'repo',
                'path': str(self.root / '.agents/skills' / self.names[0] / 'SKILL.md'),
            }, {'name': 'system-extra', 'scope': 'system', 'enabled': True}]}]}

    def test_discovered_and_enabled_repository_skill(self):
        self.assertEqual(self.module.validate_result(self.result, self.root, self.names), [])

    def test_missing_skill_fails(self):
        self.result['data'][0]['skills'] = []
        self.assertTrue(self.module.validate_result(self.result, self.root, self.names))

    def test_disabled_skill_fails(self):
        self.result['data'][0]['skills'][0]['enabled'] = False
        self.assertTrue(self.module.validate_result(self.result, self.root, self.names))

    def test_discovery_errors_fail(self):
        self.result['data'][0]['errors'] = [{'message': 'Invalid frontmatter'}]
        self.assertTrue(self.module.validate_result(self.result, self.root, self.names))

    def test_same_name_outside_repository_fails(self):
        self.result['data'][0]['skills'][0]['path'] = '/tmp/other/SKILL.md'
        self.assertTrue(self.module.validate_result(self.result, self.root, self.names))

    def test_wrong_scope_fails(self):
        self.result['data'][0]['skills'][0]['scope'] = 'user'
        self.assertTrue(self.module.validate_result(self.result, self.root, self.names))

    def test_wrong_cwd_and_malformed_response_fail(self):
        changed = copy.deepcopy(self.result)
        changed['data'][0]['cwd'] = '/tmp/other'
        self.assertTrue(self.module.validate_result(changed, self.root, self.names))
        self.assertTrue(self.module.validate_result({}, self.root, self.names))

    def test_unresponsive_process_times_out_and_is_reaped(self):
        with tempfile.TemporaryDirectory() as directory:
            executable = Path(directory) / 'fake-codex'
            executable.write_text('#!' + sys.executable + '\nimport time\ntime.sleep(60)\n')
            executable.chmod(0o700)
            with self.assertRaises(TimeoutError):
                self.module.query_skills(Path(directory), str(executable), timeout=0.1)


if __name__ == '__main__':
    unittest.main()
