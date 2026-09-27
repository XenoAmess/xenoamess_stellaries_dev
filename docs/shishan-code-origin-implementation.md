# 「屎山代码」独立 Mod 实施记录

状态：实施中。目标游戏：本机 Stellaris Cygnus 4.5.1 (358e)。开始日期：2026-09-26。当前门槛结果和未测项目见[验收记录](shishan-code-origin-acceptance-report-2026-09-27.md)。

## 2026-09-27：白绮 V2 概念图与领袖界面修复

用户指出 A05 事件图中的白绮面部破裂。重新生成该不透明事件图，以 V2 设定图固定五官、眼镜与发饰，人物面部占有足够像素且不得出现裂缝；背景仍呈现庞大的失稳机器核心。新提示词、原始输出和导出的 DDS 入库，最终在简体中文事件窗口核对脸部清晰度及裁切。

2026-09-27 文案修订：起源简介中的“许多年前，他们消失了”改为“许多年前，创造者消失了”，与设计文档措辞一致。起源局势基础月进度由用户改为 `+5`；脚本、设计、需求记录和十种语言的数字说明同步更新，仍保留每次维护 `+1` 与月速下限 `0.2`。

用户提供 `____V2.zip` 作为新的白绮人物设定图，指出当前透明半身肖像的左右发饰明显不齐，同时提供领袖界面截图：头像区域出现头部方块与分离的躯干。目标是以 V2 图为唯一白绮身份参考，用 EvoLink 重新生成透明肖像，保存完整提示词、请求和返回图，接入 Mod，并在简体中文实机验证领袖列表、小头像和详情卡的完整显示。

排查证据：本 Mod 的 `gfx/portraits/portraits/shishan_code_vivhite.txt` 把一张完整半身图指定给 `synthqueen_portrait_entity` 的 `character_textures`。原版 `synthqueen_portrait_green.dds` 是头、躯干、手臂等分区纹理图集，而本 Mod 的 DDS 是完整单图。实体的网格按原版图集 UV 取样，造成截图中的错乱。修复方向是改为 Stellaris 4.x 支持的静态 `texturefile` 肖像定义，并保留透明 DDS；不再套用合成女王的动态图集实体。公开的 4.x 静态肖像模板可作为语法参照，最终仍须本机原版解析与实机检验。V2 图和成品都必须留在仓库；旧参考版只作为历史记录，不再被成品引用。

验收标准：V2 成品左右发饰均与新设定图一致、清晰且在同一视觉水平线上；背景 alpha 真透明，发梢没有明显灰紫色软边。领袖列表和详情卡均显示连续的头肩与躯干，没有方块、分离肢体、丢脸或大幅裁切；开局事件创建白绮与复活后的肖像相同。静态检查与 `open_kaishek` 检查通过，再用简体中文实机截图验证。

V2 图已从单图 ZIP 取出并核对。EvoLink `gpt-image-2.5-sunburst` 第一张输出存于 `assets/shishan-code-origin/generated/A10-attempt-03`，发饰对称性和五官基本符合目标；但 PNG 左下角 alpha 达 244，存在半透明背景残留。须再经 EvoLink Layerize 提取人物，检查四角 alpha 与发缘后方可接入 DDS。

2026-09-27 实机继续发现：静态 `texturefile` 已消除分层网格导致的头身错位，但直接用 1024×1024 透明 DDS 时，领袖列表和详情卡只显示白绮胸甲。目标版本原版 `gfx/portraits/portraits/00_portraits_main.txt` 将 2D `icon` 锚定 `center_down`，`scale=1.0`，角色框内部高度为 380；过高的纹理从底端对齐后，头部位于裁切区上方。改用宽 512、高 384 的透明 DDS，在构建时从 V2 原图取头部与上半身并缩放到画布内，底端对齐；实机须再次检查列表与详情卡的头肩完整性。该锚定与尺寸是 Stellaris 4.5.1 本机规则，不推断为 CK3 通用语法。

2026-09-27 复活路径实机缺陷：通过领袖死亡效果触发白绮备份提示后，首版脚本已移除白绮并开放首都「重启白绮」，支付后恰好扣除 500 能量币；但领袖名单仍只有 4 人，白绮没有复活。`error.log` 指向 `clone_leader` 的备份目标无效、`event_target:shishan_code_vivhite_backup@root` 未定义。原实现先在一个 `auto_delete` 派系国家克隆，再把领袖设回本国并放逐；备份引用未能留存。原版 4.5.1 的星界裂隙和传奇领袖事件显示可在当前国家直接 `clone_leader = { target = from effect = { save_event_target_as = ... exile_leader_as = ... } }`，后续对放逐的目标克隆。修复改为在死亡回调直接克隆并放逐备份，省去临时国家；必须重新隔离实机核对备份目标、资源扣除、等级经验与特质，以及重载后有效性。

第二次实机发现直接克隆仍无法在支付时取得备份。原版 `common/on_actions/00_on_actions.txt` 明确 `on_leader_death_notify` 与 `on_leader_death_no_notify` 在 `on_leader_death` **之前**执行；原版 `bio.765` 正是在前者中克隆即将死亡的 `from` 领袖。此前本 Mod 只挂在 `on_leader_death`，此时克隆源已失效。改为在上述两种死亡前回调制作和放逐备份，再显示可复活标记；支付选项增加备份目标存在性条件，避免引用无效时扣费。两条通知分支和重载仍须复测。这是 Stellaris 4.5.1 的 on_action 顺序规则，记录于本仓库，不外推到 CK3。

## 目标与范围

按[需求记录](shishan-code-origin-requirements.md)、[详细设计](shishan-code-origin-design.md)与[验收方案](shishan-code-origin-acceptance-plan.md)制作独立 Mod `shishan_code_origin`。交付起源、物种特质、五阶段局势、来源互斥的产出修正、重复科研项目、维护建筑与岗位、白绮事件与领袖、10 种官方语言文本及已归档美术的游戏内贴图。使用独立描述符、`VERSION` 和更新日志；不改现有「无限岗位」Mod，不发布 Steam。

2026-09-27 第二层奖励池审计：Stellaris 4.5.1 原版 19 个候选特质的 `allowed_archetypes` 全部仅含 `BIOLOGICAL LITHOID`。新增 `common/traits/shishan_code_compat.txt` 的 19 个脚本专用机械兼容映射，逐项复用原版数值修正和图标；`generate_rewards.py` 改为在第二层抽取映射键、检查原键/映射键及互斥项，并为全部官方语言生成对原版名称、描述的本地化引用。原版特质定义未被覆盖。`open_kaishek` 曾把本体图标误判为缺失资源，已在工具仓库修复、验证、提交并推送 `63997f2`；修复后本 Mod 静态包级检查 `PASS`（19/19 脚本解析、13 DDS、160 本地化键）。映射实际数值、第二层切换及局势后半程项目仍需简中实机验收。

## 实施顺序与验证点

1. 冻结 4.5.1 原版脚本语法、资源键、岗位模型、领袖模型和贴图接口。先做起源资格、特质预算、局势与项目动态成本的可行性验证；发现新事实当天回写本页。
2. 建立独立 Mod 树及可重复资产转换脚本；接入透明与非透明源图，记录输入、尺寸、输出与校验。
3. 实现经济、局势、建筑岗位、特殊项目、奖励与领袖剧情；所有可变数值持久化，项目结算幂等。无法达到合同的特性必须先给出等价实现并验证，不能静默弱化。
4. 完成简体中文及其余九种官方语言译文；非中文仅静态验收。
5. 按验收方案先运行 `C:\workspace\open_kaishek` 检查；若工具缺少必要 profile 能力，先在该工具仓库按其规则补齐、测试、提交并推送，再继续。本仓库静态合同、简体中文单 Mod 实机、日志和存档重载依次通过后，才标记 Mod 验收完成。

## 验收标准

- [ ] 两类机械帝国可选、有机帝国不可选；特质点、上限、起始局势和建筑符合合同。
- [ ] 五阶段边界、月速、岗位与非岗位持续收入隔离、武器/航速/维护费均通过实机及存档复核。
- [ ] 三种科研项目的动态成本、结算、奖励层级、重构及 10% 复发通过。
- [ ] 白绮获取、不可解雇、全国科研修正、死亡复活及等级经验特质保留通过。
- [ ] 12 项美术正确接入；简体中文 UI 无原始键；其他九种语言静态校验通过。
- [ ] `open_kaishek`、本仓库合同、单 Mod 实机与存档重载的证据写入验收报告。

## 初始环境调查

- 本机只有 `C:` 文件系统卷；规则中 `D:\workspace\open_kaishek` 与 CK3 路径在本机实际为 `C:\workspace\open_kaishek`、`C:\workspace\ck3_eternal_recurrence`。
- 游戏安装在 `C:\Program Files (x86)\Steam\steamapps\common\Stellaris`；`launcher-settings.json` 报告 `Cygnus v4.5.1 (358e)`、兼容范围 `4.5`。
- 本仓库原有 `VERSION` 属于现有 Mod，不能复用于新 Mod；新 Mod 须在自身目录设独立版本源。

## 调查与偏差日志

### 2026-09-26：原版脚本入口

- `common/situations/99_README_SITUATIONS.txt` 明确 `permanent = yes` 会阻止进度抵达终点后自动结束；五阶段可用固定 `end`，建议末端 `1000`。`events/infernals_crisis_events.txt` 中有 `set_situation_progress = 10`，可作为归零探针的语法参照；实际进度 `0` 需实机复核。
- `common/special_projects/documentation.txt` 的 `cost` 允许固定数字、`base`、`modifier` 和 `scaled_modifier`，但文档没有说明帝国变量能否直接用于科研成本。动态公式仍待探针。
- `common/game_rules/00_rules.txt` 的 `can_dismiss_leader` 控制领袖解雇并已有原版不可解雇领袖的先例。为了使白绮的按钮真正禁用，需要覆盖该原版规则并增加白绮身份条件；须在 4.5.1 实机验证覆盖顺序与对其他领袖的影响。单纯 `on_leader_fired` 事后重招不符合需求。
- `common/governments/civics/00_origins.txt` 确认起源 `modifier` 支持 `ROBOT_species_trait_picks_add`、`ROBOT_species_trait_points_add`；实际主体物种谱系及个体机械兼容仍待测试。
- `common/on_actions/00_on_actions.txt` 有 `on_leader_fired`；死亡入口与领袖对象保留方式待探针。以上均为 Stellaris 4.5.1 专有资料，不推定为 CK3 规则。

### 2026-09-26：首次隔离加载（开发探针，尚非验收）

- 用户目录 `C:\Users\Administrator\AppData\Local\xenoamess_stellaries_dev\shishan_runs\20260926T095429Z`，游戏 exe SHA-256 `6fe06709f265e726722dc23f617c5fc4e5557629e2d43fe312016aba547c83e4`；只启用本 Mod。切换 Alt+Enter 后看到简体中文主菜单；日志位于该目录 `logs/error.log`，截图位于本仓库 `_runtime/shishan_code/20260926T095429Z`。
- 初次解析记录三个项目的成本权重缺少 `desc`；需要补本地化说明，不能把无报错等同于成本公式数值通过。
- `trait_shishan_iteration_assembly` 的 `planet_pop_assembly_mult` 与 `trait_shishan_iteration_experience` 的 `species_leader_exp_gain` 放进 `triggered_species_modifier` 时，原版 4.5.1 报「Modifier has entry not allowed by category」。改为该类别允许且作用于目标机械物种的小幅正面修正：前者改为住房使用 `-1%`，后者改为研究岗位产出 `+1%`；随累计变量叠加。此两项原设计数值属于可替换的设计建议，正式验收必须重新检查实效。
- 两种维护员岗位的 `mod_job_*_add` 本地化与岗位修正图标缺失；下次加载前补齐。原版其他订阅物品路径缺失的日志与本 Mod 无关，不能计作本 Mod 错误。

### 2026-09-26：首局实机与奖励池可行性

- 使用原版机械智能预设编辑并选择本起源，种族特质界面显示强制「屎山代码」、额外特质栏可用，帝国创建可完成；2200 年开局出现「大厦将倾」局势，月速为 +1.0，第一阶段 +25% 资源生产修正在局势提示中可见。开局三段事件在 1 月 4—8 日依次触发，白绮可加入；控制台 `any_owned_leader = { has_leader_flag = shishan_code_vivhite }` 记录为真。截图在 `_runtime/shishan_code/20260926T095429Z`。这只是机械智能案例，个体机械和非机械排除仍待测试。
- Stellaris 4.5.1 控制台中对机械主体物种执行 `change_species_characteristics = { add_trait = trait_industrious }` 成功，随后 `has_trait = trait_industrious` 为真（隔离探针 `game.log` 的 `SHISHAN_NONMACHINE_ADDED`）。因此非机械原版正面特质可以进入机械物种，但仍须逐项筛掉只对有机繁殖、非机械维护或不适用帝国经济生效的特质。第二奖励层将限定为经审查的通用效果白名单。
- 第一奖励层补全为原版基础机械正面特质中对当前帝国生效、无剧情或飞升前提的白名单；涉及个体机械与格式塔差异的条目须用帝国类型门槛，互斥特质须检查。两层均耗尽后才进入可叠加的小幅随机增益。不能把 DLC 专属剧情、飞升专属或不生效的条目塞进奖励池来拖延第三层。
- `open_kaishek` 现有 Stellaris 4.5.1 profile 仅接受合成女王肖像文件，对本 Mod 的起源、局势、项目等路径将 fail-closed。依据仓库规则，正式 Mod 验收前须在工具仓库先扩展可验证切片并提交推送，再运行该工具。
2026-09-27 第三次死亡实测：提前回调已经能留下完整的 5 级备份，死亡后存档含 `saved_leaders` 条目，但 `save_event_target_as` 的局部作用域无法在后续首都决议触发的复活事件里读取。因此先改用 `save_global_event_target_as = shishan_code_vivhite_backup@root` 保存带国家后缀的目标，再复测完整付费复活及重载；任何无有效备份的路径都不允许扣费。
第四次隔离局 `20260927T230000Z` 已完成死亡、500 能量币与 200 合金付费复活、领袖重新入列，以及存档重载：白绮均保持 5 级传奇行政官与正常肖像，相关错误日志为空。`save_global_event_target_as` 解决了跨决议事件的备份引用；下一步要检查连续第二次死亡是否能覆盖旧备份，并完成其余验收矩阵。
第二次死亡与复活也能覆盖旧的全局备份引用；`leader_trait_adaptable` 保留，但原领袖存档 `experience=212`，复活体经验为零。4.5.1 的 `clone_leader` 不复制当前等级的经验。死亡前回调现把 `from.trigger:has_experience` 存入国家变量。直接以该数值调用 `add_experience` 的实机复测仍过量：旧经验 `252`，新经验 `317.52`，说明效果受到 `1.26` 倍经验获取修正。现改为对新领袖先授予 1 点基础经验，读取实际增长倍率，再计算剩余所需基础经验并补授，最后清理临时变量。验收需用非零经验值比较复活前后的存档数值，并重载复核；经验增长倍率为零的特殊组合仍需单独验证。
