# `0.1.0-rc.2` 透明肖像修复与验收记录

日期：2026-09-25。目标是消除 [`0.1.0-rc.1` 验收记录](portrait-acceptance.md)中实机确认的不透明矩形背景。本轮只验收合成女王 Mod 单独启用，矩阵见 [测试策略](test-strategy.md)。

## EvoLink 请求与首次下载观察

使用仓库公开的用户三视图作为唯一身份参考，按 [透明肖像方案](reference-art-plan.md)向 EvoLink `gpt-image-2` 提交 `16:9`、`2K`、`high`、`background=transparent`、PNG、`n=1` 请求。首次任务 ID 为 `task-unified-1790326870-9581kwmf`；逐字 Prompt、脱敏请求和任务 ID 保存于 `assets/generated/evolink-paid/2026-09-25/cetana-portrait-attempt-01/`。官方参数说明见 [EvoLink GPT Image 2 API](https://evolink.ai/gpt-image-2)。

该任务已返回 `completed`，结果由 `files.evolink.ai` 提供。标准库 `urllib.request.urlopen` 下载结果时返回 HTTP 403；使用已安装的 `requests` 客户端 GET 同一结果 URL 返回 HTTP 200、`image/png`、6,054,016 字节。下载工具改为 `requests` 后再保存原图并检查真实 Alpha。临时结果 URL、API Key、完整 API 响应和 Authorization 头不得写入仓库或日志。

首次原图为 2736×1536 RGBA，Alpha extrema 为 `0–253`，四角 Alpha 为 `[4, 8, 11, 21]`，`A>16` 的包围盒覆盖全画布，`A>127` 的包围盒为 `(38, 13, 2723, 1536)`。顶对齐裁切至目标比例并以 SourceOver 叠到外交蓝灰底后，人物两侧仍有显著的暗色雾幕和方形边界；光环与角冠也过于靠近顶端。**attempt-01 淘汰**，不得进入 Mod。下一次请求只收紧对象范围和构图：禁止引用图的深炭色场景与任何人物外的色块、雾幕或光晕，缩小人物以保留头顶安全边；其余 API 参数和身份参考不变。

## attempt-02 静态候选

第二次任务 ID 为 `task-unified-1790327549-nfmkbuu8`，保持相同公开 API 参数与身份参考，只使用修订后的逐字 Prompt `assets/prompts/cetana-transparent-v3.txt`。原图 `assets/generated/evolink-paid/2026-09-25/cetana-portrait-attempt-02/original.png` 为 2736×1536 RGBA，SHA-256 `2de5a76ac2974404381be70ec7c4ca9f363f3fceeb93e827c6ffac261c8d5591`。Alpha extrema `0–254`，四角 `[0, 0, 0, 0]`，`A>0` bbox `(43, 3, 2704, 1536)`，`A>16` bbox `(763, 18, 1971, 1536)`，`A>127` bbox `(764, 18, 1970, 1536)`。极低 Alpha 边缘宽于主体，但没有 attempt-01 那种高不透明度的全画幅幕布。

按固定裁切框 `(0, 0, 2736, 1197)` 顶对齐裁切，再以 Pillow 12.3.0 的 Lanczos 缩放到 800×350，得到 `candidate-800x350.png`，SHA-256 `5c873d7a43c725976b7315b3a4b0c50f2676ccbef3ab4509b039be5658cb0a9a`。候选为 RGBA，Alpha extrema `0–255`，四角仍全为 0，`A>0/16/127` bbox 分别是 `(183, 3, 712, 350)`、`(230, 5, 570, 350)`、`(230, 6, 569, 350)`。黑、白和外交蓝灰三底 SourceOver 均显示单一人物、完整光环和角冠，没有可见矩形边界、暗幕、场景残留或额外人物；头冠上方保留约 5–6 像素安全边。静态候选通过，并已完成下述 DDS 构建与实机检查。

## 构建与静态检查

- `tools/build_art.py` 只接受上述原图的精确 SHA-256、2736×1536 RGBA 模式与固定裁切框；重复构建两次均得到相同的 800×350 预览哈希 `5c873d7a43c725976b7315b3a4b0c50f2676ccbef3ab4509b039be5658cb0a9a` 和 DDS 哈希 `5225d045670268844f539ef1ec21eec094149efcaf796af1667d82145a4732d4`。DDS 为 800×350 未压缩 BGRA8、straight alpha；Pillow 解码后 RGBA 与预览逐像素一致，四角 Alpha 均为 0。
- 生产 Mod 仍仅有 `descriptor.mod`、10 键肖像定义和新 DDS，树哈希 `5b11638e90815b7487335f272ec1540fd4fa07057d818275803483edb41811ba`。10 个键及问候声音未变，均指向新 DDS。`VERSION` 与描述符均为 `0.1.0-rc.2`，描述符经 `open_kaishek parse` 返回 `PARSED`、0 diagnostics、`roundTrip=true`。
- `C:\workspace\open_kaishek` 的 `validate --profile stellaris-4.4.6` 对生产肖像文件返回 `VALIDATED`、`syntaxDiagnostics=0`、`semanticDiagnostics=0`。因此 **P 语言静态校验通过**。

## 简体中文实机复测

隔离运行 `20260925T092342Z`，游戏为 Stellaris `Pegasus v4.4.6 (fdde)`，语言 `l_simp_chinese`，唯一启用 Mod 为本地 `0.1.0-rc.2`，Mod 树哈希与上文相同。载入上一轮冻结的 2200.01.05 危机对话存档，种子 SHA-256 `3154d57be832717584a0a6123f8e17254594454dd15e37edc2a7e530b7edeb52`。截图中女王面部、角冠、完整光环和胸甲正常显示；翻至第二页对话后保持一致。旧版图片曾在游戏人物面板之外形成一整块深色矩形；本版的人物轮廓外已能看到游戏原有背景与面板内容，**由素材画布造成的矩形边界消失**。游戏自带的人物面板仍有直角边框，这属于原有 UI。

在第二页对话中以 rc.2 保存 `rc2_cetana00.01.05.sav`，SHA-256 `c1dc1ac6ac6acbfb7d73b1619f7a565c45eb13f03c0c0e2d1218a8d105dde986`，存档检查含 `synth_queen_happened`、`synth_queen_country_global` 与 `cetana_mammalian`。先归档当前日志，再正常关闭 PID 9012，重新启动 PID 19420，载入这份新存档；原对话和透明肖像再次出现，存档哈希复算不变。第二次进程于 UTC 10:10:42 正常关闭。两次 `error.log` 均只有本机已订阅但未下载的 Workshop 物品路径缺失，没有候选肖像或 DDS 相关报错。

可审阅证据：[运行清单](../evidence/portrait-acceptance-rc2/manifest.json)、[首次对话截图](../evidence/portrait-acceptance-rc2/rc2-cetana-dialogue.png)、[第二页截图](../evidence/portrait-acceptance-rc2/rc2-cetana-second-response.png)、[进程重启后截图](../evidence/portrait-acceptance-rc2/rc2-after-restart.png)、[新存档检查](../evidence/portrait-acceptance-rc2/save-inspection-rc2_cetana00.01.05.json)、[首轮日志](../evidence/portrait-acceptance-rc2/first-run-error.log)、[重启日志](../evidence/portrait-acceptance-rc2/restart-error.log)。

## R2 与 R4 补测

R2 隔离运行 `20260925T102308Z` 从 rc.2 新存档载入，完成 `crisis.8040` 剩余对话；[最后一页](../evidence/portrait-acceptance-rc2/r2-final-dialogue.png)之后，[通讯列表](../evidence/portrait-acceptance-rc2/r2-cetana-contact.png)已列出“塞塔娜”。点击外交只得到[“没有回应”窗口](../evidence/portrait-acceptance-rc2/r2-no-response.png)，[所有物种界面](../evidence/portrait-acceptance-rc2/r2-species-list.png)也只有人类，未给出可独立观察 `synth_queen` 的条目。因此 R2 保持未验收；不能将危机对话所用 `cetana_mammalian` 当成基础肖像证据。[运行清单](../evidence/portrait-acceptance-rc2/r2-manifest.json)记录了单 Mod、中文和种子哈希；[日志](../evidence/portrait-acceptance-rc2/r2-error.log)未见新肖像报错，进程[正常退出](../evidence/portrait-acceptance-rc2/r2-stop.json)。

R4 隔离运行 `20260925T105305Z` 用同一 rc.2 存档，并在 `commands_at_date.txt` 中安排 `2200.01.06 = "event crisis.23005"`。原版 `events/machine_age_crisis_events.txt` 中该事件的 `immediate` 建立 `portrait="synth_queen"` 的物种及新领袖，再对该领袖执行 `change_leader_portrait = cetana_empty`；事件图片引用新国家领袖。2200.01.07 的[结局对话截图](../evidence/portrait-acceptance-rc2/r4-final-speech.png)可见本 Mod 新人物，头冠、光环和透明边缘无明显黑块或原版回落。但[错误日志](../evidence/portrait-acceptance-rc2/r4-error.log)在提前触发时同时出现 `councilor_trait_not_allowed`（原版事件第 14496 行）、`Failed to find portrait selector` 和无效领袖的 `species` 作用域切换；后两项不能仅凭截图排除与候选肖像定义的关系。归档的错误日志仅移除游戏输出的行尾空格及文件末尾空行，原文件留在隔离运行目录。因此此次只取得 **R4 视觉观察**，未能把原版晚期领袖状态判为运行时通过；也不能据此证明自然结局流程。[运行清单](../evidence/portrait-acceptance-rc2/r4-manifest.json)与[正常停止记录](../evidence/portrait-acceptance-rc2/r4-stop.json)保留了夹具边界。

| 场景 | 结果 | 说明 |
| --- | --- | --- |
| R1 启动及装载 | 通过 | 简体中文主菜单及新旧存档加载可见；日志无候选肖像报错。 |
| R2 `synth_queen` 基础肖像 | 未验收 | 危机国家已存在；完成首轮对话后，外交仍无回应，物种列表只有人类，未出现独立基础肖像。 |
| R3 `get_cetana_face` 外交对话 | 通过本次人物视角 | 人类联合国视角的对话已显示透明肖像，旧素材矩形边界消失；其余七种玩家物种的键映射通过静态检查，未逐一实机截图。 |
| R4 `cetana_empty` 后期切换 | 未完成 | 原版结局事件提前触发的视觉夹具显示新人物，但同时产生肖像选择器和领袖作用域错误；尚无可判定正常后期切换的证据。 |
| R5 存档重载 | 通过 | 用 rc.2 新保存，进程退出后重进并载入，人物仍正常显示。 |

**本轮矩形背景缺陷已修复并通过简体中文实机复测；整个肖像 Mod 仍因 R2 缺少独立场景证据、R4 夹具存在运行时错误而未完成全矩阵验收，也未发布。**
