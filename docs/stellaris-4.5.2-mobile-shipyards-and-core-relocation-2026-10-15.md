# Stellaris 4.5.2：移动船坞与物理母星迁移

本轮仅认证Stellaris 4.5.2（EXE SHA256 `400df27c82ddc845aa9dce79bd468d81f18f060d299cd263e3afa93aef4f7a83`），不推断CK3方言或跨游戏共性。详细迭代、原始失败和独立专项证据见[1015实施记录](../eat_everything_origin/docs/implementation-1015-2026-10-15.md)。实机为简中、Steam离线、单独启用吞噬之心。

## 移动船坞的真实边界

- 原版`common/ship_sizes/18_juggernauts.txt`的主宰有10条船坞，不应沿用旧版本2条的记忆。`common/starbase_levels/01_juggernauts.txt`提供对应移动星基地等级、母港及原生船坞按钮。
- 自定义舰型采用`shipclass_starbase`和`construction_type=starbase_shipyard`，补上等级映射后，确实可以付款、十项并行、造出实际舰船并移动；这些字段仍不足以证明附近舰队维修生效。v10同位置、同受损舰队与原版主宰比较，只有原版提供额外每日1船体维修。
- 最终方案使用原生`ship_size=juggernaut`，只给EEP事件设计独立舰段、灰风组件、舰队修正和隐藏图形文化，不覆盖原版舰型、等级或Gray蓝图。正常指派母舰为母港并返回后，十舰五日各恢复8.125，包含0.625/日蜂巢被动和1/日主宰维修。自动跟随母舰而未指定母港时，仅有被动恢复。
- 原生“自动修理”在该测试位置会选择首都站，原版主宰对照也如此；不能仅凭这次自动选站判定移动舰体不支持维修。原生返回母港按钮与修理按钮不同。母港实际保存在`fleet_template.<id>.home_base.orbitable.starbase`，不是Fleet的标量字段。
- `uses_naval_capacity=no`在该移动星基地实例没有使实际海军容量归零；原生SAV记录母舰占100。应记录实际值，不把配置字段等同运行结果。
- `is_designable=no`的星基地会按当前科技生成实例设计，并原地更新防御组件，原版`00_ship_sizes.txt`对此有注释；独立低科技母舰曾因此被换成T1防御。真实组件与军力应从SAV和游戏界面检查。

原始[船坞、移动、维修与重载专项](../eat_everything_origin/docs/evidence/1015-2026-10-15/v13-shipyard-runtime/shipyard-proof.json)为有界通过，不代表全部政体完整战役验收。

## 模型加载与静态能力

`.asset`同样是P格式，须纳入包解析检查。open_kaishek已通过独立提交`721bc27`补足发现、解析、大小写扩展名及负例覆盖。静态语法通过不认证实体引用或加载时序。

放在较早目录的`entity.clone`曾无法找到原版无畏舰父实体；直接复制小型实体注册、使用EEP唯一名称并引用原版mesh／动画／特效后，实际模型正常。原版已经注册`npf_01_juggernaut_entity`作为替身，不可将同名覆盖冒称“新增别名”。最终隐藏文化`eep_dreadnought_01`及相关实体不改变其它帝国的图形文化或原版资产。

## 母星重绑定

本机生成的`logs/script_documentation/effects.log`明确：`set_capital=yes`支持planet／ship／colony；`clear_global_event_target`支持`string@scope`。EEP迁移先清理旧物理星球上的专属修正、核心地貌、反向actor与来源已知的解限，再在新物理星球重建唯一绑定，设置原生首都并同步容量和队列。国家账本及其它活动局势保持，后续结算动态解析当前绑定。

原生SAV的Country.capital指向Colony ID，不能直接与物理Planet ID比较。队列实际并行数在下一原生日刷新；同日修正已迁移不代表缓存字段立即变更。新增世界在重载时曾只补入四项`can_fill_*_job=yes`缓存；严格比较的原FAIL保留，范围通过仅允许明确记录的人口组和四项缺省→yes，不忽略人口数量、身份或其它字段变化。

迁移[35项专项证据](../eat_everything_origin/docs/evidence/1015-2026-10-15/v14-migration-runtime/migration-proof.json)包含正常往返、并发任务、实际首都、队列刷新、资源／人口守恒及重载；不冒称完整战争占领或人工天体战役均已测试。

## 原生局势取消

`every_targeting_situation`支持Carrier，能直接枚举以当前星球为目标的局势；在内部按类型和所有者筛选后`abort_situation=this`会立即执行on_abort，SAV先保留killed=yes对象，下一原生日清理。将这种缓存对象误算作仍运行的局势会误报失败。用临时saved target跨Country遍历比较曾在决议效果预览中产生未定义目标，改为原生目标迭代器后，列表预览、决议取消与原局势方案都已实测通过。取消开着自动吞噬的任务时，应保存独立单星豁免，避免下月重新开始；中止不撤回已发生的人口迁移或原版噬岩损伤。

## 化身天灾与原生阶段

4.5.2原生`add_ascension_perk=ap_become_the_crisis`实际执行该飞升的on_enabled；本轮新开局SAV已出现`crisis_progression.path=nemesis_path`、`level=crisis_level_1`，无需再重复激活路径。实际SAV字段名是`crisis_progression`，旧观测器的空`crisis`字段不能证明路径未激活。

原生危机等级2～5分别需要威慑1000／2000／5000／10000及相应`crisis_special_project_1_complete`～`4_complete`门槛。隔离夹具产生威慑并预置门槛后，仍由原生引擎推进等级；这证明分支与月度同步，不证明自然科研项目或毁灭世界已完成。最终范围证据见[41项王庭检查](../eat_everything_origin/docs/evidence/1015-2026-10-15/v17-final-runtime/crisis-throne-proof.json)，包含真实阶段、迁移及原生重载，不直接写EEP王庭档位。

## UI与人口差分

原生建造队列项的取消控件是覆盖整行的左键`cancel_button`（`interface/planet_view.gui:8148`）；不能把无效右键输入算成清障取消失败。实际清障支付300能量、左键取消后全库存严格恢复。

拆除实验室会改变岗位供给。暂停同日SAV观测到`complex_drone`人口组-180、`maintenance_drone`组+180，并带`GROWTH_CAT_PROMOTION`记录。严格组对象差分应保留原FAIL，另按殖民地／种族核总人口守恒，并显式列出允许的组与字段；不得忽略任意人口变化或宣称全部组不变。此处仅为本机4.5.2实测结果，不移植到CK3。
