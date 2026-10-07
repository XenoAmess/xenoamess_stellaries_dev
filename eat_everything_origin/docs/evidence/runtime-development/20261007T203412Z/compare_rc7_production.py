import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
sys.path.insert(0, 'eat_everything_origin/tools')
from build_native_adapter import definition

root = Path('eat_everything_origin/mod')
previous = 'a49acac7'
files = []
old_effects = None
for path in sorted(root.rglob('*')):
    if not path.is_file():
        continue
    relative = path.relative_to(root).as_posix()
    raw = path.read_bytes()
    old = subprocess.run(['git', 'show', previous + ':' + path.as_posix()], capture_output=True, check=True).stdout
    files.append({'file': relative, 'sha256': hashlib.sha256(raw).hexdigest(), 'previous_sha256': hashlib.sha256(old).hexdigest(), 'byte_identical': raw == old})
    if relative == 'common/scripted_effects/eep_effects.txt':
        old_effects = Path(__file__).parent / 'rc6-eep-effects-exact-git-source.txt'
        assert not old_effects.exists()
        old_effects.write_bytes(old)
current_effects = (root / 'common/scripted_effects/eep_effects.txt').read_text(encoding='utf-8-sig')
names = re.findall(r'^([a-z0-9_]+)\s*=\s*\{', current_effects, re.M)
functions = [{'function': name, 'normalized_definition_identical': definition(old_effects, name)[0].replace('\r\n', '\n') == definition(root / 'common/scripted_effects/eep_effects.txt', name)[0].replace('\r\n', '\n')} for name in names]
report = {'version': '0.2.0-rc.7', 'previous_commit': previous,
          'scope': 'Read-only production file bytes versus Git rc6 and newline-normalized exact scripted-effect definitions. eep_begin changed; prior court/settlement/report tests are reusable only with affected begin regression and final production smoke, not as all-route acceptance.',
          'files': files, 'scripted_effect_definitions': functions,
          'changed_files': [value['file'] for value in files if not value['byte_identical']],
          'changed_scripted_effects': [value['function'] for value in functions if not value['normalized_definition_identical']]}
destination = Path('eat_everything_origin/docs/evidence/rc7-production-file-delta-2026-10-08.json')
assert not destination.exists()
destination.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({key: value for key, value in report.items() if key not in ('files', 'scripted_effect_definitions')}))
assert set(report['changed_files']) == {'descriptor.mod', 'common/scripted_effects/eep_effects.txt'}
assert report['changed_scripted_effects'] == ['eep_begin']
