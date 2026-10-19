# RC5 读档设计恢复：独立只读审查

## 目标、范围与结论

主线程冻结RC5并运行open_kaishek期间，独立核对[设计方案](native-load-design-repair-workaround-1019.md)、四文件工作区源码与RC4原件逐行差异、原生事件/scope文档。本线程不执行UI、Git命令、项目工具、console effect或SAV修改，不修改生产包。本文是新增调查记录，结论为`SOURCE_REVIEW_ONLY_NOT_NATIVE_ACCEPTANCE`。

**未发现可确证、需要阻止本候选启动的代码bug。** generic无scope入口、动态国家索引、死亡不重建、load不主动补RNG/资源、原PK回调隔离均符合本次限定设计。运行时接口组合、hook实际时机、健康比例和付费队列没有由这次源码检查证明；既有缓存/量化FAIL及原验收阈值保持。

## 精确差异与版本绑定

读取工作区VERSION为`0.4.0-rc.5`，原件为run `20261019T133314Z/mod/eep-1019`（RC4树`06485dc540a88b30cef15c27c323ff21cd88f04ad57b79e4f5bc0590937ef468`）。逐个比对Mod文件原字节，除descriptor版本外恰四处生产脚本变化：

| 文件 | RC5 SHA256 | 变化 |
| --- | --- | --- |
| `common/scripted_effects/eep_mothership_effects.txt` | `347254f6c966c52350d1396aeedec9304e0a3c4abd1f4d87535f5639d506c0af` | 新增layout helper；full sync调用helper并删除旧shipflag内联setter |
| `common/scripted_effects/eep_startup_effects.txt` | `6b3a3d6e876dd7b08878eba908671ddde3ed20c83a93d35ab9406e535d50c64d` | 仅给已知新建固定design打layout flag，保留原历史shipflag |
| `events/eep_events.txt` | `bee663bdf8e794999502aa52376166dd94b2c3129e5053f6b43d3a4dd4e85a02` | 新增generic eep.60，原事件正文未动 |
| `common/on_actions/eep_on_actions.txt` | `93be7df47f32895beadb5ce1f27d7abeb4e2f299e814ac959d1cf84bcafaeb6d` | 仅新增singleplayer load→eep.60一行 |

这些字节与主方案中的已完成实现表一致。主线程提及的新冻结树前缀`1cc8b77`由其gate/manifest负责绑定，本次没有另造冻结报告。

## 作用域与副作用核阅

1. **无scope到国家**：原版`common/on_actions/00_on_actions.txt:80–83`明确加载hook无scope、MP不执行。generic `eep.60`以`is_multiplayer=no`自守，经every_country取得各国作用域，只限本origin且已initialized。原版`events/game_start.txt:4–15`有相同generic→every_country形状；不是把无scope ROOT当国家。
2. **动态owner索引**：helper入口是国家C，`event_target:eep_mothership@this`绑定C自己的fleet F；F→owner时prevprev=C，`is_same_value=prevprev`精确验证原国。every_owned_ship只枚举C船；其fleet limit中的`event_target:eep_mothership@owner`以当前fleet所属国索引。无country0、无ROOT、无局部/全局目标写入，没有generic事件对ROOT的依赖。多个EEP国家分别处理自身绑定；普通国家在入口被排除。
3. **layout检查在实际设计**：`design`由ship到design；has_design_flag和set_design_flag各在design scope。只有缺layout flag的绑定ship才set_ship_design；之后ship_growth_stage是原生文档所述“current growth stage inside the ship's design”，has_component支持此scope，六个不同专属core逐一成立才标当前design。新增代码没有用实体section或旧shipflag代替该判据。layout flag表示共同的固定结构，不含国家tier，因此多个同版设计使用同一不带国家后缀的flag不构成奖励串线。
4. **startup与full sync**：create_ship.effect当前为新ship，内嵌design block退出后set_ship_flag仍是ship。原set_owner=root、core@root和mothership@root完全没改，仍只在原country启动事件链使用。full sync在国家scope调用helper；layout helper没有再调用full sync，形成单向调用，无递归。
5. **死亡与错误绑定**：目标不存在、owner不等C、非独船或非juggernaut时helper不进入；helper无create_fleet/create_ship/set_owner/target重绑，也不寻找替身。原startup的两层granted guard原字节不变。加载路径只有set_ship_design与design/ship flags，没有复活路线。实际尸体清理时序和真实死亡fixture仍需原生SAV证明。
6. **load不发RNG/账本**：eep.60只调用layout helper；helper没有initialize/startup、sync_components、random_list、变量、资源、人口、队列、任务或结算effect。六tier、R、C/L和镜像不被脚本主动改写。set_ship_design的原生刷新、健康/队列副作用仍属实机问题，不能把“没写资源effect”扩写成“运行时绝无副作用”。月度full sync仍按既有规则发积压，load入口没有多调用它。
7. **PK隔离**：三个专属PK完成/queued/unqueued on_actions原文未动，eep.50正文未动。下列六文件与RC4原件逐字节一致：PK事件、PK scripted_effect、共同settlement、native colossus consume、PK scripted_trigger、PK component template。新generic事件不传FROM，不进入Carrier/源星结算链，不能为排队/取消增加收益。

## 保留的实机不确定项

- 原生hook是否在保存目标/设计数据完全可见时调用、是否无手动sync即可即时恢复，须真实Load验证；源码不能确定引擎时序。
- 当前growthstage+六component组合有合法原生接口，但这里没有引擎执行结果。若setter或检查失败，未打flag会使下一次helper重试，不会静态伪装成功；重试的健康/队列副作用也要原样记录。
- 第一次面对“结构已新、但无designflag”的旧档会set一次，这是本设计的预期；新局已知新design直接标记，后续同会话已flag分支应跳setter。反复load是否先回退再重设、比例量化是否累积，仍按原阈值判断。
- helper不修base的旧implementation缓存；MP没有本加载hook，最多保留既有月度尝试。不能据此宣称缓存修复、MP即时支持或健康无损已通过。

## 原生来源

本次核读`runs/20261019T130448Z/logs/script_documentation`，SHA：effects `064b281a6c3a97f4261dfd30c3f761d1373a8ed82390fdc0109be9a112f6f489`，triggers `0f3ce1d0ad7b8fcce9ca654e57632683d996e579bdbb738d2cd56d91632e534f`，scopes `32f36a3584bdead0c83e4e7ece09b417be52a438518713e06b05d36240a0f352`。对应位置effects2374/2575/4414、triggers2488/3224、scopes62/378。原版on_actions文件SHA `7693e64fbe974f37db0c68969d10f7bdeec585ce59ca497b5e27ecd69ff8f306`；game_start SHA `8171b1806103ac96eb82cb5a8eca2712232764ea7712b1aa16049724268db528`。以上均本机Stellaris来源，未套用CK3方言。

## RC6直接六核心判据：第二次独立只读审查

本节追加新版本结论，不改写上述RC5源审为运行成功。主线程随后实际观察RC5：layout marker只落根global flags，二次load实际ship又回implementation1608/零core，相关FAIL保留。这说明原生文档的designflag scope声明没有证明该接口在本fixture中的实际存储/读取行为。RC6取消所有此类读写，改直接检查当前ship_growth_stage的六core；VERSION现为`0.4.0-rc.6`。主线程已冻结新树前缀`cc181`/59文件并报告包PASS，精确gate/manifest由其归档。

独立对比`runs/20261019T143452Z/mod/eep-1019`的RC5原件：除descriptor版本外，RC6实际只有两个脚本有差异：

| 文件 | RC6 SHA256 | 极小差异 |
| --- | --- | --- |
| `common/scripted_effects/eep_mothership_effects.txt` | `4e2d25004b917cd4b7c46bc13efe32765ba58fbd10aaa92a2728034a035da2cc` | 前置designflag改NOT当前stage六core；后置移除designflag setter，仅留历史shipflag |
| `common/scripted_effects/eep_startup_effects.txt` | `f3a0fb725b1ea7f9cb4f77a7225a30e7b83acb86bbd4ba496b91860ddbcbb697` | 新建船不再写designflag，只留原历史shipflag |

`events/eep_events.txt`与`common/on_actions/eep_on_actions.txt`分别保持RC5 SHA `bee663bdf8e794999502aa52376166dd94b2c3129e5053f6b43d3a4dd4e85a02`、`93be7df47f32895beadb5ce1f27d7abeb4e2f299e814ac959d1cf84bcafaeb6d`。前述六份PK文件仍各与RC5逐字节一致。

**本次未发现确定的作用域或死亡隔离bug，仍是SOURCE_REVIEW_ONLY。** 核阅证据：

- 前置`NOT = { ship_growth_stage = { A B C D E F } }`表示当前stage没有同时满足全部六core，任一缺失才进入setter；没有误写成“每个core都必须缺失”。前后集合顺序/名称完全相同，SHIELD/ARMOR/HULL/DAMAGE/TRACKING/REGEN各六项、总计12条has_component，helper仍只有一个set_ship_design。
- 原生scopes378–380明确ship→当前design内的ship_growth_stage；triggers2488–2490明确has_component支持ship_growth_stage。当前条件正处于every_owned_ship内，无design→stage错误跳转。外层owner/prevprev、@this与@owner动态国家索引完全未改；新NOT块不引入任何ROOT依赖。
- 整个生产P目录已无`eep_mothership_layout_1019`、set_design_flag、has_design_flag。旧档残留global marker不会再参与判据；历史`eep_mothership_design_1019`只在startup/成功后写，不被任何生产判断读取，所以它不能短路下一次修复。
- 当前实际设计已含六core时，every_owned_ship的limit直接不成立，不执行setter，也不为幂等补写标记。新建固定设计同样靠真实六core直接跳过；是否含完整50slot/6required仍由原生SAV验收，六core判据本身不代替完整配置检查。
- 不存在/错误owner/非独船/非juggernaut的绑定仍被原外层guard排除，未增加create_fleet/create_ship、转移或搜索替身。helper无healing/人口/资源/RNG/变量/完整sync路径；generic加载入口与fullsync调用方向未改。原生已死亡对象的exists/清理时序仍需真实死亡档证明，不能单凭原始表里有无record扩大静态结论。
- PK完成/排队/取消入口、FROM/Carrier guards、共同结算与组件数据均未改变；本次改动没有进入巨像回调。

主线程报告在RC5进程用完全相同的directguard原型执行两次原生保存：第一次实际新50slot/六core，第二次严格零差，两个SHA相同（前缀`44ebd`）。本线程未执行或另造该探针报告；该事实支持手动原型的结构判据与同会话跳过setter，不能当RC6冻结loadhook已运行的证据。RC6仍必须真实load至少两次，逐次核实际ship/base、损伤、队列及账本；RC5原FAIL、base缓存限制和原比例阈值不变。本轮只读源码/原生文档，未操作UI/Git/生产/项目工具。
