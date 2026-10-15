# 「屎山代码」Mod 文档入口

本目录存放本 Mod 的改版测试方案和后续执行记录；既有需求、设计和历史证据仍保留在仓库根 `docs` 中，通过下列链接引用。

## 当前改版

- [0.2.1发布与修订范围的继续验收](release-0.2.1-and-remaining-acceptance-2026-10-15.md)
- [用户反馈与改版设计稿（2026-10-04）](../../docs/shishan-code-origin-feedback-redesign-2026-10-04.md)
- [基于低内聚高耦合的旧时代集成服务架构：全特质 5% 与独立乘算设计](../../docs/shishan-code-origin-trait-synergy-design-2026-10-04.md)
- [改版测试方案：环境、闸门、方法与通过条件](feedback-redesign-test-plan-2026-10-04.md)
- [改版测试用例：操作、预期与证据](feedback-redesign-test-cases-2026-10-04.md)
- [开发候选实施与程序验证记录](feedback-redesign-implementation-2026-10-04.md)
- [基础数值、领袖与翻译实施](feedback-redesign-balance-implementation-2026-10-04.md)
- [全特质计数、迁移与国内模板克隆](feedback-redesign-architecture-implementation-2026-10-04.md)
- [离线脚本合同检查器与负例](feedback-redesign-programmatic-2026-10-04.md)
- [交给另一台机器验收的困难与准备（2026-10-06）](acceptance-machine-handoff-assessment-2026-10-06.md)
- [2026-10-15：更新本机、离线实机回归与发现的修复](runtime-feedback-validation-2026-10-15.md)
- [原生存档只读审计：字段、独立预期与覆盖边界](runtime-save-audit-2026-10-15.md)
- [长名称正文全文修复](feedback-redesign-full-name-ui-fix-2026-10-15.md)
- [奖励选项提示隐藏内部执行细节](feedback-redesign-reward-tooltip-2026-10-15.md)
- [实机NOT真值表与随机权重修复](feedback-redesign-reward-negation-fix-2026-10-15.md)
- [按原版审计机械候选资格](feedback-redesign-robotic-eligibility-fix-2026-10-15.md)
- [白绮维护费显示键](leader-upkeep-localisation-fix-2026-10-15.md)
- [白绮原生个人免维护修复](feedback-redesign-vivhite-free-upkeep-fix-2026-10-15.md)
- [模板权利、特使和白绮头像修复](feedback-redesign-template-state-fix-2026-10-15.md)
- [同日物种缓存交叉修复](feedback-redesign-owned-species-cache-fix-2026-10-15.md)
- [个体机械种子与普通科研路线](feedback-redesign-natural-maintenance-route-2026-10-15.md)

2026-10-15更新：当前候选为`0.2.0-rc.6`。本轮实机发现并修复引擎加载、奖励取反、原版互斥资格、模板权利/特使/头像、同日物种缓存及长名称全文等问题。工具检查、程序回归、原生存档和简中截图的实际结果与未覆盖项以[本轮验证记录](runtime-feedback-validation-2026-10-15.md)为准。

2026-10-04的rc.1仅做程序验证，作为历史保留。当前局势初始月速为1；每特质5%采用原生岗位产出加算，独立乘算未实现。白绮本人免费改用原生维护豁免，避开经济倍率下限；其它领袖正常付费，实机结果见本轮记录。九种非中文翻译仅静态校验，运行时不在范围内。

机制全名为「基于低内聚高耦合的旧时代集成服务架构」。1600×900、请求缩放0.75的简中实机确认正文可读全文，原生标题栏仍省略；其它显示矩阵未执行。

## 历史合同与证据

- [原需求](../../docs/shishan-code-origin-requirements.md)
- [原详细设计](../../docs/shishan-code-origin-design.md)
- [旧版总验收方案](../../docs/shishan-code-origin-acceptance-plan.md)
- [历史验收记录](../../docs/shishan-code-origin-acceptance-report-2026-09-27.md)
- [奖励池耗尽与迭代证据](../../docs/shishan-code-origin-pr05-reward-closure-2026-09-30.md)
- [简体中文实机与存档自动化经验](../../docs/stellaris-runtime-testing.md)

旧方案中基础月速 5、旧负面社会学、旧四类随机迭代和旧阶段惩罚等预期仅适用于历史版本。本轮改版使用当前设计与上述新测试方案，不能把历史通过结果直接记入新版本。
