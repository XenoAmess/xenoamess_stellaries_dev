# 屎山代码起源：机械主体物种特质预算修复

## 目标与范围

修复起源对主体机械物种的预算修正，使可用特质点数减少 6、可选特质上限增加 3。范围限于 `origin_shishan_code` 的物种预算修正键，以及相应静态、实机回归。机械智能和个体机械都必须受同一修正影响；有机帝国仍不可选择起源。

## 发现与依据

- Stellaris 4.5.1 原版 `common/technology/00_synthetic_dawn_tech.txt` 在同一科技中分别设置 `ROBOT_species_trait_points_add` 和 `MACHINE_species_trait_points_add`；两种键对应不同物种原型，不能互代。
- 原版 `common/governments/civics/00_origins.txt` 的 `origin_mechanists` 明确排除 `MACHINE` 主体物种，使用 `ROBOT_species_trait_points_add` 给其机器人附属物种增点。当前 Mod 起源却要求主体 `species_archetype = MACHINE`，因此它的预算修正应使用 `MACHINE_` 前缀。
- 简体中文创建界面：全新个体机械物种在普通起源下显示剩余特质点数 1、剩余可选特质数 5（Steam F12 `20260928001210_1.jpg`）；选择屎山代码后仍为 1、5（`20260928000717_1.jpg`）。这与目标的 −6、+3 不符。
- 同一创建流程证实民主政体的个体机械可选择本起源（`20260928000413_1.jpg`），人类肖像切换后起源不可选且“机械”要求为红色（`20260928000649_1.jpg`）。

## 修复设计

将起源修正中的 `ROBOT_species_trait_points_add = -6`、`ROBOT_species_trait_picks_add = 3` 分别改为 `MACHINE_species_trait_points_add = -6`、`MACHINE_species_trait_picks_add = 3`。不同时保留 `ROBOT_` 修正，以免附属机器人也被施加主体物种惩罚。保持 `trait_shishan_code` 的成本为 0、起源强制特质及选择限制不变。

## 验收标准

1. `open_kaishek` 解析和资源引用检查通过；静态核对起源预算键只使用 `MACHINE_`，数值分别为 −6、+3。
2. 在同一游戏版本与单 Mod 环境，创建界面对照普通起源与屎山代码起源的机械物种预算，或在开局后物种改造界面核对：修正分别相差 −6 点、+3 上限；界面缓存若不即时刷新，需重新进入编辑器或新开局核对，不把未刷新的数字误判为通过。
3. 个体机械、机械智能均可选且开局获得代码特质；有机物种不可选。记录 Steam F12 截图和 Mod `error.log`。

## 当前实施与检查

- 起源脚本已将两项预算修正改为 `MACHINE_` 前缀，未保留 `ROBOT_` 前缀。
- 修改后的仓库包运行 `C:\workspace\open_kaishek\tools\accept_stellaris_mod.py`：`PASS`，19/19 个脚本解析、13 个 DDS、164 个本地化键。首次误将 `--mod` 指到内部 `mod` 目录导致 `MOD_METADATA_MISSING`，改为带 `VERSION` 的 Mod 根目录后通过；这不是脚本错误。
- 原始个体机械编辑器基线在全新普通起源和修复前屎山代码起源均显示 1 点、5 上限。不能用单张创建界面截图认定新前缀已生效，仍须重新启动游戏及运行时复核。
- 已在仅启用更新后 Mod 的全新游戏进程中复核：同一全新个体机械创建流程选中本起源后，特质面板显示剩余点数 `-5`、剩余可选数 `8`，恰好相对普通起源的 `1`、`5` 分别变化 `-6`、`+3`。Steam F12 截图 `20260928002806_1.jpg`；该实例校验和 `a17f`。负点数使编辑器提示必须再选负面特质，这符合挑战性起源的预算设计。
