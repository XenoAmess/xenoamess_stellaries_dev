# 合成女王替换·牢大：`0.1.2` 缩略图更新计划

日期：2026-09-26。用户提供 `laoda.zip`，要求把已发布 Mod 的 thumbnail 换成其中的图片。ZIP SHA-256 `4ca8b7fa4522e906d3db7b2475a20e6849ce13898df779f550b3511e6d493496`，只含 `laoda.png`，800×800 RGBA、Alpha 恒为 255，原始 PNG 633,312 字节、SHA-256 `89269b3da6cea8a0071fbd61b285414e8e04ac69a4dcfad6545ed55399efc520`。目视检查：图中有此前实际游玩对话、人物与球衣广告，以及“孩子们，我终于回到了你们的身边”台词。文件是用户指定的成品，按原字节使用，不重绘、不裁切、不转码。

## 目标与范围

- 将 ZIP 中 `laoda.png` 归档为 `assets/reference/thumbnail-v0.1.2.png`，并逐字节复制到 `mod/thumbnail.png`。描述符 `picture="thumbnail.png"` 继续引用它。
- 同时把 Steam 工坊物品 `3807817109` 的**主预览图**换成这张用户提供的 800×800 PNG。原来作为主预览的 Steam F12 原始截图 `workshop/media/01-children-returned.jpg` 改为新增附加预览；现有附加截图 `02-first-dialogue.jpg` 保留。两张完整实际游玩截图及其 BBCode `[img]` 链接继续保留。
- 现有 BBCode 中“这张原始 Steam F12 截图也是工坊主预览图”一句随主预览切换而改为准确描述；其它介绍保持一致。肖像 DDS、十个原版键映射、游戏内场景、玩法脚本、语言与 `supported_version="4.5.*"` 不变。
- 远端已成功发布 `0.1.1`，本次更新使用尚未发布的新版本 `0.1.2`。上传前统一 `VERSION`、描述符、`CHANGELOG.md`、`workshop/change-note-v0.1.2.txt`；Change Note 以 `[v0.1.2]` 开头，正式 changelog 完整记录新增、变更、修复、兼容范围、验收和限制。工坊 ID 不变，绝不再调用 `CreateItem`，也不更新其它物品。

## 实施与发布顺序

1. 本计划先行；随后复制用户文件、调整图片制作工具使其验证并保留新缩略图原字节，更新版本、BBCode 和一条独立的已有物品更新工具。缩略图不得被旧的 `prepare_workshop_media.py` 重新生成图覆盖。
2. 图片静态检查：ZIP、归档文件、`mod/thumbnail.png` 的 SHA-256 一致；可解码为 800×800 PNG，四角不要求透明；头像、广告和指定台词缩略状态可见；文件小于 Steam 预览图上限。两张完整 F12 截图仍与已发布图片资产原字节一致。
3. 按仓库 P 语言验收规则，先用 `C:\workspace\open_kaishek` 的 `stellaris-4.5.1` profile 再验收未改动的生产肖像入口，并解析新描述符；检查 DDS 和肖像定义 SHA-256 与 `0.1.1` 相同。只有发布展示资源变化，无需重新宣称游戏内 R2/R4 已通过；沿用此前 R1/R3/R5 证据，明确限制。
4. 提交、推送正式包及新文案后，更新工具在干净 Git 工作树上只读预检，核对目标 ID 为 `3807817109`、当前远端是 `0.1.1`、新版本未使用、包白名单、主预览源图、截图与 Change Note。Steam 需在线；若临时改变原离线偏好，备份并在上传核验后恢复。
5. 使用 Steamworks `StartItemUpdate` 更新**已有**物品，只设置必要的标题/说明、Mod 内容文件夹、新主预览、补充一张 `01-children-returned.jpg` 附加预览、标签/可见性；以 `[v0.1.2]` Change Note 调用 `SubmitItemUpdate`。回执须为同一 ID、`result=1` 且无法律协议阻断。
6. 匿名远端详情与 Steamworks 图片查询核对新版本、说明、主预览 PNG 原字节、两张完整截图；SteamCMD 从隔离缓存重新下载四文件，与已提交 Mod 包逐文件比对。工坊 Change Note 页面读回 `[v0.1.2]`。记录证据到 `evidence/v0.1.2/`，提交并推送；远端核验后创建、推送标签 `v0.1.2` 及产品别名。

## 完成标准与限制

本地和远端 thumbnail/主预览均为用户 ZIP 中的**同一张原始 PNG**；工坊仍有两张真实游戏截图作为附加图片与 BBCode 图片资产；下载包除描述符版本和 thumbnail 外与 `0.1.1` 一致。R2 基础肖像独立界面、R4 有效结局上下文仍未验收，不把图片更换说成新一轮游戏实机通过。

## 发布前检查记录

- ZIP 只含 `laoda.png`；归档文件与 `mod/thumbnail.png` 原始字节完全相同，SHA-256 均为 `89269b3da6cea8a0071fbd61b285414e8e04ac69a4dcfad6545ed55399efc520`。图片 800×800 RGBA、完全不透明、633,312 字节，小于 Steam 预览图上限；已目视检查人物、球衣广告和指定台词。`tools/prepare_workshop_media.py` 运行后 SHA 不变，两张原 F12 JPEG 的 SHA 仍为 `ff0a65dce629a69c1d2afcb1c1b35a84f57de8f619b2e9e9f8f50df4ec74fabf`、`a3ab86f404718ec0a2259a152310eb816066922966bf5596eb9448022002a883`。
- 生产 `mod/` 为四个预期文件；DDS SHA-256 `a35c0431498c6b8511bed0604517ba629695edad86e0556c277019d0bbbbf071` 与肖像定义 SHA-256 `70c05b267415576635831cef640283f7df3c1d1f719e1fd8ba444bd7323e51b4` 均与 `0.1.1` 完全相同。`open_kaishek` 的 `validate --profile stellaris-4.5.1` 返回 `VALIDATED`、0 语法/语义诊断；新描述符 `parse` 返回 `PARSED`、0 诊断、`roundTrip=true`。
- 新版本与描述符均为 `0.1.2`，正式 changelog 和 `[v0.1.2]` Change Note 已在上传前建立。图片、更新和核验工具 `py_compile` 通过，`git diff --check` 通过。
- 匿名 Steam 发布前基线仍为物品 `3807817109`、公开状态 `visibility=0`、`time_updated=1790345259`、内容句柄 `1456108296541887760`、远端说明 SHA-256 `bf52dad7b935493c2ec8daef1583c318354974c9d213ea7b41cf57ee7cf80392`，与 `0.1.1` 发布证据一致。更新工具将此基线作为强制门禁。

## 发布与远端验收记录

- 正式包与更新工具在提交 `f7589e909656c736b1a0d082290fd740800c10b7` 推送后通过只读预检。Steamworks 对**已有**物品 `3807817109` 的更新回执为 `result=1`、同一物品 ID、`legal_agreement_required=false`；提交的 Change Note 文件以 `[v0.1.2]` 开头。回执见 [`evidence/v0.1.2/update-state.json`](../evidence/v0.1.2/update-state.json)。
- 匿名公开详情显示物品仍公开，更新后 `time_updated=1790353166`，内容句柄 `4489619570166820753`，说明与本地 BBCode 原文一致。Steam 图片服务器返回的**主预览**是 633,312 字节 PNG，SHA-256 `89269b3da6cea8a0071fbd61b285414e8e04ac69a4dcfad6545ed55399efc520`，与 ZIP 原图和 `mod/thumbnail.png` 逐字节一致。两张附加图片分别与原 F12 游戏截图 `02-first-dialogue.jpg`、含“孩子们，我终于回到了你们的身边”的 `01-children-returned.jpg` 逐字节一致。详见 [`evidence/v0.1.2/workshop-update-verification.json`](../evidence/v0.1.2/workshop-update-verification.json)。
- 使用新安装、空工坊缓存的 SteamCMD 匿名重新下载物品成功，共 4 文件、1,755,086 字节；各文件路径、大小和 SHA-256 均与本地 `mod/` 完全一致，详见 [`evidence/v0.1.2/steamcmd-roundtrip.json`](../evidence/v0.1.2/steamcmd-roundtrip.json)。另外核对前一个合成女王 Mod 物品 `3807768508` 和只读上游 `3710613857` 的更新时间及内容句柄，均未改变。
- 工坊社区网页及 Change Note 页面遭遇 HTTP 429，故**未能独立读回公开页面上的更新说明文字**；只能确认 Steamworks 提交成功及本地发送的 `[v0.1.2]` 原文。公开详情、图片原字节和下载包均已从远端分别核验。Steam 原有 `WantsOfflineMode=1` 偏好已从备份恢复，客户端重新启动。
- 本次仅更换缩略图及发布展示资源。此前 R2 基础肖像独立界面、R4 有效结局上下文尚未验收的限制继续适用；本次没有宣称新的游戏内实机通过。
