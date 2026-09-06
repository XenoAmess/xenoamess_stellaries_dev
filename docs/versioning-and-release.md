# Mod 版本与发布规范

## 版本模型

本 Mod 采用语义化版本 `MAJOR.MINOR.PATCH`，版本号独立于 Stellaris 游戏版本：

- `MAJOR`：不兼容既有存档、配置或核心玩法合同的变更。
- `MINOR`：向后兼容的新功能、新决议、新内容或显著能力扩展。
- `PATCH`：向后兼容的缺陷修复、兼容修正和本地化修正。
- `-rc.N`：正式发布候选；默认不上传到公开创意工坊。

Stellaris 兼容范围单独记录，例如 `supported_version="4.4.*"`，不得再把 `4.4.6` 拼进 Mod 自身版本号。

## 唯一版本源

根目录 `VERSION` 是唯一版本源，只包含一行版本号。以下位置必须与它保持一致：

1. `vivhite_infinite_positions/mod/descriptor.mod` 的 `version`。
2. `fixtures/iteration-1/mod-contract.json` 的 `mod.declared_version`。
3. 当前版本的 `CHANGELOG.md` 标题。
4. 正式发布的 Steam Change Note 与 Git 标签。

自动化测试必须拒绝上述版本发生漂移。`supported_version` 是游戏兼容合同，不参与一致性比较。

## 当前版本线

- 当前开发版本：`1.0.0-rc.1`。
- 计划中的首次受管正式版本：`1.0.0`。
- `1.0.0` 收录方舟/游牧殖民地支持、折叠式决议菜单、失控机仆计划 13，以及 Stellaris 4.4 兼容描述符修复。
- 在 I1-003 简体中文反向可见性和发布门禁完成前，只能递增 `1.0.0-rc.N`，不得把当前候选冒充正式发布。

## Changelog 规则

根目录 `CHANGELOG.md` 是所有版本的用户可见变更历史。每次 Steam 发布前必须把本次内容冻结为独立版本条目，至少包含：

- Added：新增功能。
- Changed：行为或交互变化。
- Fixed：缺陷修复。
- Compatibility：支持的 Stellaris 版本及重要兼容变化。
- Validation：简体中文实机与静态门禁的实际覆盖范围。
- Known limitations：尚未解决或明确不保证的行为。

不适用的分类可以省略，但不能把未测试内容写成已通过。英文及其他语言只记录静态翻译校验，不能写成运行时通过。

## 每次 Steam 发布流程

1. 文档先行：确定目标版本、发布范围和验收标准。
2. 更新 `VERSION`、描述符、机器合同和 changelog，运行版本一致性测试。
3. 完成 `open_kaishek`、仓库测试及简体中文实机门禁。
4. 把 changelog 中该版本条目提炼为 Steam Change Note，格式以 `[vX.Y.Z]` 开头。
5. 从干净 Git 提交构造上传目录；确认目标仍为 Workshop `3710613857`。
6. 发布前读取并校验远端原说明，在原文末尾追加已经审核的 BBCode，不覆盖原文。
7. 上传并重新下载/读取远端详情，核对物品 ID、版本、说明、Change Note、文件树和更新时间。
8. 写入最终发布证据并提交；创建、推送 `vX.Y.Z` Git 标签。

任何一次已经成功改变 Steam 远端内容的后续上传，都必须至少递增 PATCH，并新增 changelog 条目。只有远端未发生更新的失败重试可以沿用同一版本。
