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

### 月度对照的加载日期栏故障

第一支I已实际到2201.11.02，core5267，预声明的经济／成长账本全部不变。
重新载入R时，原native_load已完成真实选择与Load点击，但GPU完整顶部资源／
日期栏缺失，故其45秒UI日期检查超时；没有生成成功load回执，不把超时改写成功。
新截图确认其余系统／舰队／暂停UI仍在。此现象在旧
`native-relic-health-calibration-1019.md` 已有相同故障记录，原因仍UNKNOWN。

恢复先以新的原生保存核实真实日期和状态，再按旧记录的独立原生`play 0`
重申本国控制，要求新的实际日期帧和状态证据。保留首次失败、额外诊断SAV和
全部动作；恢复记录采用独立schema，不能伪造原native_load成功回执。只有
R日期／身份／账本核对成功后才继续F；若实际日期不同则停止并重载明确原输入。

额外native-save尝试未能打开原生Esc菜单，没有生成诊断SAV；随后play0尝试也因
console不可见而在输入前正确停止，未发送play命令。已核前台窗口和PID均为
32348，Shift/Ctrl/Alt/Win均未按住，游戏Responding=true。下一步先按既有
标题栏几何／HTCAPTION验证做一次物理聚焦，再重试已知play0恢复；不向不可见
console盲打命令。所有失败动作／GPU／OCR保持原件。

标题栏物理聚焦后console仍不可见，第二次play0同样在输入前被拒绝；实际没有
执行任何play0。GPU已目视主菜单按钮，物理点击仅显示tooltip而未打开菜单。
停止继续输入，改用正常退出请求和新的隔离进程恢复已保存的`r8normalreload`
（2201.10.03）进行F支；I支已保存并通过其事前账本不变量。新进程F仍从确切
同一个R的SHA载入、推进相同29日、核同日I/F原no-settlement。另显式记录进程
边界，可同时作为非零成功结算账本的跨进程幂等证据。不能将首个失败load声明
成功，也不把UI故障归因为已证的Mod脚本缺陷。旧run先实际停机／冻结完整日志。

## 最终限定补证与索引合并设计

第三进程从主菜单真实载入完成档，另存后的原no-settlement9/9；本进程实际
dispatch日志标记已出现，随后自然FF29到2201.11.02，F与旧run的I均core5267，
原同日no-settlement9/9，奖励／成长／六核心层数命中事前不变量，无活吞噬任务。
以此新的实际执行链替代此前未获日志支持的warm-reload回调，不篡改旧失败。

完整结算加真实跨进程加载使用独立全局存活性补强PASS；原27项诊断仍26真／
1假（历史岗位列表），完整嵌入。新包三批共464份源拷贝、32,441,459字节，
8份原生SAV及93对GPU/OCR，全部原字节／ZIP CRC／SAV与audit/receipt/history
闭合。原T5进度0→1→4→5→10月2日killed，10月3日Situation已清理；最初辅助
读取误假定stable仍有Situation而KeyError，发生在写报告前，随后按真实缺失记录。

下一步仅通过旧index helper合并normal三个余项与common的本国主体返还单项，
保留旧seed true、所有其它检查及18组PENDING。预期97true／41null；完整日志只
归档和诊断，不提前填入最终log证据。此设计先于索引修改。

### 合并结果

已通过旧helper合并4个原名单项，当前97true／41null，18组及组件仍PENDING；
normal四个原check均有依据，仅缺最终log门槛。其它case、经济、成长typed及旧
seed证据不改。新注册两个真实run，包含原run后共三个。

新包472份payload（含索引／作者报告／提案）、32,858,016字节，938条提案引用
全部SHA闭合。更新可变reference-plan后同步当前`_scaffold.reference_plan`的SHA；
旧`_progress.history`中的历史操作hash保留原义，不冒称当前文件hash。首次完整
引用校验发现该当前指纹待更新，已在提交前纠正；不改历史操作或原始证据。
