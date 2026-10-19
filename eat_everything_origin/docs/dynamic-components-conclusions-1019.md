# 动态组件研究的当前结论与用户说明

## 可直接向用户说明

已经找到真实组件路线：母舰实际装备六个专属AUX核心，升级改变这些组件自身提供的属性。护盾核心已在原生存档中完成0→1→2及同日重载的限定验证，收益真实生效；六类自然随机升级仍须后续RC4成长矩阵确认。方案持续提升既有六核心的等级，不承诺每次升级凭空长出一个新的可见槽位。

此结论不需要将普通永久修正伪装成组件，也没有因为standalone探针失败而宣布整个引擎做不到动态组件。当前实现与原生属性证据支持的是“固定真实装备、动态效能”，不是“运行时任意拼装无限硬件格”。

## 原生接口：存在与未证实分开

本机为Stellaris4.5.2，EXE SHA256 `400df27c82ddc845aa9dce79bd468d81f18f060d299cd263e3afa93aef4f7a83`。下表行号来自本机原始文件，不采用浏览器文本转换后的行号。

| 接口／结构 | 已核原始位置 | 能确认的范围与限制 |
| --- | --- | --- |
| `triggered_ship_modifier` | 游戏 `common/component_templates/000_documentation.txt:18`，与12行design modifier、15行ship modifier、24行triggered design modifier区分 | 真实组件可在ship scope依状态改变属性；不在设计器显示该块并不代表没有效果 |
| 原版即时组件效果 | `00_utilities_aux_first_contact.txt:46-50`；`00_biogenesis_utilities.txt:673/675、762/764、851/853` | 隐形件按is_cloaked改变盾，生物装甲按当前装甲比例触发恢复，证明组件属性不必永久固定 |
| `add_starbase_component`／`remove_starbase_component` | 072723Z `effects.log:2058-2064`，仅starbase scope | 接口真实存在，操作standalone；本轮事件主宰Mother只存入列表，没有取得预期收益，不作为正式组件路径。不能外推所有星基／引擎都无效 |
| `set_ship_design` | 同catalog2575-2580；原版 `events/biogenesis_crisis_events.txt:2317、2358` | 可以在已有ship／fleet切换到预定义设计或设计target；文档没有section／component任意编辑参数，也不凭文档承诺损伤与队列保留 |
| `create_ship_design`／`set_auto_upgrade_components` | 同catalog3240-3242／2644-2646 | 前者从预定义design key创建，后者开启design自动组件升级；不是接受任意组件数组的新设计构造器，也不是任意增槽承诺 |
| `add_growth`／`reset_growth`及growth_stages | 同catalog2935-2941；原版BioGenesis及官方DD377 | 真实生长阶段机制，阶段预先在设计中配置；不是对现有固定主宰任意增加组件／槽位的已证接口 |
| 星基建筑／模块装备链 | catalog1854-1868，原版 `00_arkship_component_buildings.txt`，见已有星基分支研究 | `equipped_component`与模块section链确有原版／作者源码，但本轮Mother上的通用有效性未由该研究证明，不冒称都成功或都不可能 |
| 任意ship添加／移除单件、任意运行时增加可见槽位 | 本轮catalog、原版定义与多条作者源码路径检索 | 未找到满足该语义的通用已证接口；不能把假想的 `add_ship_component` 等名字当成有效effect，也不能把“本次未找到”写成闭源全引擎绝对不存在 |

catalog原始文件为 `C:\Users\1\AppData\Local\xenoamess_stellaries_dev\runs\20261019T072723Z\logs\script_documentation\effects.log`，SHA256 `f7fe1e0b3e5567597db5d39a3f36b847b36cbc2a45fd68935540f9e8bca552df`。组件文档SHA为 `f9c0edfee06c59422609c04030e890afeb824055deeee18507315d8acb875286`；隐形组件SHA `49ce43fd54e1980c87ed6d33b75e9f952dfd75eb8b0534d9ca5c24ddd8c8ed60`，BioGenesis组件SHA `bbffe677f1e9a23ae5a14784c00f9f36175f2277e98b6a89192714c3603d1c9b`。

## 互联网原始来源复核

此前已从官方说明、原版BioGenesis成长设计、星基建筑／模块链、成熟Mod真实组件倍率与固定设计切换等不同路径搜索；详细查询保留在 [广泛研究记录](dynamic-components-research-1019-root.md)、[BioGenesis原生记录](dynamic-components-native-biogenesis-1019.md) 与 [星基分支](dynamic-components-starbase-1019.md)。2026-10-19本轮只读复核以下小范围原始来源，没有重新下载仓库。

- [官方开发日志253](https://steamcommunity.com/games/281990/announcements/detail/3177863179089175205)，2022-05-05，介绍triggered modifier的mult可引用modifier或script value。网页抽取器本轮只返回标题／图片，故通过Steam官方新闻API相同官方公告feed核正文，不用社区转载替代。API查询 `https://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/?appid=281990&count=20&maxlength=0&enddate=1651881600`，公告gid `4348799082189934093`，本次响应SHA `7838f252416ef4799fea040132c176b71a369f5ff3ce72c2c52b6fb967181a2e`。这是通用倍率依据，不单独证明组件／本母舰已生效。
- [官方开发日志377](https://steamcommunity.com/games/281990/announcements/detail/502820742193217628)，2025-03-27，描述生物舰各研究阶段配置在同一设计里，再随成长切换。官方API enddate `1743206400`、相同appid/count，公告gid `1795283637817914`，本次响应SHA `7f14c7dc4e5950a469888da5a7390bb0d4a2b86d4b8dc36c5bfae3777d6f863c`。它不承诺任意动态拼装主宰。
- [Gigastructures作者真实组件源码](https://github.com/Pouchkinn-s-Gigastructures/Gigastructures/blob/436812fb3acd9dc7d6cb5e666268a3a1d8135aa7/common/component_templates/giga_eawaf_components.txt#L30)，固定commit `436812fb3acd9dc7d6cb5e666268a3a1d8135aa7`。原始文件30行起的triggered_ship_modifier在36行通过mult读取event_target国家变量，2／3／4级组件也这样做；实际文件SHA `09fa80d0b3399d4fc90bcebac06a6d29046687b5e5cf38c7192ca05537116133`。这是原作者组件内动态倍率的直接用例，非本机原版、非本项目实机证明。作者descriptor声明v4.5.*，不把该声明冒充本项目兼容验收。

官方Wiki此前401／本轮其他访问Internal Error的限制仍保留；没有以Fandom镜像、普通玩家讨论或CK3方言替代Stellaris原始技术证据。

## 为什么六个核心是真实组件

RC3／RC4均预定义11个AUX格：5个原Relic辅助件保留，新增六格装盾／甲／舰体／伤害／追踪／再生核心。`common/section_templates/eep_mothership.txt:46` 固定aux_utility_slots=11；`common/global_ship_designs/eep_mothership.txt:184-191` 将六个真实template装入AUX6—AUX11。原生hw0／hw1／hw2／reload设计也确实包含这六个slot/template配对，不只是一组报告变量或名称。

各自的 `utility_component_template.triggered_ship_modifier` 读取所属fleet的持久tier，按bound-Mother条件在实际ship scope应用自己的属性。六类核心奖励没有另加普通timed_modifier；原有每级四属性成长与固定恢复的唯一基础成长modifier是另一个来源，必须在自然RNG验收中分离。不能因所有引擎属性最终都通过modifier字段表示，就把真实组件内的属性与独立奖励modifier混为一谈。

本机 `common/defines/00_defines.txt:574` 设置每个对象的triggered modifier五日刷新，SHA `82eebd807eb54af347025b061af2991fc40a1b1059e39c2cb8ee135dca02b7cc`。实机隔离探针各等六日；既不以一天无变化判失败，也不以设计器没有提示判失败。拆件负例没有在该RC3硬件报告里完成，不能另声称已经实测卸件过程；实际装备、组件源码、独立导出、属性变化及无额外奖励modifier组成目前的正面归属证据。

## RC3已完成的限定硬件证据

现有 [RC3硬件v2报告](evidence/1019-analysis/rc3-hardware-case-report-v2.json)，SHA `318604b2a58f6181a030a2c7daf2d563edb92b9e7f27d2ae051e786a17a7134a`，56项限定检查通过。本次只读其现有结论，没有重跑测试或改写历史JSON。C／L／R始终0，仅人工控制护盾核心tier，其它五类0；此为因果隔离夹具，不能套自然RNG的R=sumN判据。

| 原生档 | 日期 | 护盾tier／实际最大盾 | SAV SHA256 |
| --- | --- | --- | --- |
| hw0.sav | 2200.01.07 | 0／167310 | `815aa75e10b3629b42750347f5f30c765e339d01d67637ccfe21cd5e1691a655` |
| hw1.sav | 2200.01.13 | 1／171492.75 | `b342199c7212594db5eb63746835e9670cc41c737eb694e8e6e8773585c76983` |
| hw2.sav | 2200.01.19 | 2／175675.5 | `50d4c00dc4dbbe9422401d138b750295f9dbc633b9c2b1a342cc75a23e3ea3ad` |
| hw2reload.sav | 同日 | 2／175675.5 | `aef3706cd833d7799f67c654cc3ca3abc630d319086b9ea23fffbb00cb20d186` |

一级／二级的真实ship导出分别为script value1／2、ship_shield_mult3.1／3.2；零级未导出相应诊断值，报告明确记录缺失，没有补造0。五艘普通控制舰最大三防恒定且无自适应核心，母舰H／A与国家科技／perk和已有timed modifiers不变。组件每层+0.10是ship修正的百分点增量，不是对当前总盾再乘1.1；设计层三件盾增幅器与ship层分开，因此每层实际增4182.75，不能用错误基数倒逼结果。

结论只限真实护盾核心0／1／2刷新、控制舰与同日重载字段保留；严格整档重载比较仍FAIL、57项差异保留，不能写全档零变化。另五核心、随机抽取、无上限补差及破舰不复活不由这一报告代替验收。

## RC4尚待原生RNG矩阵

未来从同一Machine十二月经济后的干净year1C0进入成长分支；原生Mother IDs自动发现，以实际C0最大三防／十导出为截距。预先固定节点为0／9／10／19／20／49／50／200／10000，之后20500单次200预算留R400／P10，再下一月auto留410／0；六类至少各出现一次非零真实随机tier，分离L与N贡献，检查真实槽位、普通舰三防负对照、重复sync与同日重载，详见 [矩阵预声明](growth-report-1019.md)。固定模型v1／v2在未来SAV前已写，不能看结果再改系数。

本次整理时尚未收到该RC4真实成长receipt，不能把候选六核心或离线检查器测试写成六类自然成长实机通过。等级／抽取不设置人为总上限，单次预算留待后续补发；这仍不等于数学无限精度、无限内存或无限可见槽位。后续只读核验必须保留失败与缺失证据，不提前使用普通永久强化降级方案冒充真实组件。
