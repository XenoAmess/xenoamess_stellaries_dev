# rc3 机器经济进度 v2

此副本从已提交 `f6efa25c166358353707c0bed5d022887f960e98` 的 v1 复制，v1 SHA 为 `bdb014317a1c7d606e2b984b448e22a4cec7291c232f8c009ebfd095d89e93e4`，不改写 v1。目标仅为导入稳定机器子集及明确成立的单项，所有 case、组件和顶层仍为 PENDING。

独立归档 `docs/evidence/1019-rc3-machine-economy/archive-index-v1.json` 的 SHA 为 `9fdd9cf4893eb70ab138964c7d047fcf07c554c683223e556825100999a51104`。导入前已逐一核对 344 份归档及原来源文件，共 21,084,334 字节；归档验证报告 28 项均为 true。manifest 原始 SHA `4fe88804769af4bc3e35bd14a5fcc918196491d79cc5db85cecc53cb3ab2ec4c` 与已冻结 rc3 run `20261019T092935Z` 相同，生产树仍为 `178d3021fa53dd999b5537e1e58f7b59c7138232e7a7fe4fe53327b3dff8e116`。

实施只调用既有 pending helper，不增加自动判定工具。以下映射在导入前由验收线程确认；所有源报告使用归档 `analysis/` 中的原字节副本。

| case.check | 原始分析中的直接依据 |
| --- | --- |
| machine_startup.single_homeworld | startup.one_initial_colony、one_colony、one_bound_core 及 no_extra_* |
| machine_startup.correct_homeworld_type | startup.correct_homeworld |
| machine_startup.first_month_generator_jobs | startup.power_jobs_staffed，原生 technician_drone 实际 workforce > 0 |
| machine_startup.auto_devour_off | startup.automatic_devouring_off |
| machine_startup.initial_energy_200 | startup.no_startup_subsidy 精确检查初始 stock=200；economy.same_initial_energy_stock 与 clean_anchor_initial_budget_and_stock_match_nominal_start 再核干净起点仍为200 |
| machine_economy.baseline_12_months | economy.twelve_baseline_months，保留历史0.3.1基线负预算 |
| machine_economy.candidate_12_months | economy.twelve_candidate_months 及十二份独立原生存档／receipt |
| machine_economy.all_net_energy_nonnegative | economy.candidate_energy_nonnegative_all_months |

十二条候选预算从 `fmm01.economy.json` 至 `fmm12.economy.json` 原始 OBSERVATION_ONLY 报告读取，日期为 `2200.02.01` 至 `2201.01.01`。`fmm00.sav` 是原始开局，`fmm00reload.sav` 是无探针污染的真实推进起点，不能混用硬件 hw0/hw1/hw2。首月自动存档路径错误及原动作／HUD／恢复记录保留；没有再推进一次月份。`fmyearui.sav` 与最后一次自动存档的十项原生经济字段一致，只记录该限定观察。

下列命令从仓库根目录执行，路径参数相对 `eat_everything_origin`。复制步骤只在 v2 不存在时执行；后续 helper 命令允许相同证据幂等重跑，证据字节改变会失败。

```powershell
$v1 = 'eat_everything_origin/docs/evidence/1019-requirements/rc3-runtime-progress-v1.json'
$v2 = 'eat_everything_origin/docs/evidence/1019-requirements/rc3-runtime-progress-v2.json'
if (-not (Test-Path -LiteralPath $v2)) { Copy-Item -LiteralPath $v1 -Destination $v2 }
$helper = 'eat_everything_origin/tools/runtime_index_1019.py'
$idx = 'docs/evidence/1019-requirements/rc3-runtime-progress-v2.json'
$a = 'docs/evidence/1019-rc3-machine-economy'
$run = '20261019T092935Z'
$startup = "$a/analysis/rc3-machine-startup-report-v1.json"
$economy = "$a/analysis/rc3-machine-economy-12months-report-v1.json"
python $helper --index $idx add-run --manifest "$a/manifest.json" --case machine_startup --case machine_economy
1..12 | ForEach-Object {
  $stem = 'fmm{0:D2}' -f $_
  python $helper --index $idx budget --branch machine --role candidate --run-id $run --analysis "$a/$stem.economy.json" --save "$a/$stem.sav"
}
@('single_homeworld','correct_homeworld_type','first_month_generator_jobs','auto_devour_off','initial_energy_200') | ForEach-Object {
  python $helper --index $idx observe-check --case machine_startup --run-id $run --check $_ --result true --analysis $startup
}
@('baseline_12_months','candidate_12_months','all_net_energy_nonnegative') | ForEach-Object {
  python $helper --index $idx observe-check --case machine_economy --run-id $run --check $_ --result true --analysis $economy
}
python $helper --index $idx attach --case machine_economy --run-id $run --kind native_save --file "$a/fmm00reload.sav"
python $helper --index $idx attach --case machine_economy --run-id $run --kind native_save --file "$a/fmyearui.sav"
python $helper --index $idx attach --case machine_economy --run-id $run --kind analysis --file "$a/analysis/rc3-machine-year-ui-comparison-report-v1.json"
python $helper --index $idx missing
```

按已有 `attach` 命令补挂真实截图／动作时，只需 `--case`、`--run-id`、`--kind` 和 `--file`；hash 自动计算。v2 中补挂初始、首月与年末截图，开局原生保存动作、十二次原生 `fast_forward 30` 命令及实际年末 UI 保存动作；对应完整原始集合由归档索引绑定。归档 receipt、audit、首月恢复及三个限定报告均可追溯。此处不补 `--kind log`：经济归档明确未复制活动日志，不能借早期硬件日志填齐。

仍缺：`machine_startup.population_preserved`、`normal_upkeep`；`machine_economy.no_resource_injection`、`no_trade_subsidy`、`no_job_closure`、`no_ship_disband`；两组全程冻结日志及最终共同审查。报告中的“无污染”仅检查 eep_probe 变量和 C／L／R／六种 tier 均为0，不等于穷尽操作约束。其余16组未因机器报告新增通过结论，候选 Hive／Purifier 月份与全部成长样本仍待补，真正随机组件、原生巨像各路径和迁移／重载等专项保持待验。

已完成导入。v2 SHA 为 `bd79e70d3ca2ad1f4149d1ae1d0fab1d273a6076ab86994726d4d29dad9d18c9`；208 次引用／122 个唯一文件均递归通过实际字节 SHA 校验，v1 仍与已提交 blob 完全相同。机器十二个月净电从 `2.6588999999999947` 增至 `8.517049999999998`，全部非负；原浮点值保留，不人工取整。两组均已有 native_save／screenshot／actions／analysis，缺 log；8 个明确单项为 true，其余检查不晋升，18 组、组件和顶层全为 PENDING。既有严格 `validate_runtime_index` 拒绝此进度副本，原因为 `matching scoped Chinese single-production-mod acceptance required`，证明副本未被误当最终验收。本次未修改工具代码，执行的是实际归档字节核验、既有 helper 导入／missing 和最终门禁预期拒绝检查。
