# 迭代 2 Stellaris 实机验收报告

## 结论

候选 `1.2.0-rc.1` 在 Stellaris `Pegasus v4.4.6`、简体中文、仅启用本 Mod 的隔离环境中通过发布门禁，可以提升为正式版 `1.2.0`。

其他 9 种官方语言静态校验通过，运行时不在范围内。

## 运行身份

| 项目 | 值 |
| --- | --- |
| Run ID | `20260910T010503Z` |
| 游戏校验和 | Modded `6cd8` |
| 候选文件数 | 15 |
| 最终存档 | `i2_runtime_final.sav` |
| 最终存档 SHA-256 | `a691f45553ccb79b02c333f9b9cbf61809e37ac3cb391257685d3f9d9380094b` |

本地证据保存在 `_runtime/20260910T010503Z`，隔离 userdir 为 `C:\Users\1\AppData\Local\xenoamess_stellaries_dev\runs\20260910T010503Z`。

## 核心断言

| 场景 | 基线 | 执行 | 最终值 | 结果 |
| --- | --- | --- | --- | --- |
| 居住站能源容量 | 反应堆 `0/3` | 计划 09 两次 | `0/7` | 精确 `+4`，通过 |
| 居住站采矿容量 | 航天采矿湾 `0/10` | 计划 10 一次 | `0/12` | 精确 `+2`，通过 |
| 居住站科研与总槽位 | 研究 `0/4`、总槽 `2/9` | 计划 04/05/06 各一次 | 研究 `0/10`、总槽 `2/21` | 每次分别 `+2/+2`，通过 |
| 普通行星反向范围 | 总槽 `2/15` | 物理研究 deposit 一次 | 总槽仍为 `2/15` | habitat 修正未泄漏，通过 |
| 人口发展 | 无对应 deposit | 计划 14 两次 | 存档含 2 个 deposit | 每次住房 `+600`、增长 `+10%`、机械组装 `+10%`，通过 |
| 保存与重载 | 上述最终状态 | 保存并载入 | 居住站仍为 `0/7`、`0/12`、`0/10`、`2/21` | 通过 |

计划 14 的两个百分比 modifier 由游戏在简体中文控制台效果说明中实际解析；它们不会为基础值为零的殖民地凭空创建自然增长或机械组装通道。本轮选用有机体居住站，不另行启动机械体与双通道起源，因此验收范围是 modifier 生效、重复叠加及存档保持，不声明各起源 UI 来源面板的独立覆盖。

## 存档与可复验合同

最终存档解包后，目标 token 计数为：计划 09 deposit `2`、计划 10 deposit `1`、物理研究 deposit `2`（居住站与普通行星各一个）、社会研究 `1`、工程研究 `1`、人口发展 `2`。计数与验收操作完全一致。

回归夹具以 `fixtures/iteration-2/mod-contract.json` 冻结脚本合同，以 `fixtures/iteration-2/scenarios.json` 冻结本次运行状态、证据路径、数值和存档 token。后续版本应复用同一中文矩阵；非中文只做静态本地化检查。

## 证据索引

| 文件 | SHA-256 | 证明内容 |
| --- | --- | --- |
| `manifest.json` | `37cab3a8fe4adcb170c34dd5f4539d73a83335f306b01cc6adfee9da67ca8b08` | 隔离环境、唯一启用 Mod 与候选输入 |
| `i2-plan14-repeat-console.png` | `7c34da0e45fc59bc0e0b2009aecf7a05a58222b7ead93e0a19e2ec56dccb49aa` | 计划 14 第二次执行的中文效果说明 |
| `i2-habitat-all-effects-final.png` | `1041ca8adeeef842880820fa57b940efb5a69111dd5ac7f90c29ede8a3fc2256` | 居住站全部容量效果与重复叠加 |
| `i2-normal-capital-physics-console.png` | `51fa30293ab09d5888d4800253b2ed681b85b9b123bde5e8f51725890d6f1529` | 普通行星反向范围 |
| `i2-reload-habitat-verified.png` | `62ffdec4de30dc78c166f4cd36a0201208913d95358e4d606ef0cad884c9e958` | 重载后效果保持 |

## 日志审计与限制

fresh `error.log` 中两条 `Wrong scope for effect 'add_deposit'` 来自验收夹具早期一次缺少行星 scope 的探索命令；该命令未修改游戏状态，普通行星场景随后用显式 `capital_scope` 重跑。启动时的缺失 Workshop 文件记录来自隔离 userdir 中未启用的旧描述符。载入时游戏报告清理 1 个无效 deposit，但目标 deposit 计数及全部 UI 数值在重载后保持，没有发现候选 Mod 脚本可归因的解析或加载错误。

结论只覆盖 Stellaris 4.4.6、简体中文和仅启用本 Mod 的环境；第三方 UI Mod 组合及其他 9 种语言运行时不在范围内。

## 发布前静态门禁

- `open_kaishek` 全量 Maven 构建通过；Stellaris 4.4.6 profile 对生产 decisions、deposits、scripted trigger 均返回 `VALIDATED`，语法和语义诊断均为 0。
- 本仓库 `py -m unittest discover -s tests -v` 为 `33/33` 通过，`git diff --check` 通过。
- 正式 v1.2.0 Mod 树为 15 个文件，SHA-256 为 `294f9a9834f2aef8cac597a4fc2cae7d7cff734abefda2ae965f38d7f872f1f9`；工坊 BBCode 为 7,973 字节，未超过 8,000 字节门禁。
