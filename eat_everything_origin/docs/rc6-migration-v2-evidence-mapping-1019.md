# RC6 迁移 v2：发布证据字段映射

此映射只引用已存在的独立报告，供最终门禁适配器审核；它不创建最终发布索引。原 v1 的 `1e-6` FAIL 与全部严格差异保留。独立 v2 是主线程在 RC6 采样前声明的工程预算，每个可观察步骤三防比例增量各在 `[-0.000021,+0.000001]`，不是原生内存精度保证；移动船坞旧 implementation 未修复，单人实际加载后恢复真实 ship layout。

## 两个主要报告

- public：`evidence/1019-analysis/rc6-public031-migration-v2-complete-report-v1.json`，SHA256 `bff7b26f3ebc089f1f863aca341f94fc5688a5bb0c9ea145ab504832a6d33c7e`，174项 PASS_SCOPED；case `rc6-public031-migration-v2-complete-case-v1.json` SHA256 `7aa16358bf0adb6e1b158c044b5a3e050346e7b97b35f818f5d183f267043421`。
- paid：完整原生 CLI 重读报告 `evidence/1019-analysis/rc6-paid11-migration-v2-cli-report-v1.json`，SHA256 `d85667777cdd77940067baa0fcf3ffe55d357a6d6fd040660f9ff023bf315ec7`，158项 PASS_SCOPED；case `rc6-paid11-migration-v2-complete-case-v1.json` SHA256 `74fc72031694e5bb746fed40cafa8ef8701c5cad83a1094e5d11dc636dbd1618`。先前缓存执行的 complete report 仍保留，不覆盖。

二者绑定精确 RC6 树 `cc181c8a27ede295e9fcebeffc5e10bb75e9cd643edec1d194b928993ffab33a`、EXE `400df27c82ddc845aa9dce79bd468d81f18f060d299cd263e3afa93aef4f7a83`、新工具 `08b57969060c037c4e03829f0075f8e7314f262527215e991595bd4778456d38` 和不变的旧工具681836d2...。public 原件为公开0.3.1 bmm00 SHA af5f64e2...，真实部分受伤 before 为同公开0.3.1源码 p031before SHA d5921823...；paid 队列原件 j13ten SHA834ea532... 来自0.3.0-rc.1，但最终 ppaidbefore SHA40c8f8da... 的原生加载/施伤源码是公开0.3.1，须分开描述。完整SHA在case/provenance中，不用简称替代机器校验。

原生来源归档由独立线程建立 `1019-rc6-migration-checkpoint-v1`，最终引用必须等其真实 manifest/index/byte verify 后读取实际项目路径和SHA，不能凭计划路径编造。当前报告的原 SAV/provenance 绝对路径是真实只读来源，不能冒称已经是项目内归档。

## old_save_migration

下表字段均在两个主要报告中；public 满足公开0.3.1来源，paid 补充11项真实已付款队列。最终布尔字段应连同明确 v2 contract 元数据和两个报告一起提交，不能只把原模糊 `damage_preserved` 改true而隐去范围。

| 最终检查 | 实际字段与证据 | 限定范围 |
| --- | --- | --- |
| original_031_save | public 的 `provenance.fixture`、`provenance.before`、`case.fixture_sha256`、`case.before_sha256`；`genuine_public031_before_version/tree`、`fixture_sha_binding`、`genuine_partial_old_before_sha_binding` | paid 的0.3.0队列原件不能代替公开0.3.1原件；paid伤档本身运行于0.3.1。 |
| extra_world_preserved | `snapshots.before/after/reload.world_layout`、`v1_nonprecision.existing_colonies_preserved`、`after/reload.all_population_jobs_colonies_worlds_zones_preserved` | public physical2001、paid physical2158与原核心14/4同在，均保留原布局/人口，不对旧档删除赠品星。 |
| no_startup_reward | `v1_nonprecision.ledger_not_awarded_again`、`startup_flags_preserved`、`no_additional_charge_or_refund`；`after/reload.all_country_variables_preserved`、`all_audit_country_variables_preserved`、`all_country_flags_preserved`、`all_stockpiles_preserved`；人口/ship inventory | 单人加载修复路径的原经济和开局状态；不外推完整初始化功能。 |
| native_design_migration | `after/reload.actual_new_design_name`、`entire_actual_layout_matches_frozen_source`、`fifty_actual_slots`、`six_actual_required_components`、`six_real_core_slots`；`snapshots.after/reload.design_shape` | 依据当前实际引用设计，不用历史flag或实体section冒充。`native_sources.*.attached_starbase_implementation/raw`仍旧，明确列限制。 |
| identity_preserved | `v1_nonprecision.ship_identity_preserved`、`fleet_identity_preserved`、`starbase_identity_preserved`、`all_owned_ships_preserved_without_duplication`；snapshots IDs | public128/1008/15；paid146/822/13，全自有ship IDs保持。 |
| name_preserved | `v1_nonprecision.names_preserved` 与 snapshots full ship_name/fleet_name | 原内部名称键保持，不复用早前改名探针。 |
| position_preserved | `v1_nonprecision.position_and_orbit_preserved`、snapshots四类坐标与orbit_raw | 同日暂停，原星系/轨道/位置精确保持。 |
| queue_preserved | `v1_nonprecision.queue_identifiers_preserved`、`all_owned_queues_preserved`、`all_queue_costs_progress_designs_orbitables_preserved`；`after/reload.all_queues_payment_progress_civilian_items_preserved`、`all_queued_design_names_preserved` | public queue50为空；paid queue54保留items0..10，pool10，前10项10/60、末项0/60，每项81合金/payer0/orbitable13。 |
| damage_preserved | `steps.*.checks`、`signed_ratio_deltas_decimal`、`raw_readings`、`minimum_delta/maximum_delta`；`layout_checks`中的实际max检查；`v1_original_diagnostic`原样 | 仅预声明 v2 工程预算。public初迁移H0/A−7.926301e−6/S−4.232120e−6；paidH−3.899074e−6/A/S同前。两组reload本步0，public额外返回load本步0。旧v1均FAIL，其 `checks.damage_preserved_in_declared_mode=false`必须保留。 |
| migration_once | `repeat_sync_strict_zero_differences`、`repeat_sync_snapshot_exact`、`repeat_sync_strict_comparison`、`repeat_native_sources`；对应真实effect-command.action.json | 每对SAV间仅两次layout-only helper，不是fullsync。public两份SHA同edcd11a5...，paid同bedebd4a...，raw与strict均精确。 |
| layout_preserved | `v1_nonprecision.existing_layout_preserved`、`snapshots.*.world_layout`、population/jobs/worlds/zones检查 | 旧Machine/Hive原世界不套用新开局删区划。 |
| civilian_queue_preserved | 所有原生队列及items的完整归一快照、queued design真实名称与形状、付款/进度/库存检查 | 不只检查Mother队列；不通过清空/退款再建伪造保存。 |

重复实际命令均为 `effect root={eep_repair_existing_mothership_design=yes eep_repair_existing_mothership_design=yes}`。原动作 `r6paidrepeat-effect-command.action.json` SHA `2914fbf2c22c1742d6e8ecab8eb0d699bbe2b54240353c9fbb265754db448333`、`r6prepeat-effect-command.action.json` SHA `130ce1419cf3a2221845b1ab1593eb2cab8757efffa87b2971d416ec6d987ff6`，归档应包含原截图/OCR/输入而非仅这个摘要。

建议最终组保留独立 `migration_contract`：v2 schema、精确EXE/tree/checker SHA、固定 policy、classification=`predeclared_engineering_allowance_not_engine_storage_proof`、两个原始source/partial SHA、两个报告SHA、原v1状态及原false字段、单人范围/旧mobilebase限制。发布适配器应验证这些实际结构和所有checks，而非只相信顶层PASS_SCOPED。

## candidate_reload 的可复用范围

`native_reload` 可以复用两份报告的 after→reload 原生 `.load.json`：source SHA/实际源字节、UI日期核验、再次原生保存及实际新50槽/6核心均独立成立。public还有 source=after 的额外返回原生load，另列其step，未与helper重复混合。

`ledger_preserved` 与 `no_duplicate_reward` 可以在这两个 C0 旧档迁移/候选重载路径内复用 `reload.all_country_variables_preserved`、`all_audit_country_variables_preserved`、全部库存/人口/船只/开局flags及经济五账本检查。六核心奖励计数在这些旧C0档未初始化时仍为实际缺失，不能据此认证未来高等级 RNG/结算回调重载；那些路径有独立case。

`native_restart` 不由本迁移报告的 snapshot 或“有manifest”单独证明。应与 checkpoint 内真实run级启动/进程/EXE/原生窗口动作材料结合；若最终字段要求停进程再载同候选SAV，还须对应真实跨进程来源。已有真实启动材料可直接复核，不需要为了本映射追加UI。这里不把同进程 native reload 冒称进程重启，也不替发布线程预填该布尔值。

完整发布仍需其它case与最终冻结绑定；本映射没有修改原v1、旧原生证据、Mod、发布工具或最终索引。
