# RC4母舰供电／维护的最短取证路径与正式版预检

## 目标、范围与当前结论

主线程已完成同国同日Relic界面参照和实际跃迁；本轮只读定位尚缺的`power_nonnegative`与`upkeep_observed`最短证据，不改门槛、不操作UI／Steam、不建新进度索引，不造普通主宰或生成参照船。今后的成长／经济／迁移可来自同候选的新run，按各自manifest归属记录，不把旧run改名。

已重读phase-A稳定`r4relic6`和`r4jumpedge14`原生ZIP，实际Mother997／fleet159／design1511没有可直接读出的供电余额或单舰维护金额；现有配置页图亦没有这两项。当前不能据SAV给这两个check填true。原生船体／组件配置、供能源码求和与舰队修正可作辅助，不能替代实际显示或实际归属账目。

## 稳定输入

归档为[Relic／跃迁／原版回调包](evidence/1019-rc4-relic-jump-native-control-v1/archive-index.json)，索引SHA `2b984e60d900b13127628ec438885a4d0ee8cbb7b2ad01f9d195db2a4d396438`，verification SHA `23d0238c72ca5d753236e55ae07a1e545f4b4fdc0df015830d01f983a586a215`。本轮只读其副本及已停止run原件，未改变归档。

| 原生档（归档raw目录） | 日期 | SHA256 |
| --- | --- | --- |
| `r4relic6.sav` | 2200.03.13 | b067c749c7389dd830995aa8e1b14bdfae58ab10f8afa67c6cf4004e0ec70f81 |
| `r4jumpedge14.sav` | 2200.03.27 | a76691e76b2bea8fbcbe06072a6be1a1eb546cfcf6fce621e8517dadf1be1db3 |

实际配置图是`raw/r4mother13-verified-details.jpg`及`raw/r4ref13-details.jpg`；`r4mother13-details`是未打开详情的失败全景，不用作数值证据。已有[UI／跃迁限定报告](evidence/1019-analysis/rc4-relic-ui-jump-v1.json) SHA `5e849e167c16057d6f529f74ec0c7d491ebd1e28382844ffb846e17e7de85b64`，其中没有供电或维护金额。

## 原生SAV能证明什么

两份原ZIP的CRC有效；Mother仍是同一ship997／fleet159，实际设计1511。下列原生路径都已检查：

- `ships.997`：有实际三防、设计implementation、光环、坐标、旗标和后来出现的跃迁冷却字段；没有power／upkeep／maintenance标量或嵌套金额。
- `ship_design.1511`：只有名称、is_event_design、growth_stages与完整section／component／required；没有缓存功耗总数或维护总额。
- `fleet.159`：`fleet_stats`仅combat_stats；`military_power`是军力，不能当反应堆能源。没有单舰维护账目。
- `country.0.budget`：current_month／last_month提供实际经济类别总额，没有把ships／ship_components细分到ship997。

两档相同的国家实际类别为：ships能量8.09998／合金3.34999，ship_components能量8.80392／合金1.63622；另有采集站4能量、科研站1、starbases2、starbase_buildings1、starbase_modules1。这些只能声明国家聚合支出。此功能夹具已有Relic参照，海容365／69含参照250，不能据它拆出Mother实际维护，更不能计入新局经济。

本机生成的`triggers.log`未发现可直接导出舰船供电余额或单舰upkeep的numeric trigger。不要猜造`has_ship_power`等命令，也不从`ship_excess_power`源修正或伤害残差反解为“实测电量”。

## 给主线程的最少界面路径

以下是由原生GUI和已存在GPU图确定的入口；未执行的新界面动作全部待实际观察，不能把候选入口写成已经成功显示数值。

1. **维护先尝试一个悬停**：只选实际唯一Mother舰队，悬停其实际舰船行的舰名／舰体图标，核完整tooltip是否有明确“舰船维护费／维护费”及能量、合金等资源。已有1024×768图中该行在底部约`(130,708)`，这只是同布局位置参考，实际新run先看新GPU；避开右侧拆舰按钮。若该tooltip明确给出实舰维护，保留一帧图／OCR、hover动作、同日原生档与实际唯一ship归属即可，不必再等一个月或造对照船。若tooltip只有舰种／军力，不算维护观察；再尝试实际单舰舰队名／图标悬停。原生GUI没有静态写明这些hover由哪个C++构造，故不保证第一处必显示金额。
2. **供电从该实舰打开设计器**：同一实际舰船详情底部有`open_designer`按钮。既有真实Mother详情图中“打开设计器”中心约`(400,603)`，左侧下方不是另造设计入口。点击后必须核标题／实际固定组件仍对应`NAME_EEP_Baiqi_Mothership_1019`，再读右侧“能源”一项并悬停；实际余额须≥0，保留发电／消耗明细若tooltip提供。不新建／自动改装／保存设计，不授科技、不替换组件。
3. **设计器限制如实保留**：此为`is_event_design=yes`、不可升级的固定母舰。若按钮不可用或打开的是普通默认设计，保存该实际失败／限制，不拿另一艘同底盘设计的数值抵用。配置页核心反应堆hover能证明该件供电，但不能单独证明全舰余额；静态sum也只能作源推导。当前尚无已验证的raw备用接口来保证绕过这一限制。

设计器显示维护可能是**设计的预估维护**；即使读到了，也应与实舰／单舰队实际tooltip或明确归属账目区分。`eep_mothership`含ships_upkeep_mult／starbases_upkeep_mult -1，但不能仅据源码写实付为0；4.5组件另有ship_components支出，实际看到什么就报告什么。供电和维护不是同一“能源”概念：前者是组件功耗余额，后者是国家每月支付的资源。

无需为这一动作另开普通juggernaut或spawn Relic。可在下一实际功能run的现成生产母舰暂停时完成；这两个读数不要求再跑一次跃迁。同run的新证据接其本身manifest，旧phase-A截图不改日期或归属。

## 原版界面依据

路径相对`C:/SteamLibrary/steamapps/common/Stellaris`：

| 来源 | 可核内容 |
| --- | --- |
| `interface/ship_view.gui:240`起 | 详情stats逐项是hitpoints／armor／shields／speed／evasion／damage，再是rank／cloaking；未列power／maintenance |
| `interface/ship_view.gui:511`起、`:524`起 | buttons及open_designer；按钮文字SHIP_DESIGNER |
| `interface/fleet_view.gui:236`起 | 单舰subentry的name／icon／inspect；当前截图舰船行与之对应 |
| `interface/ship_designer.gui:45`、`:59`、`:298`起 | first_stat_position、info_mecship_pos和右侧info／content，具体统计行由引擎填充，不能只据GUI猜固定“能源”像素行 |
| `localisation/simp_chinese/main_2_l_simp_chinese.yml:1635`起 | SHIP_STAT_ENERGY_MAINTENENCE为维护费，SHIP_STAT_POWER_USAGE为能源；对应图标、值格式在1655～1678 |
| 同文件`:1697`、`:1699` | 维护解释与能源余额解释分开，负能源设计不能保存的说明属于设计器，不是全局事件创建成功即功耗合格的证明 |
| 同文件`:1906` | SHIP_MAINT_COLON为舰船维护费；只能作为识别实际tooltip的本地化线索 |

主要源SHA：ship_view.gui=`f0f3921c0d9523a9122af59458154a9661c7cc3e0dd5ef91af539f7a67532f34`；ship_designer.gui=`6440681db87175c29ca4428ad393a0f6d18948e859d8a1a77607da865de1119a`；fleet_view.gui=`4ec4caa29edb0dad78db7da606495e979f5fe2407e17c33f833c3bc14648e3ff`；简中main_2=`34af90279d8fbcf373469e6521e0b51d4109ca1ab0c2f713281fe3e778c3c72e`。本机EXE仍为400df27c…f4f7a83，未执行任何新原生命令。

## 正式0.4.0只改元数据的预检顺序仍适用

现工具`validate_candidate_files`只接受候选文件表中descriptor的唯一`version="0.4.0-rc.N"`原字节替换为`version="0.4.0"`；所有其它生产文件路径和SHA必须相同。`candidate_tree`在正式阶段仍用保存的候选descriptor字节重算候选树，原生manifest／静态gate／证据版本保持rc.N，不能改写成正式版。

本轮仅在内存构造descriptor正式替换后的hash字典，原门禁接受；再把events/eep_events.txt hash改为另一值时，原门禁准确拒绝“beyond descriptor version”。工作区VERSION仍0.4.0-rc.4，生产树仍06485dc…7ef468；未真的修改版本或源码。

后续由主线程执行的顺序：

1. 收齐最终候选18case及各新run原生材料、独立报告、最终完整日志；创建经共同审查的final-result。当前progress不是final-result。随机组件使用现有两个归因新字段及实际growth报告；不要把旧固定L字段或PENDING值批量改true。
2. 仅改项目VERSION与descriptor的Mod版本为0.4.0，运行正式包open_kaishek，保存新的正式静态报告；`record-static`记录正式报告／生产文件绑定，旧rc报告与manifest不改。
3. 先完成正式CHANGELOG同版本六类（新增／变更／修复／兼容／验收／已知限制）、工坊文案与新WS06单母星图；其它五图库槽位及四条历史immutable inline URL按既有协议保留，不全删再复用图片。六类验收文字必须保留实际scope／限制。
4. `prepare`派生同entry的`[v0.4.0]` note并冻结acceptance／媒体输入；注意现prepare内含四条inline图的HTTP字节取回核验，不是纯离线命令，应留给主线程最后网络发布窗口。现阶段只读审查，不调用该入口。
5. 正式冻结输入提交并推送，工作树干净后`preflight`；它核正式静态／candidate-only元数据差异、未发布SemVer、3815707212身份、精确note和媒体、HEAD与upstream一致。3710613857继续禁止。
6. 最后上传阶段Steam在线，由主线程publish；独立目录下载远端逐字节核全部文件，公开文案／note／六图库／四inline逐项核验。成功但验证不足不打tag，也不复用成功版本再上传。
7. 验证receipt提交推送后`tag-check`只读门禁通过，再由主线程创建并推送`v0.4.0`，恢复Steam离线。

正式前的check-runtime／record-static和只读hash核对可离线；prepare／publish／download／verify的网络阶段不能现在提前执行。本任务没有执行这些动作，也没有宣称最终发布预检已经通过。原工具相关66项测试已在前一任务通过；本轮没有改工具，不重复测试整套。
