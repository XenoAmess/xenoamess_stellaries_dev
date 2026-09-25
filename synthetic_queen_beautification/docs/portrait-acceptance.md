# `0.1.0-rc.1` 人物肖像制作与验收记录

日期：2026-09-25。基线：Steam Stellaris `Pegasus v4.4.6 (fdde)`，`stellaris.exe` SHA-256 `bc451c72d9654c8901f1bb0bee1dd78d76f415465c2fbf746e9f98ade333173a`。本报告只对应人物肖像阶段。

## 输入、生成与构建

| 文件 | 尺寸/格式 | SHA-256 |
| --- | --- | --- |
| `assets/reference/cetana-reference.jpg` | 1536×1024 JPG，用户三视图 | `5cf0fbb85d01a0125c6ab07425481bbadde9ebec5166d28e4c1a8c97179f7d86` |
| `assets/generated/cetana-portrait-opaque-v1.png` | 1896×830 RGB，内置图片生成工具成图 | `ed268792522a368c53f5dcf3cbf97ca346a6ee19178af9dec9a60cfb4395afa2` |
| `assets/generated/cetana-portrait-800x350.png` | 800×350 RGB，构建预览 | `97e03df1a5bab01329f66d4eb24600d88f2983ce6f52ec2a7f9403836b5debb3` |
| `mod/gfx/models/portraits/xenoamess_cetana_portrait.dds` | 800×350 RGBA，未压缩 BGRA | `6a9b2e569c64e78e260b4ae8c15fefa0805ad4976500f234989f360ac9f5ef99` |

生成时的完整提示词见 `assets/prompts/cetana-static-v1.txt`。人物保留参考图的浅色脸、金眼、机械角冠、金色光环和黑金躯体。曾尝试按原版 UV atlas 生成，但片区错位且把棋盘格画进 RGB；失败图保存在 `evidence/rejected-uv-atlas-attempt-01.png`，没有进入 `mod/`。透明半身图和透明背景提取尝试也没有得到真实 alpha，因此当前成品使用不透明深色背景。

运行 `py synthetic_queen_beautification/tools/build_art.py` 两次均得到表中的相同预览与 DDS 哈希。Pillow 能将 DDS 解码为 800×350 RGBA，逐像素转换到 RGB 后与构建预览完全一致，左上角 alpha 为 255。经目视检查，新图是单人横向半身肖像，头冠和光环位于画布内，无可见棋盘格、文字或水印。

## 静态和 P 语言检查

- 原版 `gfx/portraits/portraits/21_portraits_cybernetics_synthqueen.txt` SHA-256 为 `9A2CCD43D297112176092E62A9E488B63A8CA271915D028B84E14491724FEE18`。逐项提取原版和 Mod 的顶层肖像键，顺序和数量均相同：`synth_queen`、`cetana_mammalian`、`cetana_reptilian`、`cetana_aquatic`、`cetana_lithoid`、`cetana_plantoid`、`cetana_molluscoid`、`cetana_avian`、`cetana_empty`、`cetana_robot`。每键均指向存在的新 DDS，保留 `tox_portrait_01` 声音。Mod 包仅含描述符、此定义文件和 DDS，树哈希 `a2096ec3cc1c246c89b20f3d4332fd629a104019d509739c28282f92a6b7641e`。
- `VERSION` 和 `descriptor.mod` 均为 `0.1.0-rc.1`，changelog 同步；描述符经 `open_kaishek parse` 返回 `PARSED`、0 diagnostics、`roundTrip=true`。
- `C:\workspace\open_kaishek` 原先没有 Stellaris 肖像目录的语义规则。按本仓库规则先在该工具仓库补充 `gfx/portraits/portraits/21_portraits_cybernetics_synthqueen.txt` 的受限配置和负例测试，模块测试及全量静态验收通过，工具改动已提交并推送为 `8129c35`。随后对本 Mod 生产文件运行 `validate --profile stellaris-4.4.6`，返回 `VALIDATED`、`syntaxDiagnostics=0`、`semanticDiagnostics=0`。因此本阶段 **P 语言静态校验通过**。
- 本轮实机验收结束后再次对同一生产肖像文件运行上述 `validate` 命令，仍返回 `VALIDATED`、0 语法诊断及 0 语义诊断；本轮没有改动生产 Mod 文件。

## 简体中文实机检查

使用 `tools/runtime_acceptance.py` 创建隔离用户目录，运行 ID 为 `20260925T062216Z`，语言 `l_simp_chinese`，启用 Mod 列表仅包含本地候选包。程序于 UTC 06:22:22 启动，进程 PID 1756，`game.log` 报告 `Pegasus v4.4.6`，原版数据与肖像数据库开始初始化。程序的可见窗口始终为黑色，06:22:48、06:23:35、06:24:35 的桌面截图均未出现主菜单或可观察的人物场景；06:25:42 正常关闭进程。原始运行清单、截图和日志留在本地 `evidence/runtime/20260925T062216Z/`，该大体积临时目录不入 Git。

`error.log` 只有本机 Steam 已订阅但未下载的其他 Workshop 物品路径缺失记录；没有本 Mod 文件名相关报错。该次黑色窗口无法证明本 Mod 实际渲染正确；后续运行结果见下节。

### 2026-09-25 显示修复与危机对话复测

按 [测试策略](test-strategy.md)在启动完成后发送物理 `Alt+Enter` 扫描码，主菜单恢复显示。隔离运行 `20260925T065140Z` 仅启用本 Mod，以人类联合国进入 2200.01.01 并保存种子档；游戏显示 `Pegasus v4.4.6 (fdde)`。随后在隔离运行 `20260925T070653Z` 中载入该档，按运行清单于 2200.01.02 执行原版 `event crisis.8005`，于 2200.01.04 执行 `event crisis.8039`，点击原版选项进入 `crisis.8040` 对话。种子档 SHA-256 为 `2a51d2f11c003eda43c1a3a752bcc9720954bf2f80372098a550fbfd618e710e`；两次运行的 Mod 树哈希均为 `a2096ec3cc1c246c89b20f3d4332fd629a104019d509739c28282f92a6b7641e`。危机场景存档 `2200.01.05.sav` SHA-256 为 `3154d57be832717584a0a6123f8e17254594454dd15e37edc2a7e530b7edeb52`，检查结果含 `synth_queen_happened` 和 `synth_queen_country_global`，说明原版危机国家目标已生成。

原始运行数据保存在本地 `evidence/runtime/20260925T065140Z/` 与 `evidence/runtime/20260925T070653Z/`；可审阅副本包括 [种子运行清单](../evidence/portrait-acceptance-20260925/seed-run-manifest.json)、[简体中文主菜单与版本截图](../evidence/portrait-acceptance-20260925/main-menu.png)、[危机运行清单](../evidence/portrait-acceptance-20260925/manifest.json)、[首次对话截图](../evidence/portrait-acceptance-20260925/cetana-first-speech.png)、[同进程重载截图](../evidence/portrait-acceptance-20260925/cetana-after-reload.png)、[进程重启后重载截图](../evidence/portrait-acceptance-20260925/cetana-after-process-restart-loaded.png)、[重启进程记录](../evidence/portrait-acceptance-20260925/restart-process.json)、[对话完成截图](../evidence/portrait-acceptance-20260925/post-first-speech.png)、[联系人截图](../evidence/portrait-acceptance-20260925/cetana-contact.png)、[外交无回应截图](../evidence/portrait-acceptance-20260925/cetana-diplomacy.png)、[存档检查](../evidence/portrait-acceptance-20260925/save-inspection-2200.01.05.json)及 [重启后 error.log](../evidence/portrait-acceptance-20260925/error.log)。

| 场景 | 结果 | 证据与限制 |
| --- | --- | --- |
| R1 启动与装载 | 通过 | 简体中文主菜单、新游戏和载入均可见；候选包是唯一启用 Mod；日志没有本肖像文件或 DDS 相关报错。 |
| R2 `synth_queen` 基础肖像 | 待实机观察 | 存档确认危机国家已生成，联系人列表出现“塞塔娜”；点击外交只得到“没有回应”，未进入可观察基础肖像的物种或领袖界面。 |
| R3 `get_cetana_face` 外交对话 | 功能通过，视觉不通过 | 人类联合国视角的原版对话实际显示新人物，头冠和光环完整；但 800×350 不透明深色画布在对话框左上形成明显矩形边界，未达到美术方案的背景融入标准。其他七类玩家物种只完成静态键映射，尚未逐一实机截图。 |
| R4 `cetana_empty` 后期切换 | 待实机观察 | 尚未推进至后期领袖切换场景。 |
| R5 存档重载 | 通过 | 在首次对话中保存，同进程重载可见相同肖像；完全关闭 PID 14464 后重新启动 PID 17632，载入同一 `2200.01.05.sav`，原对话和新肖像再次出现。重启后复算存档 SHA-256 仍为 `3154d57be832717584a0a6123f8e17254594454dd15e37edc2a7e530b7edeb52`，日志无候选肖像相关新增错误。 |
| R6 单独与灰风并用 | 部分完成 | 单独启用本 Mod 已运行；尚未完成两 Mod 同时启用。 |

对话脚本可正常前进至结束；没有发现资源缺失黑块或严重人物裁切。首次危机运行的 `error.log` 曾记录 `councilor_trait_not_allowed`，调用位置为原版 `02_machine_age_effects.txt:896–1055`，出现在把危机提前到 2200 年的测试夹具中；它不能据此判为肖像 Mod 错误，也不能据此证明自然年份的危机流程无误。游戏重启覆盖了同一用户目录中的原始日志，仓库归档的是重启后的日志，故原始报错只保留上述现场摘录。第二个进程于 UTC 08:37:32 正常关闭，[停止记录](../evidence/portrait-acceptance-20260925/restart-stop.json)显示未强制终止且没有留下运行中的 Stellaris。**本候选包 P 语言静态校验通过，简体中文实机只完成上述部分场景；R3 的明显矩形背景使人物肖像美术验收不通过。** 不得标记为正式验收完成或发布。

## 已知限制与下一步

当前 10 个原版肖像键共用一张静态图，原版动画和依玩家物种变化的面部细节不再出现。深色不透明背景已在实机中形成明显矩形边界，需修订美术方案、制作真实透明背景并重新运行人物场景矩阵。覆盖原版肖像定义文件可能与修改同一文件的其他 Mod 冲突。剧情插画、对话背景、旗帜和奖励图标仍为原版。
