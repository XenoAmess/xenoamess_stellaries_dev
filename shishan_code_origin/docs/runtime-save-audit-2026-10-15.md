# 反馈改版原生存档只读审计

## 2026-10-15 rc.4 主物种指针缺口与修复设计

原生三档对照发现，旧审计器 `locate_main_species` 将权利模块 `primary.species_index` 当作实际 main species，来源不充分。`fb453_reroll1` 顶层 `country.founder_species_ref=3321888769`，领取后 `fb454_claim1` 及跨月 `fb454_claim1month` 均变为 `50`；权利模块 primary 仍指旧 `3321888769`。新物种 49/50 的 `base_ref` 均为旧主物种，故本例旧来源没有改变 U 的谱系统计，但实际 main ID 被误报旧值。不得把旧 primary 未变写为 dominant 迁移失败，也不得将没有 49 显式 rights 行直接写为默认清洗；具体权利 getter 仍由原生脚本/UI 查证。

原始国家标量、权利 primary 和物种链已保存 `runs/20261015T080652Z/rc4-main-pointer-investigation.json`。4.5.2 生成 `scopes.log:130` 说明 `owner_main_species` 指 owner 的主物种，`effects.log:1437` 说明 `change_dominant_species` 修改当前国家 dominant；文档不公开保存字段映射。与真实 effect 前后只有 `founder_species_ref` 和 `default_species` 对应更新的证据合并，目前可以判断权利 primary 不能替代主物种指针；最终 getter 与 50 的对应由主任务原生 `owner_main_species` 交叉核对，并在此补记。

主任务随后完成正确 canonical key 的原生交叉确认：`trigger owner_main_species = { has_trait = trait_robot_artificial_engineers }` 最后返回 TRUE，`trigger owner_main_species = { has_trait = trait_robot_learning_algorithms }` 最后返回 FALSE。50 的原始 traits 恰有工程核心、没有学习算法；49 两者都有，旧主两者皆无。这两个结果共同区分50、49和旧主，与保存的 `founder_species_ref=50` 一致。对应照片为 `rc4-focused-getter-engineers-result.jpg`、`rc4-focused-getter-learning-result.jpg`；准确命令在同名前缀 `.console.json`。本审计只读索引其路径与 SHA-256，原生结果由主任务目视确认，证据 `rc4-main-pointer-native-getter-evidence.json`。此前错误 `trait_robot_engineers` 键或未聚焦输入的 FALSE/空输出仍作为操作者探针错误保留，不纳入该结论。此交叉确认不负责解释 rights 模块的隐式回退。

修复范围仅本工具、其单元测试与本文：主指针改读国家顶层唯一的 `founder_species_ref`，若缺失、重复或指向未知物种明确失败，不回退到 rights primary；后者及 `default_species`、`owned_species_refs` 仅保留为独立原始定位证据。`base_ref` 链继续单独解释谱系，不能把 root ID 误当当前 main template。新增小型内存输入验证 founder 与 rights 指向同谱系不同模板、不同谱系时均以 founder 为准，以及缺失/重复/未知 pointer 的负例；新增真实 R4 领取档只读回归，期待 main=50、rights primary=旧主，同时维持真实 P/W/U 与 native traits。此阶段不修改生产 Mod，不新增实机指令，不对权利模块的隐式回退语义作推断。

该修复已经完成，reader 定向回归从 12 项增加到 18 项，全部通过、无跳过，证据 `_runtime/shishan_code/20261015-runtime/rc4-native-main-pointer-tests.json`。这是审计工具修改后的受影响回归；先前 `rc4-unit-agent-452.json` 的 83 项仍保留为修复前快照，未假称已覆盖新增六项。

主任务随后要求修正 reader 后的一次完整交叉回归：`python -B -m unittest discover -s tests -p test_shishan*.py -v` 实际执行 89 项，全部通过、无跳过，16.198 秒，退出 0；唯一新最终报告为 `_runtime/shishan_code/20261015-runtime/rc4-final-unit-agent-452.json`，未覆盖 83 项旧快照。国家主模板依赖顶层唯一 founder 指针与原生谱系链；rights primary 的独立保真记录仍可与其不同，不能据旧 primary 断言国家主模板没迁移。完整程序回归只证明工具和数据合同，不替代主任务正继续执行的原生 getter 与 CD 交互证据。

## 2026-10-15 rc.4 冷却原生保存序列阶段证据

按主任务通知，只读解析旧原生输入 `fb453_reroll1` 和本次 rc.4 `fb454_claim1`、`fb454_claim2`，没有操作游戏或主动轮询未通知文件。三档分别观察 `(n,CD,R)=(1,3,0)→(1,2,0)→(2,1,0)`；输入候选17/12/1，领取后两档 slots 均为0/0/0、pending/window/成功凭证/ready 均已消费，架构 modifier 均只有一个实例。新 claim2 的 P5581/W45189、U45189/5581 与当前观测及实例 scale 匹配，独立存档审计 PASS。前缀检查报告为 `runs/20261015T080652Z/rc4-cooldown-partial-independent.json`，原始 claim2 报告为 `fb454_claim2.independent-programmatic-audit.json`。

此处仅确认保存后状态和已给定输入的前缀，不从一次保存证明实际 on_success 调用次数，也不宣告完整 CD3→2→1→0→重选3→确认2 已完成。后续 claim3、第四票重选前后、清理期间 pending、claim4 等原生检查点收到通知后统一比对，另写最终报告，保留这份阶段证据。

## 2026-10-15 清理后同日重开候选失效调查

主任务在清理后重开已有奖励票，实际 UI 无实体选项且 R0→1，随即暂停领取验收。已独立只读保存的 `claim3 / fourth_pending / fourth_rerolled / clean_pending` 四档，原始对照保存在 `rc4-clean-pending-independent-investigation.json`。依次观察 `(n,CD,R)=(3,0,0)→(4,0,0)→(4,3,0)→(4,3,0)`；第四票 slots1/7/5，重选为11/9/12，同tier1且唯一，清理后的保存仍保留同一pending/rerolled与11/9/12、R仍0，并没有在该保存时刻误发重复层。

清理只将主模板54→56、子模板53→55，状态 raw key `trait_shishan_code` 替为 `trait_shishan_refactored`，两者实际人数仍5040/553、键数9/10，P5593/W50890/U9.09887不变。原版互斥与当前实际 traits 表明：11学习算法对main56仍合法，9情绪模拟器和12量产对两模板都合法，refactored本身不在这些互斥列表。

同一原生 `clean_pending` 的 `country.owned_species_refs` 仍为旧53/54，两者已经没有国内实际人口。当前生成 eligibility 从 `any_owned_species` 枚举后，再要求一个实际人口组 exact 相同；如果原生该枚举使用滞后的列表，所有条目都会因国内人口为零失败，refresh 会清空slots、tier0并将保存的未领取票误当奖池耗尽转成R。这是当前数据与实际脚本共同指出的原因假设，待主任务原生缓存/人口两种 iterator 的对照探针与重开后原生保存进一步确认，不能先把其写为已经直接观测到的引擎内部实现。

下一只读复现范围：独立以该保存实际popgroups55/56与缓存53/54各建明确fixture，执行冻结产物 eligibility/refresh，比较三条实际候选与R的变化，预期不得再假设克隆后物种枚举立即更新；模型只说明当前脚本对这种输入状态的结果，不宣称引擎迭代细节已经通过。暂不修改冻结Mod、工具或生产fixture，也不继续把清理后的完整CD序列判为通过。

复现已经完成：`rc4-clean-pending-cache-ast-reproduction.json` 在没有资格override的实际脚本执行中，缓存53/54输入产生三个false、R1/tier0/slots0/pending消失；实际人口模板55/56输入则三个true、R0/tier1/11,9,12/pending保留，CD两者均3。随后主任务原生cache probe确认FALSE/TRUE，定位到枚举缓存，已停止rc.4运行并由架构子任务实施rc.5人口组入口修复；不是refactored状态key本身让候选非法。

rc.4完整保存前缀报告另存 `rc4-cooldown-prefix-final-independent.json`：seed/claim1/claim2/claim3/fourth_pending/fourth_rerolled 的CD为3/2/1/0/0/3，n为1/1/2/3/4/4，R均0；每档架构实例唯一，第四票重选前后三候选同tier1、各自唯一且完全不重叠，pending保留。报告明确第四次claim没有成功、CD2没有观测，不能用静态预期补齐；完整工作流随后在清理重开失败，前缀PASS不替代全流程PASS。

修复后的checker完整99项与149组canonical资格回归详见[程序性合同记录](feedback-redesign-programmatic-2026-10-04.md#2026-10-15-rc5-物种缓存滞后回归设计)。原生reader接口没有因rc.5再改；后续新原生保存继续按当前主指针/实际人口组独立审计，源版本及运行目录必须与旧失败现场区分。

## 2026-10-15 rc.6 最终已赚奖励与同日清理复放的只读结果

本节只读 `runs/20261015T090720Z` 中主任务真正保存的rc.6 native文件。所有原件及逐档 `*.independent-programmatic-audit.json` 保留，未操作GUI或修改生产。主任务实际领取动力钻头的 UI 结果，与 `fb456_white_reboot_month → fb456_natural_claim` 原始数据一致：人口5474不变，W32844→38318恰好增加5474，U6→7；n1/R0/CD0均保持，候选票消费，架构modifier唯一。白绮仍为同一领袖ID16777294，经验25、等级5、肖像 `shishan_code_vivhite`、traits、可选特质及选择次数保持；species旧主→48，原生 `should_not_have_upkeep` 前后存在；7名owned leaders的ID均保持。限定对照见 `rc6-natural-claim-independent-comparison.json`，这是非零经验在实际物种克隆过程中的保持证据，不能冒充完整死亡/重启流程或免费UI证明。

上述输入 `white_reboot_month` 的严格即时架构审计仍保留 FAIL2：保存的月缓存P5469/W32814，实际人口P5474/W32844。领取时主动刷新后的 `natural_claim` 已全MATCH。比较报告明确“U+1和领袖保持”通过不覆盖源档刷新时点的缓存失败；没有因为两者U同为6就把P/W也写为通过。

最后两档为同日2204.04.01复放：源是R4 `fb454_fourth_rerolled`，RC6 `fb456_clean_pending` SHA-256 `4daada20d345e31989f53cc8fa9eb2ec1ec31001eb00fffead1de7dd447980c1` 中实际main55、pop模板55/56，cached `owned_species_refs` 仍53/54。人口组入口已正确保留earned票的slots11/9/12、n4/CD3/R0与pending/rerolled。按当前安装的完整原版互斥表独立核对：11学习算法覆盖main55的5040人（另一模板已有该key）；9情绪模拟器和12量产覆盖全部5593人，原版DLC/禁止伦理无额外门槛。三条都仍有实际可授人口，不依赖缓存列表或生产资格常量生成预期。注意新入口的分配顺序与R4不同，不能硬把main55误当旧报告中的sub55。

RC6实际选择情绪模拟器后的 `fb456_claim4` SHA-256 `13c8314f020292cafa7256d74ad41cc831d2d6ec8486375ac3d8090f1fe616b8`：main57、P5593不变、W50890→56483，U恰+1；n4/R0保持、CD3→2，slots清0、pending/rerolled/window/ready/成功凭证均已消费。两个rc.6档的架构观测与唯一modifier scale全MATCH。独立报告 `rc6-clean-claim4-independent-comparison.json` 保存全部原始定位/traits和canonical覆盖证据；三实体选项的实际UI另由主任务截图 `rc6-clean-earned-options` 证明，本报告不把保存数据当作已查看UI。

额外直接对照这两个原生档的完整species数据库：仅新增57/58两个物种ID，全部既有species记录原始字段不变。这为一次已选trait对两个实际模板各克隆一次、未改旧共享物种定义提供原生数据证据；没有只根据当前人口恰好落到两个新模板就忽略可能的多余未用clone。

该报告明确完整CD证据由R3已赚重选seed、R4前三次领取及第四票重选、RC6从同一R4第四票输入复放清理后最后领取组成：CD3→2→1→0→第四票0→重选3→清理仍3→确认2，R各保存点均0。冻结R4与当前rc.6的CD赋值、递减和比较AST投影完全相同；资格枚举和窗口预检是rc.5有意修复，不能称整个脚本未变，也不能称整条序列在同一个run从头跑完。R4原始清理后空选项/R1失败证据保持原样。

## 2026-10-15 rc.6 旧档重复层及真正重载的最终只读结果

收到三档齐全通知后，一次比对早先R2原生 `fb452_legacy24` 与本轮R6 `fb456_legacy24_reload → fb456_legacy25 → fb456_legacy25_reload`。原源SHA-256 `5e911d9f56d271542068f4c99182f74c9efa86d187fdef9c6633ad4a2391c32a` 重核一致；本轮三档依次为 `70eb20b1317bac4cfea4df947892817f24e6e03fc817f2466d52a9142a71574d`、`9fba512f450559cadc239058d291809ef23c11d5a6253bdcf96c0d14593ba28c`、`fc6da734a763ad377b84db1729808055cab2d243e1c7510199494d5de2425d5e`，均真正保存的4.5.2 native文件。

各档旧四计数始终7/5/11/4、迁移flag保留，P5567/W239381、全部实际模板43个正式键、U=43。三档R为24→25→25，n为1→2→2，CD始终2；架构modifier各只有一个实例，scale为67→68→68，所有即时架构观测MATCH。新增耗尽层没有实体pending/ready/window或未消费成功凭证，三个slot变量在源与新三档均未保存，明确呈现 `ABSENT/null`，没有把缺失伪填为观测0；“没有非零实体槽”与“没有实体票据”条件均成立。

最终报告 `runs/20261015T090720Z/rc6-legacy-repeat-reload-independent-comparison.json` 为PASS，包含逐档完整变量、flags、实际traits、modifier及项目原始记录；每个新档另有 `*.independent-programmatic-audit.json`。第一版比较误要求slot必须显式保存0，其FAIL报告另留 `rc6-legacy-repeat-reload-initial-slot-assumption.json`；修正的是本次报告中过严的观察要求，不是修改原生输入、生产代码或把缺失当已观测0。

中间由主任务本次原生 `complete_special_project MAINTAIN` 触发真实on_success，最终档由原生加载菜单重新加载R25再保存，操作证据为 `rc6-reload25-list / rc6-legacy25-reloaded`。本审计不操作GUI，只由保存的R/n不再增加、旧历史不变独立佐证“本次加一层且重载未重放”，不把快照当作全部引擎调用次数的跟踪。此结果是R2旧来源接入R6的迁移/耗尽/重载证据，不能写成同一新自然局从头积累到R25；原始CD2输入是旧来源受控条件，持续保真记录。没有改动已验收生产源码，不需要因只读报告重复运行107项程序测试。

新领取档只读报告为 `runs/20261015T080652Z/fb454_claim1.audit-main-pointer.json`：main pointer=50、rights primary=旧主分别呈现；P5551/W39368/U7.092055485498/R0，全部架构比较 MATCH。跨月报告 `fb454_claim1month.audit-main-pointer.json` 明确 FAIL：即时 P5581/W39608/U7.096936032969，观测缓存 P5575/W39560/U7.09596，唯一修正实例 scale=缓存7.09596；P/W/U/T 和 modifier scale 共五项诊断。未因差值较小、bonus/M 落在独立容差内而将整体写为通过。这与月份刷新缓存边界相关，主任务随后可经详情主动刷新另存新档验证；本报告没有推断权利49的实际解析结果。

balance 子任务补充独立原始人口对照 `independent-rc4-month-population-audit.json`：month 观察时点位于自然组装后、下一次主动刷新前，差额 6 人口/48 权重来自子模板49的 civilian 组装 +6；该子模板总人口511→541，实际 miner 工位一直使用500 worker。其同日 pending2 档所有人口组与 month 相同，主动刷新后缓存等于即时5581/39608。这说明上面的严格即时 FAIL 是两次观察时点间的缓存滞后，不能解释成 clone 丢人口或遗漏整个子模板；失败原件仍予保留。

收到确切文件名后，本审计也独立解析 `fb454_pending2.sav`：日期同为2204.02.13，main=50、即时与缓存 P5581/W39608 一致，架构各项比较 MATCH。新只读报告 `fb454_pending2.independent-programmatic-audit.json` 为 PASS，旧 month 缓存 FAIL 未覆盖。权利49的完整公民/体面生活/完整服役结果来自主任务实际 UI，不能由此人口/缓存报告推导。

日期：2026-10-15。承接[本轮实机验证计划](runtime-feedback-validation-2026-10-15.md)第 4 项。本工具只读取 Stellaris 已保存的原生 `.sav`，不创建或修改 `gamestate`、不操作游戏、桌面或 Steam，不把离线审计视为实机操作已经通过。

接口为 `python shishan_code_origin/tools/audit_feedback_runtime_save.py --save <原生存档> [--report <JSON路径>]`。全部采用 Python 标准库；报告包含原存档 SHA-256、ZIP 成员、meta/game 版本及日期、由 `player` 块定位的玩家国家、原始 Mod variables/flags/modifiers、项目状态、国内真实人口组与物种模板、全部正式 trait raw keys、独立计算的 U/迁移 R 和观察值差异。玩家国家不能固定为 0；多玩家或其他无法唯一定位的情况必须明确失败，不能猜测。

解析器按原生 P 格式读取直接子项，保留重复项与裸列表成员，忽略字符串内的括号和注释；按需读取各数据库，避免把国家内嵌的另一个同名 key 误当作顶层字段。国家通过 `player` 条目中的 `country` 关联 `country` 数据库。人口组的 `planet` 和国家 `owned_planets` 在此版本指向顶层 `colony` ID，并非 `planets.planet` 的物理星球 ID；必须继续沿 `colony.carrier={type=planet reference=<物理星球>}` 核对真正的 `owner`。已确认 RS04 中 colony 0 的物理 carrier 是星球 8，物理星球 0 是恒星；直接把两种 0 当成相同对象会错判所有权。人口统计读取 `key.species`、`size`，并交叉核对殖民地列出的 `pop_groups`。容器、物种或谱系关系缺失/冲突时失败，外国人口不进入分母，空模板不进入 U。若游戏当前存档采用未覆盖的游牧/航母人口容器等结构，不把缺失数据当作零人口，而是记录无法完整解释的域并失败。

主谱系由玩家国家的主物种指针/权利模块及 `species_db` 的实际 `base_ref` 链和 identity 字段关联。报告保留定位依据；不能只凭特质相似、名字相同或朴素模板数量判断同谱系。每个被纳入模板的不同正式 raw key 各计一次，正/负/零点数/隐藏/偏好/第三方键均不筛掉；当前 Mod 没有内部物种载体，排除表为空。`U=sum(size*distinct_trait_keys)/sum(size)` 使用实际人口 size，不能用就业量、劳动力或物种模板数代替。

国家 variables 中的 U/R/T/bonus/M 仅作为观测值，缺失时报告缺失，不能用预期回填为已观察。旧四计数的独立迁移预期为 `sum(max(k-1,0))`，保留原字段和异常；迁移标志不存在时只报告迁移预期，不能假称已经迁移。浮点比较采用独立期望与明确误差，历史 0.1.3 档案可以合法缺少改版变量，报告仍须分清可解析数据、缺失观察与未执行新版机制。

基础验收先用两个历史原生档只读复核：`rs04-variant-anchor-2203.09.24.sav` 应得到主模板人口 5040、子模板 511，U 为 `33817/5551`；`shishan_reward_exhausted.sav` 应得到 43 个原始物种键，四计数 7/5/11/4 的重复部分迁移预期为 23。旧档的 meta 版本继续照实记录，不把它们当作本轮 4.5.2 运行证据。另以独立小型 P 文本检查字符串括号、重复项和非 0 玩家定位等解析边界，不向正式 Mod 或原生存档注入测试内容。

## 已实现与验证

工具已落到 [audit_feedback_runtime_save.py](../tools/audit_feedback_runtime_save.py)，12 项独立回归落到 [test_shishan_runtime_save_audit.py](../../tests/test_shishan_runtime_save_audit.py)。解析器只读原文件，报告保留 ZIP 与 gamestate 哈希、原版本和日期；新版观察字段缺失时明确写 `MISSING`，整体标记 `redesign_observation_status=NOT OBSERVED`。无从当前 traits 推断历史 R 的情况，T/bonus/M 的独立预期留空；不会把理论迁移后的 23 层当作存档中已经观察到的 R。

报告分别给出未约分的加权表达式和约分后的精确分数。RS04 结果为 5040 人口、6 键与 511 人口、7 键，分子 33817、分母 5551，约分为 `4831/793`。耗尽源档为 5561 人口、43 键，`239123/5561=43`；旧四计数的预期额外重复为 23。两者原版本均为 `Cygnus v4.5.1`，没有假标为本轮 4.5.2 原生运行结果。

此次读档还确认了一个原有正则风险：`portrait="sd_hum_robot"` 包含字符串 `trait="`，使用未限定字段边界的全文正则会把肖像误计为特质。本工具只解析物种 `traits` 块的直接 `trait` 成员，精确保留原始键。所有权通过殖民地/载体/物理星球及人口组列表交叉校验，外国即使共用主物种模板也不进入分母。

本阶段明确支持行星载体的殖民地，`carrier.type=ship` 或未知载体会返回 `SAVE_UNINTERPRETABLE` 并失败，不能以空人口代替。谱系按原生 `base_ref` 链解释；显式 identity 字段目前没有已验证的存档格式，遇到即失败并报告字段。完整实机验收不能从这些尚未覆盖的域推定通过。

收到主任务的首道 Kaishek 包级 `PASS` 后，2026-10-15 并发执行以下只读检查，退出码全部为 0：

```powershell
python -B -m unittest discover -s tests -p 'test_shishan*.py' -v
python -B shishan_code_origin/tools/validate_feedback_redesign.py --game 'C:\Program Files (x86)\Steam\steamapps\common\Stellaris' --report _runtime/shishan_code/20261015-runtime/programmatic-agent-452.json
python -B tools/shishan_code/audit_reward_contract.py --game 'C:\Program Files (x86)\Steam\steamapps\common\Stellaris'
python -B shishan_code_origin/tools/audit_feedback_runtime_save.py --save assets/shishan-code-origin/evidence/rs04-variant-anchor-2203.09.24.sav --report _runtime/shishan_code/20261015-runtime/save-audit-rs04-agent-452.json
python -B shishan_code_origin/tools/audit_feedback_runtime_save.py --save assets/shishan-code-origin/evidence/shishan_reward_exhausted.sav --report _runtime/shishan_code/20261015-runtime/save-audit-exhausted-agent-452.json
```

合计 44 项测试通过，其中原反馈改版 32 项、新原生存档审计 12 项。新增边界包括非 0 玩家国家、含括号/注释符的字符串、重复项、混合/外国/空人口、肖像不计 traits、未知玩家、未知载体、所有权/殖民地反向关联错误、缺失物种、未知 identity、谱系环和 meta/gamestate 不一致。独立 P 文本仅驻留测试进程内存，没有生成假原生 `.sav` 或修改原始存档。

新 validator 五项静态/离线合同全部通过，候选 Mod 树哈希为 `230b87c89debfcf202ee47e7efc51cf5418e01ba8cb64734d935367097dfa696`。奖励 audit 的 20 个原版机械候选及 56 组离线候选状态通过。十语言仅静态校验；加算回退与独立乘算未实现的边界仍照旧保留。本轮保存的 stdout/退出码证据为 `_runtime/shishan_code/20261015-runtime/unit-agent-452.json`、`reward-audit-agent-452.json`，其余完整 JSON 路径见命令。没有覆盖 2026-10-04 或更早的历史报告。

本子任务没有启动游戏、操作屏幕或 Steam；4.5.2 的真正运行、保存/重载和 UI 结果由主任务单独记录。本工具处理后续本轮保存的真实 `.sav` 时仍须照实报告其 native version/date 和观察字段，不能沿用历史档的通过结论。

同日后续复核：rc.1 实机发现了离线脚本解释器的 `pop_amount` 作用域与命名 script value 定义假阳性；修复设计与负例见[程序性合同检查](feedback-redesign-programmatic-2026-10-04.md#2026-10-15-实机发现的解释器假阳性与修复设计)。这没有把原生存档审计的 `size` 字段改成脚本导出，也没有改变原先两档的独立人口/traits 解析结果。主任务确认 rc.2 生产包新 Kaishek 门槛通过后，完整回归重新运行：38 项脚本合同回归加本工具 12 项，共 50 项程序测试通过，证据 `_runtime/shishan_code/20261015-runtime/rc2-unit-agent-452.json`。此结果不代表 4.5.2 的实际游戏执行或存档重载已经通过。

后续 rc.3 修正 NOT 的原生多子项语义、公开提示/隐藏执行和引擎自动本地化键后，最终生产/夹具门槛通过；完整程序回归含本工具 12 项共 62 项通过，证据 `rc3-final-unit-agent-452.json`。本工具也已只读解析本轮真正 4.5.2 存档并保留逐档 JSON：`fb452_mix0`、`fb452_sentinel0`、`fb452_pending1`、`fb452_legacy23`、`fb452_legacy23month`、`fb452_legacy24`。跨档报告明确记录 rc.2 候选 `[5,33,33]` 的混层/重复失败，以及月档 P/W 缓存落后即时人口的失败，没有因架构 U/R 恰好正确而宣称整体通过。后续 rc.3 的新原生存档应继续独立审计，不能复用这些故障现场作为成功证明。
