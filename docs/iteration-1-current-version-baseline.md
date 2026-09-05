# 迭代 1：当前版本实机基线与回归夹具记录

## 状态

- 状态：本轮基线冻结完成；政体矩阵留给后续回归执行
- 开始日期：2026-09-06
- 目标：先验证 Workshop 当前版本在 Stellaris 实机中的行为，再据此设计可重复的回归夹具。
- 已完成：`open_kaishek` 静态门禁、隔离 profile 启动、13 项决议目录检查、普通帝国计划10执行、存档重载与夹具冻结。
- 尚未执行：同一决议重复执行，以及蜂巢、机械、失控机仆、游牧/方舟政体矩阵；这些场景已进入回归夹具，不能写成已通过。

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

验收时发现工具缺少 Stellaris profile，已先在 `D:\workspace\open_kaishek` 补充 `stellaris-4.4.6` profile，覆盖本 Mod 使用的 `common/decisions`、`common/deposits`、操作符、作用域和本地化引用，并增加诊断、文档与测试。

- 工具提交：`2e17cd8 Add Stellaris 4.4.6 static validation profile`，已推送远端。
- 工具测试：151 项通过。
- 本 Mod 检查：所有 P 语言文件 `VALIDATED`，语法和语义诊断均为 0。
- 结论：`STATIC-GREEN`。它只证明当前 profile 覆盖范围内的静态合同成立，不能替代实机结果。

## 5. 当前风险假设

| 风险 | 当前证据 | 需要的实机反证 |
| --- | --- | --- |
| 4.3 mod 在 4.4.6 上发生语义漂移 | 描述符版本旧，但 `supported_version="*"` 会隐藏启动器版本警告 | 加载日志、决议可见性、执行结果 |
| 决议菜单过长 | 13 个直接决议；折叠键无脚本定义 | 行星决议界面截图与 OCR |
| 格式塔岗位键已变化或无人可就业 | 历史评论曾报告蜂巢科研/行政岗位问题 | 蜂巢/机械实机岗位面板与错误日志 |
| 地块可重复添加行为不明确 | 决议没有显式 `allow`/重复限制 | 连续执行同一决议、存档重载后计数 |
| 仅有简体中文 | 只有 `l_simp_chinese` 文件 | 英文环境缺失键基线 |

## 6. 实机基线结果

### 运行指纹

- 运行 ID：`20260905T205325Z`
- 游戏 EXE SHA-256：`bc451c72d9654c8901f1bb0bee1dd78d76f415465c2fbf746e9f98ade333173a`
- 隔离运行依赖 `d3dx9_43.dll`：2,401,112 字节，SHA-256 `84b900dbd7fa978d6e0caee26fc54f2f61d92c9c75d10b35f00e3e82cd1d67b4`，来自本机 Steamworks Shared 官方 DirectX CAB。
- Mod 整树 SHA-256：`a72b3de8cdfa9df627648bc226054f097ee7e8df9efcd5b490494408ea324f57`
- 游戏内版本：Pegasus 4.4.6；启用 Mod 后 checksum 为 `b648`，未启用时基线为 `fdde`。
- 测试存档：`iteration1_plan10.sav`，1,601,355 字节，SHA-256 `eef04d10696a525892f1ca5fde0ba9890ad5cb5b294ef562cea3e0650ba8d4ea`。

### 加载结果：严格判红

游戏可以进入主菜单并创建普通帝国实局，Mod 内容确实被加载；但本轮 `error.log` 稳定出现：

```text
[dlc.cpp:339]: Invalid supported_version in  file: mod/ugc_3710613857.mod line: 7
```

外层描述符沿用了 `supported_version="*"`。因此不能因为“能进游戏”就宣告 `LOAD-GREEN`；严格加载门禁结果为 `RED`。其余“找不到订阅项”记录来自隔离 profile 中的历史启动器库存，不在实际启用列表中，与本 Mod 不同源。

### 决议目录结果

- 普通帝国地球的决议界面中，计划00至计划12共 13 项全部可见。
- 每项均显示 1000 矿物成本和 180 天工期。
- 当前版本没有折叠入口，13 项直接铺开。
- 鼠标滚轮在该长菜单中没有可靠推进列表；拖动右侧滚动条稳定有效。夹具必须以文字定位和滚动条状态为准，不能固化计划编号的绝对坐标。

### 计划10执行与持久化结果

在暂停状态记录基线后执行“计划10：深采行星地幔富矿脉带”：

| 断言 | 执行前 | 完成后 | 重载后 | 结果 |
| --- | ---: | ---: | ---: | --- |
| 矿物成本 | 基线余额 | 立即减少 1000 | — | 通过 |
| 决议工期 | — | 出现并完成 180 天队列 | — | 通过 |
| 基础星球规模 | 18 | 18 | 18 | 符合引擎显示口径 |
| 总区划上限 | 18 | 20 | 20 | 通过，`+2` |
| 采矿区上限 | 7 | 9 | 9 | 通过，`+2` |
| 可用住房 | 158（早期截图） | 720（后期截图） | 720 | 方向符合 `+600`；因年份和人口同时变化，不把差值当作精确独立断言 |
| deposit | 无 | 生效 | 存档含 `mod_extend_mining_workplace` | 通过 |

重载使用同一进程内“载入游戏”流程完成。解包存档的 `gamestate` 后能找到：

```text
type="mod_extend_mining_workplace"
```

这证明 deposit 已被序列化并在重载后继续驱动区划效果。岗位页可见劳工总量 2400 和扩展后的工作岗位行；但当前 2560×1440、此 UI 缩放下“矿工”子行被底部页签裁切，滚轮也不能可靠滚动。故本轮不伪造“矿工 +600”的独立 UI 精确断言，后续夹具应使用更小 UI 缩放或专门的新局对照。

### 当前结论

- `STATIC-GREEN`：通过。
- `LOAD-GREEN`：失败，原因是外层描述符 `supported_version` 无效。
- 普通帝国 S02：通过。
- 普通帝国 S03/计划10：功能和存档持久化通过；矿工岗位精确 UI 子断言待专用夹具补强。
- S04、S05：未执行。
- S06：简体中文和长菜单行为已执行；英文行为未执行。

因此当前版本“能加载并且计划10可实际生效”，但整个 Mod 不能被表述为全面验收通过。

所有截图和存档检查完成后，已通过游戏内“退出到桌面”确认框正常退出；PID `20652` 不再运行，没有遗留 Stellaris 进程。

## 7. 自动化经验与边界

1. Stellaris 对常规虚拟键注入并不稳定；控制台、回车、空格、Esc、F7 等核心键应发送 Windows 物理扫描码，并把扫描码写入动作证据。
2. 物理 `Ctrl+S` 在 4.4.6 实测不触发保存。可靠流程为物理 `Esc` 打开菜单、文字定位“保存游戏”、物理 `Ctrl+A` 命名并回车。
3. F7 在当前键位布局打开“殖民地和星域”，但快捷键可能随用户键位变化。运行清单必须固定布局，失败时回退到 OCR 文字定位。
4. OCR 只能识别屏幕上的标签，不理解指标语义。`720` 必须通过悬浮提示确认是“可用住房”，不能凭数值与脚本常量相同就认定为岗位数。
5. 4.4.6 的“地产”页是分公司/宗主持有界面，不是旧版本意义上的星球地块/特征页。deposit 持久化应由效果数值与存档内容共同证明。
6. Steam `applaunch` 在本机触发 SteamService 提权而不能无人值守；直启 EXE 时缺失的 `d3dx9_43.dll` 可从 Steam 随游戏分发的官方 DirectX CAB 解出到隔离运行目录。夹具应记录其哈希，不能从不明网络来源下载 DLL。
7. 游戏内相对坐标依赖分辨率和 UI 缩放。优先使用快捷键和 OCR 文本定位，绝对坐标只作为固定桌面配置下的最后手段。

## 8. 证据等级

- `STATIC-GREEN`：P 语言解析、目录/引用/profile 检查通过；不代表游戏效果正确。
- `LOAD-GREEN`：精确单 mod 在隔离 profile 中进入主菜单，且本 mod 没有加载错误；不代表玩法正确。
- `SCENARIO-GREEN`：指定政体和行星场景中，玩家可见效果、日志和存档重载均满足断言。
- `RED`：出现可复现的不满足项；必须保留输入指纹、日志和截图，不能只记录口头结论。
