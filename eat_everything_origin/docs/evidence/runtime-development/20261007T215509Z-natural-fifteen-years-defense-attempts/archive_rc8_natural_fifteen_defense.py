import hashlib
import json
from pathlib import Path
import shutil
from datetime import datetime, timezone

source = Path('_runtime/heart-of-devouring/runs/20261007T215509Z')
target = Path('eat_everything_origin/docs/evidence/runtime-development/20261007T215509Z-natural-fifteen-years-defense-attempts')
assert not target.exists()
proof = json.loads((source / 'rc8-natural-terraform-checkpoints-4-2314-03-12-proof.json').read_text(encoding='utf-8'))
assert proof['status'] == 'PASS_SCOPED' and not proof['full_terraform_completion']
shutil.copyfile(Path(__file__), source / Path(__file__).name)
target.mkdir(parents=True)
(target / '.gitattributes').write_text('* binary\n**/* binary\n', encoding='utf-8')
entries = []

def take(path, name):
    data = path.read_bytes()
    out = target / name
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(data)
    digest = hashlib.sha256(data).hexdigest()
    assert hashlib.sha256(out.read_bytes()).hexdigest() == digest
    entries.append({'path': name, 'source': str(path.resolve()), 'bytes': len(data), 'sha256': digest})

prefixes = ('rc8-hiveworld-terraform-fifteen-real-years', 'rc8-hiveworld-defense-',
            'rc8-natural-main-fleet-', 'rc8-natural-own-mother-', 'rc8-native-', 'rc8-existing-fleet-',
            'rc8-close-selected-fleet-', 'rc8-physical-return-', 'rc8-queued-orbit-', 'rc8-select-main-',
            'rc8-reselect-existing-', 'rc8-remaining-natural-source-', 'rc8-natural-terraform-checkpoints-4-')
names = {Path(__file__).name, 'rc8_read_native_defense.py', 'rc8_native_main_fleet_recall.py',
         'rc8_native_mother_orbit_order.py', 'rc8_native_stop_and_return.py',
         'rc8_native_script_return_order.py', 'rc8_native_physical_return_order.py',
         'rc8_native_queued_orbit_return.py', 'rc8_native_move_mode_return.py',
         'rc8_prepare_remaining_native_sources.py', 'rc8_natural_forward_span_recovered.py',
         'rc8_verify_natural_terraform_checkpoints_recovered.py'}
for path in sorted(source.rglob('*')):
    if path.is_file() and (path.name.startswith(prefixes) or path.name in names):
        take(path, path.relative_to(source).as_posix())
error = Path('C:/Users/1/AppData/Local/xenoamess_stellaries_dev/runs/20261007T215509Z/logs/error.log')
take(error, 'stage-full-error-through-defense-attempts.log')
manifest = {'status': 'SNAPSHOT_BYTE_VERIFIED', 'snapshot_at_utc': datetime.now(timezone.utc).isoformat(),
            'run': source.name, 'version': '0.2.0-rc.8', 'language': 'l_simp_chinese',
            'scope': 'Completed fifteen-year checkpoint, defense attempts and natural-source preflight. Partial run, not final archive.',
            'original_files': len(entries), 'original_bytes': sum(v['bytes'] for v in entries),
            'full_terraform_completion': False, 'defense_success': False,
            'final_error_log_required_after_normal_stop': True,
            'preserved_failures': 'Wrong click targets, capital_scope colony target, physical auto-move without travel, queued orbit action without travel, normal move mode without return.',
            'files': entries}
(target / 'source-snapshot.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({k: v for k, v in manifest.items() if k != 'files'}, ensure_ascii=True))
