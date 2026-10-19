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

当前所有新路径尚未通过实机，不据此宣布动态组件完成。

## 刷新等待的原生依据

本机4.5.2 `common/defines/00_defines.txt:574` 明确 `TRIGGERED_MODIFIER_UPDATE_DELAY = 5`，注释为每个游戏对象每X日更新条件修正。因此动态核心不能仅推进一天无变化就判失败。安装后先至少5日获得稳定零级基线，各升级步骤至少5日；当前组合夹具计划每步30日，兼顾原生巨像充能记录。原生组件文档又明确triggered_ship_modifier不显示在设计器，验收读取真实舰船最大属性与原生修正总量，不能只凭设计器提示是否出现来判成败。
