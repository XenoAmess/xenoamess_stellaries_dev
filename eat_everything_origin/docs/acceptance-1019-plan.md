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
