# 当前普通原生舰：最短健康 getter / 最大值对照

## 目标与范围（执行前）

旧 `nrelsrc` 发生顶栏日期核验失败，其 Relic 三 SAV 方案保留为未执行。本方案直接使用 RC5 当前公开旧档分支已存在的普通舰，不加载坏 UI 来源、不新造船、不改 Mod、不改原 `1e-6` 政策或历史 FAIL。只由主线程执行原生命令与保存；本分析线程只核对真实 SAV、回执和原生接口。

已核当前 `r5coreguard1`：Jan1，SHA256 `44ebd953fa66ffb2a891db6e24bbe7a38f57ccb8024699a8de116e6aa120562e`。country0 没有现成 Gray Control 或 NAME_Relic。fleet3 内三艘原生 corvette：ship3、4、5，实际设计均为 `HUMAN1_SHIP_Yongcheng`，三防当前/最大均 H200/200、A200/200、S100/100，均无 attached starbase。它们目前没有健康导出变量。

原生文档支持 `random_owned_ship` 在 country/fleet 内恰选一艘符合 limit 的船，也支持在 ship 上 `save_global_event_target_as`。不杜撰 `ship:<数字ID>` scope 或未文档化 ship_id trigger。为只影响一艘现有 corvette，第一条命令一次选取并绑定 `eep_native_health_reference_1019`，随后只作用于该船。其实际 ID 必须从新 SAV 的 saved target 和唯一变化 ship 块核实；允许集合仅为3/4/5，不能先声称随机选中的具体 ID。此受控分支消耗一次原生选择 RNG，不用于自然成长 RNG 验收。原始清洁档不受修改。

若必须执行前固定一个数字 ID，则可改用当前唯一 science（fleet1 / ship1 / `HUMAN1_SHIP_Earhart`，H300/300、A200/200、S100/100，无 attached starbase），country 内 `every_owned_ship={limit={is_ship_size=science} ...}` 已知只命中它。不要把 corvette 的三船集合当成唯一匹配。

## 两次暂停原生保存

第一条命令不推进时间。用正向 `reduce_hp=37`、清盾后 `damage_ship=37` 和正向盾修复 `41.34742`，制作三防均为正的部分损伤，并立即导出三个原生比例 getter。护盾非整数量用于观察实际 API 精度，不硬编码未来实际值或 getter 值。若原生实际不保留该输入精度，须报告实际值；不得补造变量。新 target 在当前 SAV 中必须原本不存在，且无相同探针变量；若已存在则停止并换新独立名称。

```text
effect root={random_owned_ship={limit={is_ship_size=corvette} save_global_event_target_as=eep_native_health_reference_1019 reduce_hp=37 reduce_shield=1000 damage_ship=37 repair_shield_amount=41.34742 export_trigger_value_to_variable={trigger=has_hp_percentage variable=eep_test_health_h_before rounded=no} export_trigger_value_to_variable={trigger=has_armor_percentage variable=eep_test_health_a_before rounded=no} export_trigger_value_to_variable={trigger=has_shield_percentage variable=eep_test_health_s_before rounded=no}}}
```

原生保存 `nchealthbefore`。只有实际 SAV 证明目标恰为上述三艘之一，且三层 current 都大于0并小于对应 max，才能作为校准前置。期望伤害方向不是未来 PASS；须核所有其它舰船、Mother 双 implementation、队列/库存/人口/岗位/布局/账本不变。

第二条命令只对实际已绑定 ship 加原版 `talon_power`，同一暂停日导出三个 `_talon` getter，不额外伤害、修复、设设计或推进日历。原生 `19_static_modifiers_paragon.txt:8-12` 定义 ship hull_add5000、armor_add5000、shield_add2000；它们是源参数，完整实际 max 以新 SAV 为准。

```text
effect root={event_target:eep_native_health_reference_1019={add_modifier={modifier=talon_power days=-1} export_trigger_value_to_variable={trigger=has_hp_percentage variable=eep_test_health_h_talon rounded=no} export_trigger_value_to_variable={trigger=has_armor_percentage variable=eep_test_health_a_talon rounded=no} export_trigger_value_to_variable={trigger=has_shield_percentage variable=eep_test_health_s_talon rounded=no}}}
```

原生保存 `nchealthtalon`。逐层并列 before/talon 的真实 current/max 算术比例、真实导出 getter 及二者差值；导出缺失即 UNKNOWN/FAIL，不以算术值代填。此两样本只校准原生 getter 与原版 modifier 最大值变化，不能替代普通舰 set_ship_design / 重载三阶段对照，亦不能令旧 Mother 迁移或设计持久性 FAIL 变为 PASS。需要 setter 校准时另建新阶段，不能把 talon 分支冒充 setter。

## 原生接口与保留边界

当前原生 effects 文档：`reduce_hp`490-492、`reduce_shield`498-500、`damage_ship`502-506、`repair_shield_amount`2824-2826、`export_trigger_value_to_variable`557-564、`random_owned_ship`5818-5827、`save_global_event_target_as`715-717，均支持上述实际 scope。`rounded=no` 是该 export 接口参数，不是无限精度保证。只观察这台 EXE 与该设计的真实结果，不预先断言内存 canonical ratio、五位小数算法或跨游戏通用精度合同。
