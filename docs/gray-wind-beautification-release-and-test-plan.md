# 灰风美化独立 Mod：实现、验收与发布方案

## 1. 目标与发布身份

- 新建一个可单独启用、单独版本化、单独发布的 Stellaris Mod，不把任何灰风内容并入现有的“无限岗位（XenoAmess 维护版）”。
- 游戏与 Steam 展示名称固定为 `[XenoAmess的灰风美化]`。
- 本地 Mod ID 固定为 `xenoamess_gray_wind_beautification`。
- 首个正式版本为 `1.0.0`；唯一版本源为 `gray_wind_beautification/VERSION`，其值必须与该 Mod 的 `descriptor.mod` 完全一致。
- `supported_version` 表达为 `4.4.*`；实现与实机验收基线为 Steam 版 Stellaris `Pegasus v4.4.6 (fdde)`。
- 新 Mod 必须创建新的 Steam Workshop 物品。上游物品 `2976454692` 和现有“无限岗位”物品 `3797257579` 都是只读对象，禁止作为上传目标。
- 发布前描述文件不得含 `remote_file_id`；新建物品成功后，才把 Steam 返回的新 ID 写回本 Mod。

仓库是多个可发布物的综合管理仓库，因此灰风 Mod 的“Mod 根目录”是 `gray_wind_beautification/`。Git 标签使用带产品前缀的 `gray-wind-v1.0.0`，避免与仓库中现有的 `v1.0.0` 冲突。

## 2. 目录与隔离边界

```text
gray_wind_beautification/
├── VERSION
├── CHANGELOG.md
├── mod/                         # 可直接安装/上传的 content folder
│   ├── descriptor.mod
│   ├── thumbnail.png
│   ├── common/
│   ├── events/
│   ├── gfx/
│   ├── interface/
│   └── localisation/
├── workshop/                    # Workshop 描述和同版本 Change Note
└── evidence/                    # 静态、实机与远端回读证据；不进入 content folder
```

不得修改：

- `vivhite_infinite_positions/` 的内容、版本和 Steam ID；
- Steam Workshop 上游物品 `2976454692`；
- Steam Workshop 已发布物品 `3797257579`；
- Stellaris 安装目录下的原版文件。

## 3. 上游调查结论与实现策略

SteamCMD 只读下载的上游 `2976454692` 同时覆盖了完整的旧版 `gray_goo_events.txt` 和 `gray_goo_effects.txt`。与当前 4.4.6 原版比较后，确认其中混有与美术无关的旧语法、领袖体系和舰队/危机数值差异，不能直接作为新 Mod 的代码基线。

实现采用以下原则：

1. 从本机已校验版本的 Stellaris 4.4.6 原版文件建立固定基线副本。
2. 只对灰风形象相关引用做最小补丁；保留当前原版的其余事件、触发器、数值与效果。
3. 使用 `xenoamess_gray_wind_` 前缀声明新增肖像、事件图、事件 namespace、本地化键和修复逻辑，避免污染全局命名空间。
4. 不覆盖共享的 `GFX_evt_ship_in_orbit_2`，而是为“第一次接触”建立灰风专用 sprite；因此其他原版事件仍使用原图。
5. 不带入上游的第三方房间背景 `areta_005_room.dds`。外交事件继续使用当前原版房间，只更换人物肖像。
6. 新旧存档中的既有灰风领袖通过一次性/低频兼容事件校正肖像；新建灰风领袖在创建时直接赋予新肖像。

需要覆盖当前原版整文件时，必须在测试中比较基线哈希与语义差异，证明差异仅限下列目标点：

| 目标点 | 当前原版 | 新 Mod |
| --- | --- | --- |
| `disco_gray_cat` 异常现象 | 共享 `GFX_evt_ship_in_orbit_2` | 专用“第一次接触”事件图 |
| `graygoo.400` 第一次接触 | 共享 `GFX_evt_ship_in_orbit_2` | 同一张专用“第一次接触”事件图 |
| `graygoo.401`—`406` 对话 | 玩家物种肖像 | 灰风专用透明肖像 |
| `graygoo.499` 创建灰风统治者 | 原版物种派生肖像 | 创建后立即切换灰风专用肖像 |
| `create_gray_official` | 原版物种派生肖像 | 创建后立即切换灰风专用肖像 |
| `graygoo.511` 战败 | 通用电路图 | 专用灰风战败图 |
| `graygoo.512` 回归 | 通用纳米星球图 + 领袖肖像 | 专用灰风回归图 + 灰风肖像 |
| Workshop 缩略图 | 上游旧图 | 新缩略图 |

## 4. 美术资源合同

| 逻辑资源 | 输出路径 | 像素与格式 | 透明度 |
| --- | --- | --- | --- |
| 灰风外交/领袖肖像 | `gfx/models/portraits/xenoamess_gray_wind_portrait.dds` | 800×350、legacy DDS、32-bit A8R8G8B8/BGRA、无 mipmap | straight alpha；四角透明 |
| 第一次接触 | `gfx/event_pictures/xenoamess_gray_wind_first_contact.dds` | 450×150、legacy DDS、32-bit A8R8G8B8/BGRA、无 mipmap | 不透明 |
| 战败 | `gfx/event_pictures/xenoamess_gray_wind_defeated.dds` | 450×150、同上 | 不透明 |
| 回归 | `gfx/event_pictures/xenoamess_gray_wind_return.dds` | 450×150、同上 | 不透明 |
| Workshop 缩略图 | `thumbnail.png` | 351×313、PNG | 不透明 |

输入采用已完成审核的候选图：

- 透明肖像：EvoLink 生成的 `gray-portrait-attempt-03/candidate-800x350.png`；
- 三张事件图和缩略图：Codex 原生图像能力生成的已归档候选；
- 构建只做确定性的格式转换和路径装配，不做二次绘制。

## 5. 测试方案

### 5.1 静态与构建测试

1. 独立性：包内标题、本地 ID、版本、目录和 Workshop ID 与“无限岗位”完全分离；包内禁止出现 `2976454692`、`3797257579` 或上游 `remote_file_id`。
2. 资源：逐个解析 PNG/DDS 头，断言尺寸、像素格式、mipmap 数量、alpha 模式和 SHA-256；透明肖像执行四角透明、非空可见区和 SourceOver 暗边风险检查。
3. 引用：每个新增 sprite、portrait 和本地化键只有一个定义，所有脚本引用均可解析；共享原版 sprite 未被重定义。
4. 基线差异：当前 4.4.6 原版覆盖文件与 Mod 文件做结构化/规范化差异，允许差异只出现在第 3 节表格列出的目标点。
5. 包纯度：上传目录不含 `.idea`、生成过程文件、测试证据、密钥、缓存、存档或 Python 构建产物。
6. 本地化：简体中文文件为 UTF-8 BOM 且键完整；如提供其他语言，只宣告“静态校验通过，运行时不在范围内”。
7. P 语言验收：先使用 `open_kaishek` 按其仓库说明校验全部 `.txt`、`.gfx` 与 `.mod` 脚本。工具不可用或未通过时，不得进入“验收完成”结论；若暴露工具缺陷，先在工具仓库修复、测试、提交并推送。

### 5.2 简体中文实机矩阵

采用隔离的用户数据目录和只启用本 Mod 的 playset；语言固定为简体中文。

| 编号 | 场景 | 操作/触发 | 通过标准 |
| --- | --- | --- | --- |
| R1 | 启动与加载 | 仅启用本 Mod 启动到主菜单、新开局 | Mod 被加载；标题/版本正确；无脚本、资源和本地化新增错误 |
| R2 | 第一次接触事件 | 在有效 ship scope 触发 `graygoo.400` | 450×150 新图正确显示，无拉伸、裁切异常或黑块 |
| R3 | 灰风对话链 | 依次检查 `graygoo.401`—`406` | 新透明肖像与原版房间正确合成；边缘无黑边/白边 |
| R4 | 统治者与官员 | 创建灰风并切换成人形官员，打开事件和领袖界面 | 立即显示新肖像；人物比例与裁切可接受 |
| R5 | 战败 | 触发 `graygoo.511` | 专用战败图正确显示 |
| R6 | 回归 | 建立所需事件目标并触发 `graygoo.512` | 专用回归图和新肖像均正确显示 |
| R7 | 存档重载 | 保存、退出到主菜单、重载存档 | 灰风肖像和事件目标仍正确；兼容修复无循环弹窗 |
| R8 | 共享资源隔离 | 打开仍引用 `GFX_evt_ship_in_orbit_2` 的非灰风事件 | 共享原图未被本 Mod 替换 |
| R9 | 日志回归 | 检查 `error.log`、`game.log` 和异常退出 | 与本 Mod 有关的新 error 为 0；游戏正常退出 |

每个核心场景保存一张原始截图，并记录分辨率、UI 缩放、游戏 build、触发命令、时间与日志哈希。Workshop 的实机预览图只能使用这些实际运行截图，不用 AI 合成图冒充实机界面。

实机自动化复用仓库已有 `tools/stellaris_acceptance.py` 的 DPI awareness、隔离 userdir、进程、截图、OCR 和物理扫描码能力；灰风发布根提供薄包装入口，只替换 Mod 根、本地 ID、树哈希和证据目录，不改变现有“无限岗位”夹具的冻结常量。

## 6. 发布方案

发布前必须依次满足：

1. `gray_wind_beautification/VERSION`、`descriptor.mod` 和 `CHANGELOG.md` 的 `1.0.0` 一致；Changelog 已记录新增、变更、修复、兼容范围、验收结果和已知限制。
2. Steam Change Note 以 `[v1.0.0]` 开头，并由同版本 Changelog 提炼。
3. 静态、`open_kaishek` 与简体中文实机测试全部通过，证据已落盘并回写本文档。
4. 在 Steam 创建新物品，确认返回 ID 不等于 `2976454692`、`3710613857` 或 `3797257579`；再写回 descriptor 并上传 content folder。
5. 如 Steam 要求接受 Workshop 法律协议，必须由用户本人完成；在协议完成前只可报告发布阻塞，不得代替用户接受。
6. 上传后从 Workshop 页面和干净的 SteamCMD 缓存分别回读：核对标题、公开状态、说明、缩略图、版本、文件清单与关键哈希。
7. 远端回读通过后，提交并推送仓库改动，再创建并推送 `gray-wind-v1.0.0` 标签。

## 7. 验收标准

- 灰风 Mod 可独立安装、启用、停用和卸载；不依赖“无限岗位”或上游 Mod。
- 只改变灰风人物的直接视觉表现和对应专用事件画面，不引入上游旧玩法差异。
- 五项美术资源均按资源合同落位并在实机中正确显示。
- `open_kaishek`、仓库静态测试和简体中文实机矩阵全部有可复核证据。
- 发布到一个全新的 Workshop 物品，远端回读一致；所有身份与版本信息回写仓库。

## 8. 当前状态与风险

- 2026-09-13：确认本机游戏基线为 `v4.4.6 (fdde)`；确认上游包不能整体继承，只能从当前原版做最小美术补丁。
- 2026-09-13：本机当前没有 `D:` 盘，因此约定路径 `D:\workspace\open_kaishek` 不存在。实施阶段将先取得该工具的受控副本并阅读其仓库说明；在工具通过之前不会宣告 Mod 验收完成。
- 2026-09-13：从 `https://github.com/XenoAmess/open_kaishek.git` 取得只读基线后，发现其 `stellaris-4.4.6` profile 尚未覆盖事件与 on_action。已按 fail-closed 要求在工具仓库补充灰风兼容切片并推送：文档提交 `86af4b6`，实现提交 `eb6d4de`。工具全套 `run_static_acceptance.py --online` 通过；目标包 6 个 `.txt` 共 107,981 bytes、0 parser error、corpus SHA-256 为 `a975e21d9c006979e03b36ec2665dea9e91cc2f509a3314b688b3e6a76762baa`；descriptor 与 `.gfx` 均 0 语法诊断并逐字节 round-trip；自有兼容事件与 on_action 均 0 profile diagnostic。
- 2026-09-13：灰风包专项 Python 静态测试 6/6 通过。全仓库测试另复现一个与既有“无限岗位”冻结树哈希有关的失败（仓库常量 `294f…`、当前受 Git 跟踪且无 diff 的旧 Mod 树 `2a61…`）；该失败不由灰风文件引起，不修改旧 Mod 来掩盖结果。
- 透明肖像已通过静态 alpha 初检，但最终结论以游戏内实际合成为准。
- 回归图的腿部构图接近下边缘；需由 R6 实机截图判断是否需要重绘，不能仅凭源 PNG 宣告通过。
