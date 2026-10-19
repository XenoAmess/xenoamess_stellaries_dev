# RC6实际母舰：来源推导供电余额与维护UI范围

## 目标、范围与方法（先于计算）

主线程确认真正post-tutorial的actual open_designer hover/click后仍为同一详情页，没有进入editor，也没有hover解释；不把先前被弹窗遮挡的动作混作该结果。用户需求是配置好母舰；现有自订UI方法未提供供电数值，现改为独立核对**实际原生ship所引用完整inventory的source-derived power balance**。这不是UI供电实测、不改Mod或门禁boolean、不预填PASS。

只读本RC6原生`r6puyearui.sav`、receipt/manifest及绑定的50slots+6required当前design，逐件定位精确原版/Mod组件定义和实际引擎固定CSV数值源。保留power正负语义、默认/变量/覆盖及CSV/TXT差别，不猜未加载CSV或省略值。对全部真实组件求产生/消耗，并核实际country/fleet/ship、已激活科技/特质/传统/修正的reactor power通道。若数值、加载优先级或修正无法确定，保留未知，不能用静态和式冒充严格非负证明。

新报告拟写`docs/evidence/1019-rc6-power-source/power-inventory-report-v1.json`，保留原生SAV/date/fullSHA、当前ship/fleet/design、逐槽来源/行/SHA、合计、修正来源与限制。只写新文档/报告，不操作UI/Git/生产/SAV，不改写既有RC4报告。

## 验收判据

- inventory以该SAV实际ship的ship_design_implementation为起点，不只读取全局预设或实体section；50槽和6required逐项无遗漏。
- 每个power输入有明确来源和符号语义；正发电、负耗电，CSV按实际表头的`power`列解释，未知默认/变量不补0。
- 所有相关power modifier通道有实际状态与源绑定，明确哪些原生组合公式可证明、哪些仍未知；结论使用“实际配置的来源推导余额”，和UI观测区分。
- 不把维护的每月资源支付与组件供电混为一谈，维护tooltip只适用实际当日/政体/海容条件。

## 主线程已观察的UI范围

run `20261019T150008Z`、2201.01.01，Purifier分支经济12/12已封存，yearUI原生档是C0基准。真正post-tutorial详情为50设计；`r6pu-verified-designer-hover`加实际click后的`r6pu-verified-designer-result`仍在detail，无editor/无hover原因。这只说明该次实际入口未给供电，未推断按钮一定灰或底层任何设计器均不可用。

同run的`r6pu-ship-maintenance-hover.jpg`由主线程FreshGPU视觉确认：实际白绮的裁决、owner EEP04种族洁癖，tooltip维护能量10.07/月、合金2.88/月，HP93960/A44787/S167310、军力173149，海容115/66、日期2201.01.01。对应hover.action.json记录client(115,700)，图/OCR与yearUI/receipt由原始SHA绑定。该数值仅作此实际状态维护观测，不推广为其它政体、其它日期或基础组件维护。

主线程已转入Hive，作者不会竞争桌面或要求返回Purifier补UI；本页后续只读计算。来源报告完成后补全实际哈希与是否能严格证明非负的结论，不据已有源码预设结果。

## 已完成的来源推导

实际配置的**source-derived power balance为+9743**：发电14300，消耗4557。该结论在本次绑定的原生组件合同、精确配置及源文件范围内严格为正；不是UI供电数值、不是引擎getter导出值，也没有填入发布门禁boolean。完整56件全部存在明确的TXT或原生固定CSV的power输入，无省略值补0。

原生`r6puyearui.sav`完整SHA256为`79c49aaae6660f341c7f3e08751a415405e44c4d139d465367a8b07870b393b0`，date2201.01.01。从实际fleet150→唯一ship1077→`ship_design_implementation.design=1918`→growth_stage0读取，结果为juggernaut的50个唯一槽加6个required组件。不是从全局预设推测当前设计。manifest绑定RC6树`cc181c8a27ede295e9fcebeffc5e10bb75e9cd643edec1d194b928993ffab33a`、唯一启用EEP Mod、简体中文及精确EXE；59个复制包文件逐件匹配manifest哈希。

| 实际组件 | 件数 | 每件signed power | 合计 |
| --- | ---: | ---: | ---: |
| TITAN_LASER | 1 | -500 | -500 |
| LARGE_PLASMA_3 | 7 | -107 | -749 |
| SMALL_DISRUPTOR_3 | 2 | -17 | -34 |
| SMALL_PLASMA_3 | 3 | -23 | -69 |
| POINT_DEFENCE_3 | 3 | -10 | -30 |
| LARGE_ARMOR_5 | 11 | 0 | 0 |
| LARGE_DARK_MATTER_DEFLECTOR | 11 | -220 | -2420 |
| SHIELD_BOOSTER | 3 | -20 | -60 |
| AUTO_REPAIR | 2 | -10 | -20 |
| 六个EEP_ADAPTIVE核心（各一个） | 6 | 0 | 0 |
| EEP_PLANET_KILLER_DEVOURER | 1 | 0 | 0 |
| JUGGERNAUT_DARK_MATTER_REACTOR（required） | 1 | +14300 | +14300 |
| SENSOR_4（required） | 1 | -20 | -20 |
| JUMP_DRIVE_1（required） | 1 | -30 | -30 |
| COMBAT_COMPUTER_LINE_SAPIENT（required） | 1 | -25 | -25 |
| COLOSSUS_SHIP_THRUSTER_5（required） | 1 | -600 | -600 |
| SHIP_AURA_INSPIRING_PRESENCE（required） | 1 | 0 | 0 |
| **56件合计** | **56** | | **+9743** |

符号合同来自本机`common/component_templates/000_documentation.txt:10`：负值耗电、正值发电。五种普通武器模板未另写power，逐键绑定引擎专名`weapon_components.csv`的第3列`power`，实际行号为85/48/54/46/96；不是cost列，也不是把任意独立CSV视作已载入。该专名路径还在精确EXE的文件offset37569608直接存在，边界仍是来源绑定而非反汇编证明。专属EEP武器使用已明确的TXT `power=0`，不依赖独立CSV。

反应堆`@juggernaut_reactor_power_6=14300`和暗物质盾`@power_L6=-220`分别来自原生`02_scripted_variables_component_cost.txt:565/:337`；其余required的同名`@power3/@power4`按各文件本地变量分别解析，不能跨文件混用：sensor4=-20、jump4=-30、computer3=-25。推力器本地`@colossus_power_5=-600`。所有明确0也保留其真实TXT定义。

## power修正与适用范围

本run generated `modifiers.log:110-111`列出的舰船供电通道是`ship_reactor_power_add`和`ship_reactor_power_mult`。对本机原生安装及绑定的复制Mod的全部TXT检索，合计27个赋值：3个未装备的REACTOR_BOOSTER和24个其它ship_size的正乘数；没有该juggernaut或本舰56件组件的适用赋值，也没有科技/特质/传统/国民理念/政策/光环/定时修正定义中的供电通道。

实际SAV再核country0只有`game_start`定时修正、fleet150只有`eep_mothership`，ship1077没有定时修正；实际aura cache仅`ship_fire_rate_mult=0.05`及`ships_logistics_mult=-0.75`，system1无storm。对应原版juggernaut和Mod的section/static modifier也没有power修正。源目录的全部27个声明都保留具体归属、行号和源SHA，因此无需猜非零add/mult的叠加公式：本配置只需56件signed power直接相加。

这严格证明**该实际配置在绑定公开来源合同下的余量为正**。未声称读取引擎内部供电缓存、反汇编加载控制流或穷尽未公开引擎代码。未发现公共实际单舰excess-power/upkeep getter；维护资源账与此处组件供电分开。若将来更换EXE、源文件、装备、适用修正或实际设计，不能沿用本数值。

## 证据与复算

- [逐槽JSON报告](evidence/1019-rc6-power-source/power-inventory-report-v1.json)，SHA256 `c6b12cab88a719d0b41e3c14d7adf24d337d97c5d2c7dda40b88b065afde4c5b`，status为`SOURCE_DERIVED_NOT_UI_MEASURED`，没有候选验收PASS/boolean。
- [实际design1918原文摘录](evidence/1019-rc6-power-source/actual-design-1918.txt)及[实际scope状态摘录](evidence/1019-rc6-power-source/actual-native-state-excerpts.txt)。JSON内含其全SHA及26份原字节source副本的相对路径/原始绝对路径/字节数/SHA、组件行号/变量来源/CSV原行、完整56行inventory与分组和式。
- [只读复算脚本](evidence/1019-rc6-power-source/collect_power_inventory.py)只读已有SAV和绑定源，写自己的报告目录，不import运行时模块或调用UI。执行命令：`python eat_everything_origin/docs/evidence/1019-rc6-power-source/collect_power_inventory.py`。26份归档源已逐件复核SHA一致。

维护UI图`r6pu-ship-maintenance-hover.jpg`原始SHA256为`271617f477016e45fb6241d3f8f52a19ccbfb0a9ca619394d90aa26cde6e1880`；OCR metadata明确Fresh Steam F12 GPU、1024×768、PID30812。配套hover action为2026-10-19T15:40:44.835079+00:00、client(115,700)。图/OCR/action/yearUI/receipt各自完整SHA都在新JSON中，主线程已视觉确认每月能量10.07、合金2.88。维护值仅属实际Purifier分支当日海容115/66，不泛化为其它政体成本；真正posttutorial designer入口仍停在detail的事实保持原样。

本次未改Mod、已有证据、SAV、外部工具或验收门槛，未操作桌面或Git；后续发布证据由主线程统一合入。
