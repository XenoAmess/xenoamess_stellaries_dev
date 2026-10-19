# RC7 成长剩余三项的最短执行顺序

## 目标与边界

本页只读整理既有最小probe计划、原生损毁片段与观察接口，供root依现有方案执行；不操作UI/Git、不改工具/Mod/源fixture，不读活动run未来raw或日志，不创建未来结果、receipt或SAV。这里只给顺序和已有命令索引，不补造任何native PASS，不扩大验收矩阵。已有跃迁/十船坞组合覆盖不再实跳或造舰。

本页所有原生保存名由root选择新的ASCII唯一前缀。下表的“低级导出后”“damage0”“day1”“death-month”“death-reload”是角色称呼，尚无新文件，不应当作已有证据引用。当前RC7树仍 `61b34f6dbdc277c44364889d5f1e1cd2773a4624786bbf0d538079fc6ba4feb0`。

两次输入加载的准确来源分别在 [r7ganchor receipt](evidence/1019-rc7-growth-v1/run/r7ganchor.native-save.json) 和 [r7evreport receipt](evidence/1020-rc7-high-level-ui-v1/raw/r7evreport.native-save.json) 的 `history` 字段：原run `20261019T164112Z` 的 `save games/eep-test-history/r7ganchor.sav`、`save games/eep-test-history/r7evreport.sav`；对应 `date` 是2201.01.01及2202.08.07，`sha256` 是 `aec53eeed736d23abb856b7a1c1696657ce55517124097f1ad6c69921f1d8385`、`0d64de5652563ebbc2a453e47c7298ceecabe0392b95562cd5ed967060d42b97`。plan的 `source_refs[1].path` / `[2].path` 是同字节canonical归档副本；原生UI应加载已存在history来源或root已按字节导入的同SHA副本，不把归档目录当活动autosave目录。

## 已有输入与直接取命令的方法

最小probe计划是 [plan.json](evidence/1020-rc7-growth-minimal-probes-v1/plan.json)，SHA `d5a861bf24bbdcc96befed194fc5f54cb032c57e504a66e799b9f177e160175f`。只读取其 `commands` 按name索引的 `command` 原文，不执行P语法wrapper：

```python
plan = json.loads(Path("docs/evidence/1020-rc7-growth-minimal-probes-v1/plan.json").read_text(encoding="utf-8"))
cmd = {row["name"]: row["command"] for row in plan["commands"]}
ordinary = cmd["ordinary-ten-modifiers"]
mother14 = cmd["mother-fourteen-modifiers"]
damage = cmd["mother-positive-damage"]
```

三个命令分别1050/1426/115个ASCII字符，不含末尾LF的SHA分别为 `b1dc9e5f73d388af4172f55f394fc1a2599201c2b30316d064762e161e8d3ccc`、`a6104e9831da971111278c09712efeb26c5e15ce7f608c523079fc3cf66c62d8`、`a51ade77d1b45589909dadfb677ac071ede6dd1dfa95c295f5f95a1d361e0f61`。原三个wrapper已由现有Kaishek零诊断通过，仅证明静态语法。

损毁与损毁后完整初始化复用 [既有execution map](../testing/colossus_1019_rc6_execution_map.json) 的 `commands`，**仅取下列两行原文，不执行整份RC6计划或采用其旧tree/run元数据**：

```python
execution = json.loads(Path("testing/colossus_1019_rc6_execution_map.json").read_text(encoding="utf-8"))
old_cmd = {row["id"]: row["command"] for row in execution["commands"]}
destroy = old_cmd["r6_destroy_mother"]
dead_sync = old_cmd["r6_destroy_sync"]
```

两行分别626/114字符，SHA `a39e896f8909000d7963e6f93af4f20d3b5833ea8fa2a2dac5101f59d855f6dd`、`1c077f459dd2cf1c361113e7013719079690751a7123ec72bd8457520ec2f17d`，与[原损毁设计](colossus-rc4-final-execution-order-1019.md)的两行逐字相同。destroy先在Mother仍存在时保存country actor，再destroy_fleet，明确kill_leader=no/destroy_template=no；dead_sync从保存的actor调用完整initialize/startup/sync，不能在Mother死亡后再次取Mother.owner。

root既有实际发送接口为 `runtime_1019.command_open(command, unique_stage)`，连续无依赖命令可共用已观察到的console；原生保存前仍按既有流程close_console、close_debug_overlay。保存接口为 `runtime_1019.base.r.native_save(unique_stage, actual_expected_date, (0,))`，不会覆盖已有artifact。此页不调用这些接口，不要求引入新自动化工具。

## 三分支串行连接

| 顺序 | 原始日期/输入与动作 | 保存和必要回档 |
| --- | --- | --- |
| 1 | 实际load同来源银河 `r7ganchor`，原生2201.01.01；执行ordinary一次，不推进时间。 | 原生保存“低级导出后”，date仍2201.01.01；随后必须load高等级输入，不能在本档人工设C或tier。 |
| 2 | 实际load同银河 `r7evreport`，原生2202.08.07；执行ordinary、mother14两条，无依赖可连续输入。 | 原生保存“高级导出后/恢复before”，date仍2202.08.07；同档同时交11普通舰负对照和母舰14getter。不要换freshMachine经济末年新银河。 |
| 3 | 在高级before单Mother仍存活、实际H/A各>200000且S<10000000、核心可用、非战斗/维修订单时，执行damage一次。 | 同暂停日**先原生保存damage0**，核实际伤甲/伤舰体/max不变和账本/tiers不变；尚未FF。 |
| 4 | 仅`fast_forward 1`，以实际SAV/HUD核日期。 | 若起点确是2202.08.07，day1应2202.08.08；原生保存day1，先读取实际恢复结论。若首日没涨，保留诊断并按既定有限窗口决定少天，不能无限自动推进。 |
| 5 | 直接以已保存的恢复day1作为损毁before，不再load高档。所有需要活母舰的本轮正例采完，且真实核心仍可用、三个grant flags仍在时，执行destroy，再执行dead_sync。 | 母舰真实销毁与初始化操作分别保留输入；无需新增同日death0存档，复用原损毁设计的after两档范围。 |
| 6 | 自实际死亡日推进到下一真实月度脉冲并留一个日处理窗口，保存death-month。 | 若恢复day1仍为2202.08.08，单次`fast_forward 24`到2202.09.02覆盖9月脉冲及一日窗口。若实际day1已另推进，按真实日期重新算；不可硬套2200年的monthly helper。 |
| 7 | 实际原生load刚保存的death-month，再执行同一dead_sync，`fast_forward 1`。 | 若death-month确为2202.09.02，则2202.09.03保存death-reload。此已毁档reload不可省，才覆盖加载后不复活；其它功能之后加载其本来需要的活舰锚点，不额外做一轮“恢复母舰”专用load。 |

低/高级普通舰必须是原11个ID `0/1/2/3/4/5/804/805/806/807/808`，同design body和owner。逐舰十项getter真实相等才接收；包括民船/原生星基，不笼统称战斗舰。ship_size不是juggernaut的其它对象如新出现或缺失，实际记录，不能默默丢弃。

恢复branch只用正向reduce_shield、damage_ship、reduce_hp；不治疗、不换装、不调tier、不编辑SAV。Mother14的原十getter在C20500重新导出，取代旧图分支残留的C10000诊断缓存；两percent/two regen_mult与静态恢复分列。不能由满血或UI伤害值宣称实际恢复；实际H/A恢复可以受百分比AUTO_REPAIR及原生非战斗倍率影响，不在此临时拟合闭源日恢复公式。

death branch保持C20500/L2050/R410/P0和六历史层63/74/76/63/56/78的真实来源；这些是输入的既有值，after仍须实际读取，不能预填PASS。snapshot_state从live0变history1符合既有合同；历史country tier不是活装备。核心/国家/grant flags必须存活，否则core guard会使“不复活”归因混淆。原舰队/舰船可在引擎清理tick后消失或保留明确dead墓碑，核全表与actor所属列表，确认无新Mother设计/flag/modifier/juggernaut替代ID、EEP target不指新活舰。跨月维护与库存自然变化不要求恒等。

该顺序只需三次必要原生load：低级输入、高级输入、已毁after；六次新原生save（低/高级getter各一、damage0/day1各一、death-month/death-reload各一），活舰probe四条effect加death两条及reload dead_sync一条，共七条effect；日期命令FF1、到下一月窗口、reload后FF1三条。首日恢复若需有限附加窗口另按真实结果记录，不预设额外存档或循环。本页未创建这些未来文件。

## 既有SAV读取接口及字段

### 1020恢复执行补充

实际继续使用新run20261019T204055Z／PID24520。等C/D原生载入链结束后才导入
成长输入，避免活动载入列表因新文件重排。低／高输入仍用本页两个原SHA；
输出采用r9growthlow/high/hurt/day/deadmonth/deadload独占名，不改原计划和命令。
当前只读原高档已核ship809属fleet125，H3396960、A2873613.6、S4718142且三项
满额，满足原伤害探针安全上界；实际加载导出后仍须在新SAV重新核H/A>200000、
S<10000000、核心可用、无战斗与维修订单，事前记录后才输入正伤害命令。
普通舰11身份及十getter必须完整实测，缺项不得当0；若长输入解析失败，保留
原始失败，按同一冻结getter原文分段重发缺项后另存新版本，不删检查或改阈值。
新伤档先核真实H/A下降且max和账本不变，再仅FF1检验自然恢复；不能从满血、
命令输入或静态恢复系数推断已恢复。后续死亡严格沿本页月脉冲及已毁档重载。

已存在Mother时，可用 `check_growth_1019.read_save(save_path, expected_sha)` 读取CRC/实际date、owner、fleet/ship、country_variables、fleet_variables、ship_variables、health、layout和三防控制舰max；`receipt_save(receipt_path)`另核receipt SHA/date。但**该函数要求唯一真实活Mother，死亡after不可用它**；其ordinary_ships也只投影三防max，不能拿它证明普通舰十个getter。

普通舰十getter和死亡after沿现有 `testing/inspect_1019.py:288` 的 `observe(save_path)`：必须对真正已保存、receipt/audit/manifest齐备且属于当前RC7运行的源artifact路径调用，再按既有归档规则冻结输出；不要直接把canonical只读包目录当原active-run新输出，也不要用其可能扫描的receipt metadata推断未来SAV。本页不调用observe或读取活动metadata。

该observer已有完整原生字段，可直接取：

```python
obs["date"]
obs["country_variables_all"]
obs["event_targets"]
obs["fleets_1019"][fleet_id]["native"]
obs["fleets_1019"][fleet_id]["ships"][ship_id]["variables"]
obs["fleets_1019"][fleet_id]["ships"][ship_id]["native"]
obs["fleets_1019"][fleet_id]["ships"][ship_id]["design"]
obs["worlds_1019"][core_id]
```

`fleet_id/ship_id/core_id`均用实际字符串ID。ordinary需要遍历原11个ship ID对应的actual fleet，再从ship.variables取完整 `eep_probe_<modifier>`；不是从country变量或旧“ordinary_ships最大三防”摘要取值。实际health直接在ship.native的hitpoints/armor_hitpoints/shield_hitpoints及max_*字段；字段省略时保留缺失事实，不能伪造显式0。

死亡全银河/actor所属扫描可在同一次观察的完整gamestate用现有 `audit_save.fields/scalars/block/ids` 读取根 `ships`/`fleet`/`country` 容器，沿 `country0.fleets_manager.owned_fleets` 校验所有实存舰队/舰船；observer本身保留所有己方/绑定Mother/Relic舰队，不要求死Mother仍存在。国家flags可从 `obs["country"]["flags"]` 或原生country.flags读取实际投影（先核实际结构），不能用旧before flags替代after。保留所有其它实际变动，不调用旧growth reader给死亡状态制造接口FAIL。

以上只是现有接口/字段整理与操作合并，未运行任何未来验收。原三probe/两损毁命令、source fixture和所有旧报告保持原字节。
