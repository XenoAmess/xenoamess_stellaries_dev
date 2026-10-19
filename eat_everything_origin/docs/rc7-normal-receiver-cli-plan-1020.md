# RC7普通吞噬：原接收CLI与字段短链

## 目标、范围与读取边界

2026-10-20只读准备。依据`rc7-normal-native-reception-1020.md`（当前SHA `98e72bf0065dc13fe453d6e30d244ae51ca9fa467d0ead128df5d5f0d22672bc`）及后续`rc7-normal-sampling-execution-1020.md`（`b93fda9945b202b85c83b656fe5d9926a79728da79fcdaf2674ca0b2b884364c`），仅保留ready50→真实简中决议start→m01→m04→真实最后未完成日→自然完成／稳定→重复与真实reload。**m02／m03不要求保存**；FF29只是读取m04实际进度后的候选，不预认固定150日。

旧ready失败已由其它线程专包封存；本页不读、不重审或改写其证据。新的有效入口使用未来交接`r7normalready2`，实际source物理ID尚未授权读取，不从旧候选、资本colony ID或enemy source17猜值。没有读取任何新normal原件、截图、完成回执或日志，不生成空证据包，不操作UI／Steam／Git，不改Mod／工具。

## 最短原CLI

原工具未变：receiver `d4daa66a575fa8c0ce5bba9796b6c6d4eef0b0573184ec9b6c4e5102fd033ca5`，checker `681836d2da9c6b28ee9bfd583c87e5ced96f06543901e71d3dc35fa226f3afdc`，inspector `1ec3ad71f877be5704959134b76e59be077b756a906f7297f278613ee8bfbf92`，publisher-interface `06c60c0a9bd406580314999ae6649365bb5c1fa6c7152c0b0a7fb5a420e06918`。可复用已有`docs/evidence/1019-requirements/rc7-settlement-native-intake-template-1020-v1.json`，交接后另写新intake；若要重新生成模板，现有命令为：

```powershell
python -B eat_everything_origin/tools/receive_functional_1019.py template --output '<新模板.json>'
python -B eat_everything_origin/tools/receive_functional_1019.py receive --intake '<实际绑定intake.json>' --cache-dir '<本normal包专用cache>' --output '<新原接收报告.json>'
```

默认只跑receiver：它直接调用原checker函数，并使相同SAV／manifest／world集合／checker／inspector键的观察只生成一次。后续新角色另写intake版本，旧报告保留，既有观察cache复用。不要再为同一批角色重复跑一次独立CLI。若单独验证已有完整case文件，原CLI实际是：

```powershell
python -B eat_everything_origin/tools/check_1019.py --output '<新报告.json>' settlement '<实际case.json>'
python -B eat_everything_origin/tools/check_1019.py --output '<新报告.json>' no-settlement '<实际same-day-case.json>'
```

它们没有`--source`／`--core`／`--q`参数；真实路径与所有期望放case JSON。所有输出拒绝覆盖，失败另留，不能覆盖原FAIL。

## intake必须实际绑定的字段

`schema=eep.1019.functional-intake.v1`，`expected_run_id=20261019T164112Z`，`expected_tree_sha256=61b34f6dbdc277c44364889d5f1e1cd2773a4624786bbf0d538079fc6ba4feb0`，`expected_version=0.4.0-rc.7`；同run无需additional runs。manifest为原run目录精确path／SHA `603236aeedc59d2f0a0308b500ca209f589fb89e2ea5d1928c8bc04d10fedd86`。`interface_sources`保持原工具生成结构与当前SHA。

`world_ids`只能是实际core2与交接后提取的source物理ID去重集合，均整数。每个role用`kind=native_ui_save`及`save`／`receipt`／`audit`各自精确path＋SHA；原receipt.archived和audit.save必须指向**该确切原路径**，不能以同SHA的另一个文件替换。原SAV与manifest同目录，薄包映射另记；真实autosave才使用`native_autosave`与原mtime／advance-start证据。

角色名为intake内自定义绑定键，工具不硬编码必须`normal_*`：建议ready50、decision_start、m01、m04、precomplete、immediate／stable、duplicate、reload。没有after时`tasks=[]`可合法观察已封角色，但不产生结算PASS。m01／m04只是同一Situation过程观察，不用要求同日的no-settlement跨月比较，也不拿它们当完整经济样本。

## 原settlement-case的精确字段

| 字段 | 原接口类型／本normal来源 |
| --- | --- |
| `schema` | 字符串`eep.1019.settlement-case.v1` |
| `path` | 字符串`normal` |
| `source_world`／`core_world` | 不同物理planet整数；source等实际交接，core2 |
| `expected_q` | 有限正数2；取任务开始冻结并持续保留的`eep_q`，不重复扣任务期间bite损耗 |
| `native` | 布尔`false`，不是字符串 |
| `expected_return` | 自然完成after读取前，以precomplete实际合格主体groups独立求和R；不预填100、不读after receipt反推 |
| `expected_other_core_pop_delta` | after读取前独立固定的数值及依据；不足时报告缺口，不拟合残差或自动填0 |
| `expected_crisis_progress_delta` | 本银河独立worlds单位奖励750；按该次before／after命名objective求差 |
| `crisis_calibration_evidence` | 精确path／SHA，复用已封校准`docs/evidence/1019-rc7-pk-crisis-baseline-v1/authored/independent-crisis-calibration-v1.json`，SHA `13af0b201319b15fe7b4a8abb30ed3cb019e2488bd83a7e9e465529a4dff2840` |
| `expected_crisis_empires_progress_delta` | 显式非负数；此自有非核心源预期0，不把已有600再加一次 |
| `crisis_empires_calibration_evidence` | 若预期正奖励才必须；0可省略，不填null冒充有效引用 |
| `before`／`after` | standalone CLI必须为precomplete／实际完成或稳定SAV字符串路径；receiver由语义role自动注入 |
| `reload` | standalone可选真实reload后SAV；receiver用task的`reload`角色名注入，未交接则省略 |

两个observation必须均为actor0 Nemesis path；原checker明确要求core owner0。q2背景若仍C21／G21／D7／made300，则事前公式为C23／G23／D7／累计made300／worlds2／L2，新增制造0、容量0；核心结算差应为R＋独立other，不把返回人口算新增G制造。先核真实before再固定，若不符保留实际差异，不套旧C19→21。

normal分支原settlement基础26条，加入合法reload后27条；在原25条colossus基础上，normal使用`persisted_normal_task_q`、`normal_source_owned_by_beneficiary`及`normal_task_evidence`三个分支检查。最后一项要求precomplete原生Situation target.id确实等于实际source物理ID；真实决议、T5持续过程、seed与UI仍由独立证据补，原settlement不代证。

## 最小tasks与幂等边界

settlement task只需`id`／`kind=settlement`／`before=precomplete`／`after=stable或immediate`／可选`reload`／上述`case`。same-day no-settlement task只需`id`／`kind=no-settlement`／实际before与after角色名／`case={source_world:实际整数,core_world:2}`；standalone同日case还需before／after实际路径，无额外schema要求。

ready50→decision_start因实际转移50人口，不运行no-settlement冒称“不变”；独立核源50→100、core−50、合计守恒、seed_existing100／seed_need0、q2／months5／Situation progress0。m01与m04及真实precomplete保留实际Situation身份／progress／日期，最后1日自然完成，没有写进度或调用完成回调。

stable→重复、重复→真实reload各按同日原no-settlement9条；完整strict单列，reload引起缓存变化不能抹去或宣称全SAV恒等。若immediate源live counters尚未清理，先保留原FAIL，再对稳定新角色另跑固定期待，不能改checker或取消liveness条件。原receiver最终18组138项始终null／PENDING，后续仅对原`normal_duration_preserved`／`normal_seed_preserved`／`normal_completion`／`normal_reload_idempotent`及已支持common项提出部分证据；停机完整日志和其它路径仍各自需要。

本页只确认原接口与执行短链，尚未读取r7normalready2或任何后续新角色，没有normal运行PASS或空归档包。
