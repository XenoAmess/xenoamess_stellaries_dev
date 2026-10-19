# RC4三类全年经济离线汇总入口

## 目标、范围与验收

主线程授权准备接收新raw后的批量认证入口。复用现有`check_single_homeworld.economy`，不新增采集器或改历史检查器；整个入口只读取SAV／audit／receipt／manifest／静态报告，不导入runtime、不操作UI、不写SAV。没有齐全13份原生档时失败，不生成空白PASS。

每分支13份是Jan1初始anchor加随后12个连续月初；源文件名为`<prefix>m00.sav`至`<prefix>m12.sav`。Hive、Machine、普通洁癖分别运行。石质Hive只要求独立首月，不在本全年入口扩展成第四个12月case。

历史baseline固定为`docs/evidence/1019-baseline`，前缀Hive=`bh`、Machine=`bm`、Purifier=`bp`。已只读核对三个m00原生来源：run053917Z、历史profile `eep-0.3.2-single-homeworld`、实际冻结descriptor版本0.3.1，receipt均存在且匹配。该历史profile允许作为baseline，不要求它冒充0.4；RC3 candidate全年结果不能作为RC4 candidate。

candidate必须与RC4 canonical manifest的精确EXE／简中／单生产Mod、版本、生产文件表与树、原始2e静态报告SHA一致；共享loader／numeric／callback门禁重新核对实际copied_mod。每份baseline及candidate核原SAV SHA／receipt／audit、ZIP CRC、gamestate SHA，再由原检查器重读实际预算；不得把月度economy JSON当原生SAV。

输出仅覆盖12月净电、库存及完整原生预算：不能自动认证无注资／交易补贴／关岗／拆船／正常维护／人口保持／UI对照，这些需要独立操作、原始库存闭合、岗位／舰船和UI专项。输出即使`PASS_SCOPED`，完整economy case仍为PENDING，最终日志亦待结束冻结。不生成最终index，不填写最终case true。

## 既有CLI

原命令已经具备`economy <baseline-dir> <baseline-prefix> <candidate-dir> <candidate-prefix>`；先完成上方前置核对，再使用新的输出文件。CLI自身使用write_text，调用方必须拒绝既有输出，避免覆盖原报告：

```powershell
python eat_everything_origin/tools/check_single_homeworld.py --output <new-report.json> economy eat_everything_origin/docs/evidence/1019-baseline bh <actual-RC4-raw-directory> <actual-hive-prefix>
python eat_everything_origin/tools/check_single_homeworld.py --output <new-report.json> economy eat_everything_origin/docs/evidence/1019-baseline bm <actual-RC4-raw-directory> <actual-machine-prefix>
python eat_everything_origin/tools/check_single_homeworld.py --output <new-report.json> economy eat_everything_origin/docs/evidence/1019-baseline bp <actual-RC4-raw-directory> <actual-purifier-prefix>
```

以上尖括号明确为尚未提供的raw参数，不是实际已存在的项目证据。更少手工出错的整套入口如下：只填写branch、实际directory和prefix，输出新版本号，所有SHA从现存字节生成。

## 完整前置核对与汇总配方

在仓库根目录定义下列PowerShell函数。它调用既有离线Python API，以`open('x')`独占输出；默认原始运行目录真实存在，但各新经济prefix尚未给出，故不预填或执行。若将来使用另一RC4 run，其manifest仍必须与本轮canonical的候选字节和门禁一致，报告记录实际run_id。

```powershell
function Invoke-EepAnnualSummary {
    param(
        [Parameter(Mandatory)][ValidateSet('hive','machine','purifier')][string]$Branch,
        [Parameter(Mandatory)][string]$Prefix,
        [string]$RawDirectory = 'C:\Users\1\AppData\Local\xenoamess_stellaries_dev\artifacts\1019-implementation\runs\20261019T112808Z',
        [ValidateRange(1,999)][int]$ReportVersion = 1
    )
    $project = (Resolve-Path -LiteralPath 'eat_everything_origin').Path
    $recipe = @'
import hashlib, json, pathlib, re, sys, zipfile
p, raw = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
branch, prefix, version = sys.argv[3], sys.argv[4], int(sys.argv[5])
sys.path.insert(0, str(p / 'tools'))
sys.path.insert(0, str(p / 'testing'))
import check_single_homeworld as old, inspect_1019 as native, publish_1019 as release
if not re.fullmatch(r'[A-Za-z0-9_-]+', prefix):
    raise ValueError('explicit native filename prefix required')
out = p / f'docs/evidence/1019-analysis/rc4-{branch}-economy-12months-report-v{version}.json'
if out.exists():
    raise FileExistsError('preserve existing report; select a new ReportVersion')
base = p / 'docs/evidence/1019-baseline'
base_prefix = {'hive': 'bh', 'machine': 'bm', 'purifier': 'bp'}[branch]
canonical_path = p / 'docs/evidence/1019-rc4-pk2-duration/manifest.json'
canonical = json.loads(canonical_path.read_text(encoding='utf-8'))
manifest = old.read_run(raw)
for key in ('schema','profile_id','language','enabled_mods','game_exe_sha256',
            'repository_mod_tree_sha256','copied_mod_tree_sha256','repository_mod_files'):
    if manifest[key] != canonical[key]:
        raise ValueError('candidate RC4 binding differs: ' + key)
for key in ('status','version','source_tree_sha256','report_sha256','tool_checker_sha256'):
    if manifest['static_gate'][key] != canonical['static_gate'][key]:
        raise ValueError('candidate frozen static gate differs: ' + key)
gate = manifest['static_gate']
static_path = pathlib.Path(gate['report'])
if old.digest(static_path) != gate['report_sha256']:
    raise ValueError('frozen static report bytes differ')
static = json.loads(static_path.read_text(encoding='utf-8'))
if static.get('status') != 'PASS':
    raise ValueError('candidate static report is not PASS')
release.validate_weapon_csv_contract(static, pathlib.Path(manifest['copied_mod']))
release.validate_planet_killer_contract(static, pathlib.Path(manifest['copied_mod']))
proofs = {'baseline': [], 'candidate': []}
for role, directory, stem in (('baseline', base, base_prefix), ('candidate', raw, prefix)):
    for month in range(13):
        save = directory / f'{stem}m{month:02}.sav'
        _, proof = native.provenance(save)
        audit = json.loads(save.with_suffix('.audit.json').read_text(encoding='utf-8'))
        with zipfile.ZipFile(save) as archive:
            if archive.testzip() is not None:
                raise ValueError('native ZIP CRC failed: ' + str(save))
            gamestate_sha = hashlib.sha256(archive.read('gamestate')).hexdigest()
        if gamestate_sha != audit['gamestate_sha256']:
            raise ValueError('original audit gamestate SHA differs: ' + str(save))
        proofs[role].append(proof)
result = old.economy(base, base_prefix, raw, prefix)
result.update(branch=branch, run_id=manifest['run_id'], version=gate['version'],
    production_tree_sha256=manifest['repository_mod_tree_sha256'],
    manifest={'path': str(raw / 'manifest.json'), 'sha256': old.digest(raw / 'manifest.json')},
    static_report={'path': str(static_path), 'sha256': old.digest(static_path)},
    checker_sha256=old.CHECKER_SHA256, native_proofs=proofs,
    economy_case_status='PENDING', operational_constraints_status='PENDING_SEPARATE_REVIEW',
    ui_comparison_status='PENDING_SEPARATE_REVIEW', final_logs_status='PENDING_FINAL_FREEZE')
out.parent.mkdir(parents=True, exist_ok=True)
with out.open('x', encoding='utf-8', newline='\n') as stream:
    stream.write(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'status': result['status'], 'output': str(out),
                  'sha256': old.digest(out), 'checks': result['checks']}))
raise SystemExit(0 if result['status'] == 'PASS_SCOPED' else 1)
'@
    $recipe | python - $project $RawDirectory $Branch $Prefix $ReportVersion
    if ($LASTEXITCODE -ne 0) { throw 'Native annual budget summary failed; preserve any FAIL report.' }
}
```

接到真实prefix后可一次传三行任务调用该函数；仅完成的分支先调用也可。不要给尚未完整12月的分支预置prefix或通过状态：

```powershell
# Fill these values only from the actual completed native capture receipt.
# Invoke-EepAnnualSummary -Branch hive -Prefix <actual-hive-prefix>
# Invoke-EepAnnualSummary -Branch machine -Prefix <actual-machine-prefix>
# Invoke-EepAnnualSummary -Branch purifier -Prefix <actual-purifier-prefix>
```

首月若出现路径失败后的真实恢复，先整理经原receipt／时间／SHA核验的原件和原m00锚点，不盲目重命名或再次推进首月。若实际初始保存名称并非`<prefix>m00.sav`，应给现有检查器一个已完成、来源可追溯的阶段归档命名，而不是覆写活动run或伪造receipt；待明确实际新raw布局后再做这一小步适配。

新独立economy collector已与本入口约定兼容布局：`<stem>m00`是只读原UI anchor，新增`m01..12.sav/.audit.json/.economy.json`，每月独占`<stem>mNN-receipt.json`，最后独占总`<stem>-economy-receipt.json`的snapshots。现有provenance的`*-receipt.json`扫描可直接识别，不需要重命名活动auto原件或多做UI保存。当前约定Machine stem为`r4mc`；该名字只说明入口协议，未在本文声称其13份raw已经生成。年末原生UI档及`<stem>-auto-ui-comparison-m12.json`仍是十字段对照的独立范围，不自动扩为全年全部业务相同。

## 准备阶段验证

既有CLI与API字段、月序和实际baseline前缀已读取；三个baseline初始档均经原生provenance验证，历史profile和实际0.3.1版本按原样保留。Python配方编译通过；真实RC4归档作为candidate但故意指定不存在的`pending_economy_missing`前缀时，在13份Machine baseline原生／CRC／gamestate前置核对后明确因candidate m00缺失失败，未写输出；真实RC3硬件归档作为candidate时，在生产树绑定前置核对被拒绝，未写输出。两项只是缺证据／旧候选拒绝验证，不是经济结果。

本文配方尚无RC4新经济13份raw，未执行全年汇总、未生成新经济报告、未自动认证任何操作约束。本任务不修改旧工具或历史证据。
