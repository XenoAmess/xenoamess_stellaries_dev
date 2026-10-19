# 0.4.0 发布适配、冻结与验收门禁

## 目标、范围与当前状态

本次把未发布的单母星 0.3.2 工作与 1019 旗舰／巨像工作合并为正式 0.4.0。新增 `tools/publish_1019.py`，复用既有 `publish_update.py` 的正式版本、changelog、冻结提交、原位图库替换、独立下载和公开图片验证协议，保留历史适配器及历史验收测试。开发使用 `0.4.0-rc.N`；只有实测最终候选可提升至 0.4.0。

本记录先于工具与测试实现。当前最终结果索引尚未生成，本文及单元测试不是实机通过证据。子任务只实现可审查的离线门禁，不操作 Steam、不启动 UI、不上传、不创建标签、不提交推送；主线程负责最终发布。Workshop 仅允许 3815707212；3710613857 永远只读。Steam 应在最后上传阶段才在线，完成验证后恢复离线。

## 设计

候选实测证据索引固定为 `docs/evidence/1019-requirements/final-result.json`，格式 `eep-1019-acceptance-v1`，状态 `PASS_SCOPED`。索引绑定精确预发布版本、生产文件逐个 SHA256、候选 descriptor 原始文本、简体中文、单生产 Mod、精确 EXE SHA256 `400df27c82ddc845aa9dce79bd468d81f18f060d299cd263e3afa93aef4f7a83`，以及 open_kaishek 报告与原生运行证据。所有证据必须归档到项目内部，使用项目相对路径及 SHA256；禁止路径逃逸和无哈希外部路径。

每个 case 记录 `status=PASS_SCOPED`、`production_tree_sha256`、`checks` 和 `evidence`。树摘要使用与运行适配器一致的算法：按原生 Path 排序，依次向 SHA256 输入相对路径 UTF-8、NUL、文件原始字节。`checks` 必须覆盖该组的强制检查名且全部为 JSON true；`evidence` 要含原生 SAV、截图、动作、完整日志及分析，分别用 `kind=native_save|screenshot|actions|log|analysis` 标记。索引还绑定实际 run manifest，避免把旧 0.3.2 的经济结果用作新候选验收。

`runs` 只列最终候选的原生 manifest；其 profile 必须为 `eep-0.4.0-single-production-mod`，唯一启用项为 `mod/ugc_eep-1019.mod`。基线是原 Mod 0.3.1、旧测试 profile 0.3.2 所产生的真实档案，不得改写为新 profile。基线 manifest 保持原样，作为 `archives` 或相关 `analysis` 证据引用即可；不把它塞入强制新候选身份的 `runs`。

必需 case 组：

| 组 | 必须实测的范围 |
| --- | --- |
| hive／machine／purifier_startup | 仅对应母星、能量200、首月发电就业、自动关闭、人口和正常维护 |
| hive／machine／purifier_economy | 各自基线及最终候选各12月；每月真实净电非负，无资源注入、贸易补贴、关岗或拆舰 |
| lithoid_hive_first_month | 独立石质蜂巢首月 |
| mothership_configuration | 同国同日 NAME_Relic 参照、真实设计／供能／维护、保留遗迹级五个辅助组件、主动跃迁、十移动船坞、未向帝国授科技、其它主宰不受影响；允许额外专属组件槽 |
| unlimited_growth | C=0/9/10/19/20/200/10000；L=floor(C/10)；每级四项5%、恢复、幂等、同日重载、毁舰不复生 |
| colossus_enemy_fire | 原生武器实际充能发射、战争中敌方天然殖民星销毁、无陆军、母星收益 |
| colossus_guards | 未殖民／人工／母星核心／殖民中／地面战／吞噬中／友好中立／已结算目标禁止，完成时重验资格和母星归属 |
| colossus_cancel_idempotence | 排队和取消无收益、重复事件／重载不重复结算与危机计数 |
| common_settlement | 普通与巨像 q/C/G/D/人口/容量同结算，原生损耗、所属人口与敌方人口、噬岩分支 |
| normal_dismantle_regression | 原有殖民拆解工期／种子／正常完成路径 |
| old_save_migration | 0.3.1额外星保留，不发启动奖励；现存母舰原生迁移保留身份／名字／位置／队列／损伤 |
| candidate_reload | 最终候选原生重启、载入与账本持久化 |
| repeat_initialization | 重复初始化不增加星球／奖励／舰船 |

每5级随机组件仍在接口研究中。索引 `component_rewards` 必须明确 `status=IMPLEMENTED` 或 `DEFERRED`、`interval_levels=5`、原因／限制和证据。IMPLEMENTED 必须额外包含 `random_components` case，验证真实组件、正向实效、随机发放、阈值幂等、重载和其它舰队隔离。DEFERRED 必须在正式 changelog／工坊说明中明确未实现，不允许把普通 modifier 或无面板实效的 standalone 条目冒充通过。主线程应依据用户当前授权决定是否允许带此限制发布；工具不自动作此产品决定。

### 真实组件动态升级与条件替代（本轮变更前设计）

用户最新原文与扩展研究记录见 [动态组件研究](dynamic-components-research-1019-root.md)：优先扩大互联网／原版文件调查，仅在真实硬件路线仍不能完成时接受随机共生强化。该条件授权没有允许直接省略奖励，也没有自动选中替代；不能把它填成 DEFERRED 的无条件发布授权。

当前 rc2 最小原型保留遗迹级原有五个常规辅助组件，新增专属 AUX6 并真实装备 `EEP_ADAPTIVE_SHIELD_CORE`。因此原门槛名 `five_auxiliary_slots` 会误导为总槽数只能等于5，改为 `five_relic_auxiliary_components_preserved`，明确检查保留原组件，允许额外专属槽。

真实组件验收允许“组件预先真实装备，奖励升级其动态 tier”，不要求每次奖励都增加物理槽或更换设计ID。`random_components` 除既有随机池、五级阈值、幂等与重载，还须证明：组件真实出现在原生设计；tier 0→1→2 的原生属性变化来自组件自身 `triggered_ship_modifier`；探针期间额外成长修正保持不变；没有独立外部随机奖励 modifier；跨多个阈值补齐真实随机抽取差额。普通全局成长修正仍独立存在，“无外部奖励modifier”只针对组件奖励，不等于要求全舰没有任何修正。

当前静态冻结快照与新字段解析只说明候选可试验，尚未证明动态实效、随机发放或重载。最小单护盾核心即使0→1→2通过，也只能支持接口探针；完整随机组件组还必须通过实际随机池和阈值／补差的其余检查。

若主线程依据条件授权最终采用替代，后续须单独实现 `AUTHORIZED_ALTERNATIVE` 模式，并同时绑定：原文授权的哈希归档；扩大网络／原版调查及已尝试硬件路径失败的可审查证据；主线程采纳替代的明确记录；独立 `random_symbiotic_enhancement` 实机组，核六池可见计数、真实正面属性、每5级一次随机、跨级逐份补差、R=六计数和、保存／重复同步不重抽、其它舰队隔离及不复生。正式changelog和工坊必须明确它是共生强化，不称装备栏组件。现阶段仅设计这条路线，代码不接受该状态，脚手架仍为PENDING，不能借 DEFERRED 跳过实现。

正式只允许根 `VERSION` 与 `mod/descriptor.mod` 的版本元数据变化。脚本、DDS、本地化键数量从当前生产树计算；不继承历史24脚本／101键常量。候选和正式均须 open_kaishek 整包 PASS；正式报告另以 `static-source-manifest.json` 绑定生产树与报告 SHA。其余九语言只静态检查，不列入实机矩阵。

发现既有工具未验武器 CSV 后，暂停原型实机，先由工具仓库修复并提交推送。新适配器还要求工具报告包含 `weapon_csv_files`、`weapon_csv_keys`、`weapon_csv_applicability=checked`，与当前 `common/component_templates` 下实际 CSV 文件数及唯一组件键一致且均大于零；没有这些字段的旧 PASS 不可作为 0.4.0 前置。旧版本历史测试继续保留原有适用范围，不追改成新版本。

### 原生巨像三回调合同（本轮实施前）

后续真实运行暴露缺少原生隐式排队／取消回调。`open_kaishek` 已在实现提交 `bec0c47` 及证据提交 `7a9a360` 完成并推送补正；旧 rc1b 按新检查精确 FAIL，不能继续沿用旧 CSV-only PASS。修正候选保留完成回调的 `eep.50`，只补原生 queued/unqueued 空回调；本记录不把这次静态补正称作实际发射／取消通过。

发布适配器将按本包 `common/component_templates` 中真实顶层 `weapon_component_template` 的直接字面量 `type=planet_killer` 计数，忽略 utility、注释、字符串和嵌套假定义。每个实际组件 key 必须在本包 `common/on_actions` 明确有 `on_destroy_planet_with_<key>`、`..._queued`、`..._unqueued` 三个根回调定义。只是声明投影和源绑定，不取代 open_kaishek 的 P 解析／运行时测试。

新报告必须同时具备 `planet_killer_callback_contract="native_completed_queued_unqueued_v1"`、`planet_killer_callback_applicability="checked"`，组件数等于本包实际计数且大于零，`planet_killer_callbacks_required=实际组件数×3`，`planet_killer_callbacks_resolved` 必须等于 required。当前一组件意味着三个回调，但工具不固定一组件，也不固定总P脚本或本地化键数。缺字段、旧合同、未检查、漏回调以及已校验后本包实际回调缺失，全部拒绝。测试需覆盖正确一／多组件、旧CSV-only报告、错误计数、漏定义与伪造文本定义。

正式条目必须先有六类 changelog；Change Note 仅由该条目生成且以 `[v0.4.0]` 开头。保留4条历史不可变正文图URL和6个有序图库位置；图库原位保留或替换，禁止全删重用旧图。WS-06 必须换成最终候选的单母星原生开局图且采用新文件名，避免旧文件名触发保留协议；源图和 SAV 必须纳入最终 case 证据。远端验证还须检查历史图片地址仍可访问，远端全包逐文件匹配后才可创建／推送 `v0.4.0`。

## 最终索引的生成方法

只有实际检查完成后由验收主线程整理索引；工具不生成 PASS 模板，也不从单元测试提取证据。根目录均指 `eat_everything_origin`。

### 待验脚手架设计（先于实现）

新增 `scaffold-index` 离线命令，默认输出 `docs/evidence/1019-requirements/final-result.pending.json`。只采集当前候选版本、原始 descriptor、生产文件及树摘要；顶层、所有 case 与组件状态一律为 `PENDING`，所有检查值为 `null`，预算与成长观测为空。生成18个待验组（17组基础要求加用户要求的每5级随机组件组），明确这只是任务清单，不能作为实测报告。不会预设 `DEFERRED`，更不会预设任何 PASS。

可选 `--reference-plan` 只导入项目内实际文件的引用、run_id 和证据类型，重新计算每个实际文件的 SHA256；禁止 plan 提供状态、检查结果、预算数值或成长观测。即使引用的静态工具报告已有 PASS，生成的验收索引仍保持 PENDING。脚手架只保留事实出处，不推导原生动作成功。

重复生成的保护：输出仅限本项目 `docs/evidence` 内部，禁止直接写正式 `final-result.json`，也不能写入 `mod`。带内容摘要且未被修改的本工具 PENDING 草稿可以刷新或原样重复；发现手工填写、验收结果或其它来源的文件就拒绝覆盖，让实际证据不丢失。生成不含时间戳，同一生产树和引用计划应得到相同字节。

从仓库根目录执行：

```powershell
python eat_everything_origin/tools/publish_1019.py scaffold-index
python eat_everything_origin/tools/publish_1019.py scaffold-index --reference-plan docs/evidence/1019-requirements/reference-plan.json
```

第二条命令的路径相对于 `eat_everything_origin`。引用计划是实际证据路径清单，可按下列形状整理；示例路径需替换为确实已归档的文件，缺失文件会使生成失败：

```json
{
  "static_report": "docs/evidence/1019-requirements/candidate-open-kaishek.json",
  "runs": ["docs/evidence/1019-requirements/final-run/manifest.json"],
  "cases": {
    "hive_startup": {
      "run_ids": ["实际run_id"],
      "evidence": [
        {"path": "docs/evidence/1019-requirements/final-run/start.sav", "kind": "native_save"},
        {"path": "docs/evidence/1019-requirements/final-run/start.jpg", "kind": "screenshot"}
      ]
    }
  },
  "component_evidence": [],
  "archives": []
}
```

计划可以先不列任何证据。输出中的期望语言／EXE／profile和 `_scaffold.required_growth_samples` 仅描述要求，所有实际检查仍为 null；不能据此声称游戏已按该配置启动。最终验收线程需补真实预算、观察与实际通过结论，删除或保留 `_scaffold` 注释均不影响严格验收规则，只有完整真实证据才能通过 `check-runtime`。

### 门槛复审与范围修订

17个基础组覆盖单母星、开局经济、母舰配置、成长、原生巨像和共同结算，并保留旧档／回归。复审后补足原先较宽的检查名：正确母星类型、22防御及遗迹级原有五个辅助组件保留／参照面板指标／原优势保留、成长报告 C/L/余量、本国非核心殖民星的实际发射、无效目标不增长、旧档布局和民用队列保持、重复初始化不增队列。它们仍须实际原生证据，不能由只读数学 checker 的局部通过自动扩为整组通过。

组件没有实现时，`DEFERRED` 只是事实分类，并不表示用户接受。最终发布门禁还必须绑定明确用户范围变更授权的归档证据；没有该授权，披露“未实现”也不能发布。默认脚手架不生成授权对象。无授权时继续实现／验证或向用户如实汇报实际边界，不把工具允许解析的状态当作授权。

### 整理实际验收索引

1. 将原生运行 manifest、SAV、截图／OCR、动作、完整日志、分析以及 open_kaishek 报告复制归档到 `docs/evidence/1019-requirements`，保留原字节和原始 FAIL。引用为 `{path: "docs/evidence/...", sha256: "64位小写哈希", kind: "证据类型"}`；不要把外部 AppData 绝对路径放进引用。manifest 内容中的历史绝对路径保留原样，不用于重新读取外部证据。
2. `production_files` 是最终候选 `mod` 的相对路径→SHA256字典；`candidate_descriptor` 用 `read_bytes().decode("utf-8")` 读取，保留 CRLF，避免 `read_text()` 自动规范换行改变证据；`production_tree_sha256` 直接取原生 manifest 的已核对树摘要。顶层还需 `schema`、`status`、`version`（实际 rc.N）、`formal_version="0.4.0"`、`language="l_simp_chinese"`、`game_exe_sha256`、`profile_id`、`enabled_mods`、`fully_accepted_civics=[]`。
3. `static_gate={report: 引用, production_files: 候选字典, production_tree_sha256: 候选树摘要}`。`runs` 为最终候选 manifest 引用列表；这些 manifest 的 `static_gate` 必须保留实际工具报告 SHA、版本与源树绑定。
4. 依 `publish_1019.CASE_CHECKS` 创建17个 case；每项为 `{status, production_tree_sha256, run_ids:[实际run_id], checks:{强制检查名:true}, evidence:[引用...]}`。只有实际通过的检查才可置 true。多组可以引用同一真实证据；每组必须具备五类来源，分析中明确支持了什么，不能用仅有配置页替代实际跃迁或武器发射。
5. `economy.{hive,machine,purifier}.{baseline_months,candidate_months}` 各为12条 `{date:"2200.02.01",net_energy:真实净值,evidence:原生SAV引用}`。日期从实际首个有效预算月起，按连续12个月升序；开局无有效预算的 2200.01.01 不计入12月。每组12个独立SAV，不复用基线为候选，候选SAV还需出现于本分支 economy case。候选每月净电须有限且非负，基线允许负值。
6. `growth_samples` 必须准确为 C/L 的 `0/0,9/0,10/1,19/1,20/2,200/20,10000/1000` 字典列表，每项用 `C`、`L` 两字段；对应原生分析仍列入 unlimited_growth 的证据。`component_rewards={status,interval_levels:5,reason:实际结论,evidence:[引用...]}`；若 IMPLEMENTED，再加入由 `COMPONENT_CHECKS` 定义的 random_components case。DEFERRED 的公开披露必须明确包含“每5级随机组件未实现”，且须另有 `release_scope_authorization={decision:"USER_APPROVED_SCOPE_CHANGE",evidence:[明确用户授权的归档引用]}`；主线程须先向用户如实报告方案选择，不得把门禁允许披露等同用户接受未完成。
7. `archives` 是其余完整归档／索引引用列表。执行 `python eat_everything_origin/tools/publish_1019.py check-runtime` 只读校验；失败就补实际证据或修复实现并重测，不能为越过门禁填造 true。

### rc3 PENDING进度副本与低误填更新器（实施前）

在已推送检查点 `2e020d137` 基础上建立 `docs/evidence/1019-requirements/rc3-runtime-progress-v1.json`，绑定冻结rc3树 `178d3021fa53dd999b5537e1e58f7b59c7138232e7a7fe4fe53327b3dff8e116`、已通过三回调合同的静态报告与source-copy，以及真实run `20261019T092935Z` 的不可变manifest原字节副本。基线从已提交 `1019-baseline` 的三分支各12份原生SAV及economy观察报告读取，保留原有负值和旧profile；不是候选经济通过证据。所有case、组件奖励和顶层状态仍为PENDING，所有未经评审的check为null，成长观测留空；硬件完整报告由验收线程另行完成，不提前引用不存在文件。

新增 `tools/runtime_index_1019.py` 仅更新PENDING副本，避免主线程手工维护SHA、case名和月度字段。命令负责添加真实run、按类型挂证据、从原始economy观察报告导入日期／真实净电及对应SAV SHA、记录明确的单项观察结论、列出缺项。导入负电时保留负值，不改成零或通过。每次更新保留前一副本SHA与操作记录；同一证据路径若已绑定不同字节就拒绝覆盖，真实报告应另起版本。单项结论必须绑定分析报告，更新器不推断该分析是否足以证明整个组。

副本及 [逐组填写步骤](evidence/1019-requirements/rc3-runtime-progress-fill-v1.md) 已生成。它复用验收线程稳定的 `1019-rc3-hardware/manifest.json` 与归档索引，记录硬件v2报告的真实 `PASS_SCOPED` 和限定scope，但没有映射任何check为true、没有把受控护盾探针升为完整随机组件通过。三组基线各12条已按聚合观察中的实际save SHA导入；候选均0月，18组全部PENDING，成长观察仍为空。原始预测FAIL在archives和限定观察中留痕。

辅助更新器8项合成测试通过（2.465秒），覆盖不晋升、冻结源绑定不改、证据幂等／篡改、旧run及错误静态gate拒绝、负预算原值保留、最终路径和非PENDING文件保护。实际副本89次引用／49个唯一文件已递归校验；基线重复导入返回 `changed=false`，没有改写副本或制造候选观察。该验证不属于实机验收。

更新器不能写 `final-result.json`，不能把顶层、case或组件状态改成PASS，不能写入生产目录，也不能改非PENDING索引。报告齐备后仍需人工审查真实适用范围，再另建正式索引并通过严格发布门禁。补充测试覆盖状态不晋升、无证据／未知key／旧run拒绝、预算来源哈希与负值保留、重复添加幂等、证据字节篡改拒绝和最终路径保护。

## 验收标准

- 离线单元测试覆盖完整合成输入以及缺组、失败状态、错误语言／EXE／生产树、证据篡改／路径逃逸、预算不足／负值、组件范围含糊、候选内容漂移、动态脚本与本地化数量、正式报告绑定及 WS-06 旧图拒绝。合成输入不得写入生产证据目录。
- `python -m unittest discover -s eat_everything_origin/testing -p 'test_publish*.py'` 应保持历史版本测试，并通过新增测试。
- 没有真实最终索引时，门禁必须拒绝，不能自动制造 PASS 索引。
- 完整发布顺序为：候选实测归档 → 索引校验 → 正式版本/changelog/工坊素材 → 正式 open_kaishek/record-static → prepare → 提交推送冻结输入 → preflight → 最后上线并上传 → 独立下载/verify → 逐字节、文案和图片确认 → 标签 → 恢复离线。子任务不执行该序列的外部操作。

## 实施与验证记录

已新增独立适配器和合成负向测试，未改旧发布实现。所有合成输入只存在于临时目录，不写到生产证据树。适配器通过上下文恢复旧模块全局量，历史0.3.1/0.3.2测试继续独立运行。

第一轮新增20项门禁测试通过，连同历史发布测试共33项通过（28.740秒）。加入 CSV 专项和标签前媒体／独立下载绑定后，最终新增22项／发布总计35项全部通过（31.184秒）；命令为 `python -m unittest discover -s eat_everything_origin/testing -p test_publish*.py`。已有图库原位协议12项测试通过（0.681秒），命令为 `python -m unittest discover -s eat_everything_origin/testing -p test_workshop_images.py`。

后续复审补齐具体检查项、DEFERRED显式用户授权门禁和 PENDING 脚手架后，新增门禁共28项通过（24.594秒），连同历史发布适配器共41项通过（31.713秒）。脚手架验证覆盖：状态始终PENDING、无预测预算／成长观测、引用真实字节、不导入检查结果、重复字节稳定、可刷新未编辑库存、手工／PASS证据不覆盖、正式索引／生产目录不能写入。实际当前树的只读内存生成也得到0.4.0-rc.1、18个待验组、全部checks为null、组件PENDING、原生run和成长观测均为0；没有写入生产验收证据。

动态硬件复审将“五个辅助槽”改为“保留五个遗迹级辅助组件”，允许额外AUX6；加入真实装备、组件自身动态加成、无外部组件奖励modifier、tier0→1→2、探针成长修正固定、跨阈值补差的强制检查。新增3项专项合成测试证明6槽不会被数量门槛误拒、旧宽泛检查不能替代真实动态证据、条件替代授权不自动选中备选；本适配器31项通过（25.674秒），连同历史发布适配器44项全部通过（33.040秒）。这些只证明门槛工具行为，不证明当前rc2原型实际组件生效。

三回调合同补正后新增3项专项测试，适配器34项通过（29.678秒），连同历史发布适配器47项全部通过（37.484秒）。正例包含一／两真实planet-killer组件与对应3／6回调；反例覆盖旧CSV-only缺字段报告、旧合同、错误／非整数／未解析数量、缺实际回调、注释／字符串／嵌套伪定义。utility及六核心扩展不会误增planet-killer计数。测试仍只验证静态门禁，不宣称原生发射、排队或取消行为通过。

只读当前生产树发现旧 AppData 根 candidate-open-kaishek 报告为33脚本/108键，而并行修改后的树已到34脚本/114键，新门禁正确拒绝这份过期报告。该数量是当时观察，不是最终冻结值；prototype-rc1另有自己的冻结快照与报告，未启动。最终实机需等 CSV 工具修复验证、提交推送后重新冻结、检查与启动；没有最终运行索引，不宣称0.4.0实机通过或发布完成。

### Changelog 只读审查

当前顶层是 `0.4.0-rc.1`，六类条目齐备，明确“开发中”“尚待实测”“未上传”，没有宣称正式0.4已发布或完整通过；目前不存在正式0.4.0条目，所以正式发布门禁会拒绝。建议最终条目根据真实最终候选重写验收与限制，明确三类12个月、原生发射／迁移／重载和组件实际范围；非中文只写“静态校验通过／运行时不在范围内”，不能把旧中间候选或局部checker通过写成0.4整组通过。CSV缺口补正前后的报告应区分。此次审查没有修改 CHANGELOG。

### rc3 开发检查点的暂存字节审核

[开发检查点字节审核](evidence/1019-requirements/checkpoint-byte-audit.json) 只针对暂存字节和待验发布口径，状态 `PASS_CHECKPOINT_SCOPED`，不属于游戏验收。原始检查点1151文件中曾有38个工作区／暂存字节差异，均为CRLF转LF；其中30个文件的原始完整文件SHA确实被暂存的运行manifest或本地化QA报告引用，另有调查JSON也应保真。

主线程给调查JSON、本地化JSON、被引用README／旧任务文档／帝国夹具加 `-text`。普通 `git add` 未强制重新clean未变stat的旧blob，随后主线程定向执行 `git add --renormalize`。最终34个保护范围文件的工作区／暂存原始字节及SHA全部一致；剩余5个普通文档／工具文本的行尾规范化没有命中任何暂存原始SHA引用。审核使用 `git cat-file --batch` 原始blob与 `read_bytes()` 比较，避免文本管道再转换。

`git -c core.whitespace=cr-at-eol diff --cached --check` 剩余335处／23文件，全部来自 `docs/evidence` 原始日志或源快照；非evidence源码／文档问题为0。保留原始空白，不修剪证据。60个生产暂存blob仍逐文件精确匹配冻结rc3 gate，没有修改Mod。

暂存 VERSION 和 descriptor 都是 `0.4.0-rc.3`；CHANGELOG／README／工坊文案明确开发候选、尚未发布与实机待验。没有正式0.4条目、最终运行索引、0.4发布凭据或本地v0.4.0标签。可提交开发检查点以保存实现和证据，rc3完整实机仍为PENDING，不宣称发布或功能验收完成。
