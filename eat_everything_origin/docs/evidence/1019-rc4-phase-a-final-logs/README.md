# RC4 phase-A 停止后完整日志

run `20261019T112808Z`、PID36644 已于 UTC `2026-10-19T13:04:30.124487+00:00` 正常退出，`forced=false`／`running_after=false`。复制前独立查询及复制前后／独立验证的进程检查均为 ABSENT；process 的 EXE／userdir 参数与 manifest 一致。

完整 19 日志（含全部 5 个 script_documentation）及 manifest／process／stop 共 22 个原文件、5,908,410 字节，全部原字节复制。`index.json` SHA256 为 `4005683aec3ae8c5a6e46b9b9501d19c449fe68c57076c57a49e6843d877b966`；`verify.json` 独立重读源／副本与 6 份既有 canonical 引用，结果 PASS。`git-byte-verify.json` 证实22原文件不会经 Git 换行归一化。未复制59个 Mod 文件、SAV、其它 profile 或后续 run。

源码／门禁复用 `../1019-rc4-pk2-duration/archive-index-v3.json` 及其 `source_snapshot/`，原始内容不改。此处只补该 phase 停止后的完整日志，不把 v3 阶段验收或本次字节校验升级为整个 Mod PASS。

完整语义审阅见 `review.json`，独立来源及逐行复核见 `review-verify.json`：

| 日志 | 完整分类 |
| --- | --- |
| error.log，53物理行／25记录 | 21条 baseline 缺失 Workshop 发现警告；1条 baseline consume 决议覆盖；1条有精确提交 receipt 的错误 DISMANTLE 试验；2条原生 nomads.94 无效 from，完整 scope 保留。 |
| game.log，6行／6记录 | 游戏版本1、defines2、first_contact 选项3；只作信息记录。 |
| debug.log，1行／1记录 | building_type.cpp 缺建筑类别警告，与 baseline 仅时间不同；日志没给建筑 key，具体对象与影响仍未解释。 |

DISMANTLE 的试验输入 UTC12:05:41.730877，错误日志20:05:42；receipt 实际使用错误回调两次，已经与 v3 原字节副本核对。它不是生产 DEVOURER 失败，也不是成功的去重测试。

第一条 nomads 错误20:09:31已在 EEP 真实实发／后续清理分支证据中；第二条20:20:06精确位于原版手动 CRACKER 完成回调＋两日推进的 P→Q375字节，FROM 显式为 Mother fleet。后者不是实际原版武器发射／90日验收。最终 error.log 与该控制 R 副本完全相同，R之后直到停止没有新增错误字节；这不证明随后 Relic／jump 功能通过。

未分类 error/game 记录为0，但两个 nomads 的精确 native hook／FROM 传播因果及 debug 建筑对象仍未解决，不能称无害或 clean。其它完整日志保留原文，不声称逐项语义验收。RC3 历史时长 FAIL 和所有未完成的迁移／经济／成长／全 Mod／公开发布用例保持各自边界。

本归档为停止后的 phase-A 完整日志证据；没有执行 UI、游戏控制、Steam、Mod／SAV修改或提交。
