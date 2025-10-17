import json
from pathlib import Path


def truncate(s: str, n: int) -> str:
    if not isinstance(s, str):
        return s
    return s[:n]


def main():
    fixture_path = Path(__file__).parent / 'api_data.json'
    if not fixture_path.exists():
        print('api_data.json not found')
        return 1

    with fixture_path.open('r', encoding='utf-8') as f:
        data = json.load(f)

    changed = 0
    for obj in data:
        model = obj.get('model')
        fields = obj.get('fields', {})

        if model == 'api.teammember':
            # DB currently enforces varchar(100) on some deployments; keep safe at 100
            fields['name'] = truncate(fields.get('name'), 100)
            fields['role'] = truncate(fields.get('role'), 100)
            changed += 1

        if model == 'api.setting':
            fields['key'] = truncate(fields.get('key'), 100)
            changed += 1

        if model == 'api.aboutfeature':
            fields['icon'] = truncate(fields.get('icon'), 10)
            changed += 1

    with fixture_path.open('w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)

    print(f'sanitized objects: {changed}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())


