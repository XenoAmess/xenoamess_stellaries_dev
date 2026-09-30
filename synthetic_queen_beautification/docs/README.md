# 合成女王美化 Mod 文档

2026-09-30 仓库已准备正式版 `0.1.1`，兼容声明更新到 `4.5.*`，检查基线为 `Cygnus v4.5.1 (358e)`；原版肖像定义与 4.4.6 基线字节相同。兼容验收见 [全项目兼容检查](../../docs/stellaris-latest-compatibility-2026-09-30.md)，工坊更新状态见 [逐包发布记录](../../docs/steam-compatibility-releases-2026-09-30.md)。以下 4.4.6 报告保留为历史证据。

本目录记录合成女王（Cetana）图片资源调查、人物替换方案、验收证据和工坊发布。肖像替换首版 `0.1.0` 已作为[全新公开工坊物品 3807768508](https://steamcommunity.com/sharedfiles/filedetails/?id=3807768508)发布：根据用户提供的三视图，经 EvoLink 生成一张真实透明的横向静态肖像，覆盖原版 10 个合成女王肖像键。矩形背景缺陷已通过简体中文实机复测；R2 基础肖像缺少独立场景，R4 提前触发夹具出现运行时错误，均未完成全矩阵验收。它还不是 16 张主要图片全部替换的完整版本。发布回执与远端核验见[首次工坊发布记录](workshop-release-plan.md)。

- [原版图片清单与引用证据](asset-audit.md)
- [参考图与人物肖像生成方案](reference-art-plan.md)
- [实施计划](implementation-plan.md)
- [测试策略](test-strategy.md)
- [透明肖像修复与本轮验收记录](portrait-acceptance-rc2.md)
- [上一候选版验收记录](portrait-acceptance.md)
- [首次工坊发布计划](workshop-release-plan.md)

调查基线为本机 Steam 版 Stellaris `Pegasus v4.4.6 (fdde)`。游戏安装目录保持只读；游戏版本变化后需重新核对图片路径、肖像键和覆盖文件。
