# RC4 原版 CRACKER 完成回调对照分析

## 目标、范围与验收

只读分析 run `20261019T112808Z` 从 `pk2base` 原生载入、显式 FROM=Mother fleet 的原版 CRACKER 完成回调、推进两日、原生保存 `pk2nativecontrol`、随后实际恢复 base 的完整链。不是原版武器真实发射或 90 日充能验收，不修改 Mod、SAV 或 UI，不提交。

准备档为 2200.03.07，SHA256 `be5a344439dafe105d4959b4afa31143331b1daaaf915dba28bc70ee23f6f2e2`；结果档为 2200.03.09，SHA256 `49b3405d5265de6b9b471f778b67a573c521f2988499b6b7c7d4d45b7d6fe208`。核实原生保存／载入回执与实际命令，直接读取 SAV 的目标17、colony1、country1、country0 原生两项目标和 EEP 账本；不因通用 auditor 不再收录未殖民星就称物理星球不存在。

B／P／Q／R 及 total-log 回执齐备后，独立核实稳定阶段副本与 delta 的字节数、SHA256、连续前缀及精确偏移，完整保留新错误。只分析这些明确标为 active observation 的已保存阶段副本，不把当前活动日志当最终冻结证据。必须区分原版 callback 的原生计分与 EEP 结算；同错误重现只支持受限复现，不能证明具体原生 hook 或 EEP 没有缺陷。

输出精简独立报告与完整来源路径／hash，不大规模归档。恢复回执仅证明实际载入动作与 UI 日期时，不升级为完整游戏状态恢复证明。

## 当前状态

R 和总回执已齐备；只使用已保存的阶段文件，未读后续 r4relic 或当前活动日志。独立报告见 [analysis.json](evidence/1019-native-cracker-control/analysis.json)，重读验证见 [verify.json](evidence/1019-native-cracker-control/verify.json)，只读提取程序为 [analyze.py](evidence/1019-native-cracker-control/analyze.py)。报告逐项列出 35 个完整来源路径／字节数／SHA256，不大规模复制档案。

## 实际对照结果

| 项目 | 观察 |
| --- | --- |
| native 输入链 | 实际 load 回执指向原始 `pk2base` SHA，UI 日期 Mar7；精确提交原版 CRACKER 完成 callback、显式 FROM=`event_target:eep_mothership0`（fleet159），再 `fast_forward 2`。结果原生 SAV／receipt／audit 对应 Mar9 和指定 SHA。 |
| physical planet17 | 原版 `pc_alpine`、size19、owner1 → 仍有物理对象，`pc_shattered`、size19、owner 字段不存在。不是物理星球对象被删除。 |
| 国家／历史殖民地 | country1 原始数据库条目为 `none`；colony1 的历史对象仍保留。这不矛盾于殖民地已毁，不能把历史缓存当仍有活跃国家或殖民地。 |
| EEP | country0 全部 `eep_*` 变量与 base 相同，包括 C0／G0／D2／made0／worlds0，六核心镜像等级与奖励字段保持0。没有把原版 callback 的计分当作 EEP 结算。 |
| native 危机目标 | 两档均为 `nemesis_path`、`crisis_level_1`。destroy_worlds 原块缺失 → progress750；destroy_empires 前后均无块，在已确认该 native path 的限定解释下是0→0，不能填写600。原有 destroy_enemy_ships75保持。保留完整 raw progression 供复核，不把本对照强制套成实际武器奖励预期。 |
| 恢复 base | 存在实际 restore load 回执，源 SHA 与 Mar7 UI 日期正确；回执本身 `state_verified=false`，没有新 post-restore SAV 时不升级为全状态恢复 PASS。 |

## 日志区间独立验证

| 阶段 | UTC | error.log 字节数 | 新区间 |
| --- | --- | ---: | --- |
| B，载入前 | 12:17:27.278958 | 3200 | 原始前缀 |
| P，派发前 | 12:19:13.444649 | 3200 | `[3200,3200)`，0 字节 |
| Q，结算后 | 12:21:49.142635 | 3575 | `[3200,3575)`，375 字节 |
| R，恢复后 | 12:23:33.142501 | 3575 | `[3575,3575)`，0 字节 |

所有阶段副本与各自 receipt／总回执完全一致；P 保持 B 全前缀、Q 保持 P 全前缀、R 保持 Q 全前缀，各 delta 文件等于相应字节切片。B／P SHA256 为 `c92f44f4b866edab8f69a8b2e1ce7a860e5487c407541f5b9a5f9298841deb98`；Q／R 为 `6546aa90e235446ceb64c213e238071cd237d10cc6172db62c31112ee4ac1192`。

P→Q 的精确 375 字节（SHA256 `b9979ba9c340db5e18766452a9c13284030b3306ddb1ff71464c18c5cf7f293a`）只包含一条新错误及其完整 scope：20:20:06，`events/nomads_events_1.txt:2268` 的无效 from；ROOT 为 EEP03 country0，FROM country id 为4294967295。B 中原先已存在另一条 nomads 错误，及缺失 `on_destroy_planet_with_EEP_PLANET_KILLER_DISMANTLE` 的诊断，均保留并分开记录；本报告没有追认该旧 DISMANTLE 调用来源，不能称总日志 clean。它们不计为本次新增，只因字节前缀得到独立证明，不是按名称过滤。

## 因果范围与限制

原版 CRACKER 完成 callback 加两日推进的这条受控路径，确实又出现同一 native nomads.94 错误；该命令没有直接派发 EEP 完成 callback，EEP 国家账本保持基线。因此该错误不能仅据出现于 EEP 拆星后就归为 EEP 结算独有。

这不证明精确由哪个引擎 hook／FROM 传播步骤触发，不证明无害，也不排除 EEP 的其它缺陷。此 run 仍启用 EEP Mod，并非无 Mod 的纯原版新局，也没有“只推进两日而不派发 callback”的平行控制。原版手动 callback 与实际武器的 Carrier 作用域／延迟／原生奖励可能不同；本次 worlds750／empires0 如实保留，不外推实际原版武器计分或 90 日时长。

总回执明确为 `OBSERVATION_ONLY`／`COLLECTED_NOT_ACCEPTED`；阶段证据不是最终整 run 的日志冻结。此处仅收集了 error.log 的 B／P／Q／R，未提供 game.log 偏移，不能声称两种日志全链都已分段验证。没有宣称全字段 SAV 严格差异通过或全部原生副作用不变。原生计分、外交、人口及碎裂矿藏等副作用不并入 EEP 收益，完整原档通过来源引用保留。

本轮只写本说明及独立证据目录，RC3 原始 22 文件、索引和 SHA 没有更改；没有 UI／Mod／SAV 修改或提交。分析稳定后停止写入，交主线程统一 checkpoint。
