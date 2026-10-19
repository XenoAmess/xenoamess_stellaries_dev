# rc3 Hive首月 PENDING v5

## 目标、设计及验收（实施前）

保留v1—v4原字节，从v4 SHA `6f62ec128741ae936387d980d801ea22e91ff125be90c6dd80f5b4c4855b1116` 另建v5。先独立检查Hive首月归档289份payload的SHA／大小、原生三SAV与audit／receipt／解压gamestate、manifest／候选源与静态gate、23项startup报告及10项独立UI比较报告。工具正在修复migration的适用范围，已冻结旧工具字节与报告必须原样保留；原来源后续修改应如实单列，不改归档来追平。

稳定归档索引为 `1019-rc3-hive-startup/archive-index-v1.json`（SHA `f87ba1d0e428f603135d6b6d925e2c14680b3c5901da6d80572330cfcecbacde`），验证报告SHA `83de22b0618f4f1e4002094ad42019ee96c27881ac59b4d71d65c954339b3d49`。仅向 `hive_startup` 追加三份真实SAV、截图／动作及两个独立分析报告；映射实际证明的5项：single_homeworld、correct_homeworld_type、first_month_generator_jobs、auto_devour_off、initial_energy_200。人口保持及正常维护仍缺独立对应分析，不由单个人口值或预算值推断。

`fhcm01.economy.json` 若为原始OBSERVATION_ONLY且SHA绑定真实SAV，可用既有helper记录Hive首个有效月的真实净电，候选预算仅1/12；不得填写candidate_12_months、all_net_energy_nonnegative或全年操作约束。首月自动／UI十类字段一致只记限定观察，不扩大为完整gamestate一致／完整重载。保留初次选择失败的原始材料及恢复，缺失的原终端异常不得重建。活动logs不导入。

Hive manifest与canonical硬件manifest来自同一run_id，验证精确绑定后仅放archives；runs仍唯一canonical，不重犯v2／v3重复登记。所有case、组件、顶层继续PENDING；Machine14项与其余case、预算、成长、候选源和已归档校准均不改。新引用全部项目内、逐字节核对，最终验收器仍应拒绝PENDING；旧索引和旧报告原SHA不变。本轮不改工具／Mod／版本、不操作UI／Steam／提交。

## 最小复填命令

从仓库根目录执行；下面只示范已有helper对实际报告／存档的填充，最终v5还记录原始scope、归档及三SAV的来源绑定。首月预算没有任何全年通过结论。

```powershell
$helper = 'eat_everything_origin/tools/runtime_index_1019.py'
$idx = 'docs/evidence/1019-requirements/rc3-runtime-progress-v5.json'
$a = 'docs/evidence/1019-rc3-hive-startup'
$report = "$a/analysis/rc3-hive-startup-report-v1.json"
@('single_homeworld','correct_homeworld_type','first_month_generator_jobs','auto_devour_off','initial_energy_200') | ForEach-Object {
  python $helper --index $idx observe-check --case hive_startup --run-id 20261019T092935Z --check $_ --result true --analysis $report
}
python $helper --index $idx budget --branch hive --role candidate --run-id 20261019T092935Z --analysis "$a/fhcm01.economy.json" --save "$a/fhcm01.sav"
python $helper --index $idx missing
```

## 实施及独立核验结果

已生成 [progress-v5](rc3-runtime-progress-v5.json)，SHA `6d648d959be464743ba981f1a7e59886952ef6069e27669927efd8e98294b21b`。归档289份／16,250,350字节全部匹配索引；loaded_mod与source_snapshot各60个生产文件精确匹配冻结manifest，三SAV／audit／receipt及gamestate独立匹配，25项归档验证均成立。v5的291次引用／157唯一文件均按实际字节核验。v1—v4原SHA不变，runs仍唯一canonical，Hive manifest只入archives。

检查期间当前工作区 `tools/check_1019.py` 因并行migration适用范围修复从归档SHA `ba17847049d050b2b76dc382e7e3e0a1796dc4976a80c77b16fef243bc612047` 变为 `df147d247240c75bc0507cb1dda0bf88af299706841d3b72c140b083e96be777`；原始289份payload仍全匹配，其中288个当前原来源仍相同，唯一变化是此工具源。旧checker快照、报告及其原始SHA均保留，没有重跑覆盖或修改生产Mod。v5和[独立字节审核](rc3-runtime-progress-v5-byte-audit.json)明确记录该时点的源漂移；审核SHA为 `b95a41b68e74ae5b87a9e04a7e7d1f604bd6d54c162a542240cffacd011146c9`。

仅增加5个Hive startup明确单项，首月 `2200.02.01` 净电原值 `18.510510000000004` 作为1/12观察；Machine12月、Purifier0月及全部成长／组件／校准保持原状。Hive startup仍缺population_preserved、normal_upkeep和完整冻结log；Hive全年7项检查全部保持null，并缺其余11个候选月和全年操作证据。19个累计单项true不代表case通过：18组、组件和顶层仍PENDING，最终验收器按预期拒绝。没有导入活动logs，也没有把初次选择中止的缺失终端输出补写为新证据。

收口时主线程报告新的PK时长疑点：3月7日排队、3月10日原生完成flag、3月13日SAV已破碎且q19仅结算一份奖励，与90／30设计不符。独立命名CSV可能未按引擎固定路径载入，属于待调查原因，尚未确认。主线程已暂停新的Mod验收，等待载入合同查明及工具修复；本v5没有导入该PK过程或提升任何firecase，仅保存已完成Hive观察。若产生新RC，现有RC3证据继续绑定原树及原SHA，不改写成新候选或最终版本的通过证据。
