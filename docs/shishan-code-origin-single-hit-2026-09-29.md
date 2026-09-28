# SC-06 单舰逐次命中实机复测（2026-09-29）

## 目标和方法

在 Stellaris Cygnus 4.5.1 简体中文隔离用户目录中，仅启用正式「屎山代码」Mod 以及先前通过 `open_kaishek` 检查的隔离战斗夹具。玩家舰队只有一艘单门原版红色激光护卫舰，目标为无武器、装甲尚未耗尽的海盗站。从同一份 `2203.06.14` 暂停存档分支：第二阶段直接推进两日；第五阶段先用 `effect every_situation={set_situation_progress=950}` 切换局势、同日保存，然后逐日推进。用玩家舰队 `fleet_stats.combat_stats` 的 `hits`、`misses`、`damage_armor` 和 `base_damage_armor` 比较相邻存档。保留同日基线，避免将开战以来的累计伤害误认为单次命中。

## 实测

| 分支和日期 | 命中 | 未命中 | 累计实际装甲伤害 | 累计基础装甲伤害 |
| --- | ---: | ---: | ---: | ---: |
| 第二阶段 2203.06.14 | 5 | 0 | 89.265 | 59.510 |
| 第二阶段 2203.06.16 | 6 | 0 | 107.535 | 71.690 |
| 第五阶段 2203.06.14 | 5 | 0 | 89.265 | 59.510 |
| 第五阶段 2203.06.16 | 5 | 1 | 89.265 | 59.510 |
| 第五阶段 2203.06.18 | 6 | 1 | 92.0175 | 61.345 |

第二阶段相邻存档恰好多一次命中，实际装甲伤害增量为 `18.2700`，基础装甲伤害增量为 `12.1800`。第五阶段第一次射击未命中，没有伤害；再过两日恰好多一次命中，实际装甲伤害增量为 `2.7525`，基础装甲伤害增量为 `1.8350`。两次实际伤害都等于对应基础装甲伤害的 `1.5` 倍，符合红色激光对装甲倍率。第五阶段确实显著降低了一次有效命中的实际伤害。

这两次命中来自原版红色激光，单次基础伤害随机，因此 `2.7525/18.2700≈0.1507` **不能**解释为局势的精确倍率，也不能据此判定设计要求的 `0.25` 未生效。既有同日舰船面板的第二/第五阶段伤害 `8.82/2.20` 支持约四分之一的属性倍率；此轮补足了单次实际命中会降低的证据，但精确实战倍率仍需固定基础伤害的隔离夹具再次测量。战斗夹具不得并入正式 Mod。

证据存档：[第二阶段基线](../assets/shishan-code-origin/evidence/sc06_singlehit_stage2_jun14.sav)、[第二阶段命中后](../assets/shishan-code-origin/evidence/sc06_singlehit_stage2_jun16.sav)、[第五阶段基线](../assets/shishan-code-origin/evidence/sc06_singlehit_stage5_jun14.sav)、[第五阶段未命中后](../assets/shishan-code-origin/evidence/sc06_singlehit_stage5_jun16.sav)、[第五阶段命中后](../assets/shishan-code-origin/evidence/sc06_singlehit_stage5_jun18.sav)。五份 SHA-256 依次为 `6192ac1c358970ff0e291fe706a55f65931644defdd9fa43a6a1638e07e942e7`、`c6cd9d8cabe7d79ba3d12fa16a69264a61d9ad27bf95dfc4fe97157c78bb7dcc`、`0214eaaa81cf086f78a2aece6d93dc5ea0f3f90feebb1a8e2cef447fccb439e9`、`ed3c9c1bca4ad8048201153d9d8088428d503246679d8592ccb417b1f3c2fff4`、`2c83f9b5c81aa95e4448364fd31a053d04faffce43d9a1365ed2d6a5fed9b3fc`。

运行目录的存档数量达到游戏上限时，将 19 份自动存档或日期命名的旧探索存档移入仓库忽略的 `_runtime/shishan_code/save_overflow_archive`，未删除数据；腾出空间后保存成功。正式证据存档始终独立复制到 `assets/shishan-code-origin/evidence`。
