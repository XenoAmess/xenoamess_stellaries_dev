# Workshop 2976454692 小灰人物美术生成计划

## 目标、范围与基线

目标是以用户提供的人物设定图为唯一身份锚点，翻修与“小灰本人”直接相关、且值得形成独立美术的素材。生成链遵循[《白绮 AI 生成图 Prompt 工程手册》](https://github.com/XenoAmess/slay-the-spire-vivhite-mod/blob/master/docs/%E7%99%BD%E7%BB%AEAI%E7%94%9F%E6%88%90%E5%9B%BEPrompt%E5%B7%A5%E7%A8%8B%E6%89%8B%E5%86%8C.md)：完整不透明场景只用 Codex 原生图像生成；只有消费合同明确要求 Alpha 的独立素材才用 EvoLink `gpt-image-2`、`background="transparent"`、`n=1`。

身份参考计划归档为 `assets/workshop-2976454692/reference/gray-character-sheet.jpg`。原文件实测为 `1024 × 1536`、24-bit RGB JPEG、`227,053` bytes，SHA-256 为 `03F7D9C25B3436259B1E795371F6CEFC567437C63A38D2284119705D65824BCD`。参考图只负责以下身份事实，不负责事件构图：

- 年轻成年女性，腰长银白直发、细碎刘海、蓝眼、浅肤色、平静而略带自信的微笑；
- 黑色高领、金边、深红内衬的不对称制服式长外套，白色紧身裤，黑色短靴；
- 蓝色晶体与金色叶片状肩饰；一侧长黑手套，另一侧裸臂配黑金臂环；
- 保持设定图的服装分区和几何徽记位置，不新增可读文字、现实旗帜或额外标志。

## 适合本轮重做的素材

| ID | 素材 | 消费合同 | 生成链 | 本轮结论 |
| --- | --- | --- | --- | --- |
| `GRAY-PORTRAIT-01` | 外交/领袖人物肖像 | 独立 Alpha 人物层；最终 `800 × 350` A8R8G8B8 DDS、straight alpha、无 mip | EvoLink 透明链，`16:9 / 2K / high / n=1` | 必做；本机尚未发现 `EVOLINK_API_KEY`，Prompt 与目录先冻结，密钥就绪后调用 |
| `GRAY-FIRST-CONTACT-01` | “安静散步”首次发现图 | `disco_gray_cat` 与 `graygoo.400` 共用；最终 `450 × 150`，全幅不透明、无 mip | Codex 原生 | 必做；让原本只有飞船的通用图真正成为小灰专属初遇画面 |
| `GRAY-DEFEATED-01` | `graygoo.511`“小灰已被击溃” | 最终 `450 × 150`，全幅不透明、无 mip | Codex 原生 | 推荐；以非血腥纳米解体表现人物状态 |
| `GRAY-RETURN-01` | `graygoo.512`“小灰归来” | 最终 `450 × 150`，全幅不透明、无 mip | Codex 原生 | 推荐；与击溃图形成视觉上的解体/重构对照 |
| `GRAY-THUMBNAIL-01` | 启动器与 Workshop 主预览 | 最终 `351 × 313` RGB/RGBA PNG，所有像素不透明 | Codex 原生 | 推荐；角色居中、无文字，缩略状态保持脸和黑金红轮廓可读 |

## 本轮排除项

- `areta_005_room.dds` 是环境背景，不是人物直接素材；保留现状。
- `graygoo.500`—`503` 的三张通用 `picture` 先做简中实机显示层级验证，不在未知是否可见时生成。
- 特质图标、旗帜、陆军图标、战舰和运输舰分别属于身份 UI、国家和单位形态，不进入人物图首批。
- Workshop additional preview 应在素材接线后用真实游戏截图制作，不用 AI 场景冒充实机画面。

## 冻结 Prompt

### `GRAY-PORTRAIT-01` — EvoLink 透明人物层

```text
Use case: identity-preserve
Asset type: exactly one complete Stellaris diplomatic character portrait layer

Consumer contract:
The source will be deterministically framed into a wide 800 by 350 diplomatic portrait and reused in leader cards with different crops. The figure must form one continuous silhouette. Keep the highest hair tips, face, both shoulders, costume collar, blue-gold shoulder ornaments, upper torso and forearms readable. Let the lower torso continue naturally through the bottom edge. Place the figure center-right and keep generous usable space on screen-left.

Input images:
Image 1 defines the authoritative identity, face, silver-white hair, blue eyes, costume construction, asymmetric gloves, shoulder ornaments, colors and insignia placement. It does not define the new pose or framing.

Primary request:
Draw exactly the same original young adult woman as one polished anime-style diplomatic portrait. Use a calm, observant expression with a faint confident smile. Turn her torso slightly toward screen-left while her eyes address the viewer. Preserve her waist-length silver-white hair, blue eyes, black high-collar military-inspired coat with gold trim and deep red lining, white lower garment, blue crystal and gold leaf shoulder ornaments, one long black glove and the opposite bare arm with black-gold bands.

Style and material:
Refined science-fiction anime game illustration; clean controlled linework; restrained cel shading with soft facial modeling; crisp black cloth, brushed gold trim, deep red fabric and blue enamel-crystal accents; neutral cool key light with subtle warm edge reflection.

Composition:
Wide 16:9 source composition. One continuous upper-body figure, crown through below the waist, center-right. Hair tips and shoulder ornaments remain uncropped. The face stays inside the central safe area for leader-card crops. No important feature may touch the top or side edges.

Constraints:
Exactly one figure and one pose. Preserve identity and costume topology. Empty hands. No weapon, spacecraft, furniture, extra character, duplicate view, pose sheet, panel, typography, watermark or newly invented readable lettering. No red line, blood, liquid, ribbon or magical strand at the mouth or face, and nothing may emerge from the mouth.
```

公开请求参数冻结为：`model=gpt-image-2`、`size=16:9`、`resolution=2K`、`quality=high`、`background=transparent`、`n=1`。Prompt 不出现透明底、白底、棋盘格或其他背景指令；透明度仅由 API 参数控制。

### `GRAY-FIRST-CONTACT-01` — 不透明首次发现横幅

```text
Use case: stylized-concept
Asset type: Stellaris narrative event banner, full opaque scene
Input images: Image 1 is the sole identity and costume reference for Gray; preserve her face, long silver-white hair, blue eyes, black-gold-red asymmetric uniform, white leggings, asymmetric gloves and blue-gold shoulder ornaments.
Primary request: depict the first discovery of Gray walking calmly and impossibly without a spacesuit across the lifeless south-polar surface of a nanite world while a distant science vessel observes her.
Scene/backdrop: full-width barren dark metallic-gray planetary surface in the foreground, subtle liquid-nanite patterns and windless dust in the midground, a curved planet horizon and a compact observing science ship in the far distance; the environment responds to her steps with restrained silver nanite ripples.
Subject: exactly one Gray, recognizable from the reference, walking with relaxed composure and looking toward the unseen observers; no helmet and no life-support equipment.
Style/medium: polished cinematic science-fiction anime event illustration consistent with the reference character design.
Composition/framing: ultra-wide 3:1 banner; keep Gray large enough to read at 450 by 150, positioned near the central-right third; keep her entire silhouette and the ship inside the central horizontal crop-safe band; no UI and no border.
Lighting/mood: cold blue-gray starlight with a controlled warm rim from a distant star; eerie, quiet, intriguing rather than threatening.
Constraints: one character only; preserve costume; no text, logo, watermark, speech bubble, spacesuit, gore, weapon or extra humanoid. No red line, blood, liquid, ribbon or magical strand at the mouth or face.
```

### `GRAY-DEFEATED-01` — 不透明击溃横幅

```text
Use case: stylized-concept
Asset type: Stellaris narrative event banner, full opaque scene
Input images: Image 1 is the sole identity and costume reference for Gray.
Primary request: show Gray at the moment her humanoid form is peacefully disassembling into countless silver nanomachines after defeat, clearly temporary and non-gory rather than dead.
Scene/backdrop: full-width damaged spacecraft command chamber with dim inactive consoles in the foreground, fractured blue holographic light in the midground and distant stars through a viewport; loose nanites drift toward a compact dormant core.
Subject: exactly one recognizable Gray from the reference, upper body and calm face still readable while the outer edges of her long silver hair and black-gold-red uniform break into fine metallic particles; empty hands; no injury or blood.
Style/medium: polished cinematic science-fiction anime event illustration, crisp character identity, controlled particles and readable silhouette.
Composition/framing: ultra-wide 3:1 banner; Gray in the central-right third, face and shoulder ornaments inside the crop-safe center; particle flow stays within the frame; no UI and no border.
Lighting/mood: subdued indigo and steel-gray light, quiet interruption and suspended time, a faint gold-blue glow remaining in her eyes and ornaments.
Constraints: one character only; no corpse, gore, blood, exposed anatomy, weapon, enemy, text, logo, watermark or duplicate body. No red line, liquid, ribbon or magical strand at the mouth or face.
```

### `GRAY-RETURN-01` — 不透明归来横幅

```text
Use case: stylized-concept
Asset type: Stellaris narrative event banner, full opaque scene
Input images: Image 1 is the sole identity and costume reference for Gray.
Primary request: show Gray fully reconstructed from a silver nanite tide, returning with her familiar calm and slightly amused smile.
Scene/backdrop: full-width alien nanite-world plain in the foreground, flowing metallic-gray particles converging around her boots and coat hem, geometric blue-gold reconstruction light in the midground, a dark planet horizon and restrained stars in the distance.
Subject: exactly one recognizable Gray from the reference, stable and intact, long silver-white hair settling after rematerialization, black-gold-red uniform and blue-gold shoulder ornaments faithfully restored, empty hands.
Style/medium: polished cinematic science-fiction anime event illustration consistent with the reference; elegant rather than explosive.
Composition/framing: ultra-wide 3:1 banner; Gray centered slightly right and readable at 450 by 150; face, shoulders and full reconstruction silhouette stay inside the crop-safe band; no UI and no border.
Lighting/mood: luminous cool silver and blue reconstruction light with restrained warm gold accents; relief, continuity and quiet confidence.
Constraints: one character only; no enemy, weapon, extra figure, text, logo, watermark, gore or incomplete anatomy. No red line, blood, liquid, ribbon or magical strand at the mouth or face.
```

### `GRAY-THUMBNAIL-01` — 不透明主缩略图

```text
Use case: ads-marketing
Asset type: square-safe game mod thumbnail, full opaque illustration
Input images: Image 1 is the sole identity and costume reference for Gray.
Primary request: create a striking character-led key art portrait of Gray for a Stellaris mod thumbnail, preserving her exact identity and costume family.
Scene/backdrop: full-frame deep-space setting with a softly glowing L-Gate arc, restrained silver nanite clouds and distant stars; the environment frames the character without obscuring her silhouette.
Subject: exactly one Gray from the reference, chest-up, facing the viewer with a calm confident smile, silver-white hair flowing gently, blue eyes and blue-gold shoulder ornaments sharply readable, black-gold-red uniform recognizable at small size.
Style/medium: premium polished science-fiction anime key art; clean silhouette, controlled detail and strong thumbnail readability.
Composition/framing: near-square composition with face centered in the inner 60 percent and generous edge safety for a final 351 by 313 crop; shoulders visible; no typography.
Lighting/mood: cool blue rim light from the gate, warm gold accents on trim, mysterious but welcoming.
Constraints: exactly one character; no extra face, duplicate, weapon, text, letters, logo, watermark, UI frame or clutter. No red line, blood, liquid, ribbon or magical strand at the mouth or face.
```

## 生成、归档与验收

- 每张语义素材独立使用 `attempt-01` 目录；原图、逐字 Prompt、可验证生成事实和检查结论只追加、不覆盖。
- Codex 原生结果不得臆造内部模型、seed 或隐藏请求字段；EvoLink 记录不得保存 API Key、Authorization、临时签名 URL或完整服务端响应。
- 不透明原图必须检查为全幅场景、无透明像素、无文字/水印/重复人物，再做确定性中央裁切和 Lanczos 尺寸适配；不得生成透明人物后补背景。
- 透明肖像必须保留 EvoLink 原始 RGBA，检查 PNG、尺寸、四角 Alpha、`A>0/16/127` 包围盒，并真实 SourceOver 到黑、白和接近外交 UI 的蓝灰底色；不得阈值化、色键、收缩或清理 Alpha。
- 第一轮达到身份、构图和消费规格即停止；失败时先归因为消费合同、Prompt、模型或验收问题，下一轮只验证一个主要假设，每个语义最多 8 次。
- 本轮只能形成静态候选。只有完成 Mod 接线、`open_kaishek` 检查和简体中文 Stellaris 实机回归后，才可宣称验收完成。

