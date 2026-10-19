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

### PK物理星系定位只读更正

原生galactic_object8以重复直接`planet`键列出physical9～22，含17，不是一个`planets`包装列表。其name key `SPEC_Dabbax_system`在原版简中译为普尔克兰；physical17 key `SPEC_Dabbax_planet`译为戴巴纳仙，moon_of=15。其他ART2_PLANET_Vurl-*原版译名本来就是沃尔*；这组UI文字与目标系统一致，不能据未见卫星名称断定Mother处在错误系统。

Mar7实际`pk1prequeue` SHA256 `67dad27edbefbe00565488c1058b8161fcad4903f19ea23bfd6e2b8dc009ffa2`，Mother159 movement(40.65677,161.7926,origin8)，target17(32.63097,152.52768,origin8)，parent15(39.05145,129.3732,origin8)。它没有destroy_planet_order，故仅是下令前探查基线；不得因文件名含prequeue而声称排队成功。唯一target/core/Mother绑定及war保持，EEP C/G/made/worlds/L/R／六tier0、D2，core人口4809、source人口5206。原生destroy_enemy_ships进度75及menace75是清场收益，worlds／empires仍无记录，证明手工1350校准已恢复。完整成员坐标、原始字段、战争／军队、库存／预算另存`rc3-pk1prequeue-location-and-ledger-v1.json`，SHA256 `615db78fe49eafc9d6e07f94c0e968579d1c45b7b589cd0762b5bd634bbb2dc7`，仅OBSERVATION_ONLY；不假定未证实planet-select API。

### Hive首月独立子集归档设计（先于实施）

将已完成Hive首月阶段独立保存于`evidence/1019-rc3-hive-startup/`。原字节复制不可变manifest／copied_mod／源快照绑定／静态gate，fhcm00、fhcm01、fhcm01ui及各自audit／receipt／economy summary、实际动作／GPU截图／OCR、既有23项startup与十类auto/UI核对报告。首次fh选择失败的实际记录完整保留，标明操作选择失败及其边界，不能改写为Mod失败或成功。

只复制已完成fh／fhc前缀白名单，以首月auto/UI comparison完成为截止，不复制Machine、硬件、PK分支或任何活动日志，不称完整run freeze。每个源文件读前／后stat及双读SHA一致、复制SHA一致，归档`* -text`保护。manifest文件表逐项匹配copied_mod／source snapshot，三SAV／audit／receipt及实际图像OCR哈希均须一致。归档索引和独立字节验证明确Hive仅开局／首月通过、全年经济及发布仍PENDING；完成后给发布agent引用路径，不操作UI／Steam／Mod／Git提交。

Hive独立归档已完成：289源文件／16,250,350字节，25项字节／来源检查全true。`1019-rc3-hive-startup/archive-index-v1.json` SHA256 `f87ba1d0e428f603135d6b6d925e2c14680b3c5901da6d80572330cfcecbacde`，`archive-verification-v1.json` SHA256 `83de22b0618f4f1e4002094ad42019ee96c27881ac59b4d71d65c954339b3d49`。148份原始fh／fhc阶段文件加两份保存名称Ctrl+A、原字节manifest、完整copied_mod／source_snapshot、原始静态报告、十份执行器／只读工具源及三份专项报告均有逐源SHA。

startup报告仍为23项限定PASS_SCOPED，SHA256 `1a525a12422911513abea8f024afaaf28d801149a8ec9ba0a17a50bd78fb142f`；另出`rc3-hive-auto-ui-comparison-report-v1.json`十项限定PASS_SCOPED，SHA256 `c14bd2961780d606918bf1b09d36bc32a754df55f70824734a48b2dff7da0438`。首次匹配停止的左栏截断行、随后实际点击与右栏完整“EEP 02 有机吞噬蜂群”标题保持；`rc3-hive-selection-attempt-review-v1.json`明确源异常字面量不等于不存在的独立终端原始错误文件，不重建stdout。没有活动日志、Machine／PK阶段或全年Hive结论，发布索引仍按PENDING引用。

### PK实际排队与充能只读方案

主线程已通过实际原生菜单“拆解星球 戴巴纳仙”下令，先保存已survey但未下令的`pk1ready`（Mar7，SHA256 `11149f60e725625393adececf6481f1dffc9b9364cc1c6fb46e3f76f328eb0ba`），随后依次取得同日queued及推进6日的charge。仅当原生SAV／audit／receipt齐备且SHA一致才读，旧模板与历史证据不改。ready→queued运行同日no-settlement并保留完整strict差异；独立抽取所有EEP country／Mother变量、源星q／flags、physical17的真实destroy_planet_order及移动子订单、真实战争与我方军队位置。charge读取原生progress字段和日期，按实际原版订单字段校准剩余天数，不凭UI字幕臆造发射状态。

另一agent正在原checker仅修migration公共空队列适用性；本轮先将当前独立只读工具链原字节保存到`evidence/1019-analysis/pk1-readonly-toolchain-v1/`，使用其tools／testing完整相对布局运行PK检查，防止执行时源码与报告SHA错配。冻结范围仅现有audit_save、check_single_homeworld、check_1019、inspect_1015、inspect_1019；逐源SHA索引和`* -text`保护。不改业务Mod、UI、SAV及任何旧报告。实际charge／fire仍分开取证，queued／charge不会自动通过完整巨像case。

已完成真实ready→queued：同日Mar7无收益九项通过；独立19项订单／完整EEP变量／原生菜单点击／无目标我方军队检查通过，报告`rc3-pk1-ready-queued-case-report-v1.json` SHA256 `f4835d18e16d163c7296750a8f664cbfe4ffd9a81f27427caf8a6f0c9625050a`。Mother.current_order.destroy_planet_order.planet=17，移动子订单坐标精确匹配源星且can_reach=yes；此时source q／colossus_active尚未出现，不将订单接受外推为callback已经执行。strict保持FAIL三差异：两处order_id1→2及完整Mother原始体新增真实订单，未忽略任何路径。

### pk1charge原生保存中途失败的紧急只读调查

真实FF6至Mar13后，helper在audit要求country1必须存在时停止；原始`pk1charge.sav`已由原生UI写入并复制，但没有原始audit／receipt，也未完成closemenu。该原件及失败状态不可覆盖。允许在独立analysis目录生成明确标为派生、无原始receipt的只读audit／观察，并将原ZIP、实际history同字节副本和已完成保存动作／GPU／OCR做最小字节留证；不能伪造标准receipt或冒充完整来源门禁PASS。

实际raw SHA256 `156ac651eb5d8d268355c2281ce347670232bd4ffe0f419795d58d4b94095b77`，ZIP CRC完整，与游戏history内原生文件同字节。Mar13实际状态已经完成结算：目标17 pc_shattered／eep_q19／old_damage0／五完成flag，country1已不存在，Mother current_order为空；C19/G19/D6/made300/worlds1，三last为4／300／0，core人口5109＝Mar7的4809＋300，worlds750／empires600、enemyships75。故名为charge的文件不证明取得充能中间态；CSV的90／30不能未经原生单位验证解释为90／30个游戏日。五完成flag时间62809656相对Jan1为69日、即Mar10，可作为完成发生在六日窗口内的时间旁证。

原生布局新事实：planet17仍保存colony=1整数链接，colony1也保留历史species／经济／增长cache；但planet已无owner／controller、源pop_groups及pop_jobs实际列表为空、实际人口0。旧settlement用`colony`字段消失判定毁殖民地是错误的布局假设，后续必须先保留旧工具诊断FAIL，再以真实失去所有权、无实际人口／岗位与pc_shattered等正面证据替代该假设；严格全差异门禁保持不变。当前raw缺原始receipt，仍只作OBSERVATION_ONLY，等待主线程另存完整fired证据后正式判断。

主线程随后授权独立部分保存恢复，设计先记于`pk1-partial-save-recovery-1019.md`。原run无audit／receipt状态不动，`pk1-interrupted-save-v1/recovered/`新建原字节SAV／manifest副本、派生country0 audit和`pk1charge-recovery-receipt.json`，明确original_helper_completed=false，保留原生history与artifact同SHA／mtime、实际保存名称／Ctrl+A／点击／GPU图、重现`requested native country does not exist: 1`异常及UTC。旧inspector本就支持`*-receipt.json`，没有修改来源门禁或伪造原helper成功receipt；恢复receipt SHA256 `057a94b2108e35fb9788c878da2966b13b4cc46024df25e5c029dd158ca134fa`。

冻结ba178旧checker实际运行完整case后，25项仅source_colony_destroyed失败，旧报告SHA256 `ee7a40f4d50851588eeccf29a3107e7a2d708c37e59c7a4951f36660b49e79de`。仅settlement函数加入真实活性模型：pc_shattered、无owner／controller、实际人口／group／job列表空、直接活人口计数为0或缺失，保留colony整数及历史cache。新checker SHA256 `681836d2da9c6b28ee9bfd583c87e5ced96f06543901e71d3dc35fa226f3afdc`，原inspector未改。13项真实正例／数据层负例／仅函数变化证明全部通过，另17项migration回归通过，未改另一agent的migration区域；原df147完整字节亦保留。

新结算报告`rc3-pk1-recovered-settlement-report-v2.json`的25项数学／持久结果检查为PASS_SCOPED，SHA256 `a7462e3360ab52d2c4ecb711b5a727507d5eabdc63373880ba1d7c402fd994c5`；strict仍完整保留179项真实差异。总报告`rc3-pk1-native-fire-duration-fail-v1.json`明确为FAIL，SHA256 `dcf8d56e47d718d20fe6e780d366ef592bc0a2d46adbceb52d8579b50b6b0342`：真实菜单／physical17订单到pc_shattered及q19恰一次、750／600奖励与无目标我方陆军可分别肯定，但六日内已完成、没有充能中间档，90／30游戏日要求未通过，不能用结算局部PASS覆盖完整case失败。自然人口预期0依据同月窗口和独立六日硬件人口基线，未按after人口差额逆推。

本轮独立恢复／动作／原生输入与原始ZIP／新旧工具及报告字节包共114源文件／7,863,767字节，16项验证全true。`pk1-interrupted-save-v1/archive-index-v1.json` SHA256 `2d233ed0c2397ba7ea30897f4d485d6e398008a8ffe192b5f8cb9a23cf6408a7`，`archive-verification-v1.json` SHA256 `d1ed2a06ddc03a0cf07a0ffad6e509385bb00db1b440e85c0818372faeb54f68`。原始helper缺audit／receipt、旧FAIL与来源字节保留；没有活动日志或后续证据，生产Mod未改，完整发布仍阻于时长合同与其他实机门禁。

### RC4独立原生时长夹具只读方案

新run `20261019T112808Z`／PID36644，冻结copied树`06485dc540a88b30cef15c27c323ff21cd88f04ad57b79e4f5bc0590937ef468`，59生产文件。主线程加载RC3未毁`pk1ready`建立独立时长夹具，不是RC4新游戏开局；首开F12过早的失败及重试保留，不推断错误点击或SAV覆盖。旧RC3六日完成、duration FAIL及全部历史文件均不改。

等`pk2base`原生SAV／audit／receipt齐备且SHA一致才读取，核physical17仍owner1／q19、C0/G0/D2／六tier0、唯一Mother159／997、global core2／target17与军队仍在home；核原始manifest、59文件表、实际copied_mod及RC4组件TXT的`windup={min=90 max=90}`／`total_fire_time=30`，并确认SAV设计实际装载对应组件key。原生订单如出现windup_time／fire_time应按真实SAV字段读取，不能将这两个词误写为TXT键。源码与manifest完整绑定只能证明实际候选配置，不替代后续原生逐日行为。

之后分别等待真实queued／day1等新SAV，按实际订单／原生计时字段与游戏日历判定充能90日、发射30日；未取得这些证据前均PENDING。run静态gate与report冻结的是pre-canonical工具副本，后续LF canonical仅EOL关联由发布agent独立记录；不改raw gate／manifest、不重写来源SHA。此阶段只读，不操作UI／Mod／Steam／Git。

`pk2base`已原生保存Mar7，SHA256 `be5a344439dafe105d4959b4afa31143331b1daaaf915dba28bc70ee23f6f2e2`。独立`rc4-pk2base-configuration-report-v1.json`为20项基线／来源／配置PASS_SCOPED，SHA256 `b626422942b18cee6883d586fcf002e6f455a3c78547c991fa18ea916419effe`；完整观察另存。source17仍pc_alpine、owner/controller1、size19、损耗0、population5206；C/G/made/worlds/L/R／六tier0、D2，core2人口4809，五home守军保持，无目标我方运输／入侵军队，worlds／empires校准没有带入。Mother唯一159／997，design1495，实际PLANET_KILLER_GUN_01装配正确key且六core在AUX6～11。

59份实际copied_mod与manifest逐SHA相符，组件TXT SHA256 `0bf1314f69f410ffcbf14875680d2689453295ee317b16d47ae219920b62dd92`，实际为`windup={min=90 max=90}`、`total_fire_time=30`；旧自定义CSV不存在。原始静态报告SHA256 `2e249c08bb39a4e30ff9d2f3eea0983a5684b328bc5018b069002df38315f20d`保持，numeric_contract为native_csv_or_literal_txt_v1且literal值90／90／30／0已解析。实际EXE SHA亦匹配。以上只证明RC4组件配置和真实SAV装配绑定，原生时长行为仍待queued／day1及后续取样。

RC4真实queued Mar7 SHA256 `700f19e7ee6e786c3a5e4ea28ac67c5d12f829b0a39707aa58f66bd6a32a1ab5`，day1 Mar8 SHA256 `03511b65668f07133ec48b6da1a415f27cf5e47c1f89a292ef85ec302aa5abc3`，各原生audit／receipt／gamestate SHA均通过。queued的physical17 destroy_planet_order仍含移动子订单；day1实际转入`planet_killer_weapon_windup_order={windup=0 windup_time=90 ...}`，因此90参数已由真实订单确证。当前没有fire_time字段，30仅为TXT配置，不能写成原生发射阶段已验证。

`rc4-pk2-queued-day1-report-v1.json`18项限定PASS_SCOPED，SHA256 `8efe970dee9bbe59d259b3500c2f46ef67b96ff174dfbf5765144b54a0558be5`；base→queued原no-settlement九项通过，报告SHA256 `1eb7e5232d1348fce36907eb5dba5677cdaf5e8315a26850ec0c4a180a8aba82`。完整EEP country／Mother变量与modifier不变、core4809／capacity2、source5206／size19／owner1存活、两危机目标无新收益、五home守军和无自有transport均保持。source persisted q／colossus_active仍缺失，只确认live有效q19，不声称queued callback已经执行。

Mar8是首个采样到windup0的日期，精确起算tick尚未连续观察。建议独立下一日Mar9确认是否0→1；若实际按游戏日+1，90日边界暂估Jun8、30日发射边界暂估Jul8，阶段转换tick必须由后续原生SAV确定。base→queued strict FAIL三差异、queued→day1 strict FAIL64差异全保留；没有拿跨日数据伪装同日无收益PASS。整个90／30时长case仍PENDING，旧RC3 FAIL不变。

### RC4 PK2第一阶段增量归档设计（先于实施）

建立独立`evidence/1019-rc4-pk2-duration/` v1，仅白名单run112808已完成的boot／welcome重试、RC3未毁档原生载入、pk2base／queued／day1三阶段及相应真实菜单输入／GPU／OCR、SAV／audit／receipt、原字节manifest／全部59copied_mod／冻结source_snapshot／raw static gate、现有RC4分析报告与只读工具源码。首次开机过早F12动作完整保留，明确没有对应图像或SAV覆盖；随后实际欢迎页及正确载入材料独立列出。原始不存在的失败截图／日志不补造。

逐文件排他创建、读前后stat与双读SHA一致，复制后逐SHA相同；检查完整文件集合不含任何当前`pk2-charge-tick`／`pk2charge1`／stop-hover阶段或活动日志。这些后续仅在稳定后追加v2，不覆盖v1。新归档使用`* -text`，独立索引与verify核对三原生SAV／receipt／audit／gamestate、所有OCR对应原GPU图、59文件表与source snapshot／gate／manifest绑定、raw gate pre-canonical指纹不变。归档结果只供全新RC4 PENDING索引引用，不导入RC3任何预算或PASS、不开完整时长／发布通过，不操作UI／Mod／Steam／Git。

归档索引构建发现RC4冻结源实际使用`gate.json`，不是RC3的`candidate-gate.json`；首次复制所有payload已排他完成，索引在读取旧命名时中止。保留全部副本原字节，按实际`gate.json`重新双读验证并生成首次索引，不覆盖任何已复制文件；该错误属于归档索引路径约定，不是Mod或原生运行失败。

RC4 v1归档已完成265源文件／15,174,376字节，20项集合／字节／原生来源检查全true。`1019-rc4-pk2-duration/archive-index-v1.json` SHA256 `b82cc8fb9ad0ab8fd67c4b9df2454837fb9f91ecdc452930e57d0286329d2712`，verification SHA256 `57d7ef97acfcff9382de1db6345f5e56f02d96fed90bbba3fc9aa53f1de95949`。独立manifest SHA256 `a83c605727f30a1d68db0e076348d814824d8ca56020ca2ab8864db8194f44f1`；三SAV／59文件源与copied／raw gate／实际输入GPU／分析均归档，charge1／Stop／cancel／活动logs没有混入。已提供发布agent建立全新RC4 PENDING索引。

v2增量设计：待charge1与cancel各原生receipt齐备后，追加Mar9 charge1计数、原生Stop按钮tooltip／hover／实际鼠标点击、同日cancel及其独立no-settlement／订单清空／全账本报告；两份实际名称编辑Ctrl+A也须归档。原v1所有payload与索引均不改。白名单仅charge-tick／charge1／select-charging／stop-hover／stop-tooltip／stop-charging-native／cancel／cancelled-state，截止取消后稳定frame；不收录后续requeued／月度autosave／活动日志。shortcut H只作为真实tooltip观察，本轮实际为鼠标点击，不冒充已按H实测。

charge1 Mar9原生SHA256 `c6d861d7ec8751586f8516efbf6fbd2b6e60c5d4bc6fdd2bfdc42613feebfba3`，实际windup1／windup_time90，较Mar8的0确实推进一游戏日＋1。cancel同日Mar9原生SHA256 `add4d9de449008c49a8885ddd6fb08d828544f7a22441eda05f45da086b2cd07`，原生订单清空。Stop真实hover／mouse click均client69,339（desktop837,675），GPU显示停止全部命令tooltip及充能1%，取消后“无指令”；H仅肉眼可见的快捷键提示，本轮没有按H。

`rc4-pk2-charge1-cancel-report-v1.json`19项限定PASS_SCOPED，SHA256 `56b26b89a75b8516f99fedadb52a0f921a79a7bf53ed0881b4798a74bec16669`；既有同日no-settlement九项全true，报告SHA256 `638c5952271b942b15bacacc29aad74c3372cf0258bfbf0f1d8bb67ce121a066`。全部EEP country／Mother变量与modifier、core/source完整原生快照、人口组／岗位／库存／危机均相等；source17 owner1仍活，core4809／capacity2，source5206，无目标我方入侵军队。strict保持FAIL一差异（Mother raw订单移除）。source q／active原本就未写入，本次不能认证带有效snapshot时的清理hook；重排必须新起算，不能累加取消前一日，完整90／30时长仍PENDING。

RC4阶段归档v2完成348源文件＝原265＋83新文件，20,061,431字节，13项追加／保留验证全true。索引SHA256 `3c60b1cc7f85131071a110a87dcfb2f96dbe3f6dfca89f15c234b26621104d13`，verification SHA256 `508b40302a4ada44ec66e9889f00e1062741e2cad76f72ebf50870c18f60f3c2`。v1索引与全部payload原字节不变；phase2严格截止取消后frame，含charge1／cancel两原生SAV／audit／receipt、Stop实际输入／GPU／OCR、两Ctrl+A及新分析，没有后续requeue／月度推进／活动日志。发布agent按新索引版本引用，全部case和完整duration仍PENDING。

### RC4重排队与月度计时只读分析设计

独立读取cancel→requeued同日原生SAV，保留完整strict差异；检查订单重新出现且windup归零，全部EEP账本／危机／源星与core完整状态不变。后续仅在每份真实autosave／audit／receipt齐备并SHA核验后读取Apr1／May1／Jun1，比较原始订单计数和360日原生日历差，不用文件名称或UI百分比替代实际字段。跨月人口、库存等自然变化单独记录，不能以跨月严格差异不等冒充收益，也不将跨月数据放入要求同日的no-settlement检查。

新增独立analysis脚本只读取这些已完成证据，提取原始destroy／windup／fire子订单、目标与core账本、所有EEP变量及危机目标；报告明确原始字段与未知字段，不尝试实现完整引擎trigger解释器。guard证据仅原生字段对应的限定事实，资格／digestible等脚本条件必须引用本run冻结源码，缺完整原生字段则保留UNKNOWN。不得操作UI、生成未来存档、修改业务Mod／原SAV或扩大已有PASS范围。采集路径失败、恢复原字节和没有重复推进须保留；完整shot后再一次性追加归档，不复制活动logs。

重排队Mar9原始SAV SHA256 `64e34870d6f4a59e1c6b32ce140ece4b48dddab8752de0c59017f0ff88022708`：新destroy order_id=2／fleet order_id=3，physical17子订单已是windup=0／windup_time=90。它同日在射程内直接开始新充能，不能沿用首轮Mar8起算或额外移动一日的暂估；取消前1／90不累计。按后续每日＋1条件推算Jun9为90边界、Jul9为30日发射边界，仍需真实阶段转换tick确证，不提前宣告fire_time字段或完成日期已验证。

主线程授权补充Jul1自然人口基线：等`pk2prefire`的immutable原生receipt稳定后，只读获取加载目录`acceptance-fixtures/autosave_2200.07.01.sav`，以真实`pk2-fire-to-lastday-command`开始UTC／mtime、ZIP CRC、meta日期及实际Mother归属验证新鲜性，排他原字节复制为artifact `pk2firejul.sav`，派生原生country0／1 audit并生成明确`native_ui_save=false`的自动存档receipt。该日没有独立HUD截图，不伪造有；Jul8真实prefire档与Jul1自动档分别保留各自来源。事前预期Jul8→Jul9非月初自然人口delta为0，不能按最终人口结果倒推自然项。

重排／月度／fire0首版28项报告已生成，但复查发现其中live q19的表达式错误地尝试读取不存在的`eep_damage`变量。冻结真实`eep_damage_count`是count_deposits(type=d_lithoid_devastation)，不是变量。该fixture实际这类deposit数为0，结论未变；仍保留v1原字节，不将错误依据视为认证，v2必须直接逐份读取实际deposit表并引用冻结script value来计算原生损耗和q。其余原生计数、来源与strict差异不改。

Jul1补证实际失败：在Jul8 `pk2prefire.native-save.json`稳定后按授权检查，`acceptance-fixtures/autosave_2200.07.01.sav`不存在，完整save-games文件名只列出新`autosave_2200.07.08.sav`及Apr1／May1／Jun1。读取在stat处抛FileNotFoundError，未创建任何Jul1 SAV／audit／receipt；不把Jul8自动档冒充月初、不伪造Jul1 HUD。该项作为明确缺失保留，事前Jul8→Jul9自然人口0预期仍依据同月日历和既有原生日步长范围，不声称独立Jul1基线已取得。

重排／计时修正报告v2为28项限定PASS_SCOPED，SHA256 `30ce2a2f010a2bf9bdcd260f7fd69c21567fedc0ab676d755f47bc5d006a00df`；cancel→requeue同日no-settlement九项全true，strict三差异保留。Mar9 windup0→Apr1 22→May1 52→Jun1 82→Jun9原生fire0／fire_time30，与实际22／30／30／8日一致，90日充能行为已由真实阶段转换确证。所有EEP账本仍初值、source live q19／owner1、两毁灭目标无提前收益；敌舰目标75→90与跨月人口变化单列，完整发射30日与结算仍PENDING。

Jul8 prefire实际fire29／fire_time30、source owner/controller1仍活，core4828／source5317；Jul9 fired真实receipt SHA256 `69a36461a8ee6617b3bd7ce6d1ff183716a0a34cad1c843c12ee018092bb53eb`后，目标已pc_shattered／无owner、订单清空、C19/G19/D6/made300/worlds1/L1、last4／300／0，原生worlds目标750。但是原始empires目标无记录、按既定规则为0，不能声称600已到账。country1仍在原始country表且带destroyer_country=0；它在Jul8仅physical17拥有owner1，Jul9实际world owner1列表为空，资本／人口cache尚留。尚不确定是延后销毁还是last-colony脚本条件未命中。

结算case先保持独立原生校准750／600、自然人口0及所有严格检查，真实运行保留缺600的FAIL，不能将expected_empires改0来迎合。将单独追踪Jul10／Jul11的原生目标与country状态，再区分原生延后奖励、显式重复callback和真正漏奖；未有证据前完整巨像case不通过。校准同一原生宇宙的Jan2与Jul8国家ID／type集合相等、仍四个default，galaxy设置保持，但这不冒充重新完成过一次RC4校准。

实际原checker Jul8→Jul9为23／25，除empires0而非600外，`source_colony_destroyed`仅直接`employable_pops=5317`缓存一项失败；其它七项pc_shattered／失去所有权／实际人口与group／job列表空均真。保持旧报告及checker不变。

Jul10 `pk2dupe`真实SHA256 `b2b65422bd5acd4b08ec493710a3ed5f612ca710517e148522cddade9d4f714b`，country1已消失、empires目标600、worlds750不变，colony1的employable_pops已缺失，EEP账本全部不变。这提供原生下一日销毁／目标奖励／缓存清理的真实补证，不能把Jul9的即时FAIL重写为PASS。主线程该日命令误用了不存在的DISMANTLE回调key，原始actions／error保留，因此此档只能作自然＋1日对照，不认证重复回调。后续正确DEVOURER双回调和重载分别独立保存验证。

稳定结算v2方案改用Jul8真实prefire→Jul10实际稳定档，保留完全相同q19／自然人口0／worlds750／empires600期望及全部25项严格条件；它是等待原生销毁tick后的结算结果，不是调整奖励预期，也不放宽缓存活性模型。90＋30日期行为仍独立用Jul9真实完成档证明，稳定结果报告不能把实际武器完成日期推迟到Jul10。

稳定v2实际原checker已25／25 PASS_SCOPED；core人口Jul8 4828→Jul9 5128→Jul10 5128，只有恰300制造人口，无敌人口返还、无额外自然人口，原check源码SHA保持681836d2。Jul9即时报告原FAIL和完整strict差异均保留，后续仍需正确callback／重载去重证据。

colossus只读线由原生generated文档核实：`any_owned_planet`迭代当前帝国拥有的colony，`num_owned_planets`统计planet／ship colonies；scopes文档直接给出planet→owner→any_owned_planet对prevprev比较的例子。因此controlled非殖民矿星导致last-colony条件失败的先前假说被排除，不能据此改生产判断。Jul10真实原生灭国补奖600与cache清理是本夹具实际观察；即时与稳定结果仍分别报告。

新duration首版23／24的唯一FAIL是分析脚本错误假设fleet原生体有owner字段；实际fleet159无owner标量，归属存于country.fleets_manager.owned_fleets。该首版与错误假设保留，v2只以各真实SAV的全country拥有舰队表反查fleet159当前唯一归属0，并结合core物理owner0认证受益者，不用ship.original_owner冒充当前拥有者。其它90／30及结算日期检查原样保留；不改任何Mod或公共checker。

`rc4-pk2-native-duration-report-v2.json`实际24／24限定PASS_SCOPED，SHA256 `eb710c8fbfe827e44c8540bfeab45ac33f5992113e35ded7b2dd1ca67e1722c5`。即时25项报告23真、SHA256 `0a53c3514a0369d6bb334b149659c051edeca127364320a83124f3ca4878fe71`，strict105；稳定25项全真、SHA256 `c4faf33a86831e7fd67ca0c645758a4cd57045a995832e697d3987050f6f2059`，strict148，全部真实差异不忽略。

Jul11正确DEVOURER双回调后原生`pk2dupevalid` SHA256 `8e48334f2bea86c10149167749ff855a02fc57fe6a02ae8dd871a9bdd0c4ba0f`，人口5128、所有EEP变量与危机worlds750／empires600均保持。回调真实输入用显式FROM=event_target:eep_mothership0，区别于前一日错误DISMANTLE键；最后原生重载与一次正确回调仍待独立保存证据，不先通过reload检查。

### RC4完整shot阶段增量归档v3设计

等正确DEVOURER重复callback与原生重载后的`pk2dupereload`原生SAV／audit／immutable receipt及最后稳定frame齐备，再一次性追加完整shot包。v1／v2索引与348源文件全部保留原字节，仅在phase3新排他目录追加重排队、三真实月度autosave、Apr路径失败／恢复、fire0／prefire／fired、错误DISMANTLE派发自然对照、正确双DEVOURER派发、原生load及重载后重放的SAV／audit／receipt／实际输入／GPU／OCR、全部新分析及明确单时点error.log样本。7次新增原生菜单保存名的Ctrl+A按name-field实际mtime与name typed UTC之间匹配原始press记录，不能仅凭数量猜配。

白名单严格为该已完成PK2阶段，截止最终稳定frame；不复制任何活动logs目录、不混入后续成长或新开局。Jul1缺失和首次路径失败均保留，不补不存在证据；原RC3 duration FAIL、RC4即时结算FAIL与分析假设FAIL全部作为历史诊断留证。新索引逐文件source／dest／SHA、读前后stat和双读原字节，独立集合verify、15份本run PK2原生SAV各audit／receipt／gamestate核验、59文件冻结source绑定和v1/v2不可变核验。这里只认证该enemy shot受限范围，owned／normal／Lithoid／完整guard矩阵及正式发布仍未完成。

正确callback与重载报告`rc4-pk2-valid-callback-reload-dedup-report-v1.json`实际28／28限定PASS_SCOPED，SHA256 `d8d093ba60dc2f10feb8e658ca414baec9069a7ef914919f8830b79ca7593736`。Jul11→原生load→一次正确callback→Jul12 SHA256 `86c1f000b1adcf260f27d0cd2ae23fb13e8b2e98045425197c92d0962d152408`，EEP账本／六tier／单成长modifier／五once时间戳／人口5128／危机750600保持；完整strict33与20差异原样保留，不宣称full-state reload完全等价。错误DISMANTLE输入另留，未计为正确重复测试。

主线程完成worker正常退出后指定fresh `pk2-complete-final-state`为本包截止；后续原版CRACKER或guard校准使用其它prefix，不扩入PK2 v3。最终error单次字节样本必须包含20:05:42无效DISMANTLE以及20:09:31原生nomads.94错误，不能过滤或声称运行无错误；原版对照调查属于下一独立阶段，本包仅记录已知错误与精确采样时间／字节区间，不做完整run日志冻结。

v3首次复制已排他完成所有payload，索引前最后16项验证中15真，唯一“source path必须全唯一”断言失败：既有v1/v2刻意把同一冻结`candidate-rc4/open-kaishek.json`保存在`source_snapshot/`与`static-acceptance/`两语义位置，原348份payload实际347个source。这不是字节差异或原生失败；不能删改旧表来迎合新增断言。保留首次复制全部字节与失败的builder原源码，在独立恢复脚本按确定性source→dest重建表并再次核所有字节；改为校验重复source所有目标必须同SHA、来源别名明确列出、新增source仍唯一。任何payload不覆盖，首次索引只在恢复验证全部通过后新建。

PK2完整v3已稳定：798份payload＝原348＋新450，47,542,644字节，22项验证全真，15份本run真实SAV／audit／receipt／CRC／gamestate与127对OCR／GPU哈希核验通过。索引SHA256 `1b371ae6e6c33bc1841af895bb94bb7e037d0a7b7da20bd689045d70e7afaf64`，verification SHA256 `730ccb110ac9ff111a916965628cb9c7c6f71fbc8c83d7f8b8a37ab922e27262`。另以独立第二进程重新打开最终索引／809个实际归档文件的完整集合／全部798份source与dest／15个ZIP，8项全真，报告SHA256 `7c4ef92c4d5a1c441f4ca677ea568f14422f04d1b721582811bc000528f80272`。v1/v2及所有既有payload不变，source别名明确同SHA，不收后续pk2nativecontrol。

原生主种族人口也独立核对：core实际pop_groups仅species3321888769，Jul8 4828、Jul9／10／11／12均5128，制造300全为实际country0 founder_species_ref，没有把敌方species2返还。最终分层summary仅合并本次enemy shot的90／30时长、25项稳定结算及28项正确callback／原生重载去重范围；即时FAIL、全部strict差异、缺失Jul1及日志原生nomads错误仍保留，完整Mod发布与18组矩阵继续PENDING。生产Mod、公共checker与inspector未改，未操作UI／Steam或提交Git。
