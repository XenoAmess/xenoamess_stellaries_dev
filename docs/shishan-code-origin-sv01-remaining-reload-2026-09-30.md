# SV-01 其余状态重载验收（2026-09-30）

## 目标与范围

补齐验收矩阵 SV-01 尚未闭环的已重构、持续优化复发、白绮待复活与复活后、奖励进入「优化迭代」后的存档重载。此前第一、第五阶段及维护次数非零的重载证据另见对应专项记录。本轮只使用正式发布的 `0.1.0` 单 Mod、简体中文和原生游戏存档；Steam 保持离线。

## 方法与验收标准

选取仓库已归档且能由正式 Mod 载入的各状态原生存档。在游戏内从另一状态载入，暂停同日另存，并保存必要的 Steam F12 界面截图。只读比对载入前后：游戏日期、局势数量和进度、维护计数、项目实例与费用、主体物种完整特质、优化迭代层数、白绮存活/待复活入口及其等级、经验、特质、全国修正的层数和唯一性。待复活状态还要检查复活备份引用；已复活状态检查其清理。与 Mod 状态无关的原版预算刷新单独记录。不同日期的存档不能直接作为严格持久化对照。

测试夹具仅可把已有证据存档复制进隔离用户目录供游戏 UI 读取，不修改原生存档内容、正式 Mod 或 Workshop 条目。每项都留存原生前后存档的 SHA-256、字段审计和界面证据。先用 `open_kaishek` 检查正式 Mod 包，通过后才标记子项通过；其他九种官方语言只做静态校验，运行时不在范围内。

## 执行记录

在 Cygnus 4.5.1、正式单 Mod 校验和 `fe44` 的简体中文局中，从其他状态经游戏内载入以下五份仓库原生存档，并在暂停的同一日期另存。所有载入后截图、存档与[17/17 字段审计](../assets/shishan-code-origin/evidence/sv01-remaining-reload-audit-2026-09-30.json)均已归档：

| 状态 | 原生锚点 → 游戏内重载后存档 | 日期与关键结果 |
| --- | --- | --- |
| 已重构 | [锚点](../assets/shishan-code-origin/evidence/pr04_optimize_natural_no_relapse_post_22290727.sav) → [重载](../assets/shishan-code-origin/evidence/sv01-refactored-reloaded-2229.07.27.sav) | `2229.07.27`，`n=1`，无局势，全国重构岗位修正一层，持续优化项目可用；[画面](../assets/shishan-code-origin/evidence/sv01-refactored-reloaded-2229.07.27.jpg)。 |
| 优化复发 | [锚点](../assets/shishan-code-origin/evidence/pr04-relapse-natural-post-2229.08.05.sav) → [重载](../assets/shishan-code-origin/evidence/sv01-relapse-reloaded-2229.08.05.sav) | `2229.08.05`，`n=2`，一条进度为 `0` 的局势，全国重构修正已撤，维护和清理项目各一；[画面](../assets/shishan-code-origin/evidence/sv01-relapse-reloaded-2229.08.05.jpg)。 |
| 优化迭代 | [锚点](../assets/shishan-code-origin/evidence/iteration-output2-2207.12.05.sav) → [重载](../assets/shishan-code-origin/evidence/sv01-iteration-reloaded-2207.12.05.sav) | `2207.12.05`，岗位产出迭代计数仍为 `2`，一条局势进度 `309.8`；[画面](../assets/shishan-code-origin/evidence/sv01-iteration-reloaded-2207.12.05.jpg)。 |
| 白绮待复活 | [锚点](../assets/shishan-code-origin/evidence/vivhite-zero-xp-pending.sav) → [重载](../assets/shishan-code-origin/evidence/sv01-vivhite-pending-reloaded-2203.06.03.sav) | `2203.06.03`，待复活旗标与经验备份 `0` 保留，受雇白绮 `0`，全国白绮基础效果 `0`；[画面](../assets/shishan-code-origin/evidence/sv01-vivhite-pending-reloaded-2203.06.03.jpg)。 |
| 白绮复活后 | [锚点](../assets/shishan-code-origin/evidence/vivhite-zero-xp-revived.sav) → [重载](../assets/shishan-code-origin/evidence/sv01-vivhite-revived-reloaded-2203.06.03.sav) | 同为 `2203.06.03`，待复活旗标及备份变量已清除，受雇白绮恰一人，全国基础效果恰一层；[画面](../assets/shishan-code-origin/evidence/sv01-vivhite-revived-reloaded-2203.06.03.jpg)。 |

五组前后日期、维护次数、项目 ID/状态、局势进度、全部物种数据库、全部领袖数据库、玩家 `owned_leaders`、白绮归属、迭代计数和玩家所有 `shishan_code` 字段均一致。物种和领袖数据库的原生文本 SHA-256 在每组前后完全相同，因此主体特质、白绮等级、经验和已获特质未漂移。所有重载存档均无测试科研加速引用，也没有重复局势或受雇白绮。各原生存档文件 SHA-256 见审计 JSON；不同文件整体哈希本就不要求相同。

**日志例外**：已重构锚点在载入前含一条 `modifier=""` 空的限时修正，载入时原版写出一次 `Invalid timed modifier`，并在重载后存档中丢弃此条；另外四份锚点和五份重载结果均无空修正。正式 Mod 脚本没有添加空修正的调用，真实的全国重构与白绮修正前后均保持一致。审计显式记录并检查了这一差别，不能把该条旧存档脏数据写成 Mod 功能错误，也不能称游戏日志完全干净。

本轮正式 `open_kaishek` 包级验收再次 **PASS**：19/19 P 脚本、13 DDS、172 本地化键，报告 `_runtime/shishan_code/accept_sv01_remaining_20260930.json`。其余九种官方语言的键、编码和引用由包级检查覆盖；八种非中文、非英文翻译的英文原文和汉字占位均为零。结论为**静态校验通过，运行时不在范围内**。连同此前第一、第五阶段和维护后 `n>0` 的同日重载，**SV-01 指定状态全部通过**。
