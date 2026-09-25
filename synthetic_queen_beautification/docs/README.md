# 合成女王美化 Mod 文档

本目录记录合成女王（Cetana）图片资源调查、人物替换方案和验收证据。当前已根据用户提供的三视图，使用 EvoLink 生成一张真实透明的横向静态肖像，并制成覆盖原版 10 个合成女王肖像键的 `0.1.0-rc.2` 候选包。矩形背景缺陷已通过简体中文实机复测；R2 基础肖像缺少独立场景，R4 提前触发夹具出现运行时错误，均未完成全矩阵验收。它还不是 16 张主要图片全部替换的完整版本，也不是已发布版本。

- [原版图片清单与引用证据](asset-audit.md)
- [参考图与人物肖像生成方案](reference-art-plan.md)
- [实施计划](implementation-plan.md)
- [测试策略](test-strategy.md)
- [透明肖像修复与本轮验收记录](portrait-acceptance-rc2.md)
- [上一候选版验收记录](portrait-acceptance.md)

调查基线为本机 Steam 版 Stellaris `Pegasus v4.4.6 (fdde)`。游戏安装目录保持只读；游戏版本变化后需重新核对图片路径、肖像键和覆盖文件。
