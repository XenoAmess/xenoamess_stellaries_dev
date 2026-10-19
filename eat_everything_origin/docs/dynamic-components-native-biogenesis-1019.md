# 1019 动态真实组件：原生生物舰、生长阶段与突变调查

## 目标、范围与证据标准

用户要求优先广泛研究真实动态组件，只有确认不可行后才接受随机共生强化。本分支只读调查本机 Stellaris 4.5.2 BioGenesis、巨兽与Grand Archive突变系统，寻找对现有固定主宰母舰真实替换组件或增加槽位的接口；不修改Mod、不操作UI、不编辑存档。

重点核对精确游戏自动生成的effects/triggers/scopes文档，以及原生事件、全局设计、船型、生长阶段和mutation组件实例。必须区分脚本effect、固定设计切换、原生设计器行为和普通modifier；不能把后者冒充动态实物组件，也不能把生物舰已存在的能力未经验证套给移动星堡类主宰。

成功候选至少应保持母舰ship/fleet/starbase身份、位置、十移动船坞、建造队列、损伤与已装组件，并在保存/重载后保持新真实组件。调查结论会标明可实测路径、失败条件和未确认边界，不凭CK3语法推测。

## 调查记录

- 本机生成文档（081638Z运行）已发现create_ship.growth_stage参数、ship_growth_stage作用域、add_growth/reset_growth（注明non-fauna ships）、set_ship_design和固定设计create_ship_design。继续读取完整接口与原生实际调用。

## 本机真实接口与实例

### 生长阶段在设计中预定义

`common/global_ship_designs/biogenesis_ship_designs.txt:6` 的NAME_CHARGER_1将三个growth_stages完整写在同一设计中。每阶段都声明ship_size、section模板与全部component；后阶段增加武器/防御槽，也是在对应section模板中预先声明。`common/ship_sizes/00_biogenesis.txt:64` 使用is_bio_ship=yes、bioship_growth_progress_required和upgrades_to串起mauler_stage_1→2→3，主宰原生船型没有这些设置。

081638Z自动生成effects.log给出：

```text
create_ship = { design = <key/target/last_created_design> growth_stage = <1..设计阶段总数> }
set_ship_design = { design = <key/target/last_created_design> }
add_growth = 120
reset_growth = {}
```

create_ship的growth_stage只控制创建时使用已有阶段；set_ship_design支持ship/fleet但没有section、component或growth_stage写参数；create_ship_design也只有预定义design和可选ftl国家。add_growth/reset_growth支持ship/fleet且注明non-fauna ships。原生 `events/biogenesis_crisis_events.txt:476` 的巨兽抵达蛋后add_growth=50，:2100从owner.growth_factor_ship_size_variable增加成长，均不接受任意新组件。

scopes.log:378的ship_growth_stage从ship进入当前设计阶段；triggers.log的has_component支持ship/ship_growth_stage，bioship_can_grow和is_growth_complete支持ship。这些是读取/成长能力，文档中未找到add/remove/change_ship_component、write_section、add_slot、set_growth_stage或add_mutation类通用effect。不能把“存在scope”当作可写设计树。

对母舰的含义：预定义若干同船型设计再set_ship_design，是可研究的真实硬件切换；不能凭生物舰实例宣称能在已有主宰上任意增槽或无限组合。将主宰改成生物舰/巨兽船型还会触及shipclass_starbase与移动星堡/队列/船坞，当前证据不足以保持用户要求的十船坞，不能贸然换底盘。

### 巨兽“突变”的两种实现必须分开

`events/biogenesis_crisis_events.txt:2317`和:2358的跃迁/隐形选项，实际对现有behemoth_04调用set_ship_design，分别选择NAME_Behemoth_04_jump或NAME_Behemoth_04_cloaking；`inline_scripts/ship_components/behemoth_stage_2_mutations.txt`的原生注释也明确说通过切换设计添加。这是固定设计变体的真实组件变化，有实物路径，但没有动态拼装参数。

其余众多巨兽奖励仅set_country_flag。`component_templates/00_biogenesis_crisis_components.txt` 的SHIP_BEHEMOTH_GROWTH加载若干inline_script提供scripted_action，而相关国家flags开启动作或被其它预写数据读取。它们不能一概被描述成“随机安装了新组件”。

### Grand Archive突变有真实组件，槽也预先固定

`common/mutations/mutations.txt`每个mutation把small/medium/large/extra_large映射到现有ship_components键，upgrades_to连接既有级别。`ship_sizes/26_grand_archive.txt:41`的voidworms_small声明mutation_components_size=small、is_space_fauna_ship=yes以及mid/mutations两个section_slots；后阶段改为其它尺寸。`section_templates/grand_archive.txt:352`的mutation_section明确compatible_with_all_ship_sizes=yes，但ANY_1..ANY_6是六个预写的invisible_any槽，不是运行时无限增槽。

原生mutation设计器因此确实装真实组件，但目前未发现把该设计器操作直接暴露为给任意ship/fleet改mutation的effect。把mutation_section加到主宰，也要先修改固定设计/船型插槽并迁移，不能只调用一个未存在的“添加突变”命令。`component_templates/01_mutation_utilities_components.txt:1692`的古代护盾组件还使用triggered_ship_design_modifier，按FROM国家的AP改变护盾，证明“组件身份固定但组件实际属性可条件变化”是原生能力。

## 更适合现母舰的真实组件增效接口

本机 `component_templates/000_documentation.txt:18` 明确triggered_ship_modifier像其它triggered modifiers一样使用，运行在ship scope，且不在设计器中展示；:24的triggered_ship_design_modifier则在design scope、FROM=country并可在设计器显示。

有两个本机真实实物组件例：

- `00_utilities_aux_first_contact.txt:46`起的隐形组件使用triggered_ship_modifier，以is_cloaked即时决定ship_shield_reduction。
- `00_biogenesis_utilities.txt:673/762/851`的生物古代装甲以has_armor_percentage决定实际ship_armor_regen_add_static。

因此可以研究“预装真实组件，组件内部依据等级提供动态船体效果”，与额外挂add_modifier有区别：安装槽/组件key必须在原生设计和SAV真实存在，效果来自该组件定义。该方案并不声称运行时增加新槽或改变组件key；若最终使用，用户文案须准确说“每5级随机升级一个已装核心的等级”。

### mult与script value的证据强度

[官方开发日志253](https://steamcommunity.com/games/281990/announcements/detail/3177863179089175205)（2022-05-05，已通过官方Steam新闻正文核对）说明triggered modifier支持mult引用modifier或script value。本机通用原生实例包括 `buildings/23_shroud_buildings.txt:1096` 的直接属性字段配 `mult = value:psionic_workforce_from_telepaths`，以及 `19_cosmic_storm_buildings.txt:433` 的nested modifier配script value倍率。组件文档说按其它triggered modifiers使用，因此组合到组件是有依据的待验假设。

目前没有找到本机component的triggered_ship_modifier块内直接mult的实例。`00_utilities_aux_grand_archive.txt:21`虽然有mult=value:num_gravity_snare_upgrade_unlocked，但它在cost块，不能作为船体属性倍率证据。也不能把通用mult支持直接当作移动星堡类母舰已经通过。

成长负责人随后找到并已独立核对的[巨构作者原始源码](https://github.com/Pouchkinn-s-Gigastructures/Gigastructures/blob/436812fb3acd9dc7d6cb5e666268a3a1d8135aa7/common/component_templates/giga_eawaf_components.txt#L28)提供更直接的外部实物例：固定commit `436812fb3acd9dc7d6cb5e666268a3a1d8135aa7` 的GIGA_EAWAF_DISENCHANTER_1组件，在triggered_ship_modifier中直接用mult读取event_target国家变量，2/3/4级同样使用。它弥补“组件块内部mult”实例缺口，但属于作者Mod源码，不能冒充本机原版或本次主宰实测，也不需要复制其组件/修正内容。

本机 `script_values/00_script_values.txt:1-61`明确以value:名称调用、base默认0、运算右值支持作用域变量，并示范先用is_variable_set护栏才读取owner变量；`06_script_values_biogenesis.txt:558`实际add=owner.growth_factor_variable，:593实际mult=owner.growth_factor_ship_size_variable。ship→fleet作用域在本次scopes.log:58有记录。因此读取母舰fleet等级可以采用以下待验形式：

```text
eep_probe_component_tier = {
    base = 0
    modifier = {
        add = fleet.eep_probe_component_tier
        fleet = { is_variable_set = eep_probe_component_tier }
    }
}
```

组件triggered_ship_modifier保持原生直接属性字段，倍率使用mult=value:eep_probe_component_tier。ship scope读fleet，避免在design scope错误假定存在fleet。先检验0→1→2及重载、回退到0、移除组件负例；尤其确认变量变化是否及时刷新属性缓存。仅SAV里保存了tier或组件列表不能宣称效果生效。

主线程已通知成长负责人先实现最小护盾探针；本分支未改其独占文件。若成立，可考虑在保留遗迹级5常规aux的基础上另加6个预装零级专属核心，以六个持久tier随机升级，既保持真实组件来源，又不需要无限静态设计组合。这里是待验候选，未宣布通过或替代用户要求。

## 官方上下文与结论

[官方BioGenesis开发日志377](https://steamcommunity.com/games/281990/announcements/detail/502820742193217628)（2025-03-27，官方Steam新闻正文可访问）说明所有已研究生长阶段在单个设计中配置，达到成长量后切换下一阶段；这与本机固定growth_stages源码一致。[官方发布说明](https://www.paradoxinteractive.com/media/press-releases/paradox-interactive/biogenesis-expansion-and-free-4-0-phoenix-update-available-now-for-stellaris)确认BioGenesis包含生物舰和巨兽危机，但不是任意组件编辑API承诺。论坛377原链接本次抓取受限，未以社区转载代替技术证据。

当前优先级是：首先实测真正已装组件的triggered_ship_modifier+mult增效；其次保留预定义设计变体切换这条真实替换路径。生物舰、巨兽和mutation配置尚未提供对固定主宰任意改件/无限增槽的通用脚本effect证据，但这不等于所有真实硬件方案不可行。只读调查没有为随机普通modifier方案下“唯一可行”结论。

## 后续验收要求

1. 准备只含一个专属护盾硬件件的冻结候选，先通过open_kaishek；组件真实出现在ship design/implementation及原生UI。
2. 在固定母舰保持C/进化L不变时设置组件tier0/1/2，逐日保存观察护盾最大值变化；既有舰队/国家修正完整保留，用额外修正百分点计算预期，不错误要求面板相对增幅正好10%。
3. 负例要求同country其它舰船、其它country与不装该组件的设计不获效；回退0和移除件后该组件增益消失，无独立timed_modifier充当效果来源。
4. 原生保存/重载后tier、装件、实效一致；ship/fleet/starbase身份、名称、位置、队列、损伤与十船坞保持。升级只影响这个硬件来源，不授全帝国科技，不覆盖原生组件。
5. 若扩六核心，每5等级实际随机升级一次，持久发放收据；同日重复同步、跳级、载入、母舰损毁均不得重发。界面报告每核心等级与累计已发次数，并准确陈述是预装组件升级，不写成运行时无限新增槽。
