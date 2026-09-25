# 合成女王替换·牢大 `0.1.0-rc.1` 制作与验收记录

日期：2026-09-25。以用户本次 ZIP 中唯一的 JPG 为参考；原图 720×1078 RGB，SHA-256 `872d656b3af25b3952321f5e7976acd7df205a662d387db7cd7b39ed29f138d2`。原图原始字节已归档在 `assets/reference/laoda-reference.jpg`，固定提交 `c057333` 的 GitHub raw URL 经 HTTP 200 下载复核，SHA-256 相同。目标为人物、衣着和胸前全部广告原样保留，只移除蓝色背景与右下角水印。

## EvoLink 首次透明编辑失败

`tools/evolink_generate.py` 使用 `gpt-image-2`、`720x1088`、`high`、`background=transparent`、PNG、`n=1` 和固定参考图 URL；逐字 Prompt、脱敏请求与任务 ID 见 `assets/generated/evolink-paid/2026-09-25/laoda-attempt-01/`。任务 `task-unified-1790340533-y2vsafzj` 完成，原始 PNG SHA-256 `9955bf82e0450d357dbe946ca2f6af2e2df22b29f14fcc60a2893c07cdefc212`，720×1088 RGBA。Alpha 最小/最大为 `0/254`，四角为 `0,0,253,250`；`A>127` 的包围盒从 `(0,8)` 延伸到整幅右侧与底边。右侧和下方仍可见大片暗色模糊背景，形成矩形画布；人物与广告也被重绘。原图与结果直接比较，主广告区域 `(210,480,520,720)` 的 RGB 平均绝对误差为 `94.39/255`。**该图不可进入 Mod**。

## 图层拆分与原广告保留

改用 EvoLink 的 `doubao-seedream-5.0-pro-layerize` 从同一原图提取“人物加完整球衣广告”为一张带 Alpha 的图层。任务 `task-unified-1790340773-g0flln41` 返回一张 832×1248 底图和一张 832×1205 人物层，后者 SHA-256 `c46511f05e2e62b87cd2a5a5c9bc1cde6d880422393b6cd9670f49063dda6f74`，`bounding_box.absolute=[0,43,832,1248]`。逐字 Prompt、脱敏请求、task ID、图层和无签名 URL 的元数据在 `assets/generated/evolink-paid/2026-09-25/laoda-layerize-attempt-01/`。该图层为 RGBA，Alpha 范围 `0–255`，四角均为 `0`。服务所用图层地址位于 `ark-acg-cn-beijing.tos-cn-beijing.volces.com`，下载工具仅允许该精确主机名及既有的 `files.evolink.ai`。

人物层的广告笔画仍被重绘，故其 RGB 不采用。`tools/build_art.py` 只提取该层 Alpha，放回 832×1248 基底后缩至原照片 720×1078，并与原照片 RGB 组合。对黑底初版预览的细蓝边，只在 EvoLink Alpha 轮廓的约 5 像素窄带内采用原 JPG 的最近内部人物像素，Alpha 完全不变；共有 `17,879/648,000` 个裁切图 RGB 像素被此边缘清理改变（2.76%）。胸前广告 ROI `(220,500,510,700)` 的 `58,000` 个 RGB 像素与参考 JPG **逐像素完全相同**，改变数为 `0`，因此「康师傅」「冰红茶」及英文和图形保持原字形、位置与颜色。只取原图 y=`0..899`，右下角 y≈1050 的水印没有进入成品。

按固定流程得 720×900 透明人物 PNG SHA-256 `5b5ce533da3abbf87868c8692b67ffe044822804cf8e2148f9f63637d82b6a6c`，再等比缩放并居中得 800×350 预览 SHA-256 `23328940a7c174acedaaa0613ea669ab486d073a9034d6f9870dd2904228eca3`，打包 DDS SHA-256 `a35c0431498c6b8511bed0604517ba629695edad86e0556c277019d0bbbbf071`。DDS 解码后的全部 RGBA 像素与预览一致。最终 Alpha 范围 `0–255`，四角 `0,0,0,0`，`A>127` 的 bbox `(264,15,535,350)`。黑、白、蓝灰三底合成图见 `evidence/static-rc1/`；已目视确认无矩形背景和蓝色轮廓。固定宽度的肖像保留头顶、双肩和胸前主广告；身体自然延伸到画布底边。

## P 语言静态检查

先按 `C:\workspace\open_kaishek` 使用说明运行既有 `stellaris-4.4.6` profile：生产肖像定义返回 `VALIDATED`、`syntaxDiagnostics=0`、`semanticDiagnostics=0`；描述符返回 `PARSED`、零诊断、`roundTrip=true`。**首次实机准备被版本锁拦下：**本机游戏已变为 `Cygnus v4.5.1 (358e)`，EXE SHA-256 `6fe06709f265e726722dc23f617c5fc4e5557629e2d43fe312016aba547c83e4`，而隔离工具仍锁定 4.4.6。实测 4.5.1 的原版合成女王肖像定义 SHA-256 `9a2ccd43d297112176092e62a9e488b63a8ca271915d028b84e14491724fee18`，与 4.4.6 基线完全相同。

已在 `open_kaishek` 新增只覆盖该文件的 `stellaris-4.5.1` 静态 profile，工具提交 `dbe1c1b` 已推送。新增测试、既有回归及 `python tools/run_static_acceptance.py` 全仓库离线检查通过；重建 CLI 对本 Mod 生产肖像文件返回 `VALIDATED`、0 语法和语义诊断，并报告 profile 的游戏指纹及 `runtime=UNSUPPORTED`。当前 Mod `supported_version` 改为 `4.5.*`，仍只含描述符、肖像定义和 DDS。下文记录第一次实机暴露的编码问题及修复后的正式验收。

第一次 4.5.1 隔离运行 `20260925T131514Z` 的 `error.log` 报 `portraits.cpp:963 Unexpected token: ﻿`，后续 `cetana_*` 键均无法找到。生产肖像文件实际以 `EF BB BF` 开头；旧静态 profile 误判为通过。游戏进程正常退出，但本次 R1/R3 失败，不可把 Steam 界面截图作为游戏画面证据。先在 `open_kaishek` 补上两个 Stellaris 肖像 profile 的 BOM 拒绝逻辑，新增 CLI 冒烟检查；全仓库离线静态验收通过，直接检测该有 BOM 文件返回 `INVALID`、诊断码 `STELLARIS_PORTRAIT_UTF8_BOM`，工具修复提交 `32d0ab4` 已推送。随后本 Mod 肖像文件以 UTF-8 无 BOM 重写，生产文件复测返回 `VALIDATED`，0 语法和语义诊断；描述符解析也为 0 诊断。修复后用于实机的生产 `mod/` 树 SHA-256 为 `3570b2e5a721b44f9e3f86e77e0a9cef09a625daff173481be96ee91ac5d4b1d`。

## 简体中文 4.5.1 实机结果

隔离用户目录运行 `20260925T132247Z` 只启用了本 Mod，使用已冻结的合成女王危机对话存档（SHA-256 `3154d57be832717584a0a6123f8e17254594454dd15e37edc2a7e530b7edeb52`）。4.4.6 种子在 4.5.1 成功载入，`风暴将至` 对话框显示新人物及其橙黄球衣，胸前「康师傅」「冰红茶」「ICE TEA」与原图一致，蓝底、水印和画布矩形均不可见。实际游戏 GPU 画面经 Steam F12 取得，原始截图见 `evidence/portrait-acceptance-rc1/cetana-dialogue.jpg`。本机 `ImageGrab` 返回旧 Steam 画面，Win32 PrintWindow 为黑屏，均未用作实机证据。首轮 `error.log` 只有缺失的既有 Workshop 订阅路径警告，没有肖像定义、DDS 或新资源错误；归档为 `first-run-error.log`。因此 R1、R3 通过。

对话未关闭时在 4.5.1 保存，生成存档 `laoda_rc1_45laoda_rc1_450.01.05.sav`，1,393,786 字节，SHA-256 `8a667c2149713c79f7b5956c49d3f035c774b2fceefe093f4ce271324ef877e8`；文件内含 `synth_queen_happened` 与 `cetana_mammalian`。退出游戏进程后用同一隔离用户目录重新启动，载入这份新存档，对话框仍显示同一人物和广告、无矩形边界。实际 F12 截图见 `after-restart.jpg`，重启运行日志 `after-restart-error.log` 同样没有肖像或 DDS 错误；存档 SHA-256 未变，游戏进程正常退出。因此 R5 通过。

R2（基础 `synth_queen` 肖像独立界面）和 R4（有效结局上下文中的 `cetana_empty` 切换）本轮**未观察到，仍为未验收**。其余九个映射键只完成静态覆盖与引用检查，不能冒称逐键实机通过。没有新增本地化；其他语言运行时不在范围内。本候选版的肖像静态、R1/R3/R5 均已通过，但尚不宣称整个 Mod 的全部预定实机场景验收完成。
