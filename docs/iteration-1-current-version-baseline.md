# 迭代 1：当前版本实机基线与回归夹具记录

## 状态

- 状态：进行中
- 开始日期：2026-09-06
- 目标：先验证 Workshop 当前版本在 Stellaris 实机中的行为，再据此设计可重复的回归夹具。
- 待完成：`open_kaishek` 静态门禁、隔离 profile 启动、普通帝国运行时场景、格式塔回归场景、存档重载和最终夹具冻结。

## 1. 固定输入

### 游戏

- 安装：Steam，App ID `281990`
- 游戏版本：Pegasus `v4.4.6 (fdde)`
- Steam build ID：`24109497`
- 可执行文件：`D:\Program Files (x86)\Steam\steamapps\common\Stellaris\stellaris.exe`
- 桌面：`2560x1440`

版本号来自本机 `launcher-settings.json` 和 Steam `appmanifest_281990.acf`，不是从 Workshop 描述推断。

### Mod

- Workshop ID：`3710613857`
- Workshop manifest：`3603172186605630693`
- Workshop 记录大小：`625141` 字节
- 仓库副本：`vivhite_infinite_positions/mod`
- `descriptor.mod`：`version="4.3"`、`supported_version="*"`

固定文件清单：

| 相对路径 | 字节 | SHA-256 |
| --- | ---: | --- |
| `common/decisions/workplace.txt` | 3902 | `1628c0e3656e1fb7d76e847832bc7d3795e68107c0fa012511d51d007abd3d71` |
| `common/deposits/extend_workplace.txt` | 12714 | `7dc9870ae5587e31ebd9ca44cc967aad81a2db617984015ce0b3cf5c4a4c8559` |
| `descriptor.mod` | 127 | `74a5ee537c467cb3be868d86841b31758447df21def8a3bb7a93047613d403c9` |
| `localisation/more_workplace_l_simp_chinese.yml` | 8849 | `2c6fc14c1185a4f9d4e68f62d5a78ea31b33196a0a6fa403f66161670e956966` |
| `thumbnail.png` | 599549 | `984d02b2ec7e5215748ef5defb90f862c3fcecd59cd8c21e2a58636a790e6afe` |

## 2. 启动隔离原则

复用 `D:\workspace\ck3_eternal_recurrence` 已经实机验证过的 Paradox 启动器共性经验：

1. 直启游戏可执行文件并传入 `-userdir=<隔离目录>`，避免覆盖真实玩家 profile。
2. 隔离目录显式提供 `mod` 外层描述符和 `dlc_load.json`，确保只启用待测 mod。
3. 每轮清空隔离日志，只把本轮新日志作为证据。
4. 固定游戏版本、mod 文件清单、启用顺序、语言、分辨率和启动参数。
5. 截图/OCR 只证明玩家可见 UI；引擎加载和脚本错误同时由本轮日志反证。
6. 退出后确认 Stellaris 进程树归零，并保留报告、日志、截图和输入指纹。

以上原则是 Paradox 启动与证据保全的共性知识，Stellaris 的具体文件格式和 UI 坐标仍须本轮实测后记录。

## 3. 当前脚本静态观察

### 决议入口

`common/decisions/workplace.txt` 定义 13 个行星决议。当前共同结构为：

- `owned_planets_only = yes`
- `enactment_time = 180`
- `resources` 消耗 `minerals = 1000`
- `ai_weight = { weight = 0 }`
- 执行效果为 `add_deposit = mod_extend_*_workplace`

### 地块效果

`common/deposits/extend_workplace.txt` 定义 13 个对应地块：

- 普通政体与格式塔政体通过 `triggered_planet_modifier` 分流岗位。
- 城市地块只为非格式塔提供政治家岗位；其余主要地块对格式塔提供对应子个体岗位。
- 地块 `potential = { always = no }`、`drop_weight = { weight = 0 }`，设计意图是只通过决议添加，而不作为自然地块生成。
- `should_swap_deposit_on_terraforming = no` 表明脚本试图阻止改造时交换地块，但是否能阻止理想城转换删除地块仍以实机为准。

### 已发现的需求线索

简体中文本地化仍包含：

- `decision_extend_workplace_expand`
- `decision_extend_workplace_collapse`

但当前决议脚本中没有这两个定义，只有 13 个直接展示的岗位决议。这与评论区“没有折叠”及作者“不做折叠”的最新状态一致；本轮应把“13 项是否全部直接占据菜单”冻结为视觉基线。

## 4. `open_kaishek` 当前能力边界

`open_kaishek` CLI 当前登记的语义 profile 只有：

- `ck3-1.19.0.6`
- `ck3-1.19.0.6-zg361`

因此它可以先为本 mod 提供通用 P 语言 lossless parser/corpus 门禁，但当前不能据此宣称 Stellaris 4.4.6 的 opcode、scope、目录 schema 或运行时语义已经通过验证。

后续处理：

1. 先运行通用 parser/corpus，确认当前文件能被 P 语言前端读取。
2. 把缺少 Stellaris profile 视为工具能力缺口；补充与本次 mod 验收范围相称的 Stellaris 4.4.6 静态 profile/夹具并推送工具仓库。
3. 即使静态工具全部通过，也必须继续 Stellaris 实机测试。

## 5. 当前风险假设

| 风险 | 当前证据 | 需要的实机反证 |
| --- | --- | --- |
| 4.3 mod 在 4.4.6 上发生语义漂移 | 描述符版本旧，但 `supported_version="*"` 会隐藏启动器版本警告 | 加载日志、决议可见性、执行结果 |
| 决议菜单过长 | 13 个直接决议；折叠键无脚本定义 | 行星决议界面截图与 OCR |
| 格式塔岗位键已变化或无人可就业 | 历史评论曾报告蜂巢科研/行政岗位问题 | 蜂巢/机械实机岗位面板与错误日志 |
| 地块可重复添加行为不明确 | 决议没有显式 `allow`/重复限制 | 连续执行同一决议、存档重载后计数 |
| 仅有简体中文 | 只有 `l_simp_chinese` 文件 | 英文环境缺失键基线 |

## 6. 证据等级

- `STATIC-GREEN`：P 语言解析、目录/引用/profile 检查通过；不代表游戏效果正确。
- `LOAD-GREEN`：精确单 mod 在隔离 profile 中进入主菜单，且本 mod 没有加载错误；不代表玩法正确。
- `SCENARIO-GREEN`：指定政体和行星场景中，玩家可见效果、日志和存档重载均满足断言。
- `RED`：出现可复现的不满足项；必须保留输入指纹、日志和截图，不能只记录口头结论。

