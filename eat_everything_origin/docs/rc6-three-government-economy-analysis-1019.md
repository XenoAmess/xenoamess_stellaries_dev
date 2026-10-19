# RC6三政体开局与十二月经济独立只读分析

## 目标、范围、设计与验收（分析前）

仅监测run150008Z由主线程独占UI生成的不可变月度receipt与原生SAV／audit，
先Purifier r6pu、再Hive r6hv、最后Machine r6mc。若实际初始UI失败导致更换prefix，
只接受root明确的新prefix，不猜测、不拼接失败分支。不读取UI／OCR或活动日志，
不操作游戏、生产Mod、Git或其它代理的进度文件。阶段缺项只报告观察，不提前写
完整分支PASS；各分支m00、m01—12、yearui及总collector receipt齐备后才排他新建
完整报告与最终schema payload提案，历史报告和本轮原件不覆盖。

显式绑定RC6版本0.4.0-rc.6、树
cc181c8a27ede295e9fcebeffc5e10bb75e9cd643edec1d194b928993ffab33a，
精确EXE400df27c…、简中、唯一Mod、59源文件、static gate与report、原生CSV／PK合同。
用已验证的economy package接口独立复核来源；每份实际SAV核SHA、ZIP CRC、根日期、
audit gamestate与receipt来源，保留原始数字精度和全预算分类。月档还核真实auto源、
mtime新鲜性和每次单独FF30、十二个正确月序；年末原生UI档仅作同日数据对照，
本任务不重新解读截图。

基线唯一映射为
`docs/evidence/1019-baseline-reference-map/baseline-031-economy-map-v1.json`，
按branch取baseline_months；逐份复核其实际0.3.1原SAV的current_month收入减费用，
不用month00缓存预算替代12个月。候选同样从原生分类独立求净电，逐月要求>=0，
给出与同月历史基线差值、库存与原生海容，并保留其它资源收支。基线保留其原
profile／版本标签，不当作RC6运行或纯原版控制。

开局核m00唯一母星／正确星球类型、实际civic、原生200电、C0、L／R／六tier及
奖励镜像0、实际六core各一件且槽位正确、自动吞噬关闭；m01核发电岗位有真实
workforce，人口对比同preset历史原母星，不把被取消的赠品星人口算损失。正常维护
以真实非零普通费用、原Mother优惠未扩大且未施加到country为范围，不能写成
Mother没有原优惠。母舰／普通舰身份与岗位全部直接字段逐检查点保留。

操作约束提案只根据总／月receipt中的12条实际FF30、逐资源库存净账闭合、原生
岗位limits与初始owned船身份检查点，不把仅月末相同夸大成全过程监控。无资源
注入／交易补贴／关闭岗位／拆船若缺足够已记录执行链支持，则对应值保留null、
case保持PENDING并明确缺项；正常原生trade收入不等于补贴，原生-1岗位哨兵不当关闭。

最终payload使用既有eep-1019-acceptance-v1字段：startup的single_homeworld、
correct_homeworld_type、initial_energy_200、first_month_generator_jobs、auto_devour_off、
population_preserved、normal_upkeep；economy的baseline_12_months、candidate_12_months、
all_net_energy_nonnegative、no_resource_injection、no_trade_subsidy、no_job_closure、
no_ship_disband。economy[branch]含实际日期／净电／native_save证据的baseline_months
与candidate_months各12行。每个提案独立输出供root／release显式组装，本线程不把
18case其它组晋级，也不创建final-result.json。所有未完成组保持PENDING。

## 完整分支后的薄归档与可移植引用

为形成真实project-relative native_save引用，完整分支仅将m00—12与yearui的
SAV／audit／receipt、12份economy摘要、总receipt与auto/UI比较原字节复制到
`docs/evidence/1019-rc6-economy/<branch>/`，按文件独占新建并逐源双读SHA／目标
字节复核，配置`-text`。不复制Mod、UI图、actions或logs；总receipt内原有图片和
命令引用原样保留，但本任务不读取图像。若root指定另一个已完成canonical归档，
优先复用它而不重复复制。manifest只作为来源绑定附件，不以此扩展为整run归档。
完整case提案在缺screenshot／actions／最终log证据种类时仍为PENDING，即使其
有限原生检查项已经满足；root组装其它线程证据后才决定晋级。每个输出的状态和
scope必须区分“原生净电／开局检查通过”与“完整case／整个Mod通过”。

## Purifier维护分类误判与追加更正设计（补证前）

Purifier12月净电均正，最小40.63438、末月41.15660；初版完整报告只因分析器沿用
旧Machine的扁平`planet_districts`费用名而把normal_upkeep置false。真实原生费用
分别在planet_districts_farming／mining／generator／cities。原版
`common/economic_categories/00_common_categories.txt:931-956`明确四者parent均为
planet_districts；它们是原生区划维护，不能把分类拆分误判为无维护。

保留Purifier的原报告、payload、索引、v1分析源码及FAIL全部原字节。先核原始
来源和该原生分类文件，再追加仅更正normal_upkeep的受限补证／report-v2／
payload-v2，继承其它已验证数据，不重新fullparse 14个SAV。更正后的维护判定
要求ships、ship_components、planet_buildings各有非零费用，并按原生parent链
汇总planet_districts及其后代；仍要求旧新Mother优惠相等且仅施加Mother舰队、
未施加country。不是放宽为“任意费用非零”。后续Hive／Machine改用独立v2源码，
按该已确认parent规则处理，不改写首次源码，也不把更正扩到其它checks。

原版分类文件SHA256为b3da494d1889bf79a361840f4e9705995e8cd2bbee09d65629d7e182cf46f01b；
修正按该文件实际parent声明递归构造区划族，而不是按名字前缀猜。Purifier原
v1 FAIL报告SHA为ded9e3d1981be029663bd9fa1aae45d2ac460e5a699a97c18696a4a5869fa9b4，
v2受限报告SHA为546d9c557a47601bb6d28b56c6f54a18aeaf4fe789648e74ea3001a8a78ce9df；
补证只改normal_upkeep及其分类说明，所有原生检查点、预算、其它checks均相同。

## Purifier完整原生分支结果

已完成薄归档`1019-rc6-economy/purifier/`，57份原始载荷9,560,674字节；含14份
SAV（m00—12及yearui）、原audit／receipt、12月摘要、总receipt与同日比较，均逐源
复制复核。Mother实际fleet150／ship1077，不能沿用其它run的159／997。

开局7项原生检查均真：唯一pc_relic母星，初始200电、母星4800人口与历史bpm00
原母星相同、首月technician实际400/400、自动吞噬关、所有14个检查点C0与实际
六核心／槽位零成长、正常普通维护存在且Mother原优惠只在自身舰队。首月净电
40.63438，末月41.15660，12月均正；逐资源库存净账闭合，所有有限岗位限额为
原生最大、全部初始舰船ID／舰队／名字在14个检查点保持。年末auto／UI各经济
字段独立比较一致，12条receipt命令均为FF30。

使用[Purifier payload-v2](evidence/1019-rc6-economy/purifier/payload-proposal-v2.json)，
SHA为9b1b8a74a8507c4194524e232cd604cfea8fb09d8d37751d0827456d9192a246。
startup的7值为true；economy的12月基线／候选／净电3值为true，其余4项操作链
约束仍null，两case均PENDING。此处没有读取UI／动作链／日志，不能替root完成
所需证据种类组装。Hive／Machine尚未有完整年度回执，不预置其结果。

## Hive真实preset识别补充（后续完整解析前）

root开始r6hv，picker标签存在截断，本线程不读取UI或从label认定分支。完整
分支解析增加原生founder_species_ref绑定species_db实体与traits核对；有机Hive
必须具有蜂巢civic且创始物种没有trait_lithoid／trait_machine_unit／trait_mechanical，
并保持pc_hive母星。Machine须有其真实机器物种特征。该前置用于拒绝误选的
Lithoid蜂巢，不改变此前Purifier数据或已冻结源码；新增v3分析源码用于后续组。
此前Purifier原audit已绑定其founder物种，人类有机traits且无上述机械／噬岩trait，
可直接从已封存原audit复读，不重新解析其14个SAV。

root明确将Hive正式新前缀改为`r6hvc`：worker26559的`r6hv`只在退出旧局UI阶段
失败，一次Esc关闭Mother左栏却未打开menu，寻找退出到菜单label时严格停止，
没有开始Hive也没有新SAV。该组失败GPU／OCR由root保留，本线程不读取或移入
新Hive经济证据。worker47638仅从已关闭左栏状态按既有方案重试；后续完整分析
只接受r6hvcm00—12／r6hvcyearui／r6hvc总receipt，机械仍r6mc。

后续v3还将同一SAV的fleet／ships原生数据库各建一次只读索引，代替按owned船
逐次扫描大数据库；取值、身份、原始体和全部校验不变，以减少年度统一解析CPU。
已冻结v1／v2和Purifier原件／补证不改。

三分支全部完整且各自byte-verification通过后，再独占新建
`1019-rc6-economy/three-branch-payload-proposal-v1.json`及精简summary：合并原6个
startup／economy case和三组12月数值，保留case的PENDING与操作链null。按实际
prefix r6pu／r6hvc／r6mc和相同run／RC6树／version核对，引用每个不可变报告、
payload、原始索引与独立复核，不复制大报告或推断未完成分支。缺任一分支时只
返回PENDING且不落盘；该汇总不是最终18case或final-result.json。

## Hive完整原生分支结果

正式prefix为r6hvc，原r6hv退出失败没有混入。已完成57份原始载荷／8,695,685字节
薄归档，14份SAV的来源、CRC、gamestate／audit／receipt和年度auto/UI字段均核验。
原生founder为HUM，traits为organic／hive_mind／continental_preference，无噬岩或
机械特征。唯一pc_hive母星初始5300人口，与历史bhm00相同；不能沿用Purifier的
4800。初始200电，首月technician_drone真实workforce508／max1200，自动吞噬关，
C0、六核心实际槽位及零成长均保持。

十二月净电18.28253→25.81228，最小18.28253；相较同月基线改善57.18918—61.86929。
能源库存200→464.85573，全库存资源净账闭合；有限岗位limit仍最大、初始owned船
身份／舰队／名称在检查点保持。正常维护按原生parent族归类后成立，不需要更正报告。
开局7值、经济12月基线／候选／非负3值均真；操作链4值仍null，case仍PENDING。

[Hive报告](evidence/1019-rc6-economy/hive/native-branch-report.json) SHA为
001acb4c75a14ee00519cf09f3d42467b55eb0900a08f1d4d98ba322705521b3；
[payload](evidence/1019-rc6-economy/hive/payload-proposal.json) SHA为
a284624c193edb08bf8405c3913cd58cd204a095482f2e7e139764a61fd9367e；
[独立11项复核](evidence/1019-rc6-economy/hive/byte-verification-v1.json) SHA为
bc79cab8d3c51fb8c82878bd47ade56869d8b51e93a6faa0c300a89e7c5848c2。
该目录及v3分析源码封口，后续Machine使用相同v3规则；不操作或离开root的Machine UI。

## Machine完整原生分支结果与三组合并

Machine正式prefix为r6mc，仅在年度总receipt和yearui完成后统一解析。后续独立
repeatinit2／growth探针不属于经济操作链，没有纳入该分支或读取其状态。Machine
真实Mother为fleet125／ship809；m12与yearui原生SAV字节一致，SHA256为
bd4104dd2e31cfff0d2f76abf55e2eb303709ec86ca3118ec0d9fb6a59a3a696，yearui
receipt为9a6f69149f8020c4504ded84b50eae78e8d76777969773e321cc6133c5f49b88。

开局7项原生检查均真：唯一pc_machine母星、初始200电、原母星4800人口与bmm00相同、
真实机器创始物种、首月technician_drone workforce904／max1800、自动吞噬关、
C0／六核心实际槽位零成长及正常普通维护。12月净电依次为2.85755、3.29658、
3.84408、4.39226、4.94032、5.48746、5.92606、6.36377、6.80222、7.34978、
7.78724、8.22547，均非负；库存200→267.27279。相较对应旧版同月净电改善
161.20939—167.99876；这不是纯原版或相同银河随机数的对照，历史profile标签
与真实0.3.1版本仍按baseline map原样保留。

Machine报告SHA为55cb53915a82c7b5be9df50c482040a6f3dee2a6c4fc5d171d45e937f86ec330，
payload为eabf39768bf373d1b99dd8a14f41ba238966d10e3a3b5a13af23e84965494994；
独立11项byte-verification均真，SHA为
f1c2e7369d3b6d446d62c8bc466ac71fe8f2ea9a444a4ea48fabf6c10775c1b5。
三分支各自原生资源库存净账、有限岗位限额、初始owned船身份与12次FF30回执
观察均通过，年末auto/UI经济字段一致；此处的UI一致指既有receipt中的字段
比较结果，本线程未执行桌面操作或独立读取图像。

三组合并已独占新建[精简结果](evidence/1019-rc6-economy/three-branch-native-summary-v1.json)
和[六case提案](evidence/1019-rc6-economy/three-branch-payload-proposal-v1.json)，SHA分别为
0f8fba5dfaad476cf3332c4867ea331da4fe59dc66bb01ee9d1723a2bff8b2e6与
801796231981aa1fbef7230877374edef817eb7ed3f10508808d4bc06296d358。
生成器只接受三组已封存的独立复核，绑定相同run／RC6版本／完整树；接着使用
独立进程仅做SHA引用闭合、六case状态、三组各12月baseline／candidate以及
操作链null保持检查，不重解析SAV。复核95个不同引用均存在且SHA匹配，6个case
全部PENDING，36个baseline月与36个candidate月日期逐组一致，12个操作链值均为
null。Machine目录62文件／9,279,626字节，其按相对路径排序、逐文件输入UTF-8
路径＋NUL＋原字节的树SHA为
65e8d3753acfe997cbc91af408f30c3a6a62055ed6c65f7b3b94aea151334e06；
三组合并源码SHA为11f43dc307eeb175fb5862e7609ca7c7dfcef050e479f41ec4b60104d15128f2。
全部分支目录、分析源码、两份合并JSON及本文至此封口，由root统一提交，不另行
执行Git写操作。未重复复制59份Mod或与本任务无关UI。

| 分支 | 首月／最小净电 | 末月净电 | 初末能源库存 |
| --- | ---: | ---: | ---: |
| Purifier | 40.63438 | 41.15660 | 200→690.71846 |
| Hive | 18.28253 | 25.81228 | 200→464.85573 |
| Machine | 2.85755 | 8.22547 | 200→267.27279 |

这三组真实12个月样本未见净电转负。Machine首月余量仅2.85755，不能从一年观察
外推永久非负，后续劳动力／人口／舰队／维护变化仍可能改变预算；本任务不据此
调整区划、赠送资源或增加未授权经济操作。完整六case仍PENDING，四项经济操作
约束仍null，等待root组装动作链／截图／最终日志；不创建18case final-result，
也不宣告整个Mod验收通过。Purifier首次错误FAIL及受限追加更正保持原字节。
