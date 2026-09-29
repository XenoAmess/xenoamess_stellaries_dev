# RS-01—RS-04 持续生产来源验收收口（2026-09-30）

## 范围与判定方法

按[总验收方案](shishan-code-origin-acceptance-plan.md)核对岗位、非岗位持续生产、同资源混合、排除项及原版加成。标准化的 `P_job=100/P_nonjob=40` 是口径示例；真实原生存档采用可复现的原版基础量，以同基线各阶段的**差额**识别本起源的一次阶段修正，避免把其他加成的常量误认成重复倍率。此次只读汇总并重跑现有审计，不改玩法代码。

## 逐项证据

| 场景 | 主要实机证据与复核 |
| --- | --- |
| RS-01 岗位 | [26 项来源矩阵](shishan-code-origin-resource-matrix-2026-09-29.md)在同日 I/III/V 阶段为 `26/26` 个等差；原版岗位基础 `1.98` 的工程学差额每跨 50 个百分点为 `0.99`。混合物种矿工岗位和贸易岗位另有受控对照；真实突触磨炼机的先进逻辑五档等差 `0.04502`。 |
| RS-02 非岗位 | 来源矩阵的 `14/14` 个稳定固定/轨道来源与 II 阶段基础的 `1.25/0.75/0.25` 比值吻合；[星港水培舱食物](shishan-code-origin-rs01-food-starbase-2026-09-29.md)为 `12.5/10/2.5`；[五种原版固定月产资源](shishan-code-origin-rs-remaining-fixed-resources-2026-09-29.md)各自 I/III/V 精确符合基础量；[完整戴森球](shishan-code-origin-resource-source-audit-2026-09-28.md)为 `4000→1000`；活体金属、暗物质、纳米机器、文物及结晶熵均有独立持续产出样本。 |
| RS-03 合并与排除 | 同一预算里工程学的国家基础、轨道研究站、工程师岗位 I/III/V 合计为 `18.99334/11.50334/4.01334`，每跨 50 个百分点差 `7.49=(10+3+1.98)×0.5`，三笔各只变化一次。[朝贡税、双边定额合同、月度市场单](shishan-code-origin-resource-source-audit-2026-09-28.md)在阶段切换中未被倍率放大；[非零商业协议收入](shishan-code-origin-rs03-commercial-pact-2026-09-29.md)同日 II/V 均为 `8.60265`；一次性先进逻辑和结晶熵各 `+10` 全额到账。五阶段岗位维护费独立为 `0.75/1/1.25/1.5/1.75` 倍。 |
| RS-04 其他加成 | [混合机械物种同岗位](shishan-code-origin-rs04-mixed-species-2026-09-29.md)每跨 50 个百分点矿物差 `61.6`；[原版岗位和站点增产科技](shishan-code-origin-rs04-vanilla-bonuses-2026-09-29.md)加上后差额仍为 `61.6/5/5`，与额外科技常量分开；白绮工程学研究**速度**没有重复计入研究**点数**生产。 |

2026-09-30 重跑现有只读审计：`audit_resource_source_saves.py` 为 `26/26` 等差、`14` 个稳定来源符合 II 基值；`audit_rs01_food_starbase.py`、`audit_rs02_fixed_resources.py`、`audit_rs03_commercial_pact.py`、`audit_rs04_mixed_species.py`、`audit_rs04_vanilla_bonuses.py` 均返回 `PASS`。`biomass`、`menace`、`integrity` 和 `feral_insight` 按[4.5.1 来源审计](shishan-code-origin-resource-coverage-2026-09-29.md)没有本起源机械帝国的常规持续生产适用样本；`advanced_logic` 和 `entropy_crystals` 已分别实机覆盖。

**RS-01—RS-04 按现行 Stellaris 4.5.1 与用户确认的“持续生产、每笔只覆盖一次”口径通过。** 原版未来新增生产来源、DLC 新经济类别需随游戏版本重新审计；本结论不把资源转移或一次性奖励算进生产池。
