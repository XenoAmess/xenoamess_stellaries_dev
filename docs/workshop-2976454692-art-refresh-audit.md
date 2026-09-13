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

## 原版提供、无需重画的图片引用

当前 Mod 的 `events/gray_goo_events.txt` 在创建灰蛊国家和小灰国家时引用：

- `icon / special / gray_goo.dds`：原版灰蛊旗帜徽记；
- `background / backgrounds / sinus.dds`：原版旗帜背景。

两者均不在下载包体内，由 Stellaris 原版资源解析。法令图标 `GFX_edict_type_time`、房间选择器列出的其他房间，以及事件 UI 边框也来自原版。因此它们不属于一比一美术替换的必交素材。

如果目标改为“玩家能看到的相关视觉全部原创”，则应额外设计灰蛊徽记和旗帜背景，并改用 Mod 自己的唯一文件名/类别，避免覆盖全局原版素材。旗帜徽记通常还要考虑默认、银河地图和小图三个尺寸变体；社区资料给出的传统规格是 `128 × 128`、`256 × 256`、`24 × 24`，但实施前必须再以目标 Stellaris 版本的原版文件复核，不能把旧 Wiki 当成 4.4 的唯一依据。

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

- 检查小灰初次通讯及 `graygoo.401`—`graygoo.406` 的人物/背景合成。
- 检查领袖列表、领袖详情、内阁席位与常见通知中的头像裁切。
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
