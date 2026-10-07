import hashlib
import json
from pathlib import Path

run = Path(__file__).resolve().parent
names = ['rc6-native120-native-mother-report-hidden-inspection',
         'rc6-native120-mother-native-and-eep-devour-hidden-inspection']
frames = [json.loads((run / (n + '.ocr.json')).read_text(encoding='utf-8')) for n in names]
checks = []

def check(name, actual, expected):
    checks.append({'check': name, 'actual': actual, 'expected': expected,
                   'status': 'PASS' if actual == expected else 'FAIL'})

for i, f in enumerate(frames):
    check('original_gpu_image_bytes_' + str(i), hashlib.sha256(Path(f['image']).read_bytes()).hexdigest(), f['image_sha256'])
    labels = [x['text'] for x in f['rows'] if x['score'] >= .8]
    check('actual_native_mother_title_' + str(i), 'EEP-Core' in labels, True)
    check('actual_infrastructure_page_' + str(i), '基础设施' in labels, True)
    check('actual_native_date_' + str(i), '2210.01.01' in labels, True)
    check('no_visible_queen_entry_or_flavour_' + str(i),
          [x for x in labels if any(term in x for term in ['觐见', '白绮', '吞噬之心'])], [])
check('native_colony_overview_visible', '殖民地总览' in [x['text'] for x in frames[0]['rows'] if x['score'] >= .8], True)
labels = [x['text'] for x in frames[1]['rows'] if x['score'] >= .8]
check('native_decision_menu_visible', '决议' in labels and '停止子个体生产' in labels, True)
check('no_devour_in_current_visible_mother_decisions', [x for x in labels if '吞噬' in x], [])
report = {'status': 'PASS' if all(c['status'] == 'PASS' for c in checks) else 'FAIL',
          'scope': 'Simplified-Chinese original non-EEP native mother interface at2210.01.01. Visually inspected actual colony infrastructure page; queen button/flavour absent. Current visible mother decision menu has no devour label. No claim about all other governments, hidden off-screen entries, or full Mod acceptance. Initial guessed-coordinate guard failure separately retained; no click executed in failed guard.',
          'images': {n: f['image_sha256'] for n, f in zip(names, frames, strict=True)}, 'checks': checks}
out = run / 'rc6-non-origin-native-mother-queen-hidden-ui-proof.json'
assert not out.exists()
out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'status': report['status'], 'checks': len(checks), 'failed': [c for c in checks if c['status'] != 'PASS']}))
