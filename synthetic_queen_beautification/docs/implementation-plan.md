# 合成女王美化独立 Mod 实施计划

## 目标与阶段

建立可独立安装的合成女王（Cetana）图片替换 Mod，工作目录为 `synthetic_queen_beautification/`。用户指定的三视图先用于**人物立绘替换阶段**：让原版 `synth_queen` 和 9 个 `cetana_*` 肖像键呈现同一张新人物图。原版图片的完整调查见 [资源清单](asset-audit.md)，具体美术方案见 [参考图方案](reference-art-plan.md)。

第二阶段再制作资源清单中的 2 张事件图、1 张对话背景和 3 张旗帜；剧情奖励图标按实机画面决定是否纳入。人物阶段不能报告成全套图片已完成。通用 UI、银河地图和 3D 材质不在默认范围。

当前候选版本为 `0.1.0-rc.1`，版本以根目录 `VERSION` 为唯一来源，`mod/descriptor.mod` 与其相同，游戏兼容范围由 `supported_version="4.4.*"` 表示。当前版本只供开发和验收；没有用户另行要求时，不创建或上传 Steam Workshop 物品。

## 人物阶段设计

1. 冻结 Stellaris `Pegasus v4.4.6 (fdde)` 的原版路径、尺寸、引用和肖像定义哈希。原版资源只读，不将游戏版权贴图提交到本仓库。
2. 用户三视图存入 `assets/reference/`；使用图片生成能力制作单人、正面、横向肖像，保存提示词与源图。仅对选定源图进行确定性尺寸及 DDS 格式转换。
3. 原版 10 张肖像 DDS 是动画网格的 UV atlas，普通人物画不能直接覆盖。人物阶段改用一张 800×350 深色不透明静态 DDS，覆盖原版 `gfx/portraits/portraits/21_portraits_cybernetics_synthqueen.txt`，使 10 个原版键都用 `texturefile` 指向它，保留 `greeting_sound`。不改危机事件、数值、触发器和声音。
4. 覆盖定义文件需与原版结构化比较，并绑定原版文件哈希。每个键由原版的 `entity`、`character_textures`、服饰/附加件选择器和镜头位置缩放参数，改为 `texturefile` 与保留的问候声音。此方案会失去原版人物动画和因玩家物种变化的细微面部差异；深色矩形背景与外交房间的衔接需实机检查。修改同一原版定义文件的其他 Mod 可能冲突。
5. 先用 `C:\workspace\open_kaishek` 校验 P 语言文件，再执行静态图像、引用和版本检查。简体中文实机验收重点是 `synth_queen`、一种 `cetana_*`、外交对话、后期 `cetana_empty`、存档重载及与灰风 Mod 并用。不能仅凭生成图预览宣称 Mod 已实机验收。

## 后续图片阶段

事件图各按 450×150 制作，并检查普通及启蒙分支的两个固定 zoom 视口；对话背景按 828×358 制作；旗帜分别按 256×256、256×256 和 24×24 制作。优先以原版同路径 DDS 替换，避免复制大型危机脚本。发现额外引用或裁切问题时，先更新文档和清单，再调整素材。

## 目录

```text
synthetic_queen_beautification/
├─ docs/                 调查、方案、测试策略、验收记录
├─ assets/reference/     用户三视图
├─ assets/generated/     图片生成源图及构建预览
├─ assets/prompts/       本次生成提示词
├─ tools/                确定性图片构建与实机验收入口
├─ mod/                  独立可安装内容包
├─ evidence/             检查记录，不进入 mod/
├─ VERSION
└─ CHANGELOG.md
```
