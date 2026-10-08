import json
from pathlib import Path
import shutil
import subprocess
import sys
pointer=json.loads(Path('_runtime/heart-of-devouring/runs/current-run.json').read_text(encoding='utf-8'))
run=Path(pointer['artifact_dir'])
copy=run/Path(__file__).name
assert not copy.exists()
shutil.copyfile(Path(__file__),copy)
subprocess.run([sys.executable,'_runtime/heart-of-devouring/rc9_restore_native_source.py','hive-missing-core','rc9-old-missing-core-reloaded'],check=True)
subprocess.run([sys.executable,'_runtime/heart-of-devouring/rc9_forward_native_days.py','rc9-old-missing-core-reloaded','2319.04.02','rc9-old-missing-core-natural-month-repaired','20'],check=True)
