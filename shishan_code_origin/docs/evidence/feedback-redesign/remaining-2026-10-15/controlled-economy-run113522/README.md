# 稳定度控制与停止组装后的原生经济证据

本目录保存简中 run `20261015T113522Z` 的原始证据及只读审计。使用4.5.2原生保存界面生成48份存档，没有手写或重新打包SAV。运行于2026-10-15T12:47:37Z正常停止，`forced=false`、`running_after=false`；见[停止回执](stop.json)。原始JSON中的绝对路径保留为采集来源，本页导航使用仓库相对链接。

## 加载身份和范围

- [实际加载清单](manifest.json)为116文件隔离经济包，启用`-debug_mode`，实际1600×900、请求缩放0.75，只用简体中文。正式0.2.1的90文件逐路径、大小和SHA与[发布身份](../../../../../evidence/v0.2.1/acceptance/release-identity.json)完全一致，其余26文件为测试覆盖；本run不是纯90文件正式包。
- 先行[116文件G1](../additive-static/v2-stability-control/additive-stable-fixture-open-kaishek.json)为PASS，SHA256 `be2f0167eaa86656c20fd74e1b6abd413ca3008c20fb54bac4e87dbe262949b7`。G1只支持其明示静态边界，不代替原生经济采样。
- [最终来源完整性核对](independent-run113522-final-input-integrity.json)逐一验证48份SAV与真实userdir源字节、原生保存回执SHA/大小、ZIP CRC、原始meta及gamestate日期；417组图/OCR的图像SHA和实际像素尺寸全部匹配。该报告只判来源完整性，不判经济算术。
- [最终审计来源身份清单](additive-final-readonly-evidence-manifest.json)保留15项原始报告及代码/测试快照。所有`.py`仅保留当时身份，不运行改名副本；执行入口仍以各独立文档所指仓库文件为准。开发测试通过不等于实机分支通过。

## 两套七分支与控制前置

| 证据 | 原生存档及结论 | 保留边界 |
| --- | --- | --- |
| [首次七支清单](additive-stable-growth-matrix-manifest.json)、[完整审计](additive-stable-growth-native-audit.json)、[数值摘要](additive-stable-growth-native-numeric-summary.json) | 21档：每支input03.02、warm04.02、measured05.02。稳定度已控制100，人口仍自然增长；整体INVALID、严格P/W共32项FAIL。 | F01/F11/FN同阶段普通就业/人口比其它支少1；算术差分通过不能覆盖窗口失败。FP使用attempt2三档，首次失败原帧保留。 |
| [正常关闭组装的原版来源计划](independent-native-population-control-source-plan.json)、[三档控制审计](independent-ecng-native-population-control-precheck.json) | `ecng_control_input_0302`、`ecng_warm_0402`、`ecng_common_0502`。原生UI停止组装，实际人口、四组及就业连续两月稳定，净增长字段0。 | 立即input的旧P/W缓存2项FAIL保留；warm/common严格通过。分来源增长细项UNKNOWN保留，控制前置本身不是七支经济PASS。 |
| [停止组装后新七支清单](additive-no-growth-matrix-manifest.json)、[完整审计](additive-no-growth-native-audit.json)、[数值摘要](additive-no-growth-native-numeric-summary.json) | 另21档：每支input05.02、warm06.02、measured07.02；独立共同源为`ecng_common_0502`。限定样本、setup、严格P/W和来源隔离均PASS。 | 限U7/U8、R0、n1、J100及下述已登记岗位/账目；不覆盖全部岗位、资源、其它特质组合、外国经济或所有中间tick。 |

共48份：两套矩阵各21份，加6份共同源/控制/失败恢复档。此前run112046的[自然F01窗口INVALID](../natural-economy-run112046/README.md)不被本轮结果覆盖。首次稳定度100但仍增长的21档及全部旧报告也不被新21档覆盖。

## 新七支的有限加算结果

F00/F10以测试抵消修正抵消B，F10/F11另加同区A=40%；正式架构modifier仍存在，不能将F00写成正式机制被删除。以真实登记就业和成熟上月账目归一化后：

| 分支 | 有效正式特质U | 凝聚力 | 社会学 | 归一化消费品维护 |
| --- | --- | --- | --- | --- |
| F00 | 7 | 1.55 | 4.65 | 1.125 |
| F10 | 7 | 1.95 | 5.85 | 1.125 |
| F01 | 7 | 1.90 | 5.70 | 1.125 |
| F11 | 7 | 2.30 | 6.90 | 1.125 |
| FP | 8 | 2.35 | 7.05 | 1.125 |
| FN | 8 | 2.35 | 7.05 | 1.125 |
| FH | 8 | 2.35 | 7.05 | 1.125 |

凝聚力Q=1、社会学Q=3；开关B的增量在A0/A40均为0.35/1.05，四格交互项为0。正、负、隐藏的无原有效果测试特质各使U7→8、B0.35→0.40，另增0.05/0.15，支持本版原生岗位加算，不能写成最终独立乘算。

被测维护岗位真实workforce100、bonus10、automated0；生物学家60、bonus6、automated0稳定，J只计真实100。全部国内岗位及人口在每个对应阶段保持一致；原生快照间的每一tick并未逐帧证明。country_base九项固定收入也在七支间保持；其阴性对照不能扩张成所有非岗位来源均已穷举。

## 有限资源和费用补充

[费用及来源补充v2](budget-supplement/native-budget-supplement-v2.json)、[简明逐行摘要](budget-supplement/final-budget-summary.json)在同一新21档及共同源上只读复核，未改SAV、夹具或核心2bee审计。29条普通费用全部保持；包括已实际存在的人口维护5行及官员上月凝聚力8。成熟上月账目与观测到的官员当月10分别保留，没有混用两者。

11条实际岗位收入行加算差分通过，涉及能量、矿物、合金、消费品、凝聚力、贸易及三科研；18条实际独立非岗位收入阴性通过，包括country_base九项、力量投射影响力、轨道矿床能量/矿物、轨道研究矿床工程学、四人口类别贸易及恒星基地模块能量。仅认证这些出现且非零的行，未出现资源或来源不据此判定。

[首次v1报告](budget-supplement/native-budget-supplement.json)的FAIL原样保留：它把`trade_policy.trade`当普通费用，发现该行随岗位贸易增产而变。v2依据[原版转换来源](budget-supplement/native-conversion-source-facts.json)精确验证当前实际default政策：岗位贸易加四类人口贸易作为上游，`trade_policy`贸易吞吐及能量/贸易收入分别按50%返还。三条转换行共59项核对通过。只对这个已核实政策分类为衍生转换，没有豁免全部非岗位，也没有将v1初报改写为PASS或把吞吐变化认定为维护缺陷。

[补充原件清单](budget-supplement/archive-manifest.json)保持独立15文件包原字节，含两版源码、测试、原版来源、首次开发失败回执及v2命令exit0回执。开发9/7测试属于开发证据；原生矩阵结论仍取相应真实存档报告。

## 历史失败与日志

- FP首次原生载入列表搜索失败的20组`econstable_FP-load-list-0`至`19`图/OCR全部保留；第二次attempt2成功，旧矩阵指向实际成功三档。失败发生于变更前，没有伪造首轮原生档。
- [F10首次READY日志守卫失败](F10-original-log-ready-guard-failure.json)、[原生状态独立复核](F10-native-after10-log-absence-check.json)、`econstable_F10_after10_log_missing.sav`及回执均保留。实际`.10`未重发，再执行`.20`继续；缺少新日志的原因仅为待证假说。
- 11份原始源码快照及5份`native-driver-*-revision.json`保留修订链，包括执行前import失败、列表搜索失败及输入守卫修正；最终driver SHA与manifest中`4de91816…67e21`相同。
- [完整原始error.log](error.log)共21条缺订阅路径提示，此外无新增诊断。没有过滤这些行或宣称零错误。[logs.zip](logs.zip)在正常停止后保存完整19文件，含空日志和原生脚本文档；逐条目SHA验证与userdir源字节相同。
- 原始action、console、native-save回执、所有原图/OCR和独立审计均保留原字节。归档清单的PASS只表示证据完整性，不代替台账的用例状态。

## 未覆盖范围

核心新七支认证当前个体机械单首都样本的登记凝聚力/社会学隔离差分，补充认证上述实际出现的11岗位收入、18独立非岗位、29普通费用及default政策三条转换行。未覆盖完整资源×岗位矩阵、国内非主体谱系岗位、外国资源账目、空间站/矿床/巨构/建筑全部收入、其它贸易政策、R高值的经济差分、所有原有效果特质组合、食物机械等特殊来源、每个阶段完整经济路径或PF-01性能。原74项台账整项仍按其完整范围判定，不能将有限七支通过改成这些整项全部PASS。

本轮环境最终恢复见[环境回执](../batch-final-environment.json)：游戏退出、Steam离线、桌面1920×1080、正式90文件保持。该回执不扩大经济验收范围。

归档在两位独立审计者确认READY并停止追加后一次性封口：[来源及日志归档清单](archive-manifest.json)、[全部文件SHA清单](file-manifest.json)。费用子目录另保留原清单；总清单排除自身，避免自引用哈希。封口后不再修改本目录原件或清单。
