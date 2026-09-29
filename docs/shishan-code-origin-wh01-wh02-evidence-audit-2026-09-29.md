# 白绮取得、科研修正与极值证据复核（2026-09-29）

## 范围与判据

按[验收方案](shishan-code-origin-acceptance-plan.md)复核 WH-01、WH-02 的既有简体中文单 Mod 实机证据；本次仅审计已归档画面、原生存档和正式脚本，不把脚本公式单独当作实机结论。WH-03 的付费复活另由[零经验记录](shishan-code-origin-vivhite-zero-xp-2026-09-28.md)、[正式非零经验记录](shishan-code-origin-vivhite-revival-probe-2026-09-28.md)及总报告验收。

WH-01 通过条件：正常开局事件链只取得一名白绮，身份、名字、肖像和不朽特质正确；受雇但空闲时全国修正仍在，`n=0/1` 分别为工程速度 `+10/+15%`、社会速度 `−5/−7.5%`。WH-02 通过条件：`n=28/29` 工程速度 `+150/+155%`、社会速度均封顶 `−75%`；高龄跨月不自然老死；主动解雇按钮禁用；真实死亡后全国修正消失并在复活后按原 `n` 恢复。研究**速度**与研究**点数生产**必须分开。

## 复核结果

| 条件 | 证据与观察 |
| --- | --- |
| 正常取得、身份和肖像 | [开局实机记录](shishan-code-origin-runtime-findings-2026-09-27.md)的三段事件链于开局 1 月 4—8 日完成，白绮加入；[正式领袖画面](../assets/shishan-code-origin/evidence/vivhite-leader-v2-stellaris-4.5.1.png)显示唯一「负疚者·白绮」、传奇行政官、完整肖像和灰色解雇按钮。正式脚本仅在事件链结尾登记白绮身份并同步全国修正。 |
| 空闲仍生效 | [空闲领袖画面](../assets/shishan-code-origin/evidence/vivhite-idle-national-bonus-2208.10.05.jpg)显示白绮未获岗位仍在受雇名单；同日[存档](../assets/shishan-code-origin/evidence/resource_advanced_logic_clean_stage5.10.05.sav)的玩家维护次数为 `0`，全国 `shishan_code_vivhite_base` 恰有一份，两种阶梯修正倍率均为 `0`。正式静态修正定义给出工程速度 `+10%`、社会速度 `−5%`。 |
| 维护一次 | 自然完成一次「持续优化」后的[存档](../assets/shishan-code-origin/evidence/pr04_optimize_natural_no_relapse_post_22290727.sav)中 `n=1`、基础修正与两种阶梯修正各一份，阶梯没有单独 `multiplier` 字段，按默认一层计；对应全国工程 `+10+5=+15%`、社会 `−5−2.5=−7.5%`。另一个自然完成两次维护的存档在[实机记录](shishan-code-origin-runtime-findings-2026-09-27.md)中记录 `n=2`、两种阶梯倍率 `2`。 |
| 高次数封顶 | [n=28 回显](../assets/shishan-code-origin/evidence/vivhite-n28-cap.jpg)为基础工程 `+10%`、工程阶梯 `+140%`、基础社会 `−5%`、社会阶梯 `−70%`；[n=29 回显](../assets/shishan-code-origin/evidence/vivhite-n29-cap.jpg)工程阶梯变 `+145%`、社会阶梯保持 `−70%`。[正式复活存档](../assets/shishan-code-origin/evidence/vivhite-formal-xp-restore-2227.03.09.sav)同时证明 `n=29`、工程倍率 `29`、社会倍率 `28`。这些高次数是调用正式刷新效果的边界夹具，不声称自然完成了 29 次项目。 |
| 不朽及不可解雇 | [500 岁跨月截图和存档](shishan-code-origin-acceptance-report-2026-09-27.md)记录同一领袖设龄后经过 `35` 游戏日仍受雇，未出现重启入口；正式领袖特质有 `immortal_leaders=yes`。领袖详情卡的「解雇领袖」按钮呈灰色；正式 `can_dismiss_leader` 游戏规则在原版规则末尾增设白绮身份的失败条件。 |
| 死亡与重新受雇 | 真实 `kill_leader` 后的[待复活存档](../assets/shishan-code-origin/evidence/vivhite-zero-xp-pending.sav)中白绮不在 `owned_leaders`、全国基础与阶梯修正均无；付费后[复活存档](../assets/shishan-code-origin/evidence/vivhite-zero-xp-revived.sav)中仅一名新白绮，基础一份、工程和社会阶梯各一份且倍率为 `0`。`n=29` 的死亡及复活分支在[实机记录](shishan-code-origin-runtime-findings-2026-09-27.md)中另证重新得到工程倍率 `29`、社会倍率 `28`。 |
| 研究点数隔离 | [RS-04 原版科技组合验收](shishan-code-origin-rs04-vanilla-bonuses-2026-09-29.md)在白绮 `n=0` 且基础速度修正存在时，三阶段国家基础、站点、岗位的工程学研究点数各只接受一次局势阶段变化；白绮修正未混入生产。 |

结论：**WH-01、WH-02 按本方案通过**。正式 Mod 的高龄、禁用解雇、空闲持续、`n=0/1/28/29` 和真实死亡恢复均有实机或原生存档证据；`n=28/29` 属受控边界夹具。其余功能场景及整体验收仍见总报告。
