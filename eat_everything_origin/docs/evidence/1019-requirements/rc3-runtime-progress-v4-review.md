# rc3 归档核对与 PENDING v4 设计

## 目标与范围（实施前）

只读复核未提交的Machine扩展归档／progress-v3、Hive首月报告及pk1独立奖励校准的原字节链，记录可以进入下一进度版的范围。主线程授权新建 v4：保留v1—v3原字节，从v3复制；修正同一run_id被两份等字节manifest重复登记的问题，保留canonical `1019-rc3-hardware/manifest.json` 为唯一runs项，Machine manifest保留在archives。旧索引不回写，候选源／检查／预算／case状态均不改。

Machine补证继续保留六项scope。pk1已独立冻结的53份校准子集可作为archives及限定观察进入v4，包含原始strict FAIL；只校准同日两目标各手工complete一次的奖励点（worlds750／empires600），不填写巨像实际发射、真实结算或目标只结算一次等case检查。不能把此校准状态作为真实发射before；后续实机结果使用独立版本。Hive首月仅有原活动run引用，本轮验证其当前原字节／SAV gamestate／receipt，不将未归档证据挂入进度；等待阶段包后另起版本。

验收：所有Machine358份及pk153份payload核对索引SHA／大小；核对报告原件与归档副本；递归校验v3／v4全部项目内引用；Hive3份SAV、audit、receipt和gamestate当前匹配。v4的runs长度必须等于唯一run_id数量，canonical原SHA保持，非canonical manifest仍可从archives追溯。保持v1—v3原SHA、18组PENDING、14个机器单项true、所有预算／成长／冻结源不变；最终验收器仍拒绝PENDING。无UI、Steam、Mod、工具代码、版本、提交或推送操作。

## 可追加与暂缓

| 证据 | v4处理 | 边界 |
| --- | --- | --- |
| Machine archive-index-v2／六项补证 | 保留v3全部有效引用和scope；仅将重复manifest从runs移至archives | 仍缺最终活动日志及case共同审查 |
| pk1独立校准包／报告／strict FAIL | 可新增archives和scoped calibration observation | worlds／empires分别是奖励点，不是击毁次数；不填firecase或随机组件 |
| Hive首月23项＋10项UI比较 | 只记录当前字节核查结论，暂不挂v4 | 原生存档等尚无项目内阶段归档；全年／操作约束未完成 |
| 正在执行的PK／Hive／活动日志 | 暂缓 | 等完整结果和稳定归档；不复用硬件早期log |

## 正式发布剩余硬门槛

1. 完成并归档全部限定运行时矩阵：Hive／Purifier各12月、Lithoid首月、母舰同国同日参照／实际跳跃／十船坞、无限成长及自然随机组件阈值／补发／幂等／重载、真实巨像发射／禁用目标／取消与统一结算、普通拆解回归、旧档迁移和重复初始化。Machine两组需完整冻结log及共同审查；新报告不得覆盖原FAIL或扩大scope。
2. 最终原生SAV／截图／动作／日志／分析五类证据、唯一run_id及精确EXE／单生产Mod／源哈希／新CSV与三回调静态合同绑定到正式 `final-result.json`，严格check-runtime通过。当前v4仍为PENDING，不创建final-result。
3. 正式只改VERSION及descriptor版本元数据至未发布的新SemVer0.4.0，再做正式open_kaishek与static-source-manifest。上传前先完成六类CHANGELOG、从同条目提炼的 `[v0.4.0]` note、准确工坊说明，6槽图库替换WS-06为已验Purifier新开局图且新文件名；保留4条历史immutable内联图并最终核可达。
4. 准备／冻结／提交推送全部发布输入，干净且已推送后preflight。最后才由主线程上线更新本项目3815707212，独立下载逐字节及公开文案／图库／内联图核验，先提交推送验证凭据，再tag-check／创建推送v0.4.0，恢复离线。只读上游3710613857始终禁止上传。

## 实施及字节审查结果

已生成 [progress-v4](rc3-runtime-progress-v4.json)，SHA `6f62ec128741ae936387d980d801ea22e91ff125be90c6dd80f5b4c4855b1116`。v1—v3原SHA未变。Machine358份／22,662,741字节与pk153份／3,206,832字节均和索引及当前原来源一致；v4全部246次引用／133个唯一文件通过实际SHA核验。Machine六项scope完整保留，18组／组件／顶层仍PENDING，14个机器单项及全部预算／成长／冻结源与v3完全相同。

新v4只保留一份canonical硬件manifest作为runs；同run_id的等字节Machine manifest保留在archives。诊断直接从实际 `validate_runtime_index` 提取完整manifest拒绝条件的Python AST，对真实元数据求值：v3两项结果为`[不拒绝, 拒绝重复]`，v4唯一项为`[不拒绝]`。没有改任何对象的验收状态来绕过前置层，也没有创建诊断PASS索引。完整最终验收器仍因PENDING按预期拒绝。AST语义指纹独立于Git换行转换，不新增对普通工具源文件原始CRLF字节的持久引用要求。

pk1校准的17项限定通过、worlds750／empires600奖励点以及原strict FAIL均以archives／限定观察追加，所有firecase检查不变。Hive当前三份SAV／audit／receipt、manifest和解压gamestate匹配，23项开局＋10项UI字段一致；因没有阶段归档，未挂入v4，也未把首月充作全年经济。更详细的读数及诊断见 [v4字节审核](rc3-runtime-progress-v4-byte-audit.json)，SHA `5e6be572372c54fe5780d9052dd61311f0938582014b687a82e32a2e08950908`。当前仍无final-result或0.4正式发布证据目录。
