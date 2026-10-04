# 全特质架构机制的实施依据与边界

日期：2026-10-04。承接[实施记录](feedback-redesign-implementation-2026-10-04.md)与[机制设计](../../docs/shishan-code-origin-trait-synergy-design-2026-10-04.md)。用户授权开发及基本程序性验证，禁止游戏、GUI、屏幕输入和截图；本记录先于新增机制脚本建立。

## 已确认的本机 Stellaris 脚本能力

只读来源为本机游戏 `common` 目录和此前生成的 `Documents/Paradox Interactive/Stellaris/logs/script_documentation`，本轮没有启动游戏生成文档。

| 来源 | 可确定的能力 | 本次用途 |
| --- | --- | --- |
| `effects.log:6092`、`triggers.log:4701` | `every_trait_of_species` / `count_trait_of_species` 遍历当前物种实际持有的特质，支持人口组和物种作用域。 | 不按费用、正负、标签或 hidden 过滤，避免只枚举奖励池。 |
| `effects.log:557`、`effects.log:5665` | 触发器数值导出与国内人口组迭代。 | 按国内人口实际数量计算特质加权平均。 |
| 原版 `scripted_effects/00_scripted_effects.txt:5145`、`script_values/00_script_values.txt:3106` | `trigger:pop_amount` 数值读取。 | 每个人口组使用相同实际人口单位，无人口组计数或劳动力替代。 |
| `triggers.log:855`、`scopes.log:130` | `is_same_species` 与 `owner_main_species`。 | 只纳入国内主谱系人口；跨国人口由国内迭代范围排除。 |
| `effects.log:528`、`:590`、`:1348`、`:1352`、`triggers.log:1236` | 变量赋值、加减、乘除、存在检查。 | 持久化 R；只派生 U、T、M，刷新不发奖。 |
| `effects.log:480` | 添加静态修正支持动态 `multiplier`。 | 已确认动态修正表达能力；不据此声称已有独立经济区间。 |

正式特质排除表目前为空：本实现只使用变量，不新造任何物种簿记特质。`trait_shishan_code`、`trait_shishan_refactored`、四个历史迭代特质与机械兼容映射均计入。统计不修改物种定义，也不改外国人口。

## 实施接口与数据合同

新增独立脚本，不修改共享奖励生成器、事件或本地化文件：

- `shishan_code_architecture_migrate_effect`：国家作用域，限定本起源。仅一次把四个历史计数的 `max(k-1,0)` 加入持久变量 `shishan_code_architecture_repeat_count`；保留旧计数与旧效果。缺失计数按没有历史重复处理；负数及非整数留下异常旗标，不擅自重写玩家历史。
- `shishan_code_architecture_refresh_effect`：国家作用域，调用迁移后重算国内真实人口加权 U。只有真实主谱系人口大于零时令 `T=U+R`，否则 U、T、增幅均为零、M=1，R 保留。刷新不增加 R。
- `shishan_code_architecture_award_repeat_effect`：国家作用域，供已验证、只消费一次的耗尽奖励结算调用；只进行 `R+1` 和刷新。凭证幂等由奖励调用方保证，不能从月脉冲调用发奖。

国家 UI 数据变量为 `shishan_code_architecture_population`（人口）、`shishan_code_architecture_trait_average`（U）、`shishan_code_architecture_repeat_count`（R）、`shishan_code_architecture_total`（T）、`shishan_code_architecture_bonus`（0.05T）、`shishan_code_architecture_multiplier`（M）。人口组临时变量在汇总后清除；国家汇总分子用于诊断，不作为独立成长历史。

## 独立产出通道调查

原版 `pop_jobs/01_ruler_jobs.txt:473` 中 `produces = { mult = value:... }` 是独立缩放资源表的真实语法，但无法用单个国家修正注入所有原版/第三方岗位；其对类别 `_add` 基值的执行顺序也不能仅靠文件证明。直接覆写全部岗位会改变兼容边界，不能无证据宣称全国岗位最终产出都乘 M。

原版经济类别 README 明确 `_add` 不继承到子类别、`_mult` 继承；这并不证明类别间乘法顺序。`planet_jobs_produces_mult` 或新命名的同类修正不能冒充独立乘算。劳动力效率已知会影响岗位维护费，同样不用于本机制。

`resource_revenue_compare` 可按经济类别读取毛收入；使用这一数值按月直接 `add_resource` 可以提供数学上的资源补贴，但不能保证岗位 UI /科研结算与真正岗位产出相同，因此本轮不把资源补贴实现为已完成的岗位机制。

数据层初版未接经济修正。主任务已先在[实施记录](feedback-redesign-implementation-2026-10-04.md#经济通道的明确回退)说明当前候选的明确回退，并向用户报告：0.2.0-rc.1 使用原生 `planet_jobs_produces_mult` 的每层 5% 加算，不宣称独立乘算完成。因此本轮新增 `shishan_code_architecture_jobs` 国家修正，每单位值为 0.05，刷新先删除旧实例、再按 T 添加永久单一实例；无国内主谱系人口时撤销。它没有岗位/人口维护费、劳动力效率、资源补发或非岗位修正。

`M=1+0.05T` 留作独立目标的诊断数值，当前加算候选的实际全量收入比例还取决于原有岗位加成，不能把 M 当作已实现的最终产出倍率。原独立乘算用例继续未完成。

## 国内奖励模板的安全修改方案

`effects.log:1792` 的 `change_species_characteristics` 只支持物种作用域，文档没有 `country` 参数。直接修改一个共享物种定义会影响其它国家，不能通过添加未记载的参数解决。

已确认的安全构件为 `modify_species`（`:854`，支持 `change_scoped_species=no` 和结果 `effect`）、`change_species`（`:1665`，支持人口组）和 `change_dominant_species`（`:1437`，`change_all` 只处理本帝国用途）。主任务奖励生成器可采用如下顺序：

1. 在国家 `every_owned_species` 范围内按 `is_same_species=prev` 筛主谱系，再明确确认该模板有本国真实人口；未应用模板和外国模板不进入目标。
2. 对每个模板按其实际特质判断新增奖励是否存在或互斥；不能只看国家主模板。
3. 保存旧模板局部事件目标，在旧模板上 `modify_species = { species=this add_trait=... change_scoped_species=no effect={save_event_target_as=新模板} }`；创建新模板，不改变旧模板的共享特质。
4. 回到发奖国家，`every_owned_pop_group` 中仅对 `is_exact_same_species=旧模板` 且 `pop_amount>0` 的人口组使用 `change_species=新模板`。国家范围先排除外国，即使其使用同一个旧模板也不改动。
5. 若国家当前主体模板恰好为该旧模板，使用 `change_dominant_species={species=新模板 change_all=no}` 更新主体指针。每个实际模板只克隆一次、全票据只结算一次，然后调用架构刷新。

`is_same_species` 是谱系/身份匹配，文档还说明 `set_species_identity` 可让物种成为同一 identity；`is_exact_same_species` 用于精确模板迁移，两者不可互换。实际执行时的迭代快照、飞升身份和人口迁移仍须后续实机验证，不能把静态构件的存在写为此完整组合已运行通过。

本轮补充上述构件的共享安全接口：物种作用域 `shishan_code_modify_domestic_template_effect={ADD_TRAIT=特质键}`，由调用方先保存国家为 `event_target:shishan_code_reward_country`；辅助接口统一把本国该精确旧模板的人口和本国领袖迁至新模板，国内主体指针相同才替换，不删除旧共享模板。`change_species` 支持领袖作用域（`:1665`），因此既有领袖的成长记录不需要重建或转移。

国家作用域 `shishan_code_architecture_refactor_species_effect` / `shishan_code_architecture_relapse_species_effect` 对实际国内主谱系模板克隆并交换 code/refactored；由国家保存上下文，然后按相同人口存在 guard 迭代。若两个状态 trait 异常共存，置 `shishan_code_architecture_state_invalid` 诊断旗标，不能让统计层悄悄掩盖异常。奖励候选同样须由实际模板判断，不能只检查空的主模板。

候选中的 `prev={any_owned_pop_group={is_exact_same_species=prevprev pop_amount>0}}` 作用域链为国家→模板→国家→人口组，此处 `prevprev` 恰为模板；国内迭代先限定人口所有权。空主模板指针只有精确对应被更新实际模板时才替换，状态机应读取明确国家状态与真实模板，不能借空模板推断覆盖。

## 程序性验收标准

基础脚本须通过包级解析；独立合同检查覆盖 800×10+200×5 得 U=9、外国/空模板不计、无主谱系人口时 M=1 且 R 保留、7/5/11/4 得 R=23、迁移重放不重复、5% 线性且没有上限。实际 hidden 计数、谱系与虚拟人口运行行为、岗位产出/维护费及长名称 UI 均未运行；不登记实机 PASS。

## 验证结果

2026-10-04：两个新增脚本分别调用 `java -jar C:\workspace\open_kaishek\kaishek-cli\target\kaishek-cli-0.1.0-SNAPSHOT.jar parse <文件>`，退出码均为 0、状态 `PARSED`、诊断为空、`roundTrip=true`。脚本值文件 308 字节、39 tokens、1 block；效果文件 5294 字节、1312 tokens、63 blocks。只是 P 语法解析，不代表状态机、所有隐含特质与实际经济行为已经运行。

同日独立算术检查通过：`800×10+200×5` 加权为 9；`7/5/11/4` 的重复部分为 23；`T=0/1/10/20/10000` 的理论系数为 `1/1.05/1.5/2/501`。三个新增文件 UTF-8、无 BOM、无替代字符检查通过。这些是合同算术和文本证据，不是 Stellaris 执行这些效果的证据。

初版解析结果对应尚未接经济修正的数据层。当前继续实施已明确说明的加算候选，结果在下方补充。没有启动游戏、修改加载目录或操作屏幕。完整包级验收由主任务统一登记，独立经济通道依旧未完成。

补充候选完成后的检查：

- 新增静态修正经 Kaishek CLI 解析通过：250 字节、23 tokens、1 block。加入国内模板克隆 helpers 后的效果脚本也解析通过：9433 字节、2228 tokens、105 blocks；退出码均为 0、零诊断且可往返。
- 通过只读导入 `shishan_code_origin/tools/validate_feedback_redesign.py` 并调用 `check_architecture`，实际 AST 的受限合同执行通过：全键样例 U=9，20% 人口增加一个特质后 U=10.2；重复层达到 10001 并验证相邻层增幅 0.05；旧重复部分 23 仅迁移一次；无人口保留 R 并撤销修正；非本起源清理残留修正而不发奖。报告明确 `economic_route=explicit native additive rc fallback`、`independent_multiplication=NOT IMPLEMENTED`、`engine_economic_effect=NOT RUN`。
- 复用相同 AST 解析器检查国内克隆结构通过：3 个克隆 helper 只使用 `modify_species`、`change_scoped_species=no`，无虚构 `country` 参数；迁移只走国内拥有的人口与领袖、精确旧模板匹配，主体替换为 `change_all=no`；2 个状态入口按主谱系及国内正人口存在判断。此项证明发出的结构满足上述边界，不证明 Stellaris 的克隆、迭代和存档迁移已经实机执行。

当前统计、迁移、无限重复奖励接口和原生加算修正均已落地；候选机制的 modifier 本地化键为 `shishan_code_architecture_jobs`，名称由主任务补齐用户指定全名，说明必须写岗位产出加算而不是实际最终倍率。三个新增脚本及本记录由主任务统一提交，未修改游戏加载目录。

## 只读集成审查

2026-10-04：审查共享事件、奖励生成器及生成的奖励脚本，未直接修改这些共享文件。

- 成功回调先消费 `*_success_pending` 再增加 n 并提供奖励；实体确认清除 pending 后旧确认重放不能再消费当前票据。奖励发放只克隆真实国内主谱系模板，清理/复发已调用国内状态克隆入口，未使用虚构 `change_species_characteristics.country` 参数。
- 国内模板候选的 `prevprev` 链与设计吻合；重抽先优先取原组选项之外，再补原组，原有候选数量不足时不发出重复键。有限池耗尽的自动 R 奖励不降低重抽冷却。
- 发现成功凭证恢复缺口：若成功旗标已保存而结算事件未消费，原月脉冲只阻止 `.11` 重开项目，没有补发 `.10/.30`；清理先处理时维护的成功旗标可能与新状态不兼容并永久残留。已提交主任务处理有效凭证恢复与不兼容状态诊断，未把未修复状态登记 PASS。
- 发现跨票据旧弹窗边界：只有 pending 布尔旗标且首都决议可重复打开同一窗口；旧弹窗的候选若恰好也属于后来票据，确认守卫无法区分。已建议主任务限制同一票据只打开一个窗口，选择/延期/重抽时释放窗口锁，或提供真正独立的票据上下文。存读档窗口持久行为仍未实机验证。

异常历史计数经实际 AST 的窄域执行再次确认：旧 `k=1.5` 保持旧值，迁移额外 `0.5` 并设置 `shishan_code_architecture_legacy_invalid`；旧 `k=-3` 保持旧值、额外量为 0 且同样诊断。重放不再迁移，不静默四舍五入或伪造修复。

白绮自身 `leaders_unity_upkeep_mult=-1` 的作用域是领袖自身，不降低其它领袖。原版 `economic_categories/00_common_categories.txt` 的 leaders 类及 `inline_scripts/paragon/leader_base_upkeep.txt` 能确认基础凝聚力维护资源表；未查到不覆盖原版资源表就能对特定领袖禁止该资源项或把最终维护强制置零的通道。存在其它正向维护倍率时，固定 -100% 不能从静态文本数学证明最终归零；不以巨量负修正冒充严格保证。原版覆盖或替换领袖 class 会扩大兼容范围，本轮不采用。实际自身维护与其它正倍率组合保持待实机验收。

## 最终集成复查

2026-10-04：针对上述成功凭证恢复与重复弹窗两项重新只读检查最新源码。`.10/.30` 现在按成功凭证且没有未确认奖励消费，跨清理/复发状态保留已经取得的维护/优化收益；`.60` 补发四类回调，已完成清理/复发状态的残留凭证留下诊断并清除，`.11` 在成功凭证未消费时不重开项目。优化的随机复发只发生于重构状态。

开窗已集中至 `shishan_code_reward_open_window_effect`，先取得持久窗口锁再调度 `.1000`；确认、延期、有效重抽释放锁，同一票据重复重开不再产生第二个窗口。但复查发现新的边界：若窗口开启后选项因人口/模板变化失效，原确认或重抽守卫拒绝时并未释放窗口锁；点击关闭窗口后票据可能无法重开。已交主任务处理，方案是确认/重抽入口先释放窗口锁，再按原守卫决定是否消费/重抽；拒绝时保持票据、候选和冷却不变，允许随后重开。此拒绝路径必须追加受限 AST 合同检查后才登记窗口锁修复通过。

本次复查不启动游戏、不操作屏幕，也不修改共享 Mod、生成器或验收器。真实事件窗口的生命周期与存读档持久行为继续为未运行。

最终修复产物已再次复查通过：

- `check_receipt_recovery` 的 13 个实际 AST 合同用例通过，覆盖维护/优化成功凭证跨状态恢复、旧票据延期、同时成功顺序结算、清理后结算维护、残留清理/复发凭证诊断；已经消费的回调重放不增加 n/R/CD 或再次发奖。情况、白绮刷新、物种克隆属于明确跳过的引擎领域，存读档未运行。
- 正常窗口合同序列通过：首次开窗、延期重开、重抽替换窗口、新成功票据的累计开窗数分别为 `1/2/3/4`，三个重复请求不产生重复窗口；确认后的旧票据不能重开。
- 追加只读受限 AST 检查通过：39 个实体确认入口和重抽入口均在守卫前释放窗口锁；模拟候选失效及冷却不允许重抽时，只有窗口锁被释放，pending、候选、n、R、CD、实际奖励保持原值，随后两个重开请求只调度一个窗口。
- 只读导入奖励生成器，以内存中的 `generate_scripts()` 对照三个已生成脚本，内容完全一致；没有运行会改写文件的生成器 `main()`。

因此两项原审查问题与此次失效选择造成的锁残留，在当前脚本结构和受限合同执行范围内已修复。该结论仍不代替真实 Stellaris 事件队列、窗口生命周期或存读档验收；独立乘算与严格最终零维护的先前限制仍然成立。
