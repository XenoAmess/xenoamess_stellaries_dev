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

## RC4 最小原版末殖民地对照计划（尚未执行）

目标仅为校准：同一未毁目标的原版 `PLANET_KILLER_CRACKER` 完成 callback 是否也在“毁掉末殖民地 → 国家消失／战争结束 → nomads.94”路径产生同一无效 from 错误。必须等待 root 的新 RC4 修复门禁通过，独立分支原生载入 `pk1ready`，不用 RC3 的真实时长 FAIL 作为 RC4 的结论，也不把 callback 调用当实际武器发射验收。不得改 Mod 或全局 on_action。

静态接口依据如下：

- 已冻结 `logs/script_documentation/effects.log:2317–2319` 明确 `fire_on_action = { on_action = <string> scopes = { from = X fromfrom = Y } }`，支持全部作用域。
- 本机 `common/on_actions/01_planet_destruction.txt:14–24` 定义 `on_destroy_planet_with_PLANET_KILLER_CRACKER`；它先派发 `crisis.5015` 等事件，再派发 `planet_destruction.100`，源码 :21 明确此事件可能杀死国家。只调用这个真实完成 callback，不模拟 queued／unqueued 或宣称经历了充能／发射。
- **FROM 保持 Mother fleet，与实际 EEP 入口同形。** 同文件 :1–3 明确 FROM 为发射舰队；冻结的 `scopes.log:58–60` 明确 `fleet` 转换支持输入 fleet，故 `from.fleet.owner` 不能证明 FROM 必须为 ship。冻结的 `triggers.log:1083–1085` 同样明确 `is_ship_size` 支持 fleet，不能因 `is_arkship_ship` 的名称推断只接受 ship。root 已通过真实 EEP 入口的 `from = { is_same_value = event_target:eep_mothership@owner }`；本对照优先显式使用 `scopes = { from = event_target:eep_mothership0 }`，执行前核对该 event target 确为当前 Mother fleet。此前“改传 Mother ship”的提案来自未查完整作用域目录的推断，现明确撤回；原生摘录及冻结日志保持原样。
- 原版 `planet_destruction.100` 会设置 flags／外交、威胁与厌战等状态（源码 :104–121、:123–280），杀人口、破坏轨道防御与建筑（:282–291），并把普通宜居星改为碎裂星球、随机留下矿藏（:313–332）。这些都是对照分支的原生副作用，不并入 EEP 吞噬奖励。

最小执行和留证顺序：

1. 绑定 RC4 不可变 snapshot、open_kaishek 修复后的通过证据、EXE／descriptor／Mod tree／语言，记录原始 `pk1ready` SHA256 `11149f60e725625393adececf6481f1dffc9b9364cc1c6fb46e3f76f328eb0ba`。实际载入后另存对照前原生 SAV，保留 audit／receipt 与全部严格差异，不覆盖原准备档。
2. 只读确认 physical planet17 仍存在且未毁，owner、真实殖民地与母舰所属国、实际战争、敌国现存殖民地数、`event_target:eep_mothership0` 的 Mother fleet 身份及其实际 ship 关联均符合原基线；记录 EEP 国家／Mother 变量、资源与计分基线。若已不是敌国末殖民地，此对照不回答原问题。
3. 记录日志原字节数、SHA256、执行 UTC 与游戏日期；在已验证的 planet17 作用域通过本机支持的 `fire_on_action` 派发上述原版完成 callback，显式使用 `scopes = { from = event_target:eep_mothership0 }`（Mother fleet）。不调用 EEP 完成回调、EEP 结算或 EEP 修改器，不编辑 SAV，不新增诊断脚本。精确实际命令与提交 receipt 必须保存，不能把方案占位符当可执行 API。
4. 保存对照后原生 SAV、audit／receipt、完整前后差异、日志新增原始字节及其源偏移／SHA256。核对 planet17、敌国／战争消失情况以及是否出现同一 `nomads_events_1.txt:2268`／无效 from，另列一切其它错误和未知变化。原版 menace／外交／厌战／flags／人口／资源／矿藏等变化全部原始留证，不静默筛掉，不与 EEP 结算收益合并。
5. 实际原生 reload 未毁的 `pk1ready` base，再保存并核对恢复后的目标、国家、战争和关键 EEP 状态，保留重载造成的严格差异。未执行 reload 前不称“已恢复基线”。对照文件只属于此独立分支。

结果解释：同错误重现，仅支持“该原版末殖民地完成路径能够重现”，不能证明 EEP 没有缺陷；未重现，则需比较两分支的实际作用域／战争／国家状态，不能据此直接断言 EEP 是唯一原因。若 callback 本身出现传错作用域等错误，该控制无效，保留失败证据。真实武器 90／30 时长及其它最终 case 仍需独立实测。

尚未确认一个静态上更小且等价的自然战争结束对照。直接结束战争绕过末殖民地销毁，不能代替本计划；没有采用未文档镜头、战争结束或模拟发射 API。本节仅方案，未操作 UI 或游戏。
