"""Confere skills, invocação implícita, rotas de prompts e links locais."""
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

import yaml


def validate(root):
    root = Path(root).resolve()
    study = root / 'estudos-concursos'
    errors = []
    try:
        catalog = json.loads((study / 'catalogo.json').read_text(encoding='utf-8'))
        expected = catalog['skills']
        routes = catalog['prompts']
        if not isinstance(expected, list) or not expected or len(expected) != len(set(expected)):
            return ['Catálogo de skills vazio ou duplicado']
        if not isinstance(routes, dict) or not routes:
            return ['Catálogo de prompts vazio']
    except (OSError, ValueError, KeyError, TypeError) as exc:
        return [f'Catálogo inválido: {exc}']
    paths = sorted((root / '.agents/skills').glob('*/SKILL.md'))
    actual = {p.parent.name for p in paths}
    if actual != set(expected):
        errors.append(f'Skills divergentes do catálogo: {sorted(actual ^ set(expected))}')
    for path in paths:
        name = path.parent.name
        try:
            match = re.match(r'\A---\r?\n(.*?)\r?\n---\r?\n',
                             path.read_text(encoding='utf-8'), re.S)
            front = yaml.safe_load(match[1]) if match else None
            if not isinstance(front, dict) or front.get('name') != name:
                errors.append(f'{name}: nome/frontmatter inválido')
            elif not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name) or len(name) > 64:
                errors.append(f'{name}: nome fora do padrão')
            if not isinstance(front, dict) or not isinstance(front.get('description'), str) or not front['description'].strip() or len(front['description']) > 1024:
                errors.append(f'{name}: descrição inválida')
            metadata = yaml.safe_load((path.parent / 'agents/openai.yaml').read_text(encoding='utf-8'))
            if metadata.get('policy', {}).get('allow_implicit_invocation') is not True:
                errors.append(f'{name}: invocação implícita não habilitada')
            interface = metadata.get('interface', {})
            if not all(isinstance(interface.get(k), str) and interface[k].strip()
                       for k in ('display_name', 'short_description', 'default_prompt')):
                errors.append(f'{name}: interface incompleta')
            if '$' + name not in interface.get('default_prompt', ''):
                errors.append(f'{name}: prompt padrão não referencia a skill')
        except (OSError, ValueError, TypeError, AttributeError, yaml.YAMLError) as exc:
            errors.append(f'{name}: {exc}')
    actual_prompt_files = {p.name for p in study.glob('PROMPTS*.md')}
    if actual_prompt_files != set(routes):
        errors.append('Arquivos de prompts divergentes do catálogo')
    for filename, entries in routes.items():
        try:
            text = (study / filename).read_text(encoding='utf-8')
            ids = [int(n) for n in re.findall(r'^(\d+)\. ', text, re.M)]
            route_ids = [entry['id'] for entry in entries]
            if not ids or ids != list(range(1, len(ids) + 1)) or ids != route_ids:
                errors.append(f'{filename}: numeração ou rotas incompletas')
            for entry in entries:
                if not entry['skills'] or not set(entry['skills']) <= set(expected):
                    errors.append(f'{filename}/{entry["id"]}: skill de destino inválida')
        except (OSError, ValueError, TypeError, KeyError) as exc:
            errors.append(f'{filename}: {exc}')
    docs = [study / 'README.md', study / 'AGENTS.md']
    docs += [study / p for p in routes]
    for path in docs:
        try:
            for link in re.findall(r'\]\(([^)]+)\)', path.read_text(encoding='utf-8')):
                url = urlsplit(link.strip('<>'))
                if url.scheme or url.netloc or not url.path:
                    continue
                target = (path.parent / unquote(url.path)).resolve()
                if not target.is_relative_to(root) or not target.exists():
                    errors.append(f'{path.name}: link local inválido: {link}')
        except OSError as exc:
            errors.append(f'{path.name}: {exc}')
    return errors


if __name__ == '__main__':
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[2]
    failures = validate(root)
    if failures:
        print('\n'.join(f'ERRO: {error}' for error in failures))
        sys.exit(1)
    catalog = json.loads((root / 'estudos-concursos/catalogo.json').read_text(encoding='utf-8'))
    print(f'OK: {len(catalog["skills"])} skills com invocação implícita; '
          f'{sum(map(len, catalog["prompts"].values()))} prompts com rotas; links válidos.')
