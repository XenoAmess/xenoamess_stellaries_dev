# 「重构完成」同日岗位产出对照（2026-09-28）

> 本文记录已被替换的物种劳动力效率方案，用于追溯为何改动；正式候选版已改为全国岗位产出修正。正式方案及同日实机结果见[验收报告](shishan-code-origin-acceptance-report-2026-09-27.md)。

## 目标与口径

按[验收方案](shishan-code-origin-acceptance-plan.md) PR-03，从同一份 2228.03.11 暂停存档分别观察清理前后：主体机械物种特质替换、局势结束、岗位实时产出提高、非岗位产出不因「重构完成」受到额外加成。正式单 Mod、简体中文、Stellaris 4.5.1，Steam 离线。清理分支通过游戏控制台 `complete_special_project` 调用真实项目完成效果；第五阶段的自然研究完成另见[自然清理验收](shishan-code-origin-clean-natural-2026-09-28.md)。

## 同日结果

| 项目 | 清理前 | 清理后 | 证据 |
| --- | ---: | ---: | --- |
| 日期 | 2228.03.11 | 2228.03.11 | 下述截图与两份存档 |
| 主体物种「屎山代码」 | 1 | 0 | 存档 `species_db` |
| 主体物种「重构完成」 | 0 | 1 | 存档 `species_db` |
| 局势/项目 | 第二阶段；维护及清理可用 | 局势消失；持续优化可用 | 游戏 UI 与存档 |
| 采矿子个体，800 劳动力的矿物产出 | 40.83 | 50.11 | [前](../assets/shishan-code-origin/evidence/refactor-stage2-miner-before-2228.03.11.jpg)、[后](../assets/shishan-code-origin/evidence/refactor-stage2-miner-after-2228.03.11.jpg) |
| 物理学家，60 劳动力的物理学产出 | 2.07 | 2.55 | [前](../assets/shishan-code-origin/evidence/refactor-stage2-physicist-before-2228.03.11.jpg)、[后](../assets/shishan-code-origin/evidence/refactor-stage2-physicist-after-2228.03.11.jpg) |
| 物理学家维护费 | 2.64 | 3.09 | 同上两张物理学家截图 |
| 国家基础能源/月、矿物/月 | 40、40 | 40、40 | 两份存档 `budget.current_month.income.country_base` |
| 采集站能源/月、矿物/月 | 11、11 | 11、11 | 两份存档 `budget.current_month.income.orbital_mining_deposits` |

前后存档分别为 [清理前](../assets/shishan-code-origin/evidence/refactor-stage2-before-2228.03.11.sav)（SHA-256 `5CDEADFB7F41C3AF13BFCDABDB3819145C9F4B957B53A730696C9BC16CAE3161`）和[清理后](../assets/shishan-code-origin/evidence/refactor-stage2-after-2228.03.11.sav)（SHA-256 `BF5D310EBEBFEFFA92511C4C948E5C83A47863068159A330C2E66B62F88FE375`）。

## 4.5.1 引擎观察

该物种特质使用原版机械正面特质同样支持的 `pop_bonus_workforce_mult = 0.25`。在已有其他岗位修正的存档里，`+25%` 以修正项叠加，实时采矿产出实际由 `40.83` 到 `50.11`（约 `+22.7%`），不应机械地要求当前值恰为 `×1.25`。同一个劳动力修正还会提高按有效劳动力计费的岗位维护费：物理学家从 `2.64` 到 `3.09`。因此现有实现确实提高岗位产出，但「仅产出、维护费不动」不能由这一物种修正保证；如将需求严格解释为后者，须另行设计适用范围。游戏存档的 `budget.current_month` 在同日切换特质后乃至推到 2228.04.16 仍记录切换前的部分岗位条目，不能单独用这个字段判定即时岗位效果；本项采用同日、同劳动力的游戏实时岗位悬浮提示，并用存档核对特质与非岗位来源。
