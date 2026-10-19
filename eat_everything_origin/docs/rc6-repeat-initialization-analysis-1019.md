# RC6 完整重复初始化：独立只读报告范围

本页对应主线程已声明的 [执行合同](rc6-repeat-initialization-execution-1019.md)，定义独立分析，不另排执行。准备时样本尚未交付，原始 intake 保留 PENDING；下文结果仅在主线程确认 `r6mcyearui` 和 `r6mcinit2` 的实际 immutable native receipts 后取得。保留经济总回执/yearUI作为干净before，后者之后的完整两轮 initialize/startup/sync 属独立功能分支。

固定 RC6 树 `cc181c8a27ede295e9fcebeffc5e10bb75e9cd643edec1d194b928993ffab33a` 与 EXE `400df27c82ddc845aa9dce79bd468d81f18f060d299cd263e3afa93aef4f7a83`。实际run、日期、Mother/core身份从本轮回执和SAV取得，不复用迁移旧档数字ID。预计before为Machine2201.01.01、C/L/R与六tier0，但报告必须逐字段读出实际值，缺失不填默认0。

收到样本后各完整解析一次，复用不变 `check_1019.py`（SHA681836d2da9c6b28ee9bfd583c87e5ced96f06543901e71d3dc35fa226f3afdc）的 observe 与 compare。报告完整旧严格比较结果，不设 ignored paths；额外比较完整解析国家对象、country0原始块、所有库存（包括原生research/effective stockpile及其来源）、五经济账本与完整country/fleet/ship变量、所有开局/授予flags、人口组/岗位/殖民地/区划/建筑/zone布局、实际唯一Mother/core、全部自有fleet/ship inventory、军用/民用/招募construction queues/items（付款/成本/进度/设计/位置）。不只抄最终四个布尔字段。

原生SAV完整字节、ZIP各member及metadata、解压gamestate的SHA与逐字节相同性分别记录。若两ZIP不同，不能称全档一致；若gamestate或关键原始块不同，保留全部原始差异/完整strict，再按本合同判断，不引入损伤舍入预算或自动忽略新字段。完整country0、construction、army等原始块另列hash/相同标记；必要时保留逐行差异以覆盖旧observer未投影的原始字段。

实际输入必须证明连续两轮完整 `eep_initialize / eep_startup / eep_sync_mothership`，并绑定已完成command action/Enter及GPU/OCR原生响应；不以两SAV相同就推断命令执行，也不把layout-only helper重复或母舰死后不重生当本case。两个SAV之间要求同日，源core与唯一Mother仍有效，普通舰及全部队列维持原状态，没有待补发的组件奖励。实际出现差异、未执行证明或缺原字段均如实报告，不修改旧checker、生产、存档、UI、日志或Git。

输出独立 immutable `rc6-r6mc-repeat-initialization-observation/report/case-proposal` 新文件，给 `repeat_initialization` 的 no_extra_world/no_extra_ship/no_extra_reward/no_extra_civilian_queue 四项逐一附实际字段basis，并附全部扩展检查、raw ZIP结论、严格差异与局限。未来输入接口 `evidence/1019-analysis/rc6-r6mc-repeat-initialization-intake-v1.json` 的实际路径/日期/ID/checks保持null/PENDING，不能提前填PASS或替代正式运行索引。其它PK功能仍按其独立确认的前缀处理。

## 实际结果：完整两轮初始化，限定范围通过

run `20261019T150008Z` 的两个原生保存均为 `2201.01.01`。`r6mcyearui.sav` 与 `r6mcinit2.sav` 均为 513135 bytes，SHA256 均为 `bd4104dd2e31cfff0d2f76abf55e2eb303709ec86ca3118ec0d9fb6a59a3a696`；独立 read_bytes 比较完全相同，ZIP 两个 member 的内容及全部读取的 metadata 也相同。gamestate SHA256 为 `b0bc4531e932436e423071c3815455ba7d3d9c4845caccef3aa7dad1f3908a56`。原生 SAV 未编辑，原 checker 未改。

[完整报告](evidence/1019-analysis/rc6-r6mc-repeat-initialization-report-v1.json) 为 `PASS_SCOPED`，41/41 检查通过，原严格比较为零差异。两份完整 observe 各执行一次并验证原生 SAV、manifest、copied source、audit 和 receipt；完整报告复用这两份固定 observation 调用不变比较器，并另外读取 ZIP 和全部原始 gamestate。完整 country0、construction、army、ships、fleet、starbase_mgr、planets、colony、pop_groups、pop_jobs、districts、buildings、zones、flags 原始块均字节相同，完整解析的国家对象也相同。

实际唯一 Mother 为 fleet125/ship809，附属 starbase15；物理 core4、内部 colony0 是唯一殖民地，实际人口4854。全部12艘自有舰、10支舰队的 ID、位置、名字、实际 design、健康、变量、flags、附属基地保持不变；5条队列及所有付款/成本/进度/设计/位置、民用与军用建造/招募数据保持不变，construction items 为0。所有库存、原生研究库存来源、effective stockpile、budget类别、人口岗位与布局、五账本、country/fleet/ship全部变量与flags、危机目标进度均相同。C/L/R/pending与六类 country/fleet tier 的0值均直接出现在原生序列化变量中，没有用 observer 默认值补0。

命令 action SHA256 `8890a54a9336e340744d86e0de78e573ca96603eac56ecced08f53990c9e8afd` 记录连续两轮完整三效果；独立 Enter action 为 scan code28。实际输入 UTC16:07:31 后，UTC16:07:41 的 fresh Steam GPU 图及 OCR 显示 `Executing effect script.`，随后 UTC16:07:48 的 fresh HUD 图保持同一 PID30812。`effect-before` 名称指关闭控制台之前，其实际时间在输入之后；原生控制台显示的条件分支描述不作为持久化变量读数。临时 driver 的 `government_raw` KeyError 发生在任何输入前，独立保留失败轨迹，不当作 Mod 错误或成功执行证据。

四项发布字段仅可按 [case 提案](evidence/1019-analysis/rc6-r6mc-repeat-initialization-case-proposal-v1.json) 的明确检查映射使用。该提案包含真实输入、原始两份 native-save receipt 的角色绑定、两SAV绝对路径及SHA；同一SHA会让通用receipt发现器同时匹配多个保存名称，因此 before/after角色以各自精确的 `.native-save.json` 为准。项目内原生证据包尚未由本分析创建，提案的发布挂载仍须等待实际归档路径，不虚构相对 SAV 路径。

本次结论只覆盖已初始化的 Machine C0、同日完整两轮 initialize/startup/sync。高等级成长、母舰死亡后不重生、结算去重、旧档 layout-only 重复、真实进程重启均有各自合同和样本，不由本报告认证。完整 ZIP 相等和原严格比较零差异没有采用迁移精度预算。
