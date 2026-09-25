# Stellaris 4.5.1 合成女王肖像文件编码与验收

日期：2026-09-25。适用范围是 Stellaris `Cygnus v4.5.1 (358e)` 的 `gfx/portraits/portraits/21_portraits_cybernetics_synthqueen.txt`，以及本仓库对此文件的同路径覆盖。该版本原版文件 SHA-256 `9a2ccd43d297112176092e62a9e488b63a8ca271915d028b84e14491724fee18`，与已核对的 4.4.6 基线逐字节相同。

本机隔离实机发现：将此肖像定义写成带 UTF-8 BOM 的文件（前三字节 `EF BB BF`）会使游戏在 `portraits.cpp:963` 报 `Unexpected token`，随后的 `cetana_*` 肖像键都无法找到。删除 BOM、保留 UTF-8 正文及相同肖像定义后，4.5.1 能正常加载，在合成女王危机对话中呈现新 DDS。这里的结论仅覆盖该实际测试文件和版本，不推广到所有 Stellaris P 语言文件。

`C:\workspace\open_kaishek` 的精确肖像文件 profile `stellaris-4.5.1` 已增加 BOM 拒绝逻辑：带 BOM 返回 `STELLARIS_PORTRAIT_UTF8_BOM`，无 BOM 的本 Mod 生产文件返回 `VALIDATED` 且 0 语法、0 语义诊断。工具修复提交 `dbe1c1b`、`32d0ab4` 已推送。Mod 的失败日志、成功实机截图和详细验收见 [牢大候选版记录](../synthetic_queen_laoda_replacement/docs/portrait-acceptance-rc1.md)。
