# RS-04 原版科技增产组合实机验收（2026-09-29）

## 目标与范围

补足验收计划 RS-04 中的原版岗位增产、采集站增产组合。继续使用已通过 `open_kaishek` 的独立简中 RS-04 夹具，不改正式 Mod 和现有测试夹具脚本。从[混合物种共同基线](../assets/shishan-code-origin/evidence/rs04-variant-anchor-2203.09.24.sav)重载，在玩家国家作用域一次性授予原版 `tech_synthetic_thought_patterns`（`planet_jobs_produces_mult=0.025`）和 `tech_space_mining_1`（`station_gatherers_produces_mult=0.10`）。两者分别来自 Stellaris 4.5.1 的 `common/technology/00_soc_tech.txt`、`00_eng_tech.txt`，原版事件脚本已有国家作用域 `give_technology={tech=...}` 实例。

## 设计与验收标准

授予科技后保存新的暂停基线，从同一个基线独立设置「大厦将倾」进度为 `0/500/950`，每支正常推进过同一月结算并停在同一天。三份原生 ZIP 存档须证明国家已持有两项科技、两种机械模板都在同一矿工岗位且劳动力不变、原版采集站来源不变、局势阶段正确。逐项提取玩家月预算的 `planet_miners.minerals` 和 `orbital_mining_deposits.minerals`，对比 I−III 与 III−V 差值；两段差须相等，且不能出现本起源同一来源修正两次。科技增益的绝对数值须与无科技分支对照，并区分原版不同修正类别本身可能发生的加法或乘法组合。

游戏日志须无新的 Mod/夹具脚本错误。归档共同基线、三份存档、对应 Steam F12 截图及 SHA-256；复核正式 Mod `open_kaishek`，在总报告中记录可证明的范围。若科技效果未生效、人口岗位或站点来源变化，标记样本无效并重做，不以放宽误差代替受控对照。

新增只读审计脚本 `tools/shishan_code/audit_rs04_vanilla_bonuses.py`：复用混合物种审计的岗位/物种权利断言，额外核对玩家科技、三阶段同日、两种来源的精确阶段差，以及与无科技同阶段存档的增量。技术取得前后的控制基线日期不同，跨基线比较仅在岗位劳动力和来源容量不变时作为加成量佐证；同日三阶段差值才是是否重复作用的主判据。脚本以非零状态码拒绝任何不符，输出带输入 SHA-256 的 JSON。

同三份科技分支存档还用于白绮研究速度与研究点产出的口径隔离。审计确认白绮基础全国研究速度修正在三个玩家国家块中均只存在一次、`n=0`，同时分别提取国家基础、轨道研究站和工程师岗位的工程学**研究点产出**；这三类产出应按局势阶段呈相等差额，而不能把白绮的 `+10%` 工程学**研究速度**再乘到产出上。科技分支的白绮修正不作设置变更。

## 实机结果

从 `2203.09.24` 科技共同基线独立推进的三支均停在 `2203.10.08`；玩家已持有两项原版科技，主体/子模板矿工分配仍为 `2300/500` 劳动力，额外劳动力 `280`。只读审计返回 `PASS`，三阶段分别为：

| 玩家月预算来源 | I | III | V | 每跨两阶段差 |
| --- | ---: | ---: | ---: | ---: |
| 矿工岗位矿物 | 166.08592 | 104.48592 | 42.88592 | 61.6 |
| 轨道采集站矿物 | 13.5 | 8.5 | 3.5 | 5.0 |
| 轨道采集站能量 | 13.5 | 8.5 | 3.5 | 5.0 |
| 国家基础工程学研究点 | 12.5 | 7.5 | 2.5 | 5.0 |
| 轨道研究站工程学研究点 | 3.75 | 2.25 | 0.75 | 1.5 |
| 工程师岗位工程学研究点 | 5.18007 | 3.20007 | 1.22007 | 1.98 |

与无科技、相同阶段且岗位分配相同的分支相比，岗位矿物在三阶段各增 `3.08=123.2×2.5%`，站点矿物和能量各增 `1.0=10×10%`。这些是原版科技自身的增量；起源阶段自身每次仅改变固定基础来源的 `50%`，无第二次作用。三个国家块均有一份白绮基础修正、`n=0`；正式静态修正为工程学**研究速度** `+10%`、社会学**研究速度** `-5%`。工程学研究点三来源仍线性变化，上表没有将速度误算成研究点生产。隔离 `error.log` 中无新的脚本/夹具错误。正式 Mod 的 `open_kaishek` 为 `PASS`（19/19 脚本、13 DDS、172 键），`audit_translations.py` 的八种非中非英语言为 0 英语原文残留、0 汉字占位，`audit_compat_traits.py` 的 19 项映射通过；非中文语言**静态校验通过，运行时不在范围内**。

归档：[审计 JSON](../assets/shishan-code-origin/evidence/rs04-vanilla-bonuses-audit-2026-09-29.json)、[科技共同基线](../assets/shishan-code-origin/evidence/rs04-tech-anchor-2203.09.24.sav)、I 阶段[存档](../assets/shishan-code-origin/evidence/rs04-tech-stage1-2203.10.08.sav)/[截图](../assets/shishan-code-origin/evidence/rs04-tech-stage1-2203.10.08.jpg)、III 阶段[存档](../assets/shishan-code-origin/evidence/rs04-tech-stage3-2203.10.08.sav)/[截图](../assets/shishan-code-origin/evidence/rs04-tech-stage3-2203.10.08.jpg)、V 阶段[存档](../assets/shishan-code-origin/evidence/rs04-tech-stage5-2203.10.08.sav)/[截图](../assets/shishan-code-origin/evidence/rs04-tech-stage5-2203.10.08.jpg)。审计 JSON SHA-256 为 `dc64b1ddfa7726739c1ae3a362ea1fd63471606f2b03ad1709951cf439abfe27`；共同基线 SHA-256 为 `36bfbace86ee4bf8b76786886b3c45ea816fad378a820b2b8fb4d874adf78530`。三阶段存档 SHA-256 依次为 `86d22d9355da962e61244bdb1f8f18a3a72b79ab947bfd4be568bf3cca6c63e2`、`9cc8401a5bbe88ad5dd69cfa740e0629c71c69e6b4bc56edcffa6c3ee8df01dc`、`f7ebaccc8809bdab0b04bfc9339ec9997e2bda77300b6094823af970b4f4335f`；截图 SHA-256 依次为 `a85b9c1f871711715f2a4787c0d6f4333ba9a12ce52d320d3ebcd537e0b64a39`、`db9ba5957c5a79a59604f6e5e14281f8c2c3f40133639e6afea3cb9430c49346`、`8cb07ed7ae04f7e7c06df242d47e9d40b7e5badf53c1b2ce783733543f2d722b`。
