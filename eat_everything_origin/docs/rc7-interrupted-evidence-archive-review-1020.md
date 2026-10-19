# RC7 中断后的证据归档接手

2026-10-20 01:35（北京时间）只读复核发现，高等级 UI 小包 `evidence/1020-rc7-high-level-ui-v1` 已复制原始文件，但尚无 index、独立 verify 和 README，不能视为封口。主线程授权在现有设计内完成这三项及补充映射；不改既有 raw、v1/v2 报告、partial 提案、Mod、工具或活动日志，不操作 UI、Git 或 Steam。

实施范围是逐件复核该包现有 110 件 `raw/r7ev*` 文件与固定 run `20261019T164112Z` 的同名源文件；单独列出 `run/manifest.json` 的来源。索引记录原来源、目标相对路径、大小和 SHA256，并引用已存在的 canonical growth/source 包及既有分析、设计文档。新索引生成后，另一轮独立重读全部目标与源文件、核索引列项集合、两份 SAV 的 ZIP CRC、图与 OCR 引用。不得读取活动日志或新局经济资料，不从其他前缀添文件，不为满足断言改写原报告。

验收标准是原始复制字节完全相等、所有新引用存在且 SHA256 匹配，归档状态明确为限定 UI 证据。原 UI v1 为 55/56、FAIL（选错点击前 frame），v2 为 60/60、PASS_SCOPED；两版完整 strict 比较必须保持相同的 21 条 FAIL。补充映射仅支持 `unlimited_growth.report_level_count_remainder`，完整 case 仍为 PENDING。

同时只读复核了 `evidence/1019-rc7-economy/purifier-attempt1-partial`：146 payload、8,472,471 B 的大小与 SHA256 全匹配，5 份 SAV ZIP CRC 有效，5 个 canonical 引用全匹配。原 receipt 为 CLEANUP_REQUIRED，仅完成 4 个月，m05..12 与 yearUI 不存在，四项操作约束仍 null，不能作为年度通过。RC7 经济分析适配与 RC6 原文按预声明的五类替换逐字一致，替换次数为 2/1/1/1/3，原、新脚本 SHA256 均匹配。

`evidence/1019-rc7-purifier-economy-worker-ui-v1` 仅 `.gitattributes` 与预备 `archive.py` 两件，没有证据 payload、index 或 verify，排除出本次可提交证据清单，不执行、不删除。

## 接手封口结果

已完成原白名单的逐件源/目标复核：artifact 内恰好 110 件 `r7ev*` 普通文件，与现有 raw 集合完全一致，无遗漏或额外前缀；manifest 另外明确列来源。封口为 111 payload、6,129,046 B，25 组图/OCR，19 个 canonical 引用与 21 个绝对引用映射。没有修改任何既有 raw、报告或 partial 提案。

新 index SHA256 为 `bc901c3dc8a0ca82fec94d7a0e34ab59b11aa4c89264a3fa7579b601e1b9c497`；独立 verify SHA256 为 `c87d4bb0b7ee331ea6a2ff21ba761a1eca04325cf91bdf0a21e1da75e737d74c`，9/9，仅为 `PASS_BYTES_SCOPED_UI_ONLY`。两 SAV CRC、所有列项大小/SHA/原字节、引用及原 v1/v2/strict 状态均分别复核。新增 [补充映射](evidence/1019-analysis/rc7-high-level-growth-ui-archive-mapping-v1.json) 绑定项目内保存、原生 receipt、audit、实际图/OCR、关闭输入及原提案；原 strict21 未忽略、未放宽。

本次可提交范围为本页、`rc7-high-level-growth-ui-binding-1020.md`、`rc7-purifier-economy-reception-1020.md`；`evidence/1020-rc7-high-level-ui-v1/` 完整目录；`evidence/1019-rc7-economy/purifier-attempt1-partial/` 完整目录；`evidence/1019-analysis/` 内 `rc7-economy-analysis-v1.py`、同名 `.adaptation.json`、两份 `rc7-high-level-growth-ui-binding-report-v1/v2.json`、原 partial 提案、ready/report 两份 UI observation 和新增 archive-mapping。预备 worker 空包与 titlebar 修复不在本复核提交范围。该清单只保存已完成的局部证据，不生成最终验收结果。
