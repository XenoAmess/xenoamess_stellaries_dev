# RC6成长执行补充计划（2026-10-19）

## 范围与事前约束

本计划与[同名JSON](rc6-growth-execution-plan-1019.json)只保存 `PLAN_ONLY` 命令、事前数值、证据形状和组装映射，不运行UI，不读取未来成长矩阵，不改生产、采集器、检查器、历史证据或Git。主线程独占简中实机。单人旧档加载恢复已由主线程另行验收；这里从RC6 Machine灭绝政体新局完成12个月经济后的干净year1 C0继续成长。

唯一候选树为 `cc181c8a27ede295e9fcebeffc5e10bb75e9cd643edec1d194b928993ffab33a`、59files、0.4.0-rc.6；EXE SHA为 `400df27c82ddc845aa9dce79bd468d81f18f060d299cd263e3afa93aef4f7a83`。source模型v4 SHA `6eb5ef0ef58fb353edd6e3f31b932ddc4bbf6b8b42b3bb6eaf2881fe51bd4c7f`，保留v1/v2/v3四链，系数及HP工程容差不变。

`check_growth_1019.py entry`会从实际保存target与国家fleet_manager自动读Mother IDs并验证source/gate；不要硬填旧159/997。`runtime_growth_1019.py`默认TREE仍历史RC3，直接调用时必须传RC6 `--expected-tree`；优先复制entry生成的完整命令。

## 入口、九节点与十八原生样本

建议新prefix `r6g`，前提是该run内没有任何 `r6g*` 文件。`$RunDir` 在以下示例中由真实RC6 manifest.artifact_dir替换，`$Anchor`指实际Machine yearui的 `.native-save.json`；均不是新造receipt。

```powershell
py eat_everything_origin/tools/check_growth_1019.py entry --anchor-receipt "$Anchor" --prefix r6g --autosave-dir "$ActiveAutosaveDir"
```

同一Machine局未reload：活动自动目录为anchor.written_at.parent。若先完成其他政体经济，再原生Load Machine yearui：活动目录取此次 `.load.json` 实际source.parent（通常history），显式传给entry；不能沿用归档目录或凭旧written_at猜测。加载后仍须原生同日确认干净C/L/R/六tier0。entry只读，之后主线程按它输出的dry-run/execute命令执行。

每个节点由现采集器执行一次 `effect root={set_variable={which=eep_c value=X} eep_sync_mothership=yes}`，FF30取得refresh，导出十modifier与两max trigger，再FF30取得final；不把两步合成FF60。十八个SAV/audit/observation、36条真实输入、HUD/OCR/date/mtime/SHA均保留。

| C | L=floor(C/10) | 距下一级 | 应得B/已发R | 待补P | 若anchor=2201.01.01，refresh / final |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | 10 | 0 | 0 | 2201.02.01 / 2201.03.01 |
| 9 | 0 | 1 | 0 | 0 | 2201.04.01 / 2201.05.01 |
| 10 | 1 | 10 | 0 | 0 | 2201.06.01 / 2201.07.01 |
| 19 | 1 | 1 | 0 | 0 | 2201.08.01 / 2201.09.01 |
| 20 | 2 | 10 | 0 | 0 | 2201.10.01 / 2201.11.01 |
| 49 | 4 | 1 | 0 | 0 | 2201.12.01 / 2202.01.01 |
| 50 | 5 | 10 | 1 | 0 | 2202.02.01 / 2202.03.01 |
| 200 | 20 | 10 | 4 | 0 | 2202.04.01 / 2202.05.01 |
| 10000 | 1000 | 10 | 200 | 0 | 2202.06.01 / 2202.07.01 |

六tier取实际独立随机结果，不预写分配。每份自然样本要求R=sum(N)、country镜像一致、临时budget变量清除、单个永久成长modifier倍率L、没有组件奖励modifier，实际design恰含AUX6盾/7甲/8舰体/9火力/10索敌/11再生。九个final才比较导出属性；refresh不能拿上一节点的旧诊断变量判当前属性。C0 final提供实际截距，且六tier必须全0。

## 原生导出与分离公式

JSON保存与现 `export_command()` 字节一致的完整控制台字符串。它显式 `event_target:eep_mothership0={every_owned_ship={...}}`，不依赖当前选中THIS。

十modifier：`ship_hull_add`、`ship_hull_mult`、`ship_armor_add`、`ship_armor_mult`、`ship_shield_add`、`ship_shield_mult`、`ship_weapon_damage`、`ship_tracking_add`、`ship_hull_regen_add_static`、`ship_armor_regen_add_static`，分别导出为 `eep_probe_<原键>`。两trigger是 `has_max_hp→eep_probe_max_hull`、`has_max_armor_hp→eep_probe_max_armor`。最大盾直接读取SAV `max_shield_hitpoints`，不使用不存在的 `has_max_shield_hp`。

以下截距均取RC6 C0 final真实值，不把Machine civic伤害+0.25或excess-power小计冒充实际总量。固定系数来自事前v1/v2，v4只确认RC6适用：

| 频道 | 相对真实C0的增量 |
| --- | --- |
| native max hull | 1500L + 3000N_hull |
| native max armor | 1287L + 2574N_armor |
| native max shield | 2091.375L + 4182.75N_shield |
| H/A/S multiplier | 各0.05L + 对应0.10N |
| weapon damage | 0.05L + 0.05N_damage |
| tracking add | 3N_tracking |
| hull/armor fixed daily regen | 各0.10L + 0.20N_regen |
| 三个flat H/A/S add | 0 |

三防HP量及两max trigger：abs=max(0.01,8×ULP32(expected))、rel0；这是事前工程余量，不宣称已证明引擎位宽。十modifier固定abs0.01、rel0；等级、计数、tier、ID、槽位全精确。这里验证最大值与恢复modifier，不声称已测面板DPS或真实损伤后的逐日恢复速率。

## C10000之后：同日repeat和原生reload

采集器结束并关闭console/debug后，先读取 `r6g-growth-receipt.json` 的最后根日期赋给 `$Date`，不能猜日历。C10000必须R200/P0，六tier都已非零；缺任一频道保持INCOMPLETE，不手设tier补覆盖。

主线程同日仅输入：

```powershell
$GrowthReceipt = Get-Content "$RunDir/r6g-growth-receipt.json" -Raw | ConvertFrom-Json
$Date = $GrowthReceipt.snapshots[-1].date
py eat_everything_origin/tools/runtime_1019.py console "effect root={eep_sync_mothership=yes eep_sync_mothership=yes}" r6grepeat-effect
py eat_everything_origin/tools/runtime_1019.py native-save r6grepeat "$Date"
py eat_everything_origin/tools/runtime_1019.py native-load r6grepeat r6gload
py eat_everything_origin/tools/runtime_1019.py native-save r6greload "$Date"
```

重复sync只在P0条件验证；不重新导出、不FF、不改C/tier。重载必须真正原生UI加载该唯一r6grepeat行，保存 `.load.json`、GPU/OCR和后续新SAV，不能用console load或手动event替代。比较最终matrix→repeat→reload：同日、同C/L/R/N、相同载荷/修正/健康/诊断；设计ID可由引擎重新编号而设计体须一致。业务scope与 `strict_gamestate_equal` 原字节判定分开，后者false不能改成完整档案PASS。

## C20500：单次预算200与下一月自动补十次

顺序必须在上述C10000/R200分支之后。先同日只同步一次：

```powershell
py eat_everything_origin/tools/runtime_1019.py console "effect root={set_variable={which=eep_c value=20500} eep_sync_mothership=yes}" r6gbudget-effect
py eat_everything_origin/tools/runtime_1019.py native-save r6gbudget1 "$Date"
```

预期C20500/L2050/B410/R400/P10，sumN400，六tier逐项不减，总增量200，临时budget已清除。该步不等触发modifier刷新，只验counts，不对即时三防/旧诊断变量写属性PASS。

然后仅输入一次 `fast_forward 30`，等待真实下个月1日HUD与新原生auto；不要手动第二次sync，不调用报告以外的功能事件、吞噬或结算。月度应自动到R410/P0、sumN410，总增量10；载荷与Mother身份不变。第二份receipt可以是单条 `{date,sha256,archived}`，同时另存输入/GPU/mtime/CRC绑定；不要求多一次UI保存。

对应现有物理输入CLI是 `py eat_everything_origin/tools/runtime_1019.py console "fast_forward 30" r6gbudget-auto-advance`；若主线程用LiveBackend，则调用同一console命令并保留其返回action/HUD绑定。此处只是提供命令，不执行。

活动auto目录取刚才真实 `r6gload.load.json.source.parent`，不能再取未reload前campaign。旧 `runtime_single_homeworld.monthly_autosaves` 仅有2200首年日历，不能用于此2202分支；使用现 `runtime_growth_1019.LiveBackend` 的单FF30/HUD与 `fresh_native`、write_new原字节归档原语，或主线程既有同等流程。新SAV/audit/单条receipt预先拒覆盖；source必须mtime新于输入开始与旧mtime、ZIP CRC完整、根日期正确。JSON给出数据与原语名称，本任务不另建/运行采集工具。

## 普通舰负对照与报告UI

现checker从十八个原SAV独立抽取同国所有非Mother舰船：ID集合和native最大H/A/S保持，三个频道均须有真实正值普通舰；缺字段不能编造0。该自动范围只覆盖普通舰最大三防。伤害/索敌/固定恢复的普通舰实际十导出没有被自动采集；其他归属结论使用冻结bound-Mother component源码+Mother实际分离增量，不谎称普通舰十频道实测。如果另加普通舰导出，须C0与C10000独立分支保存，不能改collector36条命令合同；JSON提供可选exact command，非必需扩大UI矩阵。

报告UI可在repeat/reload和预算证据完成后另存分支执行：

```text
effect root={country_event={id=eep.100}}
```

简中应显示“母舰进化等级”“距离下一级”“核心升级记录”“应得／已发／待补”以及护盾／装甲／舰体／火力／索敌／再生六层数，不能泄漏 `eep_component_report` 或 `[Root....]` 原token。组件九个动态Root值为B/R/P+六tier，另有L/next两个进化值；六tier必须逐项等于同日原SAVcountry镜像。

推荐截图点为C10000的1000级/next10、200/200/0；若预算first报告另拍，则2050级/next10、410/400/10；monthly后是410/410/0。报告叙述包括每五级随机永久升级、积压分批补发、母舰不可用保留历史，不要求额外实现术语。六core名字应是自适应护盾/装甲/舰体/火力/索敌/再生核心。

`eep.100` 的 `eep_report` 会更新派生等级、报告缓存等变量；“只读”指不增加/消费C/G/D/R/tier或结算奖励，不是完整gamestate零字节变动。UI前后原生业务账本须核，不用截图代替source归因报告。报告截图与动作/后原SAV供最终18 case groups补证，本成长工具不自动判UI通过。

## 离线报告与最终18组的边界

主线程实际路径齐备后运行现checker，不修改其公式或源证书：

```powershell
py eat_everything_origin/tools/check_growth_1019.py report --receipt "$RunDir/r6g-growth-receipt.json" --repeat-receipt "$RunDir/r6grepeat.native-save.json" --reload-receipt "$RunDir/r6greload.native-save.json" --budget-first-receipt "$RunDir/r6gbudget1.native-save.json" --budget-second-receipt "$RunDir/r6gbudget-auto-receipt.json" --budget-second-mode monthly --startup-receipt "$MachineJan1Receipt" --output eat_everything_origin/docs/evidence/1019-analysis/rc6-growth-report-v1.json
```

输出需实际 `eep.six-core-growth-report.v1`、RC6树、四模型SHA、非空十八native_evidence、C0实际十modifier/三max截距、six coverage全true、final_native_tiers六正整数且sum200、matrix/repeat/reload/budget/ordinary_controls均非空PASS_SCOPED。HP合同保持现名与数值；missing→INCOMPLETE、mismatch→FAIL。报告文件新建不可覆盖。

整体发布清单是18 **case groups**，不同于本计划18 **native snapshots**。本计划主要支撑 `unlimited_growth`、`random_components`，并为 `candidate_reload` 提供局部业务证据；startup/economy三政体、lithoid首月、母舰参考配置、巨像三组、共同结算、普通拆解、旧档迁移、重复初始化等组仍各用其独立原生证据。`unlimited_growth` 的母舰毁灭不复活、实际跳跃/十船坞保持、invalid/cancel不成长和报告UI不是checker自动PASS项目；须引用相应独立证据，不能从数值矩阵推出来。JSON保留18组全名与此范围映射，不手填发布检查布尔值。

## 计划文件校验

同名JSON SHA256 `96eaf4a9180b227f184cff4faaef861f778508053d762955e99a61d045c3ff08`。生成只导入现有纯文件collector/checker，`runtime_1019`未导入；JSON标记 `PLAN_ONLY_NOT_EVIDENCE`。确认九C节点、十八phase与36命令、18个唯一case group、UI九component Root变量、当前v4文件SHA与四模型链一致。没有运行新的live采集或生成成长PASS报告；这份计划本身不能当作18组的结果证据。
