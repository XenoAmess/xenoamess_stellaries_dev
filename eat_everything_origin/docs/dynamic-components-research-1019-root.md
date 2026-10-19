# 1019 动态真实组件：扩大检索与试验协调

## 目标、范围与验收

用户在2026-10-19追加：“优先给我研究如何做动态组件。你应该进行更广泛的互联网资料搜索，以及群星原版文件查找。实在不行的话，我接受随机共生强化方案。”因此先扩大原生真实组件方案调查，仅在有效路径均不能满足时使用明确标注为效果的替代机制，不能把此前standalone失败外推为整个引擎不支持。

三条并行线分别负责互联网原始资料与通用接口、本机生物舰/变异/条件组件、星基地模块/建筑装备链；主线程继续独占Windows桌面。代码改动前记录设计，并先通过open_kaishek才启动新候选。真实组件方案须证明组件进入实际设计、组件本身提供属性、随机升级计数真实改变属性、其它舰队不受影响、重载不重复、跨级补差且无总成长上限；单纯保存条目或普通永久modifier不能通过真实组件验收。

## 主线程互联网检索记录

- `Stellaris modding dynamically add components ship set_ship_design add_starbase_component`
- `Stellaris modding ship component variable modifier dynamic ship design runtime`
- `Stellaris Ship Components Created During Game Play`
- `site:forum.paradoxplaza.com Stellaris component variables modding ship`
- `site:github.com Stellaris add_starbase_component`
- `site:github.com Stellaris create_ship_design design`
- `site:forum.paradoxplaza.com Stellaris Dev Diary #253 modifiers mult`
- `triggered_ship_modifier component Stellaris` / `triggered_ship_modifier mult Stellaris`

官方Wiki的 [Ship modding](https://stellaris.paradoxwikis.com/Ship_modding) 与 [Effects](https://stellaris.paradoxwikis.com/Effects) 本次直接访问均返回401，不能声称已阅读全文。检索发现的Fandom/日文/俄文转述只用于定位功能名和版本，不作为技术成立证据。普通开源Mod中的create_ship_design预定义设计实例也不证明可以临时构造任意组件。

## 新的硬件路径

互联网线定位官方DD253的条件修正倍率能力；本机线确认4.5.2 `common/component_templates/000_documentation.txt` 明示triggered_ship_modifier使用ship scope，且原生生物装甲/隐形设备使用该块依舰船实时状态改变属性。因此优先验证“真实装入的组件，以舰队中的等级变量缩放组件本身的属性”。通用条件修正的mult能否在此组件字段中使用，仍是待实机证明的组合，不能仅根据文档推断成功。

最小探针先增加一个专属辅助槽并真实装入零成本、零功耗的动态护盾核心，原有遗迹级5个辅助组件不替换。零级不提供属性；通过原生命令将其所属舰队的专用等级设为1、2，分别观察最大护盾和组件提示，再重载验证。只在功能夹具修改等级，不给生产包加入测试事件，不把受控实验用于自然成长或经济验收。

星基地线另查原版arkship建筑equipped_component与模块重建链。它与已经失败的standalone接口不同，在文档和探针中分开记录；不得未经验证改变母舰底盘、丢失十船坞或替换整艘舰船。

RC3的真实已装组件自身动态倍率路线现已完成一级受控增益观察，详见下文；二级、重载和自然随机发放仍待验证，不宣布整个动态组件功能完成。

## 刷新等待的原生依据

本机4.5.2 `common/defines/00_defines.txt:574` 明确 `TRIGGERED_MODIFIER_UPDATE_DELAY = 5`，注释为每个游戏对象每X日更新条件修正。因此动态核心不能仅推进一天无变化就判失败。安装后先至少5日获得稳定零级基线，各升级步骤至少5日；实际RC3改用每步六日：hw0为2200.01.07，hw1为01.13，hw2再六日。此前每步30日是早期组合夹具计划，非本轮已执行步长。原生组件文档又明确triggered_ship_modifier不显示在设计器，验收读取真实舰船最大属性与原生修正总量，不能只凭设计器提示是否出现来判成败。

## RC3一级动态硬件观察与分层来源

冻结生产树SHA `178d3021fa53dd999b5537e1e58f7b59c7138232e7a7fe4fe53327b3dff8e116`，36P／131键／CSV／3派生回调门禁PASS；开发检查点 `2e020d137`。主线程机器开局受控夹具中C0／L0／R0，仅shield核心层数由0设为1，其它五类仍0；六日后最大盾由167310变171492.75，差4182.75。ship导出script value=1、ship_shield_mult=3.1，无新增普通奖励modifier或控制舰属性变化。该档为硬件隔离实验，R0而tier1是刻意设置，不能套用自然随机抽取R=sumN的不变量。二级与same-day reload尚待独立结果。

诊断曾误用 `every_ship` 未获有效导出，已纠正为本机文档支持的Mother fleet内 `every_owned_ship`，再在实际ship scope调用set_variable／export_modifier_to_variable。早期无导出不能视为核心值0或组件失败。

分层参数有独立原版来源：组件文档 `000_documentation.txt:12-24` 明确设计修正与实际舰船修正是不同scope；`00_utilities_shields.txt:906-907` 的大暗物质盾用设计层 `modifier.ship_shield_add=@shield_L6`，原版 `scripted_variables/02_scripted_variables_component_cost.txt:389` 定义2925；`00_utilities_aux.txt:99-100` 的SHIELD_BOOSTER在设计层 `modifier` 给+0.1，原设计三件；同文件:439-441的CRADLE_MARK则在 `ship_modifier` 给同一字段+0.10。这是原版自身的分层用例，不依赖事后拟合或社区推测。

基于真实11件盾及三件增幅器，源分层模型为 `11×2925×(1+3×0.1)×(1+ship层ship_shield_mult)`；ship层3.0／3.1分别预测167310／171492.75，与两档观察一致。查看hw2前预测tier2、ship层3.2时最大盾175675.5，仍须独立SAV核验。原始脚本没有公开闭源的完整计算函数，故这属于原始参数／scope加原生实测共同支持的模型；不把数字一致冒充读到引擎源码。更多机制与范围见 [成长组件记录](evolution-components-1019.md)。

## 后续限定结果与最终说明

上述hw1／hw2待验叙述保留调查历史。后续既有RC3硬件v2报告已完成56项限定检查：真实盾167310→171492.75→175675.5，01.19同日重载仍175675.5，六真实AUX核心保存、普通舰三防恒定、没有独立奖励timed_modifier。严格整档重载仍FAIL且57项差异保留；自然RNG与另五类核心不由该报告代替。本次仅只读复核现有报告，没有重跑测试。

可向用户简述的当前结论与已核primary URL／原版行号集中在 [动态组件结论](dynamic-components-conclusions-1019.md)：已找到真实预装组件动态效能路径，尚不承诺任意运行时拼装或无限可见槽位；未来RC4六类自然升级必须按提前声明的矩阵验收。
