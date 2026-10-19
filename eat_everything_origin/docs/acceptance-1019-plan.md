# 1019 独立原生存档专项验收设计

## 目标与范围（先于实现）

补充 `tools/check_1019.py` 与必要的只读抽取器 `testing/inspect_1019.py`，对真实原生 SAV 提取完整母舰设计、舰队修正、变量、独立组件，以及共同拆解结算差值。复用 `audit_save.py`、`inspect_1015.py` 和 `check_single_homeworld.py`；不修改它们，不更改 Mod、UI、运行入口或存档。

本工具只能报告实际有证据的专项结果；不能据此单独宣布整个 Mod 通过。历史严格差异门禁及其 FAIL 保留，新比较保留全部观察字段差异，不把筛选后的相等伪装成完整相等。

## 证据与设计

- 每个输入必须为 ZIP 原生 SAV，并具备同目录运行 manifest、native-save receipt 和原始 audit；重新计算 SHA256，与 receipt/audit 核对。检查简中、唯一 Mod、准确 EXE SHA256、静态 gate 对应生产树和拷贝包完整性。
- 母舰按实际船名与原生 `eep_mothership0` 目标辨认。完整保存设计体、section、slot/component、required component、舰体三防原始标量、fleet/ship timed_modifier 和 variables、移动 starbase standalone_components、船坞队列及相关原始体。
- 成长核对实际 C 与 `L=floor(C/10)`，记录余量，核对单一 `eep_mothership_evolution` 的实际倍率；零级无此修正。每级具体 +5%／固定回复值应同时核对冻结生产包定义，不能从面板相对增幅倒推。每 5 级随机真实组件仍在研究，抽取器只报告真实组件，不为未实现功能发 PASS。
- 提供 before/after/reload 观察与严格差异，所有字段差异保留；另列母舰身份、位置、设计体、船坞、组件和结算变量，避免设计 ID 变化掩盖设计体变化。
- 普通与 colossus 结算使用显式 case JSON，声明路径、目标、母星、预期 q／人口／容量／危机目标差值。工具从原生 SAV 检查 C/G/D、worlds、结算和销毁旗标、真实 `pc_shattered`、容量与人口变化；巨像实际发射／无需陆军仍须原生动作与 UI/日志证据，不能由 SAV 结算结果替代。
- 无效、取消、重复与重载使用显式 no-settlement 模式，保留严格差异并专项核对奖励变量、人口、容量和目标状态不再变化。

## 验收标准与实际运行矩阵

1. 工具在旧中间候选和组件探针真实 SAV 上正确抽取设计体／独立组件，能明确报告其不是 0.4.0 最终配置，不给旧候选发最终配置 PASS。
2. 同一 SAV 自比较无差异；真实不同 SAV 全部差异可追溯。任何 provenance 缺失、输入哈希不符、未定义预期或字段缺失均明确失败／观察状态。
3. 新候选可用后执行母舰配置、C=0/9/10/19/20/200/10000 成长边界、迁移及重载、正常／巨像各一次结算、取消／无效／重复专项；证据保存至独立 `docs/evidence/1019-analysis`，不覆盖旧报告。
4. 运行检查器编译及真实 SAV 自比较／负例；不存在手写或改写 SAV，不编造成功证据。

## 独立原生夹具建议

只在专用功能夹具运行原生控制台效果，不在经济 12 月分支注入资源／变量。成长边界可在国家 0 原生 scope 设置 C 后调用生产同步 effect，然后原生保存；每个边界保留命令 action 与前后 SAV，并显式标记为边界夹具。重复同步和同日重载须独立保存。组件探针独立于经济回归。

在当前玩家确认为已自然初始化的国家0、唯一母舰及绑定目标实际存在后，可分别原生输入以下命令，把示例中的9替换为0／9／10／19／20／200／10000；执行者须保存实际输入 action、执行后原生 SAV、报告截图及 receipt：

```text
effect set_variable = { which = eep_c value = 9 } eep_sync_mothership = yes
effect eep_sync_mothership = yes
```

第一条创建等级边界夹具，第二条用于同日重复同步；重载后再运行第二条并另存，核对等级、单修正倍率和完整严格差异。这些命令只是建议，不代表已执行。改变 C 的夹具不得用于证明真实吞噬经验、D／G／人口结算或经济平衡；对应项目仍必须走实际结算。每5级组件边界可另加C=49／50，仅当真实组件接口已证明生效并接入生产逻辑后才做正向验收。

实际巨像路径应保留充能、发射、击中和目标毁灭截图，发射前／结算后／重载后 SAV；不能直接调用结算 effect 冒充发射。normal 路径保留原生殖民拆解决议、situations 工期与种子证据。

## 实施与只读调查记录

- 原生 SAV 的 `ship_design.growth_stages` 与 `timed_modifier.items` 是匿名对象列表；设计的 `required_component` 为重复标量。抽取必须保留重复组件及顺序，不能直接以普通字典覆盖。
- 已核查真实 `n17l2.sav`（SHA256 `6906414c25b908ca0a6327928bed7b1c8b128885bda880a6231a4d4a1015ba48`）：`country.0.crisis_progression` 下重复 `objective={objective="crisobj_destroy_worlds" progress=14000}`；相应原生命令为连续完成20次该目标。`progress` 是目标奖励点累计，不是次数，不能把一次销毁硬编码为 `+1`。本机原版 `common/crisis_objectives/00_crisis_objectives.txt:73` 的奖励为 `150000 / num_galaxy_systems / habitable_worlds_scale`，再按50取整且至少150。检查 case 应显式声明预期奖励点增量及其独立校准证据；工具保留目标原始体，未出现的目标按“无原生记录”列出，并在存在该危机路径时才以0参与差值。
- 对外国未标记源星，旧审计器不会自动选中；新观察必须按 case 中的显式星球ID抽取其全部沉积物／殖民地／人口，不能用旧 owned-world 集合代替源星损耗。
- 普通原生吞噬在任务开始时冻结 `eep_q`，工期内原生咬噬继续增加损耗沉积物；普通结算检查冻结 q，不在完成前再次扣当前损耗。巨像为完成时现算 q，检查发射前活体规模减既有损耗。

### 工具接口

所有命令的 `--output` 必须指向不存在的新报告文件；已有证据绝不覆盖。输入 SAV 必须与原始 receipt/audit 一致。`observe` 仅输出 `OBSERVATION_ONLY`，检查命令只能输出具体范围的 `PASS_SCOPED` 或 `FAIL`。

```powershell
python eat_everything_origin/tools/check_1019.py --output <新观察.json> observe <原生.sav>
python eat_everything_origin/tools/check_1019.py --output <新母舰检查.json> mother <原生.sav>
python eat_everything_origin/tools/check_1019.py --output <新成长检查.json> growth <原生.sav> --expected-c 10000
python eat_everything_origin/tools/check_1019.py --output <新严格比较.json> compare <before.sav> <after.sav>
python eat_everything_origin/tools/check_1019.py --output <新结算检查.json> settlement <case.json>
python eat_everything_origin/tools/check_1019.py --output <新无结算检查.json> no-settlement <case.json>
```

`observe`／`mother`／`growth`／`compare` 可重复使用 `--world <ID>` 额外抽取敌国或未标记星球。重载验证使用 after/reload 作为新的 compare 输入对；结算 case 也支持可选 `reload`，并保留完整严格差异。`no-settlement` 的专项结果与内嵌严格结果分别保留：例如经济奖励未重发也不能把原严格差异 FAIL 改为 PASS。

mother 配置对照按槽位身份及 required-component 的完整重数核对冻结设计，允许序列化顺序变化；观察报告和严格比较仍保留原生顺序及完整raw，不能因此丢失真实差异。没有供能／伤害／速度／主动跃迁实机证据时，该命令的限定结果不能替代整组母舰验收。

结算 case 的固定 schema（路径均使用真实绝对路径）：

```json
{
  "schema": "eep.1019.settlement-case.v1",
  "path": "normal",
  "before": "D:/absolute/native-before.sav",
  "after": "D:/absolute/native-after.sav",
  "reload": "D:/absolute/native-reload.sav",
  "source_world": 123,
  "core_world": 1,
  "native": false,
  "expected_q": 20,
  "expected_return": 100,
  "expected_other_core_pop_delta": 0,
  "expected_crisis_progress_delta": 700,
  "expected_crisis_empires_progress_delta": 0,
  "crisis_calibration_evidence": {
    "path": "D:/absolute/independent-one-objective-calibration.json",
    "sha256": "实际校准文件SHA256"
  }
}
```

上例仅说明接口，不是已运行夹具，不得直接把示例数值当实际预期。`path` 取 `normal`／`colossus`，`native` 指噬岩者原生收益分支。普通材料预期造人为 `100 * floor(G_after / 6) - made_before`，源星主种返还量需由原生人口校准；`expected_other_core_pop_delta` 记录跨日自然增长或原生随机造人等独立预期，禁止用它掩盖未知差额。危机奖励必须在相同银河设定内独立校准，不复用旧银河的700或1500。

no-settlement case 只需 schema/path/before/after/source_world/core_world；若用于同日取消、重复事件或重载，专项检查奖励变量、母星人口／容量、目标殖民地／星球类型、结算旗标与危机进度不变，同时内嵌保留全部严格差异。

### 已完成的真实输入验证

- `cmm01.sav`：SHA256 `9ec935d9f368e8387f8e17ac7703edf47b968b835fd57d7c9324e0315fec09ec`，2200.02.01，独立组件0个。
- `componentprobe1.sav`：SHA256 `d0c67578b01bf2c7275c4feda0a4f6633d59ddf17cc81724bd7eef0479aed0d7`，2200.02.01，SHIELD_BOOSTER 1个。
- `componentprobe2.sav`：SHA256 `cbb7fe338ef130af9de2779ad3774e2c074d4222a691aed13ecdd425fc7e7539`，2200.02.02，SHIELD_BOOSTER 2个。
- `componentprobe3.sav`：SHA256 `f34b93eea231ea76f039ff361a35ca87aa61e3104e7fadbe3a6e7e17c81fcd5e`，2200.02.03，重载后仍2个。

四档完整设计体 SHA256 均为 `2e2b4a1f0e9d1d990334152808d280abad6175b9ab7ed1997549773ccfffabb0`，重载仅设计ID从1666改为1800；max_shield_hitpoints 全为48370.608。新抽取保留每份设计体、slot/component、required列表和standalone顺序，没有把列表保存成功当作属性增益成功。

同一个 probe3 SAV 独立读取两次的严格自比较 `PASS_SCOPED` 且零差异；probe1→probe2 严格比较 `FAIL`，保留30项差异；probe2→probe3 `FAIL`，保留64项差异。原生日期本身也不相同，不能冒称同日重载稳定。旧0.3.2候选的母舰／成长负例均正确 `FAIL`，因此旧经济证据不能顶替0.4.0最终配置。检查器与抽取器 Python 编译通过。

直接读取游戏实际写出的历史 probe3 SAV（不是带manifest的归档目录）时，工具按预期因缺少同目录manifest而输出 `FAIL`；这是来源前置门禁负例，没有修改或重新打包 SAV。证据为 `missing-manifest-negative-v3.json`。

再次指定该既有 FAIL 报告为输出时，工具立即拒绝，文件前后 SHA256 均为 `54e3119cab9f957f8926ea55b7e2dcc6b886e2e3a45e6b2cc3d4675d01634a1a`，验证记录见 `existing-fail-preservation-v3.json`。该阶段检查器 SHA256 为 `15246cb596f64d060209d93d9a3b746b64bf8199d6e6774d1ebd4c126bf3eb15`；母舰负例 `oldcandidate-mother-negative-v3.json` 按预期 FAIL，同时核实旧冻结设计与原生完整loadout一致。

证据位于 [1019-analysis](evidence/1019-analysis/)。报告中的 checker／inspector SHA 标识当次运行源文件；`v1`／`v2` 历史报告不随后续工具补充而重写。当前仍未取得最终0.4.0原生 SAV，结算、成长非零倍率和新母舰配置的正向运行时验证仍待主线程实机；本页与本工具没有宣布整个 Mod 验收完成。

### 0.4.0 接口原型只读检查

主线程已启动原生简中接口原型 `prototype-rc1b`，生产树 SHA256 `e3c4c176c9b6d0fa6d43cab461d6f7dd9161cc4828ff800d78bdfc33ee7df526`，运行 `20261019T081638Z`。本轮新 `pmm00` 仅用于原生设计／成长状态与组件接口调查；冻结快照仍有已知action locale／科技图标问题，不能作为最终候选验收。新SAV、receipt、audit齐备并哈希一致后，独立抽取完整组件和三防，并运行现有 mother／growth 检查。任何限定 PASS 仅指报告列出的原生字段，不含UI／供能／伤害／速度／主动跃迁或最终发布认证。

`pmm00.sav` 已完成只读抽取，SAV／receipt／audit SHA256 一致为 `2fddab313229b4bddf493cb53fd484aa3897a4c7f163838188dead442ea6e6be`，日期2200.01.01。母星目标4、Mother fleet138／ship808／starbase19；设计1875，名称 `NAME_EEP_Baiqi_Mothership_1019`。原生当前／最大舰体93960、装甲44787.6、护盾167310，三者全满。完整设计与本次冻结包一致，十船坞队列存在，standalone列表为空。

实际44个槽位组件：TITAN_LASER×1、LARGE_PLASMA_3×7、SMALL_DISRUPTOR_3×2、SMALL_PLASMA_3×3、POINT_DEFENCE_3×3、LARGE_ARMOR_5×11、LARGE_DARK_MATTER_DEFLECTOR×11、SHIELD_BOOSTER×3、AUTO_REPAIR×2、EEP_PLANET_KILLER_DEVOURER×1。required完整六件为 JUGGERNAUT_DARK_MATTER_REACTOR、SENSOR_4、JUMP_DRIVE_1、COMBAT_COMPUTER_LINE_SAPIENT、COLOSSUS_SHIP_THRUSTER_5、SHIP_AURA_INSPIRING_PRESENCE；没有仅由脚本文本推定装载。

成长初态 C=0、L=0、距下一级10；舰队 `eep_applied_level=0`，timed_modifier仅基础 `eep_mothership`，没有进化modifier，船体也没有重复进化modifier。冻结定义核对每级四项+5%与舰体／装甲日回复各+0.1。现有 mother／growth 函数均输出具体原生字段范围的 `PASS_SCOPED`；观察／摘要保持 `OBSERVATION_ONLY`。证据 `prototype-rc1b-pmm00-{observation,mother,growth,summary}-v1.json` 均明确 `interface_investigation_only`／原型范围，不得把零级初态外推到非零倍率、真实吞噬经验、随机组件、巨像发射或最终发布验收。本轮不需要修改检查器。

### 原生组件跨日与旧档迁移检查扩展（先于实现）

新增只读分析 `aurafleet1`（2200.01.02，预期SHA256 `18bf58153e1e85c2b569107f424e6eeb5bb1e8f60f50fc96691967bb174dd683`），与pmm00并列报告Mother808和普通ship1～5的最大／当前三防、设计体与standalone组件。首日原生自动设计、原始所有者字段和国家缓存可能变化，全部严格差异保留，任何护盾变化需结合完整设计体和组件实际变化单独解释，不能自动归因于光环组件。

准备 `j13ten` 原生旧档迁移case模板，源存档仍使用真实原始归档。旧档基准是fleet146／ship822／starbase13，2200.01.12，已付款造舰队列。若需要扩展现有独占检查器，新增限定scope的migration命令：对同日伤后before、迁移后after和重载后reload核对舰船／舰队／starbase身份、名称、坐标／轨道／移动状态、全部造舰queue和item ID、实际支付resources、进度以及真实舰体损伤；保留三防当前／上限和损伤比例，明确按哪一种损伤口径验收。完整严格差异同时原样保留，设计ID变化只展示完整设计体来判断，不据ID推定配置相等。无有效受伤before或无真实after时仅出模板／观察，不能发迁移PASS。

### prototype-rc1b 已完成阶段归档设计（先于实施）

将 `pmm00` 与 `aurafleet1` 已完成阶段保存到独立 `docs/evidence/1019-prototype-rc1b/`。目标为字节一致、可追溯的原型接口调查档案，不是最终验收。归档包括运行manifest、冻结copied_mod、静态报告／源快照绑定、两阶段SAV／audit／receipt／动作／截图／OCR以及已完成阶段的相关原生操作材料；不覆盖旧归档，不更改源run。每个副本记录源绝对路径、目标路径、字节长度、SHA256与取证时间，普通静态文件复制前后哈希一致才视为归档通过。

归档根目录 `.gitattributes` 使用 `* -text`，防止文本与SAV旁证在Git中被换行归一化。静态报告所绑定生产树、manifest文件表、冻结源snapshot与copied_mod逐文件核对；归档索引明确已知action locale／科技图标问题，不能引用为最终候选PASS。

活动游戏日志只对白名单日志做一次带UTC时间的字节快照，记录读取前后文件stat及实际读取字节SHA；不遍历复制整个仍在写入的日志目录，不把单次副本称为freeze。原型阶段日志可能混入后续实验，时间／stat边界作为证据限制保留。`auraship1` 尚未收到阶段稳定通知，本轮不读取其未完成文件，待通知后追加新文件及新索引，不改已归档字节。

验收：全部静态副本逐文件与源字节SHA一致、manifest生产文件表与归档copied_mod一致；所有SAV与其audit／receipt哈希一致；Git属性验证归档下文件text属性unset；索引完整标记原型范围与活动日志的时间限制。

主线程随后确认 `auraship1` 阶段稳定（2200.01.03，SHA256 `a396ad1273536baf7ba771b6eda9f572e9002e854c9a87682afd53ab4168eac3`），因此首次归档可同时包含这三个已完成阶段；新的 `auranative1` 尚未完成，明确排除。日志快照仍保留实际读取时间，不假定其边界恰好等于Jan3的游戏状态。

已完成首次字节归档：`evidence/1019-prototype-rc1b/` 共328个源文件、18,707,356字节。`archive-index-v1.json` SHA256 `c3ecb5979b693cb9a55f4a26fb4a3b88dcdbf73d1b5a6e31f2438acb38b9efc5`，逐文件记录源／目标路径、原始长度、SHA、读取UTC时间与源stat。独立 `archive-verification-v1.json` 的8项检查全部通过，仅限字节一致／manifest与source-copy绑定／三份SAV审计receipt／Git属性范围；全部328文件text属性unset。六份日志于2026-10-19 08:40:21 UTC单次读取，索引标记 `active_log_single_read_not_frozen`，不能当作Jan3静止状态日志。原run无写入。

`aurafleet1` 对pmm00的6艘指定舰船最大／当前三防均无变化：Mother808为93960／44787.6／167310；ship1为300／100／200；ship2为300／100／300；ship3～5均200／200／100（依次舰体／装甲／护盾）。六艘设计完整body及ID均相同，Mother standalone仅从空变为 `EEP_SYMBIOTIC_SHIELD_CORE` 一项。未观察到该次探针正面护盾收益或外溢。严格比较仍为FAIL并保留95项跨日差异，不能把自动设计／所有者／缓存变化当作组件收益；报告为 `prototype-rc1b-aurafleet1-vs-pmm00-v1.json`，状态OBSERVATION_ONLY。

旧队列解析不足已确认：`construction_items.ship` 仅直接标量，因此j13ten的11件 `buildable_ship` 均显示空字典；真实嵌套 `ship_design_implementation.design=1702` 与 `orbitable.starbase=13` 只在raw中。扩展只读抽取这些嵌套体及完整设计，另补queue原始体、舰船名称／目标坐标、舰队移动／轨道和三防损伤读数。j13ten冻结descriptor实际Mod版本为0.3.0-rc.1，manifest静态gate没有version字段；测试轮次“v13”不是Mod版本，不能用该夹具冒充公开0.3.1旧档。provenance将允许从已逐文件验证的copied_mod descriptor读取缺失版本，记录来源且不修改原manifest。

主线程已通知追加稳定阶段：`auranative1`（2200.01.04，SHA256 `d6f985643b249e80239a0574c7ba2a51e45182b38a482f14c8b60b68ddb3af24`）及 `aurarebuild1`（2200.01.05，SHA256 `a5a6fbccb957953cfb278a949e7841b38cd6d2b9cbb070041cf12e0521988cd0`）。追加其原生三件套及相应已完成动作／图／OCR，增建archive-index-v2与独立verification，绑定v1索引SHA，原v1及其所有副本不覆盖。活动日志仍仅额外一次白名单快照，不称freeze。主线程报告原版BULWARK及rebuild后也未见盾增益，归档本身不为该功能合成PASS。

追加归档已完成：v2索引 SHA256 `6283a76982b781b35fd54c27bdcab59232b8391303d5714fa8b0241d4a0e1104`；新增106个源文件，累计434文件／25,602,528字节，所有副本SHA、五份原生三件套、v1索引不变及Git text属性均验证通过（仅字节scope）。初始README保持原字节，新 `README-v2.md` 解释追加边界。SHIP变体也独立抽取完毕，Mother／ship1～5三防与完整设计body均不变，standalone仅 `EEP_SYMBIOTIC_SHIELD_CORE_SHIP`；跨日严格105项差异保留在 `prototype-rc1b-auraship1-vs-pmm00-v1.json`，不宣告组件成功。

### 迁移工具与模板交付

已补齐嵌套建造设计／轨道、queue raw、舰船名称／目标坐标、移动／轨道及三防损伤读取。`check_1019.py --output <新报告> migration <case.json>` 新命令要求真实来源fixture、同日原生伤后before、迁移after，可选reload。所有输入仍执行原SAV／receipt／audit／manifest／copied_mod完整来源门禁，检查器拒绝覆盖旧证据。

模板为 `evidence/1019-analysis/j13ten-migration-case-template-v1.json`，before／after／reload明确为null、状态PENDING_NATIVE_MIGRATION_INPUTS。模板声明三防绝对损失口径，容差0.001；也支持显式 `fraction`／`current_absolute`，报告始终展示全部口径，不暗中择取有利结果。须在运行前按设计要求选定口径。没有实际受伤before，检查器必FAIL。

损伤口径边界：仅比较当前绝对HP可能把“旧上限受伤、换低上限后满血”误判为保留损伤，因此额外要求before中真正受伤的每个已选防御层，在after仍然受伤。即便当前HP数值相等，也不能把迁移变满血当作受伤状态保留。

原始j13ten已重新经严格来源门禁抽取（`j13ten-native-observation-v1.json`／`j13ten-migration-template-baseline-v1.json`），版本从已验证冻结descriptor读取为0.3.0-rc.1。真实Mother822三防101460／24429.6／48370.608全满；队列54十并发、11件护卫舰，item0～9为10/60、item10为0/60，每件记录81合金／paying_country0／orbitable starbase13，完整建造设计已提取。原始未受伤同档作为before／after的负例正确FAIL，失败项为非0.4、无新设计、没有实际设计迁移、before无损伤；不会因为自比较相等发迁移PASS。队列成本记录与迁移后资金不变只证明未二次收费／退款，最初付款仍需原始入队动作与审计，不能仅由resources字段倒推。

本轮Python编译与CLI注册通过。原始迁移负例所用检查器 SHA256 `ff2ac55a190e9b29c3f899c2d38ed5548493d980c32466d647d30516fd11c819`；补充“受伤层不得变满血”保护后的检查器 SHA256 `0d4e2fe08e1888a6591ed8eb34d614684a192149b3b8d45fca4506110ace8acb`，编译通过；抽取器 SHA256 `88a88c31388013b24aba24a870110c46b463ff7d8413446da0bcdcd9b2c213a0`。尚未执行真实旧档伤后迁移，也尚未认证公开0.3.1旧档兼容。

### 原生PK排队对照与原型归档v3（先于实施）

主线程已完成 `pkbefore`／`pkqueued`，均2200.01.06，预期原生SHA分别为 `981ae76af169bfba18c27aeb95cfcc6c5750096c5debe2637cfe3dc074738566`／`b5fdedad1031e5dddbe163c5e7e4ff2a9e96c1a28f65651de5164a10bb79cd12`。只读核对来源三件套，抽取Mother138／808真实current_order、destroy_planet_order目标15及move子订单、country0对1的原生war记录、源星与C／G等账本。排队订单不等于已完成充能发射，C／G未变不能冒称结算通过。

归档v3追加本次已完成PK原生三件套、所有对应动作／图／OCR和原始WrongScope失败材料，绑定v2索引SHA，不覆盖v1／v2。第一次控制台war效果的Current=fleet错scope须作为探针失败原样保留，不归为Mod业务错误；已读原始error.log显示当次ROOT实际为country1，按日志保留，不套用随后正确country0战争操作的scope。停止流程仍在完成时，只读取已完成文件；收到stop-final完成证据后，才对已停止run日志目录完整逐文件复制、复读哈希校验并标记静止字节freeze。此前两份活动日志单读快照仍保持原有非freeze分类。

后续rc2复用pkqueued是未发布原型的原生接口迁移；清原型flag／迁移不能作为公开0.3.1旧档兼容验收。本轮不修改游戏／SAV，不接触新run UI。

已取得stop.json：原pid29844于2026-10-19 09:08:33 UTC自然退出，forced=false、running_after=false；只读进程检查亦未见旧pid。可对本run日志完整freeze并复读校验。原始日志另记录17:05:52缺少 `on_destroy_planet_with_EEP_PLANET_KILLER_DEVOURER_queued`，与早先WrongScope分列，不能删去或归为相同原因。

只读对照已完成：两份SAV日期均2200.01.06，war0的真实attackers=country0、defenders=country1、attacker_war_goal=wg_cleansing。before无current_order；queued为destroy_planet_order.planet15，含move_to_system_point_order且can_reach=yes。C／G0、D2、worlds／made0、L0、next10均未变；planet15仍owner1殖民地、非pc_shattered、没有credit／destroy旗标。严格比较FAIL保留3项订单差异；`prototype-rc1b-pkqueued-vs-pkbefore-order-ledger-v1.json` 为OBSERVATION_ONLY，不认证charge/fire或结算。

v3归档已完成，索引 SHA256 `891936b7e513e013f9dbe332ba47aaa0f6acc78be1b7b4807481e22d593d4cf2`，新增246源文件，累计680文件／42,310,475字节。全部七份原生三件套、所有复制源的目标字节、v1／v2不变、Git text属性均校验通过，仅限字节scope。进程退出后完整日志19文件／5,904,024字节双读一致，位于 `logs-frozen/stop-final/`，freeze元数据和WrongScope／queued回调分类均单独保留。

发现并更正归档生成说明的编码问题：此前通过PowerShell管道传给Python的中文说明文字变成问号，只影响自生成README.md／README-v2.md，不影响直接read_bytes复制的原始SAV／日志／Mod／索引或从UTF-8读取的JSON数据。为维持历史字节不重写旧说明，新增正确UTF-8的 `README-v3.md`。后续生成包含中文文字的文件应使用apply_patch或明确UTF-8输入机制，不能依赖当前PowerShell管道默认编码。

### Legacy section只读审查

检查旧公开0.3.1／早期原生SAV内的实际section模板与slot名称，以及项目保存的旧load原始error日志。目标是判断同一个eep_mothership_section键被新槽位定义覆盖时的载入前风险，区分真实日志故障与尚未复现的结构性风险；本审查不改Mod或SAV。真正旧section应保留原始槽位，新设计使用独立section键的方案由主线程实施并另作原生迁移／重载验收。未发布rc1b的NAME_1019已经借用旧键装新槽，不能把该特殊原型档等同公开0.3.1档。

本轮发现抽取器来源校验边界：0.3.1 baseline run中的另一个receipt把snapshots存为非列表，原实现误把字符串迭代项当mapping而抛AttributeError。先增加root／snapshots／entry形状校验并记录未识别receipt形状；仅跳过不支持的旁证结构，仍必须找到与当前真实SAV SHA和audit日期相符的mapping receipt，缺少有效receipt照常FAIL。不修改任何原receipt或SAV。

已通过严格来源门禁只读核对公开0.3.1的 `bmm00.sav`：SAV SHA256 `af5f64e2eaadb164e87796d2a9261ac97ef7d716cc3f8b3cec5f4a2f23f787f8`，Mother ship1008／fleet128。保存的设计仍引用 `section.template="eep_mothership_section"`；29件已保存组件里，`TITAN_01`、`TORPEDO_01`～`TORPEDO_04`、`MEDIUM_GUN_01`～`MEDIUM_GUN_06` 共11个武器槽在原0.3.1定义中全部存在，却在rc1b复用同键的新定义中全部缺失。原始section文件 SHA256 `fae0a4052fd8b67d732b365b82ddf70ec378672bdf1be71b5b62c449965b248d`，rc1b同键定义 SHA256 `88fd4e3c751e5cd559fd48023985680f8667533345d3a120f81a833651c2bf4e`。完整原生设计与差异见 `legacy-section-031-vs-rc1b-native-contract-v1.json`。

因此保留原section键及其原始槽位定义、让新设计改用 `eep_mothership_section_1019` 是有实际旧档结构依据的兼容修复。改设计NAME不能修复已保存的section模板引用；隐藏tech仅隔离后续选型，不能替代旧定义。该调查尚未重新加载旧档，不能声称已复现载入时掉武器，也不能据此给旧档兼容PASS。

后续实机验收应分别保存：①原公开0.3.1载入新包、尚未触发正式迁移的原生SAV与error.log，确认旧模板仍完整解析；②同一舰船经原生setdesign后的SAV，确认新模板、全组件、ID／位置／订单／队列／账本及事先声明的受伤状态口径；③同日重载后的SAV与日志。若启动同步先于可观察存档，只能验收最终原生迁移结果，不能把它表述成已观察迁移前阶段。未发布rc1b已用旧键保存新槽，属于单独的原型迁移测试，不得并入公开0.3.1兼容证明。

receipt边界修复后抽取器 SHA256 `a1292a21f8a3f4509568d348dfa5b32ce98a86c10bfeeb428e1f4b21d4087400`，Python编译通过；本次bmm00仍由匹配的原生receipt、audit、manifest与完整冻结copied_mod共同证明来源，不因跳过另一份不支持的snapshots字典而放宽来源门禁。

相关历史日志搜索已限定完成：1015迭代证据、1019基线／rc1b归档、runtime-development，以及三个已知1019原始run的 `*error*.log` 共519文件、76种不同字节内容、2,359,775字节。没有日志直接出现旧section键或上述11槽ID；107行宽松关键词命中包括53行模型entity缺失、39行旧starbase_level trigger、4行已知PK locale缺失、11行旧环站design错误，均不是旧槽被删除的直接证据。报告 `legacy-section-historical-log-search-v1.json` SHA256 `e43280084211664e5772d9f05e29b2f2d65f0cc18d330976854bf19c7404efc1` 逐源记录SHA和行上下文。此前更广的全证据扫描已取消，未产生完整结果，本结论不覆盖未列出的日志。

### 六核硬件护盾探针设计（先于实现）

新增 `hardware-case` 只读case，schema `eep.1019.hardware-case.v1`，模板状态始终为 `PENDING_NATIVE_HARDWARE_INPUTS`，tier0／tier1／tier2／reload路径先置null。仅验证人工控制的真实护盾硬件路径，不把 `C=0、R=0、shield tier=1/2` 当自然RNG不变量，也不为尚未跑出的阶段填PASS。所有输入继续要求原生SAV／audit／receipt／manifest／冻结copied_mod严格来源门禁，并绑定同一候选树。

验收要求：唯一Mother的六件真实核心分别在AUX6～AUX11、完整设计在三阶段不变；shield fleet tier严格0→1→2，其他五tier为0，country镜像一致；C／L／成长modifier、其他账本与奖励计数恒定；country／fleet／ship的全部timed_modifier不因探针新增或改变，排除外部奖励modifier；普通对照舰船ID及最大三防恒定，且不从首日自动设计ID变化推断组件收益。tier1、tier2距上一阶段均至少5个原生日，reload须与tier2同日，设计／所有核心变量／实际最大三防保持。严格全量差异始终附在报告中，跨日差异不能整体抹去。

预期盾差值从实际已装原生盾组件的 `modifier.ship_shield_add` 总和乘冻结护盾核心 `triggered_ship_modifier.ship_shield_mult` 系数计算，不硬编码167310／3575，也不把同一SAV的actual值反推为输入预期。抽取器读取manifest指定原版目录、核EXE SHA，解析组件引用的原版／冻结Mod数值变量并记录源文件SHA；未支持的表达式或冲突重复定义必须FAIL。country基准保持为tier0实际最大盾及其隐含总倍率，后续只检验增量；可选原生 `ship.variables.eep_probe_shield_mod` 原样记录，缺失标为未采集，不能补值或当成必需观测已存在。

本轮原版只读发现 `LARGE_DARK_MATTER_DEFLECTOR` 引用 `@shield_L6`，本机 `common/scripted_variables/02_scripted_variables_component_cost.txt:389` 实际为2925，11件合计32175；与先前3250估算不同。若冻结核心每级+.1，则纯源定义预测每级3217.5。最终以新run的冻结装配、源变量和country基准校验；这里的计算不是尚未执行的原生收益证据。

实现范围仅为本人独占 `check_1019.py`／`inspect_1019.py`、本页与analysis evidence。验证包括Python编译、CLI注册、PENDING模板拒绝运行、旧rc1b缺六核的真实负例；真正tier0/1/2原生输入到齐后再出限定结果。自然RNG的R=sumN、B=floor(C/50)、P=max(B-R,0)、每次最多200及六选一等权分布另立专项，不能从本探针外推通过。

首次源解析验证发现原版未装备的 `BIO_PSIONIC_STRIKE_CRAFT` 在组件顶层含 `count = @[ count * 2 ]`，旧标量解析器不支持此种内联算式。组件索引只需要按原生直接字段流读取首个key，不应完整求值所有未装备组件；改为取得key即停止该body的字段迭代。真正已装配组件涉及盾值的表达式仍要求显式可解析，未知算式继续FAIL，不将此边界误报成Mod或游戏故障。

section源记录使用 `ship_section_template={key=...}`，与ship_size的顶层命名对象格式不同；源索引按内层key定位后再核盾上下文。此处检查器初版按顶层名称匹配的错误已在真实rc1b来源验证中发现，修正仅限只读抽取器。

硬件case要求四个独立原生checkpoint路径与严格唯一的Mother全局目标，避免把tier2同一路径再次读取冒充重载快照。即使存在独立同日reload SAV，检查器仍只证明其字段保持；实际载入动作由原始actions／截图／OCR另证，不由本报告推断。

实现验证已完成：Python编译及CLI注册通过；PENDING空模板按预期FAIL（`hardware-pending-template-negative-v1.json`），真实旧rc1b无六核档作为四阶段输入也按预期FAIL（`hardware-real-rc1b-no-six-core-negative-v1.json`，SHA256 `c1ddc7d6668dc57bc92f83b5f186501b837abd4c762c910e0d4fd35df22ce104`），不是新候选故障。真实pmm00严格来源加源解析得到11×2925=32175，实际最大盾167310，完整required／ship_size／section盾上下文与变量来源SHA在 `native-base-shield-source-calculation-v1.json`（SHA256 `5e2d40b4803b2d4fbe579228e8f9dde738bc1c263090f4dcb8e819ff6339031c`）。这些结果不代替RC3 tier0／1／2及reload实测；模板仍PENDING。

### RC3 原生一级实测与盾值分层修正（先于工具修订）

RC3冻结树 `178d3021fa53dd999b5537e1e58f7b59c7138232e7a7fe4fe53327b3dff8e116`、run `20261019T092935Z` 的Machine新局已取得真实原生SAV：fmm00（Jan1，SHA256 `18cae5e75b189ee8739cdadd3fc63d5c2929fad7a1d892e5382d0750d36c33d9`）、hw0（Jan7，`815aa75e10b3629b42750347f5f30c765e339d01d67637ccfe21cd5e1691a655`）、hw1（Jan13，`b342199c7212594db5eb63746835e9670cc41c737eb694e8e6e8773585c76983`）。严格来源门禁均通过。Mother fleet159／ship997／design1379，真实50件槽组件与6件required完整，六核实装AUX6～11。零级最大三防93960／44787.6／167310；hw1只把shield fleet tier及country镜像改为1，C／L／R仍0、其他五tier0，普通ship1～5最大三防及全部timed_modifier保持。

hw1实际最大盾为171492.75，即较hw0增加4182.75；原生诊断变量 `eep_probe_value=1`、`eep_probe_shield_mod=3.1`。因此初版仅按raw盾32175乘核心+.1预测3217.5的公式必须记为FAIL，不能覆盖或事后改写。修订前先保存完整旧checker／inspector字节、版本SHA、hw0→hw1的原生差异及 `hardware-hw0-hw1-raw-basis-prediction-fail-v1.json`，后续修正另出新报告。

独立层级依据来自本机原版 `common/component_templates/000_documentation.txt`：第12行说明 `modifier` 作用于设计器显示的数值，第18行明确 `triggered_ship_modifier` 使用Ship scope，第24行另列Design scope的 `triggered_ship_design_modifier`。该文件SHA256 `f9c0edfee06c59422609c04030e890afeb824055deeee18507315d8acb875286`。原版 `00_utilities_aux.txt` 的SHIELD_BOOSTER使用设计层 `modifier={ship_shield_mult=0.1}`，真实已装三件；源文件SHA256 `2f6ee0210a8cbd3f3e4b42b1884a6b365224e6b92b937a52e2d204eb0f8b3699`。冻结 `eep_mothership` 的ship层静态修正为3，新核心使用Ship scope的triggered修正+.1×tier。required／ship_size／section没有其他基础盾add；它们的全部盾上下文继续保留。

据这些已知层级，先由raw盾32175乘设计层 `(1+3×0.1)` 得设计盾41827.5，再乘ship层 `(1+3+0.1×tier)`。在尚未读取hw2前独立得到预测：tier0为167310，tier1为171492.75，tier2为175675.5，每级增量4182.75。这是根据原版层级定义的推导；hw0／hw1与原生export是对照验证，后续hw2趋势只能补证，不能替代层级来源。原先3217.5仅是遗漏设计层的失败预测，不是原生组件配置事实。

工具修订范围：保留 `base_shield=32175` 表示原始add之和，新增设计层mult贡献、设计层倍率与进入ship修正前的盾值41827.5；hardware增量按该设计盾乘冻结核心系数计算。条件性Design scope的盾mult、未知非零ship_size／section设计倍率等未实现情况明确FAIL，不猜测条件。可选诊断变量全部按原始 `eep_probe_*` 记录，缺失继续为缺失。旧FAIL与旧工具源码均不覆盖，旧严格差异门禁完全不动。

hw0最后一次诊断命令误用 `every_ship`，原始error.log第26行记录17:43:36 Invalid scripted effect；hw0所有ship probe变量确实不存在。此为诊断命令失败，与此前真实快进、SAV最大三防及Mod业务分开归类。hw1改用 `every_owned_ship` 后诊断值存在，不能反填hw0。

RC3分批归档范围拟为 `evidence/1019-rc3-hardware/`：每阶段完成通知后复制原生SAV／receipt／audit、不可变manifest／copied_mod／静态报告／源snapshot绑定及对应已完成actions／截图／OCR，逐文件SHA索引并设 `* -text`。不复制或冻结仍在写入的动态日志；当前阶段日志若有必要仅单次读取并注明UTC，停止后才另作完整freeze。本节及先前文档不把人工硬件探针等同自然RNG、12月经济或完整发布验收。

旧预测FAIL已落盘，SHA256 `e5b32f8cd125314e71135fc6c9c4c02fc891145e0ad826c265fe19829537d947`；旧checker／inspector原始字节保存在 `evidence/1019-analysis/hardware-formula-v1/`，并以 `* -text` 防止Git归一化。hw0→hw1的24项严格差异原样保留。另保存了两份完整只读原生观察，未改SAV或原始receipt。

原版同一 `00_utilities_aux.txt` 还提供独立管道对照：SHIELD_BOOSTER在第99～100行把同名盾倍率放进 `modifier`，CRADLE_MARK在第439～441行放进 `ship_modifier`。这与原版文档的设计／舰船scope区分一致。完整引擎数值函数为闭源；这里的乘法模型是源参数、scope定义与独立原生读数共同校验的推导，不能表述为已经读取引擎实现。hw2只验证此前已明确的175675.5预测，不用于反拟合系数。

### RC3 护盾硬件四阶段结果与归档

完整 `rc3-hardware-case-report-v2.json` 为 `PASS_SCOPED`，56项限定检查全true，报告SHA256 `318604b2a58f6181a030a2c7daf2d563edb92b9e7f27d2ae051e786a17a7134a`。实际最大盾依次为hw0 Jan7的167310、hw1 Jan13的171492.75、hw2 Jan19的175675.5、hw2reload同日的175675.5。两次各6日刷新、六核真实装配、同日重载硬件快照、C／L／R0及其他五tier0、普通ship1～5最大三防、modifier均符合case。原生value／shield modifier导出依次为缺失／缺失、1／3.1、2／3.2、2／3.2，没有给hw0补值。hw2与reload SAV SHA分别为 `50d4c00dc4dbbe9422401d138b750295f9dbc633b9c2b1a342cc75a23e3ea3ad`、`aef3706cd833d7799f67c654cc3ca3abc630d319086b9ea23fffbb00cb20d186`。

最终硬件工具Python编译通过；checker SHA256 `c2ec4162a87db939dc5396199c54ca381efcde19047dd0541f4a531f9230c562`，inspector SHA256 `1ec3ad71f877be5704959134b76e59be077b756a906f7297f278613ee8bfbf92`。`hardware-report.v2` 同时保留raw base32175、设计层1.3、设计盾41827.5和原生导出，所有期望仍从源定义得到，未硬编码实测盾值。

严格比较完全保留FAIL：hw0→hw1为24项，hw1→hw2为24项，hw2→reload为57项。前两组包含受控tier／实际盾／诊断变量、战力缓存、snapshot旗标时间及原生计时器变化。重载Mother设计索引1379→1446、普通站ship0索引17→1431，但设计内容保持；原先缺失的original_owner写0；10个己方舰队的last_ftl_jump补写to与fleet，其他movement直接字段原始文本相同；核心planet2的carrier_binary_flags从1→3，含义未校准。以上原生差异均没有称为无害或忽略。分类报告 `rc3-hardware-difference-classification-v1.json` 为OBSERVATION_ONLY，SHA256 `713ff5b6a1911d7e43b2a81db9471f3cc45bad791c05e4daf79c3e41e19c8dd2`，指回完整严格报告。

本批 `evidence/1019-rc3-hardware/` 已完成430个源文件／22,500,921字节的逐源双读字节归档，13项字节／来源绑定检查全true，未复制任何活动日志。索引 `archive-index-v1.json` SHA256 `eded63efe29b20e1f99223fa1bf9bef9787ad94e7b09a2a33a7e761498d70722`；归档manifest SHA256 `4fe88804769af4bc3e35bd14a5fcc918196491d79cc5db85cecc53cb3ab2ec4c`，静态工具原始报告SHA256 `a5054bd863896d2cf842402c544ebde7f5a823d01f6a1589c5b0c0d5b709d96f`。实际截止于hw2reload原始receipt，后续自然经济阶段尚未归档；索引明确整个发布仍PENDING。

### 干净Machine基线与首月只读事实

主线程原生重载fmm00后重存 `fmm00reload`（Jan1，SHA256 `5119586edead4b55f06b6adde5df76ef057c4d1dcc378961c22e4b08eccebccc`）。与真实初始档的13项限定事实均一致：country／fleet／所有己方ship没有eep_probe变量，六fleet／country tier0，C／L／R0，能量200且全部stock一致，单殖民地0／core planet2、原layout不变，人口原始总量4800（complex_drone2700、simple_drone2100），Mother最大三防93960／44787.6／167310。观察报告 `rc3-clean-fmm00reload-observation-v1.json` SHA256 `eeb4aafbf0d0752a38f85affabe287082a7bafd97d31f8e3d119e7c3bbab3d98` 为OBSERVATION_ONLY，完整严格比较仍FAIL54。这里只认证干净经济基线字段，不能称全量重载零差异。

真实首月 `fmm01` 为Feb1，SHA256 `c2d8c0b912b3cead2cb57b442152c1fc588c7f8d9eff4b99e8b2c7c4f141de9b`。来源匹配fm-monthly-autosave-receipt中真正 `eep-test-history/autosave_2200.02.01.sav` 与audit。旧startup(machine)原样运行23项全true，结果仅为新局及首月PASS_SCOPED：单pc_machine母星、矿区2／发电区3、2并行星球队列、10移动船坞等。原生首月收入165.6228、支出162.9639、净+2.6589、energy stock202.6589；人口原始总量4805。原生岗位workforce为矿工1200/1200、发电905/1800、复制300/300、协调560/560、三科研各180/180、合金900/900、巡逻100/100、后勤300/300。C／G0、D2、L0／next10、R／B／P0、state0、六tier0。

第一次monthly命令误用加载前的anchor目录，真实autosave已经存在；主线程按原字节恢复首月并记录 `fm-first-autosave-recovery.json`，没有重复推进。该操作故障与Mod经济结果分开保存。12月自然经济仍在运行，只读首月事实先记录本页，全年完成后再统一核对和归档，不复制仍在变化的整个run。

### 世界与帝国危机目标分别验收（先于工具补充）

原版的世界毁灭与帝国毁灭使用不同 `objective.progress` 累计奖励点，最后一个殖民地可能额外涉及灭国回调。现有settlement初版只检查destroy_worlds，不能据此宣称两目标都没有重复奖励。补充case必填 `expected_crisis_empires_progress_delta`：普通非灭国场景显式为0；灭国场景必须填同一银河设置下独立原生校准的正奖励点，并提供 `crisis_empires_calibration_evidence={path,sha256}`。原字段 `expected_crisis_progress_delta` 仍专指destroy_worlds，旧接口字段不混用。

只读工具分别按内层objective键抽取 `crisobj_destroy_worlds`、`crisobj_destroy_empires` 的before／after／delta，重复同名记录继续拒绝；原生没有记录时明确按未得分0处理，并保留present状态。两个目标都必须与各自显式期望相符才可输出settlement限定PASS。不能把progress写成次数+1，也不能把潜在两次灭国奖励假定为严格2倍；实际毁国后参与奖励公式的国家计数可能变化。

建议校准为两份真实同日SAV：calbefore后在Mother实际owner country依次原生complete worlds／empires，保存calafter，独立读取两个目标差值作为单位奖励；该校准与真实发射／拆除结算另行进行。此改动只加强尚待实测的结算检查，不修改Mod、原SAV、硬件报告或旧FAIL；旧硬件报告的对应工具字节已归档可复现。

补充已实现并通过Python编译。两份真实历史原生SAV独立验证读取结果：世界目标1500／帝国目标无记录0，以及世界2250／帝国550，均与此前独立观察一致，重复外层objective未被字典覆盖。证据 `crisis-objectives-real-native-readings-v1.json` 为OBSERVATION_ONLY，SHA256 `3025e8532b90d875074591be953b3e6c1086a1e7fa0429592d5ffb14a5ca5fdc`；只证明实际同版本SAV的解析，不声明这些历史档的EXE来源或RC3结算通过。当前加强后的checker SHA256 `ba17847049d050b2b76dc382e7e3e0a1796dc4976a80c77b16fef243bc612047`；硬件报告原对应版本c2ec仍保持原字节归档，未覆盖。

### Machine全年经济子集归档设计（先于实施）

主线程已完成fmm01～12及2201.01.01年末原生UI存档fmyearui，随后在相同run开始fh Hive新游戏。经济归档仅选择已经完成的 `fm*` 文件，以稳定 `fm-auto-ui-comparison-m12.json` 为截止点，明确排除全部fh、hw及活动日志，目标为 `evidence/1019-rc3-machine-economy/`。保存13个初始／月度SAV、实际干净anchor fmm00reload、年末fmyearui及各自audit／receipt、12份真实30日命令／HUD／OCR、原首月错误anchor的命令和日期HUD、`fm-first-autosave-recovery.json` 与更正后的完整月receipt。冻结Mod／静态门禁复用已校验的RC3硬件归档，旧机器基线复用 `1019-baseline` 中13份原字节SAV和索引，按SHA建立引用，避免重写旧证据。

只读初检已得到旧economy原门禁5项全true：12个月实际净能量均正且库存逐月不降，Feb1净+2.6589／stock202.6589，年末净+8.51705／stock267.60783。候选13份SAV与旧基线13份SAV的manifest／copied_mod、匹配原生receipt、SAV SHA及gamestate audit SHA已独立复核。旧0.3.1机器基线首月-161.26091、年末-153.60543及缺失energy键等原始结果不更改，不把它包装为旧版经济通过。

生成startup／完整12月经济报告时保留旧检查器的所有原始月度预算数据，增加实际anchor、12个提交动作均为 `fast_forward 30`、无probe变量、C／L／R与六tier0的原生读取和两侧来源证明。年末原生UI对照只重核预算、库存、变量、flags、殖民地、区划、岗位、人口组、星球、殖民地体十类字段；不能据十类一致宣称全量gamestate零差异。新报告限定Machine新局／首月与12月经济，不外推Hive／Lithoid／Purifier、自然RNG或完整发布。

项目gitattributes现已由主线程增加tools／testing Python原字节保护；旧硬件报告对应c2ec源码在 `1019-rc3-hardware/analysis_tools/check_1019.py` 已复核SHA256完全一致。经济归档同样使用 `* -text`、逐源双读哈希及独立验证索引，不修改原run／原SAV／原receipt，不捕获新Hive资料，不把仍活跃的run称为完整freeze。

### Machine全年完成结果

三份最终限定报告已完成：`rc3-machine-startup-report-v1.json` 为23项PASS_SCOPED，SHA256 `b4870b0459a8dfa0e438e6c0ae0e60438a339d5d08292176bde40c0b5c72be22`；`rc3-machine-economy-12months-report-v1.json` 为14项PASS_SCOPED，SHA256 `7e6722da9e9f0b2d0ea0dd3e21ad1f7d98c2e998a3b2b027dada542a89008ed5`；`rc3-machine-year-ui-comparison-report-v1.json` 为十类字段PASS_SCOPED，SHA256 `395d308ef3584c6bea60f9cb4d6d3924d1188f02c217874a35c71b3dc8846b4c`。原末月SAV SHA256 `676d996da685c01a2cd8e006b8567ba48f33774bf46de0dda2a30477f35fdcc6`，年末UI原生SAV SHA256 `f9633c53cb2be74841f9ac3e6ecb426d2bce357b86ab1031d770bbd1717b19d7`。

14项经济检查保留旧5项原门禁，并独立补证26份旧基线／候选原生SAV来源、实际干净anchor、12个逐月receipt和12次真实fast_forward30动作、实际anchor初始预算及stock与原fmm00一致、所有初始／月度SAV无eep_probe且C／L／R／六tier0、首月恢复没有二次推进、年末十类字段一致。人口保留只证明原fmm00与干净Jan1重载的4800相等；不能将其映射成全年人口恒定。正常全额upkeep、无任何资源注入／贸易补贴／岗位关闭／拆船等更广条件未由本报告穷尽，不能自动填true。

`evidence/1019-rc3-machine-economy/` 已归档344个源文件／21,084,334字节，28项字节／来源验证全true。索引SHA256 `9fdd9cf4893eb70ab138964c7d047fcf07c554c683223e556825100999a51104`，验证文件SHA256 `65012eaa9eea67e91f5730f1457cb276822bfe07afba22c98863aa0869e3bfbc`。其中334份fm阶段原始资料含首月失败命令、两次日期HUD／OCR、恢复记录、更正anchor及原生UI保存动作，另外包含manifest、5份对应工具源码及4份只读分析。没有fh或任何日志文件；旧基线和冻结Mod通过哈希引用连接已有归档，原字节未重写。先完成源复制时的历史receipt保留当时状态，最终索引另行生成，不覆盖任何历史文件。

### Machine操作约束与startup补证

设计先记录于 [machine-operational-constraints-1019.md](evidence/1019-analysis/machine-operational-constraints-1019.md)，复现采集器只导入既有只读解析器，没有导入运行时UI驱动。结果 `rc3-machine-operational-constraints-report-v1.json` 为六项限定PASS_SCOPED，SHA256 `6479fecf564ad78ad738b11f91fd22ebebd2d7b2aeef8fd41741a1d10ee64a62`。四经济操作约束均有实际依据：109份action与另两份底层Ctrl+A共111输入，12提交全为fast_forward30；22点击全部绑定实际截图SHA、OCR与源码；九资源逐月库存差值等于原生预算净额；14检查点10有限岗位限额保持最大值且均有人，全部12初始owned ship ID、fleet ID、舰名保持。结论限定已记录执行路径和检查点，不声称连续监控任意外部输入，也不把正常原生logistics贸易收益排除。

人口保留补证使用同preset旧0.3.1原生bmm00：原母星复杂2700＋简单2100＝4800，与RC3母星相同；旧赠品星球100单列，不当作母星损失。它不是另跑的无Mod原版夹具。normal_upkeep补证为实际普通ships／ship_components／建筑／区划维护逐月非零，既有Mother两项-1优惠值不变且仅在舰队159，冻结所有P源没有新增全局免维护；并不宣称原Mother特惠被取消。country确有原生game_start，源定义仅减少派系产出，不能将其误写为空modifier列表或新增免维护。

年末唯一通知点击匹配`eep.10.a`，冻结`events/eep_events.txt:166`仅有`option={name=eep.10.a}`、无effect，源SHA256 `e4be49df425db8dd4c4919a788c38ef2d4075466a9da946e6dc35a6c47cf55a1`；简中键源SHA256 `b1add578c1f81db6e558485c1f8d96a7e780d1c4c932f2016a34f2a0e2c9fe66`。二者已在既有硬件冻结包逐字节归档。年末十类auto/UI一致另证实际点击没有改变这些账本／人口字段。

追加经济归档v2：358源文件＝原344不变＋14补充（两Ctrl+A、五执行器源、三原版源、旧Mother源、采集器／设计文档／报告）。`archive-index-v2.json` SHA256 `350a6e3a8d04f71d00dfc7e8891ef09eb28fa1a79384dc93e22d5eb658feac6f`，`archive-verification-v2.json` SHA256 `3ad46788ffce352ae4d2b8c41f29f728c073b00f731b587656707ac8d2647a5b`，九项全true。v1索引和payload原字节、所有旧FAIL保持；没有活动日志、Hive或PK分支，完整发布仍待其余实机门禁。

### Hive首月独立只读复核

同一RC3冻结树／run的`fhcm00`、`fhcm01`、`fhcm01ui`均通过原生receipt、SAV SHA、manifest／copied_mod来源与gamestate audit SHA核对；SAV SHA依次为`0297ff12409b944373caa07996eb8a5d34ff16ba6ffcc723c40a361276aefa7f`、`32225a7809d6c9c07252216429aa795da5a77977f1f498e3daa8c987f77edf9d`、`e4ef976d8ac33626281f65b9c2f6a126f96957c069205ca17bd34e8fd7234b51`。既有startup(hive)23项全部true；同日首月auto/UI十类字段独立复核全相等。

单母星planet5为pc_hive，区划为主区3、食品2、矿2、电2；发电workforce508／1200，原生首月人口5308，能源80.98098收入－62.47047支出＝18.51051，库存218.51051。结果`rc3-hive-startup-report-v1.json`为限定PASS_SCOPED，SHA256 `1a525a12422911513abea8f024afaaf28d801149a8ec9ba0a17a50bd78fb142f`。没有复制仍活动的整个run，也没有把Hive首月外推全年经济、其他政体或完整Mod通过；Machine经济包保持独立。

### 真实PK路径发射前只读基线

`pk1base`为2200.01.02，SAV SHA256 `dccb1e17d6f76c915e3f0a916e627f068c559d381e7a6962becc21c77093b38a`，已核原生receipt／audit／manifest来源。摘要`rc3-pk1base-summary-v1.json` SHA256 `a962580db7fdd3c6487e0e09b8464de7acd0d45a7535f8f07a712038783f7a27`，完整观察另存`rc3-pk1base-observation-v1.json`，两者仅OBSERVATION_ONLY。真实war0的攻击方country0、守方country1，目标wg_cleansing actor0／target1；Mother fleet159／ship997属于actor，global victim1／target planet17／core2绑定均在原生SAV。

发射前账本C／G／made／worlds／L／R及last三收据均0、D2；core2人口4800／capacity2。敌方源planet17是pc_alpine、size19、owner1、colony1人口5200，原生d_lithoid_devastation数量0，新鲜有效q为19；两危机objective尚无记录，按present=false／progress0保留。Mother三防93960／44787.6／167310，当前没有完成巨像订单或结算证据。

no_army的准确范围为目标没有actor入侵军队，而非整个帝国不存在守军：自有army0～4全是machine_defense、colony0／spawning_colony0，在home母星；目标colony1只有enemy守军，自有transport fleet数量0。ship992～995是采矿站、996是研究站，不能称为运输军队。Mother被测试准备命令teleport至目标星系origin8；此事实不构成主动jump验收。危机目标手工complete校准将另存同日SAV，绝不当作原生发射或事件收益。

同日校准设计：`pk1base`对`pk1calafter`只读比较，要求实际动作在Mother.owner范围内分别仅调用一次worlds／empires complete；读取两个内层objective各自progress差值，不使用总menace。独立校准JSON必须包含before／after原生SAV与receipt／audit／manifest证明、实际命令及SHA、同日检查、EEP所有账本变量／核心人口与容量／源星完整体保持检查。两目标奖励各为明确正值后，结算case方可按对应独立差值引用；校准本身始终不表示发射通过。最小证据子集追加于`evidence/1019-analysis/pk1-objective-calibration-v1/`，仅复制已完成白名单文件，逐源双读哈希，不冻结当前活动run。

校准已完成：`pk1calafter`同日Jan2，SAV SHA256 `6d736fd34099cadc449121180fb372029d65dc3a344a1465c16b0c86ab70037f`。实际命令在global Mother的owner块内对两目标各complete一次；worlds的progress由无记录0变为750，empires由无记录0变为600。EEP全部country变量／flags、core2与source17完整原生快照、所有pop_groups／pop_jobs均相等；core人口4800／capacity2，source人口5200／size19保持。stock唯一差异为原先缺失的menace写入1350，报告没有用该总量校准任意objective。

独立`rc3-pk1-objective-calibration-v1.json`为17项PASS_SCOPED，SHA256 `58416a43891a899cc7ded7982760cd1dfbe93180e78123937842de011bbba87a`；两种case校准evidence字段可按SHA分别引用同一报告，对应奖励750／600。非灭国结算的expected_crisis_empires_progress_delta仍需显式为0，不能把600无条件写入所有case。严格比较保持FAIL及三项真实差异，原报告未覆盖。最小包53个源文件／3,206,832字节，八项字节／来源检查全true；其`archive-index-v1.json` SHA256 `f96198b616a731f37e563a9d29513f12c7f13e95dd750c4f9e9e02a25de3b891`。没有活动日志，整体运行仍非freeze。主线程恢复pk1base后才下实际巨像命令，校准不作为发射通过或自然收益证据。
