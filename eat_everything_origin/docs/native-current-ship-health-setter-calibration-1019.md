# 当前单艘原生护卫舰到原生 Relic：setter / reload 精度对照

## 独立分支与验收（执行前）

使用 RC5 当前 `r5coreguard2`，Jan1，SHA256 `44ebd953fa66ffb2a891db6e24bbe7a38f57ccb8024699a8de116e6aa120562e`。现有 country0/fleet3 的 ship3、4、5 均为原生 corvette `HUMAN1_SHIP_Yongcheng`，全满 H200/A200/S100，无 attached mobile starbase。以原生 `random_owned_ship` 恰选一艘并保存 ship target；实际选中的数字 ID 必须从第一份新 SAV 验证，不事先虚构。其余舰船、Mother、队列、资源、人口、岗位、布局与业务账本保持不变。随机选取是受控夹具操作，不作为自然成长 RNG 样本。

此独立三 SAV 分支直接测试原生 corvette → 原版 `NAME_Relic` 的 set_ship_design，再实际重载。原生 API 文档没有承诺跨 ship_size 一定支持，设计切换是否成功是待测前提；若被拒绝或载入失败，保留真实 FAIL，不能假装完成校准。此处不使用 talon_power。原 talon 两样本方案保留为另一未执行分支；旧 nrelsrc / Relic 三 SAV 方案仍为日期核验失败、未施伤。原 Mother `1e-6` 政策、全部历史 FAIL、检查器与 Mod 不变。

## 直接可执行序列

三阶段都保持同日暂停，只由主线程执行。当前 `eep_native_health_reference_1019` 和下述 probe variables 尚不存在。第一步绑定现有单艘 corvette，正向减少 hull、清盾后伤甲、正向修盾，并导出三个原生 fraction getter；不补造任何缺失变量。实际三防 current 必须均大于0且低于 max 才可作为校准前置。

```text
effect root={random_owned_ship={limit={is_ship_size=corvette} save_global_event_target_as=eep_native_health_reference_1019 reduce_hp=37.12345 reduce_shield=1000 damage_ship=37.12345 repair_shield_amount=41.34742 export_trigger_value_to_variable={trigger=has_hp_percentage variable=eep_test_health_h_before rounded=no} export_trigger_value_to_variable={trigger=has_armor_percentage variable=eep_test_health_a_before rounded=no} export_trigger_value_to_variable={trigger=has_shield_percentage variable=eep_test_health_s_before rounded=no}}}
```

原生保存 `nchealthbefore`。新 SAV 必须证明 saved target 为 ship3/4/5 中恰一艘、仍为原 corvette，并绑定实际 current/max 和全部三个 `_before` 导出。

第二步只作用于实际 ship target，调用原版 design key 并立即导出 `_set`，不新增伤害或修复。

```text
effect root={event_target:eep_native_health_reference_1019={set_ship_design={design=NAME_Relic} export_trigger_value_to_variable={trigger=has_hp_percentage variable=eep_test_health_h_set rounded=no} export_trigger_value_to_variable={trigger=has_armor_percentage variable=eep_test_health_a_set rounded=no} export_trigger_value_to_variable={trigger=has_shield_percentage variable=eep_test_health_s_set rounded=no}}}
```

原生保存 `nchealthset`。必须读取实际 referenced design/body/ship_size/required/components 与 current/max；仅命令无错误不等于跨尺寸 setter 成功。

第三步实际通过原生菜单加载 `nchealthset`，要求原 helper 的真实日期核验成功；只再次导出 `_load`。

```text
effect root={event_target:eep_native_health_reference_1019={export_trigger_value_to_variable={trigger=has_hp_percentage variable=eep_test_health_h_load rounded=no} export_trigger_value_to_variable={trigger=has_armor_percentage variable=eep_test_health_a_load rounded=no} export_trigger_value_to_variable={trigger=has_shield_percentage variable=eep_test_health_s_load rounded=no}}}
```

原生保存 `nchealthload`。逐层并列三份 SAV 的 current/max 算术比例、真实 getter、二者差值和各阶段变化。原生 getter 缺失或不变都按真实值报告，不以算术值代填。不预先断言 canonical 内存五位精度、无损伤政策或任何未来 PASS。保留严格比较的全部原始差异，专门区分设计切换成功、重载持久性、真实 getter 精度和原 Mother 迁移政策四种范围。
