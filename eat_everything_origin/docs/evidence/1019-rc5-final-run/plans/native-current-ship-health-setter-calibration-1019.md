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

## 已观察 before 与 setter

`nchealthbefore` 原生 SHA256 `ee26b57e209b88e2d38215e1db9060b645683826fe1140a1a842c7a4594e300d`，Jan1。saved target 实际为 ship3/fleet3，旧 implementation45/corvette，未命中其它两艘。真实 H/A 各162.87655/200，算术比例0.81438275，真实 `_before` getter均0.81438；真实 S41.34742/100，算术0.4134742，getter0.41347。故这些 API 导出值与未取整的实际 current/max 比例已分别相差 `-2.75e-6`、`-2.75e-6`、`-4.2e-6`，不能将导出变量本身称为已证实内存 canonical ratio。

`nchealthset` 原生 SHA256 `2e8c78cffec9f4185065aaeac27b23c10292175d18741d47861e9c3536420189`，同日。实际 ship3 implementation1609 成功引用原版 `NAME_Relic` / `npc_warship_01`，真实43槽/6required，证实本受控实例的跨尺寸 setter 执行成功。H16287.6/20000 与 A25034.0412/30740 的算术比例均0.81438；S57204.60817/138352.5 的算术比例约0.4134699999638604。真实 `_set` getter H/A均0.81438、S0.41346。特别是此时 S getter 与算术比例又差约 `-9.9999638604e-6`，不得用它反推一个被假定精确的内存比例字段。

相对实际 before 的算术比例，原生普通舰 setter 后 H/A 各改变约 `-2.75e-6`、S约 `-4.20003614e-6`；这独立说明同台原生 API 在非移动船坞、普通原生设计到原生设计的本实例中也未达到旧 `1e-6` 比例政策。不把此观察自动推广为通用容差或改判 Mother 历史 FAIL。实际重载尚待其独立 SAV/回执，以上不预认证后续结果。

## 实际重载与完整校准报告

`nchealthload` SHA256 `cbf368925ddce6ec9a182a936a05e7fc99f4137616f2352f34852da4fc641b17`，同日原生重载。目标 ship3 仍引用1609 / NAME_Relic，43槽/6required，所有三防 current/max 与 setter 后逐数字完全相同，三个 `_load` getter 也分别保持0.81438、0.81438、0.41346。因此这次普通舰原生 setter 有超过旧1e-6政策的误差，而该目标的实际 reload 没有新增算术比例损失。

完整 [native-current-ship-health-setter-calibration-report-v1.json](evidence/1019-analysis/native-current-ship-health-setter-calibration-report-v1.json) SHA256 `6e7b1fa1895fad154a657bcdbf6168347bc6ee31cdb2e42356b68eea1da5654a`，40项限定检查中36项为真，状态 OBSERVATION_WITH_FAILURES，保留三项 setter 原政策 FAIL。before/set 阶段除目标以外11艘自有船完整 raw 精确不变；实际 reload 后 raw 变化船号0、4、5、1008均列明，不能继续声称所有其它船 raw 不变。特别是 Mother1008 复现已知RC5独立缓存/设计回退：旧1625 / 29槽/5required，A24308.67348/24429.6、S25542.52272/61776；该变化另行保留，不能隐去或归给参考 ship3 的 setter 精度。

报告保留 baseline→before10、before→set26、set→load43、before→load65项完整严格差异，绑定各自原始 SAV/审计/回执和命令动作。Talon 与旧 nrelsrc 分支仍未执行。此观察没有修改旧政策、历史报告、业务 Mod、共享检查器或原生来源。
