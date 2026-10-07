import json
import logging
from pathlib import Path
import shutil
import sys
import zipfile

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, 'eat_everything_origin/tools')
sys.argv = ['runtime', '--fixture']
import runtime as r
import audit_save as q
logging.disable(logging.INFO)
h = r.harness
run, user, manifest = h.load_run()
shutil.copyfile(Path(__file__), run / Path(__file__).name)
assert manifest['pid'] == 23020
stage = 'rc8-hiveworld-terraform-ten-real-years'
assert not (run / (stage + '.sav')).exists()
frame = r.gpu_capture(stage + '-recovered-full-or-cropped-receipt')
labels = [row['text'] for row in frame['rows']]
assert '2309.03.12' in labels
assert '暂停' in labels
assert any(h.normalized(text) in {'fastforwarded1800days', 'fastforwarded1800d'} for text in labels)
h.write_json(run / (stage + '-recovered-calendar-receipt.json'), {
    'status': 'CALENDAR_CONFIRMED', 'actual_date': '2309.03.12', 'actual_native_days': 1800,
    'original_helper_result': 'Stopped exact Python worker after repeated full-days OCR guard failure.',
    'recovered_guard': 'Fresh exact date + paused UI + exact full/cropped 1800-day completion row; native progress checked below.',
    'frame_sha256': frame['image_sha256'], 'labels': labels,
    'performance_measurement': 'NOT_VALID: extra monitoring waits followed completed native fast-forward.'})
h.press_scan_code(0x29, stage + '-recovered-console-close', 1)
after = r.native_save(stage, '2309.03.12', (0,))
with zipfile.ZipFile(run / (stage + '.sav')) as z:
    native = z.read('gamestate').decode('utf-8-sig')
planet = q.block(q.block(q.block(native, 'planets'), 'planet'), '1')
terraform = {k: v for k, v, obj in q.fields(planet) if 'terraform' in k}
t = q.scalars(terraform['terraform_process'])
assert t['progress'] == 3600 and t['total'] == 7200 and t['planet_class'] == 'pc_hive'
h.write_json(run / (stage + '-native-terraform-checkpoint.json'), {
    'date': after['date'], 'actual_class': after['planets']['1']['planet_class'],
    'terraform': terraform, 'save_sha256': after['save_sha256'],
    'eep_ledger': {k: after['countries']['0']['variables'][k] for k in ['eep_c', 'eep_g', 'eep_d', 'eep_made', 'eep_worlds']},
    'country_scope': 'Focus country0 and actually present EEP owners; not all native foreign countries.'})
c = after['countries']['0']
print(json.dumps({'date': after['date'], 'terraform': t, 'energy': c['stockpile'].get('energy', 0),
                  'minerals': c['stockpile'].get('minerals', 0),
                  'population': after['colonies']['0']['actual_pop_sum'], 'sha256': after['save_sha256']}, ensure_ascii=True))
