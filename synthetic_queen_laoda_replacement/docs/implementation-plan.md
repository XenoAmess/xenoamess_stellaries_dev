# 合成女王替换·牢大：实施计划

## 目标与输入

日期：2026-09-25。用户要求另建独立 Mod，准确名称为 **XenoAmess的合成女王替换·牢大**，以本次 ZIP 内唯一的参考图通过 EvoLink 生成真实透明背景人物图。ZIP SHA-256 为 `6991e3afcd9bb6fee75cc198ee05fd12942b02cdb3d55a035feeee31f69d2714`；内含一张 720×1078 RGB JPG，原始文件 SHA-256 为 `872d656b3af25b3952321f5e7976acd7df205a662d387db7cd7b39ed29f138d2`。参考图是深肤色、短发男性正面半身像，面带笑容，穿橙黄色无袖运动球衣。**人物、球衣的款式和颜色，以及胸前「冰红茶」「康师傅」等广告文字、商标、图案和排版都属于必须原样保留的主体内容。只去掉蓝色背景及右下角水印。**

## 范围与设计

- 使用独立目录 `synthetic_queen_laoda_replacement/`，独立 `VERSION`、`CHANGELOG.md`、`mod/descriptor.mod`、生成源图和验收记录。版本先定为 `0.1.0-rc.1`，`supported_version="4.4.*"`。不继承或写入其他 Workshop 物品 ID；本轮不发布。
- 复用 [已核实的 10 个原版肖像键](../../synthetic_queen_beautification/docs/asset-audit.md)，覆盖 `gfx/portraits/portraits/21_portraits_cybernetics_synthqueen.txt`，让全部键指向本 Mod 专用的 `gfx/models/portraits/xenoamess_cetana_laoda_portrait.dds`。保持原问候音与原版事件调用的键名，不改玩法脚本。
- 生成图以参考人物的面部、笑容、肤色、橙黄球衣及其全部广告为严格参照，画面只允许原参考人物；面部、衣着、胸前「冰红茶」广告及其他可见文字、商标、图案的位置和形态必须原样保留，不接受改写成伪文字或重设计。保持肩膀、面部和头顶完整，底部身体自然延伸到画布边缘。只去掉蓝底和右下角水印，不生成星空、房间、雾幕、发光矩形和额外人物。
- 原版合成女王材质是 UV 分片与动画网格，不可把普通半身画像直接覆写成原版 1024×1024 贴图；沿用已验证的静态 `texturefile` 肖像定义，输出 800×350 BGRA8 DDS，保留 straight alpha。原版动态动作和按物种变化的细节会被统一静态图替代。

## EvoLink 透明生成合同

依据 [EvoLink GPT Image 2 API](https://evolink.ai/gpt-image-2)，使用 `POST /v1/images/generations` 的 `gpt-image-2`，`size=16:9`、`resolution=2K`、`quality=high`、`background=transparent`、`output_format=png`、`n=1`，`image_urls` 只含本次参考图的固定 Git 原始文件 URL。EvoLink 说明透明背景仍为 Preview，因此不能仅凭参数认定有 Alpha；必须检查原始 PNG。

先把参考图以原始字节归档并推送，取得固定提交 URL，再提交生成任务。每次尝试保留逐字 Prompt、脱敏请求、task ID、原始 PNG、检查结果；不记录 API Key、Authorization 头、临时签名 URL 或完整服务端响应。只有原人物与原球衣广告忠实保留、真实 RGBA、四角透明、无可见矩形场景污染且主体适合 800×350 视口的候选可进入 Mod。失败图留作证据，按具体问题修订 Prompt 后再生成；如生成器改动了广告，评估其遮罩编辑能力，使球衣原始像素得到保留，同时由 EvoLink 生成透明通道。不以阈值、色键或本地抠图伪造透明度。

通过的原图只做记录了参数的确定性裁切、Lanczos 缩放与 BGRA DDS 打包；原图、800×350 PNG、DDS 的尺寸、模式、SHA-256 和 Alpha 范围均应可复核。候选需分别 SourceOver 到黑、白和接近游戏外交面板的蓝灰底上目视检查，确认没有画布矩形边界。

## 交付与验收标准

1. `mod/` 只包含描述符、10 键肖像定义和新 DDS，版本与 changelog 一致；不得携带参考图、提示词、其他 Mod 文件或远端 ID。
2. 生成原图有真实透明通道，DDS 与预览 PNG 解码后逐像素一致；人物、衣着及「冰红茶」广告与参考图一致，广告文字可辨且未改写；头肩完整，蓝底和水印消失，画布外缘不形成矩形背景。
3. 先按 `C:\workspace\open_kaishek` 说明校验 P 语言生产入口，再完成静态引用和简体中文隔离实机检查；未观察到的 R2/R4 场景必须明确标为未验收。
4. 不做与上一合成女王 Mod 或灰风 Mod 的并用测试；两个合成女王替换包覆盖同一原版肖像定义文件，玩家应择一启用。
