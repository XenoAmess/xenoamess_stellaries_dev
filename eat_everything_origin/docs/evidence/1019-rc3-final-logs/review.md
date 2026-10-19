# RC3 最终日志审阅

本目录归档 run `20261019T092935Z`。正常停止证明为 `stop.json`：PID 34832，UTC `2026-10-19T11:16:49.568209+00:00`，`forced=false`、`running_after=false`。复制前、复制后、独立复核三次查询均确认该 PID 不存在，归档来自已停止进程。

`index.json` 列出 19 个原日志（含全部 5 个 `script_documentation` 文件）及 manifest／process／stop 三个原证明，共 22 文件、5,950,376 字节。复制前后源文件集合、源 SHA256 和归档 SHA256 完全一致。`verify.py` 另行读取全部源与副本，生成 `verify.json`，结果 PASS。`.gitattributes` 禁止原始载荷文本归一化，`git-byte-verify.json` 另证 22 文件预期 Git blob 与原字节一致。没有复制 SAV 或其它 run。

## 完整 error.log

完整 42 物理行、26 条带时间记录均在 `review.json` 中保留，包含空行和原生 scope 续行。

| 原行 | 记录数 | 分类及边界 |
| --- | ---: | --- |
| 1–21 | 21 | 已知启动时缺失 Workshop 文件发现警告；与 `1019-baseline/logs-final/error.log` 同行仅时间不同。当前 manifest 只启用 `mod/ugc_eep-1019.mod`，不能据这些发现警告声称缺失的 Workshop Mod 已加载。 |
| 22 | 1 | 已知原版决议覆盖提示，明确采用 `common/decisions/zz_eep_native_decision.txt:2`；同 baseline。保留这条 Mod 相关提示。 |
| 23 | 1 | 已知原版帝国选择窄条目的 `portrait_container` 警告；同 baseline。它不能单独解释 EEP05 的设计合法性提示。 |
| 24–27 | 2 | 已记录的 hw0 手工诊断失败：`export_modifier_to_variable` 缺参数和无效 `every_ship`。冻结的 `1019-rc3-hardware/hw0-export-command.action.json` 精确包含该命令，提交 UTC09:43:35。没有给 hw0 补写成功导出结论。 |
| 28–42 | 1 | **新增原版事件错误，因果未明**：19:07:59，`events/nomads_events_1.txt:2268` 的 `nomads.94` 在 EEP03 country scope 进入无效 `from`；捕获 `from.id=4294967295`。原版该行是 `from = { is_nomadic = yes }`，事件挂在 `on_war_ended`／`on_becoming_subject`。完整续行、原版源摘录与 SHA256 均保留在 `review.json`。是否由 EEP／巨像结算触发及其影响仍未确认，不能称为无害或排除。 |

本轮没有新增指向 EEP 脚本文件的诊断（除已知覆盖提示），但原版游牧事件错误仍未解决，因此不得写为“无错误”或“日志 clean”。未识别记录计数为 0，因果尚未解决的原版错误计数为 1；两者在报告中分开记录，没有丢弃未知项。

## 完整 game.log 与验收边界

完整 19 行／19 记录包括游戏版本 1、defines 2、同步信息 1、生成世界 2、原版事件选项 10、`eep.10` 选项 3，全部逐条列入 `review.json`。这些是信息记录，事件选项出现不等于事件效果验证通过。该 run 含多个新局，不能仅凭时间或种子给每条信息推定 Machine／Hive 身份。

全部 19 日志已归档；语义审阅范围是完整 error.log 和 game.log，其余 17 日志保留原文，不宣称逐项语义验收。

- RC3 巨像 90 日充能／30 日发射时长：**FAIL，保持原结论**。日志没有指向 EEP 的新诊断也不能推翻真实时长失败。
- Machine 最终 case：**PENDING**；本归档只补受限日志证据。
- Hive 最终 case：**PENDING**；本归档只补受限日志证据。
- 没有执行 UI、Steam、Mod 修改或提交；其它九语言运行时不在范围内。
