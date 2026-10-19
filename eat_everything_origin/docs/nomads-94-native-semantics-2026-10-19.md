# nomads.94 原生语义只读核对

## 目标与范围

核对本机 Stellaris 4.5.2 的 `nomads.94` 完整定义、全部原生调用来源与 ROOT／FROM／PREV 作用域契约，并核对原生行星、殖民地销毁效果的文档与实际脚本用例。回答这些静态来源是否足以证明 EEP 销毁末殖民地时必然传错 FROM，以及替换某个销毁效果是否有原生依据保证消除错误。

只读原生安装、现有日志文档及当前 Mod 源码；只新增本说明与 `evidence/1019-nomads-semantics/` 证据，不修改 Mod、游戏、UI、Steam、既有冻结日志，不提交。RC4 正在进行的真实发射与原版 callback 对照由主线程独立执行，本调查不得替代其运行时结论。

## 方案与验收标准

1. 在调查前记录本目标、范围、设计及验收标准。
2. 保存原生定义与所有调用的精确文件路径、完整行段和文件 SHA256，检索范围与零命中也留证。
3. 区分脚本文本、引擎生成的作用域文档、脚本注释和推断；不得把缺失调用链或未知引擎内部行为写为因果事实。
4. 明确 `destroy_colony`、可能的 `destroy_planet` 及原版 CRACKER 路径的支持范围、作用域与可见副作用。没有证据的修复建议只能记为未验证候选。
5. 保留未知项并给主线程和委派者简明结论；不宣告 Mod 验收完成，不改变 RC3 时长 FAIL 或其他 PENDING case。

## 执行与结论

已完成只读核对。静态来源不足以证明 `destroy_colony` 必然传错 FROM，也不足以保证替换为另一个效果可以消除 RC3 的错误。没有修改 Mod、原生脚本、UI 或冻结日志，没有运行游戏或提交。

本说明仅确认本机 Stellaris 4.5.2 的规则和文本，不外推到 CK3 或其他 Paradox 方言。版本来源为冻结的 `game.log:1`，EXE SHA256 由同 run manifest 绑定为 `400df27c82ddc845aa9dce79bd468d81f18f060d299cd263e3afa93aef4f7a83`。

### nomads.94 的完整定义及全部可见入口

完整定义位于原生 `events/nomads_events_1.txt:2256–2276`，已保存包含首尾的原字节摘录。它是隐藏、仅触发的 `country_event`。触发条件先排除 `champions_forge_contestant`，随后要求 ROOT 或 FROM 的 `is_nomadic = yes`；FROM 检查在 `:2268`，前面没有 `exists = from` 守卫。通过后 `:2273–2274` 分别对当前国家和 FROM 调用 `nomads.96`，后者用于恢复其被停用的方舟舰队、舰船和驿站。

检索原生安装目录的 3,262 个 `.txt/.log/.gui/.gfx` 松散文件，精确 `nomads.94` 共 7 处：1 个定义、2 个实际挂接、4 条注释。全部结果和命令见 [search-results.json](evidence/1019-nomads-semantics/search-results.json)。没有发现直接 `country_event = { id = nomads.94 }` 调用或第三个文本挂接；引擎内部、二进制和动态事件 ID 分发不在此静态检索的可见范围内。

| 原生入口 | 来源行 | ROOT／当前国家 | FROM | PREV 契约 |
| --- | --- | --- | --- | --- |
| `on_war_ended` | `common/on_actions/00_on_actions.txt:2627–2647`，挂接 `:2640` | 战败方 Loser | 主胜利方 Main Winner | 入口注释没有声明 |
| `on_becoming_subject` | 同文件 `:4496–4515`，挂接 `:4500` | 附庸 Subject | 其宗主 Overlord | 入口注释没有声明 |
| `on_colony_destroyed` | 同文件 `:1337–1351` | Carrier；owner／controller 清除前 | 注释没有声明 | 注释没有声明；且此入口没有挂接 `nomads.94` |

`nomads_events_1.txt:2256–2257` 自身再次写明上述前两项 ROOT／FROM 契约。事件类别为 `country_event`、`is_nomadic` 的引擎文档支持范围也仅为 country（`triggers.log:703–705`），因此 `:2268` 的 FROM 应为有效国家，不能把行星或射击舰队直接当成其预期 FROM。

PREV 和 FROM 不能互换。冻结的 `scopes.log:66–80` 明确：FROM 为上一个事件的 ROOT 或引擎预设 FROM；ROOT 为本上下文的初始作用域；PREV 为前一个作用域。由此可读出：在 `nomads.94` 的 `from = { ... }` 内，当前作用域转为 FROM，前一作用域为该事件的 ROOT 国家。入口顶层 PREV 没有原生 hook 契约，本调查不为其赋值，也不将它解释为胜利者、被销毁殖民地或射击舰队。事件 `nomads.94` 自身未引用 PREV。

### 销毁殖民地不等于直接调用 nomads.94

原生 `on_colony_destroyed` 挂接的是 `nomads.13`、`colony.2002`、`origin.3002` 等事件，不是 `nomads.94`。`nomads.13` 的完整定义 `nomads_events_1.txt:711–835` 也已保存；其目标是处理有宗主的游牧清洗附庸的资源与消息，没有调用 `nomads.94`。

与 RC3 manifest 精确匹配的候选代码路径为：EEP 行星杀手完成回调 → `eep.50` → `eep_colossus_settle` → `eep_settle_source`。结算的 `eep_settlement_effects.txt:126–134` 先设完成标志，再 `destroy_colony = yes`、`change_pc = pc_shattered`、清矿与清理任务。对应 RC3 文件 SHA256 与 manifest 匹配，未借用正在变化的工作区代码。RC3 Mod 全部 `.txt` 也没有 `nomads.94`、`on_war_ended`、`on_becoming_subject` 或 `on_colony_destroyed` 文字定义／调用。

这些文本只支持“EEP 使用一个原生销毁殖民地效果，国家消失／战争结束可能产生其他原生事件”的待验证链路。它们没有展示引擎内部何时移除国家、战争何时结束、向哪一方派发 `on_war_ended`、此时 FROM 是否仍有效，也没有证明销毁末殖民地一定经过这个 hook。不能写成“`on_colony_destroyed` 必然把错误 FROM 传给 `nomads.94`”。

冻结的 RC3 `error.log:28–42` 确认一次实际错误：ROOT 为 `EEP 03 铁心灭绝者`、country ID 0；`from` 记录为 country ID 4294967295；报错位置为 `nomads_events_1.txt:2268`。这证明当次检查 FROM 无效，不能独立证明是哪一个 hook、哪一步清理或哪个脚本操作使其失效，也不能证明 `nomads.96` 的 immediate 实际运行或 gameplay 损害范围。该记录继续作为未解决的新增运行错误保留。

### destroy_planet 与可见原生替代路径

| 接口／路径 | 原生证据 | 静态结论 |
| --- | --- | --- |
| `destroy_colony = yes` | `effects.log:432–434`：“Destroys the colony on the scoped carrier”；支持 planet、ship、colony | 已文档化的合法效果；没有声明由调用者提供战争赢家 FROM 的参数 |
| `destroy_planet = ...` | 完整上述松散脚本赋值检索为 0；全部冻结脚本文档无该效果条目 | 本机来源未确认其存在或受支持，不能直接当作可用修复接口；检索不能排除一切未文档化二进制实现 |
| `remove_planet = yes` | `effects.log:1638–1640`：移除 scoped planet；支持 planet、ship、colony | 名称确实存在；物理移除行星和保留碎裂星球的目标不同，文档未保证避免该错误 |
| 原版 `PLANET_KILLER_CRACKER` | `01_planet_destruction.txt:1–24`；`planet_destruction_events.txt:20–339` | 是一条包含外交／旗标／厌战／人口／建筑／星球类别等副作用的完整路径，不能视为单一销毁效果的等价替换 |
| 原版 NEUTRON 与 TOXIFIER 等 | `planet_destruction_events.txt:979`、`:1973`、`:2502` 均使用 `destroy_colony = yes` | 原生也使用该效果；这既不能保证它无引擎缺陷，也不能单凭 Mod 使用它就认定 Mod 传错作用域 |

原版 CRACKER 完成 callback 的来源契约为目标 planet／Carrier、FROM 为射击 fleet（`common/on_actions/01_planet_destruction.txt:1–3`）；`planet_destruction.100` 排在后面的注释明确写着它可能杀死国家（`:21`）。普通宜居星路径先逐 pop group `kill_all_pop = yes`（`planet_destruction_events.txt:282–284`）、破坏防御和建筑，随后 `change_pc = pc_shattered`（`:313–337`）。该事件没有使用 `destroy_planet`，其可见清理顺序也不同于 EEP。

`from.fleet.owner` 不能反证 FROM 必须为 ship，因为本机 `scopes.log:58–60` 明确 `fleet` 转换支持 fleet 输入。原版 callback 的 fleet FROM 与 `nomads.94` 的 country FROM 是两个不同事件上下文，不能混用；主线程的显式 `FROM=Mother fleet` 对照方案与前者相符，但是否重现及是否排除 EEP 因果必须由真实执行留证。

当前没有 primary native 依据保证“把 `destroy_colony` 换成 `destroy_planet`／`remove_planet`／`kill_all_pop` 或调用 CRACKER 就能消除错误”。这些候选可能改变国家清理时序及 gameplay，需要单独设计、文档先行和引擎验收，不能仅为清洁日志而未经验证替换。

### 证据完整性与未解决项

独立证据目录为 [1019-nomads-semantics](evidence/1019-nomads-semantics/sources.json)，包括 15 个来源的 SHA256、行数与路径、30 段原字节摘录、带行号阅读本、搜索命令／完整命中／零命中以及范围文件清单。`sources.json` SHA256 为 `141fbb9265d8c351a810041631322b57160a3e1e750ef1f1ebab3146eb35eb4c`。独立 [verify.json](evidence/1019-nomads-semantics/verify.json) 已重新读取原始来源并逐字节匹配全部摘录，状态 PASS；它仅验证证据拷贝，不是 Mod 或运行时验收 PASS。原始 `1019-rc3-final-logs/` 未修改。

仍需主线程运行证据确认：当次到底由战争结束还是成为附庸入口触发；哪个国家／战争对象在分发前消失；原版显式同形 FROM 的末殖民地 callback 是否同错；EEP 与原版的收益、国家和战争清理差异及实际影响。若原版也复现，只能证明该原版路径可复现，不能据此认定 EEP 没有缺陷；若原版不复现，也不能未经比较就认定 EEP 为唯一原因。

RC3 巨像 90／30 时长 FAIL 不变，RC4 真实射击与最终 case 均由主线程独立验收；本调查不解除任何 PENDING。
