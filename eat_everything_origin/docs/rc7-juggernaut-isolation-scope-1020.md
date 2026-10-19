# RC7其它主宰隔离：原合同与来源范围

## 目标与边界

2026-10-20按root追加任务，只读核`other_juggernauts_unchanged`原发布／checker合同及当前精确RC7源隔离。只新增本页，不改已封口的repeat-init／Relic包、旧接收文档、工具、Mod、SAV或Git；不操作UI，不读取当前jump或活动日志，不增加实舰测试矩阵。

结论：**现有合同没有规定这一项必须生成另一艘普通主宰；当前来源证据足以形成“未全局覆盖普通主宰，专属装配／基线／成长作用域限定母舰”的SOURCE_SCOPED结论。不能把它写成已经观察到另一艘普通主宰的运行时负对照，也不能声称所有友舰数值永不受原生光环影响。** root可据此在后续新分析／最终共同审查中处理该项，旧partial提案的null保持原字节。

## 原代码确实要求了什么

[publish_1019.py](../tools/publish_1019.py)的`CASE_CHECKS`在`mothership_configuration`列出`other_juggernauts_unchanged`；`validate_runtime_index`逐组要求status、精确tree／run、所有所列check为true，以及整组真实native_save／screenshot／actions／log／analysis五类引用。该项没有专门的other-juggernaut存档角色、特定设计名、实舰数、前后pair或附加typed合同。它与组件归因／旧档迁移的专门验证函数不同。

这不是“boolean门槛就能代替证据”：仍须真实来源支持所声明结论。本页补的是精确的来源隔离证明，配置组其它需要运行时的UI／真实jump等要求照旧，不因本项来源范围而免除。

[check_1019.py](../tools/check_1019.py)的`mother()`原14项检查只覆盖候选版本、Mother唯一舰队／独船／全局绑定、实际设计名与配置、Relic装备、PK、required推进／传感／计算机、三防最低值及10yard；**没有`no_global`、`other_juggernauts_unchanged`或普通主宰负对照检查**。其14／14不能被当成已经自动证明本项。

[功能receiver设计](rc7-functional-offline-receiver-1019.md)曾把“其它主宰负对照”列作母舰checker范围之外；这是尚需独立论据的提醒，没有规定必须临时生成另一艘实舰。本页用原版定义／专属作用域的来源对照填补这个论据，明确限于来源范围。

本次核查的发布工具SHA为`06c60c0a9bd406580314999ae6649365bb5c1fa6c7152c0b0a7fb5a420e06918`，原checker SHA为`681836d2da9c6b28ee9bfd583c87e5ced96f06543901e71d3dc35fa226f3afdc`。代码未改。

## 精确RC7来源证明

候选仍为0.4.0-rc.7、59文件树`61b34f6dbdc277c44364889d5f1e1cd2773a4624786bbf0d538079fc6ba4feb0`。以下来源均已在原RC7 static／growth／供电canonical中封存，本页仅读并核当前SHA：

| 论据 | 已核内容 |
| --- | --- |
| 原版普通juggernaut船体未被替换 | 冻结59文件manifest没有`common/ship_sizes/`下任何文件；存在的空目录不是定义。descriptor无`replace_path`。原版`common/ship_sizes/18_juggernauts.txt`当前SHA=`3402b13978de2bbcc36c6d4eedab9e4a9ac7f5160183fa2b908029f10842f11f`，与[已封存原版源](evidence/1019-rc6-power-source/source/native/common/ship_sizes/18_juggernauts.txt)同字节。 |
| 独立section／global design | 新key为`eep_mothership_section_1019`、新设计名`NAME_EEP_Baiqi_Mothership_1019`；没有覆盖原版普通主宰section／设计键。Mod设计仅引用该专属section；不能把自订section存在本身说成改写了所有juggernaut。 |
| 基线只给创建的Mother fleet | `eep_startup_mothership`在专属create_fleet.effect中给该新舰队一次`eep_mothership`修正，并保存`eep_mothership@root`；没有按ship_size遍历全国普通主宰授基线。 |
| 设计迁移只选已绑定Mother | `eep_repair_existing_mothership_design`要求已初始化、绑定舰队存在／owner正确／num_ships=1／juggernaut；其`every_owned_ship`另要求`fleet.is_same_value=event_target:eep_mothership@owner`，才执行`set_ship_design`。不能只看外层`every_owned_ship`就误读为换掉所有主宰。 |
| 每级成长只更新绑定Mother | `eep_sync_mothership`验证同一绑定／归属／独船／juggernaut，然后进入该event_target，替换`eep_mothership_evolution`及同步真实组件；没有country级该舰防御／伤害成长修正。 |
| 六真实组件再次限制绑定Mother | 六`EEP_ADAPTIVE_*_CORE`虽为实际组件，其`triggered_ship_modifier.potential`均要求当前fleet等于`eep_mothership@owner`。装备逻辑和效果逻辑各有隔离，不会仅因country有相同tier镜像就给其它普通舰生效。 |
| 实机观察范围明确 | 本轮Jan7原生完整growth-stage解析后，全表只有ship1044是juggernaut；Relic ship1068是npc_warship_01。原native／UI配置实际证明了Mother／Relic，没有产生或观察普通juggernaut样本。 |

本轮源文件完整SHA：

- `common/scripted_effects/eep_mothership_effects.txt`：`f704c30ea845d57dbad5bcb6c60ec657d5ae8d4ab6a55082055dccb38d7d5ec1`。
- `common/scripted_effects/eep_startup_effects.txt`：`f3a0fb725b1ea7f9cb4f77a7225a30e7b83acb86bbd4ba496b91860ddbcbb697`。
- `common/component_templates/eep_evolution_components.txt`：`490b9711e77709bfeb0bd7bccba6373b4385c0fff118cedc95def2362ac78b26`。
- `common/section_templates/eep_mothership.txt`：`a45774b96c4dc8efd99d538b809a7c6f7152e4ab67852553926a7a6f2fb46493`。
- `common/global_ship_designs/eep_mothership.txt`：`0e1bc46c7d1d534e0a9d3619cef1d93e366ddc7d5a4d2fde766b0ca111929123`。
- `common/static_modifiers/eep_modifiers.txt`：`a5fd09db86cf418fb0a95f0d28fb8347003c9fd513e64d8d90ced067ddc2129d`。
- `descriptor.mod`：`88d02ca3d6d8ba249a6a76a8ddec2a6033e86dc026cb7e58af9f9234206fd359`。

来源文件相对当前`mod/`，对应冻结副本见`docs/evidence/1019-rc7-static/candidate-rc7/mod/`；本页不重复复制。原版船体SHA只证明该精确源未变；不外推所有引擎内部行为或多Mod组合。

## 必须保留的光环边界

“专属基线／成长隔离”不等于“任何加成都只影响Mother”。Mother保留了原生`SHIP_AURA_INSPIRING_PRESENCE`；本轮Relic实际hover已显示“来自白绮的裁决：舰船武器射速+5%”。友舰仍按原版光环规则获益，这是预期的原生作用范围，不应为了负对照而去掉光环或断言其不存在。

同样，实际tooltip“舰船后勤维护费−75%”与EEP源码`ships_upkeep_mult=-1`不是同一修正通道；本项不授予免维护结论，不改已核实的Mother实际10.07电／2.88合金。

建议后续单项结论写为：

> `other_juggernauts_unchanged=true`，范围SOURCE_SCOPED：原版juggernaut船体／普通设计未被全局覆盖；EEP专属装配、基线与成长只作用于已绑定Mother。没有普通juggernaut实舰负对照；保留的原生友军光环仍正常影响范围内友舰。

这是一项新增、可引用的范围判定，不回写旧partial提案，也不是整配置case通过。整个case仍须合并root真实jump与完整终态日志后共同审查；门禁不会自动从本文推导true。

## 是否需要再生成普通主宰

本次精确合同**不要求**，当前源隔离已有充分依据，因此不新增实舰或测试矩阵。顺便核实本机全部`common/global_ship_designs/*.txt`的实际`ship_design.ship_size`：没有普通juggernaut固定global design；不能凭空编`NAME_Juggernaut`。

已停止RC6同EXE的[generated effects](evidence/1019-rc6-final-logs-v1/logs/script_documentation/effects.log)原文在361–374支持`create_ship.design=<key/target/last_created_design>`或`random_existing_design=<ship_size>`，3240–3242的`create_ship_design`也只是从既有key创建设计。它们不提供本机当前不存在的普通主宰global key。

若未来root明确要另做活实舰，最小前提应是**已有且已只读确认section为原版的普通juggernaut country design**，再把这个实际design target显式传给原生create_ship；不授科技、不改Mod、不用Mother section。当前country唯一juggernaut是Mother，`random_existing_design=juggernaut`可能正好复制Mother，不能作为普通主宰对照；`create_ship design=juggernaut`也不能把ship_size冒充不存在的global design键。此页不提供或执行未经本机原生来源支持的替代生成命令。

本次仅完成来源判定，未读root正在运行的jump前缀；不复用旧银河origin0或其它旧目标数字。
