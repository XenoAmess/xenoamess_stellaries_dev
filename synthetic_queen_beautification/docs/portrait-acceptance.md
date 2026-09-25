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

## 简体中文实机检查

使用 `tools/runtime_acceptance.py` 创建隔离用户目录，运行 ID 为 `20260925T062216Z`，语言 `l_simp_chinese`，启用 Mod 列表仅包含本地候选包。程序于 UTC 06:22:22 启动，进程 PID 1756，`game.log` 报告 `Pegasus v4.4.6`，原版数据与肖像数据库开始初始化。程序的可见窗口始终为黑色，06:22:48、06:23:35、06:24:35 的桌面截图均未出现主菜单或可观察的人物场景；06:25:42 正常关闭进程。原始运行清单、截图和日志留在本地 `evidence/runtime/20260925T062216Z/`，该大体积临时目录不入 Git。

`error.log` 只有本机 Steam 已订阅但未下载的其他 Workshop 物品路径缺失记录；没有本 Mod 文件名相关报错。不过黑色窗口无法证明本 Mod 实际渲染正确，也无法把 R1 启动与装载判为通过。**简体中文实机验收未完成**；R1–R6 的人物画面、裁切、存档重载和与灰风并用均待观察。此候选包不得标记为正式验收完成或发布。

## 已知限制与下一步

当前 10 个原版肖像键共用一张静态图，原版动画和依玩家物种变化的面部细节不再出现。不透明背景可能遮住外交房间。覆盖原版肖像定义文件可能与修改同一文件的其他 Mod 冲突。待游戏能正常显示后，应按 [测试策略](test-strategy.md)继续简体中文实机矩阵；若背景或人物裁切不可接受，先修订美术方案与文档再迭代。剧情插画、对话背景、旗帜和奖励图标仍为原版。
