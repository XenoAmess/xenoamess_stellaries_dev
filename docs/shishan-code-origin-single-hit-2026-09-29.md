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

## 固定伤害复测方案

为核对精确的阶段倍率，下一轮只在隔离测试 Mod 副本中启用 `SHISHAN_SC06_FIXED_LASER`：从 4.5.1 原版 `SMALL_RED_LASER` 复制 CSV 行，仅把最小/最大基础伤害都设为 `10`，命中率与追踪率均设为 `1`，保留装甲倍率 `1.5`；脚本模板使用同版原版红色激光的合法组件字段。隔离事件创建一艘只装此武器的玩家护卫舰及一座无武器海盗站。先用 `open_kaishek` 检查隔离副本，再重启游戏并检查 `error.log` 没有组件模板或 CSV 解析错误。从相同接敌前存档分出第二和第五阶段，每支分支分别取得恰好一次命中的前后存档，且目标装甲不耗尽、没有资源短缺，期望实际装甲伤害分别等于 `10×1.5×对应国家武器伤害倍率`。若夹具未在游戏中装上固定武器，或两个分支的其他国家修正不同，不得据此宣告精确倍率通过。

首次执行结果：隔离副本通过 `open_kaishek`（22/22 脚本）；重启后游戏存档证实单舰单站和 `SHISHAN_SC06_FIXED_LASER` 组件确实存在，`error.log` 未报告组件或 CSV 解析错误。然而从 `2203.06.03` 推进到 `2203.06.22`，攻击舰的 `fleet_stats.combat_stats` 仍无命中或未命中，目标未受损，故这个自定义组件夹具没有产生可用战斗。不能把“已装配”误当作“已射击”。

修订方案：隔离副本的 `weapon_components.csv` 完整保留当版原版表，仅将 **原版 `SMALL_RED_LASER` 行**的 `min_damage` 和 `max_damage` 都设为 `10`，其余列包括命中率、追踪率和装甲倍率一律保留原版。原版组件模板和已验证能正常射击的单舰战斗夹具不变。Stellaris 4.5.1 表头注释明确称 CSV 可由控制台 `reload stats` 重载；先在隔离游戏执行该命令并通过舰船面板/实际命中验证已生效，若热重载无效再重启。`open_kaishek` 对每次改动后的隔离副本仍须通过。所有固定伤害改动只在被忽略的隔离目录，测完恢复原版行；正式 Mod 不覆盖武器数值表。

第一次修改 CSV 时，编辑器意外写入 UTF-8 BOM；游戏 `reload stats` 后的 `error.log` 报 `Could not find header key`、`Could not find header power` 和 `Failed to parse ... weapon_components.csv`。`open_kaishek` 的包级 `PASS` 不覆盖这个游戏专有 CSV 解析语义。现已改为直接读取原版 CSV **字节**，只替换 `SMALL_RED_LASER` 行中的 `6.00;16.00` 为 `10.00;10.00`，保持原版无 BOM、字段数和其他所有字节；工具再次 `PASS`（22/22）。修正后的热重载没有追加新的解析错误，但先前失败过的同一游戏会话随后在尝试保存时退出，不能从这份会话采集有效战斗结果。下一轮从修正后的隔离 CSV 直接启动全新游戏进程，载入旧的原版红色激光接敌前存档，不再依赖可能被先前解析失败污染的热重载状态。正式 Mod 不包含此 CSV。

## 固定伤害实机结果

2026-09-29 从修正后的隔离 CSV 全新启动游戏，加载同一 `2203.06.03` 接敌前存档。该武器表相对 4.5.1 原版仅改变红色小型激光的最小和最大伤害为 `10`，没有 BOM；隔离副本的 `open_kaishek` 为 `PASS`（22/22），报告 `_runtime/shishan_code/accept_sc06_vanilla_fixed_nobom_20260929.json`。无新的 CSV 表头解析错误。第二阶段直接推进 10 日；第五阶段从相同接敌前存档执行 `effect every_situation={set_situation_progress=950}`，再推进相同的 10 日。游戏内第五阶段局势与舰队战力变化已由控制台和截图确认。

| 分支 | 日期 | 命中 | 累计基础装甲伤害 | 累计实际装甲伤害 | 每次实际命中 |
| --- | --- | ---: | ---: | ---: | ---: |
| 同一接敌前基线 | 2203.06.03 | 0 | 0 | 0 | — |
| 第二阶段 | 2203.06.13 | 5 | 50 | 75 | 15 |
| 第五阶段 | 2203.06.13 | 5 | 12.5 | 18.75 | 3.75 |

两条分支使用同一艘船、同一门武器、同一目标、同一日期和相同命中数。目标装甲从 `2735` 分别降至 `2660` 与 `2716.25`，均未耗尽。单次实际命中 `15` 与 `3.75` 的比值恰为 `4:1`；由于红色激光对装甲的原版倍率为 `1.5`，分别对应武器基础伤害 `10` 与国家阶段伤害倍率 `1.0/0.25`。这证明 SC-06 的第二/第五阶段实战武器伤害倍率精确生效，并补齐先前随机伤害比较不能说明的部分；其余阶段的实战单次命中不由这两份存档证明。

可重载证据：[同一基线](../assets/shishan-code-origin/evidence/sc06_red_fixed_clean_pre.sav)、[第二阶段结果](../assets/shishan-code-origin/evidence/sc06_red_fixed_clean_stage2_jun13.sav)、[第五阶段结果](../assets/shishan-code-origin/evidence/sc06_red_fixed_clean_stage5_jun13.sav)。SHA-256 依次为 `55cbb459c704f99f776f6ebc9e3e13a475a1cbae1fe1e443eaf82194262c6bb0`、`9ff4dff7e0fb694e499930ed3717c9a5194485e9baff359efaac9fbbd2163636`、`53ee50f4794d98c9f3c73150e765e1eb06522bb5e7843afd8bb796812f3dd5e9`。隔离武器表的 SHA-256 为 `a39a34e823fee085dcb53e7f7c91e86fd2220a6a022a9b7d68170568e3aedd16`。此表和自定义战斗事件均未加入正式 Mod。
