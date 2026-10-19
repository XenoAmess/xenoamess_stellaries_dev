# 最终发布索引中的独立迁移v2范围

## 目标与范围

2026-10-19主线程报告RC6原生public／paid迁移v2已产生独立限定通过证据，要求发布门禁诚实表达这一预先声明的有界舍入范围，不将原v1失败改为通过。本轮只修改`publish_1019.py`及其测试、发布验收映射文档，不改生产树cc181c8…、版本、迁移工具／既有报告、UI、发布或Git。

## 设计与验收标准

先读取v2工具、合同、两类真实报告和acceptance线程的字段映射，确认现索引对旧档损伤的语义。若现有布尔check不足以表达独立v2，新增显式合同／类型化报告引用：精确RC6tree／run／EXE／简中单生产Mod、public0.3.1与独立paid来源、原生加载／reload／重复sync、每步loss2.1e-5与gain1e-6、全部非精度不变量及actual-design检查必须有真实证据。保留嵌套v1 FAIL与stale mobilebase限制，不以未知或缺字段默认通过，不放宽其它case。

定向测试必须证明v2限定正例可被新门禁接受，同时原v1失败字节／状态保持；拒绝未知合同／扩大预算／缺一来源或必要原生证据／错误tree、EXE、run、actual design、队列、账本和假报告状态。临时合成guard数据不是原生证据。文档还需给主线程准确的18case索引schema与既有assembly helper用法；缺项保持PENDING，不能预置PASS。

## 调查与实施

现有门禁只要求old_save_migration的`damage_preserved=true`，没有表达独立v2合同；直接把它填true会误称旧严格政策通过。保留原字段为false，新增`damage_within_predeclared_v2_budget=true`及显式`migration_contract.schema=eep.1019.migration-release-scope.v2`，仅该组、仅完整v2证据通过时允许这一项false。所有其它check仍必须为true；未知scope不进入例外。原严格v1无此scope时沿用旧门槛，不会自动从v2得到true。

scope需包含原始checker／事前policy文档引用、精确policy、单人模式、三项明确限制，以及public031／paid11两份独立case／report／六角色native SAV引用（fixture、before、after、reload、repeat_before、repeat_after）和实际load receipts。所有引用为项目相对path＋真实SHA；报告与case本身须出现在该组analysis evidence，SAV须出现在native_save，load receipts须出现在actions；两份来源与输出不混淆。

`classification`必须为`predeclared_engineering_allowance_not_engine_storage_proof`。它表示事前工程预算，不是引擎位宽证明或数学无损承诺。预算按每次实际load分别判定：最大损失0.0021个百分点、最大回血0.0001个百分点，不把累计多次加载损失包装成零。

验证固定RC6 tree／EXE／v2 checker原SHA、case哈希和原case语义、v2当前174／158检查键合同及全部true、固定旧原件SHA／身份／0或11项队列、原版不同fixture版本、当前run／manifest、全部源收据／audit绑定、actual design与layout checks、每步Decimal raw current/max重算、原1e-6诊断及v1 FAIL不改、重复sync严格0差异和旧mobilebase原生引用保留。检查键集合hash仅固定本版工具的完整两类报告结构，不能用一两个true代替；报告原SHA验证仍独立。公开报告含第三次真实load后repeat路径，付费报告从reload直接repeat，均按各自真实case检查，不要求伪造多一次load。

acceptance已确认稳定源（均docs/evidence/1019-analysis）：public完整report `rc6-public031-migration-v2-complete-report-v1.json` SHA `bff7b26f3ebc089f1f863aca341f94fc5688a5bb0c9ea145ab504832a6d33c7e`，case `rc6-public031-migration-v2-complete-case-v1.json` SHA `7aa16358bf0adb6e1b158c044b5a3e050346e7b97b35f818f5d183f267043421`；paid真实CLI report `rc6-paid11-migration-v2-cli-report-v1.json` SHA `d85667777cdd77940067baa0fcf3ffe55d357a6d6fd040660f9ff023bf315ec7`，case `rc6-paid11-migration-v2-complete-case-v1.json` SHA `74fc72031694e5bb746fed40cafa8ef8701c5cad83a1094e5d11dc636dbd1618`。原v1均为FAIL且damage=false；不能把未完成的canonical归档路径预填进索引。

## 归档映射与最小合并

迁移检查点已真实封存于`docs/evidence/1019-rc6-migration-checkpoint-v1/`，index SHA为`9bd49ca3bfdf1e13da6175833390384ac90a430ad67a4d9a38ef9a97eaf7438d`，verify SHA为`6de924841b76c247c4cc73a199fd1e40fd72e8caf0a4a911f6ab34ec4a7a4171`。唯一candidate manifest为其中`run/manifest.json`，SHA为`10f2ce0f5a699d8ad9f39769f46f919cf3e19f64f8cc24cc5d67ebf0347935f9`。不能把同run的多个归档manifest重复加入`runs`。

另引用已有原件，无需再次复制SAV：

| 角色 | 原生三件套前缀（均位于docs/evidence） |
| --- | --- |
| public fixture | `1019-baseline/bmm00` |
| public before | `1019-legacy-damage-run-final/run/p031before` |
| paid fixture | `1015-2026-10-15/v13-shipyard-runtime/j13ten` |
| paid before | `1019-legacy-damage-run-final/run/ppaidbefore` |

三件套是`.sav`、`.audit.json`、`.native-save.json`。paid原始fixture为0.3.0-rc.1，不能改称0.3.1；两份已施伤before才是0.3.1旧树。输出SAV、收据、报告取检查点的`run/`及`analysis/`，均按原报告SHA定位。

为减少手工schema错误，新增小型映射提案`docs/evidence/1019-requirements/rc6-migration-v2-scope-pending-v1.json`。目标、设计与验收如下：只按以上稳定文件生成44个真实引用，调用新的纯只读validator复核；不新造原生数据、不改历史报告、不生成完整进度索引。顶层与迁移组保持PENDING；11个非损伤check暂为null，原严格损伤为false，独立v2预算为true。原证据的174／158 scoped true不是完整矩阵通过。

映射按SHA去重保存引用。真实repeat的前后SAV有逐字节相同样本，因此多个角色可指向同一个canonical字节副本；各角色原路径、audit、独立save receipt和真实输入仍在原报告／合同中分别保留，不把一次保存冒充两次动作。后验发布门禁校验也不冒称原迁移worker导入了此后修改的发布工具。

主线程审阅映射后，可将提案`cases.old_save_migration.migration_contract`及该组`evidence`合并到当前RC6 PENDING工作副本，按真实报告逐项填写其余11个check。保留该组已有log／screenshot／actions引用；提案只提供本迁移合同需要的analysis、native_save和actions，不代替该case要求的全部五类证据。`runs`按run_id去重，保留唯一manifest引用。不得直接把提案作为`final-result.json`。

提案SHA为`f32db65df944cf8b4d715c17d7e5a0913fa794ce6bcaf23036bba7de0fc0a073`。下面是可重复的只读合同复核入口，不写任何索引：

```powershell
@'
import sys
from pathlib import Path
sys.path.insert(0, 'eat_everything_origin/tools')
import publish_1019 as p
root = Path('eat_everything_origin').resolve()
data = p.read_json(root / 'docs/evidence/1019-requirements/rc6-migration-v2-scope-pending-v1.json')
runs = {p.read_json(p.reference_path(ref, root))['run_id']: ref['sha256'] for ref in data['runs']}
p.validate_migration_contract(data['cases']['old_save_migration'], data['production_tree_sha256'], root, runs)
print('MIGRATION_V2_BINDING_VALIDATED; CASE_AND_FULL_MATRIX_PENDING')
'@ | python -
```

合同结构固定为：

```text
case.migration_contract = {
  schema: "eep.1019.migration-release-scope.v2",
  execution_mode: "single_player_postload_layout_repair",
  classification: "predeclared_engineering_allowance_not_engine_storage_proof",
  policy: {step_signed_ratio_min:-0.000021, step_signed_ratio_max:0.000001,
           v1_absolute_tolerance:0.000001, relative_tolerance:0},
  limitations: ["single_player_postload_only", "mobile_starbase_cache_not_repaired",
                "original_v1_failure_retained"],
  checker: <analysis ref>, contract_document: <analysis ref>,
  fixtures: {public031:<bundle>, paid11:<bundle>}
}
bundle = {report:<analysis ref>, case:<analysis ref>,
          native_saves:{fixture,before,after,reload,repeat_before,repeat_after},
          audits:{same six roles}, save_receipts:{same six roles -> [actions refs]},
          load_receipts:{after,reload[,repeat_before]}, repeat_action:<actions ref>}
ref = {path:<existing project-relative file>, sha256:<actual bytes>, kind:<kind>}
```

## 18组最终索引与现有组装入口

最终schema仍是`eep-1019-acceptance-v1`，正式review目标路径仍是`docs/evidence/1019-requirements/final-result.json`。当前真实组件路线`component_rewards.status=IMPLEMENTED`需要**恰好18组**：

```text
hive_startup, machine_startup, purifier_startup,
hive_economy, machine_economy, purifier_economy,
lithoid_hive_first_month, mothership_configuration, unlimited_growth,
colossus_enemy_fire, colossus_guards, colossus_cancel_idempotence,
common_settlement, normal_dismantle_regression, old_save_migration,
candidate_reload, repeat_initialization, random_components
```

每组为`{status,production_tree_sha256,run_ids,checks,evidence}`；迁移v2另有上述`migration_contract`。必需check名精确取`publish_1019.CASE_CHECKS`及`COMPONENT_CHECKS`，不手写同义名称。顶层还必须包含candidate version／formal_version／语言／EXE／profile／单生产Mod／完整production_files／原candidate_descriptor／树指纹／static_gate／唯一runs／component_rewards／三分支economy／growth_samples／archives／fully_accepted_civics=[]。每个经济分支各有12个baseline_months和12个candidate_months，行格式为`{date,net_energy,evidence}`，候选月份须非负、原生、互异且连续；历史baseline不伪装成RC6。组件报告须有四个预声明模型链、固定HP政策、十八原生phase、六种真实非零RNGtier、独立source归因和普通舰负对照。这里的十八phase与十八case组不同。

以下命令均从仓库根执行，参数中的路径相对`eat_everything_origin`。最小reference plan只允许`static_report,runs,cases,component_evidence,archives`，不能提供PASS、checks、月份或成长观测。例如plan可绑定`docs/evidence/1019-rc6-static/candidate-rc6-open-kaishek.json`与上述canonical manifest。

```powershell
python eat_everything_origin/tools/publish_1019.py scaffold-index --output docs/evidence/1019-requirements/rc6-runtime-progress-v1.pending.json --reference-plan docs/evidence/1019-requirements/rc6-reference-plan-v1.json
python eat_everything_origin/tools/runtime_index_1019.py --index docs/evidence/1019-requirements/rc6-runtime-progress-v1.pending.json add-run --manifest docs/evidence/1019-rc6-migration-checkpoint-v1/run/manifest.json --case old_save_migration
python eat_everything_origin/tools/runtime_index_1019.py --index docs/evidence/1019-requirements/rc6-runtime-progress-v1.pending.json baseline --directory docs/evidence/1019-baseline
python eat_everything_origin/tools/runtime_index_1019.py --index docs/evidence/1019-requirements/rc6-runtime-progress-v1.pending.json missing
```

`attach --case NAME --run-id ID --kind KIND --file PATH`绑定额外证据；`observe-check --case NAME --run-id ID --check CHECK --analysis PATH --result true|false`只记录有范围的单项事实；`budget --branch hive|machine|purifier --role candidate --analysis PATH --save PATH --run-id ID`从真实观测提取一个月。helper拒绝写final-result、拒绝改冻结源、保持所有case／component／top为PENDING。新增v2预算字段和typed合同由显式映射合并，不让旧helper自动宣告通过；`missing`仍会列出原`damage_preserved=false`，这是保留旧诊断的预期结果，最终validator仅在完整v2合同成立时解释该一项。

没有自动promote为PASS的组装命令。主线程逐组完成review后，才另存最终索引并将实际完成的status设为PASS_SCOPED、组件设IMPLEMENTED，然后执行`python eat_everything_origin/tools/publish_1019.py check-runtime`。任何其它check缺失／false、其它tree报告、未完成case或未授权跳过组件仍失败。此命令只读，不发布。

定向测试以两份已冻结报告的结构为夹具，深拷贝到临时目录，替换为明确标记的合成SAV、audit、收据与run引用；仅临时覆盖旧fixture字节指纹，不改真实报告或生产常量。检查所有真实报告字段约束及重新计算预算，原报告SHA和嵌套v1 FAIL另行核实。畸形引用／缺字段统一拒绝；原生ID及数量不接受bool。

## 实施结果与验证

2026-10-19完成：真实canonical提案44条引用通过独立v2合同验证；只得出迁移字段绑定成立，未修改任何case为PASS_SCOPED。两份原报告及原case、原v1 FAIL、RC6 Mod与历史manifest保持原字节。新发布工具是本次后验验证源，旧报告不回填其SHA。

稳定代码指纹：`tools/publish_1019.py` SHA `50185608b9bb0bc60a57ce8bb10717c388c52119c2619fb9ef75114fbc5558f6`；`testing/test_publish_1019.py` SHA `779fa8ed20da7e5f84463f040c9e2663a5ecb3801ddfd27dbccd8e0442192344`。独立v2 checker仍为`08b57969060c037c4e03829f0075f8e7314f262527215e991595bd4778456d38`，其原报告未改。

最终验证命令：

```powershell
python -m unittest discover -s eat_everything_origin/testing -p test_publish_1019.py
python -m unittest discover -s eat_everything_origin/testing -p test_runtime_index_1019.py -v
git -c core.whitespace=cr-at-eol diff --check -- eat_everything_origin/tools/publish_1019.py eat_everything_origin/testing/test_publish_1019.py
```

发布门禁54项测试全部通过（68.001s），进度helper8项全部通过（3.245s）。覆盖旧v1失败保留、未知模式／schema／分类拒绝、扩大预算拒绝、raw重新计算后的超额损失与回血拒绝、缺任一来源／SAV／audit／save／load收据、错run／manifest／tree／EXE／actual design／队列、伪造旧诊断和丢失原始读数。原有组件归因、HP预算、CSV／PK合同、18组要求、metadata-only正式化、图库与远端核验后tag门禁保持通过。空白检查退出0。

一次将两个包名合并交给`unittest`的尝试，因进度测试按相邻模块名导入`test_publish_1019`而发生入口路径ImportError；使用其既有discovery入口后8项全过，未修改测试导入规则。此后又用正确discovery入口完整运行发布54项并取得独立退出0。

尚未完成的最终审查仍包括迁移组另外11个顶层check／该组log与screenshot等完整证据的显式合并，其余当前候选18组的所有实机缺项、最终运行日志冻结和共同review。C0迁移报告不认证高等级RNG重载，也不单独认证进程restart。未生成最终索引，未改正式CHANGELOG／VERSION／descriptor，未操作UI／Steam／Git提交推送。
