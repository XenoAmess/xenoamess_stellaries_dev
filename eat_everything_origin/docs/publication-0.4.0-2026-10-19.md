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

早期发现既有工具未验武器 CSV 后，暂停原型实机，先由工具仓库修复并提交推送。当时适配器要求 `weapon_csv_files`、`weapon_csv_keys`、`weapon_csv_applicability=checked` 与实际CSV计数对应且大于零。该“必须有CSV”要求已被下方PK数值载入合同修订取代：0CSV的真实TXT数值来源合法，CSV语法PASS本身不证明引擎加载。旧版本历史测试保留原有适用范围，不追改历史证据。

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

### rc3 机器经济 PENDING v2 导入计划（实施前）

保留已提交 `f6efa25c1` 的 `rc3-runtime-progress-v1.json` 原字节及 SHA `bdb014317a1c7d606e2b984b448e22a4cec7291c232f8c009ebfd095d89e93e4`，另建 `rc3-runtime-progress-v2.json`。待验收线程完成独立机器经济归档、给出稳定索引后，先核验索引列出的全部原字节与冻结 rc3 manifest／静态报告，再使用既有 `runtime_index_1019.py` 导入机器分支十二份月度原生 SAV 及其原始 `OBSERVATION_ONLY` 预算报告。原始开局、实际干净重载起点与年末 UI 存档分别留痕，不把硬件探针状态作为经济起点。

单项 check 只映射归档报告明确证明的同义事实；报告仅有“非负”不能据此填写“恰为200”，单一人口读数也不能证明人口没有损失。未能证明的开局检查及禁止补贴／关岗位／解散舰船等操作约束保持 null，待补齐对应分析。年末十项原生经济字段一致只作为限定观察，不扩大为完整 gamestate 一致或完整重载通过。所有 case、组件交付与顶层继续 PENDING，成长样本保持原状。

独立归档中的动作、截图、原生存档、audit、receipt 和分析可按实际类型引用；不把硬件早期日志挂为经济全程日志。活动 run 的完整日志仅在最终冻结后补入，当前明确保留缺项。输出记录 v1 父副本 SHA、稳定归档引用、逐项映射依据、预算日期／净值与完成／未完清单；递归核对所有新增引用并执行 helper 的只读 `missing`。本次只整理证据，不修改 Mod、版本、正式 changelog，不进行 UI、Steam、tag、提交或推送。

机器独立归档稳定后已完成上述 v2：344份归档与原来源／21,084,334字节全部一致，归档28项范围与字节检查成立。实际导入12个连续月预算，记录开局5项及经济3项明确观察；`initial_energy_200` 使用精确200的原始开局及干净anchor双重检查，未由“非负”推断。其余6个机器单项仍为null，两组缺完整冻结log，18组和组件／顶层仍全PENDING。v1 SHA及已提交blob未变；v2 SHA `bd79e70d3ca2ad1f4149d1ae1d0fab1d273a6076ab86994726d4d29dad9d18c9`，208次引用／122唯一文件逐字节核验。既有最终运行时门禁按预期拒绝PENDING副本；详细映射、可重复命令及未完项见[机器经济v2填写记录](evidence/1019-requirements/rc3-runtime-progress-machine-v2.md)。没有改工具代码或生产Mod，没有补造日志或最终结论。

### rc3 机器六项限定补证 PENDING v3 计划（实施前）

保留 v1／v2 原字节，从 SHA `bd79e70d3ca2ad1f4149d1ae1d0fab1d273a6076ab86994726d4d29dad9d18c9` 的 v2 另建 `rc3-runtime-progress-v3.json`。稳定扩展归档 `1019-rc3-machine-economy/archive-index-v2.json` SHA `350a6e3a8d04f71d00dfc7e8891ef09eb28fa1a79384dc93e22d5eb658feac6f` 包含原344份未变文件和14份补证；先核验358份原字节、父索引与9项归档检查，再由既有 helper 导入操作约束报告的六个明确 claims。逐项保留报告原始 scope 和全部 limitations，不能只保存一个 true。

人口比较明确为同preset历史原生母星4800与rc3母星4800，旧赠品星100另列，不称纯原版对照或全年人口恒定。正常维护保留非零原生成本及原有Mother舰队优惠，不称完全无优惠。无交易补贴允许正常native logistics trade收入；操作约束只涵盖记录的执行路径和采样边界，不称连续系统输入监控。机器开局／经济单项虽可补全，两个case及其余case、组件、顶层仍PENDING，等待最终活动日志与共同审查。Hive尚无阶段归档，本轮不挂；危机奖励校准也不列为原生巨像发射证据。本轮不改生产／工具／版本或历史进度副本，不操作UI／Steam／Git提交。

v3补证已完成，SHA `c6dd8394f34d530934894c00630040705552d64d7dc2aac5aeb6efe3b679b365`。358份payload／22,662,741字节与来源一致，旧344份未改；新索引231次引用／126唯一文件全部核对，六项scope及limitations原样携带。机器两组全部14项单项已记录true，仍缺最终冻结log与共同审查；18组、组件和顶层仍PENDING。其余16组、预算及候选源未改，v1／v2保持原SHA，最终门禁仍拒绝该PENDING副本。详细范围和复填步骤见[机器六项v3记录](evidence/1019-requirements/rc3-runtime-progress-machine-v3.md)。

v4归档审查已完成：[设计及剩余硬门槛](evidence/1019-requirements/rc3-runtime-progress-v4-review.md)／[字节审核](evidence/1019-requirements/rc3-runtime-progress-v4-byte-audit.json)。发现v2／v3重复登记同一run_id的两份等字节manifest；仅在新v4保留canonical硬件manifest为唯一runs项，Machine副本留archives，历史副本不改。实际最终验收器的manifest AST条件已分别对v3／v4真实元数据求值，重复拒绝条件得到修正；最终PENDING门禁仍拒绝。v4 SHA `6f62ec128741ae936387d980d801ea22e91ff125be90c6dd80f5b4c4855b1116`，246次引用／133唯一文件均匹配。pk1的53份独立手工奖励校准仅入archives和限定观察，保留strict FAIL，不填巨像case。Hive首月23＋10及三份原生来源当前字节一致，但缺阶段归档，未挂v4。Machine358份及全部预算／检查／scope、18组PENDING不变；当前无正式final-result，也未进行发布操作。

Hive独立首月归档完成后已生成v5：[范围及填写记录](evidence/1019-requirements/rc3-runtime-progress-hive-v5.md)／[字节审核](evidence/1019-requirements/rc3-runtime-progress-v5-byte-audit.json)。289份／16,250,350字节、三SAV及全部来源绑定独立通过；v5 SHA `6d648d959be464743ba981f1a7e59886952ef6069e27669927efd8e98294b21b`，291次引用／157唯一文件均匹配。增加5项Hive开局事实和首月1/12实际预算，全年checks仍null；18组、组件和顶层全PENDING。runs唯一canonical，v1—v4未改。并行migration修复使当前checker与归档ba178470旧快照不同，已单列源漂移，未改历史报告／工具字节，也没有将新工具行为冒充旧结果。仍缺Hive人口／维护专证、全年月份和完整日志；最终门禁继续拒绝PENDING。

v5收口时主线程发现原生PK排队至完成时长与90／30设计不符，正在调查独立命名CSV及引擎载入合同；原因未确定，新的Mod验收已暂停，须先解决工具／合同再继续。v5只含既有Hive限定观察，没有导入本轮发射过程或晋升PK case。可能的新RC必须使用实际新源／新gate／新运行绑定；RC3历史原SHA不改，也不冒充最终候选通过。

### PK数值载入合同门禁修订（实施前）

真实原生时长异常说明“CSV语法可解析”不足以证明数值已被引擎载入。下一轮只接受open_kaishek新合同明确证明的PK数值来源；合同字段／枚举／计数以工具线程最终实现为准，未定字段前不推断为通过。RC4目标源形状为实际TXT顶层weapon组件内的 `windup={min=90 max=90}`、`total_fire_time=30`、`power=0`；任意命名CSV不得据语法PASS充当已载入来源。CSV本身可以为0，不再以“至少一个CSV／key”作为0.4运行前置。

实现将抽出发布适配器中的数值载入合同校验，由 `runtime_1019.prepare_1019` 与发布静态门禁共用；保留实际顶层planet_killer组件计数和三个原生回调绑定，不固定总脚本／本地化／所有组件数量。CSV存在时仍按实际文件数／唯一key校验其语法覆盖报告，0CSV使用工具明确的无文件适用性；语法覆盖与数值载入是两个证据边界。旧RC3报告缺少新合同，必须在运行准备创建任何新用户目录／manifest前拒绝，也不能进入正式发布静态门禁。

定向合成测试覆盖：真实TXT inline且0CSV通过、旧CSV-only报告拒绝、缺合同／错枚举／非整数或错误数量／未解析条目拒绝、源码实际数值或组件集合与报告不一致拒绝、多个PK及原有三回调继续按实际计数；若工具支持固定路径CSV来源，再按明确合同增加独立用例，不根据任意文件名自行认定加载。新增runtime prepare测试以fake base和临时目录验证拒绝发生于原prepare之前，绝不导入真实UI／启动游戏／改AppData。历史0.3.1／0.3.2适配器测试保持原行为，旧归档报告／工具字节／原型不修改。

外部open_kaishek修复必须在其仓库测试通过、提交并推送后，才由主线程创建新候选和恢复实机；本工具修订及其单元测试不宣称当前原生发射、90／30时长或新RC验收通过。生产Mod由其专属线程修改，本线程只改运行／发布门禁及相应测试和文档，不操作UI／Steam／版本／提交。

工具线程已确认稳定合同字段：`planet_killer_numeric_contract="native_csv_or_literal_txt_v1"`、`planet_killer_numeric_components=N`、`planet_killer_numeric_resolved=N`、`planet_killer_numeric_applicability="checked"`；N为本包真实PK独立键数，非bool整数，必须与三回调合同计数一致。`weapon_csv_loader_contract="native_fixed_paths_v1"`、`weapon_csv_unsupported_files=0`；仅Mod根相对路径 `common/component_templates/weapon_components.csv` 和 `.../mutation_weapon_components.csv` 受支持。0CSV要求实际0计数及 `not_applicable_no_weapon_csv_files`，有CSV仍要求checked和精确计数。

`planet_killer_numeric_sources` 必须每个已解析PK键恰一项，key集合与本包一致，来源kind仅 `literal_component_txt`／`native_fixed_csv`／`mod_fixed_csv`，path为绝对原来源路径（允许不同构建／复制目录），line为正整数，SHA为64位小写。values恰含 `windup_min`、`windup_max`、`total_fire_time`、`power`，均有限非bool数值；前三非负，power可负，允许90／0哨兵且不检查max≥min。Mod来源通过实际包内对应文件SHA绑定，不强迫旧source报告路径等于copied目录；native来源独立校验原路径SHA及固定CSV路径，不假设它属于Mod。数值不在门禁硬编码成90／30，实际时长仍待后续原生验证。

CSV中的键关联继续由open_kaishek的native＋Mod定义解析负责，根门禁不再要求所有native键在Mod TXT重声明。固定CSV的定向正例只覆盖原生直接定义的 `PLANET_KILLER_CRACKER` 与EEP键；不扩展完整原版表的宏／inline生成定义，已有有限解析限制继续明确FAIL，不为本轮RC4新增白名单或豁免。合成RC4形状夹具为59文件／0CSV／四实值90、90、30、0，59只属于测试夹具，不成为生产数量常量。

本轮实现及离线验证已完成：发布适配器提供两个共享纯校验接口 `validate_weapon_csv_contract(report, mod_path)` 和 `validate_planet_killer_contract(report, mod_path)`，后者同时校验实际三回调与新数值合同；`runtime_1019.prepare_1019` 在原prepare创建运行目录之前调用二者。growth collector已由其线程接入相同接口。Source路径允许原构建／复制目录不同，通过包内实际对应源文件SHA绑定；native固定CSV允许位于Mod之外。根门禁不重新实现原生P数值解析、键语义关联或宏展开，工具报告SHA及原prepare的gate／tree校验继续保留。

发布适配器及历史版本合计54项测试通过（51.392秒）；新增fake-base prepare4项通过（2.141秒），pending helper8项通过（3.589秒）。固定CSV正例按收窄范围改为原生直接定义key后，2项相关测试再次通过（1.044秒）。覆盖0CSV59文件、inline90／90／30／0、90／0哨兵与负power、多PK、缺合同／旧合同／bool及不完整计数、来源key／kind／path／SHA／finite形状、实际源漂移、Mod固定CSV含native未重声明行、原生CSV独立来源、任意CSV拒绝及原prepare前拒绝；所有合成夹具仅在临时目录，不是实机PASS。

还对不可变RC3报告SHA `a5054bd863896d2cf842402c544ebde7f5a823d01f6a1589c5b0c0d5b709d96f` 与其原copied_mod执行两项只读拒绝检查，分别得到 `matching supported native weapon CSV loader contract required` 和 `matching checked planet-killer numeric loading contract required`，报告原字节保持不变。外部工具完整构建／提交／推送由其线程完成后，主线程才能重新gate并启动RC4；本记录未创建新正式PASS报告、未启动游戏、未修改Mod／原型／旧证据，也未提交或上传。

外部工具实现 `2c8f8a9fe7e8a9d27c910a4c21adcfef840c76f2` 及证据提交 `9a286b9321a4d1ecacc0680a8bb0d914e0679b99` 已推送。根独立冻结报告 [rc4-open-kaishek.json](evidence/1019-requirements/rc4-open-kaishek.json) 的原工具字节SHA为 `2e249c08bb39a4e30ff9d2f3eea0983a5684b328bc5018b069002df38315f20d`；外部 `D:/workspace/open_kaishek/docs/evidence/stellaris-pk-numeric-source-2026-10-19/candidate-rc4-package-report.json` 后续统一LF后的canonical SHA为 `7c0c4ffcc48206d205083e6c52ad9fdd9d4bc1ca45e291c43dbd6f57c23113b1`。两者分别针对实际冻结candidate-rc4/mod通过根 `validate_static_report`：59文件／36P／131keys／0CSV／numeric1/1及literal90、90、30、0来源符合新共享静态合同，校验没有改任何报告字节。该核验不调用prepare或游戏，也不证明90／30原生时长或最终RC4实机通过；新gate／实机由主线程执行。

主线程在外部证据统一LF前，已将原工具输出SHA `2e249c08bb39a4e30ff9d2f3eea0983a5684b328bc5018b069002df38315f20d` 独立冻结进本项目与artifact，运行 `20261019T112808Z` 的manifest／gate绑定的是该2e原字节副本。外部证据提交后的canonical SHA为 `7c0c4ffcc48206d205083e6c52ad9fdd9d4bc1ca45e291c43dbd6f57c23113b1`，不能据此改写既有root gate／报告／manifest。设计新增独立 `rc4-open-kaishek-report-link-v1.json`：只读比对root两份原字节、external canonical及run绑定，验证JSON语义相等且差异仅CRLF→LF，分别记录两个有效来源身份；不改任何被引用文件，不要求重启或重验相同Mod，也不把静态关联称作运行时通过。根证据继续由已有-text属性保留原字节。

[独立报告关联](evidence/1019-requirements/rc4-open-kaishek-report-link-v1.json) 已生成，SHA `381cfe922135d8c5858a7bd2e5a9d211e811895c21d120e925ebf7ed60a25d14`，9项核对成立。root项目／artifact两份2e报告字节完全相同；2e共2386字节、含64处CRLF，转LF后恰等于external7c的2322字节，JSON语义完全相同，无其他差异。运行 `20261019T112808Z` 的manifest及gate仍绑定2e、rc4树06485dc…；未改gate／报告／manifest，未重启或重复实机。Git text属性为unset（-text），实际filtered／raw hash-object相同，根副本会按原字节入Git。外部格式规范化不改变既有run的静态证据身份；此关联本身仅为 `PASS_REPORT_LINK_ONLY`，运行时验收继续PENDING。

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
