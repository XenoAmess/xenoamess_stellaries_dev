# 反馈改版的程序性合同检查

日期：2026-10-04。用户要求只做开发和基本程序性验证，不启动游戏、不抢占屏幕。本检查器在实施记录约定的范围内开发，先记录目标与验收边界，再增加工具和测试。

工具位置为 `shishan_code_origin/tools/validate_feedback_redesign.py`，负例和边界回归为 `tests/test_shishan_feedback_redesign.py`。工具直接解析候选包脚本和本地化，不导入生产生成器的数值常量作为预期。使用标准库，运行期间不导入桌面自动化依赖、不启动进程或游戏，不改写 Mod。

数值预期独立来自已批准的设计：初始月速 1，维护次数每次 +0.25，两个维护职业的实际劳动力合计后每满 100 减 0.25，下限 0.2；起源额外 -6 点/+3 选择；维护/清理/优化费用分别为 2000+1000n、8000+2000n、4000+2000n；研究所岗位社会学 3、凝聚力 1；阶段经济/武器/速度惩罚减半；白绮的社会学为正向增益，凝聚力维护减免只作用于本人。工具解析实际 script values，固定输入与独立预期进行对照。

奖励检查针对实际产物的有限触发器/效果子集进行离线执行。验收重点为候选唯一性、第一层优先、同票据最多一次重抽、三次实体确认冷却、耗尽奖励和旧档迁移的幂等性。只覆盖解释器明确支持的语法；未知触发器或效果默认报错，不能静默当成通过。候选状态机使用独立夹具提供资格事实，另执行无资格覆盖的实际触发器样例，并检查所有 39 个资格/授予入口的国内、主体谱系和实际人口条件。物种克隆只检查生产 AST 的作用域结构，授予步骤由明确标记的抽象夹具 hook 表示；这不证明引擎克隆行为。

改版审查补充的窗口锁和成功凭证恢复同样检查实际 AST：重复打开只排一个窗口；稍后关闭释放锁但保存票据；重抽替换窗口；确认释放锁。选项在显示后失效时，引擎关闭窗口但内部守卫可能拒绝操作，所以 39 个确认入口和重抽入口均须在守卫前释放锁。拒绝只改变窗口锁，待选票据、候选、n/R、冷却和授予均保持；通过实际首都决策 wrapper 重开后，执行 `.1000` 的刷新可修复失效候选。业务快照比较只排除该窗口锁，其他字段仍精确对照。保存中的维护/优化凭证通过 `.60` 排队恢复，旧票据待确认时新凭证保留，两个凭证不能覆盖同一待选票据，清理先完成后仍保留已赚取的维护奖励。凭证夹具明确不执行局势变更、白绮刷新和物种状态克隆；这些字段在 JSON 中列为排除的引擎域，不能把离线队列通过写成存档实机重载通过。

当前候选版本采用实施记录已声明的原生加算回退：`planet_jobs_produces_mult=0.05`，按 U+R 动态缩放，统计刷新先移除再添加单一实例，岗位维护不随之增加。检查器拒绝额外维护/劳动力修正，也检查无人口或起源丢失时撤销旧增益。数学数据层的 M 变量通过不代表经济独立乘算通过；JSON 明确写 `independent_multiplication=NOT IMPLEMENTED`、引擎经济效果 `NOT RUN`。

本地化静态检查覆盖十语言目录、BOM、文件头、重复/空值/缺失键、自有引用完整性、非中文占位、指定完整名称。简体中文名称必须完整保留「基于低内聚高耦合的旧时代集成服务架构」，18 个汉字、UTF-8 54 字节。其长度只有数据完整性结论，实际界面字段长度、换行、遮挡和可读性仍为 NOT RUN。

命令示例：

```powershell
python shishan_code_origin/tools/validate_feedback_redesign.py --mod shishan_code_origin/mod --game 'C:\Program Files (x86)\Steam\steamapps\common\Stellaris' --report <报告路径>
python -m unittest discover -s tests -p test_shishan_feedback_redesign.py -v
```

此工具补充合同校验，不替代 `C:\workspace\open_kaishek\tools\accept_stellaris_mod.py` 的首道包级验收。JSON 必须分别列出静态合同检查与未执行事项：游戏运行、UI/OCR、存档重载、自然局、实际经济独立乘算、性能与其他语言运行时。负例需要证明错误系数、错误取整、重复候选、错误冷却、迁移双计、名称截断和缺失本地化不会被误判为通过。现有 `tools/shishan_code/audit_reward_contract.py` 保留原版机械候选身份、正向标签与机械适用范围检查，奖励行为改为调用新 AST 检查器，不再要求旧随机四类迭代形态。

## 当前程序性验证证据

2026-10-04 执行以下命令，退出码均为 0：

```powershell
python -m unittest discover -s tests -p test_shishan_feedback_redesign.py -v
python shishan_code_origin/tools/validate_feedback_redesign.py --game 'C:\Program Files (x86)\Steam\steamapps\common\Stellaris'
python tools/shishan_code/audit_reward_contract.py --game 'C:\Program Files (x86)\Steam\steamapps\common\Stellaris'
python -m py_compile shishan_code_origin/tools/validate_feedback_redesign.py tests/test_shishan_feedback_redesign.py tools/shishan_code/audit_reward_contract.py
```

32 项单元/产物回归全部通过。包含实际脚本数值、架构统计/迁移、奖励状态、凭证恢复、本地化及故意破坏产物的负例：初速错误、5% 错误、重复迁移第一层、共享原物种直接修改、岗位维护跟随增加、重复候选、错误重抽冷却、丢失窗口锁、拒绝确认/重抽后漏清锁、丢失成功凭证恢复、名称截断、缺键、无 BOM、循环/缺失引用、中文占位和未知操作。负例通过表示这些错误被检查器拒绝，未向正式候选写入故障。最后追加的两个拒绝路径分别验证资格失效和冷却失效，均可保留原业务状态后由实际首都 wrapper 重开；确认路径在重开窗口时修复失效候选，重抽路径保留有效候选。

拒绝选项解锁修复前的开发快照为 `mod_tree_sha256=4ea8e8f98b4b9b35e918680ff1ab579e68ca4a1e27bc60a446fa9d9b201c8b6c`，90 个文件，属于历史检查结果；最终快照以主实施记录的 final JSON 为准，不能把这个旧哈希当作修复后的最终产物。五个合同检查覆盖静态/离线结果：22 个速度输入、12 个费用输入、22 类阶段资源；全键加权 U=9 和 20% 新增键的 U=10.2；43 原始键加 23 历史重复为 T=66；R=10000 后再加一层没有截断；候选数量 0–6 各 8 个种子共 56 组；确认冷却 3→2→1→0；窗口队列计数 1→2→3→4，加两组拒绝操作后的解锁/重开；13 组跨状态/待选/同时成功/清理先完成/异常陈旧凭证恢复。窗口修复后仅重跑上述 32 项测试，未另写 final JSON，以免覆盖主任务的最终证据。

十语言 50 个本地化文件、每语言 268 键、2070 处引用及 154 个脚本引用键静态校验通过，已读取本机原版本地化校验外部引用；包含最终追加的起源说明中的机制名称/说明引用，完整名称保留 18 汉字/54 字节。旧奖励 audit 检查 20 个原版机械正向候选及新奖励状态机通过。非中文结果仅为静态校验通过，运行时不在范围内。

这些命令未启动游戏、未调用桌面输入/截屏、未运行 Steam 发布。UI 长名称布局、实际物种克隆/隐性特质迭代/谱系识别、保存重载、实际岗位经济效果、自然局和性能全部保持 NOT RUN；独立乘算区间尚未实现。最终包级验收和最终快照证据由主实施记录汇总。

## 2026-10-15 实机发现的解释器假阳性与修复设计

本轮第一次实际加载的错误原件位于 `_runtime/shishan_code/20261015-runtime/rc1-loading-failure/error.log`。引擎报告了原版 `pop_amount` 展开到 `count_owned_pop_amount` 时的作用域错误，以及 `shishan_code_architecture_per_trait` 为无效 script value。先前离线解释器错误地把 `pop_amount` 当成任何作用域都有的人口字段，也接受普通命名的裸数值 script value；因此本文件早前的离线 PASS 不能证明这两个引擎合同成立。这是检查器能力缺口，不能用旧结果抵消实机失败。

修复先于再次 Mod 验收设计如下：人口组只接受原生 `pop_group_size` 比较和 `trigger:pop_group_size` 数值导出，`prev.trigger:pop_group_size` 必须先解析 prev，再检查目标确为 `pop_group`。在国家、物种、trait 等其他作用域使用这一原生字段应失败；在 pop_group 使用 `pop_amount` 或其导出也应失败。实际原版脚本和当前生成文档已由主任务核对，不能继续用离线同名别名掩盖作用域差异。

普通命名 script value 只接受 `{ ... }` 块定义，例如 `per_trait={base=0.05}`；`per_trait=0.05` 必须被拒绝。`@` 编译期常量与普通可执行命名 script value 是不同对象，此检查器未明确支持的常量解析也不得默认为可执行值。

新增独立故障/修复样例须先证明旧形式被拒绝，再证明人口组的 `pop_group_size` 正确比较、导出及 prev 导出可执行，以及 `{base=0.05}` 可计算；同时加入错误目标作用域的负例。现有产物结构合同同步要求原生人口组字段。Mod 与生成器由主任务统一修改，本子任务只改检查器和测试；Kaishek 修复与首道包级验收恢复前，仅运行解释器开发回归，不宣告 Mod 再验收通过。

这两项修复已经落地。除了被执行的命名值，加载 script_values 定义时也拒绝未引用的普通命名裸数值；`@` 常量可以保留为定义，但检查器不会把它作为普通 script value 执行。新增 `NativeScopeRegressionTests` 六项开发回归通过，命令为 `python -B -m unittest discover -s tests -p test_shishan_feedback_redesign.py -k NativeScopeRegressionTests -v`，退出码 0。证据为 `_runtime/shishan_code/20261015-runtime/interpreter-scope-development-tests-20261015.json`，只属于解释器开发自测。

另已读取主任务冻结的原始实机失败包 `C:/Users/Administrator/AppData/Local/xenoamess_stellaries_dev/runs/20261015T064353Z/mod/shishan-feedback-local`，对该未修改源使用修正后的解释器验证：裸 `shishan_code_architecture_per_trait` 定义、实际奖励资格 01 的人口组 `pop_amount`、实际架构刷新的人口组 `pop_amount` 三处均被明确拒绝。原始三个源文件 SHA-256、错误诊断与当时五项独立故障/修复自测保存在 `_runtime/shishan_code/20261015-runtime/interpreter-baseline-rejections-20261015.json`。冻结包来自主任务保存的实际 PID 5812 运行包，不是由本子任务伪造的 gamestate 或 Mod。

主任务随后把四个旧计数迁移逻辑内联并移除旧 migrate_counter helper，以降低引擎初始化解析链；检查器的迁移数学合同并不要求 helper 存在，原有 `legacy_extra -1` 故障注入标记仍出现在四个内联分支，因此不需要把预期改成生产代码推导的值。实际原生五遍初始化限制由主任务的调用图分析和重启后的实机日志验证，Kaishek 本次有限规则不覆盖此项，本解释器不把自己的递归执行能力当作引擎能加载任意深度 effect 的证明。此阶段没有重新执行候选 Mod 全量验收或宣告其通过，等待主任务恢复工具首道门槛。

## 2026-10-15 rc.2 生产包程序性复核

本节随后补充的实机否定证据：rc.2 原生待选存档 `fb452_pending1.sav` 的 `tier=1`、槽位为 `5/33/33`，实际同时出现跨层与重复候选，因此这里的离线 PASS 不能作为奖励实机通过结论。下方新增逻辑节点修复记录以原生证据为准。

主任务确认 `open_kaishek` 提交 `47c3c4e` 的 rc.2 生产包首道检查通过，证据为 `_runtime/shishan_code/20261015-runtime/package-rc2-452.json`，25/25 个脚本、13 个 DDS、每语言 268 键。该门槛通过后，本子任务并发运行纯生产包的完整回归、validator 和原版数据 audit；没有启动游戏，也没有对未通过门槛的实机夹具发出运行指令。

以下结果均退出码 0，完整 stdout/错误输出与命令分别保存在本轮新 JSON，未覆盖 rc.1 或历史证据：

- `python -B -m unittest discover -s tests -p 'test_shishan*.py' -v`：50 项通过，包含原 32 项、这次补充的 6 项原生作用域/命名值负例，以及 12 项原生存档审计。报告 `rc2-unit-agent-452.json`。
- `python -B shishan_code_origin/tools/validate_feedback_redesign.py --game <当前4.5.2安装目录> --report .../rc2-programmatic-agent-452.json`：五项静态/离线合同通过，Mod 树哈希 `f393c57d2120113634e25cfc9e1e14283183c9a4f6bdf84b53c999eac2a7d778`。
- `python -B tools/shishan_code/audit_reward_contract.py --game <当前4.5.2安装目录>`：20 个原版机械正向候选及 56 组离线状态合同通过。报告 `rc2-reward-audit-agent-452.json`。
- `python -B tools/shishan_code/audit_compat_traits.py --game <当前4.5.2安装目录>`：19 个映射的原版数值、适用机械类别与各原版语言名称/说明引用静态校验通过。报告 `rc2-compat-audit-agent-452.json`。

上述报告目录均为 `_runtime/shishan_code/20261015-runtime/`。validator 实际读取本机 4.5.2 原版本地化，十语言 50 文件、每语言 268 键、2070 引用、154 个脚本本地化键静态校验通过；完整名称仍为 18 汉字/54 字节。迁移已改内联，但独立 23 层预期和故障双计负例继续通过。

本节仅证明程序/静态结果通过。正确原生作用域在 4.5.2 中的实际执行、effect 初始化链、物种克隆、窗口与保存重载，以及总体用户体验仍待主任务实机验证；新实机夹具当时尚因保存事件目标的类型推断不足而等待工具完善，不得从生产包程序检查推定该夹具已经通过。独立乘算区间仍未实现，当前经济通道仍是明确标记的原生加算回退。

## 2026-10-15 原生 NOT 真值与候选权重修复设计

主任务在 4.5.2 实机控制台直接验证：`NOT={always=yes always=no}` 返回 FALSE，而 `NOT={AND={always=yes always=no}}` 返回 TRUE。原图为运行 `20261015T071829Z` 下的 `native-not-multiple-result.jpg`、`native-not-and-result.jpg`，输入与原始结果另有 `console.json`。这证明多个直接子触发器的 `NOT` 应取各子项的 NOR 结果，不能按此前解释器的 `not(all(children))` 实现。这个错误让旧 `random_list` 的非法候选屏蔽在离线模型中有效、实机却失效。

修复只针对已经确证的节点：`NOT` 改为 `not(any(children))`，已有 `NOR` 保持相同逻辑；`AND`、`OR` 和默认子项合取保持原实现，不借此改写未经实机确认的其他节点或添加未支持节点。生产生成器由架构子任务将整体可用条件明确包入 `NOT={AND={...}}`，本子任务不修改生成器或 Mod。

新增回归包括 `NOT` 的空/单/双项真值表、显式 AND 包裹的区别，以及现有 AND/OR/NOR/default 的固定输入对照。候选屏蔽必须使用确定性权重断言：读取冻结 rc.2 的真实第一个 draw 分支，对它不满足层或已经在某槽位的场景计算实际权重，旧守卫仍为 1 时必须报错；修正后相同候选权重必须为 0。不能靠多次随机抽样“恰好没抽出错项”宣告修复。冻结的原生 `5/33/33` 存档及跨档报告继续保留为失败证据，不覆盖为新的通过结果。

解释器现已采用上述原生 `NOT` 语义，并把权重计算抽为可直接检查的 `random_weights`。奖励合同在随机抽样前，先对三个槽位、普通/优先新候选两分支执行共 27 组确定性权重场景：合法候选为 1，跨层、已选、无资格和优先分支的旧组成员为 0。三项 `NativeLogicRegressionTests` 开发回归通过。

使用冻结实际 rc.2 运行包 `C:/Users/Administrator/AppData/Local/xenoamess_stellaries_dev/runs/20261015T071829Z/mod/shishan-feedback-local` 的真实生成产物执行该检查，立即在第一个非法输入被拒绝：`slot 1, else_if, wrong tier: expected 0, got 1`。这是确定性的权重错误，不依赖随机种子或抽样次数。源奖励文件 SHA-256、原始诊断、三个真值表/权重开发回归命令与输出保存于 `_runtime/shishan_code/20261015-runtime/interpreter-not-frozen-rc2-rejection.json`。此时尚未对后续生成器修复重新宣告生产包通过，仍等待其完成和首道门槛。

## 2026-10-15 rc.3 程序复核与原生旧档观察

修正生成器的 234 处 NOT 整体取反、公开提示与隐藏执行后，主任务确认 rc.3 生产包 G1 通过。本子任务并发复核：当时完整 61 项回归通过，含 27 组确定性候选权重；validator 五合同通过，reward audit 与 19 项原版映射 audit 均通过。报告为本轮 `rc3-unit-agent-452.json`、`rc3-programmatic-agent-452.json`、`rc3-reward-audit-agent-452.json`、`rc3-compat-audit-agent-452.json`，当时树哈希 `ed45042269f2ec2adb356ad3a68a480af047fb488cbfabaf6369c548e191092c`。这是补兼容本地化键前的开发快照，后续最终快照以主任务新 G1 和报告为准。

旧冻结 rc.2 运行另留下三份真正原生档：`fb452_legacy23.sav`、`fb452_legacy23month.sav`、`fb452_legacy24.sav`。独立解析显示旧四计数 7/5/11/4 始终保留，R 为 23→23→24，n 为 0→0→1，最后完成项目为 MAINTAIN；最终观察 CD=2、U43/T67/bonus3.35、唯一修正实例 multiplier67。CD=2 的完成前输入由主任务受控设置，三份 native 文件未保存该中间输入，报告明确区分这一来源。

月档日期 2227.04.12 的实际人口 P5567、W239381，而刷新变量仍为 P5561、W239123，原生审计据即时值合同记录两项 MISMATCH；没有因为 U 恒为 43 而把 P/W 也记为通过。实际完成维护后保存的 legacy24 已刷新为 P5567/W239381、R24，审计通过。三档 legacy 历史/CD/实例的限定对照保存在 `fb452_legacy24.independent-cross-save.json`，并明确保留月档缓存失败和 rc.2 运行身份，不替代 rc.3 实机验收。

同次实机 error.log 发现自动生成的 modifier 本地化键 `mod_leaders_unity_upkeep_mult` 缺失。公开文案的显式引用完整，并不能覆盖引擎自动拼接的该键。先记录检查器补充设计：当实际 Mod 的 trait self modifier 使用 `leaders_unity_upkeep_mult` 时，本地化检查须额外要求兼容键存在于十语言，增加“十语同时缺自动键也必须失败”的独立负例，不能靠各语言缺失集合恰好相同就判完整。生产本地化补丁由架构子任务负责，本子任务只改检查器和测试；等补键与新 G1 完成后再复查本地化及受影响全回归。

补键后主任务确认最终生产/夹具 G1 分别为 25/25、26/26 个脚本，每语言 269 键，报告 `package-rc3-final-452.json` 和 `fixture-rc3-final-452.json`。随后本子任务只重跑受影响的完整回归与最终 validator：62 项通过；validator 五合同通过，27 项确定性权重全部符合；十语 50 文件、269 键、2080 引用、154 个显式脚本本地化键及引擎自动键 `mod_leaders_unity_upkeep_mult` 静态校验通过。完整名称仍为 18 汉字/54 字节。最终程序性快照哈希为 `f5aa60abc66f67f869b071b4fa5e1d08b50b6e65181339fe2e016684ceda6f1e`，证据 `rc3-final-unit-agent-452.json`、`rc3-final-programmatic-agent-452.json`。此前每个故障或开发快照报告均予保留，不以此结果覆盖；实机对照仍由主任务继续执行。

## 2026-10-15 原版机械候选资格的独立静态审计设计

最终 rc.3 初始待选原生存档的 19/6/18 均在当前两个实际模板上适格；独立读取 4.5.2 原版定义时，同时发现手工奖励池把三个研究核心的 opposites 写为空。原版物理学核心与社会学/工程学核心、`trait_structural_awareness` 互斥，社会学核心亦有对称互斥；因此初始合法不代表选中一个后可以继续提供另一个。不能只核查 archetype/positive 标签或用生成器自身的空列表生成预期。

先补强只读 `tools/shishan_code/audit_reward_contract.py`：直接从安装的 `05_species_traits_robotic.txt` 解析所选 20 个原版定义，读取 canonical opposites、forbidden_ethics、DLC 与关键添加资格；对照生成器声明以及真实生成的 eligibility/claim 模板过滤和国家资格。机器原版的 species_potential_add 是常规改造 UI 的额外入口条件，奖励授予受已批准设计的绕过点数/选择数限制约束，不能未经分析直接把整个原版改造 UI 条件照搬或忽略；报告应明确实际核对的字段与例外理由。

新增确定性负例须证明：原版存在 core 互斥，而生产声明或生成 guard 漏掉该 key 时立即失败；关键禁止格式塔等条件遗漏也必须失败。以小型独立 canonical P 定义和当前实际原版数据为预期，不从生产 opposite 常量反向造答案。生成器由架构子任务修改，本子任务仅修改 audit、自己的测试和文档；全部为静态/离线检查，不替代后续核心互斥的实机行为验收。

架构子任务将保留四项 tuple 接口，补齐全体原版 traits 文件中直接与反向的 opposites 并新增四个 Machine Age DLC gate，同时在实际 species 条件上限定 ROBOT/MACHINE。原版存在同一 trait 多个 `opposites` 字段，审计器必须合并全部字段；不能先转成 dict 再覆盖较早的互斥项。解释器相应增加明确的 species archetype 字段，`is_archetype` 仅 species 作用域有效；DLC 由离线夹具明确给定 host DLC 集合，不能默认假设拥有任意 DLC。保留 14/16 已批准的个体/经济保守过滤，并在报告中列明相对原版的额外限制。

`audit_reward_contract.py` 已完成上述加强，提供 `--game`、可选 `--mod` 和 `--report` JSON 接口。读取 44 个原版文件，保留重复字段并合并反向关系；检查原版 DLC、禁止格式塔条件、机械类别和机器所有者的 `species_potential_add` OR 分支。未建模的资格字段或分支明确失败。14/16 的额外格式塔过滤单列为保守策略。真实生成的 eligibility、claim 国家守卫、claim 模板守卫、coverage 人口组守卫直接执行，预期来自原版数据，无资格 override。

工具开发回归命令为 `python -B -m unittest discover -s tests -p test_shishan_robotic_canonical.py -v`，11 项全部通过、无跳过；涉及 149 个确定性场景、596 个实际守卫断言。测试涵盖重复与反向互斥、声明漏 core/DLC/禁止伦理、未知条件失败、DLC 默认为空、错误 archetype 作用域，以及分别删除真实 eligibility/claim/coverage 中 core 互斥的负例。冻结实机 rc.3 的物理学核心 guard 在已经存在社会学核心时返回 True，按原版独立预期 False 被确定拒绝；不依赖随机抽样。证据为 `_runtime/shishan_code/20261015-runtime/canonical-qualification-development-tests.json`。这是工具开发单测；在新生产包 G1 与完整回归完成前，不据此宣告新 Mod 包验收。

## 2026-10-15 原生克隆权利、使节与空目标的程序验证补强设计

新实机观察显示普通领袖迁移正常，但使节保留旧主模板；旧子模板拥有明确权利，新子模板缺失覆盖后回落到国家默认清洗/低生活标准。另在悬停提示时，空国家事件目标进入 `owner_main_species` 产生引擎错误。这些是实际运行发现的合同缺口，先前抽象 clone hook 默认继承本国属性不能作为原生权利或使节处理的证据。

待架构子任务确认原生接口并完成生产改动后，结构合同应要求三个 modify_species helper 显式继承亲本权利、独立人口与普通领袖/使节的旧模板到新模板迁移，以及事件目标存在守卫；负例分别删除字段、迁移迭代或存在守卫必须失败。离线状态模型必须由实际字段控制继承与迁移，禁止无条件复制掩盖漏写，并明确实际国家默认权利、外国共享模板和空事件目标的输入。此项仅覆盖程序合同；原生新模板权利表、使节身份、外国共享模板隔离和悬停错误仍以新原生存档与引擎日志验收，不把 hook 通过写成实机通过。

架构子任务确认接口为 `modify_species.inherit_parent_rights=yes`；三个 helper 在进入国家事件目标前用 `exists=event_target:shishan_code_reward_country` 守卫，拒绝路径写日志 `SHISHAN_CODE_TEMPLATE_COUNTRY_TARGET_MISSING`；country 下新增 `every_envoy`，exact old 匹配后 `change_species=new`；普通领袖有原薇薇特旗标时恢复 `change_leader_portrait=shishan_code_vivhite`。原版 `00_scripted_effects.txt` 及生成 effects 文档有对应原生接口。离线解释器只实现此窄域 fixture：国家权利表按模板对象身份索引，缺少继承字段按默认权利建新表，迭代确实按本国所有权过滤，领袖/使节迁移修改物种引用而保留身份、经验、旗标；不执行 engine 原生权利逻辑。测试应同时比较字段删除后的实际 fixture 差异与合同拒绝，避免只检字段字符串。

上述程序验证已经落地。`check_domestic_templates` 要求三条继承字段、三条存在守卫/诊断、使节迭代与薇薇特肖像恢复；`check_domestic_template_model` 执行三 helper 的主模板、子模板、空目标共 9 个场景。fixture 输入含本国 5040/511、零人口模板、共享同一旧物种对象的外国 200 人口、5 名主模板普通领袖、2 名本国使节，以及外国领袖/使节；本国默认权利为清洗/低生活标准，旧子模板为完整公民/正常标准。实际 `inherit_parent_rights` 控制新权利表，字段省略确实回退到默认并失败；使节迭代删除确实保留旧物种并失败；事件目标为空且守卫被删时明确解析失败。特殊肖像恢复也有实际 fixture 差异断言；其中“change_species 后默认肖像”仅为使漏恢复可观察的保守 fixture 假设，不是引擎行为结论。

`python -B -m unittest discover -s tests -p test_shishan_clone_contract.py -v` 开发回归 10 项通过、无跳过；包括真实三个 helper 各自漏继承字段的负例。证据 `_runtime/shishan_code/20261015-runtime/clone-rights-envoy-development-tests.json`。没有用这些 fixture 写入或伪造原生存档，也没有操作游戏。新包完整程序验收仍等待主任务确认 G1；原生 rights/envoy/UI 结果等待下一运行的真实保存证据。

## 2026-10-15 rc.4 冻结源程序性复核

主任务确认冻结 `fixture-rc4` 后，生产 G1 25/25、实机夹具 G1 26/26、269 键均通过，分别保存 `package-rc4-452.json` 与 `fixture-rc4-452.json`。随后本子任务并行执行以下纯程序复核，四项命令均退出 0，没有修改 Mod 源文件或操作游戏：

- `python -B -m unittest discover -s tests -p test_shishan*.py -v`：83 项全部通过、无跳过，包含原生缺陷的确定性负例、克隆字段控制模型、原生存档只读解析；`rc4-unit-agent-452.json`。
- `validate_feedback_redesign.py --game <当前4.5.2安装目录> --report .../rc4-programmatic-agent-452.json`：五合同通过，冻结 90 文件树 SHA-256 为 `98fe2c5ec6a3641d687083a9fa9858d1375af88ce04527a74b18d36098d0e366`；56 候选状态用例、27 确定性权重场景、13 凭证恢复场景及 9 克隆 fixture 场景通过。
- `audit_reward_contract.py --game <当前4.5.2安装目录> --report .../rc4-reward-audit-agent-452.json`：44 原版文件、20 机械正向候选的完整互斥/DLC/禁止伦理/类别与已审查机器所有者分支一致，149 场景 596 守卫断言通过，没有资格 override。
- `audit_compat_traits.py --game <当前4.5.2安装目录>`：19 个兼容映射的原版效果、机械类别及语言引用通过；`rc4-compat-audit-agent-452.json`。

报告均位于 `_runtime/shishan_code/20261015-runtime/`，保留先前失败和开发快照。最终本地化为十语 50 文件、每语 269 键、2080 引用、154 显式脚本键及 1 引擎自动 modifier 键，静态校验通过；非简体中文运行时不在范围内。以上结果仅为工具和程序合同通过，真实克隆权利/使节、空事件目标错误、奖励 UI 和实际冷却序列由主任务新 rc.4 原生运行另外验收。经济机制仍为明确标识的原生加算回退，独立乘算没有实现。

原生 R4 领取后又发现存档 reader 将 rights primary 误作国家当前主模板来源；修复详见[原生存档审计](runtime-save-audit-2026-10-15.md)。`country.founder_species_ref` 已原生从旧模板变为50，rights primary 保留旧值，二者在新报告中独立呈现；新增六项明确验证不回退到旧 rights primary。修正 reader 后，主任务要求的完整交叉回归已执行一次：89 项全部通过、无跳过，16.198 秒，证据 `rc4-final-unit-agent-452.json`；83 项旧快照保留，生产 Mod 源冻结未改。此项仍是程序验证，原生 getter/权利/UI/CD 由主任务另记。

## 2026-10-15 rc.5 物种缓存滞后回归设计

真实 `fb454_clean_pending` 保存的国内人口在55/56，`owned_species_refs` 仍53/54；冻结 rc.4 在这种明确输入上将实际可用的11/9/12全部判失效，清票并发R。独立实际AST复现已保存 `rc4-clean-pending-cache-ast-reproduction.json`：只替换fixture枚举列表，旧缓存输入得到R1/tier0/slots0；当前人口模板输入则R0/tier1/11,9,12保留。主任务随后原生 iterator 探针确证 `any_owned_species` 看不到 refactored、`any_owned_pop_group.species` 能看到。此前奖励 hook 即时更新 `species_templates` 是有界抽象假设，未覆盖这次原生同日状态，旧89项通过不能作为该情形成功证明。

生产修复由架构子任务负责，本子任务只改检查器、audit及测试：资格从实际人口组进入species；claim和状态迁移都在country的每个人口组上执行，外层与内层均重检当前population/lineage/species条件，避免首个模板被批量迁移后又因另一个旧人口组重复克隆。解释器窄域真实clone不再自动更新缓存列表；新增显式fixture模式让pop迭代在效果前预选目标，效果时动态解析group.species，用于保守验证内层重检有实际防重作用。这是测试输入假设，不把引擎具体预选实现当作已证实事实。已有普通迭代语义与旧冻结反例保留。

另新增隐藏1004预检事件：持有唯一window锁并refresh，票仍有效才发1000；1000仅计算coverage，不再次处理会耗尽票的refresh。窗口合同应区分预检队列与可见事件，验证真正耗尽只发一次R并关闭锁、不绘制空旧窗口、重放不再次消费。新测试同时执行原生clean_pending读取来的缓存/实际组输入、同模板多组、空/外国组与内层重检删除负例；149组原版资格场景继续从canonical资料生成预期。完成新G1后才生成rc.5完整程序报告，不改Mod/生成器/版本。

rc.5 程序实现与验收已完成。窄域真实clone执行不再写入 `species_templates` 缓存；新增显式 `snapshot_pop_group_limits` fixture选项，预先选定人口组后，内层guard仍读取当前group的species。新 `test_shishan_species_cache.py` 10项覆盖：从真正 `fb454_clean_pending` 读取的53/54缓存与55/56实际组；冻结真实rc.4在同输入上仍错误R1；新refresh保留11/9/12和R0/CD3；不依赖资格override的实际claim每模板一次、部分覆盖只克隆一个模板；refactor/relapse在stale缓存下双向迁移；删除claim/state内层重检后确实产生额外clone并被合同拒绝；隐藏预检保票及真耗尽不绘制1000。原始输入解析只缓存不可变数据，各次执行重建独立scope，未写入原生档。

主任务确认 `package-rc5-452.json` 25/25 与 `fixture-rc5-452.json` 26/26 的 G1 均通过后，并行完成四项必要静态复核，退出码全部0：完整99项测试无跳过、18.612秒（`rc5-final-unit-agent-452.json`）；validator五合同通过（`rc5-programmatic-agent-452.json`），90文件树哈希 `21f327ecb3082d23eb7434e7a02e9376f890726d655b8bc72eeaee172dba42ec`；44个原版文件/20机械候选、149场景共745条实际守卫断言通过（`rc5-reward-audit-agent-452.json`，新增外层人口guard独立断言）；19兼容映射及原版引用通过（`rc5-compat-audit-agent-452.json`）。报告目录仍为 `_runtime/shishan_code/20261015-runtime/`，旧rc.4的89项报告和native失败现场均保留。

十语50文件269键2080引用继续静态通过；全部非简体中文运行时仍不在范围内。程序报告不替代rc.5原生载入、跨状态重开、最终第四次确认及真实UI/权利验收；原生输出机制仍是加算回退，独立乘算未实现。本子任务没有操作GUI或修改任何冻结生产Mod文件。

## 2026-10-15 rc.6 白绮免费维护的原生规则回归设计

主任务原生rc.5领袖界面已明确显示白绮维护1.0，证据 `runs/20261015T084453Z/rc5-white-before-leaders.jpg`；这是免费目标FAIL，不能再写UNKNOWN，也不能把self modifier=-1当成实际0。生产设计见 `feedback-redesign-vivhite-free-upkeep-fix-2026-10-15.md`。原版 `common/game_rules/00_rules.txt:418` 的 `should_pay_for_leader_upkeep` 明确排除 `has_leader_flag=should_not_have_upkeep`，其余普通领袖仍需付维护。

本子任务仅增加工具模型与测试：读取当前安装的完整原生规则AST，不从生产代码生成预期；执行新增refresh中的本国白绮旗标过滤，验证新本人得到原生豁免，而普通领袖、外国同旗标领袖和不在owned列表的备份均不获授。初建.4、重启.41、旧档月刷新.60各入口必须实际调用同一refresh；备份.40 effect必须显式先移除豁免，不能以克隆继承掩盖重启刷新缺失。限定模型只执行旗标/当前刷新；不把它扩展成整个领袖死亡和非零XP恢复引擎。

新增负例删除豁免授予、删除白绮过滤、删除备份移除与重启refresh均应失败；额外确认执行前后本人级别/经验、已选职业特质、肖像与身份变量不变。解释器仅补原生规则用到的owner存在、country is_gestalt和leader is_councilor作用域；未知条件继续失败。rc.6新G1通过后才重跑必要完整程序报告。实际免费UI、非零自然成长、实际死亡/付费重启和还原由主任务另行原生验收。

上述检查已落实为 `check_vivhite_upkeep`，validator新增第六项 `vivhite_native_upkeep_contract`。读取当前安装原版完整 `should_pay_for_leader_upkeep` AST，原始文件 SHA-256 为 `1bcd16731633bc2f2411a868b4a626572f1722068e53875193e12a4c41920566`：本人有flag时rule不收费、移除flag仍收费、普通领袖收费。冻结真实rc.5同样执行refresh后没有原生豁免，rule仍收费，继续作为失败负例保留；这不覆写主任务原生UI维护1.0的FAIL证据。8项新测试还实际执行旧档事件.60、检查grant过滤及备份/reboot入口，fixture非零XP=748只用于不改成长断言，不冒充主任务正在使用的真实20XP种子或完整死亡恢复。

主任务确认 rc.6 正式G1 25/25、实机夹具G1 26/26、13DDS与269键通过后，最终并行复核四命令均退出0：`rc6-final-unit-agent-452.json` 为107项全部通过、无跳过、19.862秒；`rc6-programmatic-agent-452.json` 为六合同通过，90文件树哈希 `566030887c51815361b4a9d3d102258c821f7eaf89b1d219241b9a6b0f597b1d`；`rc6-reward-audit-agent-452.json` 为149场景745实际资格守卫断言通过；`rc6-compat-audit-agent-452.json` 为19兼容映射及原版引用通过。十语50文件、每语269键、2080引用静态校验通过，非简体中文仍只做静态、不进入实机矩阵。

这些报告都在 `_runtime/shishan_code/20261015-runtime/`，未覆盖rc.5及之前的失败/通过快照。程序实现收口后没有修改生产源码、没有操作GUI；实际免费、自然成长保留、支付500能量/200合金后的重启由主任务rc.6实机另行验证，不能将规则模型PASS直接表述为原生领袖维护UI通过。
