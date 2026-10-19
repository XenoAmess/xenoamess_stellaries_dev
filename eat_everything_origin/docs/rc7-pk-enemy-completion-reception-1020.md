# RC7敌星自然完成与结算接收

## 目标、范围、设计与验收

2026-10-20先登记最后发射日的接收。本页与新`docs/evidence/1020-rc7-pk-enemy-completion-v1/`承接已封前三阶段；旧文档／包、Mod、工具与存档不改，不操作UI／Steam／Git，不读取活动日志。只接收root逐次明确封口的原件；现只有prefire闭合，最后一天／immediate／自然完成可见帧等活动原件禁止读取。

固定候选`0.4.0-rc.7`、59文件树`61b34f6dbdc277c44364889d5f1e1cd2773a4624786bbf0d538079fc6ba4feb0`、run `20261019T164112Z`、manifest SHA `603236aeedc59d2f0a0308b500ca209f589fb89e2ea5d1928c8bc04d10fedd86`、简中单生产Mod与既有原receiver／checker。前三阶段canonical引用，不重复observe或归档其原件。

root封口`enemy_prefire=r7pkfireprefire.sav`，2201.05.26，SHA `7ebbaff3d0af80b4e1adfffbdedc4a7c2065507bceb9d953292a66c570a52887`及同stem后接`.`或`-`。白名单仅`r7pkfire-advance-to-fire-last*`、`r7pkfire-observe-fire-last-date*`、`r7pkfire-prefire-console*`／`debug*`／`visible*`及`r7pkfire-select-at-prefire*`；原inspector跨prefix仅可读root授权的完成receipt metadata。新intake先仅原receiver观察prefire，当前不运行没有after的settlement，也不凭fire29／30认定已发射完成。

事前期待已由root在最后1日前固定于`docs/rc7-enemy-prefire-expectations-1020.md`，SHA `b67cb2ce41d22635c017cc80b5274d7a401af45ea3eb47272a32245791d8fd13`。本包保存其当时原字节快照：q21、敌方返还R0、C21／G21／D7／累计made300／worlds1／Mother L2／六rank0、核心容量2→7，核心人口4877＋300＋R0＋other0＝5177。other0依据prefire两组current／month_start分别2700／2700和2177／2177、current-month growth detail空、May26→27同月；它是预先期待，不冒称通用引擎时序证明，不得从after人口残差回填。任何不符先保留原FAIL，再调查实际原因。

独立prefire必须重新读source17活殖民地、owner1／q21（size21减真实损耗0）／人口4966／各group非actor founder，core2仍owner0／容量2／人口4877，Mother151／1044的order2／planet17／实际fire29／fire_time30／可达，真实war、无己方陆军参战与global ground_combat空，全部EEP账本未结算。既有enemy-ships危机进度单列；worlds750／empires600来自已封本银河独立校准，不从总危机差推算。

后续只在root封口后追加immediate、native cleanup stable、destroyed-source重复callback／真实reload。原settlement-case按实际prefire和各after路径分别运行，schema／path／q／native=false／return0／other0及校准引用全部显式；最后殖民地国家若尚未清理，immediate原FAIL保留，stable另报告。跨日核心自然人口变化若不符合事前0，不能用after残差修饰原期望。所有严格差异和原始缓存保留。

最后完整输入／原生订单／war和军队／真实破碎与清人口／EEP收益／危机奖励／幂等链共同支持原case的逐check true或null；单次原settlement PASS不代表90／30、无陆军或完整case通过。自有Lithoid星、普通吞噬、guards、重启仍各自独立。完整case保留PENDING直至本run停机日志和共同终审。

## 接收状态

当前只有prefire封口，尚无after角色；完整shot与结算均PENDING。

首份原receiver已EXIT0、`OBSERVATION_ONLY`，只观察May26 prefire角色，没有运行settlement。独立prefire限定15项通过：fire29／30、order2／planet17／可达，source size21／损耗0／q21／owner1／人口4966；按实际actor founder3305111553逐组求和，source返还0。core2 owner0／人口4877／容量2，5支actor machine_defense均位于本土colony0，全局ground_combat空，原生war0仍actor0对country1、wg_cleansing。

原生`current_month_growth_data`整块**存在**，其`growth_and_size`明确month_start_size4877／growth0，主体两组为2700／2700和2177／2177；全部原始colony／group文本保留。事前期待文档所说的空增长明细不解读成整个data块不存在；只以当前growth0和组内month_start对照记录其事前依据，仍不证明普遍时序。enemy-ships objective为60，worlds／empires空，EEP C0／G0／D2等仍未结算。期望other0／核心5177保持事前值。

## immediate追加交接（接收前登记）

root封口`enemy_immediate=r7pkfireimmediate.sav`，2201.05.27，SHA `e0a604f835f86fe2e5bf1396b99a54c835cb3d406ac3bd5422c7fd0a6db10dc7`及同stem后接`.`或`-`；准许`r7pkfire-complete-native-final-firing-day*`、`r7pkfire-observe-natural-completion-date*`、`r7pkfire-immediate-console*`／`debug*`及`r7pkfire-natural-completion-visible*`。root交接源17已pc_shattered／无owner、q21／old_damage0／done flags，C21／G21／D7／made300／worlds1／L2／next9／R0／六rank0、corecap7／pop5177、订单空；这些仍逐项独立原生复核，不用after残差设置预期。

原生country1尚缓存存在，worlds750、ships60、empires尚无。先新增intake-v2和独立prefire→immediate原settlement任务，仍用事前worlds750／empires600固定值；若empires未清理而FAIL，保留该原报告及EXIT2，不把预期改0换PASS，不标once通过。后续stable另任务判断自然country清理；v2原报告不覆盖。新stable1／wait-native-country-cleanup／observe-stable／stable-debug／close-known-console等活动前缀禁止读取。

实际v2原receiver报告`INCOMPLETE`，原settlement25项为23 true／2 false：`separate_empire_crisis_reward_matches_explicit_expectation`为0对固定600；`source_colony_destroyed`的实际人口／group／job列表均空、owner／controller无、pc_shattered均true，但残留colony1的原生population counters尚非0。原FAIL完整保留，不能只报公式通过。原Python实现非零返回2，外层PowerShell执行器报告exit1；没有成功退出声明。

原生core人口5177、q／G差21、made300、capacity差5／最终7、return0和worlds750均命中事前固定期待；source实际人口0，q21／old_damage0，5个原checker receipt flags均在。源完整flags另含`3_year_owner_change_flag`与`nomad_recent_combat`，完整列表保留，不把它们算成EEP完成receipt。country1仍保留含历史人口的raw cache。待后续stable实际清理结果，再运行新的固定期待任务；不覆盖v2两项FAIL或拟合other0。

## stable1失败诊断追加（接收前登记）

root封口`r7pkfirestable1.sav`，2201.05.28，SHA `8a1ac05027925032bfcf1915ddc933aeb24af4cbae6e3f0f45992e0e190f9126`及同stem后接`.`或`-`；准许`r7pkfire-wait-native-country-cleanup*`、`r7pkfire-observe-stable-date*`、`r7pkfire-stable-close-known-console*`、`r7pkfire-stable-debug*`。原生country1此时已灭国清理，actor world750／empire600／ships60，但保存调用仍要求audit countries(0,1)，原auditor正确拒绝不存在国家1，SAV已复制而未生成audit或native-save receipt。独立原字节及ZIP／清理状态只作diagnostic，不作为receiver角色、不合成缺失文件。root改为(0,)同日原生新保存stable2，当前该stem活动，禁止读取；后续正式角色再独立封口接收。

独立诊断已核May28原生ZIP：country1对象不存在，worlds750／empires600／ships60；旧colony1历史对象仍在，但此前非零`employable_pops`字段已消失，实际group／job仍空。整个历史colony raw保留，不因其其它旧缓存非0就假定活殖民地，也不借诊断角色提前标原settlement PASS。36件已封诊断／清理原件原字节归档，原SAV缺audit／receipt均如实保留；目前只等待新stable2合法角色。

## 正式stable2交接（接收前登记）

root封口`enemy_stable=r7pkfirestable2.sav`，2201.05.28，SHA `8a1ac05027925032bfcf1915ddc933aeb24af4cbae6e3f0f45992e0e190f9126`及同stem后接`.`或`-`。ZIP与失败stable1相同，但该次合法原生保存仅请求仍存在的actor0，具有自己确切路径的audit／native-save receipt；不能据同SHA把缺回执stable1改称成功角色。

新增intake-v3：复用本包prefire／immediate缓存，新增合法stable2观察；只对prefire→stable运行原固定25项settlement，事前q21／return0／other0／world750／empire600不变，仍在May26→May28同月范围如实核人口。v2的immediate双FAIL另留不覆盖，不夹在v3中伪装成已通过；stable结果独立报告。root新增duplicate／dupereload／dispatch／actualreload等前缀活动，禁止读取。

正式v3已EXIT0、`OBSERVATION_ONLY`，原prefire→stable固定settlement25／25 `PASS_SCOPED`。source pc_shattered／无owner／controller、实际人口／group／job空及live counters zero-or-absent均成立，仍保留历史colony1引用；worlds差750、empires差600各自命中独立校准。C差21／G差21／made300／R0、核心人口4877→5177、容量2→7，全部按事前固定q／other0公式命中，没有修订期待或通过after残差归因。完整EEP与Mother当前level／modifier另留原值，immediate23／25双FAIL报告不改。

此处只完成正式结算检查，重复callback与真实reload尚未交接；最终原case逐check支持与归档封口待最后幂等链一起完成，不能先写完整case PASS。

## duplicate追加交接（接收前登记）

root封口`enemy_duplicate=r7pkfireduplicate.sav`，2201.05.28，SHA与stable2同为`8a1ac05027925032bfcf1915ddc933aeb24af4cbae6e3f0f45992e0e190f9126`；只准许同stem后接`.`或`-`及`r7pkfire-dispatch-two-completed-source-callbacks*`。原资产`testing/colossus_1019_postfire_plan.json`的`duplicate_destroyed_enemy_twice`877字符命令须与真实type_text／Enter逐字核对；ROOT为已毁source17、FROM为真实Mother fleet151，已毁／receipt／事件目标等limit从该次实际状态核对。A/B日志标记只能待停机完整日志复核，当前不读活动日志。

新增intake-v4合法duplicate角色并复用同SHA已核缓存，仍严格核其自身真实receipt／audit的路径，运行stable→duplicate同日原no-settlement；同ZIP相同不等于实际输入已被证明，须另绑真实命令／Enter。actual-reload-duplicate／dispatch-callback-after-real-reload／dupereload等后续前缀仍活动，禁止读取，待正式交接再接续。

v4原receiver已EXIT0，全部角色缓存复用；stable→duplicate原同日no-settlement9／9 `PASS_SCOPED`，full strict亦PASS_SCOPED／0差异。实际type_text逐字等877字符原命令且submitted=true，原生source17已毁／receipt及fleet151／core2绑定等前提可由同ZIP稳定态独立核对。输入／原生无变化已闭合，A/B标记仍待最终停机日志，不在此处认证日志。

## 真实reload后再次回调交接（接收前登记）

root封口`enemy_duplicate_reload=r7pkfiredupereload.sav`，2201.05.28，SHA `c11216d66545c69aacf5686e80a0ad68fa049a8640ef3fbd25663f70e86d0cc6`，并明确整个`r7pkfire*`前缀全部停止写入。最后批次`r7pkfire-actual-reload-duplicate*`、`r7pkfire-dispatch-callback-after-real-reload*`与dupereload同stem后接`.`或`-`可接收；旧三个阶段包只canonical引用，不重归档或修改。新`r7normal*`活动前缀及活动日志禁止读取。

新增intake-v5合法reload角色，复用其余缓存；原固定settlement加入真实reload检查，重复回调前后及真实reload后分别运行原同日no-settlement，完整strict差异原样保留，不冒称全ZIP相同。779字符原资产命令／物理Enter与实际native-load源SHA、日期输入链逐件绑定。source17已毁状态及ROOT／FROMfleet151前提核对，dispatch A／B／AFTER_RELOAD日志标记仍缺停机完整日志。

统一封存前检查整个已封`r7pkfire*`清单：前三包已归档对象只引用，当前completion已收对象不重复，其余已完成尾部原件另增raw-copy批次。最后提案只列原case可支持true与未覆盖null：敌星完整shot五项，自有星项等Li；common的敌方公式／人口／容量／敌方不返还／一次结算按实际链支持，normal／Li项不推断；取消的排队／取消由既有取消包提供，当前只补重复／reload／危机一次。所有case仍PENDING，原immediate两FAIL与stable1缺回执诊断不改。

## 最终限定结果与封口

最终v5原receiver已EXIT0／`OBSERVATION_ONLY`：prefire→stable加实际reload为26／26 `PASS_SCOPED`，stable→duplicate和duplicate→真实reload再callback各9／9 `PASS_SCOPED`。前者完整strict为0差异PASS；后者完整strict为47差异FAIL，原报告及独立整份strict副本均保留。变化包括核心amenities／housing／stability缓存重算、已毁colony历史字段清理、军力、普通空间站design索引、carrier flags等；没有把全SAV／全玩法字段宣称恒等。EEP完整变量、核心人口5177／容量7、worlds750／empires600／既有ships60保持，不发生第二次结算。

实际native-load输入来自`r7pkfireduplicate.sav`、SHA `8a1ac05027925032bfcf1915ddc933aeb24af4cbae6e3f0f45992e0e190f9126`、May28；其`state_verified=false`原值保留，状态证明来自随后真实另存并audit的dupereload角色。779字符原命令与Enter逐字核对，load时间先于命令输入。稳定态与duplicate虽然全ZIP同字节，仍各自绑定确切路径的真实native-save receipt／audit；failed stable1不冒充这两个合法角色。原3个dispatch日志标记仍待停止后日志复核。

实际原生完整shot由同order2／target17／Mother151／1044串联：Jan27 windup0／90，Jan28 1／90，Apr26 89／90，Apr27 fire0／30，May26 fire29／30，May27订单完成与实际源破碎，May28原生灭国／live counters清理。实际简中GPU已目视菜单、fire0%及prefire96%；May27远景只作为实际日期／完成后画面保留，`pc_shattered`和清人口依据原生SAV，不由远景猜测。

完成报告限定21项事实通过；独立归档24／24通过，1166个typed refs逐件核SHA。新包`docs/evidence/1020-rc7-pk-enemy-completion-v1/`共280文件，278 payload共16,296,293字节，含236原件共13,979,676字节、50对原GPU／OCR、4份唯一SAV cache、58个canonical引用。整个冻结`r7pkfire*`清单440件，前三阶段204件只引用，本包236件完整覆盖尾部；未读新normal原生内容／截图或活动日志。原inspector的跨前缀例外仅为root授权已完成receipt metadata。

| 封口对象 | SHA-256 |
| --- | --- |
| `archive-index.json` | `5a31463aaa8fd209aa419b63600972ecd25f2226a8acc40302f9ec3e335f8e8d` |
| `verification-v1.json` | `0dec9389fa0ae05a1545a7eda0c665ea2eb277f9e650e084ff9d72779418779d` |
| `authored/enemy-native-shot-completion-report-v1.json` | `cdb5b45d704d4d98ac102dee7ea6aa9cd9918bba5c9dd3590ecd990e6824b0e0` |
| `partial-case-proposals-v1.json` | `76f747bad5064a913cea62fcba9b331ad423df19c2c35de26df8c65067c05d65` |
| `partial-colossus-enemy-fire-v1.json` | `62b3b1c25d2bd9684b1024f38a1906f08fd3fe40f5c89ffdd30d5c467b72b47b` |
| `partial-common-settlement-enemy-v1.json` | `40a3401cd81b2d61f6e4e3303d9be139a6de3f2794aeda53edde4bd3e2f7b347` |
| `partial-colossus-cancel-idempotence-v1.json` | `d3db5bf9bd8551fa100aa810517a57c9707ae8f5c5768b96613926ef5b1bfd54` |

13项部分提案严格用原check名，三个case均`PENDING`，未覆盖null只列于`checks_not_inferred_here`，不得把别处已有true重置：

| 原case_id | 本包supported true | 本包不推断 |
| --- | --- | --- |
| `colossus_enemy_fire` | `native_charge_and_fire`、`enemy_colony_destroyed`、`war_target`、`no_army`、`beneficiary_is_core_owner` | `owned_noncore_colony_fire`待Li |
| `common_settlement` | `q_c_g_d_match`、`population_matches`、`core_capacity_matches`、`enemy_population_not_returned`、`settlement_and_destruction_once` | `native_devour_loss_deducted`、`owned_main_species_return`、`lithoid_native_branch`等对应路径 |
| `colossus_cancel_idempotence` | `repeat_event_no_reward`、`reload_no_reward`、`crisis_objective_once` | `queue_no_reward`、`cancel_no_reward`只由既有取消包提供 |

原receiver18组138个final check仍全部null／PENDING，部分提案不改原工具输出；最终索引线程可逐项观察，整组仍缺冻结完整日志、dispatch标记与其它路径／共同终审。本线程没有Git／Steam／UI／Mod／工具改动。一次私有战争列表解析误将匿名列表交给只解析具名字段的helper，在写报告前退出；改用原始已保留列表内的明确country字段读取后完成六项资格事实核对，原工具和原件不改。
