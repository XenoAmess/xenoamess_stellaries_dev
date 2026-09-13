# Workshop 2976454692 图片素材审计与翻新规格

## 目标、范围与验收口径

- 目标：为 Steam Workshop 物品 `2976454692`（`Gray with animated portrait`，小灰立绘替换）建立可直接交给美术制作的素材清单。
- 范围：当前 Workshop 包体中的图片、脚本实际引用的外部图片、Workshop 页面发布图片，以及一比一替换时必须保持的导出合同。
- 不在本次范围：制作新图片、修改 Mod、发布 Workshop 物品或完成 Stellaris 实机验收。
- 核心验收口径：区分“Mod 自带并由游戏加载”“Mod 自带但只用于发布”“Workshop 页面额外媒体”“由原版游戏提供”四类，不能把原版依赖误报为 Mod 缺图。

## 调查基线与证据

调查日期为 2026-09-13。通过 Steam 官方公开元数据接口和 SteamCMD 匿名下载取得当前包体：

```text
consumer_app_id = 281990
publishedfileid = 2976454692
hcontent_file = 6443227808037005187
file_size = 2713400 bytes
time_created = 2023-05-16 04:09:38 UTC
time_updated = 2026-06-20 20:07:56 UTC
```

可复现下载命令：

```powershell
steamcmd.exe +login anonymous +workshop_download_item 281990 2976454692 validate +quit
```

包内 `descriptor.mod` 标记 `supported_version="v4.4.3"`。Workshop 页面说明该 Mod 用一张 AI 生成插画替换小灰肖像，并注明旧素材来源为 Pixiv 作品 `107157087`、作者 `earth aeolian`。来源：[目标 Workshop 页面](https://steamcommunity.com/sharedfiles/filedetails/?id=2976454692)、[Steam Workshop 实现文档](https://partner.steamgames.com/doc/features/workshop/implementation)。

## 数量结论

按不同交付边界，数量如下：

| 交付边界 | 数量 | 构成 |
| --- | ---: | --- |
| 只翻新游戏内画面 | 2 张 | 透明人物肖像、外交事件房间背景 |
| 形成可发布 Mod 包 | 3 张 | 上述 2 张 + `thumbnail.png` |
| 同时翻新现有 Workshop 页面 | 4 张 | 上述 3 张 + 1 张页面展示截图 |
| 连原版旗帜视觉也改为原创 | 额外 2 个逻辑设计 | 灰蛊徽记、旗帜背景；当前由原版提供，不是缺失文件 |

因此，当前需求按“一比一完整翻新并更新页面”估算，应向美术收取 **4 张成品**；其中真正进入游戏画面的新画为 **2 张**。

这里的“4 张”只回答“逐文件翻新当前 Workshop 包体”，不能解释为“小灰在原版流程中的全部视觉触点”。下文对 Stellaris `4.4.6` 原版代码的补充审计确认：该 Mod 漏掉了首次发现事件图，后续通讯背景、重生事件图、旗帜、特质图标、陆军图标和战舰模型也仍使用原版共用素材。完整角色视觉翻新的工作量明显大于 4 张。

## 当前素材的精确规格

### 游戏内必需素材

| 素材 | 当前路径 | 用途与引用 | 当前像素规格 | 文件合同 |
| --- | --- | --- | --- | --- |
| 小灰人物肖像 | `gfx/models/portraits/gray.dds` | `gray_altered.txt` 将 `gray_01` 指向此图；领袖头像和 `graygoo.401`—`graygoo.406` 外交事件复用 | `800 × 350` | 旧式 DDS 头；未压缩 32-bit BGRA / A8R8G8B8；直通 Alpha；1 个图面；无 mip 链；1,120,128 bytes |
| 外交事件房间背景 | `gfx/portraits/city_sets/areta_005_room.dds` | 上述六段小灰外交事件的 `room = areta_005_room` | `952 × 340` | 旧式 DDS 头；未压缩 32-bit BGRA / A8R8G8B8；含 Alpha 通道；1 个图面；无 mip 链；1,294,848 bytes |

DDS 规格不是按文件大小猜测：两个文件的 payload 都精确等于 `宽 × 高 × 4`，另加 128-byte DDS 头；像素掩码为 `R=00FF0000`、`G=0000FF00`、`B=000000FF`、`A=FF000000`，FourCC 为空。

人物图的构图与 Alpha 基线：

- 非零 Alpha 包围盒为 `x=130..687, y=18..349`，即有效内容约 `558 × 332`，下沿贴底。
- 193,510 个像素完全透明，80,934 个像素完全不透明，5,556 个像素为半透明抗锯齿边缘。
- 半透明边缘保存的是非预乘色值，应按 straight/unassociated alpha 导出，避免黑边或白边。
- 当前人物位于画布中央偏右，桌面向左延伸；脸和上半身同时要经受外交事件框、领袖卡和内阁界面的不同裁切。

背景图是约 `2.8:1` 的超宽构图。其 Alpha 通道没有全透明像素，321,100 个像素为完全不透明，2,580 个像素为部分透明；翻新时可以按“视觉上不透明的整幅背景”设计，但导出时保留 32-bit Alpha 合同最稳妥。

### 发布素材

| 素材 | 所在位置 | 当前像素规格 | 当前格式 | 是否影响游戏画面 |
| --- | --- | --- | --- | --- |
| Mod 缩略图 / 主预览图 | 包根目录 `thumbnail.png`，由 `descriptor.mod` 的 `picture` 引用 | `351 × 313` | PNG，RGBA8，但所有像素均不透明；203,166 bytes | 否；用于启动器/发布展示 |
| Workshop 额外截图 | 只存在于 Workshop 页面，未收入包体 | `547 × 347` | PNG，RGBA8，所有像素均不透明；352,878 bytes | 否；用于页面展示 |

Workshop 当前主预览图与包内 `thumbnail.png` 的字节数和 SHA-256 完全一致；页面只有 1 张 additional preview。因此这不是两份不同的美术需求，而是同一缩略图被同时用于包内和页面主预览。

Steam 官方文档确认主预览与 additional preview 是独立的 Workshop 发布媒体，但没有在该通用文档中给出 Stellaris 专属的固定像素尺寸。因此上表中的尺寸是目标物品当前实测值，不应误写成 Steam 的硬性上限。

## “animated portrait” 的实际含义

当前包体没有任何逐帧图集、`noOfFrames`、动画配置、骨骼、mesh、视频、法线图或发光图。`gray_01` 只有一条静态 `texturefile` 引用。也就是说：

- 一比一翻新只需要一张透明静态人物图，不需要绘制动画帧。
- 若新需求确实包含眨眼、呼吸、发丝或 Live2D 式运动，这是新增功能，不能按现有素材替换估价；需要另立动画技术方案和验收标准。

## 原版提供、当前 Mod 未重画的图片引用

当前 Mod 的 `events/gray_goo_events.txt` 在创建灰蛊国家和小灰国家时引用：

- `icon / special / gray_goo.dds`：原版灰蛊旗帜徽记；
- `background / backgrounds / sinus.dds`：原版旗帜背景。

两者均不在下载包体内，由 Stellaris 原版资源解析。法令图标 `GFX_edict_type_time`、房间选择器列出的其他房间，以及事件 UI 边框也来自原版。因此它们不属于“逐文件翻新现有包”的必交素材，但旗帜属于“完整重塑小灰角色视觉”时应评估的触点。

如果目标改为“玩家能看到的相关视觉全部原创”，则应额外设计灰蛊徽记和旗帜背景，并改用 Mod 自己的唯一文件名/类别，避免覆盖全局原版素材。Stellaris 4.4.6 原版小灰使用的徽记实测包含默认 `256 × 256`、银河地图 `256 × 256` 和小图 `24 × 24` 三个文件变体，旗帜背景为 `400 × 400`；不能按旧 Wiki 的历史规格直接下单。

## Stellaris 4.4.6 原版“小灰”视觉链审计

本节以本机 Steam 原版 `Pegasus v4.4.6` 为基线，逐一追踪 `disco_gray_cat`、`graygoo.400`—`graygoo.512`、`create_gray_*`、`gray_army` 和 `NAME_Gray_Warship`。结论是：原版没有专用的“小灰人形立绘”；小灰以玩家物种外貌出现。Workshop Mod 新增的 `gray_01` 是自定义肖像 ID，并非原版素材。原版文本资源中不存在独立的精确 `gray_01` ID。

### 首次发现事件图：确认漏改

- `common/anomalies/95_anomaly_categories_distant_stars.txt:1712` 的 `disco_gray_cat` 异常类别使用 `picture = "GFX_evt_ship_in_orbit_2"`，成功后调用 `graygoo.400`。
- `events/gray_goo_events.txt:2136` 的 `graygoo.400` 注释为 `Encountered Gray`，也使用同一个 `GFX_evt_ship_in_orbit_2`。简体中文标题实际是“安静散步”，并不字面叫“第一次接触”；它在功能上就是发现小灰、接入视频前的首次接触页。
- `interface/eventpictures.gfx:2248` 将该 sprite 映射到 `gfx/event_pictures/ship_in_orbit_2.dds`，同时使用 `gfx/interface/situation_log/event_mask.dds` 作为显示蒙版。
- 原图是飞船掠过星球、右侧强光的横幅，不直接画出小灰。实测规格为 `450 × 150`、旧式未压缩 `A8R8G8B8` DDS、全部 Alpha 为 255、无 mip 链、`270,128` bytes。
- 当前 Mod 的 `graygoo.400` 仍引用这个原版 sprite；它从 `graygoo.401` 才将 `portrait` 和 `room` 改为 `gray_01` / `areta_005_room`，并且没有覆盖 `disco_gray_cat`。所以这是一个确定的遗漏点，同一张新图需要接到“异常卡片”和“异常完成事件”两个脚本位置。

为避免连带修改其他使用 `GFX_evt_ship_in_orbit_2` 的原版事件，实现时应新增专用 sprite（例如 `GFX_evt_gray_first_encounter`）及专用 DDS，再将上述两个小灰入口指向它；不要原地覆盖原版共用文件。美术最终交付可按 `450 × 150`、3:1、无 mip 制作，建议母版至少 `1800 × 600`。

### 小灰专属事件链的全部画面引用

| 环节 | 原版画面引用 | 当前 Mod 状态 | 完整翻新判断 |
| --- | --- | --- | --- |
| `disco_gray_cat`、`graygoo.400` 首次发现 | `GFX_evt_ship_in_orbit_2` | 未改 | **确认漏改**；一张新事件横幅，两个代码接点 |
| `graygoo.401`—`406` 初次对话 | `portrait = root.species`、`room = root` | 已改成 `gray_01`、`areta_005_room` | 已覆盖；六页复用同一立绘和房间 |
| `graygoo.499` 创建小灰国家和首领 | 首领 `species = root`；旗帜 `gray_goo.dds` + `sinus.dds` | 给首领补了 `change_leader_portrait = gray_01`，旗帜未改 | 人物肖像已间接覆盖；旗帜仍是遗漏/可选扩展 |
| `graygoo.500` 初始菜单 | `GFX_evt_mysterious_signal`；`portrait = from.ruler`；`room = root` | 肖像由 499 的持久改头像间接覆盖；事件图和房间未改 | **房间接点漏改**；是否另画事件图取决于 UI 实机显示与风格范围 |
| `graygoo.501` 行政官形态菜单 | `GFX_evt_busy_spaceport`；`portrait = gray_official`；`room = root` | 重建领袖时会再次改成 `gray_01`；事件图和房间未改 | **房间接点漏改**；事件图为可选 |
| `graygoo.502` 战舰形态菜单 | `GFX_evt_fleet_neutral`；小灰 ruler 肖像；`room = root` | 肖像间接覆盖；事件图和房间未改 | **房间接点漏改**；事件图为可选 |
| `graygoo.503` 陆军形态菜单 | 同 `GFX_evt_fleet_neutral`；小灰 ruler 肖像；`room = root` | 肖像间接覆盖；事件图和房间未改 | **房间接点漏改**；事件图为可选 |
| `graygoo.504` 重组中 | `room = no_video_feed_room`，没有人物 portrait | 未改 | 原版有意断开视频，不应默认判作漏洞；只有要做专属“离线/重构”画面时才扩展 |
| `graygoo.511` “小灰已被击溃” | `GFX_evt_circuitry_modification` | 未改 | 完整叙事翻新时建议新增专属受损/重构事件图 |
| `graygoo.512` “小灰归来” | `leader_story` 窗口；`GFX_evt_gray_gooed_planet`；小灰 ruler 肖像；`room = root` | 肖像间接覆盖；事件图和房间未改 | **房间接点漏改**；回归事件图建议专属化 |

上述 `picture` 字段与外交窗口的 `picture_event_data` 同时存在时，具体哪一层在当前 UI 布局中可见，需要简体中文实机逐事件确认；但它们都是原版代码中真实存在、而当前 Mod 未替换的美术引用，不能从静态清单里删除。后续 `graygoo.500`—`503`、`512` 的 `room = root` 可以直接复用现有 `areta_005_room`，所以这里主要缺的是脚本接线，不一定要再画五张房间图。

这些事件横幅的原版实测合同如下；全部为 `450 × 150`、无缩小 mip，sprite 均在 `interface/eventpictures.gfx` 中另挂事件蒙版：

| 原版文件 | 被小灰流程引用的位置 | DDS 像素格式 |
| --- | --- | --- |
| `ship_in_orbit_2.dds` | 异常类别、`graygoo.400` | 未压缩 32-bit `A8R8G8B8` |
| `mysterious_signal.dds` | `graygoo.500` | 未压缩 24-bit `B8G8R8` |
| `busy_spaceport.dds` | `graygoo.501` | 未压缩 32-bit `A8R8G8B8` |
| `fleet_neutral.dds` | `graygoo.502`、`503` | 未压缩 24-bit `B8G8R8` |
| `circuitry_modification.dds` | `graygoo.511` | 未压缩 24-bit `B8G8R8` |
| `gray_gooed_planet.dds` | `graygoo.512` | 未压缩 32-bit `A8R8G8B8` |

### 事件窗口之外的遗漏点

| 触点 | 原版解析链与实测规格 | 当前 Mod 状态 | 翻新建议 |
| --- | --- | --- | --- |
| 小灰国家旗帜 | `flags/special/gray_goo.dds`：`256 × 256` A8R8G8B8；`flags/special/map/gray_goo.dds`：`256 × 256` A8R8G8B8；`flags/special/small/gray_goo.dds`：`24 × 24` A8R8G8B8；背景 `flags/backgrounds/sinus.dds`：`400 × 400` 24-bit B8G8R8；均无 mip | 未改 | 若要求外交列表/旗帜也统一，交付 1 套徽记的 3 个文件变体及 1 张背景；使用专用文件名，不能覆盖共用原图 |
| 小灰行政官专属特质图标 | `leader_trait_governor_gray` 实际复用 `GFX_leader_trait_psionic_chosen_one` → `psionic_chosen_one.dds`，`29 × 29` A8R8G8B8，共 5 级 mip | 未改 | 交付一枚专属 `29 × 29` 图标并定义新的 sprite；其他职业/等级特质是通用 UI，不算小灰身份素材 |
| 小灰陆军图标 | `gray_army` 复用 `GFX_army_type_machine_assault`，即 `army_icon.dds` 第 11 帧；原图集 `578 × 34`、17 个横排 `34 × 34` 帧、A8R8G8B8，只有基底级 | 未改 | 美术交付有效画面为 `34 × 34`；实现为专用单帧 army sprite，不能直接覆盖整张通用陆军图集 |
| 小灰战舰三维外观 | `NAME_Gray_Warship` → `gray_warship_key` → `gatebuilder_01_mothership_section_entity` → `gatebuilder_01_mothership.mesh` | 未改 | 这不是一张 2D 图；完整翻新要有专用 mesh/entity/material，或明确保留原版纳米舰 |
| 战舰纹理 | mothership mesh 只直接引用 diffuse、normal、specular 三张纹理；均为 `2048 × 2048`、12 级 mip：diffuse 为 DXT1，normal/specular 为 DXT5 | 未改 | 若重做舰船，至少交付 1 个 mesh + 3 张贴图；原文件为灰蛊/门建者共用，不能原地覆盖 |
| 小灰陆军运输舰 | `create_army_transport` 中专用 `graphical_culture` 行被注释，因此使用所属国/默认运输舰视觉 | 未改 | 完整“三种形态”翻新时另做专用运输舰接线；只做人物 2D 包时可明确排除 |

原版 mothership mesh 实测为 `726,195` bytes；三张贴图依次为 `2,796,344`、`5,592,560`、`5,592,560` bytes。战舰模型同时服务其他灰蛊内容，因此直接覆盖 `gatebuilder_01_mothership_*` 会污染非小灰单位。

### 不应误算成小灰人物素材的灰蛊/L 星团画面

`GFX_evt_gray_goo`、`GFX_evt_gray_goo_ships`、灰蛊星球模型和 `pc_gray_goo` 天空等资源属于更宽泛的灰蛊危机/L 星团题材，不是“小灰这个人物”的专属素材。`graygoo.550`“进入空荡星团”使用 `ruined_system.dds`（`450 × 150`、A8R8G8B8、无 mip），它与小灰结局背景有关但还没有出现小灰，可放在主题扩展包而非角色基础包。`graygoo.555` 的 `gray_gooed_planet.dds` 则由 `gray_goo` 危机国家触发，不属于小灰同伴链。

据此划分交付范围：

1. **最低修漏版**：现有 4 张发布/包体素材之外，新增 1 张 `450 × 150` 首次发现事件图；并把已有房间接到 `graygoo.500`—`503`、`512`。游戏内原创成品由 2 张增至 **3 张**。
2. **完整 2D 角色版**：在最低修漏版上，建议再做 1 张击溃/重构图、1 张归来图、1 枚 `29 × 29` 特质图标、1 枚 `34 × 34` 陆军图标、1 套旗帜徽记三变体及 1 张旗帜背景。后续菜单的三张通用 `picture` 是否单独绘制，应以实机确认其显示层级后决定。
3. **完整三形态版**：再加入战舰专用 mesh + diffuse/normal/specular，以及专用运输舰视觉；这已经是 3D 舰船 Mod 工作，不应按“补几张图片”估价。

## 建议的新美术交付规格

保留高分辨率、分层母版，再由构建流程生成游戏文件。推荐交付：

1. 人物母版：至少 `3200 × 1400`，透明背景，人物/前景道具/光效分层；最终等比缩小到精确 `800 × 350` 的 straight-alpha DDS。
2. 背景母版：至少 `3808 × 1360`，主要视觉焦点避免贴左右边；最终导出精确 `952 × 340` DDS。
3. 缩略图母版：建议方形 `1024 × 1024`，标题和脸部留在中央安全区；当前 `351 × 313` 可以直接一比一替换，但页面会以方形卡片展示并可能 letterbox。最终仍命名 `thumbnail.png`。
4. Workshop 展示图：建议另做 `1920 × 1080` 的实机截图或合成展示图；`547 × 347` 只是旧页面现状，不是建议继续沿用的制作分辨率。

母版尺寸是制作建议，不是引擎硬约束；两张 DDS 的最终画布、路径、Alpha 和像素格式才是一比一替换合同。

## 替换与验收标准

### 静态检查

- 三个包内图片文件存在，路径和大小写与脚本/`descriptor.mod` 一致。
- `gray.dds` 为 `800 × 350`、32-bit、含有效透明区域、无 mip；透明边缘没有明显黑/白色污染。
- `areta_005_room.dds` 为 `952 × 340`、32-bit、无全透明破洞、无 mip。
- `thumbnail.png` 可被解码，缩略状态下主体和标题仍可读。
- 包内不因“animated”字样误增无引用的帧图或视频文件。

### 简体中文实机检查

依照仓库语言范围，只使用 `l_simp_chinese` 启动 Stellaris：

- 检查 `disco_gray_cat` 异常卡片和 `graygoo.400`“安静散步”是否都显示专属首次发现图，且没有污染其他使用原版 `GFX_evt_ship_in_orbit_2` 的事件。
- 检查 `graygoo.401`—`graygoo.406` 初次通讯和 `graygoo.500`—`504` 形态菜单的人物/背景合成；`graygoo.504` 应保持预期的无视频信号状态。
- 检查 `graygoo.511`“小灰已被击溃”和 `graygoo.512`“小灰归来”的事件图、肖像与房间层级。
- 检查领袖列表、领袖详情、内阁席位与常见通知中的头像裁切。
- 若纳入完整 2D 角色版，检查小灰国家旗帜的默认/地图/小图缩放、行政官特质图标和小灰陆军图标。
- 在 100% UI 缩放和项目既定回归分辨率下确认头顶不截断、脸部不被 UI 遮挡、桌面/下沿不悬空。
- 检查透明边缘、发丝和高亮处无黑边、白边、色带或异常闪烁。
- 重新进入存档后确认 `gray_01` 仍解析到新图。

本调查只完成静态资产审计，尚未制作或装载新素材，因此不得表述为“Mod 实机验收通过”。

## 非美术风险

- 当前 Mod 为了替换小灰画面，复制了较大的原版 `gray_goo_events.txt`、`gray_goo_effects.txt` 和房间选择器；这会扩大版本漂移和 Mod 冲突面。单纯换画时复用现有文件名即可，不需要再次扩大脚本覆盖范围。
- `descriptor.mod` 的 `version="3.8.2"` 与 `supported_version="v4.4.3"` 表达的是两类版本，但旧版本字段容易让外部人员误判基线；正式翻新应遵守本仓库的独立 SemVer 规则。
- 旧图的署名不等于可再分发授权。新图应保留创作过程、授权范围和可发布证明，避免继续依赖原 Pixiv 作品的许可状态。

## 当前文件指纹

用于确认后续比较的基线：

| 文件 | SHA-256 |
| --- | --- |
| `gfx/models/portraits/gray.dds` | `837A4A6B8BA4D2C83CB0AE922E6EE8E8A5593A039533CBC807830F73205DC2FC` |
| `gfx/portraits/city_sets/areta_005_room.dds` | `4C10E3C418410942FBD9EF82959AA6BB882ED87116401622B0AD8E8694DDEAF2` |
| `thumbnail.png` | `8262DFC590502E17CF81864EFD795D52010E0027471552DAD39D2F25B4288D0A` |
