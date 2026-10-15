# 个体机械种子的最短正常维护与月速复核路线

## 目标、范围与依据

本轮只读准备由主任务执行的简体中文 UI 路线：在同一 n=0 存档中依次验证 J=0 的月速 1、J=100 的月速 0.75，再通过普通社会学研究完成维护。不给生产包增加夹具，不操作游戏、不改主实机记录。

种子为 `assets/shishan-code-origin/evidence/individual-machine-2203.05.22.sav`，SHA-256 `3bff62df806073a10e53364cd0150dee8f9af61815675050e34038ffd4ba88e8`。已有[独立种子审查](feedback-redesign-individual-seed-audit-2026-10-15.md)及其 JSON 已证明 country=0、n=0、一座研究所、维护员实际 workforce=100；bonus_workforce=10 是另外字段，不并入 J。源档局势进度为 199、历史月速为旧版 4.9，维护项目 ID=1 可用且未研究；社会学库存 657.98021，三个科研队列均为空。首都维护员所在 colony=0，岗位对象 ID=16777323 仅为此源档锚点，重分配后不要求对象 ID 固定。

当前 4.5.2 原版 `interface/planet_view.gui:3694` 的建筑详情有 `enable_disable_building` 按钮；`localisation/simp_chinese/main_2_l_simp_chinese.yml:1460`、`:1461` 对应中文「禁用」「启用」。同文件 `:2148` 对应「研究项目」。本 Mod 维护项目 `location=no`、研究部门为 society_technology、n=0 成本为 2000，因此无舰船、科学船或定位调查步骤。[历史个体机械记录](../../docs/shishan-code-origin-individual-machine-2026-09-28.md)已经用该种子通过普通项目 UI 启动、跨月、取消维护，本轮需继续到正常科研完工。

## 操作与每阶段验收

先加载种子并保持暂停，检查当前科研/建造加速未开启。跨一个完整月更新旧缓存后另存基线，确认 n 仍为 0、没有待领项目。下列进度增量必须采用实际 J 已稳定后的相邻两个完整月初存档，避免把就业重排中的半月算作样本。

| 顺序 | 最少 UI 操作 | 独立存档与 UI 预期 |
| --- | --- | --- |
| 1：停工 | 首都→建筑页→点击「屎山维护研究所」→建筑详情「禁用」。正常推进几天，让引擎重分配就业，再在岗位页确认维护员实际已分配为 0。 | 两类维护员全国实际 workforce 合计 J=0，n=0；局势显示 +1/月。保存稳定月初 A，再正常跨一个月保存 B；`situation_shishan_code.progress(B)-progress(A)=1`、`last_month_progress=1`。建筑仍在，不能用拆除代替停工。 |
| 2：复工 | 点击同一建筑→「启用」；正常推进至维护员实际已分配恢复 100，再取稳定月初 C 与下个月初 D。 | 全国 J=100，n=0；月速 +0.75，`progress(D)-progress(C)=0.75`、`last_month_progress=0.75`。建筑容量 100 与 bonus_workforce=10 都不能代替真实 J。 |
| 3：启动科研 | 暂停时打开「科技」，在社会学空槽选择一项正常可选科技；同一暂停日打开「情报日志」→「维护屎山」→「研究项目」。 | 普通科技选择被保留；维护状态变「研究中」，成本 2000；新 `country[0].tech_status.society_queue` 能定位到维护项目 ID 1，项目不再只是未启动条目。此时 n=0，不能因为启动而归零或获得奖励。保存 E。 |
| 4：正常推进 | 只让游戏正常走时，保留研究所运行；不加科研资源/倍率、不使用 `complete_special_project`、直接回调事件或测试凭证。至少跨一个月保存 F，然后等待真正完成。 | 与 E 比较，社会学项目真实累计 progress 增加，预算与库存变化可解释；界面给出实时预计耗时。源档库存约 658、历史收入约 18.3/月只是起点，不能按旧预算写死完工日期。 |
| 5：成功 | 等待项目自然研究完毕，正常查看奖励界面，暂停后保存 G；再走一天核对后续项目状态。 | 原生 `last_completed_special_project=SHISHAN_CODE_MAINTAIN`，旧项目结束、n 只从 0 变为 1、局势归零后才继续走时、出现真实三选一待领状态；社会学普通科技恢复研究。若 J 仍为 100，维护后公式月速为 1；领取奖励前后分别留存，不将维护成功与选择结果合为一次取证。 |

若复工后实际 J 尚未恢复 100，应继续正常等待或由正常岗位界面调配，先确认真实就业再采样；不按建筑图标或容量直接宣布速度通过。自然研究期间出现经济缺口、事件、阶段变化或未完工，需要保留现场并报告实际进度，不以控制台加速补成「自然完成」。

## 原生字段与结果边界

每份存档只读检查：`country[0].variables.shishan_code_maintenance_count`；`situations.situations[*]` 中该国 `type=situation_shishan_code` 的 `progress/last_month_progress`；全国该国星球两类维护员 `pop_jobs[*].workforce` 及对应人口组分配量；`country[0].tech_status.society_queue`、`events.special_project` 的实际 ID/状态、`tech_status.stored_techpoints` 的社会学项和所选科技记录；成功后的 `last_completed_special_project` 与奖励标记。星球归属使用 colony 与 carrier 链解析，不把 colony=0 当作恒星 planet=0。队列精确层级额外用已归档的 `pr02-dual-projects-queued-2229.09.10.sav` 原生嵌套结构复核，确认队列属于 `tech_status`，并非国家直接子字段。

启动和跨月研究这条路线使用真实项目状态与正常 UI，能验证普通科研占用和成功回调；它仍属于已有旧档的续玩验收，不是从 2200 起步的长期自然平衡结论。本文为只读资料与操作准备，尚未执行本轮 UI 或原生验收。主任务继续负责 G1、游戏交互、截图、存档及证据归档。

## 最后数值边界的只读资料补充

主任务已另行在主实机计划记录：从 rc6 `fb456_natural_claim` 的 n=1/J=100 分支受控增加四所研究所，再由引擎自然分配维护员到 J=500。此时独立预期 `max(1+0.25-0.25*floor(500/100),0.2)=0.2`，必须取实际 workforce 合计、稳定后相邻月初进度差，不按新建筑数量或 bonus_workforce 推断。该分支是受控岗位容量边界，不能替代正常建设平衡样本。

当前 4.5.2 本次原生生成的 `effects.log:2468`、`:2472` 分别给出 `add_situation_progress=5.5` 和 `set_situation_progress=5.5`，两者均只用于 situation 作用域。原版 `events/infernals_crisis_events.txt:600` 使用绝对 set，`common/scripted_effects/02_machine_age_effects.txt:3776` 等使用 add。为避免累计误差，阶段检查使用国家控制台 `effect every_situation = { limit = { is_situation_type = situation_shishan_code } set_situation_progress = 500 }`，随后分别改为 750、950；属于受控切换，不写作自然发展到阶段。

生产 `common/situations/shishan_code_situation.txt` 的边界是 III `[500,750)`、IV `[750,950)`、V `[950,1000]`。`common/static_modifiers/shishan_code_stages.txt` 明确三阶段的 22 项资源产出、武器伤害、亚光速分别为 -12.5%/-25%/-37.5%，岗位维护分别 +12.5%/+25%/+37.5%。最短 UI 入口为「情报日志→大厦将倾→当前阶段图标/罗马数字悬停」，直接读阶段 tooltip 中的修正；需要最终产出时要额外跨月刷新预算，不能把架构加算混合后的总产出比率当作阶段系数。

本补充仅核实语法、原版实例及预期，不操作游戏、不改变冻结生产；floor 与阶段 UI 实测由主任务继续执行。
