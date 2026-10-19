# RC5限定范围复验设计与发布合同影响

## 目标与范围

2026-10-19主线程要求只读分析RC5四处生产变化对已归档RC4 PK时长／结算去重／Relic原生对照／实际跳跃证据的影响，提出最少且充分的复验方案。本轮不改生产、门禁、旧manifest／报告／归档或验收状态，不操作UI／Steam／Git。RC5静态门禁仍由主线程与open_kaishek执行；本报告不提前声称候选已通过。

## 设计

逐字节比较RC4冻结源码与RC5候选，列出所有变化及依赖闭包；检查loadhook、actual-design识别与startupflag对新局、原生加载、初始迁移、同日回调、重复初始化和数值／配置的可观察影响。把RC4报告保留在其原run／tree下；只有依赖逐byte不变且在新候选实机重载后能独立验证相同业务不变量的范围，才考虑新增明确的scope revalidation报告。必须把RC4观察和RC5补测分别绑定真实run／tree／原生文件／工具字节，不允许替换旧报告tree或在精确tree门禁下借用旧case PASS。

同时只读检查publish_1019的精确tree／run／native evidence合同，提出若需要跨tree限定结论应使用的显式schema与验证要求；仅提出建议，不实施门禁变更。对同一run中途更换capture工具，提出独立tool-source delta receipt与新执行器源归档要求，保持旧manifest及旧source不变，防止后段操作被误绑定到旧工具。

## 验收标准

- 生产差异及不变依赖有真实路径、文件SHA和完整覆盖范围；推断与已核事实分开。
- 最小复验逐项说明触发、所需新原生证据、可沿用的历史事实及仍未证明部分；不得用静态不变代替受loadhook影响的实际重载／新局行为。
- 明确当前门禁能否表达该复验方案，任何schema建议均不自动提升PENDING或豁免case。
- 工具切换补证须绑定切换前后SHA、实际生效边界及原字节来源；无法定位边界的旧后段声明保留不确定，不倒填。

## 调查与建议

### 已核源码事实

逐59文件比较已保存[原字节依赖审计](evidence/1019-analysis/rc5-source-dependency-audit-v1.json)，SHA `279f40692d81d65a2f1f19e60458379e1e0445da622acbc8571f9e98956972ea`。RC4树为`06485dc540a88b30cef15c27c323ff21cd88f04ad57b79e4f5bc0590937ef468`，RC5冻结目录树为`1cc8b77c28f3d59b0d840982c7f039a209cb66f3e26d9c3280ad2dfa0f9dbd52`；两者均59文件，无新增／删除。变化为四个P脚本及descriptor元数据，共5处原始文件字节不同，54完整文件相同。descriptor除rc.4→rc.5外有换行字节差异；归一换行与替回版本后其余内容一致。本报告只记录冻结字节，不修改metadata。

| 变化文件 | 实际变化与风险边界 |
| --- | --- |
| `common/on_actions/eep_on_actions.txt` | 新增原生单人load→eep.60；每次真实加载均进入此前没有的新执行路径。 |
| `events/eep_events.txt` | 新增无scope的generic event，遍历已初始化且有指定origin的country，仅调用existing-design repair。其它事件原体虽未改，整个事件文件已变。 |
| `common/scripted_effects/eep_mothership_effects.txt` | 新增按actual design flag判断的country helper；sync先调用helper，替代原按ship flag判断的换设计逻辑。set_ship_design、实际组件stage验证、designflag持久化及舰体／缓存／队列影响必须原生复验。 |
| `common/scripted_effects/eep_startup_effects.txt` | 新创建母舰同时写actual design flag；新局与重复初始化的行为依赖发生变化。 |

PK component TXT（90／90／30／0）、component set、PK guards／effects、settlement、固定ship design、两section、六真实core component TXT及mothership modifier定义均在54个完整相同文件中。changed mothership effects内的`eep_sync_mothership_components`原始函数块也完全相同，SHA `36ee7d6046cf40411ee82ea3efaca06a26faac29a5033c931c2f4303cabae020`；这只证明RNG分支源码没改，不能证明新design切换未影响装备／tier作用。

依赖并未完全隔离：PK完成的`eep_colossus_settle`先执行不变settlement，随后调用已变`eep_sync_mothership`；正常拆解完成和月度eep.2也进入该sync。新load event虽没有initialize／reward调用，但引擎执行set_ship_design可能影响真实design／最大值／旧伤比例／命令／cooldown，静态注释不是原生无副作用证明。helper明确不修关联mobile-starbase缓存，10船坞／队列不能仅凭ship body推断。

### 最小足够复验：优先维持现有精确tree合同

RC4报告均保留原run／tree／限定scope；包括已知即时结算FAIL、错误手输事件、nomads错误与迁移旧伤FAIL。它们可以作为输入fixture与历史对照，不是RC5 case PASS。建议不为这一轮扩大gate：在RC5静态PASS后，新run加载现有原生fixture并保存新输出；同run可顺序加载不同功能分支，run_id只登记一次，输入旧SAV与输出新SAV明确区分。这样既有contract即可表达，避免为一次源码调整新增跨tree推断器。

| 已有RC4范围 | 可直接保留的历史／源码事实 | RC5必须补的最小原生范围 |
| --- | --- | --- |
| PK90／30时长 | 原EXE下RC4完整90日充能与30日发射；本轮PK数值／组件解析依赖字节不变。 | 先实际load旧ready fixture，核actual design body、六core、PK key、计数／stock／队列未被修复路径改变；在RC5发起一次真实enemy shot。可只保留queue0、windup89、fire0、fire29、完成等决定性原生状态，不重拍RC4全部密集采样；新90／30结论仍须新run的日期／native timer／完成状态证明。只核component字段或加载旧shattered结局不能写RC5实际充能发射通过。 |
| PK结算／回调／reload去重 | RC4单次enemy shot的C/G/D／population／crisis数学、正确回调去重的原始观察；不变settlement公式。 | 上述同一次RC5发射兼收稳定结算、正确completed queued／unqueued回调后重复触发、同日native save→实际reload→新save。核实际design与layout／HP、ledger／tiers／source receipts／objective不重复；不能用旧DISMANTLE无效手输对照顶替。新loadhook直接影响reload，必须重测。正常拆解的reload分支同理，并入其本来仍需完成的正常回归，不另增新局。 |
| Relic同国同日配置／面板 | 原版NAME_Relic源、RC4母舰／参考舰真实配置和UI数值；不变固定设计／slots／组件／section。 | 直接load已有同时包含母舰与Relic的r4relic6原生fixture，无需重spawn或建造参考舰。新save独立读实际design／11AUX／6required／三防／10yards；同日两舰UI复核足以重认证配置／参考结论。已有power_nonnegative与upkeep_observed缺口仍需真实hover／设计器证据，不能由源码不变补齐。 |
| 实际jump | RC4真实8→196、14日充能、落地cooldown原始观察；原版jump component／自定义设计逐byte不变。 | 同一Relic fixture分支母舰可再次执行一次真实jump，无需新参考舰；核命令、出发／到达系统和计时／cooldown。只在RC5加载旧r4jumpedge14并核位置／cooldown，只能证明“跳跃后状态能保留”，不能填写actual_jump。若要验证upgrade时正在jump的命令不丢，应从原生pending-jump输入另作加载持久性补测，不能宣称已由普通已完成存档覆盖。 |
| 初始化／旧存档／候选reload | 原fixture来源和原始失败仍有效；不变人口／经济布局代码提供独立对照。 | RC5新局actual design flag与一次重复eep.1、同日重复sync／连续两次原生reload，覆盖实际设计体与stage／shipflag而非仅flag或entity section；旧0.3.1 public和历史paid fixture各自重测旧伤、identity／position／队列／population／stock／奖励，原FAIL不迁移成PASS。destroyed／missing bound Mother及不合格owner不应被新helper复活或修理，可与原有对应guard case共用before／after，不新增一套额外开局矩阵。 |

真正可以免重复的是RC4原始观察的重新抽取、原版源重新查找、旧fixture／参考舰重新制造、相同组件文件的额外固定L UI和PK密集每月截图；这些没有必要反复做。改变代码的原生load路径、实际发射与完成后sync、actual jump本身不是源码SHA能替代的事实。仍未完成的成长18phase／三政体全年经济／Lithoid与普通拆解／guards不得借“数值布局不变”省略；沿用原计划在最终候选完成，不额外扩大全矩阵。

### 精确tree合同与可选schema建议

现`validate_runtime_index`要求唯一最终production tree，static gate的files/tree相同，所有`runs`manifest的repository/copied tree和file hash相同，case tree／run_ids属于该集合；组件独立report也要求同tree／run。`candidate_tree`仅为正式metadata-only版本替换还原候选descriptor，不能把四个脚本变化当metadata。RC4 manifest不能加入RC5的runs；可留archives，旧报告文字不得改tree。当前gate不理解scope revalidation；给case加未知说明字段也不构成自动验证或允许跨tree。

上述“旧输入fixture＋新RC5原生输出”的方案无需扩gate。若主线程另决定只对某个完全不变子系统采用历史runtime事实＋新candidate桥接证明，则必须先实现独立严格合同，例如`eep.scope-revalidation.v1`，而不是放宽现有tree相等条件。建议至少：

```json
{
  "schema": "eep.scope-revalidation.v1",
  "status": "PENDING",
  "current_candidate": {"tree_sha256": "RC5完整树", "manifest": {"path": "真实新manifest", "sha256": "真实SHA"}},
  "historical_observation": {"tree_sha256": "RC4完整树", "report": {"path": "原报告", "sha256": "原SHA"}},
  "source_delta_audit": {"path": "逐源差异清单", "sha256": "真实SHA"},
  "claims": [{
    "name": "独立且完整限定的子结论",
    "classification": "SOURCE_INVARIANT_WITH_CURRENT_NATIVE_BRIDGE",
    "required_unchanged_dependencies": [{"path": "明确路径", "old_sha256": "旧SHA", "new_sha256": "同一SHA"}],
    "changed_dependency_edges": ["所有进入修改函数／on_action的边"],
    "current_native_bridge": [{"path": "真实RC5报告或SAV", "sha256": "真实SHA"}],
    "unverified_scope": ["未在RC5实际观察的行为"],
    "status": "PENDING"
  }]
}
```

验证器需重新算全部files差异、逐claim固定依赖白名单／调用边、旧报告原tree与新原生run／EXE／language、桥接实际checks及原字节；变化依赖未列、bridge缺失、旧FAIL／scoped遗漏、未知claim一律拒绝。需要从release case拆出逐check来源，而不是把一个历史PASS提升整个case；候选三政体月度样本和六core实际自然RNG矩阵不得改成历史源。不变dependency闭包仍经过新repair的PK后置结算／reload，不能白名单豁免。当前仅为设计建议，未实施、未批准任何跨tree PASS，也不建议为本轮引入该额外复杂度。

### nrel中途工具切换的补证建议

该问题与生产RC5无关：run`20261019T133314Z`仍是其原RC4树`06485…`，中途nrel worker86592使用了新截图枚举工具，不能更改旧run manifest使它看起来从一开始就在用新工具。应新建独立tool-source supplement／delta receipt，由归档线程按主线程授权保存原字节，至少包括：

- run_id、原manifest SHA／原生产tree、Stellaris PID及worker PID分别标注；worker启动时间／原始命令与实际nrel阶段白名单，不把worker PID当游戏PID。
- 旧runtime.py SHA `91b831241440a04ffa55d7226c7e2eb158907ebdc62054a906ff51e9f5e77adf`与新SHA `84b7fdda9489392f5abab5fc71c9bd61bcc5933185a02f7c6c479d703b155ffc`，实际新runtime与single／1015／1019／执行worker源字节及逐文件索引；原归档旧source继续不动。
- “新worker在工具封口后启动、源前后未变”的证据链与最早／最晚明确新工具action/OCR指纹；若没有采内存loaded-source证明，不把仅当前磁盘SHA称为已证所有历史进程加载SHA。边界不明的其它样本不得回填到新工具。
- 引用[截图枚举等价报告](evidence/1019-analysis/ocr-screenshot-scan-benchmark-v1.json)的3×15003完整path／mtime相同、[OCR等价报告](evidence/1019-analysis/ocr-session-reuse-benchmark-v1.json)的三帧完整输出相同，以及`testing/test_runtime_screenshot_scan.py`／[设计结果](ocr-session-reuse-1019.md)6项测试；明确没有改变Mod／F12新文件证明／mtime规则／OCR参数。

localization_docs线程已接此独立补充归档任务，并已收到稳定8文件路径／SHA与边界建议。本分析只引用，不创建第二份工具切换归档、不覆写其payload或旧manifest。后续新candidate run从启动就归档当时实际工具字节，仍要区分生产tree与工具版本；工具切换不产生一个伪造的新production run_id。

本轮仅生成此建议文档与原字节差异JSON，无UI／Steam／Git操作、无门禁／生产变更、无新的runtime PASS。
