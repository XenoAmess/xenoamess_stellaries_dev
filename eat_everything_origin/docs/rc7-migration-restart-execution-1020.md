# RC7旧档迁移与真实进程重启的最短执行链

## 目标、范围与验收标准（执行前）

本清单供主线程独占桌面执行；本次准备仅做离线只读调查和文档记录，不操作游戏、Steam或Git，不读取活动日志及r7puc，不修改工具、Mod、旧SAV或旧报告。随后只在本文指定的新目录生成文件存在性、原字节SHA和既有角色清单。清单或路径核验通过不等于实机迁移或重启通过。

复用真正旧伤档，不重造伤情，不把RC6结果改成RC7。新输出须来自完整59文件RC7树`61b34f6dbdc277c44364889d5f1e1cd2773a4624786bbf0d538079fc6ba4feb0`、版本`0.4.0-rc.7`、EXE `400df27c82ddc845aa9dce79bd468d81f18f060d299cd263e3afa93aef4f7a83`、简中单生产Mod profile。

迁移只验证单人真实load后layout修复。每步三防比例差固定在`[-0.000021,+0.000001]`，原双向`1e-6`诊断和原v1 FAIL保留；重复helper须严格零差异。原身份、原名、位置、赠品世界、人口、岗位、库存、所有队列付款/费用/进度不变。实际50槽/6required/六core必须出现。旧mobilebase缓存不承诺修复，多人即时加载不在验收范围。

重启必须由旧进程真实退出、新PID及新run记录、原生load回执和新原生SAV共同证明；同进程reload和manifest存在不能证明重启。首档复用已经完成的C20500/R400/P10，先证明pending持久，再仅FF30证明自动补10。另载真实PK/普通拆解成功后稳定档验证非零结算账本与去重；该输入尚未产生，不预填路径或结果。

## 已核实的真实旧输入

以下绝对路径均已读取原字节、核实存在及SHA。`A`仅为阅读缩写，实际根目录是`C:\Users\1\AppData\Local\xenoamess_stellaries_dev\artifacts`。

| kind/角色 | 相对于A的真实路径 | SHA256 |
| --- | --- | --- |
| public031 fixture | `single-homeworld-20261019/runs/20261019T053917Z/bmm00.sav` | `af5f64e2eaadb164e87796d2a9261ac97ef7d716cc3f8b3cec5f4a2f23f787f8` |
| public031 before | `1019-legacy-damage/runs/20261019T130448Z/p031before.sav` | `d5921823d723d4eb0dec5d912ae0e586aac5b903643472d44062229b66b0b1e2` |
| paid11 fixture | `1015-implementation/runs/20261014T223819Z/j13ten.sav` | `834ea5325f93e3d3e92a44aabccd87195564cd4f1292d4439ae865eba5af8d2e` |
| paid11 before | `1019-legacy-damage/runs/20261019T130448Z/ppaidbefore.sav` | `40c8f8dac9530594d501143132d55fef1205346d7f679f16c8858058ed392ff1` |

public before日期2200.01.01，Mother fleet128/ship1008/base15/queue50为空；paid before日期2200.01.12，fleet146/ship822/base13/queue54。paid11每项81合金、payer0、orbitable13；pool10，前十项进度10/60，最后一项0/60。两份before运行源都为公开0.3.1；paid原队列fixture本身是0.3.0-rc.1，不能改称0.3.1。

原manifest分别位于上述三个原run目录：public baseline SHA`bf540076292d39f95a711aed0aeb2e145356d667241da80f9de2e811c8a19095`；共同旧伤run SHA`6e004fb14f81fd0b1f3708c7298241f864b492b5bd2f48216960b2f6c6d5dedd`；paid原件SHA`daef4a396b85056f091612d959c4a90f181c62ff078330afcafa12501d328703`。完整audit/native-save/manifest路径与SHA已写入`evidence/1020-rc7-migration-restart-preparation/input-inventory-v1.json`，只登记实际已存在文件。

最终索引可直接复用已归档旧三件套，无须复制旧SAV：public fixture=`docs/evidence/1019-baseline/bmm00`，public before=`docs/evidence/1019-legacy-damage-run-final/run/p031before`，paid fixture=`docs/evidence/1015-2026-10-15/v13-shipyard-runtime/j13ten`，paid before=`docs/evidence/1019-legacy-damage-run-final/run/ppaidbefore`。每个前缀均为`.sav/.audit.json/.native-save.json`三角色。旧伤canonical manifest在`1019-legacy-damage-run-final/manifest.json`，不在其`run/`下面。

## 同一RC7进程内的两个迁移分支

所有以下命令从仓库根执行，Python使用`.venv/Scripts/python.exe`。先让当前功能分支完成保存，再执行新分支。必须先关闭已观察console/debug；native-load函数不负责替调用者清理console。新stage均为此前未用名称；若已存在，另取新prefix，不能覆盖旧尝试。

把两份原before导入当前隔离userdir的`save games/acceptance-fixtures`，不能往普通玩家目录写。调用既有`copy_seed_save`前须显式确认目标文件不存在且native_load递归搜索只会找到一份同名SAV；该工具函数本身不是独占创建器。下面是主线程实际执行片段，不是本准备已执行动作：

```python
from pathlib import Path
import sys
sys.path.insert(0, 'eat_everything_origin/tools')
import runtime_1019 as w
b = w.base
artifacts, userdir, manifest = b.h.load_run()
assert manifest['copied_mod_tree_sha256'] == '61b34f6dbdc277c44364889d5f1e1cd2773a4624786bbf0d538079fc6ba4feb0'
old = Path(r'C:\Users\1\AppData\Local\xenoamess_stellaries_dev\artifacts\1019-legacy-damage\runs\20261019T130448Z')
receipt = artifacts / 'r7-migration-input-imports.json'
assert not receipt.exists()
imports = []
for filename in ('p031before.sav', 'ppaidbefore.sav'):
    assert not list((userdir / 'save games').rglob(filename))
    imports.append(b.h.copy_seed_save(old / filename, userdir / 'save games'))
b.h.write_json(receipt, {'status': 'IMPORTED_BYTES_ONLY', 'imports': imports})
b.close_console('r7-migration-clean-console')
b.close_debug_overlay('r7-migration-clean-debug')
```

public保留原174项checkset的第三次真实返回load，不能缩成无额外load的路径。按顺序执行，不加FF、回血、fullsync、initialize或startup：

```powershell
.venv/Scripts/python.exe -B eat_everything_origin/tools/runtime_1019.py native-load p031before r7pautoload-native-load
.venv/Scripts/python.exe -B eat_everything_origin/tools/runtime_1019.py native-save r7pautoload 2200.01.01
.venv/Scripts/python.exe -B eat_everything_origin/tools/runtime_1019.py native-load r7pautoload r7preload-native-load
.venv/Scripts/python.exe -B eat_everything_origin/tools/runtime_1019.py native-save r7preload 2200.01.01
.venv/Scripts/python.exe -B eat_everything_origin/tools/runtime_1019.py native-load r7pautoload r7prepeatbase-native-load
.venv/Scripts/python.exe -B eat_everything_origin/tools/runtime_1019.py native-save r7prepeatbase 2200.01.01
.venv/Scripts/python.exe -B eat_everything_origin/tools/runtime_1019.py console 'effect root={eep_repair_existing_mothership_design=yes eep_repair_existing_mothership_design=yes}' r7prepeat-effect
.venv/Scripts/python.exe -B eat_everything_origin/tools/runtime_1019.py native-save r7prepeat 2200.01.01
```

paid保持原158项checkset，不插第三次load。reload本身就是repeat_before：

```powershell
.venv/Scripts/python.exe -B eat_everything_origin/tools/runtime_1019.py native-load ppaidbefore r7paidauto-native-load
.venv/Scripts/python.exe -B eat_everything_origin/tools/runtime_1019.py native-save r7paidauto 2200.01.12
.venv/Scripts/python.exe -B eat_everything_origin/tools/runtime_1019.py native-load r7paidauto r7paidreload-native-load
.venv/Scripts/python.exe -B eat_everything_origin/tools/runtime_1019.py native-save r7paidreload 2200.01.12
.venv/Scripts/python.exe -B eat_everything_origin/tools/runtime_1019.py console 'effect root={eep_repair_existing_mothership_design=yes eep_repair_existing_mothership_design=yes}' r7paidrepeat-effect
.venv/Scripts/python.exe -B eat_everything_origin/tools/runtime_1019.py native-save r7paidrepeat 2200.01.12
```

native load触发`on_single_player_save_game_load → eep.60 → eep_repair_existing_mothership_design`，已经是待验的生产迁移路径。不能先手工fullsync再把结果称为自动迁移。每次native-save保存新三件套；load回执仍保留自身`state_verified=false`，后续SAV/audit另证状态，不能修改回执为true。

## v2 case与发布typed合同

checker完整SHA为`8a8cf5a52d0c4dfbdfeaa0506a0d8728539d80ca72b56ab875b081a94b8ee0aa`；其`TREE`和无参数template默认仍RC6。显式RC7模板命令：

```powershell
.venv/Scripts/python.exe -B eat_everything_origin/tools/check_migration_1019.py --output eat_everything_origin/docs/evidence/1019-analysis/rc7-public031-migration-v2-template-v1.json template public031 --candidate-tree 61b34f6dbdc277c44364889d5f1e1cd2773a4624786bbf0d538079fc6ba4feb0
.venv/Scripts/python.exe -B eat_everything_origin/tools/check_migration_1019.py --output eat_everything_origin/docs/evidence/1019-analysis/rc7-paid11-migration-v2-template-v1.json template paid11 --candidate-tree 61b34f6dbdc277c44364889d5f1e1cd2773a4624786bbf0d538079fc6ba4feb0
```

从新template另建`rc7-<kind>-migration-v2-complete-case-v1.json`，固定fixture/原before/身份/policy不改，只按下表实际新路径填空；`R`为本轮真实manifest.artifact_dir，不预填未来run。完整case独占创建，不能改写template或RC6 case。

| 字段 | public031（前缀R） | paid11（前缀R） |
| --- | --- | --- |
| after | `r7pautoload.sav` | `r7paidauto.sav` |
| reload | `r7preload.sav` | `r7paidreload.sav` |
| after_load_receipt | `r7pautoload-native-load.load.json` | `r7paidauto-native-load.load.json` |
| reload_load_receipt | `r7preload-native-load.load.json` | `r7paidreload-native-load.load.json` |
| repeat_before | `r7prepeatbase.sav` | `r7paidreload.sav` |
| repeat_after | `r7prepeat.sav` | `r7paidrepeat.sav` |
| repeat_load_source | `"after"` | `null` |
| repeat_before_load_receipt | `r7prepeatbase-native-load.load.json` | `null` |

运行`check`必须等各角色原生文件稳定；新报告独占创建，完整CLI会重新读取SAV/manifest/copied完整源，不用旧RC6观察缓存改标签：

```powershell
.venv/Scripts/python.exe -B eat_everything_origin/tools/check_migration_1019.py --output eat_everything_origin/docs/evidence/1019-analysis/rc7-public031-migration-v2-complete-report-v1.json check eat_everything_origin/docs/evidence/1019-analysis/rc7-public031-migration-v2-complete-case-v1.json
.venv/Scripts/python.exe -B eat_everything_origin/tools/check_migration_1019.py --output eat_everything_origin/docs/evidence/1019-analysis/rc7-paid11-migration-v2-complete-report-v1.json check eat_everything_origin/docs/evidence/1019-analysis/rc7-paid11-migration-v2-complete-case-v1.json
```

最终`old_save_migration`采用`eep.1019.migration-release-scope.v2`：`execution_mode=single_player_postload_layout_repair`、classification=`predeclared_engineering_allowance_not_engine_storage_proof`、固定policy和原三限制。`damage_preserved=false`保留；只有真实两报告全项通过后，`damage_within_predeclared_v2_budget=true`。其它11项逐报告复核，不从顶层状态自动提升。

typed `checker`引用当前8a8工具；`source_certificate`必须引用`docs/evidence/1020-migration-rc7-source/source-certificate-v1.json`，SHA`29742bf394cf83d0b1fd3b9f8221bf06f0c359b40668afea30e3aaa82a946046`，两者均列本组analysis evidence。`contract_document`引用原固定预算合同。两个fixture bundle各有report/case、六角色`native_saves/audits/save_receipts`、after/reload load receipts，public再含repeat_before load，以及精确helper action。`r7prepeat-effect-command.action.json`、`r7paidrepeat-effect-command.action.json`才是repeat_action；它们必须实际记录同一literal命令和physical Enter。

归档后用项目相对路径及实际SHA建新typed提案，不直接修改旧RC6提案；所有四candidate角色的`candidate_source_identity`须为完整59文件RC7和实际新run manifest。可按`release-migration-v2-gate-1019.md`原结构组装，并用当前`publish_1019.validate_migration_contract`只读复核。原public174/paid158 checksets、原嵌套v1 FAIL和strict差异不变。

## 最后一次真实进程重启

等当前run所有功能输出稳定、原生保存和必要截图完成后才执行。复用已完成`r7gbudget1`，不要再setC或重复制造400/P10：

- 原run：`20261019T164112Z`，旧PID37300，process SHA`421bb7f4f436b0cbb6f3d6d63331f322fd66cf7a3e8276ee7f327cf1d5260f32`。
- 原manifest SHA`603236aeedc59d2f0a0308b500ca209f589fb89e2ea5d1928c8bc04d10fedd86`。
- 原SAV：`C:\Users\1\AppData\Local\xenoamess_stellaries_dev\artifacts\1019-implementation\runs\20261019T164112Z\r7gbudget1.sav`，SHA`bf7eeee89794dcdec2fa88adfdcca2053abe30cfd5e26aab2489974980e5733f`。
- 其精确native-save receipt SHA`acd2b76ddc8656a45b637e193153cba3d70742201a9a323de62a623615acf9d1`，audit SHA`866a77ff5a26c6b799ba5061de0e9edd6b93209d6c461e2e2bc5ea0937c4322f`，日期2202.07.01。
- 账本C20500/L2050/B410/R400/P10，S/A/H/D/T/Re tiers=`58/73/75/61/55/78`；G0/D2/made0/worlds0。tier和为400。此时十导出和max可仍为前一刷新缓存，首档pending持久性只要求账本/实际六组件，不把即时HP作为这一测试的新标准。

现`stop`发送真实WM_CLOSE，等待timeout后**内含强制终止fallback**。以下命令不能保证正常退出；必须检查真实`stop.json.forced=false`、`running_after=false`和PID已不存在，才称正常退出；如forced为true，保留原结果并如实记录，不能改回false。

```powershell
.venv/Scripts/python.exe -B eat_everything_origin/tools/runtime_1019.py stop --timeout 30
# 确认旧stop.json/进程退出后，冻结旧run完整日志；然后才prepare。
.venv/Scripts/python.exe -B eat_everything_origin/tools/runtime_1019.py prepare-single candidate-rc7 'C:\Users\1\AppData\Local\xenoamess_stellaries_dev\artifacts\1019-implementation\runs\20261019T164112Z\r7gbudget1.sav'
.venv/Scripts/python.exe -B eat_everything_origin/tools/runtime_1019.py launch --timeout 60
.venv/Scripts/python.exe -B eat_everything_origin/tools/runtime_1019.py native-load r7gbudget1 r7restart-pending-load
.venv/Scripts/python.exe -B eat_everything_origin/tools/runtime_1019.py native-save r7restartpending 2202.07.01
```

`candidate-rc7-gate.json`真实SHA`ed6c0fc3bfa92c38b75c7a89bca0453e164e6f5f70a5eab546fa7be0bcb91d04`；其实际源`.../1019-implementation/candidate-rc7/mod`仍为冻结59文件RC7。不要调用`gate-candidate`重命名当前工作源，也不要借用RC6 gate。prepare会建全新run/userdir及manifest.seeded_save，launch会建实际新process.json；这些就是新的candidate_reload run，需要最终登记新run_id。Steam保持离线，不加`--via-steam`。

新load本身只layout helper，不应领取pending。先独立核`r7restartpending`C/L/B/R/P和原tiers/身份/账本，再执行一次`fast_forward 30`、确认真实HUD为2202.08.01，关闭console/debug后保存。使用root现有FF30+wait方案，不重复手动sync：

```powershell
.venv/Scripts/python.exe -B eat_everything_origin/tools/runtime_1019.py console 'fast_forward 30' r7restart-month
# 等实际HUD到2202.08.01、关闭console/debug后再native-save。
.venv/Scripts/python.exe -B eat_everything_origin/tools/runtime_1019.py native-save r7restartmonth 2202.08.01
```

自动补奖结果验收R410/P0、六tier各不下降且总和410/新增10，C20500/L2050/B410保持；不硬编码随机分配结果等于旧r7gbudget2。月度普通资源随时间变动，不能把全档byte相等设为此跨月合同。保存前后load链、tiers、原料、经济/结算账本、实际组件、root player及stopped/started/PID证据另做独立有界报告。

随后把主线程**实际完成的非零C/G/D/made稳定结算档**经`copy_seed_save`独占导入新userdir（同前导入守卫和新import receipt），原生native_load→同日新save，检查原target settled标记、原生目标销毁/人口、C/G/D/made/worlds/容量/返还/制造账本和六tiers不重复增长，再真实重复原完成回调进行去重验证。命令/目标ID必须取该已完成case的实际绑定，不复用旧银河ID。该步骤可以共用candidate_reload、common_settlement和cancel-idempotence既定角色；当前无新源档，禁止填写未发生路径或PASS。

最后停止这个新进程、冻结其实际完整日志/stop/process，给两run唯一manifest和完整新load/save/actions/screenshots/analysis五类证据建最终索引。新迁移分支若已在旧RC7进程完成无需再重复跑一遍；跨进程pending与稳定结算档承担真正restart证明。此清单没有新增验收矩阵或宣称任何实机结果。

## 1020恢复执行的命名与输入准备

实际继续run为20261019T204055Z／PID24520，先前两个候选进程都已正常退出；
跨进程的非零普通结算与月界幂等已有独立新档和日志marker，仍须补高C pending。
旧档迁移继续同一冻结RC7来源和原v2政策，不另建源桥、不重造伤情。
恢复时先在当前artifact生成r9migration-public031-template-v1.json与paid11模板，
由原template函数显式传RC7_TREE，所有未来角色继续null/PENDING。真实导入在
当前C/D保护条件的UI载入链结束后进行，避免操作期间新文件改变存档列表顺序。
新UI角色采用r9前缀和易识别字母名；实际native输出齐备后再填写独立complete
case并运行原checker，不改模板、旧FAIL、before或政策。

实际高C跨进程加载及自然月补10已完成，下一步在同一24520进程执行public031
再paid11。为避免多个新输入卡同时改变原loader分组选择，只在本分支开始前
导入该一份before的同SHA易识别别名（r9publicseed／r9paidseed），明确不是新
原生保存。原case.before仍指固定旧原件，原load receipt用实际别名源SHA闭合。
public输出r9publicauto/reload/base/repeat，保留第三次真实返回after加载；paid
输出r9paidauto/reload/repeat，repeat_before复用reload。全程无FF、回血、完整
初始化或手动sync，repeat只用原两次layout helper字面量。完整case在原生角色
齐备后独占创建；先保留原v1严格FAIL，再按原v2政策验，不能为通过改预算。

## 离线准备结果

已独立核实四个旧输入角色的原SAV/audit/native-save/manifest全部存在，四份canonical旧三件套逐byte匹配原件；原pending三件套及其canonical副本也匹配，15项已记录原生变量符合上述值。checker、完整源证书、静态gate/report固定SHA均匹配。只形成`BYTES_AND_EXISTING_ROLES_ONLY`输入清单，未执行任何新load/save/checker实机报告/stop/prepare/launch/Steam/Git，也未读取活动日志或r7puc。后续实机执行结果须另建实际报告和不可变归档，不能修改这个事前清单为PASS。
