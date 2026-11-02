"""Confere descoberta local via skills/list, sem iniciar turno ou chamar um modelo."""
import argparse
import json
import os
from pathlib import Path
import selectors
import shutil
import subprocess
import sys
import tempfile
import time


def validate_result(result, root, expected):
    """Valida apenas o catálogo do cwd solicitado; skills de sistema são ignoradas."""
    root = root.resolve()
    data = result.get('data') if isinstance(result, dict) else None
    if not isinstance(data, list):
        return ['Resposta skills/list sem lista data']
    entries = [entry for entry in data if isinstance(entry, dict)
               and isinstance(entry.get('cwd'), str)
               and Path(entry['cwd']).resolve() == root]
    if len(entries) != 1:
        return ['Resposta deve conter exatamente um catálogo para o cwd solicitado']
    entry = entries[0]
    errors = []
    if entry.get('errors') != []:
        errors.append('Erros de descoberta: ' + json.dumps(entry.get('errors'), ensure_ascii=False))
    skills = entry.get('skills')
    if not isinstance(skills, list):
        return errors + ['Catálogo sem lista skills']
    for name in expected:
        matches = [skill for skill in skills if isinstance(skill, dict)
                   and skill.get('name') == name and skill.get('scope') == 'repo'
                   and isinstance(skill.get('path'), str)
                   and Path(skill['path']).resolve()
                   == root / '.agents' / 'skills' / name / 'SKILL.md']
        if len(matches) != 1:
            errors.append(f'{name}: ausente, duplicada ou fora do caminho/escopo do repositório')
        elif matches[0].get('enabled') is not True:
            errors.append(f'{name}: descoberta, mas não habilitada')
    return errors


def query_skills(root, codex, timeout=25):
    """Consulta JSON-lines com timeout total e configuração pessoal isolada."""
    deadline = time.monotonic() + timeout
    root = root.resolve()
    with tempfile.TemporaryDirectory(prefix='radar-codex-') as home, tempfile.TemporaryFile() as stderr:
        env = dict(os.environ, CODEX_HOME=home)
        # Desabilita telemetria no ambiente temporário, sem modificar config pessoal.
        Path(home, 'config.toml').write_text('[analytics]\nenabled = false\n[otel]\nexporter = "none"\n')
        process = subprocess.Popen([codex, 'app-server', '--stdio'], cwd=root, env=env,
                                   stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=stderr, bufsize=0)
        pending = bytearray()
        selector = selectors.DefaultSelector()
        selector.register(process.stdout, selectors.EVENT_READ)

        def send(message):
            process.stdin.write((json.dumps(message) + '\n').encode())
            process.stdin.flush()

        def receive(response_id):
            while True:
                while b'\n' in pending:
                    line, _, rest = pending.partition(b'\n')
                    pending[:] = rest
                    if not line.strip():
                        continue
                    try:
                        message = json.loads(line)
                    except (ValueError, UnicodeDecodeError) as exc:
                        raise RuntimeError('Saída app-server não é JSON válido') from exc
                    if not isinstance(message, dict):
                        raise RuntimeError('Mensagem app-server não é objeto JSON')
                    if message.get('id') == response_id:
                        if 'error' in message:
                            raise RuntimeError('Erro de protocolo: ' + json.dumps(message['error']))
                        if 'result' not in message:
                            raise RuntimeError('Resposta app-server sem result')
                        return message['result']
                remaining = deadline - time.monotonic()
                if remaining <= 0 or not selector.select(remaining):
                    raise TimeoutError(f'Codex skills/list excedeu {timeout}s')
                chunk = os.read(process.stdout.fileno(), 65536)
                if not chunk:
                    stderr.seek(0)
                    diagnostic = stderr.read().decode(errors='replace').strip()
                    raise RuntimeError('App-server encerrou antes de responder. ' + diagnostic)
                pending.extend(chunk)

        try:
            send({'id': 1, 'method': 'initialize', 'params': {
                'clientInfo': {'name': 'radar-check', 'version': '1'},
                'capabilities': {'experimentalApi': True}}})
            receive(1)
            send({'method': 'initialized'})
            send({'id': 2, 'method': 'skills/list', 'params': {
                'cwds': [str(root)], 'forceReload': True}})
            return receive(2)
        finally:
            selector.close()
            if process.poll() is None:
                process.terminate()
                try:
                    process.wait(timeout=2)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait()
            else:
                process.wait()
            process.stdin.close()
            process.stdout.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument('--codex', default='codex', help='Executável Codex CLI')
    parser.add_argument('--timeout', type=float, default=25)
    args = parser.parse_args()
    try:
        if args.timeout <= 0:
            raise ValueError('--timeout deve ser positivo')
        executable = shutil.which(args.codex)
        if executable is None:
            raise FileNotFoundError(f'Codex CLI não encontrado: {args.codex}')
        catalog = json.loads((args.root / 'estudos-concursos/catalogo.json').read_text())
        expected = catalog['skills']
        if not isinstance(expected, list) or not expected or any(not isinstance(n, str) for n in expected):
            raise ValueError('catalogo.json não contém lista skills válida')
        result = query_skills(args.root, executable, args.timeout)
        errors = validate_result(result, args.root, expected)
        print(json.dumps({'ok': not errors, 'verificacao': 'descoberta-local-codex',
                          'skills': sorted(expected) if not errors else [],
                          'total': len(expected) if not errors else 0,
                          'errors': errors}, ensure_ascii=False, indent=2))
        return 1 if errors else 0
    except (OSError, ValueError, KeyError, RuntimeError, TimeoutError) as exc:
        print(json.dumps({'ok': False, 'errors': [str(exc)]}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
