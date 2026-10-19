# RC7 自有星结算后的历史岗位引用：原生检查补强

## 已确认事实

恢复 run `20261019T201325Z` 的普通吞噬在2201.10.02自然完成。事前固定的
112人口返还、core5262、C/G23、D7、制造增量0、世界积分+750全部命中。
原 `check_1019.settlement` 在 immediate 与次日 stable 均25/26，唯一失败为
`source_colony_destroyed` 中要求旧colony.pop_jobs列表为空。

完整原生表进一步显示：源已pc_shattered，无owner/controller；colony18的实际
人口列表及活人口计数为空；所有国家owned_planets/controlled_colonies已排除18。
岗位表仍保留原23个岗位及原分配缓存，其中复制者110、巡逻2指向旧group83886081，
但该group已从全局pop_groups移除，112人口已合并到core0的实际group29。
次日这些历史记录仍在。因此“岗位ID列表非空”等同“殖民地仍活”的判断不成立；
也不能仅凭源人口列表为空就忽略全局仍活的人口或岗位。

这属于本项目原生SAV检查器的覆盖缺口，`open_kaishek`的P语法／包级检查本轮
已通过且没有发现该工具缺陷。生产Mod、既有checker/inspector/receiver以及所有
历史FAIL保持原字节；本次仅增加独立的原生存活性补强，继续使用原结算数学。
这里只确认Stellaris 4.5.2本机行为，不推广为Paradox共通规则。

## 目标、设计与范围（实施前）

新增 `tools/check_settlement_liveness_1020.py`，读取实际before/after SAV及原生
来源元数据，重跑原settlement并完整保留其FAIL、各检查值和strict差异。只有原
检查全部通过，或仅source_colony_destroyed失败时，才允许进一步判断。

新增判断同时要求：源破碎、无owner/controller；旧colony没有人口引用或正的活
人口计数；扫描整个全局pop_groups后也没有属于旧colony的正人口；所有国家的
拥有／控制殖民地列表均不含该colony。保留的岗位必须全部是before同一源已有
岗位，原生记录逐字不变、无正自动劳力，所有实际人口分配引用在after全局表中
已消失或为零；全局所有指向旧colony的岗位也要满足这些条件，不能只查局部列表。
非空历史workforce只在分配目标均已死亡且原记录不变时接受；不得接受仍活人口、
新岗位、变化岗位或新的自动生产。无效ID4294967295只按原生无目标哨兵处理。

报告明确区分“无活殖民地／无活岗位分配”与“存储中所有历史对象已被物理删除”。
不修改SAV，不清理缓存，不绕过人口／容量／once-only／危机积分等原检查。
未来重复／真实reload仍用原no-settlement，最后将其传入原settlement的reload参数。

## 验收标准

1. 原25/26 FAIL与其完整差异不改，补强报告单独存储并列出工具与SAV来源SHA。
2. 实际before活殖民地必须拒绝，真实stable已毁源按全局对象核实；不能按after
   核心人口残差设返还预期。
3. 有意义的正反测试覆盖：死引用可保留；仍活人口／遗漏的全局人口／国家拥有
   引用／仍活岗位分配／正自动劳力／新建或变化岗位必须失败。
4. 只有这些独立检查通过，才恢复普通吞噬的后续幂等链；不将原FAIL改为PASS，
   最终报告注明补强合同及其“历史对象未必删除”的边界。

## 已实施与验证

新增独立工具及10项正反单元测试，全部通过。真实 `r8normalpre` →
`r8normalstable` 已运行完整CLI，结果 `PASS_SCOPED`：所有原非存活性检查均真，
原失败仅涉及岗位列表，全局存活性检查通过。原26项诊断仍为25/26 FAIL并完整
嵌入新报告，没有修改旧工具SHA或原件。报告为新run内
`r8normal-stable-global-liveness.json`；后续归档将保留全部源SAV／回执和该报告。

随后恢复原重复回调／真实reload链，最终结果尚待其实际运行。该补强不认证
历史存储已删除、不替代幂等检查、不推进发布总门槛。

## 下一月脉冲的幂等补证（执行前）

原 `normal_destroyed_source_repeat` 的native_save_checks还要求观察下个真实月脉冲。
同日重复与真实reload完成后，复用该实际reload档为R，不新建月脉冲起点档。
从2201.10.03自然FF29到2201.11.02保存I；真实加载同一R，再派发原重复回调、
自然FF29到同一日期保存F。I/F用原no-settlement，比核心人口、容量、账本、
危机及源收据；这样不会把跨月自然人口增长当成重复奖励，也无需按after残差
设人口预期。另从R到I/F核C/G/D/made/worlds、返还/制造收据、成长/六核心等级
保持，以及源无人且没有新的活Situation。完整strict仍保留，若自然状态或日期
不符则保留失败，不自动填PASS。
