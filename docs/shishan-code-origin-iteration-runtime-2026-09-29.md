# 优化迭代实机数值验收（2026-09-29）

## 目标与方案

PR-05 的两层正面特质池耗尽后，会在四类可重复“优化迭代”中随机发放，每类计数可叠加。已有同日存档确认四类计数写入和重载，以及岗位效率计数 `1→2` 的简中提示；本轮进一步验证实际人口/岗位数值，避免只凭说明文字判断。正式 Mod 不改，测试只在隔离简体中文存档中进行。

首先从已有的 `2207.11.05` 第二阶段、海军覆盖率对照存档出发，该存档的首都矿工容量为合法 `2000`，岗位未满员。分别从同一存档创建两支：在玩家国家作用域将 `shishan_code_iteration_output` 设为 `1` 或 `2`，并给主体机械物种添加一次 `trait_shishan_iteration_output`；每支跨过同一个月结算后，比较主体物种特质计数、矿工已分配人数、有效劳动力、岗位矿物产出和维护费。每层设计值是 `pop_bonus_workforce_mult=+0.01`，因此相同人口和岗位下增加一层应提高约 `1%` 基础劳动力；还需确认是否有额外维护费副作用，不能把实测产出变化全部归因于该层。

随后用相同基线方式检查机器人维护费、住房使用和研究员劳动力三类：各自设 `1/2` 层，跨月读取相应 UI 和预算来源，固定人口及岗位容量。若某项不能构成稳定非零样本，记录待测而不猜测。每类保留存档、截图及 `gamestate` 变量/特质计数，并核对两层之间只多发一层、不是复制第二个特质。压力池抽签与本轮直接设变量的数值夹具分开记录；数值夹具不证明随机权重。

认知缓存预检查：首都现有物理学家岗位面板显示 `60/60`，已经满劳动力，直接比较科研产出可能被容量上限遮蔽。两分支在同一基线各增加相同数量的原版 `building_research_lab_1`，先确认游戏保留这些合法建筑及物理学家岗位未满员，再跨月比较；原版该建筑使用 `inline_script jobs/researchers_add`。若建筑上限或分配使研究员仍满员，应改用数量相同的未满员科研岗位，不能把零变化判为特质无效。

探针补充：在临时分支加到物理学家 `300/300` 后，再加研究实验室被游戏拒绝，`error.log` 明确记录 `add_building: failed to add a building`，说明建筑槽位已满；继续加都市区划也达到星球区划上限。第一种 `random_owned_pop_group = { remove_pop_amount = 800 }` 会随机命中不同职业阶层的人口组，重复执行导致测试分支人口归零并触发游戏结束，不能作为稳定夹具。从已归档的 `2207.11.05` 存档重载，添加四座合法原版实验室；随后参照原版 `machine_age_situation_events_3.txt` 的 4.5.1 语法，只选择 `is_pop_category = specialist` 的人口组，使用 `kill_pop_group = { pop_group = this amount = 500 }`，月结算后再减少 `700`，使科研岗位未满员。将此稳定的 `2208.01.06` 未加迭代特质状态存为共同基线，然后分别设层数 `1/2` 并各添加一次特质，推进同样的 30 日。此人口缩减仅用于隔离数值夹具，不是 Mod 正式游戏流程。

## 通过标准

四类每增加一层均产生与正式定义一致的实际效果，主物种只有一个对应特质，其他物种不受该物种特质影响；存档重载后层数与数值不丢失。若游戏采用异步刷新，观察至月结算并用相同日期的分支比较；不能把即日未变化直接当成失败。

## 岗位效率迭代：已执行

从同一 `2207.11.05` 第二阶段存档分别设 `shishan_code_iteration_output=1/2`，给主物种各添加一次 `trait_shishan_iteration_output`，两支均推进至 `2207.12.05`。游戏简中矿工岗位面板如下：

| 层数 | 劳工总数 | 矿工有效劳动力 | 矿物岗位产出 | 岗位维护费：能量/矿物 |
| ---: | ---: | ---: | ---: | ---: |
| 1 | 945 | 1042/2000 | 49.00 | 10.32/2.58 |
| 2 | 945 | 1051/2000 | 49.45 | 10.32/2.58 |

同一人数、同一合法岗位容量、同一日期，增加一层后矿工有效劳动力增加 `9`，约等于 `945×1%` 的显示整数；矿物产出增加 `0.45`，与此前约 `0.04706` 的每单位劳动力产出相符。岗位维护费在面板显示精度内没有改变。两份 `gamestate` 均只有一个迭代特质，变量分别为 `1` 和 `2`；实测符合“一项特质按国家计数叠加”的实现。此为**数值夹具**，未代替自然项目完成和随机抽签验收。

[一层画面](../assets/shishan-code-origin/evidence/iteration-output1-2207.12.05.jpg)、[一层存档](../assets/shishan-code-origin/evidence/iteration-output1-2207.12.05.sav) SHA-256 `bf7f8696979f8ff79af0ddd7cacf33f4f3ecb5b03b797f732d11d4f9786e9ba7`；[两层画面](../assets/shishan-code-origin/evidence/iteration-output2-2207.12.05.jpg)、[两层存档](../assets/shishan-code-origin/evidence/iteration-output2-2207.12.05.sav) SHA-256 `ad1ef6930373d19ec73bac00f4618af8b10a9e53104c66dc3f42f9efa21ca5c4`。

## 供能调度迭代：已执行

同一 `2207.11.05` 基线分别添加一次 `trait_shishan_iteration_energy` 并设置计数 `1/2`，两支推进到相同的 `2207.12.05` 月结算后保存。两支主体物种均只有一个该特质，人口总数均为 `2645`。玩家预算的 `current_month.expenses.planet_pops.energy` 分别为 `28.7651` 和 `28.5012`，增加一层使每月人口能量维护费下降 `0.2639`（约为原总额的 `0.918%`）。该特质定义只修正机器人维护费组成项，预算来源还可能含不受该键影响的维护费；因此不能把总预算的相对变化要求为严格 `1%`。方向、数量级和同人口条件支持“每层 `-1%` 机器人维护费”在实机生效；更细的原版组成拆分仍可补充。

[一层存档](../assets/shishan-code-origin/evidence/iteration-energy1-2207.12.05.sav) SHA-256 `fb5115a9de2033ba063612057fc8725783e982482853583c335e7635230830d9`；[两层存档](../assets/shishan-code-origin/evidence/iteration-energy2-2207.12.05.sav) SHA-256 `88c6a355fadb0001de502ce2500df8cc0a36a0aa13842701173abb1dc63bec73`。此项同样是直接设变量的数值夹具，不证明奖励池抽签概率。

## 空间调度迭代：已执行

从同一基线分别设置 `shishan_code_iteration_assembly=1/2`，给主物种各添加一次 `trait_shishan_iteration_assembly` 并跨过相同月结算。首都住房悬浮说明在一层时显示人口 `2645`、人口住房需求 `2618`；两层时人口 `2646`、需求 `2593`。两支各自符合 `2645×0.99≈2618.55`、`2646×0.98≈2593.08` 的 UI 整数显示。人口在随机分支中多出一名，所以不能直接将 `2618−2593` 全部解释成单层效果；按各支人口归一后，每层 `-1%` 住房需求吻合设计。两个存档的计数为 `1/2`，对应特质均只出现一次。

[一层住房画面](../assets/shishan-code-origin/evidence/iteration-housing1-2207.12.05.jpg)、[一层存档](../assets/shishan-code-origin/evidence/iteration-housing1-2207.12.05.sav) SHA-256 `3d41fff54b0e39c56c9d834a17a5573943c19b51ce58da339e35d0b8541607b9`；[两层住房画面](../assets/shishan-code-origin/evidence/iteration-housing2-2207.12.05.jpg)、[两层存档](../assets/shishan-code-origin/evidence/iteration-housing2-2207.12.05.sav) SHA-256 `0dab38127da7ef73897a048e5d222adad301078a01a847ba7e2758effff3ce1a`。

## 认知缓存迭代：已执行

两支均从相同的 `2208.01.06` 未满编科研岗位夹具分支，各添加一次 `trait_shishan_iteration_experience`，变量分别设为 `1/2`，推进到 `2208.02.06`。物理学家均分配 `200/300`，研究岗位物理学产出从一层 `7.88` 增至两层 `7.95`，增加 `0.07`，约为原值的 `0.89%`；这是岗位面板两位小数下与每层 `+1%` 劳动力修正相符的数值。物理学家提示中的能量维护费两支均为 `2.20`，另一项维护费从 `4.43` 到 `4.46`，因此该键也可能轻微增加随有效劳动力计费的岗位维护费。不能声称此增益完全没有维护费副作用。两份 `gamestate` 均仅含一次对应特质，计数变量分别为 `1/2`。本项证明固定岗位与人口夹具中的实际产出差异；它不证明自然项目奖励的随机权重。

[一层画面](../assets/shishan-code-origin/evidence/iteration-research1-2208.02.06.jpg)、[一层存档](../assets/shishan-code-origin/evidence/iteration-research1-2208.02.06.sav) SHA-256 `45bf847d0ea6f332d7ecfe80107afe2162ae1dfc6f2cdf6af0644278289eac19`；[两层画面](../assets/shishan-code-origin/evidence/iteration-research2-2208.02.06.jpg)、[两层存档](../assets/shishan-code-origin/evidence/iteration-research2-2208.02.06.sav) SHA-256 `e6356400a90e250ea1715f6c40375c4beef7d0eb221aa20c0817d98df37ad8d6`。

## 本轮闸门与边界

正式 Mod 未改。2026-09-29 重新执行 `py C:\workspace\open_kaishek\tools\accept_stellaris_mod.py --mod shishan_code_origin --game "C:\Program Files (x86)\Steam\steamapps\common\Stellaris" --report _runtime\shishan_code\accept_iteration_20260929.json`，结果 `PASS`：19/19 脚本、13 DDS、167 本地化键。`audit_compat_traits.py` 对 19 个机械兼容特质映射 `PASS`；`audit_translations.py` 对八种非中非英语言各为 0 个英语原文残留与 0 个汉字占位，英文及其余语言的键/引用由包级工具核对。九种非简中语言结论仅为**静态校验通过，运行时不在范围内**。`git diff --check` 为 0。四类迭代的实机数值子项已覆盖，Mod 整体验收仍受其他待测场景限制。
