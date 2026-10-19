"""Independently reread the local source and exact excerpt bytes."""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json

base = Path(__file__).resolve().parent
raw_index = (base / 'sources.json').read_bytes()
index = json.loads(raw_index)
checks = []
search_index = json.loads((base / 'search-results.json').read_bytes())
inventory = (base / 'search-inventory.txt').read_bytes()
assert sha256(inventory).hexdigest() == search_index['inventory_sha256']
assert len(inventory.splitlines()) == search_index['inventory_file_count']
for search in search_index['searches']:
    assert len(search['matches']) == search['match_count']
    assert search['stderr'] == ''
    assert search['exit_code'] == (0 if search['match_count'] else 1)
    for match in search['matches']:
        line = Path(match['path']).read_text(encoding='utf-8-sig').splitlines()[match['line'] - 1]
        assert line == match['text']
for source in index['sources']:
    raw = Path(source['source_path']).read_bytes()
    assert len(raw) == source['source_bytes']
    assert sha256(raw).hexdigest() == source['source_sha256']
    lines = raw.splitlines(keepends=True)
    assert len(lines) == source['source_line_count']
    for excerpt in source['excerpts']:
        raw_excerpt = (base / excerpt['path']).read_bytes()
        assert raw_excerpt == b''.join(lines[excerpt['start_line'] - 1:excerpt['end_line']])
        assert len(raw_excerpt) == excerpt['bytes']
        assert sha256(raw_excerpt).hexdigest() == excerpt['sha256']
        checks.append(excerpt['path'])
report = {'status': 'PASS', 'verified_at_utc': datetime.now(timezone.utc).isoformat(),
          'sources_json_sha256': sha256(raw_index).hexdigest(),
          'source_count': len(index['sources']), 'excerpt_count': len(checks),
          'checks': 'Original source hash/size/line count and every raw excerpt byte independently matched.',
          'excerpts': checks, 'runtime_acceptance': 'Not performed; causal attribution unresolved.'}
(base / 'verify.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
print(json.dumps({key: report[key] for key in ('status', 'source_count', 'excerpt_count', 'sources_json_sha256')}))
