# PR-02 同一学科两个特殊项目的队列行为（2026-09-29）

## 目标与范围

验证「维护屎山」和「清理屎山」在同一国家都被点击“研究”后，游戏是否把两项同时结算，或通过社会学队列按顺序执行。此项补充[PR-02 验收方案](shishan-code-origin-acceptance-plan.md)中研究中断与重复结算风险；它不把“两个项目都显示研究中”等同于两个项目同时取得研究点。

## 方法和验收标准

从正式单 Mod、`n=2` 第一阶段的[取消后存档](../assets/shishan-code-origin/evidence/pr02-n2-cancel-post-2229.09.10.sav)继续，玩家在同一暂停日期先重新启动维护，再启动清理，并选择一个普通社会学科技。记录两项目 UI 状态、玩家原生 `society_queue` 的全部条目和项目实例状态；正常推进约一个月后再存档。合格标准：队列中每个项目键只有一份；研究点只分配给队首一个项目；未达到费用前 `n`、特质和局势不因排队而重置或发奖。若普通科技排在项目后面，应记录其排位，不将科技界面的“已选择”误作正在消耗本月研究点。

先对正式 Mod 运行 `open_kaishek`，只在简中运行时观察；非中文语言静态校验，运行时不在范围内。若原生存档证明两个项目被平行研究且会同时结算，则需回到设计和 Mod 脚本修复。

## 初始观察

`2229.09.10` 的[简中截图](../assets/shishan-code-origin/evidence/pr02-dual-projects-ui-2229.09.10.jpg)确实把维护和清理都标为“研究中”；[同日原生存档](../assets/shishan-code-origin/evidence/pr02-dual-projects-queued-2229.09.10.sav)的 `society_queue` 则顺序列出项目 ID `5`、ID `6` 和普通科技 `tech_planetary_unification`，三个条目此时均未累计进度。

## 推进后的证据和结论

正常推进 35 游戏日至 `2229.10.15`，存档仍是[同一三个队列条目](../assets/shishan-code-origin/evidence/pr02-dual-projects-after35d-2229.10.15.sav)，顺序没有变化；仅项目 `5` 的 `progress=28.33912`，项目 `6` 和普通科技都为 `0`。[维护 GUI 提示](../assets/shishan-code-origin/evidence/pr02-dual-projects-maintain-progress-2229.10.15.jpg)为 `28/4000`，[清理 GUI 提示](../assets/shishan-code-origin/evidence/pr02-dual-projects-clean-still-zero-2229.10.15.jpg)为 `0/12000`，均与原生存档一致。[严格审计](../assets/shishan-code-origin/evidence/pr02-dual-queue-audit-2026-09-29.json)为 `PASS`（7/7）：两项目实例 ID 各唯一、队列排序稳定，`n=2`、主物种特质及白绮修正均不变；局势只按一个月自然从 `7→14`。两份存档 SHA-256 分别为 `1524e9ff7cc9d8705b49f8b95882c0152ed60e63608284873f1cdae3ffc1268d` 与 `161e7610835b7782b4cd3b395add38fd3957bdcb6d33eeeb960528bf96053340`。

**结论：两项目的“研究中”是排队状态，社会学研究只投入队首；本场景没有并行结算或误发奖励。** 此观察没有让队首维护中断，因此不能把它写成“研究中断”已通过；本项仅补充同学科排队和防并行子项。正式 Mod 在本次测试前已通过 `open_kaishek`（19/19 脚本、13 DDS、172 键）；非中文语言静态校验通过，运行时不在范围内。

## 同日改选普通科技的边界探针

继续在 `2229.10.15` 的已暂停双项目队列中打开科技界面，点击社会学当前研究的“更换”，再选「统一数据标准」普通科技。科技面板随即仍显示正在研究「维护屎山」（[简中截图](../assets/shishan-code-origin/evidence/pr02-n2-research-switch-ui-2229.10.15.jpg)）；[同日原生存档](../assets/shishan-code-origin/evidence/pr02-n2-research-switch-2229.10.15.sav) SHA-256 为 `799648f01ec2b1515a36e9a0b86bdb560c9ed521601a3dc0a241a6b8d34a6d2b`。对比改选前存档，社会学队列仍为维护项目 ID `5`（进度 `28.33912`）、清理 ID `6`（`0`）、普通科技 `tech_planetary_unification`（`0`）；日期、`n=2`、主物种特质、两个项目状态、局势进度 `14` 与白绮阶梯修正也逐项一致。截图 SHA-256 为 `93ff03801edb2fcebed2260651dcc0a0d32ca1cb9bafa79617d254f4a508f8f0`。

**此操作没有中断队首项目。** 科技更换只影响普通科技候选，不能充当“研究中断”通过证据；PR-02 的该边界仍需另找真实停止获取研究点的原版路径。
