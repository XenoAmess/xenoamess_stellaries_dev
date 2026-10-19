# RC7敌星90／30完整发射：独立接收清单

## 目标、范围与当前状态

2026-10-20先登记本次接收方案。root独占实机；本线程只在root明确封口后接收其白名单原件，使用现有receiver／checker并独立读取原生订单、战争与人口状态，不改Mod／工具／存档，不操作UI／Steam／Git，不读取活动日志。archive_review负责selected、base／校准／取消包；本线程只新增此页及后续独立`docs/evidence/1020-rc7-pk-enemy-positive-v1/`，引用其封存包，不重复归档或改写。

当前没有完整shot；取消3／90及实际reload仍由root执行，不能认定正例通过。只读过已提交selected包、既有执行方案及原receiver／checker接口，未读取未封口cal／取消／完整发射的`r7pk*`原件。

候选固定`0.4.0-rc.7`、59文件树`61b34f6dbdc277c44364889d5f1e1cd2773a4624786bbf0d538079fc6ba4feb0`、run `20261019T164112Z`、简中单生产Mod、EXE SHA `400df27c82ddc845aa9dce79bd468d81f18f060d299cd263e3afa93aef4f7a83`。实际manifest SHA `603236aeedc59d2f0a0308b500ca209f589fb89e2ea5d1928c8bc04d10fedd86`。完整case终审仍需要停机后完整日志。

## 已有入口与边界

已提交`docs/evidence/1019-rc7-pk-enemy-selected-v1/index.json` SHA `ebee0665d37ec24b1e3896e2c1a419c50aa627e07db921fd4fd95a743d214b12`，其独立verify9项只证明字节及单角色观察，不证明开战、充能或结算。

selected为2201.01.21：victim country1、source物理17／原生colony1、pc_tundra、size21、真实Lithoid损耗deposit0、q21、实际人口4954；5个group均非actor founder，敌方返还期望0。core物理2／owner0，Mother fleet151／ship1044／design1844；C0／G0／D2／made0／worlds0／L0，六rank0。该入口只是绑定目标，**prefire必须重新读取活源owner、q、实际人口／group和core可用性**，不得把4954抄成后续人口。

方案登记时root已告知本银河scratch单位奖励worlds750／empires600，而校准包尚未封口；当时只作待接收值，不代替独立校准引用或继承旧RC6奖励。其后root明确封口，接收结果如下。

2026-10-20只读已封存`docs/evidence/1019-rc7-pk-crisis-baseline-v1/`，index SHA `0c62761bfaf7ec4d4e801052e19c02bd3b948fd1606a005212ce269c4eb37b23`、verify SHA `7a36f10317bdff6163716f38ca5dc0d03a1a7378557a184e0763c076e989e740`（12／12）。`authored/independent-crisis-calibration-v1.json` SHA `13af0b201319b15fe7b4a8abb30ed3cb019e2488bd83a7e9e465529a4dff2840`按两个原生命名objective独立观测worlds750／empires600，保留原样校准命令、物理Enter、实际Load回base及新存restored角色。两objective在restored均回空，EEP账本及源／core人口不变；原no-settlement9／9只证明未重复支付EEP收益。

原严格恢复比较72项差异及FAIL完整保留，含original_owner、设计索引、移动／军力缓存等；首次Load后原生council slots0→4，Mother design_id1844→16777234而原设计shape相同。本正例不能固定旧design1844不放；每个实际role重新读当前design_id并核shape／组件，不能因索引更新误判母舰替换，也不能宣称全存档无差异。

Jan21暂停base原生war0为country0攻击country1、进攻`wg_cleansing`；source17与Mother同origin81，Mother空订单、move_idle，无活动海战。全局ground_combat空，actor五支machine_defense均在本土colony0，无己方军队在敌源。该事实只限已封存日期，不能直接外推120天后prefire。本线程未重新执行校准或重审archive_review的原始151件归档；上述对象仅作后续canonical引用。

## root封口后的最短接收顺序

1. 按root指定完整角色名和白名单前缀逐件核对SAV、native-save receipt、audit、manifest、SHA与日期；原路径保留共目录关系，原始输入／失败帧不改。已完成receipt metadata允许跨prefix供原inspector provenance查找；不因此读取其它原始SAV／图／日志。
2. 引用已封存base／校准／cancel-reload包，确认恢复后的source17仍活、core2归owner0、真实war仍有效、Mother唯一且账本未因scratch／队列／取消增加。只读原生战争参与方／目标关系与军队／运输／ground状态，避免把selected或命令文本本身当实机资格。
3. 接收requeued→windup_last→fire_start→prefire→immediate→stable；每个节点独立提取同fleet151／ship1044订单、source17、core2和全EEP账本。移动日不算90天充能；从实际子订单计数定位边界，不由点击日或保存名推断。
4. 以prefire实际活源定义结算case，用原receiver调用原settlement；独立核受益国、人口来源与原生星球／殖民地／灭国清理。immediate与stable分别保留，不能把稳定前未清理状态抹成已通过。
5. 对root之后实际完成的destroyed-source duplicate／真实reload另接收，同日调用原no-settlement并保留strict差异；若尚未交接，仅把相应最终check保持null，不补造角色。
6. 归档此次白名单原件及原receiver输出／cache／独立报告／partial proposal，已有source20、manifest和selected／base／cal／cancel包用canonical路径＋SHA引用；独立重读所有payload和引用后封口。完整case保持PENDING直到日志与共同终审。

| 语义角色 | 从本次实际原生状态验收 | 不代替的事实 |
| --- | --- | --- |
| `requeued` | 真正重新右键“拆解星球”；`destroy_planet_order.planet=17`；仍活源且无EEP收益 | 不从首次cancel订单延续充能 |
| `windup_last` | 当前子订单`planet_killer_weapon_windup_order`，实际89／90 | 不从FF天数猜完整充能 |
| `fire_start` | 当前子订单切为`planet_killer_weapon_fire_order`，实际fire0或1、fire_time30 | 不把windup结束当已摧毁 |
| `prefire` | 实际fire29／30；source17仍殖民、owner1／war有效，当前size与真实损耗、population／group可读，core2仍owner0 | 不由after收益倒推q／返还／人口 |
| `immediate` | 1日自然完成后的真实星球／owner／实际population、订单和receipt状态 | 不假设最后殖民地灭国缓存即时完成 |
| `stable` | 原生清理后source17破碎、owner／controller无、实际population／group／job空；受益国EEP及worlds／empires奖励 | 不把延后灭国奖励误算成第二次收益 |
| `duplicate`／`duplicate_reload` | 仅已毁receipt源的既有callback、真实reload后再次callback；同日无额外结算 | 不用回调代替实际90／30发射 |

## 原工具接口与最小任务

原receiver SHA `d4daa66a575fa8c0ce5bba9796b6c6d4eef0b0573184ec9b6c4e5102fd033ca5`；checker SHA `681836d2da9c6b28ee9bfd583c87e5ced96f06543901e71d3dc35fa226f3afdc`；inspector SHA `1ec3ad71f877be5704959134b76e59be077b756a906f7297f278613ee8bfbf92`；publisher-interface SHA `06c60c0a9bd406580314999ae6649365bb5c1fa6c7152c0b0a7fb5a420e06918`。工具接口未变；在角色封口后生成当前模板，不复用旧模板的接口SHA。

```powershell
python -B eat_everything_origin/tools/receive_functional_1019.py template --output '<新模板.json>'
python -B eat_everything_origin/tools/receive_functional_1019.py receive --intake '<已按实际角色绑定的intake.json>' --cache-dir '<本包新cache>' --output '<原receiver报告.json>'
```

本次intake `world_ids=[2,17]`；每role必须带实际`kind=native_ui_save`或真实autosave类型以及save／receipt／audit精确路径和SHA。`validate_role`要求receipt指向**该确切原路径**，即便两个SAV同SHA也不能互换；封存映射另存，原receipt不改。

最小任务为prefire→stable的原`settlement`，以及已提供同日duplicate链的原`no-settlement`；实际稳定C值可用现有`growth`复核。原receiver按角色可输出订单，但不证明原生物理点击、真实war／no_army或人口归因，独立报告补这些已有验收项。原工具始终输出18组PENDING，不改工具来直接填最终通过。

settlement-case按原schema明确：`schema=eep.1019.settlement-case.v1`、`path=colossus`、`source_world=17`、`core_world=2`、`native=false`、实际prefire得到的`expected_q`与敌方`expected_return=0`、独立确定的`expected_other_core_pop_delta`、本银河worlds／empires单位奖励及校准path／SHA。若prefire与stable跨月导致核心自然变化，按既有方案保留独立人口证据；不把after人口残差填回expected_other_core_pop_delta。

若prefire仍q21、before账本仍C0／G0，则公式事前为C21／G21／D7／made300／worlds1／L2，下一升级还需9，容量增加5。这个条件预期只作公式，最终用actual before值推导；不把它提前记为观察结果。Enemy return0不依赖当前总人口与selected4954一致。

## partial proposal的原check名称与支持范围

| 原case_id | 本完整敌星shot可支持的原check | 仍由其它实际分支支持 |
| --- | --- | --- |
| `colossus_enemy_fire` | `native_charge_and_fire`、`enemy_colony_destroyed`、`war_target`、`no_army`、`beneficiary_is_core_owner` | `owned_noncore_colony_fire`等待独立Lithoid自有星 |
| `common_settlement` | `q_c_g_d_match`、`population_matches`、`core_capacity_matches`、`enemy_population_not_returned`；`settlement_and_destruction_once`须同时有实际duplicate链 | `native_devour_loss_deducted`、`owned_main_species_return`、`lithoid_native_branch`等待对应正例 |
| `colossus_cancel_idempotence` | `repeat_event_no_reward`、`reload_no_reward`、`crisis_objective_once`仅在稳定结算＋实际重复／reload链各自完成后支持 | `queue_no_reward`、`cancel_no_reward`由archive_review的实际取消包，不在本包重做 |

所有check仅按已交接事实逐项true或null，不从一次settlement PASS推成整个case PASS；不新造测试矩阵。完整shot尚未交接时本页只处于PREPARED，最终日志仍缺，当前未产生任何正例PASS。

## 首个闭合角色：重新排队（接收前登记）

root明确封口`enemy_requeued=r7pkfirerequeued.sav`，2201.01.27，SHA `73421574dd6f6f2fc08b95dc25aaa88da5d152cd0b5824dfddb119d8ad946714`及同stem receipt／audit。白名单严格为`r7pkfirerequeued`后接`.`或`-`，以及`r7pkfire-select-mother-after-cancel-reload*`、`r7pkfire-ready-target*`、`r7pkfire-open-target-context*`、`r7pkfire-target-context-menu*`、`r7pkfire-click-native-dismantle*`。

before由root单独授权`r7pkshotcancelreload.sav` SHA `895c2b1beb85b2ac688cf0c2271f28aaedeacdbf667ef35db4969147d91c9053`及同stem receipt／audit、`r7pkshotcancelreload`后接`.`或`-`的文件；取消整包仍在archive_review封存，不读取未封包。源17／core2、同run和manifest保持本页固定值，Mother当前设计索引必须实际读取。仅使用原receiver记录两角色、同日原no-settlement和真实重新排队订单／输入链，不提前声明90／30发射。`r7pkfirewind1`明确活动，禁止读取。

本阶段派生报告将新增版本文件，已有selected／cal／cancel包不改。先读取精确授权文件清单和固定receipt，核字节后生成新intake／cache；before原件先引用其确切授权路径，待取消包封口后再引用canonical归档，不重复收其全包。报告最终检查保持PENDING／null，只记录重新排队阶段的限定事实。

为使已闭合角色可单独封口，本阶段使用独立`docs/evidence/1020-rc7-pk-enemy-requeued-v1/`；后续完整positive包只引用此阶段，不反复改本阶段文件。该包只收31件已白名单重新排队原件，before的cancelreload三件在原receiver中按root明确授权原路径读取，归档层等待取消包canonical引用。原receiver缓存与同日no-settlement属于本次实际执行，队列变化的strict差异如实保留。

## 充能首日：新增闭合角色（接收前登记）

root随后封口`enemy_charge_start=r7pkfirewind1.sav`，2201.01.28，SHA `bdcc0b6649fd6e4ebfd1e8a674ae412a7f1eddc4814380d0f95e662a656f2bd1`、同stem后接`.`或`-`，以及`r7pkfire-first-day*`。其预期原生订单由重新排队Jan27 windup0／90变为Jan28 windup1／90，planet17、order_id2、可达，证明重新从零计时。仍需本次独立解析；跨日不运行要求同日的no-settlement冒充通过，只逐项核EEP成长／收益账本和订单推进，保留自然经济／研究差异。

从原receiver缓存复用已完成观察，仅新增该SAV观察；实际后续包只引用首阶段canonical，不改首阶段已封对象。本次生成受控独立派生报告，不改原工具；`r7pkfirewind89`、`r7pkfire-advance-to-windup-last*`和`r7pkfire-windup-last*`尚在活动，禁止读取。既有正例before已经存在的`crisobj_destroy_enemy_ships=45`不算PK收益，worlds／empires仍各自独立比较。

首日阶段使用`docs/evidence/1020-rc7-pk-enemy-charge-start-v1/`，原receiver只新增观察`enemy_charge_start`，前一阶段缓存以canonical引用作跨日订单／账本比较，不再对before重跑observer。本阶段不增加原final checks或任何90／30完成断言。

## 两个早期闭合阶段的接收结果

重新排队原receiver EXIT0、`OBSERVATION_ONLY`，同日cancelreload→requeued原no-settlement9／9 `PASS_SCOPED`。原strict3项订单变化及FAIL保留。Jan27同Mother fleet151／ship1044当前design16777250；before空订单，after真实`destroy_planet_order.planet=17`、order_id2、windup0／90、can_reach=yes。实际源17仍pc_tundra／owner1／q21／人口4954，core2仍owner0／人口4859，完整EEP国家变量不变，C0／G0／D2／made0／worlds0／L0／六rank0。

已直接目视原始`r7pkfire-target-context-menu.jpg`：简中“拆解星球EEP_R6_ENEMY”；对应OCR行box493–620／489–506，实际client click为(620,497)，原输入链与菜单帧均留存。原生战争／军队上下文另读两份授权SAV，保留实际war raw、全局地战空、本土5支machine_defense及敌源守军，没有把敌方守军存在误算成己方陆军登陆。此结论只覆盖这两个暂停角色，不延伸后续日期。

首日原receiver只观察新增Jan28角色，EXIT0、`OBSERVATION_ONLY`；canonical复用重新排队cache。原生同planet17、order_id2、Mother151／1044／design16777250从0／90推进到1／90，实际`fast_forward 1`与物理Enter对应；跨日未调用同日no-settlement。源／core人口、全部EEP变量均未变化，已有`crisobj_destroy_enemy_ships=45`保持，worlds／empires仍空。这是1／90的限定通过，未完成90／30。

| 独立封口阶段包 | payload／raw／canonical | 原检查及独立复核 |
| --- | --- | --- |
| `docs/evidence/1020-rc7-pk-enemy-requeued-v1/` | 43 payload，2,694,331字节；31 raw，1,959,968字节；40 canonical；含index／verify共45文件 | 原no-settlement9／9；限定排队14项；归档12／12、327 typed refs |
| `docs/evidence/1020-rc7-pk-enemy-charge-start-v1/` | 43 payload，2,522,420字节；35 raw，2,172,893字节；45 canonical；含index／verify共45文件 | 新角色原receiver；限定首日15项；归档11／11、180 typed refs |

| 对象 | SHA-256 |
| --- | --- |
| requeued `archive-index.json` | `ecca5735c419a0b85fd34b48d603856f5609eab290bb96b5c851890a9a698770` |
| requeued `verification-v1.json` | `26104bc804b3c7aae0e3bd55038cfdf3e7f194adb35673b8d47faea15cc4ac86` |
| requeued `authored/enemy-requeued-summary-v1.json` | `a21b52971279ea17190263091004e5de26d53195a7cbbbd08b20d5068587afe9` |
| charge-start `archive-index.json` | `f767ea6571827d9c8f66baa09f9a29a93dbf842989d3e91d2825033fa145a648` |
| charge-start `verification-v1.json` | `1a52902679df4f57176f27bcd3e04452d21ed14f15428cd2a5b1c5a3eb41af95` |
| charge-start `authored/charge-start-summary-v1.json` | `1f0d1f492526daefef852ee2953228654856e1296f940505e51e24efe61cd5a0` |

取消包封口后只引用其index／verify及cancelreload三件canonical，未重复收取消前缀；生产执行源和manifest继续canonical复用。重新排队观察前后77个已完成receipt metadata全部原样，未以metadata读取授权扩展任何活动SAV／GPU／日志。原receiver的18组138个final check全部保持null／PENDING，两包`final_checks_supported={}`；这里只完成首两阶段，不能在最终索引中把完整shot升级通过。

离线派生命令一次遗漏显式UTF-8，读取OCR即退出，随后显式UTF-8修正；一次私有归档核验误将payload相对`.gitattributes`解析到Mod根而停止，改为明确bundle-relative优先后重新核验通过。两次均未改原工具／原件或已封包，也未把失败输出写成PASS报告。

root另已交接长FF后保存过早的失败diagnostic：名称wind89实际55／90、日期Mar22、无native-save receipt；当前本线程尚未获准读取其原件，未收为89／90，也未补造receipt。待后续恢复与完整shot实际角色封口，再在新的completion接收文档／包中接续，不改这两个已封阶段包。
