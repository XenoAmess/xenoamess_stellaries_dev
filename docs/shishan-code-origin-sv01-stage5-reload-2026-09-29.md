# SV-01 第五阶段存档重载（2026-09-29）

## 目标与范围

按[验收方案](shishan-code-origin-acceptance-plan.md)核对第五阶段存档在正式单 Mod 简体中文游戏中重载后，局势、维护次数、主物种特质、白绮阶梯和双项目研究队列均保持。此项只执行既定重载测试，不修改正式 Mod 或研究进度。

## 操作与结果

正式单 Mod 校验和为 `fe44`。在同一游戏进程中先载入已重构的 `2230.07.03` 存档，再从游戏内菜单重新载入[第五阶段锚点](../assets/shishan-code-origin/evidence/pr02-stage5-maintain-anchor-2229.10.15.sav)。重载后简中局势界面仍在第五阶段，月进度显示 `+7.0`，资源负面修正显示 `-75%`；[局势截图](../assets/shishan-code-origin/evidence/sv01-stage5-reload-situation-2229.10.15.jpg)。情报日志保留研究中的清理项目，费用为 `12000` 社会学；[项目截图](../assets/shishan-code-origin/evidence/sv01-stage5-reload-clean-cost-12000.jpg)。暂停同日重新保存[重载后存档](../assets/shishan-code-origin/evidence/sv01-stage5-reloaded-2229.10.15.sav)，SHA-256 `9698058083d9cafd72dc44c72f48cd4a8bd91191e95a58286c605b450b8713af`。

只读解包两份原生存档，以下字段重载前后**逐项一致**：日期 `2229.10.15`、维护次数 `n=2`、局势数 `1`、进度 `950.0`、主物种仅有一个 `trait_shishan_code` 且无 `trait_shishan_refactored`、全国重构岗位修正 `0`、白绮基础修正一层且工程/社会阶梯各两层、维护项目 ID 5 研究进度 `28.33912`、清理项目 ID 6 排队进度 `0`、普通社会学科技仍在第三位。两份存档均无临时社会学加速修正。锚点 SHA-256 为 `35deeddcd9a1ca23156ed9e013fb206e69a16c19e2f858b1512fa7575676823e`；重载后存档哈希不同是重新序列化的正常结果，判断依据是上述逐项状态与游戏界面。

**结论：SV-01 的第五阶段重载子项通过。** 这不代替 SV-01 其他指定状态的逐项核对。
