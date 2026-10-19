# RC4 验收矩阵合并与最少串行操作

## 目标、范围与验收标准

主线程独占简中桌面，继续当前真实90／30巨像时序；本轮只读审核既有生产代码、原生阶段归档和发布门禁，减少重复新局、重复发射和重复保存。本文不执行UI／Steam，不修改Mod、版本、工具或旧证据，也不晋升任何case。RC4 progress-v1已经封版，后续按完整功能批次集中归档，不为每个小采样滚动索引。

验收依据是[当前需求](requirements-2026-10-19.md)及[发布门禁](../tools/publish_1019.py)的17组固定case加已实现随机组件1组。合并只能共用同一真实证据，不能省略分支或把代码审阅改名为实机通过。本文没有新增PASS数字；最终仍由主线程与独立验收共同审查。

仅适用于RC4树 `06485dc540a88b30cef15c27c323ff21cd88f04ad57b79e4f5bc0590937ef468`、59文件、run `20261019T112808Z`。唯一canonical manifest为[本轮归档manifest](evidence/1019-rc4-pk2-duration/manifest.json)，SHA `a83c605727f30a1d68db0e076348d814824d8ca56020ca2ab8864db8194f44f1`；原始静态报告仍为2e249c，不用外部LF版本替换。精确EXE、单Mod、简中与每份SAV的receipt／audit绑定继续生效。

## 当前材料能直接复用的范围

[RC4基线报告](evidence/1019-rc4-pk2-duration/analysis/rc4-pk2base-configuration-report-v1.json)已保存唯一Mother159／ship997、实际PK槽／组件、C0／L0／R0／六tier0、敌方天然殖民星17、真实战争、母星2归属及所有己方军队仍在家、无运输舰。它是加载未发布RC3未毁夹具后的RC4观察，不能用于新开局或公开0.3.1迁移。

同一SAV已有完整50槽组件及6个required component；现有`mother`子命令可以离线核对冻结设计、22大防御槽、原Relic五辅助组件、六专属core、十并发移动船坞和三防读数。无需专为这些字段再操作配置页或保存新档。独立验收线程已确认可离线补报告，但本文不假定尚未生成的报告已存在。供能、速度／伤害、同国同日Relic对照与实际跃迁仍缺实测。

[排队／day1](evidence/1019-rc4-pk2-duration/analysis/rc4-pk2-queued-day1-report-v1.json)与[phase2真实Stop](evidence/1019-rc4-pk2-duration/phase2/analysis/rc4-pk2-charge1-cancel-report-v1.json)已支持排队无收益、windup0→1／90、同日鼠标停止后订单消失且无收益。无需重做同一次早期取消；完整90日充能／30日发射、取消后重载、完成后重复回调仍分别欠证。取消的一日不计入后续requeue时长。phase2尚未挂入封版progress-v1，不是要求再采一次的理由。

静态代码足以确定公式、字段所有权、回调接线和待覆盖的分支，不足以确定原生API的运行效果：

- `eep_sync_mothership`按C推导L，只有一条替换型成长modifier；六个真实组件各自持有`triggered_ship_modifier`，六等权随机分支每次只增加一类tier和一次R，200是单次工作预算。其实际属性、RNG执行、刷新和重载仍靠RC4原生样本。
- 排队／取消空回调不发奖励；完成事件和共同结算再次调用同一目标谓词；C／G／D／造人和各once标记集中在`eep_settle_source`。可共享数学与幂等分析，不能因此省掉真实普通与巨像入口。
- 新局布局、启动奖励有独立一次性guard，月度只做修复／同步；这解释了重复初始化应保持什么，不能替代实际旧档迁移和重复调用。

本轮逐一核对上述相关9份工作区源文件：与归档`copied_mod`及manifest中的原始SHA全部相同。具体为startup、mother sync、六组件、共同结算、两种native consume、PK trigger、on_actions及通用effects。未据“源码和RC3相同”继承RC3的运行PASS。

## 18组case的最少独立操作

下表的“可合并”表示证据复用建议，所有case继续PENDING。

| Case | 最少保留的RC4真实操作／观察 | 可合并及仍不能省略的部分 |
| --- | --- | --- |
| hive_startup | 新Hive的Jan1与首月原生档，初始200、单母星、发电就业、人口／维护 | 直接用该分支12月经济的起始与第1月，不另开首月游戏 |
| machine_startup | 新Machine同上 | 干净Jan1另存为功能分支入口；当前PK夹具不是新局 |
| purifier_startup | 新普通洁癖同上 | 与全年经济及最终WS06新开局图共用实际画面／SAV |
| hive_economy | 本候选12个连续月初原生档、预算／库存／操作约束 | 复用已归档0.3.1历史baseline12月；不重跑baseline，不用RC3 candidate月 |
| machine_economy | 同上 | 同一新局可另分成长分支；功能注入、Relic、军队、移民不进入经济档 |
| purifier_economy | 同上 | 不把另两政体的非负预算当本政体结果 |
| lithoid_hive_first_month | 独立新石质Hive的Jan1与首月，非负净电 | 只首月，无须恢复已停止自然战役；之后另分支可做native结算 |
| mothership_configuration | 当前SAV离线mother／隐藏科技与专属舰段隔离；同国同日Relic实际对照、供能／维护／性能、实际跃迁 | 在一个Machine功能分支集中进行；不额外新造普通主宰，已有源码隔离和原生适用性如实说明。原生装备了Jump不等于已跳跃 |
| unlimited_growth | C0／9／10／19／20／200／10000，单modifier、四属性／回复、重复sync／同日reload、报告UI、母舰损毁不重生 | 与九节点collector、随机组件及一次最终restart共用；不需自然吞10000规模，也不在每政体重跑 |
| random_components | C49→50的门槛、自然RNG总账与六tier、六类独立原生导出／实际属性、普通控制舰、reload、C20500分批补差 | 自然九节点与成长合并；按预先固定源公式分离L与各tier贡献，actual C0作截距。六类均须有本轮真实非零RNGtier，缺一种不得过；不强制另做六类固定L UI |
| colossus_enemy_fire | 当前敌星真实原生完整90／30发射，precomplete／完成／重载、目标与军队状态；另一本国非核心真发射 | 同一敌星shot兼数学／成长／危机／敌人口不返还；本国shot可与Lithoid native分支合并，不能由回调手动结算顶替 |
| colossus_guards | 有真实前提的目标负例、完成时目标失效与核心失去归属；实际回调后零结算 | 七持续独立目标可共享ready／idle-day1／fired-day1；殖民中、真实地战及真实核心转手不能用同名flag代替，不需每种无效目标等90／30 |
| colossus_cancel_idempotence | 已有queue／Stop、取消后reload；真实完成后重复完成回调／reload，危机目标仅一次 | 复用当前取消和完整shot；重复回调只作防重放探针，不冒充第二次武器发射 |
| common_settlement | enemy普通材料、owned主种返还、native损耗／原生收益；每例q、C/G/D、人口、容量、once receipts | 所有实际结算统一离线分析；同一SAV可挂多个case，不能仅看总人口相等掩盖错误受益者或敌人口返还 |
| normal_dismantle_regression | 一次真实普通材料拆解决议、原始种子迁移、冻结q与ceil(2.4q)工期、自然完成及重载 | 在功能分支用符合生产前提的小q星减少模拟等待；不强制另跑旧native-normal全流程，不改progress／工期直接完成 |
| old_save_migration | 原始公开0.3.1空队列与历史付费队列两个独立来源，真实受伤before→迁移after→reload | 两个来源各load一次并保留各自身份；兼核额外星／布局／民用队列／无启动奖励。0.3.0付费档不是公开0.3.1替代品 |
| candidate_reload | 实际退出重启并加载已验RC4档，账本／奖励／设计不重发 | 安排在完整shot或成长repeat的reload处，连同最后一次日志freeze；同进程load不能抵native_restart |
| repeat_initialization | 对已有初始化的真实档重复生产initialize／startup／sync并保存，世界／船／奖励／民用队列不增 | 可与新局功能分支或迁移的重复sync合批；完整initialize/startup也要实际调用，不把仅sync相等当全初始化已测 |

## 保留分支，减少等待

建议最少四个新开局：Machine、Hive、普通洁癖各完整12月，加石质Hive仅首月。三组旧baseline只作为baseline和初始人口比较资料。母舰、成长、组件和普通功能可以共用一个Machine功能分支；石质native功能复用第四个新局首月后的独立分支。无须为每个case另开新局，也无须把成长／母舰／巨像在三政体重复一遍；有明确政体条件的native收益仍独立覆盖。

Machine只开一次：保存干净Jan1 anchor，经济与功能选择任一顺序，切换时实际原生reload该anchor并核C/L/R／六tier0、库存200、原布局和装备。经济可在新局直接完成后再回到anchor做功能；若先做功能，则必须核reload恢复后才开始经济。新局fixture给功能的任何资源／人口／变量不进入经济；不要仅重置C或tier后接着跑经济。原生autosave目录由实际当前load路径／written_at记录决定，不能把history归档目录当活动写入目录。

完整shot只需围绕引擎真实阶段采样，复用已有0／90和逐月计数，不逐日保存90次；首个真实fire字段、临完成一日和完成一日仍保留。当前完整shot完成后同档重复回调，再原生reload／保存，可同时覆盖结算防重、危机防重、成长无额外增加及candidate_reload的load部分。一次全进程restart可放在这条链或成长reload处，没必要每case重启游戏。

普通入口与巨像入口虽共享结算，但native咬噬有两个不同实现：`eep_native_consume`与`eep_native_consume_colossus`，后者把随机人口直接给母星。最少正向组合为当前敌星普通材料PK、本国非核心Lithoid PK、一次普通材料normal：分别覆盖敌方无返还／共同普通材料数学、本国主种返还／新增native巨像、普通入口种子与工期。未另外运行的旧native-normal明确列为未观察，不扩大成所有原生路径实测；不为它新增一个完整串行流程。原生随机结果只报告实际抽中的资源／人口类别，公平分布不要求以200次频率拟合等权声明。

成长固定九节点合并自然RNG记录、六频道原生导出与所有C边界；C49→50只需现有两个节点，不另跑专用门槛游戏。C10000已经有200次应得奖励，可检查六频道是否实际被抽到；若某频道仍为0，保留未覆盖，不能按概率说一定覆盖。C20500在同日第一次sync后立即UI保存first，检查R400／P10；随后实际FF30跨月采原生auto，检查月度自动补差至R410／P0。这样只用一份额外UI档，并保留单次预算与月度兑现两条证据。同日手动second仅为历史备选，不是当前必需步骤。

六类硬件效果采用主线程在未来样本产生前明确选择的自然增量路线：实际C0十原生导出与最大三防作截距，后续按已固定源系数独立计算L与各tier贡献，不用后续结果拟合系数；六种真实装备core分别必须有非零实际RNGtier、原生导出及对应实际三防／属性验证，经过刷新，普通舰负对照保持。满足这些要求时，不再强制额外六类固定L0／1／2重复UI。旧RC3 shield0／1／2只保留历史，不更名为RC4已跑固定L对照。报告明确测试的是组件自身源码归属与本轮实际RNG增量，不能写为“六类固定L2全部已测”。

护栏无需多次有效毁星：[既有批量方案](colossus-native-guard-batch-1019.md)把七个拒绝条件保持在七个不同真实目标上，可在全部构造且核实后共用一组before／after。分条控制台动作仍保存各自输入；人口、is_colony、目标ID和持久flag以实际SAV核验，不能因缺owner／空殖民导致联合trigger失败就认指定guard成功。殖民中与地战的真实布尔分别求值；完成重验可在未改变原始base的分支使目标或核心失效，再显式FROM派发实际完成回调。若原生武器先取消，这只算引擎中止，另一次无效状态回调才覆盖业务重验；无需重等完整充能。有效发射仍只有真实UI原生完成才计。

## 仍须主线程操作的最短清单

1. 当前shot的真实90／30完整完成、precomplete／fired人口与危机差值、重复／reload；本国非核心实际shot与native巨像分支。
2. 四个新开局；前三各12月原生预算，第四仅首月。旧baseline不重跑。
3. 一个Machine功能链：Relic同国同日、供能／性能／维护、实际跃迁；成长九节点合并六类真实RNG／独立属性归因、月度补差／报告、损毁不复活和重复初始化。普通舰负对照和主宰静态隔离共同保留，不另加普通主宰生成流程。
4. 一批真实护栏状态及完成重验；一次普通材料normal的实际种子／工期／完成。
5. 公开0.3.1空队列、历史付费队列分别真实受伤迁移／重载；至少一次RC4进程restart，结束后冻结完整本轮日志。

相同实际SAV／截图／动作／日志可被多个case按原SHA引用，最终只维护唯一run-id manifest。日志在对应进程停止后集中冻结一次，保留已知错误与因果未知项；不能提前声称clean。完整批次归档后再建下一版progress，逐单项保留scope，不为本表中的拟议步骤预置true，也不根据文件齐全直接给case PASS。

## 只读核对结果

本轮核对了需求、18case字段、母舰／成长检查器实际范围、原生批量护栏／损伤迁移／采集设计与三份已稳定RC4限定报告；9份相关生产源SHA与59文件冻结清单吻合。当前封版[progress-v1](evidence/1019-requirements/rc4-runtime-progress-v1.json)仍18组PENDING、0个true case check，未加入phase2、后续fire或任何RC3 candidate PASS。没有代码或测试夹具变化，因此未重复运行单元测试；也未执行上述任何待实机动作。

## RC4稳定base离线配置补证设计（实施前）

主线程授权立即对已归档`pk2base.sav`执行现有`check_1019.py --output <新文件> mother <SAV>`，另生成精简原版`NAME_Relic`源组件对照报告。只读取同一原生ZIP、receipt／audit／manifest和冻结源，不重复20项基线或18项排队报告，不创建阶段大归档或新进度索引。

预期核验：50槽、6 required、11 AUX、Relic原5 AUX与6真core各自槽位；十并发移动船坞；冻结专属科技定义、原生国家科技列表及其它实际juggernaut的存在／装备，用明确适用范围区分静态隔离与原生负对照。原版Relic对照保留源路径／SHA及完整组件重数和required差异，不把原版源码当同国同日原生参照。跳跃、供能、参考面板性能、其它主宰运行不受影响若没有实际对象仍PENDING／NOT_OBSERVED。

同时审阅已有全年经济CLI与读档合同，准备三类分支接到新raw后的批量离线汇总命令和范围说明；不创建缺raw的PASS，不调用任何runtime或UI。验收为新报告独占写入、所有实际引用SHA匹配、旧报告／索引／生产树未变，三类入口分别绑定原baseline及RC4新run。报告即使限定通过，也不提升`mothership_configuration`整case。

## 六组件发布门禁命名修订设计（未来RNG样本前）

主线程明确授权改内部case字段：`native_tier_zero_one_two_effect`改为`native_component_effects_source_attributed`，`growth_modifier_held_constant_during_component_probe`改为`growth_component_contributions_separated`。这两个名字分别要求组件自身的实际属性归因、基础成长L与各随机tier贡献分离，不把自然增量样本改称固定L探针。

验收覆盖不减少：本轮六类真实装备core各有非零实际RNGtier；actual C0原生十字段／最大三防作截距；所有后续系数在读未来样本前已由原版与冻结Mod源固定，L和各tier分别计算；全部必要导出／属性预测匹配且普通舰负对照通过。任何一种core未触发、缺导出、模型不符、后拟合系数、缺对照，均不能满足这两项；旧RC3报告与PENDING历史索引原字节保持。

实施只改发布case要求及必要的结构化归因核对、对应定向正反测试；不放松其它case或状态要求。年度汇总配方和当前mother离线报告先完成，再实施门禁修订。旧名称不能替代新要求或默默保留为true。

与growth工具已确定实际对接：random_components填写一个`component_attribution_report`的项目相对path／SHA，必须同时属于该case的analysis证据；不手写六类属性结果。它指向真实`eep.six-core-growth-report.v1`，合同`source_separated_native_rng_v1`，run_id／tree须匹配。门禁核六个非零实际整数tier、六coverage、C0零C／L／tier及实际10modifier／3最大值、两份预先固定模型SHA、十八原生phase的SAV SHA均已挂入该case；matrix／repeat／reload／budget／ordinary_controls各专项都必须有非空全true检查且限定通过。普通舰最大三防对照必须非空；该scope不冒称普通舰DPS／tracking／恢复均有导出。缺core／导出／原生文件／对照、未提供补样、不匹配的模型或旧运行报告均拒绝。

## 当前mother离线补证结果

已按现有CLI独占生成[原生mother报告](evidence/1019-analysis/rc4-pk2base-mother-report-v1.json)，SHA `305ee00fc8567eae218a48bb4b16990f93e59fb769aa1a74159416e40cb750f6`，14项`PASS_SCOPED`。随后独立重读原ZIP及原版`NAME_Relic`源，生成[完整组件对照](evidence/1019-analysis/rc4-pk2base-relic-source-comparison-v1.json)，SHA `50daf485727f3beac619a9cc946314b1a48d2725a8eacb3eec2aacb755712321`，17项限定检查通过。

实际50槽／6 required／11 AUX；原版Relic43槽逐slot／template全匹配，额外六core准确位于AUX6～11及一个专用PK槽；原版六required中四件相同，反应堆／推进器换为主宰／巨像底盘对应件。十船坞成立。全ZIP1008艘船／实际使用设计均检查，只有Mother997一艘juggernaut；34个国家的tech_status均没有`eep_mothership`。两专属舰段要求不可研究、未授予科技，无原版section key或相关ship-definition同路径覆盖。这支持静态隔离，不宣称已测试第二艘主宰运行。

同存档没有原生`NAME_Relic`参照船，实际jump、供能、速度／伤害面板仍未观察；完整`mothership_configuration`保持PENDING。未修改任何旧报告、SAV、manifest／gate／进度索引。三类全年汇总的前置核对和批量调用配方另见[经济汇总入口](economy-summary-1019.md)。

## 组件门禁实施与定向验证

已仅在`publish_1019.py`替换两个内部check名，并新增对独立growth报告的字节／scope／六类覆盖／C0截距／原生文件绑定核对；其它case及其字段未放松。`test_publish_1019.py`中的新输入全部为临时目录里的合成guard数据，非原生SAV或实机证据；正例不要求额外固定L UI，负例逐六类拒绝零tier／假coverage、bool／float计数，另拒缺导出／最大值、后改模型／容差、无对照、缺补样、旧run/tree、未挂原生文件或重复／错序phase，以及旧固定L名称顶替新字段。

实际验证：发布1019套件45项（57.985秒）、pending helper8项、历史single-homeworld5项、历史publication8项，共66项通过；定向diff空白检查通过。未生成新的真实RNG或经济PASS报告，18组封版progress仍PENDING且0个true check，SHA仍为`2cf16f8eebd1c4f09ee9d21c25c5b7f146e0a15ee36b88fd1aed23b224d6d36a`。主线程后续收齐完整功能批次时，仅需把实际growth报告经既有helper挂为random_components的analysis，并用同文件的collect_reference结果设置`component_attribution_report`；不手填SHA，不为每采样增加run或进度版本。

## HP工程容差合同追加（未来RNG样本前）

主线程已在真实成长样本生成前批准：仅HP量使用绝对`max(0.01,8*ULP32(expected))`、相对0；它是事先声明的工程允许量，不证明引擎内部存储位宽。源预测公式和系数不改。十项modifier导出（包括ship_hull_add）仍固定绝对0.01；账本／身份／槽位等仍精确比较。

growth工具已稳定新增`hp_tolerance_contract=max_0p01_or_8_binary32_ulp_expected_v1`及`hp_tolerance={absolute_floor:0.01,binary32_ulps:8,relative_tolerance:0,classification:predeclared_engineering_allowance_not_engine_storage_proof}`；顶层absolute_tolerance仍0.01。数值row完整保留observed／actual、expected、raw_delta、applied_tolerance、ulp32_expected／ulp_error、relative_tolerance。tolerance_kind仅`hp_binary32_ulp_engineering`或`fixed_absolute`。

发布门禁须绑定精确合同／8ULP／floor／rel0／声明范围，并独立核数值row使用的允许量；HP类型只适用于原生当前／最大H/A/S和max hull／armor trigger。把modifier套入HP允许量、增加ULP／相对误差、非有限值或旧报告缺合同均拒绝。新定向正反测试使用合成guard输入；不改任何历史实机报告或PENDING索引，不把工程允许量写成已经读到引擎位宽。

实施与验收：已绑定合同并独立重算ULP／允许量／原始差值，兼容工具实际使用的空格和ordinary三防斜杠字段名；两种标签都拒绝把modifier认作HP。发布1019套件46项（60.984秒）、pending helper8项、历史single-homeworld5项、历史publication8项，共67项通过；定向diff空白检查通过。与growth工具的稳定合同字面相同；未改其工具或读取未来RNG样本。封版progress原SHA `2cf16f8eebd1c4f09ee9d21c25c5b7f146e0a15ee36b88fd1aed23b224d6d36a`再次核对不变，所有18组仍PENDING，未生成真实成长PASS。
