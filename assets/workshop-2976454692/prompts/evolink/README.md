# 小灰 EvoLink 透明素材 Prompt

本目录保存最初冻结的 EvoLink 逐字 Prompt 和请求规格。实际付费生成已经执行三次；每次逐字 Prompt、脱敏请求、task id、未经处理原图和检查证据分别保存在 `assets/workshop-2976454692/generated/evolink-paid/2026-09-13/gray-portrait-attempt-01/` 至 `gray-portrait-attempt-03/`，本目录中的原始计划文件不覆盖。

`gray-portrait-v1.txt` 的固定公开请求参数为：

```text
endpoint=https://api.evolink.ai/v1/images/generations
model=gpt-image-2
size=16:9
resolution=2K
quality=high
background=transparent
n=1
image_urls=https://raw.githubusercontent.com/XenoAmess/xenoamess_stellaries_dev/main/assets/workshop-2976454692/reference/gray-character-sheet.jpg
```

当前结论：attempt-01 因全画幅场景污染 Alpha 淘汰，attempt-02 因发冠触顶保留为研究候选，attempt-03 的 `candidate-800x350.png` 通过静态 Alpha 与三底 SourceOver 检查。不得覆盖任何旧 attempt，也不得把 API Key、Authorization 头、临时签名结果 URL 或完整 API 响应写入仓库。
