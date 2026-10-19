# rc3 机器六项补证进度 v3

从 v2 原字节 SHA `bd79e70d3ca2ad1f4149d1ae1d0fab1d273a6076ab86994726d4d29dad9d18c9` 另建 v3，v1／v2 不改。扩展归档358份payload及父索引先逐字节检查，再用既有 pending helper 导入六个明确 claims；case、组件与总状态继续 PENDING。候选源仍是 rc3 run `20261019T092935Z`、树 `178d3021fa53dd999b5537e1e58f7b59c7138232e7a7fe4fe53327b3dff8e116`，预算原值不重写。

来源报告是 `docs/evidence/1019-rc3-machine-economy/supplement-v2/analysis/rc3-machine-operational-constraints-report-v1.json`，SHA `6479fecf564ad78ad738b11f91fd22ebebd2d7b2aeef8fd41741a1d10ee64a62`。扩展索引 SHA `350a6e3a8d04f71d00dfc7e8891ef09eb28fa1a79384dc93e22d5eb658feac6f`，验证报告 SHA `3ad46788ffce352ae4d2b8c41f29f728c073b00f731b587656707ac8d2647a5b`。报告六项 value 均为 true；下列 scope 必须原样随分析引用保留，limitations 也完整复制到进度元数据。

| case.check | 报告 claims 中的原始 scope |
| --- | --- |
| machine_startup.population_preserved | Same-preset old native core 4800=RC3 core 4800; excludes removed gift colony100. Not a separate pure-vanilla fixture or constant population through year. |
| machine_startup.normal_upkeep | Nonzero native normal costs each month; only existing Mother-fleet discounts retained at equal values; no newly global free upkeep. |
| machine_economy.no_resource_injection | Recorded clean-load/year-UI actions plus all-resource monthly native ledger closure; no unrecorded-input guarantee. |
| machine_economy.no_trade_subsidy | No recorded market/trade/gift/resource-subsidy operation; normal native logistics trade production remains included. |
| machine_economy.no_job_closure | No job-management action; all finite native jobs retain max limits and positive workforce at all 14 checkpoints. |
| machine_economy.no_ship_disband | No recorded disband action; all initially owned ship IDs, fleet IDs and names retained at all 14 checkpoints. |

这六项分别绑定同名 `claims.<check>`，不扩大事实范围。358份payload保留109条动作及两个底层Ctrl+A、实际点击OCR／图像／执行器源码、12次原生30日推进、九资源×十二月库存闭合、14检查点有限岗位限制／workforce和全部原有舰船标识；没有活动日志、Hive或PK分支。两组完整log仍待最终冻结，不能用早期硬件log或本次动作分析替代。

从仓库根目录可用下列既有命令填相同六个布尔项，helper 自动计算报告SHA。最终 v3 另外将原始六个scope、limitations、父索引和扩展归档引用存入 `_progress.machine_operational_constraints_v3`，每项 `check_observations` 也携带自己的scope及claim路径。

```powershell
$v2 = 'eat_everything_origin/docs/evidence/1019-requirements/rc3-runtime-progress-v2.json'
$v3 = 'eat_everything_origin/docs/evidence/1019-requirements/rc3-runtime-progress-v3.json'
if (-not (Test-Path -LiteralPath $v3)) { Copy-Item -LiteralPath $v2 -Destination $v3 }
$helper = 'eat_everything_origin/tools/runtime_index_1019.py'
$idx = 'docs/evidence/1019-requirements/rc3-runtime-progress-v3.json'
$report = 'docs/evidence/1019-rc3-machine-economy/supplement-v2/analysis/rc3-machine-operational-constraints-report-v1.json'
@('population_preserved','normal_upkeep') | ForEach-Object {
  python $helper --index $idx observe-check --case machine_startup --run-id 20261019T092935Z --check $_ --result true --analysis $report
}
@('no_resource_injection','no_trade_subsidy','no_job_closure','no_ship_disband') | ForEach-Object {
  python $helper --index $idx observe-check --case machine_economy --run-id 20261019T092935Z --check $_ --result true --analysis $report
}
python $helper --index $idx missing
```

任何后续补证另起版本；不重写本轮报告，也不把没有归档的Hive观察或奖励校准挂到v3。最终共同审查需要核对六项限定是否足以满足实际发布范围，再将完整冻结日志纳入正式索引。

实施结果：358份归档及其当前原来源逐字节一致，总22,662,741字节，旧344份payload与父索引不变，9项归档验证均为true。v3 SHA `c6dd8394f34d530934894c00630040705552d64d7dc2aac5aeb6efe3b679b365`；231次引用／126个唯一文件均通过实际SHA校验。机器两组共14个检查为true，各自六项scope与报告claims完全一致；两组只缺log类型证据及最终审查，18组／组件／顶层仍PENDING。其余16组、全部预算、成长样本和候选源绑定均与v2完全相同，v1／v2原字节保留。既有严格最终门禁继续按预期拒绝PENDING副本。本次仅使用已有helper及实际字节核验，没有改工具代码或重新宣称整包验收。
