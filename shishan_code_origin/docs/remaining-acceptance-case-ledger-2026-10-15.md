# 原74用例的剩余验收追踪

日期：2026-10-15。用途：在先发布当前版、再继续本地验收的授权范围内，逐项保留原用例、已取得的证据和最小剩余操作。本次只读梳理，不启动游戏、不操作GUI、不修改生产、共享计划或历史结果。正式0.2.1已发布、远端90文件核验通过且标签已推送；功能脚本沿用rc.6，真实发布回执见[本轮发布计划](release-0.2.1-and-remaining-acceptance-2026-10-15.md)，本表不代替发布回执。

依据：[74用例原表](feedback-redesign-test-cases-2026-10-04.md)、[测试方案](feedback-redesign-test-plan-2026-10-04.md)、[10-15实机记录](runtime-feedback-validation-2026-10-15.md)和[原始证据索引](evidence/feedback-redesign/runtime-2026-10-15/README.md)。原表开头的“全部NOT RUN”是10-04历史快照，不能覆盖10-15的新证据；反过来也不能用少数新样本把整项矩阵全部改为PASS。

## 范围和判定口径

- NAT-01至04及其22局、长期发展/自然V救援路线均为 **EXCLUDED**。不恢复这些路线，也不把排除登记为通过。PR等功能用例中的项目回调、普通科研进度与状态恢复仍需分项判断；受控完成不冒充自然研究完成。
- 用户允许无可靠、兼容的独立乘算通道时采用加算回退。[通道调查](trait-multiplication-investigation-2026-10-15.md)已收口：在全国岗位、维护/就业不变、兼容成本等本轮约束下，无合适且充分证实的最终独乘通道，本版采用用户授权加算。保留原乘算目标历史，不声称引擎数学普遍不可能；TS-05/06等改为新合同待实测，不再以“调查未完成”阻塞，也不自动PASS。
- **PF-01独立保留**：其100游戏月性能采样不是NAT长期体验路线，不因排除NAT而删除。
- `PASS`仅表示该行所需证据类型及当前适用分支已完成；`NOT RUN`表示整项尚有未执行分支，即使已有明确PASS子样本；`BLOCKED`表示先有合同/异常处理策略或必要观测能力待解决；`EXCLUDED`只用于本轮明确排除项。历史FAIL/UNKNOWN仍留在原报告，不覆盖为PASS。
- 原表要求除明确分工外，核心功能覆盖个体机械和机器智能两类。两政体“各有部分实机”不等于全部用例已经双政体完成。九种非中文语言只有静态校验，运行时不在范围内。
- 正式0.2.1新的G1和包身份核对已通过（E-REL）。rc.6的107项程序回归、本轮149资格场景/745守卫断言可说明相同功能源码的程序合同，不能冒充新的原生分支、GUI、保存重载、经济来源或性能采样。

## 可直接复用的真实输入和证据

| 简称 | 已冻结输入/证据及适用边界 |
| --- | --- |
| E-REL | [正式0.2.1程序检查](release-0.2.1-programmatic-checks-2026-10-15.md)、[正式G1](../evidence/v0.2.1/acceptance/package-open-kaishek.json)、[90文件身份](../evidence/v0.2.1/acceptance/release-identity.json)、[远端逐字节核验](../evidence/v0.2.1/workshop-verification.json)。正式树835267fa…6ae94；相对rc.6生产投影只改descriptor版本和十语各一处“预发布→本版本”，其余79文件相同；明确保留初次raw91清单差异FAIL。 |
| E-FORMAL | [正式无夹具同日重载独立审计](evidence/feedback-redesign/remaining-2026-10-15/formal021-no-fixture-run103709/independent-formal021-claim-reload-audit.json)：run103709Z真实新档SHA d6f89ed7…9f9b9f8，对源rc.6自然领取档SHA9ddcb31c…4bbc4d。当前Mod核心状态保持PASS；严格raw全不变9PASS/3FAIL原样保留，权利去重、外国1人口就业组转移、预算缓存变化单列；没有外国probe哨兵，不能据此补哨兵用例PASS。同run[高R实际重载独立审计](evidence/feedback-redesign/remaining-2026-10-15/formal021-no-fixture-run103709/independent-formal021-high-r-reload-audit.json)补机器智能R25/n2/CD2及完整领袖保持，原始区段差异保留。新增8条game_text诊断原样保留，来源及无Mod对照见下文，不冒称零错误。 |
| E-CONTROL | [无Mod实际对照JSON](evidence/feedback-redesign/remaining-2026-10-15/localization-settings-control-comparison.json)及[原图/原始日志/保存档归档索引](evidence/feedback-redesign/remaining-2026-10-15/formal021-settings-control-README.md)：run110858Z实际enabled_mods=[]、同4.5.2 EXE/简中、no-debug/borderless1280×720、菜单9776/默认1.0x，主菜单设置复现同8条；只去首个时间前缀后按序逐字相同。两run正常停机完整logs各19文件及原始29行error.log全保留。 |
| E-MIN | [1280×720/1.0两政体正文独立核对](evidence/feedback-redesign/remaining-2026-10-15/formal021-min1280-run111512/independent-formal1280x1-display-check.json)：run111512Z正式90文件/no-debug/无夹具，实际首都决议到正文，原图直接目视与OCR/SHA一致；完整18字名称、个体U7/R0/B0.35及机器U43/R25/B3.4、关闭按钮均可读，原生紧凑标题仍省略。仅该配置这两子样本PASS，日志21descriptor之外无新增；无新SAV，不冒充全状态或其它分辨率通过。 |
| E-ECN | [原自然F01完整归档](evidence/feedback-redesign/remaining-2026-10-15/natural-economy-run112046/README.md)保留run112046Z三档窗口INVALID/严格P-W FAIL；[run113522Z完整归档](evidence/feedback-redesign/remaining-2026-10-15/controlled-economy-run113522/README.md)另保留首次稳定度100但仍增长的21档INVALID/严格P-W共32FAIL，再以原生UI停止组装、稳定两月的独立共同源取得新21档。[新七支完整审计](evidence/feedback-redesign/remaining-2026-10-15/controlled-economy-run113522/additive-no-growth-native-audit.json)及[数值摘要](evidence/feedback-redesign/remaining-2026-10-15/controlled-economy-run113522/additive-no-growth-native-numeric-summary.json)在登记范围内limited/setup/strict PASS：U7/U8、R0、n1/J100，A40四格与正负隐藏dummy5%增量。[费用/转换补充v2](evidence/feedback-redesign/remaining-2026-10-15/controlled-economy-run113522/budget-supplement/native-budget-supplement-v2.json)另核11岗位收入、18独立非岗位、29普通费用及default政策3转换行PASS；v1把贸易吞吐当普通费用的首次FAIL保留。全部48SAV/417图OCR逐来源字节核对；旧失败不覆盖，未测全矩阵不自动PASS。 |
| E-ST | [rc.6包级G1](evidence/feedback-redesign/runtime-2026-10-15/static/package-rc6-452.json)、[107项程序回归](evidence/feedback-redesign/runtime-2026-10-15/static/rc6-final-unit-agent-452.json)、[程序合同/十语静态](evidence/feedback-redesign/runtime-2026-10-15/static/rc6-programmatic-agent-452.json)。程序报告明确保留其引擎NOT RUN边界。 |
| S-M / E-M | [第四票已重抽源档](evidence/feedback-redesign/runtime-2026-10-15/rc4/fb454_fourth_rerolled.sav)：2204.04.01，n4/R0/CD3，slots11/9/12，国内两模板553/5040人口、外国同物种哨兵200人口。[政体原始核验](evidence/feedback-redesign/runtime-2026-10-15/rc6/independent-runtime-seed-polity-scope.json)：auth_democratic、gov_moral_democracy、fanatic_xenophobe/pacifist。不是机器格式塔。 |
| S-N / E-N | [普通科研开始](evidence/feedback-redesign/runtime-2026-10-15/rc5/fb455_natural_start.sav)、[进度](evidence/feedback-redesign/runtime-2026-10-15/rc5/fb455_natural_progress.sav)、[自然成功](evidence/feedback-redesign/runtime-2026-10-15/rc5/fb455_natural_success.sav)；[完成审计](evidence/feedback-redesign/runtime-2026-10-15/rc5/independent-rc5-natural-success-audit.json)。为个体机械旧2203种子的自然延续；本轮此段无console，历史种子失败resource命令仍披露，不是fresh2200自然新局。 |
| E-SP | [J0/J100原生审计](evidence/feedback-redesign/runtime-2026-10-15/rc5/independent-rc5-initial-speed-audit.json)：n0月速1/0.75；[J500下限](evidence/feedback-redesign/runtime-2026-10-15/rc6-numeric/independent-rc6-floor-j500-audit.json)：n1、五所启用、实际分配500、bonus50排除、月速0.2。 |
| S-V / E-EC | [III/IV/V数值审计](evidence/feedback-redesign/runtime-2026-10-15/rc6-numeric/independent-rc6-stage3-4-5-numeric-audit.json)：原生stage2/3/4及progress500.6/750.4/950.4；九类country_base结算及岗位维护预算、中文tooltip。舰伤/航速只有修正提示，非战斗/航时实测。V原生档可作为受控V功能前置。 |
| E-RR | [跨候选冷却前缀](evidence/feedback-redesign/runtime-2026-10-15/rc4/rc4-cooldown-prefix-final-independent.json)及[rc.3重抽原始对照](evidence/feedback-redesign/runtime-2026-10-15/rc3/independent-reroll-claim-audit.json)。已观察3→2→1→0及第四票重抽；rc.3报告内原失败保留，不能整体继承为最终包PASS。 |
| E-CL | [rc.6清理/领取第四票](evidence/feedback-redesign/runtime-2026-10-15/rc6/independent-rc6-clean-claim4-audit.json)：单特质置换、待领奖励保留、CD3→2、两实际模板各+1、七名领袖含envoy及外国哨兵；七组新增空派系字段单列。 |
| E-OP | [优化/受控复发/无凭证重放](evidence/feedback-redesign/runtime-2026-10-15/rc6/independent-rc6-optimize-relapse-replay-audit.json)：n4→5一次、R0/CD2/slots不丢、唯一新局势从0开始。显式复发凭证不是自然10%概率样本。 |
| S-W / E-W | [准确死亡前](evidence/feedback-redesign/runtime-2026-10-15/rc6/fb456_white_before.sav)、[死亡审计](evidence/feedback-redesign/runtime-2026-10-15/rc6/independent-rc6-white-death-audit.json)、[重启审计](evidence/feedback-redesign/runtime-2026-10-15/rc6/independent-rc6-white-reboot-audit.json)：真实kill/on_action、UI精确支付500能量/200合金、XP25/level5/四次待选及技能保留，唯一active新ID，跨月官员预算8、本人免费/其他四人各4。仅一次死亡重启。 |
| S-Z | [历史零倍率待恢复档](../../assets/shishan-code-origin/evidence/vivhite-zero-xp-pending.sav)、[历史已恢复档](../../assets/shishan-code-origin/evidence/vivhite-zero-xp-revived.sav)；来源见[零经验倍率记录](../../docs/shishan-code-origin-vivhite-zero-xp-2026-09-28.md)。只作新候选的冻结输入，不继承旧PASS。 |
| S-L / E-L | [原始耗尽旧档](../../assets/shishan-code-origin/evidence/shishan_reward_exhausted.sav)、[首次23层历史证据](evidence/feedback-redesign/runtime-2026-10-15/rc2/fb452_legacy23.sav)、[最终旧档重复层审计](evidence/feedback-redesign/runtime-2026-10-15/rc6/independent-rc6-legacy-repeat-audit.json)、[再次真实重载](evidence/feedback-redesign/runtime-2026-10-15/rc6/rc6-legacy-repeat-reload-independent-comparison.json)。auth_machine_intelligence/gov_machine_empire/gestalt，U43、R24→25→25、CD2不动；只有耗尽旧档分支，不是机器格式塔完整自然路线。 |
| E-UI | [真实长名称修复与边界](feedback-redesign-full-name-ui-fix-2026-10-15.md)、[旧档完整名称帧](evidence/feedback-redesign/runtime-2026-10-15/rc3/rc3-legacy-full-name.jpg)。1600×900、请求UI缩放0.75；正文全名可达，原生紧凑标题仍省略，其它组合未执行。 |
| E-CACHE | [清理缓存故障及原生双探针](evidence/feedback-redesign/runtime-2026-10-15/rc4/independent-rc4-clean-target-audit.json)、[月内人口快照](evidence/feedback-redesign/runtime-2026-10-15/rc4/independent-rc4-month-population-audit.json)。同日owned_species枚举滞后问题已用真实population枚举修复；月内统计与即时人口差的严格FAIL原样保留，不能用另一个delta PASS覆盖。 |

所有复用都先验证对应`.native-save.json`、SHA和Mod manifest。E-M/E-N/E-W是个体机械，E-L才是机器格式塔；不按文件名推断。原始43份save是历史证据，新的0.2.1原生结果另建run，不覆盖这些文件。

## 逐项追踪：工具、起源、局势和岗位

| ID | 用例级状态 | 已有证据 | 最小剩余输入与操作 |
| --- | --- | --- | --- |
| ST-01 | PASS（现行包级工具范围） | E-REL正式0.2.1生产25/25脚本、13DDS、269键G1退出0，工具/EXE身份、命令及JSON齐全；E-ST保留已实际运行夹具的G1。语义边界为工具明确注册的有限规则。 | 当前输入无剩余。后续Q2至Q9若新增P夹具，在首次运行前单独过G1；该未来门禁不改写现有正式包PASS，也不宣称工具覆盖完整引擎语义。 |
| ST-02 | PASS（现行静态合同） | E-ST独立数值/预算/引用/凭证/资格合同通过；乘算渠道另由TS-06登记。 | 功能源码未变时无追加GUI；新调查若改变合同/生产，再按影响范围复核，不把加算登记为独立乘算。 |
| ST-03 | PASS（正式包边界） | E-REL正式VERSION/descriptor一致为0.2.1；正式90文件不含probe、诊断开关、预置状态或证据，原始91运行包与授权90生产投影分别留存；Steam匿名回下载90文件逐字节相同。 | 当前正式包无剩余。纯正式run103709Z/111512Z的新重载/显示样本分别列E-FORMAL/E-MIN，其余未执行观察不冒充完成；若增加夹具须继续与生产分离。 |
| LD-01 | NOT RUN（旧档加载子样本通过） | 个体机械各rc.6运行及机器格式塔耗尽旧档正常加载；最终日志仅21条环境描述符提示。 | Q1：两政体各一次短功能新开局，简中、单正式包，保存唯一局势及首次日志。仅开局/首月，不跑NAT路线。 |
| OR-01 | NOT RUN | -6/+3静态保留；已有机械存档和正式trait。 | Q1：创建器同物种有/无起源对照，检查两机械政体预算/栏位、有机不可选、强制trait仅一次；后继改造另接SV-04。 |
| OR-02 | NOT RUN（部分岗位容量已实证） | E-SP五所研究所可共存；旧种子n0及项目可用。 | Q1：短功能开局核n0/进度0/唯一项目与白绮链；无起源国家作负例；Q6正常建两所，不能拿add_building代建造证据。 |
| SP-01 | NOT RUN（n0 J0/100通过） | E-SP原生1/0.75；J500实证是n1，不能代n0。 | Q2：n0真实分配J99/199/200/299/300/399/400/499/500/1200及容量有空岗J0；逐状态保存，连续三月核进度。控制实际jobs，禁止只写J变量。 |
| SP-02 | NOT RUN（n1 J500下限通过） | E-SP：n1/J500原生0.2；E-OP n5计数不等于完整速度矩阵。 | Q2：补n1 J0/100/300/400/499及n5 J0/100/700/800/899/900；检查一次维护+0.25与真实100劳动力抵消。 |
| SP-03 | NOT RUN | 全国合计后floor只有程序检查，尚无两颗星球分配样本。 | Q2：两已拥有合法殖民地设置真实50+50、99+1、停一边就业；两政体分别核普通/无人机岗位。保存各planet→colony→job链。 |
| SP-04 | NOT RUN（部分阈值/惩罚通过） | E-EC已覆盖I及500/750/950跨阶段、V仍推进；E-CL清理撤局势。 | Q2：补249/250/499/749/949/1000及连续三月V，原生普通维护回I和V清理；每次核唯一active局势/旧修正撤销。 |
| JB-01 | NOT RUN（3/1描述和真实岗位部分通过） | E-SP实际J0/100/500、原生建筑提示3社会学/1凝聚力；预算类别包含普通生物学家。 | Q6：同星球隔离普通岗位与维护员，各固定100，再J50和空岗；关/开架构配对，读取岗位毛产出，补机器无人机。 |
| JB-02 | NOT RUN | 静态400矿物/360天/能量2与原岗位维护；五所是受控容量输入。 | Q6：正常UI排队并建成两所，记录真实扣矿/天数/能量及岗位消费品或能量来源；不新增稀有维护，两政体各核。 |
| EC-01 | NOT RUN（阶段及稳定七支子样本通过） | E-EC九类country_base与生物学家费用支持III–V减半。E-ECN旧自然F01及首次增长七支INVALID原样保留；新停止组装七支有限PASS，I期同上下文人口/岗位固定，归一化消费品维护均1.125，country_base九项固定，凝聚力/社会学可作开关架构配对。 | Q6无需重跑已冻结七支；补II与其它适用岗位资源在各阶段的毛产出/维护，按加算合同区分岗位、非岗位及衍生转换。新有限PASS不覆盖历史INVALID/严格P-W FAIL或整项全部阶段/资源。 |
| EC-02 | NOT RUN | E-EC有实际产出/费用行，但未做同岗位单位成本隔离。 | Q6复用EC-01账本，按基准毛产出和费用独立算1.285714/1.666667/2.2；加算回退下重新算开启架构后的值，不套旧倍率。 |
| EC-03 | NOT RUN（仅tooltip通过） | E-EC原生舰伤/亚光速提示III/IV/V为整数12/25/37；不能据此称战斗通过。 | Q7：固定同舰型、武器、提督、科技及路径，做阶段面板、单次受控命中与同路线计时；包含I/II，记录其它加成。 |

## 逐项追踪：特质、经济来源和兼容

| ID | 用例级状态 | 已有证据 | 最小剩余输入与操作 |
| --- | --- | --- | --- |
| TS-01 | NOT RUN（公式及若干实际点通过） | E-ST独立5%算术；原生U6/7、加权U与T66/67/68样本。 | Q3：单一合法模板非负R构造可达T10/20/40/100/1000，开关架构对照实际毛产出；低于合法基底的1/5只留算术。 |
| TS-02 | NOT RUN（常见正式键已有样本） | 原生负面、偏好、底盘/身份及旧43键计入U；白名单外第三方/异常双键未实机穷举。 | Q3/Q6：冻结键分类清单，分别加入正/负/零费/正式隐藏/事件/第三方键及原键+映射双键，取真实列表与独立U；不按特质点费过滤。 |
| TS-03 | NOT RUN（非均匀权重样本通过） | E-M/E-CL实际5040/553等权重；全覆盖+1使U精确+1。 | Q3：补800×10/200×5、空高键模板/未应用模板、全应用及仅20%实际覆盖+1；核9→10和+0.2，不用设置缓存U冒充。 |
| TS-04 | NOT RUN（外国共享模板隔离通过） | E-CL外国200人口/旧定义/七领袖克隆已实证。未证明国内外来物种岗位也只受一次架构。 | Q3/Q6：在同国内加入有实际岗位的外来谱系，保留外国同物种；开关架构配对全部国内岗位，核外来不入U、外国经济不吃本国B。 |
| TS-05 | NOT RUN（登记资源行有限样本通过） | [通道调查](trait-multiplication-investigation-2026-10-15.md)依据用户许可采用加算。E-ECN新七支U7/R0/B.35；正、负、隐藏dummy各使U8/B.40，单位凝聚力+0.05、社会学+0.15。补充11实际岗位收入行差分通过；29普通费用固定，含人口维护5行，消费品岗位维护归一化1.125。未出现资源/特殊来源及R经济隔离尚未覆盖。 | Q6保留已冻结11行及其资源；补食物/战略等其它合法岗位资源、未出现的人口费用/组装及国内非主体谱系岗位，保持traits和劳动力、仅改变R隔离B。不再要求旧Y/Y0=M，有限样本不代替资源×岗位穷举或另一政体。 |
| TS-06 | NOT RUN（A40加算四格子样本通过） | 原独乘目标历史保留，按授权加算合同验收。E-ECN凝聚力Q=1/社会学Q=3，A0/A40下开关B的增量均.35/1.05，交互0；新四格原生PASS支持同区加算，未把B直接当实际收入比值。 | Q6补原表其它A值/专项资源修正及重构兼容；逐项核实际分区与成熟账目。A40有限样本不把原独乘150/187.5/300/93.75表判PASS，也不覆盖其它资源或所有修正组合。 |
| TS-07 | NOT RUN（R23→24→25样本通过） | E-L真项目回调自动+1、单modifier、CD不动；程序压力至10001不是引擎压力。 | Q3：R100/1000/10000作前置，各调用真实结算得+1，分别核B邻层差0.05和真实岗位增量；另一政体保留最大压力哨兵。 |
| TS-08 | NOT RUN（幂等部分通过） | E-OP无凭证重放不变；E-L真实重载不重复迁移；E-CACHE严格即时快照FAIL保留。 | Q3/Q5：三月无票据、删一正/负键再加回，核仅U变化、R不刷和单modifier；固定人口或明确月脉冲时点，不覆盖旧FAIL。 |
| TS-09 | NOT RUN（R0交叉通过） | E-CL/E-OP状态特质一换一；E-W死亡不撤架构，但这些交叉R=0。 | Q5：从R>0种子分别清理/复发/真实死亡重启/改名/实际模板替换；复用S-L或只设前置R，逐项保留R并核U人口权重。 |
| TS-10 | NOT RUN（跨候选迁移/重载证据已有） | rc.2首次7/5/11/4→R23；rc.6 R24→25→25不重复，旧键/计数保留。 | Q5：正式0.2.1直接首次载原始耗尽旧档，保存重启再载并跨月，核R23/U43/T66及cd首次0；已迁移R24不能替代首次迁移。 |
| TS-11 | NOT RUN（部分覆盖提示/清理交叉通过） | E-CL领取09全覆盖；学习算法候选有部分覆盖提示，未有仅部分模板实际领取的完整对照。 | Q3：S-M同类pending选择11，仅未持有的主模板得键、子模板不动；再补等待中真实改造与重载，核原特质效果/维护提示。 |
| TS-12 | NOT RUN | 无主谱系实际人口/恢复尚无原生样本。 | Q3：R>0，把实际主谱系人口迁出/移除但保留空模板，再恢复真实人口；新save核无架构收益、R不丢及恢复U+R。 |
| TS-13 | NOT RUN（自然组装/事件刷新部分通过） | E-CACHE实际人口511→541；月内缓存窗口披露，奖励刷新后匹配。E-ECN实际P5491→5497→5503、U7，各档缓存比即时少6人口/42加权量，严格FAIL保留，不能靠U恰巧不变改判通过。 | Q3/Q9：组装/移入移出/局部改造和就业变化分别取月前后；准备真实1/10/50模板及小中大规模，与PF-01合并计时，不把工作效率当人口。 |
| TS-14 | NOT RUN（冷却前缀通过） | E-RR跨候选3→2→1→0，第四票重抽；E-CL最终领取CD2。 | Q4/Q5：最终正式包同run补跨月、真实研究中断、失败操作，完成RR-01至04缺失分支及机器智能样本。 |
| TS-15 | NOT RUN（若干重载通过） | S-M跨run重载候选/CD3；E-L层数重载；E-FORMAL补正式无夹具已领取R0/CD0/slots000重载。不是全部reroll状态集合。 | Q4/Q5：补重抽前/未确认/CD2/1/0实际退出重启，完成RR-05至08小池/AI/失效，逐state真实保存。 |
| RS-01 | NOT RUN（18实际独立非岗位行通过） | E-ECN新七支补充阴性18行PASS：country_base九项、力量投射影响力、轨道矿床能量/矿物、轨道研究矿床工程学、四人口类别贸易、恒星基地模块能量。default政策贸易吞吐及能量/贸易返还另按原版50%/50%衍生转换精确验证，不当独立阴性或普通维护。 | Q6复用已测行，补未出现的空间站/矿床资源、巨构/建筑等非岗位来源及混合账本；按实际来源分区判定，不能把18行或default政策转换泛化为所有非岗位均已通过。 |
| RS-02 | NOT RUN | 尚无市场、附庸、协定、月转移和一次性奖励的同日账本。 | Q6：同paused seed建合法订单/税/转移并留价格，架构开关配对独立来源；不能用顶部净额或价格波动替代。 |
| RS-03 | NOT RUN（已登记有限来源行） | E-ST涉及22类资源modifier；E-ECN补充原版category父链/文件SHA及实际11岗位、18独立非岗位、29普通费用、3default转换行的有限表。岗位资源出现能量/矿物/合金/消费品/凝聚力/贸易/三科研，不是所有岗位/DLC来源穷举。 | Q6扩展现有来源表至未出现资源、岗位/非岗位/转移/DLC组合；每个适用岗位有实际样本，无岗位来源才凭静态依据N/A，缺DLC才具体BLOCKED。foreign、其它政策、R高值及性能不从本表自动PASS。 |
| CP-01 | NOT RUN（独立第三方键子样本通过） | E-ECN原生新七支已载入夹具新增正式正、负、隐藏dummy键，未覆盖原版定义；各使U7→8/B.35→.40，凝聚力/社会学额外5%差分通过，A40同区加算子样本通过。尚非真实第三方完整Mod或冲突组合兼容验收。 | Q3/Q6复用已通过dummy样本，补实际第三方Mod、专项岗位/资源修正及定义冲突输入，逐项核原有效果/维护保留；明确加载集、版本和资源分区，不扩大为所有第三方组合PASS。 |

## 逐项追踪：奖励、reroll和项目

| ID | 用例级状态 | 已有证据 | 最小剩余输入与操作 |
| --- | --- | --- | --- |
| RW-01 | NOT RUN（自然成功及最终领取子链通过） | E-N普通科研自然成功n1、科技恢复；最终rc.6领取同一自然票据，流程跨候选。 | Q4：正式0.2.1在同run取成功前/后/选择后，核仅一实体、n不再加及下轮项目；补机器智能非耗尽池。 |
| RW-02 | NOT RUN（仅程序边界完整） | E-ST池0–6/层优先离线；实机有机械层三项和两池耗尽。 | Q4：两层各N3/2/1/0，保留低层优先和兼容层可用对照；以trait前置构造池，不直接写期望slot。 |
| RW-03 | NOT RUN（部分守卫/克隆通过） | 149资格场景/745实际守卫是程序；原生已持有/部分覆盖和外国隔离子样本。 | Q4：实际模板分别持有/互斥/政体不适用/不使用食物，另一个模板合法；确认全无受益不展示、部分受益只改合法者，两政体。 |
| RW-04 | NOT RUN（等权源码已审计） | E-ST精确权重遍历/原版守卫；实机只领取少数机械候选。 | Q4：39候选逐个构造合格前置并真实领取/读提示，至少一次每候选；资格不适用按来源说明，不用少数随机频率证明等权。 |
| RW-05 | NOT RUN | 清理后候选保持已修复；尚无真实中途失效1项→部分池→全耗尽的完整输入。 | Q4：保存pending后给实际模板加已抽候选/互斥键，使1项失效；重开，核仅失效项替换且CD不动，再耗尽全池一次R+1。 |
| RW-06 | NOT RUN（受控维护耗尽通过） | E-L原生complete_special_project触发R+1/CD2冻结，非自然科研；无耗尽优化普通科研完成。 | Q4/Q5：耗尽前置下维护/优化各走实际研究进度到完成，或先明确受控科研合同；仅R+1/n+1、旧计数不变、无实体，不能继承NAT通过。 |
| RW-07 | NOT RUN（10/20/30重放通过） | E-OP实际无receipt重放主结算事件不变。 | Q4：补无票据直接确认旧候选option、已消费选择重复点击、三个月检查、各事件重复窗口；机器智能分支也核。 |
| RW-08 | NOT RUN（同日清理/领取通过） | E-CL最终同日pending→清理→领取仅一次，无误R；原失效rc.4报告保留。 | Q5：在clean_pending真正退出重启加载后领取，再核优化恢复/维护不过期重建/局势不复建；补机器智能。 |
| RR-01 | NOT RUN（首次重抽子样本通过） | 原生三新项、CD3/used、同票据按钮禁用；最终两政体完整资源/失败操作矩阵未齐。 | Q4：cd0/N≥4首次重抽前后raw资源/状态，再实际尝试禁用入口；只扣合法选择冷却，不重开新票据。 |
| RR-02 | NOT RUN（跨候选前缀通过） | E-RR与E-CL已实证3→2→1→0及第四次可抽。 | Q4：正式0.2.1连续同run走四张真实项目receipt，两政体各留完整链；可受控项目完成，不称四次自然科研。 |
| RR-03 | NOT RUN（关闭/重开/跨月部分通过） | later及跨月未减CD的样本存在；真实中断/取消、失败按钮未覆盖完整。 | Q4/Q5：cd0不用重抽正常选；cd>0重开/失败点击/跨月/中断研究，各核不减CD不补票据。 |
| RR-04 | NOT RUN（自动补丁不减CD通过） | E-L R24→25 CD2不动；没有单候选实体确认CD2→1样本。 | Q4：耗尽连续两项目保持CD2，另造仅1合法实体候选，无法reroll但确认变1；两类政体。 |
| RR-05 | NOT RUN | 实机已见N足够时三项全新；N6/5/4原生精确替换数未做。 | Q4：三个冻结小池依次重抽，分别核3/2/1项来自旧组外、无重复、不跨层，保存前后实际候选。 |
| RR-06 | NOT RUN | N≤3禁用/候选失效仅离线合同。 | Q4：N3/2/1窗口实读disabled说明，再使一项失效，核自动修复不改变CD/used、不用洗牌冒充重抽。 |
| RR-07 | NOT RUN（部分重载已过） | 真实跨run加载S-M/CD3及R25；不覆盖所有cd/used和窗口重放。 | Q5：重抽前、后未选、确认后CD2/1/0逐档真正退出重启，重放旧动作，逐项核receipt/cd/used/candidates。 |
| RR-08 | NOT RUN | 新字段初始化/幂等程序合同，旧档部分重载；尚无AI原生选择/重抽。 | Q4/Q5：两个实际起源国家其一AI，项目成功后观察只领一项且遵同CD；原始旧档首次cd0/二次不重置单列。 |
| PR-01 | NOT RUN（n0维护2000自然完成通过） | E-N实际project1进度与成功/普通科技恢复；其它成本为程序公式/部分UI。 | Q5：n0/1/2/5各读三项目UI成本；清理/优化补至少一条真实科研进度完成，受控科研输入须明确区别自然路线。 |
| PR-02 | NOT RUN | E-ST13类receipt恢复为离线；真实自然研究启动/推进已过，但没有取消/中断三月重载。 | Q5：载S-N研究中，分别UI取消与真实引擎中断，三月后退出重载；优化也做一次，pending时检查不恢复下一循环。 |
| PR-03 | NOT RUN（I自然维护通过） | E-N实际维护2000、n一次/普通科技恢复；E-EC受控V不等于V维护完成。 | Q5：S-V作阶段前置，走普通科研完成维护并确认，核归零/旧惩罚撤销/新月速+0.25/清理成本+2000；补机器智能。 |
| PR-04 | NOT RUN（受控早期清理/优化/复发通过） | E-CL/E-OP原生on_success、换trait、单新局势0、待选不丢。 | Q5/Q6：补V清理和同岗位重构+25%/维护不变的开关账本，优化非复发/显式复发两支各重载；10%只用静态权重，非重复频率。 |
| PR-05 | NOT RUN | 外国共享模板哨兵不是第二个拥有pending的起源国家。 | Q3/Q4：两起源国家同时pending，分别重抽/领取/清理后保存重载双方；核state和模板按country隔离，不只看外国人口。 |

## 逐项追踪：白绮、保存迁移、显示及性能

| ID | 用例级状态 | 已有证据 | 最小剩余输入与操作 |
| --- | --- | --- | --- |
| VV-01 | NOT RUN（n0/1及死活样本通过） | E-W三country bonus死亡撤销/复活scale1；n0/1静态正确、非零XP恢复。 | Q5：n28/29仅作计数前置，分别指派/空闲读取工程150/155%、社会75/77.5%；补机器智能和实际科研面板，架构不随死亡撤销。 |
| VV-02 | NOT RUN（个人免费已实机通过） | E-W本人0/其他4人各4，native免费flag与跨月官员8；旧rc.5费用1.0 FAIL不覆盖。 | Q5：另一政体核本人/普通领袖任职与空闲费用；白绮选中时核无解雇入口，以原生不老死资格/高龄前置替代长期等年龄。 |
| VV-03 | NOT RUN（一次真实死复活通过） | E-W一次实际kill/on_action、严格500/200、唯一active、XP25/level5/技能/四待选、备份清理；E-FORMAL补正式包实际重载后白绮16777294整条raw不变、经验25/四待选/头像/freeflag保持。 | Q5：在真实复活档第二次死亡，分别energy499或alloys199不足资源禁用/不扣，再足额UI付款；核原统治者不替换、成长和n/R/CD不变。 |
| VV-04 | NOT RUN | 普通非零XP恢复不能替代零经验倍率恢复链。 | Q5：复用历史vivhite-zero-xp-pending/revived来源，读入当前正式包；零倍率前置下恢复、恢复途中再死、各自真实重载，最终清临时特质。 |
| SV-01 | NOT RUN（若干原生重载通过） | S-M跨run、E-L R25再载及S-W种子加载；E-FORMAL补正式90文件无夹具的I/n1/R0/CD0、已领取且白绮已重启状态，真实重载后Mod字段/全species定义/七领袖/国内人口raw保持。其它状态多数只有save，未真正退出重启。 | Q5：最小去重状态集I/V/n>0/重构/复发/pending/used/CD2/1/0/R>0/dead/reboot/迁移后逐一真实重启加载；已有同状态证据不重复。 |
| SV-02 | NOT RUN（干净旧种子延续部分通过） | E-N旧个体机械首次获得U加算/R0/cd0，但原表预算/二次重载全子项尚未齐。 | Q1/Q5：原始无旧迭代变量、已有正式正负键seed首次载0.2.1，核R0/不补n层/原trait，保存重启跨月；预算与OR-01合并。 |
| SV-03 | NOT RUN（异常策略与输入待逐项核验） | [实施文档](feedback-redesign-implementation-2026-10-04.md)已定缺失R补0、负数/非整数旧计数标异常且不静默取整、合法正重复量保留精度；代码保留旧效果/计数，未迁移时才执行。只读确认这些规则不等于异常旧档已实机通过。 | Q5先按实施文档逐项核对缺失/k0图标/负数/小数/正计数无载体/冲突状态的诊断和保留行为，再用副本构造输入并真实重载；某一未定处理策略才单列BLOCKED，不笼统宣称所有策略缺失，也不自行补造收益。 |
| SV-04 | NOT RUN | 普通clone/base_ref保留不是合法飞升/虚拟人口后继路线。 | Q3/Q5：有对应DLC的合法后继/虚拟输入，真实改造和重载，核谱系、实际人口口径和外国排除；缺具体DLC才标具体BLOCKED。 |
| UI-01 | NOT RUN（多处简中交互通过） | 实机奖励/disabled/清理优化/白绮重启和阶段tooltip已看；创建器、全候选及所有恢复状态未齐。 | Q1/Q4/Q5逐入口补缺截图：创建器、原特质维护成本/部分覆盖、死亡不能正常交谈、重构后架构入口；沿其它功能用例取帧，避免独立重跑。 |
| UI-02 | PASS（静态） | E-ST及E-REL18汉字/54UTF-8字节、十语键/引用/BOM/格式保护与完整名称通过；正式措辞修订后已重验。 | 生产文案不变时无新GUI；九外语仅“静态校验通过、运行时不在范围内”。 |
| UI-03 | NOT RUN（单配置正文完整通过） | E-UI正文完整名称/5%及动态值可达，紧凑标题省略已记录。 | Q8补正式包国家modifier悬停、起源/局势、普通/耗尽/优化结果，混合/高R及disabled；逐字人工核全名，不能仅OCR存在即判PASS。 |
| UI-04 | NOT RUN（1280/1.0两正文子样本通过） | E-UI保留1600×900/requested0.75；E-CONTROL原生1280×720默认1.0x，E-MIN正式1280×720/1.0两政体正文、统计与按钮直接可读，标题省略仍记录。不是三分辨率/全状态矩阵。 | Q8继续核G0所有实际合法组合和最小/默认/最大缩放；补1920/2560及UI-03其它入口/状态，保留实际像素帧和Windows缩放。环境不支持有设置证据，必需且无法跑才BLOCKED。 |
| UI-05 | NOT RUN（个别重载正文通过） | E-L高R重载全文可达；并非普通/耗尽/清理/复发/used完整正式无探针矩阵。 | Q5/Q8合并：移除展示fixture后正式包重启加载去重状态集，核全文/U/R/T/系数/CD/覆盖，无旧名、无重复modifier。 |
| L10N-01 | PASS（静态） | E-ST及E-REL十语言各269键/50文件、BOM/语言头/引用/空重键/外语简中占位检查通过；正式措辞修订后已重验。 | 文案变化才重做相应静态检查；九外语运行时不在范围内，不启动游戏。 |
| PF-01 | NOT RUN（独立保留） | 没有100月开/关配对的tick耗时证据；107程序通过及“无每日银河扫描”源码不替代性能。 | Q9：小/中/大帝国×1/10/50真实模板，预热后关/开各100游戏月，采p50/p95；>10%先复现再判。不得并入NAT排除。 |

## 逐项追踪：用户明确排除

| ID | 用例级状态 | 既有观察 | 本轮剩余操作 |
| --- | --- | --- | --- |
| NAT-01 | EXCLUDED | E-N旧档自然完成是功能子路径，不是22局正常发展配对。 | 无。保留原表和排除依据，不启动第一/第二种子长期自然新局。 |
| NAT-02 | EXCLUDED | 已有项目与reroll功能样本，不等于前30年优先维护路线。 | 无。不因已见维护成功把本路线改PASS。 |
| NAT-03 | EXCLUDED | E-CL/E-OP为受控清理/优化交叉，非完整自然优先清理体验。 | 无。不要求补长期经济发展记录。 |
| NAT-04 | EXCLUDED | E-EC受控V仅验证数值，不是约79.17年自然拖延后救援。 | 无。不运行自然V和后20年观察；功能V输入由SP/PR独立验。 |

## 最小执行批次与GUI路径

所有新夹具先写设计、通过正式G1，再进入隔离简中run；不得给生产加调试开关或把预期U/产出/候选写回当“实测”。下列为主任务顺序参考，可复用同一实际原生前置减少重复加载。

| 批次 | 最小前置 | 最短实际操作与合并覆盖 |
| --- | --- | --- |
| Q0 正式身份 | 正式0.2.1生产及fixture清单 | E-REL已完成G1/manifest/文案静态/源码与rc.6差异、Steam回执/回下载/标签核验；没有新输入时不重复。发布完成不混成74项已全通过。 |
| Q1 创建器与短功能起局 | 个体机械、机器智能各一合法配置；一有机/无起源对照 | 创建器看预算/资格→开始→暂停→F1项目/局势→原生save→首月。只跑短功能初始化，非NAT22路线。 |
| Q2 月速与边界 | S-N n0、S-V n1；两合法殖民地/实际就业输入 | 殖民地岗位页开关/限制实际分配，先读save确认J可达，再普通跨月；F1局势阈值/维护/清理。若引擎分配粒度无法达99/50等，先查真实API并明确BLOCKED，不能写虚构J。 |
| Q3 特质与谱系 | S-M和受控800/200、空模板、外来谱系、R高值、无主人口/虚拟前置 | 物种页实际改造/合法trait前置→架构详情→save，分别取population group/traits/ownership；候选部分覆盖选择11可复用S-M家族。R设置只作压力前置，不伪称已结算次数。 |
| Q4 奖励状态机 | 两政体分别预备每层N0–6，cd0/2与pending；第二origin国家可设AI | 真项目on_success→三选一→reroll/disabled/later→实体确认；保存每state。待选失效只改真实模板，不设置期望slot；39候选逐一核；同一批次完成CD链和AI/双国家隔离。 |
| Q5 恢复与领袖 | 既有实际S-M、S-N、S-W、S-L及零XP历史副本；缺失状态另造前置 | F4开始/取消研究→普通跨月→退出游戏/正式包重启载入；首都决议重启白绮。把有R清理/死亡、第二次死复活、预算成本和UI-05合并。受控complete_special_project与真正科研完成分别记账。 |
| Q6 经济隔离 | 同人口/traits/就业/效率/阶段的paused分叉，至少一合法岗位对应每资源与必要DLC | 先只开关架构，不改trait集合；正常刷新后读岗位毛产出、人口/岗位维护、非岗位和转移账本。合法食物机械、战略/DLC来源按安装原版核实；不能只看顶部净额。正常建两所另核400/360/2。 |
| Q7 舰船 | 同舰型/武器/提督/科技、固定环境和目标 | 切阶段后面板→同路线行进计时→一次受控命中；不把stage tooltip或静态25/12.5/37.5当实战完成。 |
| Q8 显示 | 已有mixed、高R、清理/复发/used和白绮状态；正式包无展示探针 | 暂停→引擎设置列合法分辨率/缩放→逐界面打开并人工逐字核名/数值/按钮→原图OCR匹配SHA。沿Q4/Q5重载一次补UI-05，不重跑自然路线。 |
| Q9 性能 | 独立1/10/50真实模板、小中大规模seed；相同日期/速度/机器 | 预热→同seed关/开各100游戏月→tick/刷新p50/p95；保留trace与噪声复验，和TS-13人口刷新样本共用种子，但不以普通几月顺畅代替。 |

## 已调查回退合同与待实测分界

当前实现可确认的量为B=0.05×(U+R)，进入原生岗位产出加算区，未增加岗位/人口维护。`1+B`只是机制系数展示，不自动等于实际收入比值。2026-10-15[通道调查结论及六项新合同](trait-multiplication-investigation-2026-10-15.md)已采用用户允许的回退；[只读依据](evidence/feedback-redesign/remaining-2026-10-15/trait-multiplication-readonly-evidence.json)包括本机原版/生成文档20组证据。TS-05/06、EC-01/02、RS-01/03、CP-01保留原目标历史，依新合同执行Q6后才判定。

只在其它修正A与B**确实同属原生岗位加算区**的隔离例中，基底100、T10的修订示例才是150/175/250/112.5（A为0/+25/+100/-37.5%）；同区重构+25%、T20为225。国家资源总修正、岗位专项或资源专项可能位于其它引擎分区，不得把所有修正强行合成A；实际配对必须解释分区。至少保留一个A非零对照、同国内非主体谱系岗位、非岗位/外国阴性、维护/J不变与真实重载；此段是验收设计，不是已经测得上述产出的PASS。

## 本次核对与后续更新

本次仅把原表74项逐项保留，静态PASS与原生子样本、尚未执行分支分开；四个NAT明确排除，PF完整保留。数值原生证据、白绮真实付费重启、两模板/七领袖/外国隔离、旧档重复层与既有错误均可按上方证据定位。正式0.2.1发布和后续本地用例取得新证据后，应按行追加run/存档SHA/原始日志及真实结论，不删除历史失败或用程序报告一键替换全部状态。

逐项集合校验为74/74，无缺漏、重复或额外ID；当前完整用例级状态为5项PASS（ST-01/02/03、UI-02、L10N-01）、65项NOT RUN、4项EXCLUDED、0项BLOCKED。55个本地Markdown引用均可定位，UTF-8无BOM、无替换字符、无行尾空白；校验报告为`_runtime/shishan_code/20261015-remaining/remaining-case-ledger-static-audit.json`。NOT RUN中的原生通过子样本继续按行保留，不能把这组严格完整性计数理解为既有实测全部失效。

正式0.2.1单状态补充：E-FORMAL实际副本90文件逐路径/字节/SHA等于发布身份且无probe，同日2209.11.28，国内P5474/W38318、U7/R0/T7/B0.35，n1/CD0/slots000，单架构mult7与白绮三bonus各1保持；主体48、所有species定义及七名owned leader整条raw一致，白绮当前唯一活跃、XP25/level5、四待选、中文原名/专属头像/freeflag均在。历史死亡通知不代表当前白绮死亡。

原始不变断言的3个FAIL没有抹掉：rights中两条完全相同的48条目重载后只留一条，primary/default/built及保留条目所有权利值不变，但此处未重新验证解算UI；外国colony3/species16777220的group956301353维护子类1→0并killed，group23简单子类1832→1833，带GROWTH_CAT_PROMOTION且同星同species总量守恒，支持原生就业重分配推断，不能称外国所有raw不变；九组新增空factions/wanted_factions。country仅AI、budget、modules顶层raw变化，modules差异仅上述rights去重；当前预算/高水位缓存43个递归字段变化（如矿工59.34614→69.4412），AI strategy id59的188缓存项消失，其余按id值相同。这些事实保留在JSON，经济不变与其它完整用例不能从本次核心状态保持自动PASS。

同run停止后`error.log`共29行，21条环境descriptor提示之外有8条真实game_text诊断，主任务第一次日志归档因此正确中止。[只读来源调查](evidence/feedback-redesign/remaining-2026-10-15/formal021-no-fixture-run103709/independent-formal021-localization-diagnostics.json)逐条保存原文、base64、原版键/文件/行号及SHA：3条global_event_country来自原版简中`federations_l_simp_chinese.yml:1591/1593/1595`三项理事会通知；5条owner/GetName/fromfrom/solar_system来自`nomads_1_l_simp_chinese.yml:16`游牧民裂隙通知，引用`astral_planes_l_simp_chinese.yml:200`。原版message_types和scripted_loc亦有对应声明；实际正式90文件无这些精确键/getter/格式引用或文件覆盖，普通owner作用域及既有游牧民解雇规则的广义交集另列，没有以零直接引用证明无间接影响。8条均为18:39:34，和原生设置页点击同秒、先于首次读档约11分34秒。当时结论仅为来源归属，**only source attribution, not yet causal reproduction**；旧调查JSON原样保留。

后续E-CONTROL已实际无Mod复现8/8相同文本，含CPP行号、中文及控制字符，只有时钟前缀不同；实际dlc_load与manifest均为enabled_mods=[]，菜单9776、默认1.0x有原图/OCR及设置快照。本构建这8条设置本地化签名无需本Mod/debug或其存档状态也出现，因此按原版可复现基线单列，不能把8条自动算成新Mod故障。两run的分辨率/缩放/debug并非完全相同，本对照不声称完整引擎因果轨迹或任意配置无间接影响。全部原始29行日志、停机完整logs、SAV/图/OCR/审计均逐SHA归档，没有删掉8条、改写历史调查或宣告零错误；其它新增诊断和未执行完整用例仍按自身证据判断。

后续E-MIN仅补UI-04的1280×720/1.0正文分支：独立逐字目视原图，个体P5474/U7/R0/T7/B0.35与机器P5567/U43/R25/T68/B3.4均能完整显示18字机制名、换行统计与关闭按钮；原生标题省略和正常操作可达全文同时记录。个体关闭有真实click及后图，机器仅核按钮完整可见，不虚写已点击。实际90文件逐SHA等于正式发布包，无probe/无debug，原始error.log21条descriptor之外无新诊断，完整日志19文件及全部27图/27OCR归档。没有新增SAV或对其它入口/合法缩放组合的证据，UI-04完整项继续NOT RUN。

后续E-ECN保留旧经济104包的F01试跑：三SAV与原生来源meta及ZIP日期一致，受控`fast_forward64/30/30`完整披露；37图/OCR的SHA/实际像素尺寸全对，warm等待守卫的12帧不删，独立直接看wait7已是03.02/暂停且console只有一次warm30天确认，主任务未重发。三档核心输入局部PASS不能覆盖原窗口INVALID、七支NOT RUN或即时P/W缓存严格FAIL；普通civilian自然增长和稳定度0.0114漂移均记录。旧审计80dd/precheckf78原字节与后续就业/载体边界开发32项报告、新旧源码/测试快照分列，修订后被测就业可保持，稳定度仍使窗口INVALID。error.log21条descriptor之外无新诊断，完整logs20文件含原gamestatetimer日志保原；没有改动programmatic单独timer取证目录或把现有少量月份当PF-01通过。

后续E-ECN新增run113522Z的48原生档：旧稳定度100但增长21档INVALID/32严格P-W FAIL保持；原生UI关闭组装、稳定两月后另取新21档，核心加算门禁有限PASS。凝聚力/社会学四格在A0/A40的B增量相同，正/负/隐藏独立键各额外5%，仍是加算。补充29普通费用及18独立非岗位行保持，11岗位收入行加算差分通过；贸易政策3行依精确上游及50%/50%转换另验，首次v1 FAIL不覆盖。官员成熟上月费用8与当月10分别记录，不混为同一账目或新的白绮费用结论。完整logs19文件中error.log只有原21缺订阅路径提示，所有417图/OCR及48SAV与原生来源逐字节一致。当前仅据实际登记资源更新TS-05/06、EC-01、RS-01/03、CP-01子样本；整项仍NOT RUN，另一政体、foreign资源、R经济差分、未出现来源及PF-01均未补造通过。

本文件未提交或推送；由主任务与本轮相关工作统一收口。
