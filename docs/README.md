# 文档知识库

## 验收语言范围

- Stellaris 实机、UI、OCR、存档重载和运行时回归只覆盖简体中文（`l_simp_chinese`）。
- 英文及其他语言只提供翻译并执行静态校验，不启动对应语言的游戏运行，不宣称其通过实机测试。
- 静态校验覆盖本地化键完整性、文件头与编码、引用一致性、原始 key 泄漏风险和简体中文占位文本。

本目录是 `xenoamess_stellaries_dev` 的文档知识库，用于沉淀 Stellaris 开发知识和本项目约定。

## 文档索引

- [迭代 1 需求文档](iteration-1-requirements.md)
- [迭代 1：当前版本实机基线与回归夹具记录](iteration-1-current-version-baseline.md)
- [迭代 1：Stellaris 实机回归方案](iteration-1-regression-plan.md)
- [迭代 1 实施记录](iteration-1-implementation.md)
- [Stellaris 验收夹具特性调研计划](stellaris-fixture-research-plan.md)
- [Stellaris 实机自动化经验](stellaris-runtime-testing.md)
- [Steam 创意工坊发布方案](steam-workshop-release-plan.md)

## 知识归档原则

- Stellaris 特有的语法、行为和实践记录在本目录。
- Paradox 脚本语言的共性基础可以参考 `D:\workspace\ck3_eternal_recurrence\docs`。
- CK3 文档属于 CK3 方言资料；应用到 Stellaris 前必须验证差异。
- 新确认的 Paradox 共性知识也应同步更新到 CK3 项目的 `docs`，并提交、推送对应仓库。

## 验收工具

- `D:\workspace\open_kaishek` 是 P 语言引擎验收工具项目。
- 任何 P 语言 mod 在验收完成前，都必须先通过该工具的检查。
- 如果检查暴露出工具缺陷或功能缺失，应先修复、完善并验证工具，再继续验收 mod。
- 工具的相关修复和功能完善必须在 `D:\workspace\open_kaishek` 仓库提交并同步推送到远端。

## 工作方式

- 本项目文档先行：功能、夹具和工具实现前，先记录目标、范围、方案与验收标准。
- 调查和实测中获得的新事实应实时回写知识库；代码与文档必须保持一致。
