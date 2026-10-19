# EEP05 石质蜂巢设计合法性调查

## 目标、范围与验收

只读检查 `testing/single-homeworld-user-empires.txt` 中 EEP05 与本机 Stellaris 4.5.2 原版帝国设计规则，查找可由原始定义直接证明的无效字段；区分证实原因、未证实候选和不适用于设计合法性的运行规则。读取 portrait／species class／trait／authority／government／civic／origin、country_customization、galaxy／settings／DLC 定义和本轮配置，不启动或操作 UI，不修改测试夹具或 Mod。

整理进入简体中文编辑器红色错误说明的最短语义路径和截图／OCR 原始留证要求，不猜坐标或把本地化通用警告当作精确原因。若需要修复夹具，必须另补具体设计与验收方案后再实施，本次只调查。`nomads.94` 无效 from 继续保留为未解释错误，不因本调查过滤。

## 调查记录

已完成本轮只读核对，原始路径／逐文件 SHA256／带行号摘录见 [native-sources.json](evidence/1019-eep05-design/native-sources.json)，共 37 条来源记录。当前 `20261019T112808Z` 实际 `user_empire_designs_v3.4.txt` 与仓库夹具原字节一致；本轮配置读自运行中目录，记录为当时观察，不称活动配置 frozen。

**未找到可仅凭公开原版脚本证实的 EEP05 拒绝原因。统治者 `gender=not_set` 是目前最强候选，仍需原生红色错误提示确认。** 没有修改夹具，也没有把通用“未激活 DLC”合并提示当作 DLC 缺失证据。

| 检查项 | 原版依据与结论 |
| --- | --- |
| `LITHOID`／`lith11` | `01_base_species_classes.txt:143–165` 的 LITHOID 只排除 machine intelligence，要求 `has_lithoids`；`14_portraits_lithoid.txt:103` 声明 lith11；官方 `93_lithoids_prescripted_countries.txt:10–18` 实际使用该头像与 class。没有查到头像不存在或禁止蜂巢的定义。 |
| trait 与 authority | `02_species_traits_basic_characteristics.txt:33` 明确 hive trait 支持 LITHOID，:273 的 lithoid trait 支持 LITHOID；`00_authorities.txt:1215–1227` 的 Hive 需要格式塔、非 MACHINE，并提供 hive trait。EEP05 满足已列的限制。 |
| base civic 与政府 | `02_gestalt_civics.txt:227–253` 的吞噬蜂群允许 hive，EEP05 的起源及第二国策不在其禁配列表；:277–286 对 LITHOID、非荒野、非游牧交换石群显示。`civic_hive_ascetic:100–116` 仅要求 hive。`03_civic_governments.txt:784–799` 的 `gov_devouring_swarm` 需要 hive、非荒野和 base 吞噬国策，没有石质排除。不能改成只用于显示的 `civic_hive_devouring_swarm_lithoid`。 |
| Mod 起源 | 当前 `eep_origin.txt` 的 playable 要求 Nemesis，possible 要求非游牧与所列灭绝国策之一。EEP05 的 `is_nomadic=no` 及 base 吞噬国策满足所列 possible；EEP02 使用同起源。 |
| DLC | 当前 `dlc_load.json` 是 `disabled_dlcs=[]`，含义是禁用列表为空，不能读作“没有 DLC”。原版 `has_lithoids`／`has_nemesis` 分别检查 host 的 Lithoids／Nemesis；本机两份 DLC descriptor 和 archive 均存在。安装文件不能独立证明当前 host entitlement，也没有在这里证明 entitlement 缺失。 |
| 统治者性别候选 | EEP05 `ruler.gender=not_set`（夹具 :375），已观察可选的 EEP02／03 为 female；官方同头像 Khennet 的 species.gender 是 indeterminable（:17），ruler.gender 是 female（:61）。原版有专用 `GAMESETUP_LEADER_GENDER_MISSING`，简中 `main_3_l_simp_chinese.yml:3186` 为“统治者性别未选定。”。统治者 GUI :1473–1491 仅列 male／female／indeterminable；物种 GUI :403–409 另外存在默认随机性别按钮。不能把物种的默认 not_set 与统治者已选性别等同；但错误字符串和字段差异仍未直接暴露引擎校验分支，须实际提示确认。 |
| country_customization／galaxy／settings | `00_country_customization.txt` 通过权重选择殖民地首府与随机图形风格，没有列帝国设计合法性谓词。tiny scenario 只设置星数、帝国数和星系几何等，没有石质／蜂巢排除；`pc_continental` 原版 `initial=yes`。当前 `settings.txt` 为简中、1024×768、gui_scale=0.75；这些值不能解释该设计错误。`00_rules.txt`／`01_gui_rules.txt` 中未找到所查帝国设计校验 hook 名，不能据此声称不存在引擎内部校验。 |

## 最短简中 UI 取证路径（方案，未操作）

1. 在“选择帝国”页确认实际高亮的是 EEP05，并拍下右侧名称／石质头像／国策信息。若左栏名称被截断，使用实际观察到的条目与右侧身份交叉确认，不要求 OCR 凭不存在的完整左栏文字点击，不猜旧坐标。
2. 点击“编辑”。原版 `select_empire_design.gui:90–97` 的 edit 按钮使用 `CUSTOMIZE`，简中 `main_1:3075` 为“编辑”。进入后先悬停禁用的“完成”或“保存”，等待原生 tooltip 稳定，保存完整红色原因；不点击性别或其它会修改设计的控件。原版 `customize_species.gui:65–82` 定义这两个按钮，具体当前落点由截图确认。
3. 若完整提示指向统治者性别，再进入左栏“统治者”下的 `species_ruler` 外观编辑入口（GUI :338–358），页标题“初始统治者”，区域“选择性别”。原版另有“统治者外观”本地化键；当前实际按钮文字仍以截图／OCR 为准，不把静态 APPEARANCE 键直接当已观察文案。拍下是否存在性别选中状态，仍不改变或保存。

最少需要：编辑前 EEP05 身份截图、未改变设计时完整错误 tooltip 截图及 OCR、必要时统治者页截图；每份保留原始图、OCR JSON、实际动作 receipt、UTC／run manifest／EXE SHA、语言与分辨率。OCR 应核对可能的精确字串“统治者性别未选定。”；若显示其它或多条原因，必须全部保留并按实际结果调整候选，不能只截通用警告。

`main_3:3174–3175` 的保存／下一步通用红字同时写“设计包含错误”与“禁用／未激活 DLC”，不能用于二选一归因。实际精确原因尚未取证前，不修 fixture、不声称 EEP05 设计已通过。后续若只修改 ruler 性别作受控夹具验证，应另先记录单字段修改、原生选择／保存与前后字节差异的验收方案。

`nomads.94` 因果仍未解释，相关最终日志保持原字节，未过滤。
