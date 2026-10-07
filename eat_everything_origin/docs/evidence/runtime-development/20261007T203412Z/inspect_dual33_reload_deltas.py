import json
from pathlib import Path
run = Path('_runtime/heart-of-devouring/runs/20261007T203412Z')
a = json.loads((run / 'rc7-dual33-report-pending-native.audit.json').read_text(encoding='utf-8'))
b = json.loads((run / 'rc7-dual33-report-reloaded-native.audit.json').read_text(encoding='utf-8'))
changes = []
def walk(left, right, path):
    if left == right:
        return
    if isinstance(left, dict) and isinstance(right, dict):
        for key in sorted(left.keys() | right.keys()):
            walk(left.get(key), right.get(key), path + '/' + key)
    else:
        changes.append({'path': path, 'before': left, 'after': right})
for key in ['countries', 'colonies', 'pop_groups', 'pop_jobs', 'planets']:
    walk(a[key], b[key], key)
out = run / 'rc7-dual33-original-full-reload-deltas.json'
assert not out.exists()
out.write_text(json.dumps(changes, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'change_paths': len(changes), 'non_budget': [value for value in changes if '/budget' not in value['path']][:65]}, ensure_ascii=True))
