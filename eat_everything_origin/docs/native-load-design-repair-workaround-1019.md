# 单人加载后恢复母舰实际设计：受控方案（2026-10-19）

## 目标与范围

在已证实的旧母舰重载问题下，研究使用原生单人加载回调恢复**现存、唯一、归属正确的母舰 station ship 实际设计**。这是候选 workaround；不修复、不伪称修复关联 starbase 的旧 `ship_design_implementation` 缓存，不删除旧设计或更改存档。本文先记录设计与验收，未改生产文件或工具，未操作 UI。

此前旧档迁移与登记、名称、fleet-scope 等失败原证据保持不变。尤其 ship/base 两份引用不同和原三防比例 `1e-6` 检查失败，不因增加加载后修复而改为通过。相关历史见 [native-design-persistence-research-1019.md](native-design-persistence-research-1019.md)。

## 已核原生合同与现有生产链

原版 `common/on_actions/00_on_actions.txt:80–83` 明确 `on_single_player_save_game_load` 无 scope、MP 加载时不运行（OOS原因）。文件 SHA256 `7693e64fbe974f37db0c68969d10f7bdeec585ce59ca497b5e27ecd69ff8f306`。

因此该 on_action 应接无国家 scope 的 generic `event`，不能假设 ROOT 已是玩家国家或直接接 country_event。原版 `events/game_start.txt:4–13` 的 generic event→every_country 是已有同类入口；当前 generated effects4414–4416也明确 every_country 支持 all scope。

当前冻结生产：

- `common/on_actions/eep_on_actions.txt` 只有游戏开始 country、月度 country、转移/改造和巨像回调，没有加载回调。SHA256 `f37870ca1050ca976cbee80312a8862a698ca4596bae55a7b9e9fdfec897db8e`。
- `events/eep_events.txt:21–25` 的 eep.1 会 initialize→startup→full sync；28–38的 eep.2会 initialize→full sync→自动吞噬扫描。二者均不是仅恢复设计的加载入口。文件 SHA256 `e4be49df425db8dd4c4919a788c38ef2d4075466a9da946e6dc35a6c47cf55a1`。
- `eep_mothership_effects.txt:119–128` 当前用持久 shipflag 判是否迁移。原生重载已证明该 flag仍留而实际 design回旧，故它不能当设计正确的判据。冻结 SHA256 `b4efb84032796adc1f87d0613a56e601926dca25ba645b7b2cd60dd13ea17ed5`。

以下接口来源仍是 `runs/20261019T130448Z/logs/script_documentation`，effects SHA256 `064b281a6c3a97f4261dfd30c3f761d1373a8ed82390fdc0109be9a112f6f489`，triggers SHA256 `0f3ce1d0ad7b8fcce9ca654e57632683d996e579bdbb738d2cd56d91632e534f`，scopes SHA256 `32f36a3584bdead0c83e4e7ece09b417be52a438518713e06b05d36240a0f352`：

| 原生位置 | 实际含义 |
| --- | --- |
| effects2374–2376 | `set_design_flag=<key>` 仅design scope |
| triggers3224–3226 | `has_design_flag=<key>` 仅design scope |
| scopes62–64 | ship→`design`，读取当前实际设计 |
| effects2575–2580 | set_ship_design支持ship/fleet |
| scopes378–380 | ship→`ship_growth_stage`，当前设计内部的当前成长阶段 |
| triggers2488–2490 | `has_component=<template>` 支持ship/ship_growth_stage |
| effects4414–4416 | every_country支持all scope |
| triggers1436–1438 | is_multiplayer支持all scope |

`ship_growth_stage + has_component` 的组合有分别对应的原生合同，尚未在本受控修复上完成实机验证。不能仅凭实体 section 中看见六核心便给错误 implementation打正确设计标记；旧混合状态恰好已有新实体 section却引用旧设计。

## 候选实现安排（只建议，不实施）

### 入口与作用域

1. 在项目 on_action新增 `on_single_player_save_game_load={events={eep.<新ID>}}`，事件 ID由主线程分配并查重。
2. 新事件使用 generic `event={hide_window=yes is_triggered_only=yes ...}`。它的 immediate通过 every_country取得国家 scope，limit含 `has_origin=origin_heart_of_devouring` 和 `has_country_flag=eep_initialized`；可加 `is_multiplayer=no` 防止人工触发时误解范围。不能把generic ROOT当国家，也不把固定country0写入生产。
3. 每国调用一个**仅设计恢复**的 country helper。该 helper复用现有 Mother存在/owner正确/num_ships=1/juggernaut guard，再在该国every_owned_ship中精确匹配绑定fleet。没有绑定、失去所有权、母舰毁灭或不唯一时不操作，不搜索替身、不创建/转移/复活。
4. 不从加载入口调用 eep_initialize、eep_startup、eep.1、eep.2、full sync或自动吞噬。尤其不在load额外补发RNG积压，避免加载动作改变 R、六 tier、资源或付费队列。

结构示意（事件ID与helper名仅占位，不可原样作为已实现代码）：

```text
event = {
    id = eep.<new_id>
    hide_window = yes
    is_triggered_only = yes
    trigger = { is_multiplayer = no }
    immediate = {
        every_country = {
            limit = {
                has_origin = origin_heart_of_devouring
                has_country_flag = eep_initialized
            }
            eep_repair_existing_mothership_design = yes
        }
    }
}
```

### 检测实际设计，避免无条件切换

使用一个带版本含义的设计 flag，例如 `eep_mothership_layout_1019`。它与目前同名含义的shipflag区分，读取必须在 `design={...}` 内。

- 新局：create_ship.effect里对刚从新固定设计创建的 ship执行 `design={set_design_flag=...}`。随后游戏开始full sync读取实际designflag即可跳过 set_ship_design。不给新局无谓地换一次设计。
- 现有舰：仅在当前 `design` 缺少该 flag时切换。对确认的绑定ship调用 set_ship_design到 `NAME_EEP_Baiqi_Mothership_1019`。
- 成功后再对当前design打flag。建议先通过当前 `ship_growth_stage` 确认六专属核心均在设计里，再标记；不要在切换失败时直接给当前旧设计打新 flag而掩盖下次检测。必要时受控第一版可使用create目标+is_same_value验证，但已知注册方案未解决base、额外设计实例会增加干扰，不默认引入。
- 月度完整sync和加载入口共享同一个layout-only helper。现有shipflag可以保留作历史，不能再当跳过设计检查的依据。
- 对已正确且已标记的实际设计，重复helper不调用set，不重复改健康；组件RNG、C-derived L仍只由原有full sync处理。

生产中是否需要更强的固定载荷验证，以及六核心成长阶段trigger是否按预期读取implementation，必须由先行原生探针决定；静态检查不能替代它。

## 单人与MP边界

原版明确该加载回调不运行于MP。本候选只承诺**单人原生load后恢复实际ship载荷**的待测范围，不声称MP即时修复、跨平台同步或解决OOS。若monthly仍执行同一设计helper，MP最多在下一月触发后尝试补正；加载至月度之前存在旧actualship状态，不能称为等价支持。

即便单人hook有效，旧starbase引用仍可能保留；下次load可能先回退，再由hook恢复。因此应报告“单人加载后受控恢复”，而非“基础设计绑定/序列化已修复”。完整缓存修复政策下的原FAIL继续保留，发布范围需据实际结果明确。

## 健康、付费队列与随机奖励风险

原观察有约五位小数健康比例量化，旧纯load与set_design均可能触发；新hook没有原生脚本能力找回已丢失的旧精确比例尾数。重复load可能重复经历量化，不能只验证满血或把偏差归为回血。原 `1e-6` 规则未获修改。

同一暂停会话中重复helper应因designflag完全不切换，因此原生current/max三防、变量和奖励应精确不变；这与跨次load再修复是两个独立测试。后者必须按原损伤比例政策如实报告，不能将“实际设计对了”代替“损伤比例也通过”。

本候选不显式更改基地、资源、队列或订单，但set_ship_design本身的原生副作用仍需对真实paid fixture完整比较。不得清队列、退费、重建基地、补资源或复活来制造通过。

## 事前验收与门禁

先有docs候选，再实现、冻结新的可溯源tree并通过open_kaishek新包检查；不热改当前RC4运行字节。

1. **原生hook实际触发**：简中单人通过真实Load界面加载新保存的测试档。保留选择截图、文件名、SAV SHA、加载后日期及原生日志；不以手动 `event`/`effect` 替代loadhook验收。generic无scope→every_country正确，未误遍历普通国家。
2. **新局无切换**：新建Mother实际设计正确并含flag；重复sync后没有额外设计切换/实例、损伤或RNG奖励。
3. **旧受损档即时恢复**：原生Load后不手动sync、不推进日期，原生保存；ship implementation为新完整固定设计，50slots/6required/6core正确。base旧引用作为已知未修复项单独保留。
4. **重复helper幂等**：同日重复两次设计helper和正常full sync；设计/健康current-max、C/L/R/six tiers及country镜像不变。若存在P>0，full sync可按既有规则补差，故幂等对照应使用P0或把helper与补差分开；不能重置tier伪造条件。
5. **重载幂等边界**：对hook恢复后的真实SAV至少再原生load两次。每次实际ship应恢复、IDs/归属/付费队列保持，记录三防比例变化并用原政策判。分别保留cache FAIL与load后功能检查结果。
6. **没有母舰与错误绑定**：毁灭/不存在/非唯一或归属错的独立fixture中hook不创建、不转移、不消费/发放。不要拿人为删target而仍有活舰的fixture冒充真实毁灭。
7. **普通舰负对照与回调错误**：普通舰实际设计/current-max与队列不变；日志无新scope/缺event/无效trigger错误。非中文只静态检查；MP即时load修复不在范围。
8. **动态属性刷新分开报告**：同日载荷/损伤检查与至少6日触发修正刷新检查分开，不能把推进期间自然恢复计为迁移无损。自然RNG矩阵仍待最终新tree执行。

以上是受控方案，不是验收通过。若量化、队列或重复load失败，保留原报告，不自动放宽阈值或把workaround解释为完整持久化修复。

## 授权实施范围与固定命名

主线程在本文方案落盘后授权实现，限四个现有生产文件：`common/scripted_effects/eep_mothership_effects.txt`、`common/scripted_effects/eep_startup_effects.txt`、`events/eep_events.txt`、`common/on_actions/eep_on_actions.txt`。不修改VERSION/descriptor、不提交/冻结/操作UI；主线程负责新RC5候选、open_kaishek和原生验收。

固定选择 `eep_repair_existing_mothership_design` country helper、`eep_mothership_layout_1019` designflag及此前未使用的generic事件 `eep.60`。helper保留原存在/归属/唯一/尺寸约束；只有实际design缺flag才执行set，切换后在当前design内部growthstage核六core，均存在才标designflag与历史shipflag。新局create_ship.effect直接标已知新design。full sync移除原shipflag guard/内联setter，转为调用helper；单人load仅调用helper，不触及C/L/R/六tier、初始化或资源逻辑。

静态核阅须确认新事件ID唯一、四文件括号/AST可解析、load→helper没有startup/随机发放/资源写路径、已flag分支没有setter，并记录最终文件SHA。静态核阅不等于原生回调、六组件trigger组合或健康/队列通过。

## 候选实现完成与源码核阅

四文件已按上述固定命名完成：

| 文件（相对mod） | SHA256 |
| --- | --- |
| `common/scripted_effects/eep_mothership_effects.txt` | `347254f6c966c52350d1396aeedec9304e0a3c4abd1f4d87535f5639d506c0af` |
| `common/scripted_effects/eep_startup_effects.txt` | `6b3a3d6e876dd7b08878eba908671ddde3ed20c83a93d35ab9406e535d50c64d` |
| `events/eep_events.txt` | `bee663bdf8e794999502aa52376166dd94b2c3129e5053f6b43d3a4dd4e85a02` |
| `common/on_actions/eep_on_actions.txt` | `93be7df47f32895beadb5ce1f27d7abeb4e2f299e814ac959d1cf84bcafaeb6d` |

源码检查使用现有 `tools/audit_save.py` 的token及命名字段读取器：四文件括号平衡、根命名字段可读取；新helper子树可递归读取；eep.60在项目事件ID中恰一处、由唯一singleplayer loadhook引用；helper只含一个setter、actual designflag guard与恰六个预期core条件；helper/load没有初始化/新建/转移/资源/变量/随机奖励/完整sync调用；full sync改为恰一次helper调用且无内联setter；startup没有setter而直接给已知新设计打flag。四文件均LF，限定四文件的 `git diff --check` 无错误（没有stage/commit/push）。

此结果记为 `SOURCE_REVIEW_ONLY_NOT_NATIVE_ACCEPTANCE`。字段读取器不是完整P语言或scope验收；open_kaishek、最终tree冻结、generic回调实际时机、growthstage组合、重复调用健康与付费队列仍由主线程执行，未预填通过。旧base指针/量化失败报告保持原值。

## RC5??????????????

VERSION?descriptor????0.4.0-rc.5?59?????`1cc8b77c28f3d59b0d840982c7f039a209cb66f3e26d9c3280ad2dfa0f9dbd52`?open_kaishek????PASS?36/36 P???12 DDS?131??10?????SHA`706f3b00d5b7447d3825bf7a2f7c7e55f7f20c28b530ce6a83f34b77b57bf7bf`?gate SHA`a313bbdd70d381f13030f62dccf58631df90b3a25cbb19eb0622ed672aa20b4e`??????gate???????????????[evidence/1019-rc5-static](evidence/1019-rc5-static/source-index.json)?????????????????????????loadhook???designflag?????????????????133314Z????RC4???????RC5????????
