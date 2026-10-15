# 加算原生矩阵审计器独立只读复核

日期：2026-10-15。对象为 `tools/audit_additive_runtime_matrix.py` 与对应32项开发测试；主任务告知冻结工具SHA256为 `d6948a5d874b6684912df3e53f69bb3db5e65b925956b5a9068733d0da152787`。

## 目标、范围与验收标准

只读审查7分支×3阶段原生矩阵审计的数据来源、控制条件、算术比较与失败边界。重点核对共同起点manifest、跨阶段测量类就业固定及其它岗位同日跨分支一致、原版/Mod资源分类源表与分母、P/W即时缓存严格合同和有限经济合同的独立状态、完整月 `budget.last_month`、受控输入与原生输出的分离。

先核对当前工具身份，再阅读设计、源码、测试及既有静态/开发报告；不重复执行已通过的32项测试，不改工具/测试/生产代码，不操作GUI或运行游戏。必要时仅用独立内存反例检查可疑路径，并把反例明确写成开发证据，不能当作真实sav或原生经济结果。实质缺陷立即报告主任务，修复由工具所有者处理。

结论应列出可复核的源码位置、覆盖与遗漏，未知语义保留未知；本复核本身不宣称7×3实机矩阵通过。自有JSON保存在 `docs/evidence/feedback-redesign/remaining-2026-10-15/programmatic/additive-matrix-review/`，文档只链接仓库内实际文件。

## 复核记录

已完成冻结版本的只读审查。工具实际SHA256与指定 `d6948a5...` 完全一致，39398字节；测试实际SHA256为 `bd5beb7b10315e62b7ee762eb68ef84ed248a3f9d9d94e8bda2afdf2da7896e2`，AST枚举32个 `test_` 定义。未执行这些既有测试，未修改受审工具或测试。

## 需要修正的两处门禁

1. **已明确失败的社会学差分被总状态忽略。** 受审版本 `audit_matrix` 第550行只汇合guards、unity和阴性checks，没有汇合 `society_secondary`。独立开发反例保持全部控制/就业/凝聚力不变，仅把FP measured的 `last_month.income.planet_biologists.society_research` 改为999；得到社会学 `DUMMY_INCREMENT_FP=FAIL`，但limited/top仍为PASS。主任务已确认：在来源已隔离的有限范围中，明确FAIL不得被吞；次级NOT COVERED可以单列，但不能把失败包装成整体通过。
2. **同分类岗位的来源隔离只看基础workforce。** 第525行 `active` 只认 `workforce>0`。在所有21个开发快照加入已登记同分类额外岗位，固定其base workforce=0而 `automated_workforce=100`，或单独 `bonus_workforce=100`，两反例都得到guards空、limited/top PASS。非零有效来源或无法解释的字段不应因base=0绕过NOT COVERED。这里证明审计器防线有孔洞，不声称当前真实116包样本已出现这个额外有效岗位。

三个确定性输入/完整结果保存在 [开发反例](evidence/feedback-redesign/remaining-2026-10-15/programmatic/additive-matrix-review/development-counterexamples.json)，全部明确为内存开发数据，未生成任何sav。反例复用既有开发数据构造函数后施加上述单一改变，没有调用unittest用例；它们只验证失败传播与源隔离，不能当作经济原生结果。

主任务已把修正交给architecture代理，要求其文档先行、独占同一工具与测试，保持冻结116包不变；本协作者只提交审查事实和证据。原版/包级G1与采样可继续，最终21档须使用修正后的离线审计器重审。在修正与对应负例完成前，本审查结论为 **REVIEW FINDINGS**，不写审计器完整门禁通过。

## 已核对的合同与实际边界

| 合同 | 受审源码位置与结论 |
| --- | --- |
| 七分支、共同源与缺档 | `audit_manifest:569–629`固定七支、三阶段；路径相对manifest解析，缺任一档或声明的common缺失返回NOT RUN。common先读，之后21档顺序读取。`audit_setup_inputs:454–470`比较同日、版本/actor/mod名列表及全部国内岗位语义分配；未提供common单列NOT COVERED。它验证共同源的就业不变性，不自动证明任意声明路径的历史分叉链。 |
| 测量类就业 | `employment_signature:315–329`按岗位/殖民地记录workforce、bonus、automation、容量/限制，并按类别+基础trait键集合计分配，排除易随clone改变的group/species ID。`audit_matrix:480–504`对整个资源分类做input/warm/measured固定检查，包含已知其它同分类岗位；其它国内岗位只要求同phase/日期跨分支一致，允许共同自然增长。 |
| 原生预算与分母 | `budget_snapshot:108–122`保留两期原生表、不填0；`resource_matrix:396–416`仅以measured的 `budget.last_month` 作数值观察。凝聚力分母为维护员实际 `(workforce+bonus_workforce)/100`，社会学为维护员+biologist合并值，未用J100当整个分类分母。自动量在当前两个被测岗位中非零则NOT COVERED；额外来源的漏口见上。 |
| 来源检查 | `source_profile:246–298`读取声明游戏与包的岗位资源表、researcher inline及哈希；原维护员直接产出表严格匹配，biologist表不产凝聚力，未知/条件来源保留有限边界。本次实际只读解析当前游戏+冻结116包得到24个源文件、unity源隔离PASS，同分类为biologist、calculator_biologist、维护员和维护无人机四项。[原源表检查](evidence/feedback-redesign/remaining-2026-10-15/programmatic/additive-matrix-review/source-profile-readonly.json)不证明这些磁盘文件就是任意sav历史所加载字节，仍须共同运行清单/G1/拷贝哈希交叉关联。 |
| 输入与输出分离 | 控制U7/U8、R0、n1、唯一modifier及counter倍率均检查原生观察；dummy键逐真实有居民模板核对，不只看平均整数。Q由实际四格响应独立推导，不硬编码草案差0.44/0.055。工具无sav写入路径；仅写JSON报告，开发快照与原生读取入口明确分开。 |
| P/W即时严格合同 | `extract_snapshot:223–240`保留原生人口/缓存的全部比较，严格缓存有差异则FAIL。`core_guards:368–371`只允许P/W滞后不阻断固定U的有限差分，U/T/B/R等不一致仍门禁失败；顶层汇总仍保留严格FAIL，不能用有限经济PASS抹去。 |
| 日历与完整月份 | `audit_matrix:496–522`要求各支同phase日期一致，input早于warm且在前月或更早，warm/measured相邻月同一1–3日，读取measured.last_month。该表是完整上一自然月，不能把current_month部分累计替代；warm若在2/3日，其前1/2日已属于被测预算月，必须由输入和原生运行顺序证明控制已在月初前成立。端点相同本身不证明整个中间月无临时变动，源码scope已明示此限制。 |
| 阴性与其它未覆盖 | `negative_controls:419–451`要求维护和country_base有实际非零来源，缺失/零不作PASS。外国及station/deposit/building分别NOT COVERED；不能将国内country_base推广为所有非岗位收入已验证。 |

此次只读检查发现的两个失败传播/隔离问题均已立即通知主任务和architecture。其它上述路径在冻结源码层面与已记设计一致；这不是实际21档验收或对所有原版动态modifier的求值证明。

## 证据身份

保留受审源码/测试原字节副本及其SHA，避免工具后续修正后无法复核旧发现：[审查清单](evidence/feedback-redesign/remaining-2026-10-15/programmatic/additive-matrix-review/review-manifest.json)、[d6948a5工具副本](evidence/feedback-redesign/remaining-2026-10-15/programmatic/additive-matrix-review/audit-additive-reviewed-d6948a5.py)、[32项测试定义副本](evidence/feedback-redesign/remaining-2026-10-15/programmatic/additive-matrix-review/tests-reviewed-bd5beb7.py)。新报告为UTF-8/LF，复制的旧源码保持原字节；没有覆盖任何已有实机报告、工具或生产文件。

## 修复后复核范围（先行）

主任务随后指定修正版工具SHA256 `2bee9c8460e07a228d8d0f577aa8245792e2ecc936497c975e6bd422be0173a1`，要求独立只读核修复diff、原三反例的原样重放和结果SHA。复核仍不改工具、测试或冻结116包，不重跑已通过的43项测试；只对旧反例已有JSON输入作三次离线重放，保存新结果及源/结果身份，保留旧反例与结论原件不变。状态只代表两项已发现门禁的修复，不能替代真实21档原生矩阵。

## 修复后独立结论

**两项已发现门禁均确认堵住。** 当前工具实际SHA256完全匹配 `2bee9c8...`；只读diff限定为三处：源表报告显式声明 `society_source_isolated`；对所有branch/phase中整个分类的workforce、bonus、automation逐项判定非零或无法解释；在社会学来源隔离成立时把FAIL/INVALID纳入有限经济总门禁。未引入预算、人口或实验预期输出写入；受审工具仍只读存档并输出报告。

本协作者直接载入原 `development-counterexamples.json` 中的三个 `input/profile`，不改字段或预期，独立重放三次。common使用原F01 input；工具所有者回执使用原F00 input，这两者在setup审计实际比较的同日身份/就业字段一致，重放全部观察结果也逐字段相同。

| 旧反例原名 | 旧limited/top | 修正版独立limited/top | 关键证据 |
| --- | --- | --- | --- |
| `society_failure_does_not_gate_top` | PASS | FAIL | FP社会学dummy增量异常保留FAIL，并传播到limited/top；凝聚力自身仍PASS，未掩盖定位信息。 |
| `extra_category_job_automated_workforce_only` | PASS | NOT COVERED | `UNITY_SOURCE_NOT_ISOLATED`列出额外同分类岗位。 |
| `extra_category_job_bonus_workforce_only` | PASS | NOT COVERED | 同一来源隔离诊断，不再由base workforce=0绕过。 |

输入/profile的规范JSON哈希在调用前后相等；原反例文件SHA256仍为 `47d9525866823e5473dd400cb5115db09b5d810ae7ec60e76950a03f4b81fe6d`。三组独立观察与工具所有者回执的 `repaired_observed` 完全相同。未知/缺失社会学来源仍明确NOT COVERED，不能冒充已覆盖的数值oracle；本修复不把此可选次级未覆盖变成原生测试通过。

另只读核对既有43项测试回执：实记43、failures/errors/skipped均0、工具SHA为本次冻结身份，当前工具测试源码SHA与其 `tests_after_sha256` 相同且AST有36个工具用例定义；另7项为稳定夹具用例。未运行该43项测试，也没有把其开发替身当native矩阵证据。

后续证据单独归档，不覆盖旧发现：

- [独立三反例重放与结果](evidence/feedback-redesign/remaining-2026-10-15/programmatic/additive-matrix-review/after-fix/independent-after-review.json)。
- [修复diff](evidence/feedback-redesign/remaining-2026-10-15/programmatic/additive-matrix-review/after-fix/reviewed-fix.diff)、[冻结修正版工具](evidence/feedback-redesign/remaining-2026-10-15/programmatic/additive-matrix-review/after-fix/audit-additive-fixed-2bee9c8.py)。
- [工具所有者三反例原回执](evidence/feedback-redesign/remaining-2026-10-15/programmatic/additive-matrix-review/after-fix/owner-original-counterexamples-after-fix.json)，原字节SHA256 `cd846500b7a682dde4b6830b653496e625d55091b9db4423c7e1c3a9ea699dee`。
- [已有43项测试原回执](evidence/feedback-redesign/remaining-2026-10-15/programmatic/additive-matrix-review/after-fix/owner-gate-fix-development-tests.json)，原字节SHA256 `0df7be9f4976205efd05cbd71d58584e5a3b9029811d2a73de9e081de6c1201f`。
- [本次归档清单](evidence/feedback-redesign/remaining-2026-10-15/programmatic/additive-matrix-review/after-fix/archive-manifest.json)，记录六份原件/生成证据及SHA。

本章的PASS只指这两处审计门禁的独立修复确认；真实七支21档、严格P/W与有限经济结果须由修正版另行读取原生样本后报告。冻结116包、生产、GUI与源档均未由本复核修改。
