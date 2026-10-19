# RC7 恢复后的保护条件运行记录

沿原四组三档执行卡，不增加矩阵。当前run20261019T204055Z、PID24520、简中单
生产Mod；已从主菜单真实载入原r7pkbase并另存。O/M/V命令仍按V同ID优先覆盖，
生产包及原checker/inspector/receiver不改。

## A组实际ready

十条既有构造命令已实际输入，r9gaR原生日期2201.01.21。核心物理2、Mother151，
九个不同源均存在，七个构造殖民地各有100真实人口且owner/controller0：

| 别名后缀 | 实际物理ID | 原生状态 |
| --- | --- | --- |
| guard_active | 1 | eep_active |
| guard_devouring | 5 | being_devoured |
| guard_credit | 8 | eep_credit_done，源仍活 |
| guard_destroy | 4 | eep_destroy_done，源仍活 |
| guard_secondary_core | 6 | eep_core，实际绑定仍为2 |
| guard_artificial | 7 | pc_habitat，实际殖民地23 |
| guard_qzero | 3 | size2、两个真实d_lithoid_devastation |
| r6_uncolonized | 1071 | pc_nuked，无owner/colony，人口0 |
| r6_neutral | 28 | pc_ocean，owner16777218，实际人口5357 |

中立owner实际type=default、capital字段2为colony ID，不是物理ID；war0只含
actor0和country1，未与该中立国交战。人工星判据来自本机构建原生
`00_planet_classes.txt`的pc_habitat段`is_artificial_planet=yes`；引擎生成
triggers文档明确is_artificial读取planet_classes设定，不靠测试flag命名推断。

下一步先逐项核ready前提，再自然FF1保存I（2201.01.22）；用新的主菜单薄包装
真实加载同一个R，执行原batch_dispatch、V uncolonized_dispatch、M neutral_dispatch、
原current_bound_core_reject，再FF1保存F同日比较。每源独立运行原no-settlement，
另核成长/奖励/六country与fleet层数及唯一增长修正；完整strict差异保留。
任何目标不存在、前提消失、未派发或日期不符均不得判拒绝成功。

B/C/D仍待执行，A构造成功也不代表负例已通过。所有结论按实际完成阶段追加。

首个A idle自然tick另出现原生`on_action_events_1.txt:8490`向
`EEP_GUARD_QZERO`添加district_city失败：该刻意size2＋两损耗deposit夹具只支持
1区划，殖民初始化的延迟原生布局事件尝试超出上限。保留完整错误和时间链；
须分别检查I/F的q0源仍有真实人口／殖民地、两损耗和size2，不能因总账未变就
忽略构造失效。此处不删日志、不归为生产脚本已通过，最终日志审计另逐项分类。

## A组完成与归档方案

R为2201.01.21，I/F均为2201.01.22。十个原no-settlement任务全部
PASS_SCOPED；原receiver也独立接收三档及base并复算十任务通过。各角色的
真实前提持续，核心可用、合格起源与灭绝机械政体均在；I/F的成长账本、
last三项、随机组件奖励和六层数及Mother对应字段一致，原growth检查两支均通过。
完整strict差异保留，不把作用域结果当作全存档相同。

现建立独立A包，仅复制已完成r9gaR/I/F、r9guardAbase及r9ga操作、精确输入
导入回执和receiver缓存。源文件先后SHA一致、SAV ZIP CRC、截图/OCR图SHA
及原生save/audit/receipt绑定逐项核验；归档原字节，索引引用项目内canonical
路径。活动日志仅保存明确标为诊断的摘录，最终停机日志另验。A可支持未殖民、
人工、吞噬中、已结算、中立五项；all_core仍等B/C，target复验等B，invalid
无成长等A/B/C/D及既有取消，不提前封整组。归档方案先于包及索引写入。

A包已复制254份原件（16,627,112字节）、四份原生档及48对截图/OCR，全部
SHA、ZIP CRC和图像绑定通过。原receiver十任务均PASS_SCOPED，原始前提与
增长补充报告均保留。仅将上述五项记true，索引现102 true／36 null，全部
18组与组件仍PENDING；未把活动日志附作final log。

## B组构造中的诊断边界

殖民探针已实际记录COLONIZING_TRUE及IS_COLONY_TRUE；外国secondary转交已实际
记录。首次地战建军后虽有ARMIES_CREATED，紧邻另有控制台`Invalid scripted
effect: e`；首次ground_inspect输出异常字面event_target并有`= effect`解析错误。
这不能证明地战成立或不存在，typed action只证明意图输入，不冒充引擎完整接收。
先按原卡自然推进一天，再检查真实ground_combat及army全表。如果原长探针仍
不能解析，保存独立诊断SAV并使用只读短log探针分别检查has_ground_combat和
双方owner，避免重建军队改变战场；必要时才使用原后备运输登陆。任何失败和
原始输入保持，未建立的状态不得派发回调或计通过。该诊断不改生产Mod、
原命令资产、checker或inspector。

2201.01.22诊断原生档r9gbDiag1确认ground_combat0关联colony1（物理17），
attacker73为owner0的machine_assault_1，defenders10～18实际owner1；双方均有
真实ground_combat0关联，攻击军血量171.23561/200，已发生战斗。短探针也记录
R9GB_GROUND_TRUE。原长探针为何异常仍未定，不能改称没有战斗。复用该未派发
回调诊断档作B-R，不再另造同态R；I/F目标日期2201.01.23，F须真实载入
r9gbDiag1。完整world17补充观察另存v2，原首次未请求world17的观察和诊断保留。

B-F仍先用原三段dispatch。如果ground原段仍出现同样解析失败且无实际派发marker，
则在同一次R加载、尚未推进时间的相同战场上，用短段显式作用于已核物理17的
eep_guard_ground_target，先检查has_ground_combat，再log专属marker并传Mother
作为FROM触发同一生产on_action。双方owner与真实combat的独立原生证据不省略，
这只替换失效的测试输入，不修改生产保护条件。每次失败、补充短命令、实际
marker及I/F完整原checker结果均归档；短段也失败则该项继续PENDING。

B首次ready重载在存档选择阶段安全失败，未点击读取：右栏保留旧滚动位置，
左栏最新r9gbI.sav被OCR成r9gbl.sav，原loader因此没选中组，向下扫描不能找到
上方ready。保留原失败截图及调用栈；用已观察1024×768截图中的同组卡位置
选择，再按原loader既有右栏滚顶动作重置，重新观察后用独占stage调用原load。
该修正只改变原生列表位置，不改SAV或receipt；原主菜单退出/确认截图保留为
本次载入的真实前置，最终新SAV仍必须确认身份。若原名OCR也失败，再考虑
同SHA导入易识别别名并记录映射，不伪造新的原生保存。

滚顶后文件名仍读成r9gbDiagl.sav；独立截图的原名标签正确，但紧接原loader
新帧又将标签读成r9gbDiagl，未达到原loader的唯一识别条件。第二
尝试也在读取前失败，未派发任何B回调。现已按前述方案将原r9gbDiag1原字节
独占导入当前隔离acceptance-fixtures/r9gbR.sav，另有LOAD_ALIAS_BYTES_ONLY
回执记录source、destination、共同SHA；ready角色仍是原生Diag1。重新从真实
主菜单打开载入列表并滚顶，用独占新stage载入r9gbR。不得把别名副本算作新
原生保存，不改第一次失败或原ready的audit/native-save。

别名已实际载入且SHA等于ready；B三段原dispatch均已记录：05:35:07殖民中、
05:35:52地战、05:36:33外国secondary。原ground_dispatch完整成功，备用短
dispatch没有执行。输入后立即读取活动game.log的断言先失败，随后原日志可见
最后marker；怀疑是提交与引擎日志写盘之间的时序，尚未证明根因。现三marker
已实际闭合，继续当前同一ready派发支的FF1和F保存，不重复输入、不重置战场。
原失败调用栈事实保留，诊断摘录另标而不冒充完整停机日志。

B完成后沿同一原receiver三角色接收，包名1020-rc7-guard-b-v1。白名单为已
完成r9gb前缀的操作／保存／失败诊断、ready别名导入回执与receiver缓存；
不读后续r9gc/r9gd或活动日志全文。先核三档真实前提和同日原no-settlement、
全部eep变量和Mother层数，再归档原字节、核ZIP/receipt/audit/图OCR/SHA。
只在通过后合入colonizing、ground、completion_revalidates_target三项；所有
core仍等C，owner复验等D。原短探针只读、备用短dispatch未执行须如实区分。

B已完成：R为2201.01.22，I/F为2201.01.23；原receiver三任务全通过，三档真实
前提持续，I/F所有eep变量和Mother层数一致，两支原growth通过。391份原件
20,771,236字节、三份原生档和84对截图/OCR均已核SHA/ZIP/receipt/audit。
所有失败与完整strict保留，未执行备用短dispatch。按前述限定三项合并设计
继续更新索引；C实际来源r7normalready2现已从主菜单载入，正在绑定old/new
物理别名，尚未执行迁移决议。

B三项已实际合入，当前105 true／33 null；5,256处引用／3,300唯一文件已复核
SHA，历史plan指纹不改，当前_scaffold同步。整组和组件保持PENDING。

C原生行星已确认为EEP_REG_Q2_50、50人口、May28。首次迁移选项点击被原精确
OCR保护在输入前拒绝；去掉悬停提示后确认迁移条目不在当前可见段，故只滚动
原生决议列表查找，不用console直接调用迁移效果。该次未执行迁移的截图和
异常原样保留，尚未创建C-R或给core拒绝计通过。

滚至底部后已目视确认迁移条目及“将母星绑定、帝国首都、王座岗位加成、累积
区划容量与已授予的额外并行建造队列转移至此；不搬建筑人口”等说明。该小字
未形成可用完整OCR标签。根据已观察1024×768原图，以原生条目标题位置
(800,430)物理点击，前后新GPU截图保留；仍须原migration_inspect与新SAV实际
确认才判迁移成功，不以点击本身代替结论。

C-R原生验证全部成立：May28，新绑定物理1/colony18，人口50；旧物理2仍属
本国、人口5177且无EEP core标记，实际capital等于新colony18。C/G21、D7、
made300、worlds1未变。后续I/F采用wait/fire语义名，避开已确认容易被OCR
混淆的单独大写I及尾数1；R仍用已保存r9gcR。按原卡自然一天、真实R重载、
原migrated callback、同量一天，C-I/F预计同为May29，实际仍以native日期为准。
D延续迁移成功后的同一状态，预计R May29、I/F May30；不跨六月月脉冲。
每次派发后等待限定日志写盘窗口核实际marker，不把即时读空再当作未派发。

C已完成原同日负例和增长检查：R May28，wait/fire均May29，实际迁移后核心
回调marker闭合。三档new core均只有d_eep_core，并有capacity/court/parallel
三个实际修正；旧core对应三修正与核心deposit均已移除，人口始终50/5177。
现准备1020-rc7-guard-c-v1，只归档已完成r9gc前缀及原receiver三档缓存，排除
活动D与日志全文。经原receiver和SHA/ZIP/receipt/audit/截图OCR核验后，只合入
all_core_worlds_rejected；其依据明确组合A当前/本国secondary、B外国secondary
和C迁移后bound core。失主与全invalid无成长仍等D，整组仍PENDING。

D转交原段已实际记录成功，但长inspect再次出现控制台`Invalid scripted effect:
og/l`且没有状态marker，自动链在保存前停止。保留原错误，不重复转交；现在
直接原生保存r9gdready并解析实际受益core owner、绑定、活receiver、old core
本国人口、initialized与Mother。只有实际前提全成立才继续I/F。原dispatch仍
优先；若同样解析失败，无实际marker，则在同一R加载且未推进的状态，用短段
作用于已核old core别名，log专属marker并以Mother为FROM调用原生产on_action。
短段只去掉重复的测试前提文字，独立R/I/F原生前提和原checker不省略；失败原件
全部归档，未派发不能计通过。

另在05:53:07记录同一原生nomads.94无效FROM错误，发生于C的真实May28→29；
最终完整日志审计须同时复核该旧结算输入的war清理链，不称零错误或直接当噪声。

C包286份原件、64对GPU/OCR、三档ZIP/audit/receipt校验及原receiver均通过，
all_core单项已合入，索引106 true／32 null。D-R实际receiver16777218、core
人口50、old core5177；原生capital已自动为colony0，但EEP绑定仍物理1，未重绑。
全部D原生前提已建立，后续wait/fire均预计May30，仍待实际原checker。

补充只读核对：C-R原生war0仍有attacker country0、war goal target1，但没有
defenders，country1对象已不存在；C-wait/fire中war0均已移除，与05:53:07原生
nomads.94无效FROM同日。新诊断r9log-nomads-native-war-cleanup-v2.json保留
三档SHA、完整war0原块及原版事件源码片段/hash，将并入最终停机日志审计包。
这支持旧战争清理触发链的推断，不等于可见完整引擎栈。C封包原件不追加改写。

D wait原生前提通过且ready已真实重载。06:03:11原长dispatch编译失败，实际
控制台报缺少log/fire_on_action等参数及`vent_target:eep_reg_old_core`无效；未
出现原marker。按事前短段方案同暂停日执行，06:03:35出现
R9GD_CORE_OWNER_LOSS_SHORT_DISPATCH。THIS仍是已核old物理2，FROM仍Mother151；
后续F原生和原no-settlement尚在执行。不得把长段失败改写为成功，也不只凭短
marker就给owner复验通过。

D-F实际完成，R May29、wait/fire同为May30；原no-settlement及两支growth均
PASS_SCOPED，全部EEP变量和Mother层数相同，三档foreign绑定与old core活人口
前提持续。实际使用短dispatch，原长段失败与完整strict保留。现按原receiver
三档复算后建立1020-rc7-guard-d-v1，白名单为已完成r9gd前缀、该receiver缓存；
不吸入正在进行r9growth或完整活动日志。原件SHA、ZIP、audit/receipt与图OCR
核完后仅合入core-owner复验，并以A/B/C/D全无成长加既有取消原件合入
unlimited.invalid_or_cancelled_no_growth；18整组与组件仍PENDING，最终日志未验。

D包198原件／11,418,131字节、40对GPU/OCR及三档ZIP/audit/receipt均通过。
核心owner复验与全invalid/cancelled无成长已按限定报告合入，索引108 true／
30 null；guard原十项均true，所有18整组与组件仍PENDING。取消部分另独立
验证五个原cache的SHA及内容指纹，再调用冻结原growth并比较全部EEP与Mother
变量及修正，不只复述旧报告标题。原失败和预算政策均未改。
