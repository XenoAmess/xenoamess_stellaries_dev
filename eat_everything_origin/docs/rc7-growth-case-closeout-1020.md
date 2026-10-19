# RC7 两组成长检查的限定收口

## 目标、范围与验收标准

2026-10-20先记录本轮只读审查及新提案的设计：仅接收已冻结的RC7九节点十八原生样本、重复同步、实际同日加载、预算补发，以及高等级详情和报告UI证据，逐项映射现有发布门禁的 `unlimited_growth` 十项与 `random_components` 十三项原检查名。只新增本文与两组partial提案；不改Mod、工具、原报告、原SAV、归档、索引或正式发布结果，不操作游戏、桌面、Steam或Git。

候选树固定 `61b34f6dbdc277c44364889d5f1e1cd2773a4624786bbf0d538079fc6ba4feb0`，版本 `0.4.0-rc.7`，run `20261019T164112Z`。C0是RC6干净Machine年末存档在RC7中实际加载和保存的成长入口，不能证明RC7新游戏、首月就业或全年经济。`PASS_SCOPED`不自动成为整case通过。

新提案采用完整原检查名，明确已证据支持项为 `true`、未完成项为 `null`，两组status均为 `PENDING`，组件总体状态也保持 `PENDING`。每项写明原报告具体子区、证据路径及来源限制；项目相对引用必须存在且SHA逐字节一致。模型保持五版原SHA、每级及每core系数、原HP工程容差、1850检查的既定范围；不得重新拟合或扩大容差。高等级UI原v1选错关闭帧的失败、原strict21条差异必须保留。

完成标准是逐项检查名与当前 `publish_1019.py` 完全一致，所有新增引用存在且SHA复核正确，无未经实际证据支持的true；剩余实机步骤列成可交给主线程的清单。本文和partial提案不填 `final-result.json`，不代表发布验收完成。

## 审查结果

原生主报告 [rc7-growth-native-report-v1.json](evidence/1019-analysis/rc7-growth-native-report-v1.json) SHA `4677e82c62ce30851f247691dad38703f52d6187ce26f2e63ea9fe0d7df9d1a3` 是1850/1850、`PASS_SCOPED`：matrix1125、ordinary_controls616、repeat20、reload20、budget69。没有startup稳定性证明，原 `startup_stability=NOT_PROVIDED` 保留。其模型、系数、HP政策及全部原检查没有改动。

九节点为C0/9/10/19/20/49/50/200/10000，各有refresh/final十八个实际SAV；不是仅用九个摘要点代替原档。C10000实际六层shield/armor/hull/damage/tracking/regen为28/37/44/25/27/39，合计200；六种都有非零真实抽取记录。单次C20500同步只补200，产生R400/P10；原生下月自动补10到R410/P0，原预算报告只验账本计数，不把新核心的即时属性缓存当已刷新。

同日重复sync原生ZIP与此前final一致，SHA `f733e79be5cb9cac7ad9101fc171d5bf4ddfe5fdc7adce479c3b8dae6bd2eb52`。实际原生load/save后SHA `a1458045bc7b9bb18ea7ef91b539617a3f0b8e731b0911d8a06a33884a1390aa`，业务二十项保持，design ID 16777235→16777257但设计体SHA相同；并非全gamestate或全ZIP相等，也不是新进程重启。

高等级UI v2报告SHA `e52bcb0355ee29db8552c3b95ff450da9c6b11bc9029104ed8c5ba71e598dd29`，60/60 `PASS_SCOPED`。C20500、L2050、next10、B410/R410/P0及六层63/74/76/63/56/78在真实简体中文报告单页完整显示，关闭后同日业务状态保持。原v1误把点击前识别图当关闭证明的55/56 FAIL原样保留；修正只绑定真正点击后的frame。完整strict仍为21条FAIL：八个country展示缓存在两套投影中共16条，两个core展示缓存在两套投影中共4条，core原始块1条；两档并非字节相同。详情满血与旧C10000导出缓存不能证明实际恢复或C20500新modifier导出。

## unlimited_growth 原十项

| 原check | 提案 | 证据与剩余边界 |
| --- | --- | --- |
| count_level_samples | true | 原matrix十八SAV的C、L、next及country/fleet镜像，九节点全部通过。 |
| four_stats_five_percent_per_level | true | 原matrix固定源模型、独立C0截距、三防native max与十项export；分别剥离每级0.05与实际core贡献，非复利或面板DPS。 |
| daily_regeneration | null | 固定恢复export符合base+0.1L+0.2Nr；尚无实际受损舰按日自然恢复序列，不能用满血替代。 |
| single_scaled_modifier | true | C0无成长modifier；正L仅一个永久eep_mothership_evolution，multiplier=L，原生modifier列表与core归因均通过。 |
| repeated_sync_idempotent | true | 实际同日双sync，原二十项通过且ZIP不变。 |
| same_day_reload_idempotent | true | 实际同日原生load/save二十项业务与health保持；保留全字节不等及设计ID更换。 |
| destroyed_mother_not_respawned | null | 未有实际摧毁后initialize/startup/sync、monthly和load仍不复活的RC7组合证据。 |
| jump_and_shipyards_preserved | null | 所有SAV保留JUMP_DRIVE_1及相同装备体；仍缺实际jump订单、到达和冷却与移动船坞运行态证明。 |
| report_level_count_remainder | true | 真正简中UI v2、正确关闭后frame和前后SAV；保留原strict21差异与v1失败。 |
| invalid_or_cancelled_no_growth | null | 仍须原生无效目标、排队和取消分支的前后C/L/R/P/六层账本。 |

新 [unlimited partial提案](evidence/1019-analysis/rc7-unlimited-growth-partial-case-proposal-v1.json) SHA `1080572cc9162f00020c7aee6a008091f8a913fca53dfb52f22b686ea6181afd`：6项true、4项null、57个真实引用、整组PENDING。true只对表中范围成立。

## random_components 原十三项

| 原check | 提案 | 证据与剩余边界 |
| --- | --- | --- |
| real_component | true | 十八原生SAV实际AUX6..11六个具体组件及源triggered_ship_modifier。 |
| positive_effect_observed | true | 六种真实抽取皆非零，实际native三防max与十项exports对应正向贡献；不宣称实战DPS或自然修复。 |
| random_pool | true | 六层28/37/44/25/27/39皆有实际记录；不推断抽样均匀性。 |
| every_five_levels | true | B=floor(L/5)、R=sum六层、P和镜像覆盖边界，C50首次奖励；未用写tier命令冒充抽取。 |
| threshold_idempotent | true | C10000实际双sync、计数/health不变、原生ZIP不变。 |
| reload_persistent | true | 同进程真实原生reload保持六层、装备体与账本；不冒充新进程或pending重启。 |
| other_fleets_unchanged | null | 原616检查仅覆盖11普通舰身份及可用native最大H/A/S字段；没有它们的伤害、追踪、恢复exports，不外推全效果未变。 |
| equipped_component_present_in_native_design | true | 六个core各一个真实槽位，十八SAV及reload设计体保持。 |
| component_owns_dynamic_bonus | true | 实际tier与固定core payload逐项相符，剥离单level modifier及country/C0固定截距。 |
| no_external_reward_modifier | true | 无ship reward modifier；fleet只固定母舰modifier及单个成长modifier，核心效果由实际组件payload提供。 |
| native_component_effects_source_attributed | true | 原五版source链、独立C0、十exports/三max、原HP与数字合同全部保持。 |
| growth_component_contributions_separated | true | H+1500L+3000Nh，A+1287L+2574Na，S+2091.375L+4182.75Ns，damage+.05L+.05Nd，tracking+3Nt，固定regen+.1L+.2Nr。 |
| cross_threshold_catchup | true | 单次仅补200至R400/P10，原生下月再10至R410/P0；原69检查只接收counts。 |

新 [components partial提案](evidence/1019-analysis/rc7-random-components-partial-case-proposal-v1.json) SHA `22c45fae04f84fd3fc88bf0298179645f2338c556e74bfcea833f70533f0da2d`：12项true、1项null、42个真实引用，整组及component_rewards均PENDING。`component_attribution_report`明确指向canonical大包中的原1850报告，并列出全部十八native SHA与五source模型，供主线程审核后显式填入；本轮不自动promote。

## 尚须主线程实机与索引收口

1. 在独立功能分支采集真正受损母舰的日初/日末native健康及时间、战斗/维修环境，区分固定静态恢复、原有百分比AUTO_REPAIR、停靠维修与其它实际来源。源export已通过，无须重复整九节点矩阵；满血详情不是恢复证据。
2. 高等级实际母舰死亡后，分别重复完整initialize/startup/sync、原生下月与加载，确认没有新增母舰且历史六层/奖励账本保留。该分支不得污染经济轨迹。
3. 复用已规划Mother/Relic同国同日C0分支的实际跃迁出发订单、到达/冷却及十船坞证据；不能仅凭设计里有JUMP_DRIVE_1给true，也不能从growth设计体推断全部运行态。
4. 复用原生巨像guard、queue和cancel前后档，核对C/L/奖励和六层均无变化。实际完成分支另有奖励同步，勿用无效事件调用代替。
5. `other_fleets_unchanged`保持保守null。若最后采用“所有成长效果均不影响普通舰”的广义结论，仍需实际普通舰伤害/追踪/固定恢复export负对照；原三防616检查可以复用。不要为此把旧报告scope改成全channel，也不要重跑整九节点无新增问题的已通过测试。
6. 真实新进程重启和pending持久性属于独立 `candidate_reload` 组，不能由同进程C10000reload或manifest存在代替。原生process重启、P10加载与次月补10仍待主线程既定方案；本两提案不预填其它case。
7. 最终停机后将该run完整日志冻结一次，供两组共用。当前两包不含最终log；整组PENDING必须等实际剩余检查和共同review。index_prepare已登记唯一canonical manifest和raw，主线程只需attach这两个新proposal为analysis，逐check显式审查，不重复add-run或自动整体accept。

## 离线复核

本次逐字节复核两个提案全部引用，并将十/十三原check名对照当前发布器常量；两组均保留PENDING/null，未改任何原报告、原模型、源SAV、归档、工具或Mod。原1850检查分区、全部passed、五source SHA及十八不同native SHA已核对。全部新引用使用 `eat_everything_origin` 内相对路径，未把活动artifact绝对路径写进新提案；原报告中的历史绝对路径由已sealed原reference map保留并映射。

## 两项最小补充设计（先记录，尚未执行）

主线程追加授权仅离线设计普通舰十modifier负对照和受损自然恢复。拟新增 `evidence/1020-rc7-growth-minimal-probes-v1/`，只含新执行计划、原样一行控制台命令、对应去除console前缀的P语法包装、原生出处与SHA，以及现有open_kaishek CLI parse输出。绝不安装为Mod、调用UI、读取活动run日志或修改SAV；不修改任何工具。静态只能证明语法零诊断及出处匹配，不能提前给native实验true。

普通舰命令直接从 `tools/runtime_growth_1019.py:49` 的 `export_command()` 提取原十个export_modifier_to_variable，保持getter和 `eep_probe_*` 变量名逐字不变；仅将外层变成绑定Mother.owner的country.every_owned_ship，limit排除juggernaut。C0选择r7ganchor，C20500选择r7evreport，均同一来源银河，实际先验证原11普通舰ID/设计/owner仍存在，然后导出并各原生保存一次。不把读取diagnostic变量当舰体属性修改。实际普通舰身份之外若多出新对象，必须记录并按同ID交集比较，不能悄悄删除差异。

受损接口只用已经完成原生旧伤fixture所证实的正向effects：reduce_hp及reduce_shield，再damage_ship；原旧ldpaid真实清盾后damage_ship=120确实减甲120，不再采用旧“有护盾时damage_ship直伤甲”的未证推测。高L已有H3396960/A2873613.6/S4718142，设计一行reduce_shield=10000000、damage_ship=100000、reduce_hp=100000，保留大量舰体/装甲；原生必须确认清盾后伤甲、母舰存活及actual max不变，再原生FF1观察。此命令不是已运行或保证实际变化的结论。不开战、不生成敌舰、不调tier、不主动治疗、不使用负repair或编辑SAV。

恢复对照按实际native current/max、日期和五账本/六tiers，而非从UI满血推断；原两AUTO_REPAIR百分比通道、静态恢复和原生out-of-combat倍率须分别记录。若FF1不涨，保留失败/延时，不改成长系数：母舰具有移动星堡底盘，原版另有station10日/starbase30日self-repair计时，不能擅自把无增长归因于Mod。最低只承诺实际观察到的恢复事实，不在没有引擎公式证明时反推每类来源精确日恢复贡献。

### 已固定命令与静态结果

最小包 [plan.json](evidence/1020-rc7-growth-minimal-probes-v1/plan.json) SHA `d5a861bf24bbdcc96befed194fc5f54cb032c57e504a66e799b9f177e160175f` 固定命令及全部来源，不是已执行报告。普通舰原样一行 [ordinary-ten-modifiers.command.txt](evidence/1020-rc7-growth-minimal-probes-v1/ordinary-ten-modifiers.command.txt) 为1050字节命令加末尾LF；命令本体（不含LF）SHA `b1dc9e5f73d388af4172f55f394fc1a2599201c2b30316d064762e161e8d3ccc`，整个文件SHA `90f6c0e9c7f07b0862a2c9a665e0fd18b5483d430f7446f38a34e5d209ba39b0`。原十getter及变量名直接用AST读取collector `MODIFIERS/export_command`，无桌面import；collector SHA `cab98ce18119f27838456dd6118001cc7fee5254b3150c5e5c8fcf5365f7e747`。新增外层仅为：

```text
effect event_target:eep_mothership0.owner={every_owned_ship={limit={NOT={is_ship_size=juggernaut}} <原十export逐字保留>}}
```

上面缩写只解释scope，不应复制执行；完整可执行一行在命令文件中。原生已归档effects文档5839～5841明确every_owned_ship支持country/fleet并按limit筛选，triggers1083～1085明确is_ship_size支持ship；全部原件SHA见plan。**必须加载同来源银河的r7ganchor与r7evreport，比较原11舰0/1/2/3/4/5/804/805/806/807/808及其设计体、owner；不得换用三经济最后那个freshMachine新银河。** 这些普通舰包含真实民船/星基对象，报告按真实ship_size列出，不能一概称战斗舰。

母舰 [fourteen命令](evidence/1020-rc7-growth-minimal-probes-v1/mother-fourteen-modifiers.command.txt) 为原十项加已在原生registry登记的两add_perc、两regen_mult，命令本体SHA `a6104e9831da971111278c09712efeb26c5e15ce7f608c523079fc3cf66c62d8`、含LF文件SHA `837a5834bde0ad31a66a1d57d2cecb1d48e6139488a93dae5316594b289608a1`。它只写观察vars，不能调用repair或改变L/tier。

正向施伤原样一行为：

```text
effect event_target:eep_mothership0={every_owned_ship={reduce_shield=10000000 damage_ship=100000 reduce_hp=100000}}
```

命令本体SHA `a51ade77d1b45589909dadfb677ac071ede6dd1dfa95c295f5f95a1d361e0f61`，含LF [命令文件](evidence/1020-rc7-growth-minimal-probes-v1/mother-positive-damage.command.txt) SHA `f5b0fdedcf09dea153a0e1a666d0f2ef200a3e7c24b57d51e2b13b3283b98379`。沿旧真实ldpaid施伤顺序正向清盾后伤甲；旧原生实际减甲120由原action和report SHA绑定，不以只读原版注释冒充实际验证。本次量级尚待高L原生同日damage0验证，不能沿用旧120减甲数值。

本次使用现有open_kaishek提交 `9a286b9321a4d1ecacc0680a8bb0d914e0679b99`、既有JAR SHA `6ac143ebf03f3e1a041dff01b2d808e60de8e289d18cebf9855682f0a80b6d82`。三个命令去掉控制台前缀`effect `后，以单个命名scripted-effect包装，由CLI `parse --file` 分别返回PARSED、零diagnostics、roundTrip true，3/3通过，原stdout/argv保存在包内三个`.kaishek.json`。这与既有Mod包验收采用同一lossless语法入口；只代表语法，不认证新console执行、作用域对象存在或自然恢复引擎公式，不宣称新增Mod runtime通过。未修改open_kaishek或其它工具。

### 根线程执行的最少额外动作

1. load同银河r7ganchor；普通舰十项导出一次；新native save。
2. load同银河r7evreport；同普通舰十项导出一次、Mother十四项导出一次；新native save作为高L未伤before。
3. 暂停同日正向施伤一次；**先另存真实damage0**并复核当前三防/母舰存活/max不变/账本和tiers不变，不得施伤后直接FF而丢掉伤后起点。
4. 仅`fast_forward 1`，核对真实下一日，另存day1并比较恢复。只改health及观察vars，无手动治疗。若首日没有恢复，保留诊断并由主线程按实际状态决定有限追加少天；不自动循环、不无限加新测试、不要求重跑已通过矩阵。

合计最低2次load、4条effect、4次原生save与1条FF1。加载与原生保存所需的实际菜单关闭/确认/frame仍不可省略。所有结果目前 `PENDING_NATIVE_EXECUTION`；三个parse输出不改变上述两partial提案任何null或整组状态。最终复核三个命令文本无多行、UTF-8无BOM、包装等于原命令体、全部plan引用SHA一致；新包只包含文档证据及静态语法结果，不进入生产Mod。

## 跃迁与十船坞保留合同的补充只读调查

本轮受主线程明确授权，只读原有1019验收合同、现有check实现、已sealed `1020-rc7-native-jump-v1` 和原十八成长快照，判定 `jump_and_shipyards_preserved` 是否已可由同RC7真实跃迁与成长稳定性证据组合覆盖。优先沿既定合同收口，不自动新增高L跃迁、船坞建造或其它矩阵。原partial提案保持原字节，必要时另交新的事实性结论；不读活动r7pk或活动日志，不操作UI/Git，不修改工具或Mod。只有原合同确实要求而现有证据未覆盖时，才列出现有最短补充动作；不编新验收要求。

原1850报告显式证明各level装备/身份稳定，但没有命名的yard检查。为避免把摘要外推，本只读调查将直接从已sealed十八SAV提取Mother实际ship_size/required jump、mobile starbase绑定、shipyard_build_queue/owner/type/simultaneous和订单列表；先逐个核原ZIP SHA/CRC，再与原mother check的既有判据一致核查。新增独立 `evidence/1019-analysis/rc7-growth-jump-yard-contract-review-v1.json`，不改1850原报告或原partial；已有C0跃迁包只作同候选另一实例的实际能力正对照，不冒称成长实例曾在高L实跳。

主线程已明确按原合同采用上述组合覆盖，不追加高L重复实跳或造舰。审查后另建 `evidence/1019-analysis/rc7-growth-jump-yard-partial-case-proposal-v1.json`，只提案 `unlimited_growth.jump_and_shipyards_preserved=true`，整组PENDING/finalfalse/缺最终logs保持。原 `rc7-unlimited-growth-partial-case-proposal-v1.json` 中历史null及原字节SHA保持；本补充仅补现有单项，不推升daily_regeneration、destroyed_mother或invalid/cancel等其它项。

### 原合同解释与实际只读结果

原 [1019需求](requirements-2026-10-19.md) 的措辞是“进化不锁开局动力与船坞”，验收列“主动跃迁、十船坞”，没有要求L1000重新实际跳跃或重新付费建舰。原 [最少矩阵](acceptance-rc4-efficient-matrix-v1.md) 明确同SAV离线mother检查可核十并发移动船坞，“无需专为这些字段再操作配置页或保存新档”；主动跃迁另需实际运行证据。当前原checker `mother()` 的十船坞判据保持为：唯一mobile starbase的station绑定该Mother ship，其真实shipyard_build_queue存在且simultaneous=10，不要求新下造舰单或等待完工。本轮没有更改这些合同或判据。

新增 [只读组合报告](evidence/1019-analysis/rc7-growth-jump-yard-contract-review-v1.json) SHA `1d5c2a875934d89ecb25744ef8dd6a97d2e345b0c7728fcbd2cfa69152fc517e`，`PASS_SCOPED_COMBINED_EVIDENCE`。十八原ZIP的SHA及CRC先复核；每档十项原生字段核对共180项全部成立：Mother fleet125/ship809、juggernaut、唯一JUMP_DRIVE_1、唯一绑定mobile starbase15、原生juggernaut等级和starbase_shipyard类型、真实queue48/owner0/type ships/simultaneous10。十八档queue身份/元数据/空订单列表完全相同，C0至C10000及每个refresh/final都保留十并行能力；不称本轮有付费订单完成。

C0实际跃迁来自另一真实实例Mother151/ship1044，同一RC7树、相同固定生产设计；原25项jump观察与到达mother14项报告均通过。它实际从5→7，14日蓄能，Jan21到达并有原生cooldown与UI200日提示，移动后仍有十船坞。成长实例125/809在九节点十八档保留同一固定设计的JUMP_DRIVE_1及原生yard绑定。二者组合支持“能力未被进化锁住”这一原检查；**没有把151/1044写成125/809，也没有写成高L已经实跳**。保留两个实例、不同日期和不同分支的事实，不能推导高L实跳、边移动边造舰、最大跃迁距离或200日冷却结束。

因此无需新增高L跃迁或native造舰。此前本文表格/原partial中该项null是当时证据阶段快照，原件保持；现单独 [新增partial提案](evidence/1019-analysis/rc7-growth-jump-yard-partial-case-proposal-v1.json) SHA `eebdc0eae3f328934561eca949e3b8c5aec0b4267b170dafeff258f69c7ea9d4`，只支持 `jump_and_shipyards_preserved=true`，45个实际引用。该结论按原合同组合覆盖，交index_prepare显式合并，final_result_written=false、case_status=PENDING、最终logs缺口与其它未测check均保持，不改原1850/native/UI报告或旧partial字节。

只读采样的首次临时Python把growth_stages匿名对象列表交给具名fields解析而拒绝，未产生报告或改任何源；随即复用现有 `inspect_1019.design()` 的匿名列表解析，不改工具。最终十八档报告完整覆盖原全部phase，没有删失败原生样本、扩大HP政策或新增实机步骤。
