# 小灰 EvoLink 透明素材 Prompt

本目录只保存计划发送给 EvoLink 的逐字 Prompt，不代表请求已经发送或产生费用。

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

不得把 API Key、Authorization 头、临时签名结果 URL 或完整 API 响应写入仓库。真实请求成功创建后，另在 `generated/evolink-paid/YYYY-MM-DD/gray-portrait-attempt-01/` 追加保存未经后处理 PNG、逐字 Prompt、脱敏 request 和 task id；不得覆盖本目录中的版本文件或任何旧 attempt。
