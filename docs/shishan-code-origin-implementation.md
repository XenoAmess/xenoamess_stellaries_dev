# 「屎山代码」独立 Mod 实施记录

状态：实施中。目标游戏：本机 Stellaris Cygnus 4.5.1 (358e)。开始日期：2026-09-26。

## 2026-09-27：白绮 V2 概念图与领袖界面修复

用户提供 `____V2.zip` 作为新的白绮人物设定图，指出当前透明半身肖像的左右发饰明显不齐，同时提供领袖界面截图：头像区域出现头部方块与分离的躯干。目标是以 V2 图为唯一白绮身份参考，用 EvoLink 重新生成透明肖像，保存完整提示词、请求和返回图，接入 Mod，并在简体中文实机验证领袖列表、小头像和详情卡的完整显示。

排查证据：本 Mod 的 `gfx/portraits/portraits/shishan_code_vivhite.txt` 把一张完整半身图指定给 `synthqueen_portrait_entity` 的 `character_textures`。原版 `synthqueen_portrait_green.dds` 是头、躯干、手臂等分区纹理图集，而本 Mod 的 DDS 是完整单图。实体的网格按原版图集 UV 取样，造成截图中的错乱。修复方向是改为 Stellaris 4.x 支持的静态 `texturefile` 肖像定义，并保留透明 DDS；不再套用合成女王的动态图集实体。公开的 4.x 静态肖像模板可作为语法参照，最终仍须本机原版解析与实机检验。V2 图和成品都必须留在仓库；旧参考版只作为历史记录，不再被成品引用。

验收标准：V2 成品左右发饰均与新设定图一致、清晰且在同一视觉水平线上；背景 alpha 真透明，发梢没有明显灰紫色软边。领袖列表和详情卡均显示连续的头肩与躯干，没有方块、分离肢体、丢脸或大幅裁切；开局事件创建白绮与复活后的肖像相同。静态检查与 `open_kaishek` 检查通过，再用简体中文实机截图验证。

V2 图已从单图 ZIP 取出并核对。EvoLink `gpt-image-2.5-sunburst` 第一张输出存于 `assets/shishan-code-origin/generated/A10-attempt-03`，发饰对称性和五官基本符合目标；但 PNG 左下角 alpha 达 244，存在半透明背景残留。须再经 EvoLink Layerize 提取人物，检查四角 alpha 与发缘后方可接入 DDS。

## 目标与范围

按[需求记录](shishan-code-origin-requirements.md)、[详细设计](shishan-code-origin-design.md)与[验收方案](shishan-code-origin-acceptance-plan.md)制作独立 Mod `shishan_code_origin`。交付起源、物种特质、五阶段局势、来源互斥的产出修正、重复科研项目、维护建筑与岗位、白绮事件与领袖、10 种官方语言文本及已归档美术的游戏内贴图。使用独立描述符、`VERSION` 和更新日志；不改现有「无限岗位」Mod，不发布 Steam。

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
