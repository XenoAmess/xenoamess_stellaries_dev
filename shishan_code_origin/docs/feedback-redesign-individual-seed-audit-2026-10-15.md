# 个体机械旧档作为维护续玩种子的只读审查

日期：2026-10-15。只读解析原生 ZIP 存档与历史文档，不操作游戏、不改生产文件、不创建新夹具。提取结果见 [原生字段证据](evidence/feedback-redesign/runtime-2026-10-15/individual-machine-seed-audit.json)。

源文件 `assets/shishan-code-origin/evidence/individual-machine-2203.05.22.sav`，SHA-256 `3bff62df806073a10e53364cd0150dee8f9af61815675050e34038ffd4ba88e8`；当前 run `20261015T074214Z` 中 `save games/acceptance-fixtures/` 的同名副本与源文件逐字节相同。源版本为 Cygnus 4.5.1，日期 2203.05.22；不能把源内旧缓存当作已在 4.5.2/rc.3 重算的数据。

## 可直接用于操作决策的事实

| 项目 | 源档事实与取证路径 |
| --- | --- |
| 玩家与政体 | `player[].country=0`；`country[0].government.authority=auth_democratic`、`type=gov_moral_democracy`，起源正确，非格式塔个体机械。 |
| 维护次数 | `country[0].variables.shishan_code_maintenance_count=0`；没有待领、refactored 或架构补丁层字段。 |
| 真实维护员 J | 原生 `pop_jobs[16777323]` 类型为 `shishan_code_maintainer`，首都 colony 0；`workforce=100/max_workforce=100`，pop group 13 分配 100。`bonus_workforce=10` 是另一字段，不并入脚本采用的已分配 J；当前 J=100。 |
| 局势 | 原生 `situations.situations[4]`：country 0、进度 199、阶段 0（I）、`last_month_progress=4.9`。4.9 是旧版 5−0.1 的历史缓存，不是 rc.3 观测。 |
| 项目 | `country[0].events.special_project` 中维护 ID 1、清理 ID 2；未存 status/research，国家三系 queue 均不存在。源内没有正在研究的维护或清理。n=0 对应新合同成本维护 2000、清理 8000。 |
| 社会学收入 | `budget.current_month.income.country_base.society_research=12.5`，`planet_biologists.society_research=5.80626`，合计 18.30626/月；last_month 合计 18.2893。均为旧版预算，加载后要过完整月重新取证。 |
| 储存科研 | `tech_status.stored_techpoints` 顺序为 physics/society/engineering，社会学 657.98021；三系已有 alternatives，auto_researching 均 no，尚未选择普通科技。 |
| 人口与特质 | 国内主体谱系实际人口 5029，唯一实际模板正式特质数 6；新架构正确迁移后的预期 U=6、R=0、B=0.30，尚不是本次只读审查的实机结果。 |

此种子有意义：可以正常 UI 启动维护，按真实研究队列跨月积累并触发成功回调，检查 n、奖励、成本与速度变化。它验证的是**旧档续玩及普通研究流程触发维护的功能**，不能代替从 2200 开始的新局自然平衡样本。

以 n=0/J=100 开始，新合同月速应为 **0.75**。此状态不能单独证明 J=0 时基础为 1。若需要实测，可正常 UI 暂停研究所或禁用维护员岗位，确认原生 J=0 后跨完整月，检查进度差 1；再正常恢复岗位，确认 J=100 后进度差 0.75。这是合法经营操作，但仍须记录停工/复工与就业重分配，不能用建筑容量猜 J。

建议载入后先保存并跨一个完整月，让候选预算、架构与旧缓存更新；再选择一项普通社会学科技，随后在情报日志启动维护 ID 1。这样可以同时观察普通社会学研究被项目占用、原科技恢复以及自然成功回调。原档社会学每月约 18.3、储存约 658，成本 2000，不会立即完成；新岗位/架构/白绮和阶段重算后耗时应以真实 UI 预计与两份跨月存档中的 `society_queue`/research 变化为准，不给未验证的固定完工日期。期间不加科研 boost，不直接完成项目。

## console 与夹具来源边界

[2026-09-28 原始记录](../../docs/shishan-code-origin-individual-machine-2026-09-28.md)明确写该一所基线的建筑用正常资源和正常建造等待完成。也明确记录曾试图输入 `resource minerals 500`，但中文输入法将其连写，**无成功执行证据**；应披露这一 console 尝试，不能声称整个来源从未打开控制台。

同文后续的 instant_build 加速属于 2203.07.11 两所分支，不是此 05.22 一所种子。只读审查未发现已持久化的 `shishan_test_society_boost` 或其它明显科研加速 modifier；完整 country timed_modifier 只有正常 `game_start` 与白绮基值/工程学步进/社会学步进，后两者 multiplier=0。原生 `cheated_on_save=no`，但这不证明历史上没有任何 console 操作，也不证明没有任何外部配置影响。

此存档未序列化最终计算后的 `research_speed` 全量缓存。旧国家保留的是 modifier 键及倍率，加载时会由当前脚本重新解释；要核对 rc.3 白绮正社会学、普通领袖/帝国研究速度，请在新包加载并跨月后读取科研 UI 与新原生队列，不用旧缓存或“没有 boost 字符串”替代实际观测。

## 白绮与七名领袖、维护预算映射

白绮在此源档是 **leader ID 16777287、等级 5**，不是简单 ID 7；识别依据是专属 portrait、`leader_trait_shishan_code_vivhite` 与 `flags.shishan_code_vivhite`，country=0，当前无任职 location。

| ID | 类型/等级 | 身份或位置 |
| --- | --- | --- |
| 16777287 | official 5 | 白绮，传奇，专属 flag/trait，空闲。 |
| 167772189 | official 2 | `country[0].ruler`。 |
| 90 | official 2 | 首都总督，council position 12。 |
| 150994969 | scientist 2 | 科研船，council position 11。 |
| 150994968 | commander 2 | 舰船，council position 10。 |
| 134217755 | envoy 1 | 使节。 |
| 150994970 | envoy 1 | 使节。 |

准确取证路径是 `country[0].budget.current_month.expenses.leader_officials.unity`（旧档 18）与 `last_month.expenses.leader_officials.unity`（旧档 16）；指挥官/科学家对应 `leader_commanders.unity`、`leader_scientists.unity`，两个月都是各 2。`balance` 中相同类别是负值，不能和 expenses 相加。源档当前月与上月不同，本身就说明不能把两个不同时点差额直接归因于某位领袖。

这些预算按类别合计，存档此处没有白绮个人的支出行。验证“只免她自己”需要加载 rc.3 后她个人 UI 的凝聚力维护为 0，同时普通行政官的 UI 维护仍正常；并用同一任职/等级条件下的新存档预算类目交叉确认。不能只见 `leader_officials` 总额下降就宣告本人归零，更不能用 aggregate 总额反推一个未观测的个人值。新运行中的其它种子可能使用不同领袖 ID，须以该份存档实际 owned_leaders/专属 flag 重新定位，不能把此 ID 强套到其它世界。

本次只生成只读提取证据和此文档；没有修改存档、源脚本、生产包或游戏状态。实际续玩、UI 操作及自然成功仍由主任务执行。
