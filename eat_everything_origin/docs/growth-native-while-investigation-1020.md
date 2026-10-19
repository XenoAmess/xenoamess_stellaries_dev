# C10000原生奖励循环与导出时序调查

## 目标与边界（调查前）

RC6固定C10000 final实际六tier为shield34／armor37／hull39／damage22／tracking41／
regen27，合计R200，原生最大三防匹配既有source预测；但June1导出的7项modifier
仍显式匹配先前shield14／armor18／hull24／damage13／tracking22／regen13，合计
R104，而进入该节点前R4。本轮调查只读核查这条差异，不先假定引擎、Mod或
采样器有错，不放宽模型、不替换原18样本、不改生产代码或工具，不操作UI／Git。

待证假设分别是：（一）Mod虽有单次预算200，实际while无显式count导致引擎
限制100次，因此初次只发100、月度补剩96；（二）计数已足，export／触发修正／
原生health cache刷新先后不同；（三）其它可由真实计数／时间证据支持的原因。
不从组件名、计数巧合或二手wiki单独下结论。

## 只读设计与验收

先绑定运行manifest及冻结RC6实际脚本SHA，定位while条件、临时预算、奖励增量、
monthly调用与export命令顺序。查本机4.5.2生成的effects文档和原版while用例，
记录确切scope／count语法／默认或显式上限文字、文件行号和SHA；必要时补充
原作者／官方primary来源并保留URL。原生文档没写默认上限时明确标未知。

复用独立observer已固定的refresh／final audit与原FAIL，避免重解析仍在采样的
大SAV；原报告全部保留。主线程独占同日repeat／reload、新export及独立20500
counts probe，调查仅在回执固定后读取其结果，不改动采样。区分“原生文档
规则”“静态调用路径”“实际SAV计数／属性时序”三种证据，最后给最小下一步
和是否需要新RC重验的条件，不用假设替代实机结果。

## 已固定的源证据

原始证据与摘录集中于
[`1020-native-while-primary-evidence-v1.json`](evidence/1020-native-while-primary-evidence-v1.json)，
SHA256为`0058ad7333e0c5b594eb06117d856ef3130b064912295523cac4681ecc69112c`。
run manifest SHA为10f2ce0f5a699d8ad9f39769f46f919cf3e19f64f8cc24cc5d67ebf0347935f9，
RC6树仍cc181c8a27ede295e9fcebeffc5e10bb75e9cd643edec1d194b928993ffab33a。

- 本机EXE完整SHA复核为
  `400df27c82ddc845aa9dce79bd468d81f18f060d299cd263e3afa93aef4f7a83`。
  ASCII十进制offset38214336是
  `while effect limit never reached, aborting after 100 repetitions. Set a higher max count if needed. %s`。
  这是已发布二进制中的真实诊断数据；本调查没有反汇编调用路径，也没有据字符串
  的存在声称本轮一定执行了这个分支。相邻38214144／38214283分别为while文档
  描述与count示例，和生成文档对应。
- 本run userdir的`logs/script_documentation/effects.log:3343-3346`只明确limit或
  `count = [3|Variable]`及all scope，没写默认100；完整SHA为
  `985c95672f491f0458fcd34232743e2c2a1b9e1862743e2b156eea7e9ca5a773`。
- 冻结／实际载入的`common/scripted_effects/eep_mothership_effects.txt:33-63`
  与manifest SHA均为`4e2d25004b917cd4b7c46bc13efe32765ba58fbd10aaa92a2728034a035da2cc`。
  它先设work_budget200，while只有limit而无count；每次随机加一tier、R+1、budget-1，
  后清budget并镜像国家ledger。`events/eep_events.txt:46-57`中的eep.2再次调用sync，
  `common/on_actions/eep_on_actions.txt:3`将它挂到monthly pulse。临时预算200
  本身不能证明引擎执行200次。
- 原版`common/solar_system_initializers/federations_initializers.txt:1703-1708`、
  `fallen_empire_initializers.txt:475-480`都是planet scope的`while { count=115
  create_pop_group=... }`。两文件SHA分别
  `16b8cf994c5b46b8e08a56f2741f93cffd0b2979702d9a1e53914ae9c5356bfd`、
  `804c01dd8b168e349ab71b989844d0fb4144cac3a680a56381d2c0369af18cc7`。
  这些是原版直接大于100的count用例，证明语法／设计意图，不冒充本轮实际循环结果。
- 原版`events/origin_events_machine_age.txt:1936-1958`在owner/country scope同一
  while内同时使用limit和`count=num_dead_identities`；文件SHA为
  `bd42f473f2f43c59f6aa1e3d89fc1c0eb89ad4caff4f9a08f271db17cf3a6176`。
  其中循环内还递减同名变量，count与limit共存有直接原版依据。

只读扫描common／events共152个含while文件，提取1631个可直接解析的while，
literal count最大115。另10个块有直接比较／宏等超出简单字段解析器的形状，
本调查未解释它们，不将该枚举称为完整原版语义验证。

互联网搜索获得的[CWTools作者schema](https://raw.githubusercontent.com/cwtools/cwtools-stellaris-config/99147efe8072b331005b50536762dcc0b8573224/config/effects.cwt)
固定commit的899-909行也允许count与limit，但这是校验器作者的规则，不能代替
引擎默认上限证明。[EHOF原讨论串](https://steamcommunity.com/workshop/filedetails/discussion/2008059495/4203492762826532607/?ctp=9)
有玩家在2021年直接贴出的100次中止日志，只作历史原始观察；不外推它与当前
4.5.2完全相同。当前最强来源仍是本机原版文件、生成文档、二进制字符串及待完成
的同日实际计数探针。

## 真实计数与缓存反推必须区分

独立observer固定报告n07/C200 SHA为
`6331577631532bff6cb9e94aa050aa227a5612aeac2ed0b259e1636f83cc555d`，当时R4，
armor2／damage2，其余0。n08/C10000 SHA为
`177c8b96cb32152ce2fcc818eba417a9b75bf72bddb21a1ca68cf76bd086a37c`，refresh和final
两份SAV实际ledger都已R200，最终tiers为34／37／39／22／41／27。所谓R104及其
14／18／24／13／22／13 tiers，是从固定源系数、存储modifier export与refresh
最大三防反推的中间缓存状态；没有保存到直接R104账本。这条限制已同时告知root。

collector的`runtime_growth_1019.py:154-164`在每节点先sync再FF30取refresh，
之后在refresh日期export再FF30取final；因此final保存的export刻意来自refresh
日期，不能视为final当日即时export。假如初次只发100，refresh月度补齐96，但
modifier/HP刷新较晚，那么“ledger200、export/HP缓存对应104”与此顺序一致。
这仍是推断；要由同日即时export及单次20500 ledger确定。

## 最小下一步与决策条件

主线程已安排原18样本后的同日重新export新SAV，以及不经过monthly的C20500
单次sync存档。从基线R200起，单次后R300／pending110则直接支持只执行100；
R400／pending10则否定这次Mod调用受100次上限的假设，须调查其它刷新时序。
日期、Mother身份、C值、entitled410、R、pending、六tier之和与临时budget清理
都必须核对，不能只看一个R值。原样本和原FAIL不替换。

如仍需把引擎原语与Mod路径隔离，可由主线程在独立已声明probe分支用原生
country/root scope先设一个专用计数变量0，执行limit<250的无count while；
再用另一个0变量执行同limit、显式count200的while。每次只change_variable+1，
同日save。预期100／200是待测值，不是已执行结果；该候选不调用sync或随机奖。

如果实际单次预算不达设计200，须先修Mod显式count／工作预算合同、新RC冻结和
静态验收，再重验单次budget／累计ledger／C10000大节点的即时与延迟属性；不能
靠工具容差或少量补采把原设计bug变PASS。如果单次确达200而仅export采样过早，
应保留原FAIL，另行设计明确的收敛期＋即时export补采，不覆盖原18节点或改公式。
截至本报告，单次探针和重新export仍由root执行，尚未在此宣告最终根因。

## 同日实证复核与最小修复设计（改Mod前）

root已完成新的r6gexport1与r6gbudget1，均属run20261019T150008Z、2202.07.01。
其报告事实为重新export全部R200属性符合v4，而单次setC20500＋sync只将R200
增加为R300，entitled410／pending110，实际tiers46／57／57／36／62／42。先
独立核原生SAV、回执SHA和原始字段，再将确切结果追加到不可变新证据记录；
不将root口述值直接当本线程已验证。

本次授权生产改动严格只是在`eep_sync_mothership_components`现有while内增加
literal `count = 200`一行。保留预算设置200、两项limit、六路随机奖励、R增量、
budget减量、清理、国家镜像、pending计算及其它文件原字节；不改版本、descriptor、
source模型、collector或报告工具。静态防退化放在独立Mod结构回归测试中，读取
直接脚本结构，明确要求literal唯一count200，并核现有预算／limit／增减／清理
未移走；缺count、count100、嵌套伪count或移除limit等负例应拒绝，避免只靠文本
某处出现count200形成假通过。

静态检查只证明源合同，不能代替新的候选包静态验收和原生单次预算测试。root
负责后续新RC冻结，实测从R200单次到R400／pending10，再次到R410／pending0，
以及真实同日repeat／reload、不重复付奖、C10000大节点的收敛与即时导出；原RC6
18样本和FAIL永久保留，不以本次一行修复倒写旧验收结果。

独立原生复核现已完成，记录在
[`1020-component-budget-native-probes-v1.json`](evidence/1020-component-budget-native-probes-v1.json)，
SHA为`95dfc3983db4b2bd9a1ea86f4f7d004dfdf6be588664018ce627aff1113c418d`。
两份原生history与archived／receipt的SHA一致，日期均2202.07.01，owner0、
Mother fleet125／ship809不变。r6gexport1 SAV SHA为
`93e3f5826f10873f28a983f0660a446bdfba881d9dd6e82f8231085d5f0f4850`，其实际
R200与13个固定source预测通道全部匹配；r6gbudget1 SAV SHA为
`983e06cd8af63e4b5e35b02d1fe8d639e321ea62ebb8ef0c02eaca263ecf3925`，实际
R300、entitled410、pending110，tiers之和300、国家／舰队镜像与临时budget清理
成立。本线程只读SAV和回执，不宣称独立审核桌面命令链；“只调用一次sync且未
经过monthly”由root收集链负责。实际+100而非预算+200现已确认，与二进制诊断
一致，允许执行下述最小修复，但新显式count的实际效果仍待新RC探针。

## 生产修复与静态回归结果

生产`common/scripted_effects/eep_mothership_effects.txt`现只在原while直接增加
`count = 200`一行；新SHA为
`f704c30ea845d57dbad5bcb6c60ec657d5ae8d4ab6a55082055dccb38d7d5ec1`。
只删除这条唯一新增的8空格缩进／LF行，整文件SHA精确还原冻结RC6的
`4e2d25004b917cd4b7c46bc13efe32765ba58fbd10aaa92a2728034a035da2cc`。
因此budget、limit、random_list、增减、清理、镜像和其余所有脚本字节均未改。
本线程没有修改VERSION／descriptor；root独立将它们推进rc.7，包冻结归root。

新增`testing/test_component_work_budget.py`，SHA为
`b9e5d20af789a169ca894e05354bd1a25dbd9de523e6633ac4e0c575b92976b2`。
它从直接字段结构检查唯一literal count200、前置budget200、两项精确limit、
六路等权单tier奖励、R+1／budget-1和后置clear；缺count、count100／变量／object／
重复／嵌套伪count、guard缺失、预算／增减／清理／随机权重改变均有负例。
在`eat_everything_origin/testing`执行
`python -m unittest test_component_work_budget`：7 tests／0.045s全部通过。
这是一条Mod源合同回归，不修改或冒充外部工具及运行时语义执行。

生产文件已明确通知root封口，不再改动，允许主线程冻结candidate-rc7。当前只证明
静态源符合预期，RC7必须另做完整包验收和单次200原生probe；原RC6失败证据不变。

## RC7静态候选源独立归档设计（复制前）

root已完成candidate-rc7外部open_kaishek静态PASS并启动新简中run20261019T164112Z。
本线程不操作该run／UI，只新增`docs/evidence/1019-rc7-static/`保存完整候选59份
Mod源、候选VERSION、原始静态gate／report／source-index及必要冻结元数据；
不修改外部候选包，也不把静态PASS称为原生单次200预算或完整Mod验收。

复制前核实际candidate source-index的version／每文件SHA与59总数，计算tree与
root声明61b34f前缀精确值相符；核gate、report相互SHA绑定及同树、版本与PK／CSV
合同。目的目录独占创建、所有源字节复制前后双SHA、目标逐字节复核，设置-text
保护。归档索引记录每个source→destination、大小与SHA；独立二次进程重算本地
源清单与目标closure。不复制UI、旧run raw或完整游戏文件。与RC6档独立，不改写
任何历史静态报告或运行时FAIL。

## 真实错误日志与RC7归档封口

localization_docs已冻结RC6最终日志。本线程另读canonical
[`error.log`](evidence/1019-rc6-final-logs-v1/logs/error.log)原字节，SHA为
`b8a0cc17158bf05ebde64f42ed71ec17bd12687d5488fb8d6e7d462ceaf740f6`，第24行
00:24:35确有100次中止，并明确追踪到原
`eep_mothership_effects.txt:35`→`eep_sync_mothership_components`的:195调用→
`eep_sync_mothership`。这将缺省100由二进制诊断线索推进到本RC6 run实际执行的
错误证据；日志本身没绑定具体采样stage，不擅自指定它发生于n08或预算probe。
原真实错误不删、不改写；新candidate需在其独立run再验证不会出现该错误。

RC7静态源已原字节归档于
[`1019-rc7-static`](evidence/1019-rc7-static/source-index.json)，精确Mod树为
`61b34f6dbdc277c44364889d5f1e1cd2773a4624786bbf0d538079fc6ba4feb0`，
version0.4.0-rc.7，59份Mod源＋VERSION＋原gate／report共62份原始载荷／3,837,366字节。
候选与run20261019T164112Z实际copied_mod的59文件逐源一致。source-index为验证后
新建的归档清单，而非伪造外部工具输出；SHA为
`40f160a5e733761556421f683b135694443255cad2975eccc4b88bf421b056cf`。

原gate SHA为`ed6c0fc3bfa92c38b75c7a89bca0453e164e6f5f70a5eab546fa7be0bcb91d04`；
原open_kaishek报告SHA为
`b48b6160c234ba77f6b18a5ce7b6b7987b0cfc47fd98ebe5675455f917f61fb9`，
PASS36P／12DDS／131keys／10语言。0CSV适用性、原生固定路径合同、1个PK inline
数值来源及3个native回调均与实际源字节匹配；其它语言仅静态校验通过，运行时
不在范围内。没有在归档过程重新执行外部工具或运行游戏。

独立二次进程的9项来源／目标字节、完整59树、gate/report SHA、run单Mod简中
绑定、显式count修复和报告合同复核全部通过，记录
[`byte-verification-v1.json`](evidence/1019-rc7-static/byte-verification-v1.json) SHA为
`7685f699871a7a6501e9807bd064d9da3535f1894541ae39cb47092252c5739f`。
本目录至此封口，状态始终STATIC_PACKAGE_PASS_RUNTIME_PENDING；不借静态归档
宣告单次200或整个RC7已实机通过。生产、测试及本文一并交root统一提交，本线程
不执行Git或桌面动作。
