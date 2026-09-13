# GRAY-PORTRAIT-01 attempt-01 静态检查

## 结论

本轮淘汰，不得转为运行时候选。人物身份、姿态和服装可读性良好，但返回图把完整太空港、行星、舰船和舷窗场景写入了几乎全画幅的非零 Alpha；它不是消费合同要求的独立人物叠层。禁止通过阈值化、色键、抠图或 Alpha 清理把本轮结果伪装为合格透明素材。

## 请求事实

- EvoLink task：`task-unified-1789282822-3w6ojxia`
- `model=gpt-image-2`
- `size=16:9`
- `resolution=2K`
- `quality=high`
- `background=transparent`
- `n=1`
- 只引用公开的身份设定图 URL；Prompt、脱敏请求和 task id 已独立归档。

## 原图与 Alpha 事实

- 文件：`../original.png`
- PNG，`2736 × 1536`，RGBA8，`6,649,032` bytes
- SHA-256：`D48EB6B5FF94590E5E79CC301ED986EF173BA6F198EA7FB4627178FECA7B6B8D`
- Alpha extrema：`1–253`
- 四角 Alpha：`[4, 4, 3, 94]`
- `A>0`：`4,202,496` pixels，bbox `(0, 0, 2736, 1536)`
- `A>16`：`3,972,103` pixels，bbox `(0, 0, 2736, 1536)`
- `A>127`：`3,054,360` pixels，bbox `(315, 0, 2736, 1536)`

## SourceOver 与禁项检查

- `sourceover-black.png`、`sourceover-white.png` 和 `sourceover-diplomatic-bluegray.png` 均真实使用原始 Alpha 合成；三底都能看到完整太空场景，白底还暴露出大面积半透明云状边界。
- Alpha 灰度图为 `alpha-channel.png`，证明问题不是普通查看器误显 `Alpha=0` RGB，而是全画幅真实存在非零 Alpha。
- 未见第二人物、武器、血腥、口部红线或口部异物。
- 服装出现参考式伪字形和十字状徽记；不是本次透明失败的主因，但正式候选仍需复核。

## 下一轮单变量假设

保持模型、API 透明参数、画幅、质量、身份参考和人物构图不变，只把 Prompt 的对象范围收紧为“画面中唯一可描绘对象是小灰本人”，并明确排除场景、建筑、舷窗、星空、行星和舰船。Prompt 仍不描述透明底、白底、灰底、绿幕或棋盘格，透明度继续只由 API 参数控制。
