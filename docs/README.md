# 文档知识库

本目录是 `xenoamess_stellaries_dev` 的文档知识库，用于沉淀 Stellaris 开发知识和本项目约定。

## 文档索引

- [迭代 1 需求文档](iteration-1-requirements.md)
- [迭代 1：当前版本实机基线与回归夹具记录](iteration-1-current-version-baseline.md)
- [迭代 1：Stellaris 实机回归方案](iteration-1-regression-plan.md)

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
