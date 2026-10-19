# RC7暂停收尾的正常停机与冻结日志

目标是按用户收尾授权封存固定run `20261019T164112Z`正常停机后的完整冻结日志，支持后续接手续查；不启动验收、游戏或UI，不改Mod/工具/Git，不读取userdir日志。所有未来guard等测试保持未完成，不提升18case日志门槛或总体PASS。

只读白名单为artifact run下`vacation-stopped-logs/`中明确冻结的19文件、`r7vacation-stopped-log-freeze.json`、`stop.json`、`manifest.json`、`process.json`及`r7vacation-last-paused-frame.*`三件。root交接停机UTC20:00:25.788、PID37300、forced=false、running_after=false；stop SHA `281e90717598a62a0568473e3f3cf856a13b71e5270377f9d751e03d92a9a5b8`，freeze receipt SHA `e4907202f40bcac72d15732ca949227d734b4774698d5ceb7b3e393e4bb6f459`。实际原件双读稳定后才归档。

目的目录`evidence/1020-rc7-vacation-stopped-run-v1`保留原字节，建立来源/hash索引、独立verify和README。验收是完整19日志及5,977,753字节与回执闭合、停机字段/SHA明确、全部原件来源/字节/引用闭合、原图OCR绑定正确。只列简单日志triage及既有PK A/B/AFTER_RELOAD实际marker；原决议key覆盖、原绑定parse错误、修复1 invalid deposit、unowned change_pc时序owner警告均完整保留，不能删掉或宣称wholeproduction无错误。

root追加已闭合`r7vacation-steam-offline-config.json`原字节记录。只读取该已清理记录中的WantsOfflineMode值、alltrue及源hash，不读取原loginusers.vdf，不复制账号ID／名称。该值只证明持久离线偏好，不是实时联网探测；root未改变Steam模式、未发布。

## 封口结果

正常停机回执实际为UTC `2026-10-19T20:00:25.788093+00:00`、PID37300、forced=false、running_after=false，与root给定SHA一致。19份冻结日志共5,977,753字节全部匹配freeze receipt并双读稳定。共27份原件加2份派生清单／triage，29payload、6,241,690字节；末帧图/OCR的PID、图SHA和早于停机的capture时间核对通过。

简单日志清单如下，仅保留事实和已明确的历史上下文，不作全面根因审计：

| 冻结日志时间 | 保留事实／边界 |
| --- | --- |
| 00:41:19 | 多条Workshop路径缺失；不据此推断这些Mod被加载 |
| 00:42:47 | decision_lithoid_swarm_consume_world key由zz_eep_native_decision覆盖 |
| 01:19:40 | select_empire_design的portrait_container缺失消息 |
| 02:45:34–35 | 原绑定输入NOT语法错误、其后无效trigger/effect及undefined target，完整原样保留 |
| 02:53:29 | Repaired savegame, cleared 1 invalid deposits |
| 03:42:08 | timeline_events.txt:2732的owner上下文警告；root提供上下文为unowned change_pc夹具时序，不删除原文 |
| 03:45:39 | nomads_events_1.txt:2268的from上下文错误，country0、from无效ID；保持未归因风险，不断言属于fixture或生产 |

完整error.log共54行及所有上下文未裁剪。game.log实际保留EEP_POSTFIRE_DUPLICATE_A、B（03:24:52）及DUPLICATE_DESTROYED_ENEMY_AFTER_RELOAD_DISPATCH（03:26:59）各一次；这只证明marker出现，不替代原生收益／幂等检查。初始Q2_TARGET_MISSING、纯log probe及后续Q2_CREATED也都保留，不覆盖旧失败。

Steam已清理记录中的WantsOfflineMode为["1"]，all_recorded_accounts_want_offline=true，原VDF源hash为`8f12fbd10f950628d02b6538f5796595155d7b987da980ee3fe4089de7e5a985`。只读该闭合记录，没有读取原VDF，没有账号标识／名称；不能将持久离线偏好说成实时联网状态。未改变Steam模式、未发布。

- [index](evidence/1020-rc7-vacation-stopped-run-v1/index.json)：`e1749b8aa0a44c6df84345149eca06299e9ca61b13f54c8813a5c2d86808f41f`
- [verify](evidence/1020-rc7-vacation-stopped-run-v1/verify.json)：`61dcd178d3a5db9bb27f996ea9ad8c61b8d92a8366f2beeeeb05dd4809ed3b3f`，10/10，限定PASS_NORMAL_STOP_FROZEN_BYTES_TRIAGE_ONLY。

完整日志仍未最终审核，18case日志门槛、总体验收、未来guard等测试均不提升为PASS。主交接见[收尾交接](handoff-heart-of-devouring-2026-10-20.md)；本文不修改主交接。精确stage为本文及整个`evidence/1020-rc7-vacation-stopped-run-v1/`（33文件），共34文件。所有原始source只来自本次明确白名单冻结拷贝和closed root记录，没有读取userdir活动日志、原VDF或未来raw，也未操作UI/Git或改Mod/工具。
