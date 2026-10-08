"""Read the original physical source even after native ownership is removed."""
import hashlib
import json
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, 'eat_everything_origin/tools')
import audit_save as q


def inspect(path, physical=1641):
    with zipfile.ZipFile(path) as z:
        text = z.read('gamestate').decode('utf-8-sig')
    roots = list(q.fields(text))
    planets = next(v for k, v, b in roots if k == 'planets' and b)
    raw = next(v for k, v, b in q.fields(q.block(planets, 'planet'))
               if k == str(physical) and b)
    p = q.scalars(raw)
    p['name'] = q.scalars(q.block(raw, 'name')).get('key')
    p['variables'] = q.scalars(q.block(raw, 'variables'))
    p['flags'] = {k: q.scalars(v) if b else q.unquote(v)
                  for k, v, b in q.fields(q.block(raw, 'flags'))}
    p['deposits'] = q.ids(q.block(raw, 'deposits'))
    pending = [q.scalars(v) for k, v, b in roots if k == 'player_event' and b]
    return {'save_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'date': next(q.unquote(v) for k, v, b in roots if k == 'date'),
            'physical': physical, 'raw_physical': raw, 'source': p,
            'player_events': pending, 'EEP_probe_reference': 'eep_probe' in text,
            'EEP_origin_reference': 'origin_heart_of_devouring' in text}


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    source = Path(sys.argv[1])
    result = inspect(source)
    output = source.with_suffix('.raw-source.json')
    assert not output.exists(), output
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n',
                      encoding='utf-8', newline='\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'raw_physical'},
                     ensure_ascii=False))
