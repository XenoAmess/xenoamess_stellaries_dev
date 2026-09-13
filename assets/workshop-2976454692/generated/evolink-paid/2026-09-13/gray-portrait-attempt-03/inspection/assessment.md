# GRAY-PORTRAIT-01 attempt-03 静态检查

## 结论

`candidate-800x350.png` 通过本轮身份、构图、原生 Alpha、三底 SourceOver、实际尺寸和禁项静态检查，可作为小灰外交/领袖肖像的接线候选。这里只确认 PNG 美术源；尚未转换为 A8R8G8B8 DDS、接入 Mod、运行 `open_kaishek` 或执行简体中文 Stellaris 实机回归。

## 请求事实

- EvoLink task：`task-unified-1789284058-xrd0dcsi`
- `model=gpt-image-2`
- `size=16:9`
- `resolution=2K`
- `quality=high`
- `background=transparent`
- `n=1`
- 参考图为仓库公开 HTTPS URL；API Key、Authorization 和结果下载 URL 均未写入仓库。

## 原图与 Alpha 事实

- 文件：`../original.png`
- PNG，`2736 × 1536`，RGBA8，`3,592,147` bytes
- SHA-256：`FF2DABB36B3B95C471797D2366D2E3C9DB123CDB480C16CA463D80ACB24937DE`
- Alpha extrema：`0–254`
- 四角 Alpha：`[0, 0, 0, 0]`
- `A>0`：`1,240,222` pixels，bbox `(47, 9, 2696, 1536)`
- `A>16`：`1,143,482` pixels，bbox `(936, 20, 2146, 1536)`
- `A>127`：`1,123,983` pixels，bbox `(937, 21, 2146, 1536)`

## 确定性派生

- 保留未经后处理的 `original.png` 不变。
- 为适配 `800:350` 消费比例，使用固定顶对齐裁切框 `(0, 0, 2736, 1197)`；保留全宽、顶部发冠和人物中心，允许腰下自然延续出底边。
- 使用 Pillow 12.3.0 `Image.Resampling.LANCZOS` 缩放为 `800 × 350` RGBA PNG；没有生成式扩图、阈值、色键、抠图、Alpha 收缩或边缘清理。
- 候选文件：`../candidate-800x350.png`，`208,445` bytes
- 候选 SHA-256：`BEE88ED2DD5C9A7330777BE807D1D8310F514A3A6D2B19ABACDB1B1FD3490C4C`
- 候选 Alpha extrema：`0–255`
- 候选四角 Alpha：`[0, 0, 0, 0]`
- 候选 `A>0` bbox：`(271, 4, 631, 350)`
- 候选 `A>16` bbox：`(273, 6, 628, 350)`
- 候选 `A>127` bbox：`(274, 6, 627, 350)`

## 视觉、SourceOver 与禁项

- 银白长发、蓝眼、平静微笑、黑金红制服、蓝金肩饰和非对称手套关系与身份参考一致；脸部和服装在 `800 × 350` 实际尺寸下清楚。
- 人物居中略偏右，左侧有大面积可用空间；发冠上方保留 6 px 的 `A>16` 安全边，肩饰和发梢没有碰触左右边。
- 黑、白和外交蓝灰三底 SourceOver 均没有矩形底、场景残留或肉眼可见的全画幅光幕。
- 只有一名人物；未见场景、额外人物、武器、血腥、口部红线或口部异物。
- 服装保留参考式伪字形、鹰形和十字状徽记；它们没有形成连贯可读正文，但正式采用仍需用户确认其视觉含义。

## 状态

`static_accepted_pending_runtime_and_user_review`。下一步应先由用户确认人物风格与服装徽记，再转成目标 DDS、接线并执行项目规定的 Mod 验收链。
