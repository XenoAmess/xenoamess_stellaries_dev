# RC6 已完成证据的 PENDING 汇总索引

## 目标与范围

使用现有 `publish_1019 scaffold-index`／`runtime_index` helper，新建 `docs/evidence/1019-requirements/rc6-runtime-progress-v1.json`。静态report固定为 `docs/evidence/1019-rc6-static/candidate-rc6-open-kaishek.json`；manifest固定为 `docs/evidence/1019-rc6-migration-checkpoint-v1/run/manifest.json`，run150008Z／RC6。合并已完成public／paid迁移严格v2限定资料、Purifier／Hive及随后获准追加的Machine薄归档payload proposal、母舰UI／source-derived power部分checks。18个case全部保持PENDING，没有独立结果的字段为null，不生成final-result、不写正式通过、不提交或操作UI。

## 设计与边界

先读取当前helper／schema与各稳定proposal，再按现有字段合并，保留原始严格v1 FAIL与迁移v2独立范围；不改变其它agent文件。原始evidence用项目相对路径／SHA绑定；现有raw SAV复用薄归档，不复制。Machine r6mc尚在活动且未年度完成，不读取其文件、不填它的结果；不读取活动日志。母舰维护UI与power源推算范围分开，r6pu后置85UI不混入经济过程。

经济no-injection／trade／jobclosure／disband四项由root最终review。可另建不可变Purifier／Hive economy worker UI／actions小包，限定各native newgame→12 monthly／yearUI的原worker、source与receipt；按原始证据核对恰12条FF30命令及既有collect流程，不混postUI或Machine。root交接只有该受控worker链，直至总receipt完成没有其它UI／console；此事实按root交接与可核worker证据记录，不能声称全过程系统输入审计。缺独立来源的四项仍null，不因文字声明置true。

root随后通知Machine worker14463正常exit0、12月／yearUI完成，授权追加；kaishek线程已封口machine薄archive及三分支summary／payload，6case均PENDING、12项操作约束null。Machine薄包tree65e8d375…、summary SHA0f8fba5d…、payload SHA80179623…。本轮改用这些已封口资料整合六case，另建Machine worker UI小包，严格排除独立r6mcinit2 repeat-initialization probe与当前活动r6g成长。先将初版P/H汇总原字节保存为快照，再通过同一helper追加Machine，保留原assembly hash与history；最终byte-audit／missing以追加后的主索引为准。此前“不读Machine”是未完成时的首轮边界，完整通知后仅该已完成经济链进入授权范围。

## 验收标准

新索引schema由现有helper生成且可被对应PENDING路径只读校验；18case status均PENDING、缺结果null、无final-result；引用的static／manifest／proposal／UI／power原字节SHA一致；旧v1失败和source-derived非UI边界不变；活动logs、r6mcinit2、r6g与r6pu postUI不混入经济证据。输出真实missing清单与18组剩余项，交root审查四项与整体收尾，不git／UI／Steam。

## 封口结果

主索引 SHA256 为 `94ed603301ae0913d2c3eb602e4b6a2b21eeeadf4f23443000cd2bb77b9016aa`；原字节引用复核报告 `rc6-runtime-progress-v1-byte-audit.json` SHA256 为 `dbb593325083a5639e8fa1f77464caf54f216fb3db3b82e00e73467269a5e47a`。全部18case、component与顶层均PENDING，唯一run为20261019T150008Z，RC6树为 `cc181c8a27ede295e9fcebeffc5e10bb75e9cd643edec1d194b928993ffab33a`。1310个引用对象归并为947个唯一项目相对路径／SHA引用，均已核对原字节。原P/H索引原字节保留在 `rc6-runtime-progress-v1-before-machine.json`，Machine合并阶段审计另存，未覆盖历史SHA。

139项观察中34true、1false、104null；true只表示记录下来的单项观察，不提升case。三分支startup各7true；经济各3true、4null，各含12个月baseline与12个月candidate。共12项经济操作约束等待root审核受控worker链。母舰仅维护观察、source-derived非负供电、22大防御槽三项true；`+9743`仍标源推算，未称UI测量。迁移保留原严格 `damage_preserved=false`，独立v2预算字段true，完整typed v2合同只读校验通过，其余11项顶层映射仍null。公开／paid载入代表截图、原OCR与F12动作从既有checkpoint绑定，未重新操作UI。

新增两份完成经济worker操作归档，不重复SAV：

| 小包 | payload | 原字节 | 图／OCR绑定 | 复用canonical引用 | index SHA256 | verify SHA256 |
|---|---:|---:|---:|---:|---|---|
| `1019-rc6-economy-worker-ui-v1`（Purifier／Hive） | 444 | 17,548,584 B | 100 | 128 | `651c25a0144a9c789f44ada6ccb45b5c4393e98e2c03c41e9db7ad165d88e5b9` | `64b9a2f310407431a9c79b14b29eae4520012ded534b518b68c2cd7165df1fdc` |
| `1019-rc6-machine-economy-worker-ui-v1` | 227 | 9,010,835 B | 51 | 62 | `f82a7eb15568b6fcf5e6521ba0e5fb4e3edd78f37216e1839d92cd973cfc2a0f` | `4e4f03e9a749e152b6074c34753970960cecf836d8d407de4c5065e0e86ea8dd` |

每分支核对原receipt恰12条 `fast_forward 30` 及其动作绑定。collector源SHA与原receipt一致；其余源副本只是事后磁盘审阅来源，不证明旧进程内存载入内容。root交接声明仅限定其独占受控worker执行链，不是全系统输入审计。两个小包的独立verify仅通过原字节及命令绑定，不是Mod验收。

18组精确剩余键和证据类型见 `rc6-runtime-progress-v1-missing.json`／`.md`。全部组尚未绑定最终运行日志；本轮没有读取活动日志。repeat-initialization独立报告／proposal已由acceptance线程封口，但其原生新after-SAV与操作链尚未进入本索引的项目归档，记录为待独立归档、绑定与审核，不要求凭空重做样本。活动成长r6g、最终日志及其它尚未封口功能链未收集。未创建final-result，也未写任何case PASS或整Mod PASS。
