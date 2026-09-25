# 合成女王替换·牢大：实施计划

## 目标与输入

日期：2026-09-25。用户要求另建独立 Mod，准确名称为 **XenoAmess的合成女王替换·牢大**，以本次 ZIP 内唯一的参考图通过 EvoLink 生成真实透明背景人物图。ZIP SHA-256 为 `6991e3afcd9bb6fee75cc198ee05fd12942b02cdb3d55a035feeee31f69d2714`；内含一张 720×1078 RGB JPG，原始文件 SHA-256 为 `872d656b3af25b3952321f5e7976acd7df205a662d387db7cd7b39ed29f138d2`。参考图是深肤色、短发男性正面半身像，面带笑容，穿橙黄色无袖运动球衣。**人物、球衣的款式和颜色，以及胸前「冰红茶」「康师傅」等广告文字、商标、图案和排版都属于必须原样保留的主体内容。只去掉蓝色背景及右下角水印。**

## 范围与设计

- 使用独立目录 `synthetic_queen_laoda_replacement/`，独立 `VERSION`、`CHANGELOG.md`、`mod/descriptor.mod`、生成源图和验收记录。版本先定为 `0.1.0-rc.1`。实机开始前发现本机 Stellaris 已自动更新为 `Cygnus v4.5.1 (358e)`，可执行文件 SHA-256 为 `6fe06709f265e726722dc23f617c5fc4e5557629e2d43fe312016aba547c83e4`；该版本原版 `21_portraits_cybernetics_synthqueen.txt` 与此前 4.4.6 基线**逐字节一致**，SHA-256 均为 `9a2ccd43d297112176092e62a9e488b63a8ca271915d028b84e14491724fee18`，十个键与问候音均未变。因此改为面向当前实机的 `supported_version="4.5.*"`，并为 `open_kaishek` 增加只覆盖该精确肖像文件的 4.5.1 静态验收切片。不继承或写入其他 Workshop 物品 ID；本轮不发布。
- 复用 [已核实的 10 个原版肖像键](../../synthetic_queen_beautification/docs/asset-audit.md)，覆盖 `gfx/portraits/portraits/21_portraits_cybernetics_synthqueen.txt`，让全部键指向本 Mod 专用的 `gfx/models/portraits/xenoamess_cetana_laoda_portrait.dds`。保持原问候音与原版事件调用的键名，不改玩法脚本。
- 生成图以参考人物的面部、笑容、肤色、橙黄球衣及其全部广告为严格参照，画面只允许原参考人物；面部、衣着、胸前「冰红茶」广告及其他可见文字、商标、图案的位置和形态必须原样保留，不接受改写成伪文字或重设计。保持肩膀、面部和头顶完整，底部身体自然延伸到画布边缘。只去掉蓝底和右下角水印，不生成星空、房间、雾幕、发光矩形和额外人物。
- 原版合成女王材质是 UV 分片与动画网格，不可把普通半身画像直接覆写成原版 1024×1024 贴图；沿用已验证的静态 `texturefile` 肖像定义，输出 800×350 BGRA8 DDS，保留 straight alpha。原版动态动作和按物种变化的细节会被统一静态图替代。
- 实机发现 PowerShell 写入的肖像定义带 UTF-8 BOM (`EF BB BF`)，Stellaris 4.5.1 将其视为非法 token，十个肖像键失效。`open_kaishek` 的漏检已先行修复并推送；本 Mod 肖像定义必须按 UTF-8 **无 BOM** 重写，目标文件开头应为 `# Static`，然后重新通过工具及实机检查。

## EvoLink 透明生成合同

依据 [EvoLink GPT Image 2 API](https://evolink.ai/gpt-image-2)，使用 `POST /v1/images/generations` 的 `gpt-image-2`，优先以 `size=720x1088` 贴近原图 720×1078 的构图（自定义宽高需为 16 的倍数）、`quality=high`、`background=transparent`、`output_format=png`、`n=1`，`image_urls` 只含本次参考图的固定 Git 原始文件 URL。先要求服务仅做人物原位抠取并保持原始人像、球衣及广告的每个像素，不重绘、不改姿势、不横向改画幅。之后把透明人物按比例缩入 800×350 肖像画布，务必显示脸及胸前主广告。EvoLink 说明透明背景仍为 Preview，因此不能仅凭参数认定有 Alpha；必须检查原始 PNG。

先把参考图以原始字节归档并推送，取得固定提交 URL，再提交生成任务。每次尝试保留逐字 Prompt、脱敏请求、task ID、原始 PNG、检查结果；不记录 API Key、Authorization 头、临时签名 URL 或完整服务端响应。只有原人物与原球衣广告忠实保留、真实 RGBA、四角透明、无可见矩形场景污染且主体适合 800×350 视口的候选可进入 Mod。失败图留作证据，按具体问题修订 Prompt 后再生成。不以阈值、色键或本地抠图伪造透明度。

首次 `gpt-image-2` 请求实际返回的 RGBA 虽有 Alpha，却把暗色背景作为不透明内容留下，并重绘了人物和广告，因此不得用于生产图。改用 [EvoLink Seedream 5.0 Pro Layerize](https://evolink.ai/blog/how-to-use-seedream-5-0-pro-layerize-api) 的图层拆分：以同一 JPG 作为唯一输入，语义提示只提取“完整人物及其衣服广告”作为一张透明 PNG 图层，排除背景和水印。该服务输出的图层具备透明通道及坐标元数据，适合保留原图主体。已获得 832×1248 基底和 832×1205 人物层，后者坐标为 `(0,43,832,1248)`；人物层四角 Alpha 均为 0，但其 RGB 仍重绘了球衣。因此生产路径只取该人物层的 Alpha，依坐标放回基底，再缩至原图 720×1078，与原 JPG 的 RGB 合并。肖像取原图顶部 900 像素，包含脸、主广告和球衣下方副图案，同时完整避开底部水印；按比例缩到高 350 后置于 800×350 透明画布中央。初版黑底预览可见原 JPEG 在人物轮廓上的细蓝边；只在 EvoLink Alpha 轮廓内侧固定 5 像素窄带中，用原 JPG 的最近内部人物像素替换受蓝底污染的 RGB，**胸前广告和人物中央区域仍与原 JPG 逐像素相同**。Alpha 全程保持 EvoLink 图层数据，不以本地阈值或色键创建。配准位置、广告区域与原 JPG 的像素一致性、边缘效果须另记实测证据。

通过的原图只做记录了参数的确定性裁切、Lanczos 缩放与 BGRA DDS 打包；原图、800×350 PNG、DDS 的尺寸、模式、SHA-256 和 Alpha 范围均应可复核。候选需分别 SourceOver 到黑、白和接近游戏外交面板的蓝灰底上目视检查，确认没有画布矩形边界。

## 交付与验收标准

1. `mod/` 只包含描述符、10 键肖像定义和新 DDS，版本与 changelog 一致；不得携带参考图、提示词、其他 Mod 文件或远端 ID。
2. 生成原图有真实透明通道，DDS 与预览 PNG 解码后逐像素一致；人物、衣着及「冰红茶」广告与参考图一致，广告文字可辨且未改写；头肩完整，蓝底和水印消失，画布外缘不形成矩形背景。
3. 先按 `C:\workspace\open_kaishek` 说明以当前 `stellaris-4.5.1` 肖像切片校验 P 语言生产入口，再完成静态引用和简体中文隔离实机检查；未观察到的 R2/R4 场景必须明确标为未验收。
4. 不做与上一合成女王 Mod 或灰风 Mod 的并用测试；两个合成女王替换包覆盖同一原版肖像定义文件，玩家应择一启用。
