# 4.5.1 特殊资源生产覆盖复核（2026-09-29）

## 范围与脚本依据

此轮检查《大厦将倾》的阶段修正是否覆盖机械起源国家可能拥有的额外**持续月度生产**。原版 `common/strategic_resources/00_strategic_resources.txt` 另外定义了 `biomass`、`menace`、`integrity`、`advanced_logic`、`feral_insight`、`entropy_crystals`。`common/pop_jobs/13_machine_age_jobs.txt` 的 `neural_chip` 岗位持续产出 `advanced_logic`；机械帝国不被 `ap_cosmogenesis` 的原版潜在条件排除。`common/static_modifiers/13_static_modifiers_nemesis.txt` 的 `relic_vacuum_flower_crisis_empire_star` 给 `country_base_entropy_crystals_produces_add=75`，是帝国固定持续月产出。引擎生成的 `logs/script_documentation/modifiers.log` 含两个 `country_*_produces_mult` 键。

因此四个有效阶段现在对这两种资源设置与其他资源相同的生产百分比，第二阶段无修正。此处的 `country_*_produces_mult` 仍是每资源**唯一一项**本起源阶段生产修正，不再叠加岗位专用修正。其余四种资源此次没有符合起源范围的持续月产出证据：`biomass` 仅对荒野帝国可见，无法与机械主体起源共存；`menace` 使用独立的无 `country` 父类经济类别；`integrity`、`feral_insight` 当前查到的是事件奖励或支出。此结论限定于原版 4.5.1 已审计来源；后来若发现新的合格来源需补测。

## 简中实机：结晶熵的固定月产出

在单 Mod、简中、离线隔离局中，给同一玩家国家施加原版 `relic_vacuum_flower_crisis_empire_star` 国家修正，确认存档中该修正唯一存在，按局势进度切换五个阶段，每次跨月后从存档 `gamestate` 的玩家 `budget.current_month.income.country_base.entropy_crystals` 读取月产出。基础值恒为 `75`，没有市场交易、附庸转移或岗位来源。结果：

| 阶段 | 目标百分比 | 实测固定月产出 | 与 75 的关系 | 证据存档 |
| --- | ---: | ---: | --- | --- |
| I | `+25%` | `93.75` | `75 × 1.25` | [stage1](../assets/shishan-code-origin/evidence/resource_crystals_stage1.03.05.sav) |
| II | `0` | `75` | `75 × 1` | [stage2](../assets/shishan-code-origin/evidence/resource_crystals_stage2.02.05.sav) |
| III | `-25%` | `56.25` | `75 × 0.75` | [stage3](../assets/shishan-code-origin/evidence/resource_crystals_stage3_valid.05.05.sav) |
| IV | `-50%` | `37.5` | `75 × 0.5` | [stage4](../assets/shishan-code-origin/evidence/resource_crystals_stage4.06.05.sav) |
| V | `-75%` | `18.75` | `75 × 0.25` | [stage5](../assets/shishan-code-origin/evidence/resource_crystals_stage5_fixture.01.05.sav) |

五份存档 SHA-256 按 I→V 顺序为 `a05ad0256d32468f04535304fc61be056da9b5ec82b78ce2a547fd8000a667e3`、`ccba52ac9092b1b63adbafb8c5099f2c54eb1cc6f500426a51bb46c65185074a`、`aad34ad08f22fba4cac9850c7adf7172af4d5bea18749e4e480d2aa38aaf28ee`、`928c6f624587f51701bc02886df0e7c8910be6e2b8dffa3d4a4153d500442c66`、`f61cccd6d607052a4d0b0160cb52b6adcac02b72514259319c38a7ca23b97370`。第三阶段的第一次自动化输入被中文输入法合并为无效命令，旧存档仍停在第一阶段，**没有计入证据**；表中 `stage3_valid` 是重新输入并在控制台回显 `500.00` 后跨月保存的有效结果。对 P 语言控制台自动化，必须复核命令回显和存档进度，不能只信任输入脚本退出码。

## 静态检查与待测

本轮 `open_kaishek` 包级检查 `PASS`：19/19 个 P 脚本、13 个 DDS、169 个本地化键，报告 `_runtime/shishan_code/accept_resource_expansion_20260929.json`。兼容特质 19 项检查通过，翻译审计的八种非中非英语言各有 0 项英文残留和 0 项非预期汉字。十种官方语言补齐两个显示键；九种外语由 MiniMax-M3 生成，候选见[翻译原始结果](../assets/shishan-code-origin/evidence/resource_expansion_minimax_2026-09-29.json)。非简中语言**静态校验通过，运行时不在范围内**。

`advanced_logic` 目前完成了来源和修正键静态核对，尚需构造有实际 `neural_chip` 岗位的宇宙创生世界并核对阶段收入；这项不能以结晶熵的帝国固定月产出测试代替。一次性奖励是否确实不被这两个新键放大也要按原验收矩阵检查。Mod 整体验收仍未通过。
