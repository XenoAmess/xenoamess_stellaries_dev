# 合成女王（Cetana）图片资源调查

## 调查目标与证据边界

确定制作“替换合成女王立绘及相关图片”的独立 Mod 时，需要绘制、打包及验收的原版图片。调查日期为 2026-09-25。以本机 Steam 版 Stellaris `Pegasus v4.4.6 (fdde)` 的安装文件为准；未改动原版。Paradox 的 [《机械纪元》发布说明](https://store.steampowered.com/news/posts/?appids=281990&enddate=1714740824&feed=steam_community_announcements)把 Cetana 明确列为该 DLC 的终局危机。

调查方法：按 `synthqueen`、`synth_queen`、`cetana` 搜索图片文件名，再回查 `gfx/portraits/portraits/21_portraits_cybernetics_synthqueen.txt`、`interface/eventpictures.gfx`、`interface/leaders.gfx`、`events/machine_age_crisis_events.txt`、`common/scripted_effects/02_machine_age_effects.txt` 等引用。尺寸由 Pillow 读取 DDS，压缩类型由 DDS 头检查。下面的路径均相对于 Stellaris 游戏根目录；“必须”指本项目计划完整替换人物和主要剧情视觉时的素材合同，不代表游戏要求所有图片同时替换。

## 第一阶段：人物与剧情视觉，共 16 个文件

### 人物肖像：10 张，均为 1024×1024 DDS

原版 `21_portraits_cybernetics_synthqueen.txt` 将下列肖像全部绑定同一个 `synthqueen_portrait_entity`；实体经 `gfx/models/portraits/synthqueen/` 下的 mesh 与 idle 动画显示。原图均为 DXT5 DDS。替换时保留原尺寸和透明区域，逐个复核脸部位置、近景/中景裁切及动画变形。

| 逻辑用途 | 原版图片路径后缀（共同前缀 `gfx/models/portraits/synthqueen/`） | 原版肖像键 |
| --- | --- | --- |
| 女王本体/物种基础肖像 | `synthqueen_portrait_green.dds` | `synth_queen` |
| 哺乳类及人形文明所见形象 | `synthqueen_portrait_mammalian.dds` | `cetana_mammalian` |
| 爬行类形象 | `synthqueen_portrait_reptilian.dds` | `cetana_reptilian` |
| 鸟类形象 | `synthqueen_portrait_avian.dds` | `cetana_avian` |
| 节肢/软体/毒物类所见形象 | `synthqueen_portrait_molluscoid.dds` | `cetana_molluscoid` |
| 真菌/植物类所见形象 | `synthqueen_portrait_plantoid.dds` | `cetana_plantoid` |
| 石质形象 | `synthqueen_portrait_lithoid.dds` | `cetana_lithoid` |
| 水生形象 | `synthqueen_portrait_aquatic.dds` | `cetana_aquatic` |
| 机械/机器形象 | `synthqueen_portrait_robot.dds` | `cetana_robot` |
| 空白/后期状态形象 | `synthqueen_portrait_empty.dds` | `cetana_empty` |

`get_cetana_face` 位于原版 `common/scripted_effects/02_machine_age_effects.txt`，按玩家物种类别选择上述八种对话形象。`synth_queen` 是危机势力基础物种的肖像；`cetana_empty` 还在 `events/machine_age_crisis_events.txt` 的后期领袖切换中直接引用。因此仅替换一张肖像会留下大量原版人物画面。

### 事件插画与对话背景：3 张

| 用途 | 原版路径 | 尺寸 | 引用证据 |
| --- | --- | --- | --- |
| 合成女王危机常规事件图 | `gfx/event_pictures/synth_queen.dds` | 450×150 | `interface/eventpictures.gfx` 的 `GFX_evt_synth_queen` / `_nomask`；危机事件、情况、特殊项目、事件链和观察者事件引用 |
| 启蒙/结局分支事件图 | `gfx/event_pictures/synth_queen_enlightenment.dds` | 450×150 | 同文件的 `GFX_evt_synth_queen_enlightenment`、无蒙版及两个 zoom sprite；`crisis.10020`、`crisis.21000` 等及 `timeline.72` 引用 |
| 合成女王对话窗口背景 | `gfx/interface/leaders/recruitment_bgs/crisis_conversation_bg_synth_queen.dds` | 828×358 | `interface/leaders.gfx` 的 `GFX_crisis_conversation_bg_synth_queen`；`crisis.8040` 起多段对话 `picture` 引用 |

两张事件图各有多个 sprite，但每组只指向同一张 DDS，无须按 sprite 数量重复绘制。`synth_queen_enlightenment.dds` 的 zoom sprite 使用固定裁切坐标 `0,0–450,150` 和 `169,22–279,88`；新画面必须按这两种视口检查。对话事件另外使用 `picture_event_data` 绑定 Cetana 领袖肖像和目标国家的 room；本次确认的专用背景是上表 828×358 文件。`synth_queen_room` 仅在原版 room selector 中出现为 `always = no`，本机未找到同名 DDS，暂不把它列为待绘素材；实机若发现独立房间图，再补证据并修订清单。

### 危机旗帜：3 张

危机脚本多处以 `category = "special"`、`file = "synth_queen.dds"` 设置势力旗帜。原版同时提供以下三种文件，全部替换可避免星图或小图标仍显示旧徽记。

| 路径 | 尺寸 |
| --- | --- |
| `flags/special/synth_queen.dds` | 256×256 |
| `flags/special/map/synth_queen.dds` | 256×256 |
| `flags/special/small/synth_queen.dds` | 24×24 |

## 第二阶段候选：专属图标，共 5 个文件

这些图直接代表合成女王危机或其故事奖励，建议在确定统一美术风格后评估是否一并重绘；若原图没有人物形象，也可保留原版。不得为了“文件名含 Cetana”而默认改动玩法数据。

| 原版图片 | 尺寸 | 界面位置 |
| --- | --- | --- |
| `gfx/interface/icons/situation_log/situation_log_synth_queen.dds` | 39×39 | 事件链、特殊项目 |
| `gfx/interface/icons/galactic_focus/galactic_focus_defeat_synth_queen.dds` | 45×45 | 星海共同体危机焦点 |
| `gfx/interface/icons/specimens/cetana_love.dds` | 100×100 | Cetana 标本 |
| `gfx/interface/icons/relics/r_cetanas_heart.dds` | 150×150 | Cetana 之心遗珍 |
| `gfx/interface/icons/relics/r_cetanas_heart_shine.dds` | 150×150 | 同遗珍的发光蒙版，必须与底图配套 |

## 其余同名图片：已发现，但不纳入人物插画首版

| 组别 | 文件/数量 | 判断 |
| --- | --- | --- |
| 科技与组件图标 | `tech_synth_queen_knowledge.dds`、`tech_nanite_repair_system_synth_queen.dds`、`ship_part_nanite_repair_system_synth_queen.dds`，共 3 张 | 功能图标；需要统一全套 UI 风格时再选 |
| 对话/界面装饰 | `button_75_24_animated_synth_queen.dds`、`button_sound_synth_queen.dds`、`button_mute_synth_queen.dds`、`outliner_tile_synth_queen.dds`、`line_medium_synth_queen.dds`、`planetview_topright_bg_small_synth_queen.dds`、`situation_progressbar_empty_synth_queen.dds`、`situation_progressbar_monodirectional_synth_queen.dds`，共 8 张 | 界面皮肤和进度条；动帧/九宫格等结构须单独研究，不能按普通插画替换 |
| 银河地图纹理 | `gfx/map/synth_queen/synth_queen_galaxy_map.dds`、`synth_queen_galaxy_map_alpha.dds`，共 2 张 | 危机星图覆盖层；与立绘无直接关系 |
| 星系特效贴图 | `gfx/models/effects/synth_queen/` 下 `synth_queen_system_effect_diffuse.dds`、`synth_queen_system_effect_flowmap.dds`、`synth_queen_system_orb_effect_diffuse.dds`，共 3 张 | 3D/粒子特效配图，不是事件插画 |
| 舰船与空间站材质 | `gfx/models/ships/synth_queen_01/` 下 8 组 diffuse/normal/specular，共 24 张 | 3D 材质；不属于立绘替换 |

工作坊缩略图是新 Mod 的发布素材，原版中不存在对应“合成女王 Mod 缩略图”；如以后发布，需另作一张并单独验收。其他没有专属文件名的通用危机插画不因出现在相关事件中就纳入替换范围，以免影响其他内容。

## 尚待实机确认的风险

1. 以上是 4.4.6 的静态引用清单，还没有实际进入危机验证画面显示、文件覆盖优先级或 DLC 可用状态。
2. 人物 10 个变体共用 mesh、动画及视口偏移；直接替换贴图是否保留预期构图，应以游戏中简体中文对话和领袖界面确认。
3. 原版 `synth_queen_room` 没有找到同名实体图片；若运行时出现独立房间画面，需要先追溯实际文件路径。
4. Stellaris 更新可能更改图片路径、裁切或事件引用；实施前和发布前均须与已安装版本重跑清单对照。
