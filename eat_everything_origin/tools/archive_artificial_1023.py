"""Freeze a stopped isolated habitat run and verify every archived byte."""
import hashlib
import json
from pathlib import Path
import re
import sys
import zipfile

import psutil

ROOT = Path(__file__).resolve().parents[1]
LOCAL = Path.home() / 'AppData/Local/xenoamess_stellaries_dev'
RUNS = LOCAL / 'artifacts/artificial-worlds-20261023/runs'
OUTPUT = ROOT / 'docs/evidence/artificial-worlds-2026-10-23'


def freeze(identity):
    if not re.fullmatch(r'\d{8}T\d{6}Z', identity):
        raise ValueError('explicit isolated run identity required')
    artifacts = RUNS / identity
    manifest = json.loads((artifacts / 'manifest.json').read_text(encoding='utf-8'))
    user = Path(manifest['userdir']).resolve()
    user.relative_to((LOCAL / 'runs').resolve())
    process = artifacts / 'process.json'
    if process.exists():
        pid = json.loads(process.read_text(encoding='utf-8')).get('pid')
        if pid and psutil.pid_exists(pid) and psutil.Process(pid).name().lower() == 'stellaris.exe':
            raise RuntimeError('stop the game before freezing logs')
    entries = [(p, 'artifacts/' + p.relative_to(artifacts).as_posix())
               for p in sorted(artifacts.rglob('*')) if p.is_file()]
    for name in ['logs', 'mod/eep-artificial-1023']:
        base = user / name
        entries += [(p, 'userdir/' + p.relative_to(user).as_posix())
                    for p in sorted(base.rglob('*')) if p.is_file()]
    for p in sorted(user.iterdir()):
        if p.is_file() and (p.name in ('settings.txt', 'pdx_settings.txt', 'dlc_load.json', 'user_empire_designs_v3.4.txt')
                            or re.fullmatch(r'art_[a-z_]+\.txt', p.name)):
            entries.append((p, 'userdir/' + p.name))
    OUTPUT.mkdir(parents=True, exist_ok=True)
    archive = OUTPUT / ('run-' + identity + '.zip')
    index = []
    with zipfile.ZipFile(archive, 'x', zipfile.ZIP_DEFLATED, compresslevel=6) as out:
        for source, name in entries:
            before = source.stat()
            raw = source.read_bytes()
            after = source.stat()
            if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
                raise RuntimeError('source changed during freeze: ' + str(source))
            out.writestr(name, raw)
            index.append(dict(path=name, bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest()))
    with zipfile.ZipFile(archive) as check:
        assert check.testzip() is None
        assert check.namelist() == [e['path'] for e in index]
        for entry in index:
            assert hashlib.sha256(check.read(entry['path'])).hexdigest() == entry['sha256']
    copied = {e['path'].removeprefix('userdir/mod/eep-artificial-1023/'): e['sha256']
              for e in index if e['path'].startswith('userdir/mod/eep-artificial-1023/')}
    expected = {e['path']: e['sha256'] for e in manifest.get('repository_mod_files', [])}
    if copied != expected:
        raise RuntimeError('actual isolated production bytes differ from manifest')
    result = dict(status='BYTE_VERIFIED_NOT_GAMEPLAY_ACCEPTANCE', run_id=identity,
                  archive=archive.name, archive_sha256=hashlib.sha256(archive.read_bytes()).hexdigest(),
                  production_files=len(copied), source_tree_sha256=manifest.get('repository_mod_tree_sha256'),
                  entries=index)
    (OUTPUT / ('run-' + identity + '.index.json')).write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'entries'}))


if __name__ == '__main__':
    freeze(sys.argv[1])
