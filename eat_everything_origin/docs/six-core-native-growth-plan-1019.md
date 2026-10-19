# RC3六核心：最少原生全频道成长探针

## 目标与范围

在冻结RC3、Machine政体、绑定Mother fleet159／ship997的独立功能分支上验证C派生等级、真实组件随机tier、属性增量、重复同步、重载与超预算补差。主线程独占UI；本文只给经本机原生文档核对的命令和预先固定判据，不改Mod，不读未来自然成长SAV，不改写v1／v2源预期或既有证据。

实际判据采用 [v2源适用说明](evidence/1019-analysis/six-core-source-expectations-v2.json) 的独立C0截距＋固定增量，来源系数不随未来结果修改。机器政体已知伤害来源小计4.05仍不是完整实际aggregate，供能来源是否全数包含在ship导出中由C0记录，不倒算未来随机tier。

## 已证API与避免的无效命令

- `export_modifier_to_variable` 在本机effects.log:549-551支持ship scope；本轮shield硬件已实际导出成功。十个字段均为本机modifiers.log中的准确键。
- `export_trigger_value_to_variable` 在effects.log:557-564支持ship；原版 `events/grand_archive_events.txt:7940-7946` 实际用 `has_max_hp` 与 `has_max_armor_hp` 导出最大舰体／装甲，triggers.log:1220-1226也列为ship trigger。
- 当前catalog没有 `has_max_shield_hp`，不能照命名规律臆造。最大护盾直接读本次保存的原生ship `max_shield`，它也是硬件0／1／2已用的实际来源。`has_shield_hp`只表示当前盾，不能冒充最大盾；不额外加入当前盾除百分比的未实测组合。
- `every_owned_ship`在本机支持fleet，`every_ship`不是本轮可用迭代接口。tier本身已是原生fleet持久变量；需要在同一个ship诊断快照中复制时，使用原生 `set_variable` 的 `fleet.variable` 右值，不发任何奖励或modifier。
- tracking／damage／固定regen导出的是实际ship modifier总量，不是每门武器最终tracking、面板DPS或本日实际治疗HP；这些不同语义没有一个已证单数API可以互换。

## 每个C节点只需两条控制台命令

第一条在country scope设置受控C并调用实际生产同步一次，将X替换为本节点整数：

```text
effect set_variable = { which = eep_c value = X } eep_sync_mothership = yes
```

之后正常推进至少六个游戏日并重新暂停；不要把一天无变化判失败。第二条只做诊断导出，不再次sync，以免预算节点消化待发量：

```text
effect event_target:eep_mothership@this = { every_owned_ship = { export_modifier_to_variable = { modifier = ship_hull_add variable = eep_probe_ship_hull_add } export_modifier_to_variable = { modifier = ship_hull_mult variable = eep_probe_ship_hull_mult } export_modifier_to_variable = { modifier = ship_armor_add variable = eep_probe_ship_armor_add } export_modifier_to_variable = { modifier = ship_armor_mult variable = eep_probe_ship_armor_mult } export_modifier_to_variable = { modifier = ship_shield_add variable = eep_probe_ship_shield_add } export_modifier_to_variable = { modifier = ship_shield_mult variable = eep_probe_ship_shield_mult } export_modifier_to_variable = { modifier = ship_weapon_damage variable = eep_probe_ship_weapon_damage } export_modifier_to_variable = { modifier = ship_tracking_add variable = eep_probe_ship_tracking_add } export_modifier_to_variable = { modifier = ship_hull_regen_add_static variable = eep_probe_ship_hull_regen_add_static } export_modifier_to_variable = { modifier = ship_armor_regen_add_static variable = eep_probe_ship_armor_regen_add_static } } }
```

立刻同日用原生UI保存，抽取ship997上述十变量、native最大三防和fleet159持久tier。保存本身不需要额外命令；不调用未经支持的console save。

如果希望一次把最大H/A和六tier也复制进ship诊断变量，可将下列片段加入第二条的同一个 `every_owned_ship` 块；这些是可选冗余记录，最少方案直接从同份SAV读取native最大值与fleet tier即可：

```text
export_trigger_value_to_variable = { trigger = has_max_hp variable = eep_probe_max_hull }
export_trigger_value_to_variable = { trigger = has_max_armor_hp variable = eep_probe_max_armor }
set_variable = { which = eep_probe_shield_tier value = fleet.eep_component_shield_level }
set_variable = { which = eep_probe_armor_tier value = fleet.eep_component_armor_level }
set_variable = { which = eep_probe_hull_tier value = fleet.eep_component_hull_level }
set_variable = { which = eep_probe_damage_tier value = fleet.eep_component_damage_level }
set_variable = { which = eep_probe_tracking_tier value = fleet.eep_component_tracking_level }
set_variable = { which = eep_probe_regen_tier value = fleet.eep_component_regen_level }
```

可选片段使用已证接口组合，但本子任务没有替主线程执行；若实际引擎拒绝，保留失败命令与日志，使用原生SAV字段，不把复制失败当组件失败。

## 最少节点与事先固定计数预期

从干净C0开始单调增加，绝不从C10000降回0继续当自然分布样本。

| C | L=floor(C/10) | 应得B | 本次新增抽取（从前一节点） | 完成后R／P |
| --- | --- | --- | --- | --- |
| 0 | 0 | 0 | 0 | 0／0 |
| 9 | 0 | 0 | 0 | 0／0 |
| 10 | 1 | 0 | 0 | 0／0 |
| 49 | 4 | 0 | 0 | 0／0 |
| 50 | 5 | 1 | 1 | 1／0 |
| 200 | 20 | 4 | 3 | 4／0 |
| 10000 | 1000 | 200 | 196 | 200／0 |
| 20500，第一次sync | 2050 | 410 | 200 | 400／10 |
| 20500，后续一次sync | 2050 | 410 | 10 | 410／0 |

每份自然样本都要求六tier非负整数、R为六tier之和、country镜像与fleet真实值相同、snapshot_state=0、临时工作预算变量已清除；此表不指定随机分布。用实际SAV六tier代入公式，不从属性倒算tier。C10000／20500证明没有总200或L20上限。

## 属性固定增量与C0截距

记Nh／Na／Ns／Nd／Nt／Nr分别为真实hull／armor／shield／damage／tracking／regen层数。基线C0须确认L0=0且六tier为0，并记录真实H0、A0、S0、D0、T0、RH0、RA0；这些是当前同舰同国的原生对照，不强填3.8或4.05。

| 实际观测量 | 相对C0的固定预测 |
| --- | --- |
| max hull | H0＋1500L＋3000Nh |
| max armor | A0＋1287L＋2574Na |
| max shield | S0＋2091.375L＋4182.75Ns |
| ship_weapon_damage | D0＋0.05L＋0.05Nd |
| ship_tracking_add | T0＋3Nt |
| ship_hull_regen_add_static | RH0＋0.1L＋0.2Nr |
| ship_armor_regen_add_static | RA0＋0.1L＋0.2Nr |

十字段另核船体flat add保持原始来源-70000，armor／shield出现新的非零ship flat add时必须核查模型适用性；三个mult增量分别是0.05L加对应0.10核心tier。实际装备、反应堆、帝国政体、科技／领袖／临时修正必须稳定或有独立来源说明。发生外部变化时保留差异，不按未来数据调整L／tier系数。原生小数按既有检查器明确的数值容差判定，不临时改阈值来消除失败。

AUTO_REPAIR的百分比regen不能填进两个固定regen字段；满血导致本日未治疗也不能否定fixed modifier。若某类tier一直0，只能确认其零层行为，该类非零核心贡献仍未覆盖；不可仅因抽取总数大就声称六类全测。

## 仅增加必要的幂等、预算和月度检查

1. C50完成并导出保存后，暂停同日再执行 `effect eep_sync_mothership = yes`，重新导出保存；R、六tier、十字段、设计体、唯一成长modifier倍率均应保持。随后对该档同日原生重载、导出保存，限定业务字段仍应一致；严格全档差异单列，不能因已知设计ID重编号而写全量PASS。
2. C20500第一次sync后先不等六日，立即保存一份计数快照，固定R400／P10。此刻核心触发修正可能尚未刷新，不用它判属性。必须在可能的月度自动sync前保留该快照，否则无法证明单次200预算。
3. 最少自动路径是保留P10让既有下一次月度sync自然补完，记录补完时日期，之后再至少等六日导出保存；应R410／P0且六tier总增量10。若为减少等待改为同日手动sync第二次，也可证明可继续补差，但须明确这是手动路径，不能冒称月度补差已经实测。
4. 待P0后重复sync／重载都不得新增tier。观察实际设计仍各装一个六核心，无六类普通奖励modifier；基础成长只保留唯一 `eep_mothership_evolution`（L0不挂，L>0倍率L）。Mother身份／归属、普通控制舰三防和有关修正同样检查。

所有节点保存原生SAV、原始输入动作、日期与SHA；异常或无导出原样保留。该计划尚未执行，不是运行时通过声明，也不复用此前C0人工shield1／2、R0的不自然硬件档作为此自然抽取基线。
