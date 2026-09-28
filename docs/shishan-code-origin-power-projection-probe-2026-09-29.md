# 力量投射影响力受控探针（2026-09-29）

## 目标与边界

关闭 RS-02/RS-03 中“力量投射影响力是否被局势产出倍率正确覆盖”的待测点。已有同一基线分支的第二/第五阶段收入为 `1.17646/0.2`，但原版 `navy_coverage_shortage` 对 `country_power_projection_influence_produces_mult` 另有 `-1` 修正，低海军覆盖率可能触及最低收入，因此不能直接把 `0.2` 当作第五阶段脚本漏项。

本轮仅在隔离简体中文测试存档内造舰，不改正式 Mod 或原版文件。先从已归档的第二阶段存档加载，在玩家首都恒星创建一支由玩家拥有的护卫舰测试舰队，使海军覆盖率达到 `1`；保存共同基线。然后从共同基线分别设局势进度 `300` 与 `1000`，固定舰队、帝国规模、其他修正，各跨过同一次月结算后读取 `budget.current_month.income.country_power_projection.influence`。同时核对 `gamestate` 的 `navy_coverage`、舰队规模及局势阶段。

执行前检查发现，已归档的 PR-05 隔离存档 `pr05_mining_capacity_no_trait_month.25.sav` 的玩家国家本来就有 `navy_coverage=1`、`fleet_size=75`、力量投射收入 `2`。因此改用此存档作为共同基线，无须人为造舰；避免造舰夹具引入额外舰队变化。两支从该存档分别切到进度 `300/1000`，跨过同一次月结算。只有无法保持覆盖率 `1` 时才回到造舰方案。

## 通过标准

两支必须有相同且非零的海军覆盖率，最好均为 `1`；收入非零且第五阶段恰为第二阶段的 `0.25`（容许 UI 舍入）。若仍被原版下限截断，增加合法护卫舰或记录无法隔离的原因，不能直接记为通过。保存控制台效果、原版脚本出处、双方存档与哈希；试验舰队不得进入正式发布内容。若对照发现第五阶段漏修正，先更新设计，再修改 Mod 并重跑 `open_kaishek` 与实机回归。

## 执行结果

在 `pr05_mining_capacity_no_trait_month.25.sav` 同一 `2207.10.25` 基线分别设置进度 `300` 和 `1000`，使用游戏控制台 `effect root = { every_situation = { set_situation_progress = N } }`。两支均自然跨过 `2207.11.01` 月结算，并于同日 `2207.11.05` 暂停保存。Steam F12 的[第二阶段](../assets/shishan-code-origin/evidence/power-projection-stage2-2207.11.05.jpg)和[第五阶段](../assets/shishan-code-origin/evidence/power-projection-stage5-2207.11.05.jpg)画面确认阶段分别为 II/V，后者进度停在 `1000/1000`。

| 从同一基线分支读取的玩家国家字段 | II 阶段 | V 阶段 |
| --- | ---: | ---: |
| `navy_coverage` | 1 | 1 |
| `fleet_size` | 75 | 75 |
| `empire_size` | 50 | 50 |
| `budget.current_month.income.country_power_projection.influence` | 2 | 0.5 |

第五/第二正好为 `0.25`，且两支舰队和覆盖率不变。因此力量投射影响力也只受到一次第五阶段 `-75%` 修正，RS-02 中此来源子项通过。原先低覆盖率夹具的 `1.17646/0.2` 由原版 `navy_coverage_shortage` 与低端截断共同干扰，不应解释为本 Mod 漏项。原版脚本证据：`common/static_modifiers/00_static_modifiers.txt` 的 `empire_base` 给力量投射影响力基础值 `2`，`navy_coverage_shortage` 给此来源独立 `-1` 倍率；存档中覆盖率与预算由游戏实际结算确认。此次未改正式 Mod。

[第二阶段存档](../assets/shishan-code-origin/evidence/power-projection-stage2-2207.11.05.sav) SHA-256 `66593691a17fba39f73911c76601fccbb0be685206755da8ca222ca33a162dab`；[第五阶段存档](../assets/shishan-code-origin/evidence/power-projection-stage5-2207.11.05.sav) SHA-256 `449260bf26258fe499e3d87ca5742dce55a5b56a638f2f76e0e182c20fea3cc8`。
