# RC7 高等级母舰与报告 UI 限定证据

固定 run `20261019T164112Z`、`0.4.0-rc.7`，仅包含已结束的 `r7ev` 压力分支。`raw/` 的 110 件文件与原 artifact 目录全部同名 `r7ev*` 普通文件集合一致；`run/manifest.json` 为单独列明来源的一件额外文件。共 111 payload、6,129,046 B，保留原字节，没有活动日志或新局经济数据。

`index.json` 逐件记录来源、目标路径、大小、SHA256，并绑定 19 个既有 canonical 引用、25 组 GPU/OCR 图像及 21 个原绝对引用的项目内映射。`verify.json` 是在另一 Python 进程中独立重读源与目标、核原报告 SHA、两份 SAV ZIP CRC 和 OCR 绑定后的 9 项检查结果。复核时可以按索引逐件比较源/目标字节与 SHA，遍历 `raw/`、`run/` 比较列项集合，并检查 canonical 与 absolute-reference 映射，不必启动游戏。

原 UI v1 仍为 55/56、FAIL：把点击前的匹配 frame 当作关闭后的证明。v2 通过实际点击后、下一次 Escape 前的 frame 证明关闭，为 60/60、PASS_SCOPED。两版完整 strict 比较逐项相同，21 条 FAIL 全部保留，不因归档改判。

本包只支持 `unlimited_growth.report_level_count_remainder` 的实际 UI 部分；完整 case 仍 PENDING。母舰详情中的高等级三防是受控压力分支的当时显示；旧 export 变量没有重新导出，不能作为 C20500 新 modifier 测量，面板 damage 也不能作为实测战斗 DPS。本包不替代全功能配置、跳跃、自然恢复、新局年度经济或最终 18 组验收。

原 v1/v2 报告和 partial 提案位于 `../1019-analysis/`，保持原字节；新增 `rc7-high-level-growth-ui-archive-mapping-v1.json` 把 index、verify 与真实项目内原件补充绑定。归档接手过程与可提交范围见 `../../rc7-interrupted-evidence-archive-review-1020.md`。
