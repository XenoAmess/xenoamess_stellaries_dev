# RC3 结束后日志冻结与受限审阅

## 目标与范围

主线程已正常关闭 `20261019T092935Z` run：PID 34832，停止时间 UTC 2026-10-19 11:16:49，`forced=false`、`running_after=false`。本任务先确认停止证明与源进程不再运行，再将该 run 的完整 `logs`（含全部 `script_documentation`）按原字节归档到 `docs/evidence/1019-rc3-final-logs/`，同时复制 run manifest、process、stop 证明。不得复制 SAV、其它分支或其它 run，不操作 UI／Steam／Mod，不提交。

## 设计与验收标准

1. 只接受指定 run 的停止记录、正确 PID 和源进程已停止；活动日志不得标记 frozen。
2. 枚举源日志全部文件，复制前后逐一计算 SHA256／字节数，核对源文件集合未变、源内容未变、归档内容完全一致。保留独立 index 与复核报告，明确原始路径和复制时间。
3. 独立验证再次读取源与归档，不依赖复制成功返回值；归档必须包含全部脚本文档和三个运行证明。
4. 完整审阅 error.log／game.log，逐项区分已知启动警告、已记录的 hw0 手工命令错误、真正新增 EEP 运行错误和未知项，不静默过滤。
5. 日志证据只支持所检查的有限范围；RC3 巨像 90／30 时长已经 FAIL，日志无错不得更改此结论。Machine／Hive 最终 case 仍为 PENDING。

## 执行与结论

已完成，只修改本说明及 `evidence/1019-rc3-final-logs/`。源 PID 在复制前、复制后和独立复核三次均为 ABSENT；stop 证明为正常退出。19 个日志（含全部 5 个 script_documentation）加 manifest／process／stop 共 22 个原文件、5,950,376 字节，复制前后源集合和 SHA256 不变，归档逐一匹配。独立 `verify.py` 再读全部源与副本，`verify.json` 为 PASS；原始载荷另设 `-text` 并以 `git-byte-verify.json` 核对全部 22 个预期 Git blob 无换行归一化。

归档索引 [index.json](evidence/1019-rc3-final-logs/index.json) 的 SHA256 为 `8312c071af1918715a390af3702d800d51574181c1c5cace868b7b2436c0c95e`。完整审阅见 [review.md](evidence/1019-rc3-final-logs/review.md)／[review.json](evidence/1019-rc3-final-logs/review.json)，没有静默过滤。

error.log 共 42 物理行／26 记录：21 条缺失 Workshop 发现、1 条预期 native 决议覆盖、1 条 portrait_container 与历史 baseline 仅时间不同；2 条 hw0 诊断失败精确关联已冻结的 unsupported every_ship 手输命令。最后新增 1 条原版 `nomads.94` 在 `events/nomads_events_1.txt:2268` 的无效 from 上下文错误，捕获 from.id=4294967295；源定义及 on_action 挂接已摘录并哈希，是否由 EEP／巨像结算触发及影响仍未解决，不能称日志无错或无害。完整 game.log 的 19 行均逐条记录为有限的信息证据，不能单独证明功能通过。

RC3 巨像 90／30 时长 FAIL 保持；Machine／Hive 最终 case 仍 PENDING。归档路径与这些限制已发 release_pipeline，不把受限日志审阅变为最终验收通过。

## RC4 最小原版末殖民地对照计划（历史方案）

本节保留执行前设计。主线程随后已完成原版 callback 对照及实际 base 载入恢复动作；稳定 B／P／Q／R、结果 SAV 与限定结论见 [RC4 原版对照分析](rc4-native-cracker-control-analysis-2026-10-19.md)。本节的“未执行”仅描述原先方案与本线程不操作 UI 的边界，不代表后续对照仍未开展。

目标仅为校准：同一未毁目标的原版 `PLANET_KILLER_CRACKER` 完成 callback 是否也在“毁掉末殖民地 → 国家消失／战争结束 → nomads.94”路径产生同一无效 from 错误。必须使用 root 的新 RC4 修复门禁证据，按最新安排独立分支原生载入 `pk2base`，不用 RC3 的真实时长 FAIL 作为 RC4 的结论，也不把 callback 调用当实际武器发射验收。原 `pk1ready` 只是最初未执行的计划基线，已由 `pk2base` 替代。不得改 Mod 或全局 on_action。

静态接口依据如下：

- 已冻结 `logs/script_documentation/effects.log:2317–2319` 明确 `fire_on_action = { on_action = <string> scopes = { from = X fromfrom = Y } }`，支持全部作用域。
- 本机 `common/on_actions/01_planet_destruction.txt:14–24` 定义 `on_destroy_planet_with_PLANET_KILLER_CRACKER`；它先派发 `crisis.5015` 等事件，再派发 `planet_destruction.100`，源码 :21 明确此事件可能杀死国家。只调用这个真实完成 callback，不模拟 queued／unqueued 或宣称经历了充能／发射。
- **FROM 保持 Mother fleet，与实际 EEP 入口同形。** 同文件 :1–3 明确 FROM 为发射舰队；冻结的 `scopes.log:58–60` 明确 `fleet` 转换支持输入 fleet，故 `from.fleet.owner` 不能证明 FROM 必须为 ship。冻结的 `triggers.log:1083–1085` 同样明确 `is_ship_size` 支持 fleet，不能因 `is_arkship_ship` 的名称推断只接受 ship。root 已通过真实 EEP 入口的 `from = { is_same_value = event_target:eep_mothership@owner }`；本对照优先显式使用 `scopes = { from = event_target:eep_mothership0 }`，执行前核对该 event target 确为当前 Mother fleet。此前“改传 Mother ship”的提案来自未查完整作用域目录的推断，现明确撤回；原生摘录及冻结日志保持原样。
- 原版 `planet_destruction.100` 会设置 flags／外交、威胁与厌战等状态（源码 :104–121、:123–280），杀人口、破坏轨道防御与建筑（:282–291），并把普通宜居星改为碎裂星球、随机留下矿藏（:313–332）。这些都是对照分支的原生副作用，不并入 EEP 吞噬奖励。

最小执行和留证顺序：

1. 绑定 RC4 不可变 snapshot、open_kaishek 修复后的通过证据、EXE／descriptor／Mod tree／语言。最新准备档为 run `20261019T112808Z` 的 `pk2base`，原生日期 2200.03.07、SHA256 `be5a344439dafe105d4959b4afa31143331b1daaaf915dba28bc70ee23f6f2e2`。只读解包原档的 saved_event_target 已确认 `eep_colossus_probe_target` 是 planet17、`eep_mothership0` 是 fleet159；实际 reload 后必须再次核对。另存对照前原生 SAV，保留 audit／receipt 与全部严格差异，不覆盖原准备档。该读取没有执行重载或对照。
2. 只读确认 physical planet17 仍存在且未毁，owner、真实殖民地与母舰所属国、实际战争、敌国现存殖民地数、`event_target:eep_mothership0` 的 Mother fleet 身份及其实际 ship 关联均符合原基线；记录 EEP 国家／Mother 变量、资源与计分基线。若已不是敌国末殖民地，此对照不回答原问题。
3. 记录日志原字节数、SHA256、执行 UTC 与游戏日期；在已验证的 planet17 作用域通过本机支持的 `fire_on_action` 派发上述原版完成 callback，显式使用 `scopes = { from = event_target:eep_mothership0 }`（Mother fleet）。不调用 EEP 完成回调、EEP 结算或 EEP 修改器，不编辑 SAV，不新增诊断脚本。精确实际命令与提交 receipt 必须保存，不能把方案占位符当可执行 API。
4. 保存对照后原生 SAV、audit／receipt、完整前后差异、日志新增原始字节及其源偏移／SHA256。核对 planet17、敌国／战争消失情况以及是否出现同一 `nomads_events_1.txt:2268`／无效 from，另列一切其它错误和未知变化。原版 menace／外交／厌战／flags／人口／资源／矿藏等变化全部原始留证，不静默筛掉，不与 EEP 结算收益合并。
5. 实际原生 reload 未毁的 `pk2base` base，再保存并核对恢复后的目标、国家、战争和关键 EEP 状态，保留重载造成的严格差异。未执行 reload 前不称“已恢复基线”。对照文件只属于此独立分支。

结果解释：同错误重现，仅支持“该原版末殖民地完成路径能够重现”，不能证明 EEP 没有缺陷；未重现，则需比较两分支的实际作用域／战争／国家状态，不能据此直接断言 EEP 是唯一原因。若 callback 本身出现传错作用域等错误，该控制无效，保留失败证据。真实武器 90／30 时长及其它最终 case 仍需独立实测。

尚未确认一个静态上更小且等价的自然战争结束对照。直接结束战争绕过末殖民地销毁，不能代替本计划；没有采用未文档镜头、战争结束或模拟发射 API。本节仅方案，未操作 UI 或游戏。

### 完整命令与原生结果边界

确认实际重载后的两个 saved target 后，主线程计划使用下面一条 ASCII 原生 console 命令；本线程没有执行：

```text
effect event_target:eep_colossus_probe_target = { fire_on_action = { on_action = on_destroy_planet_with_PLANET_KILLER_CRACKER scopes = { from = event_target:eep_mothership0 } } }
```

调用对象、完整命令、准备档来源和原生文档位置另记 [rc4-native-callback-plan.json](evidence/1019-rc3-final-logs/rc4-native-callback-plan.json)。它派发原版完成 callback 的完整事件列表，非单独调用 `.100`；不能删掉原生计分／外交等副作用来使结果看似与 EEP 相同。普通宜居目标走 `.100:313–332` 的 `change_pc=pc_shattered`、清矿藏与随机矿藏分支，此前 :282–291 杀人口、毁轨道防御、移除建筑。国家消失及战争结束须实际对照 SAV／日志确认，不能因末殖民地假定必然按某个 FROM 传播。

`nomads.94` 的静态调查另见 [原生语义](nomads-94-native-semantics-2026-10-19.md)：只在 `on_war_ended`／`on_becoming_subject` 挂接，`on_colony_destroyed` 不直接调用它；没有证明 `destroy_colony` 必然传错 FROM，也没有原生依据把未文档的 `destroy_planet` 当修复。

### baseline／pre／post 日志偏移方案

日志仍由活动进程写入，以下只生成带来源偏移的**阶段观察**，不称最终 frozen run，也不覆盖 RC3 的 22 个原文件或索引。

1. `baseline`：实际原生载入 `pk2base`、确认暂停及前置状态后，记录每个源 `error.log`／`game.log` 的路径、run、观察 UTC、总字节数 B、前 B 字节 SHA256 与末行边界。该前缀用于保留此前启动、RC4 真实发射与重载诊断，不能清空日志。
2. `pre`：紧邻 callback 提交前再记录字节数 P 与前 P 字节 SHA256。验证其前 B 字节与 baseline 一致，保存原始区间 `[B,P)` 作为“载入／准备阶段”，不混为 callback 错误。动作 receipt 的实际 UTC、完整命令与游戏日期另列。
3. `post`：待主线程确认 callback 及相关事件处理、保存后原生档后，记录字节数 Q、前 Q 字节 SHA256，验证前 P 字节未变。派生原始区间 `[P,Q)`，记录 offset_start／offset_end、字节数与 SHA256，不作换行／编码归一化。若需完整行上下文，可另附从 P 前最后 LF 开始的重叠区间，但保留原始精确偏移，不能隐去边界外错误。
4. 源变短、前缀变化或发生轮转即判 append 假设失败；保留事实并重建明确的时间片，不能沿用旧 offset 或声称“无新增错误”。读取期间可能增长时只哈希明确长度的已读取前缀，记录实际读取 UTC／长度；后续增长属于下一观察段。
5. 实际 reload base 后另记录 `restore` 的后续区间 `[Q,R)`、原生 SAV 和 receipt，区别恢复／重载告警与 callback 诊断。最终进程停止后再由既有冻结流程保存该 run 全部日志；阶段区间不能代替最终完整日志审阅。所有 unknown 与 `nomads.94` 错误保留，不按名称自动过滤。
