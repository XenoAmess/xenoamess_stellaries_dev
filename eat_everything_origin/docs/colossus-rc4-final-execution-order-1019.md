# RC4 收尾：最少重载顺序与母舰损毁证明

## 目标与边界

本页只读整合既有39命令计划；不降低验收门槛，不改Mod/工具/SAV，不执行UI或销毁。所有未来步骤PENDING。当前run `20261019T133314Z`，manifest SHA256 `557a73280c6d263fbe7ce5723e15d19154e209acf57c81bc22bec275401ffa79`，冻结树仍`06485dc540a88b30cef15c27c323ff21cd88f04ad57b79e4f5bc0590937ef468`/59文件。旧迁移仍由主线程先收尾；以下建议避免重复发射、重复采月及为恢复状态额外load。

## 一页执行顺序

| 顺序 | 分支与必要锚点 | 可共用的操作／证据 |
| --- | --- | --- |
| 1 | 当前公开0.3.1与付费队列旧档迁移各自完成 | 保持各来源before→after→reload，不互相代替。若取消后reload仍欠证，使用已导入r4cancelsrc一次load/save；已有证据直接复用。 |
| 2 | 本进程加载r4restartsrc，存candidate-restart | 该导入件来自前进程pk2dupereload，SHA `86c1f000b1adcf260f27d0cd2ae23fb13e8b2e98045425197c92d0962d152408`。结合真实新PID/启动日志，覆盖跨进程重启；同次核C19/G19/D6/made300/worlds1、母舰/组件、重复完成不再付。不要另开一个只为同样加载的进程。 |
| 3 | 同分支建Machine q2/50，保存owned-ready，再真实普通决议 | 同暂停日存normal-start，证明source50→100/core−50、合计守恒、seed_existing100/need0、q2/T5/progress0。逐月尽量复用真实autosave；progress接近5时留完成前一日和完成后，不预填150天。完成账本C21/G21/D7/made300，return真实R；重复已毁回调与重载复用该完成链。 |
| 4 | 在normal-done、核心仍可用时，独立销毁母舰分支 | before直接复用normal-done；执行下述原生损毁与重复生产初始化，过一次真实月脉冲并保存；重载此已毁after再同步/保存，证明0母舰。随后本来就要load owned-ready，无需额外恢复母舰的load。 |
| 5 | 实际load owned-ready，做核心迁移与owner-loss | 该档源仍50，母舰恢复来自显式加载旧before，不能称免费重生。先UI迁移、核新旧物理核心；转手新核心前旧核心仍有人作为保命备份。保持外方owner与EEP绑定，完成负例后再保存。无需在此核心不可用状态测母舰不重生，否则startup的core guard会混淆原因。 |
| 6 | 实际load pk2base，7独立目标+当前/外国secondary core | 必须换干净base：normal的q2已reserved一个home候选，直接接batch_split_bind会缺7个未reserved对象。按既有短命令setup，SAV证实7种持续状态，共用ready/idle-day1/fired-day1；foreign secondary core在这支转手，真实绑定core保持可用。 |
| 7 | 再load一次pk2base，同时准备colonizing与enemy-ground两个目标 | 可共用state_guard_bind及一组ready/idle-day1/fired-day1，不必各load一次。先分别运行短setup，再用同日SAV证明真实殖民进度、地战双方；idle到下一日两状态都仍真才reload ready依次dispatch两callback，保持状态到after。若idle地战已结束，构造不合格，不能因零收益判通过。 |
| 8 | 独立Lithoid新局Jan1→首月，之后功能分支pc_hive q2/300 | 首月净电证据先封存；再运行lithoid_q2_setup/inspect并保存lith-owned-ready，完整原生90/30一次，兼自有天然非核心与native收益/返回。before C0/G0/D2/made0，after C2/G0/D2/made0/L0；R实测，native随机矿/合金/pop分列。不得用Machine世界或从Machine复制数字ID。 |

所有load后的活动autosave目录以真实load路径为准，不把历史归档目录当新写入目录。共用证据只减少操作，不省略来源、状态或独立checker要求；39命令资产仍是操作详情，本文没有晋升任何case。

## 母舰损毁：原生接口与最短证明

本run引擎生成`logs/script_documentation/effects.log:766–774`明确`destroy_fleet`支持all scopes，块参数target、kill_leader（默认yes）、destroy_template（默认no），描述为带死亡图形的destroy；1657另有destroy_ship，1541的delete_fleet没有死亡图形。本测试选destroy_fleet并显式kill_leader=no、destroy_template=no，避免额外杀指挥官；这是受控原生损毁，不冒称实战击杀。原版`events/paragon_events_3.txt:2960`和`events/astral_planes_events.txt:2065`均有真实块实例；`events/nomads_arkship_events.txt:4996`也实际destroy_ship，证明有殖民载体的舰船同样走原生销毁接口。

**只在主线程决定执行时使用**：先确认真实绑定Mother独船juggernaut、核心可用、grant flags仍在且所有母舰正例已采完。保存actor helper必须发生在销毁之前；销毁后不能再从不存在的Mother取owner。

```text
effect if = { limit = { exists = event_target:eep_mothership0 event_target:eep_mothership0 = { num_ships = 1 is_ship_size = juggernaut } event_target:eep_mothership0.owner = { eep_qualified = yes eep_core_available = yes has_country_flag = eep_initialized has_country_flag = eep_startup_granted has_country_flag = eep_mothership_granted } } event_target:eep_mothership0.owner = { save_global_event_target_as = eep_destroy_probe_actor } destroy_fleet = { target = event_target:eep_mothership0 kill_leader = no destroy_template = no } log = "EEP_MOTHER_NATIVE_DESTROY_REQUESTED" } else = { log = "EEP_MOTHER_DESTROY_NOT_READY" }
effect event_target:eep_destroy_probe_actor = { eep_initialize = yes eep_startup = yes eep_sync_mothership = yes }
```

before复用normal-done；销毁图形/动作与日志证明调用，随后重复生产initialize/startup/sync、真实推进到下一月脉冲并留事件处理窗口，保存mother-dead-month。实际load此已毁档，再执行同一生产同步片段、推进一日、保存mother-dead-reload。只需新增这两个after档；若存在月度缓存暂态，保留原件并采稳定状态，不编辑SAV。

两份after必须：原fleet/ship原始对象已不存在或明确native dead且不在actor所有列表；全表扫描actor所有舰船/舰队，Mother设计、专属flag/modifier及juggernaut不能出现新ID替代品；EEP绑定不得指向新活Mother；核心/国家仍存活可用，三个grant flags保留，C/G/D/made/worlds与已发tier/rewards不因同步改变。允许country的component_snapshot_state从live0变为history1（无快照时2），pending仍按entitled−paid，不能把历史mirror当活装备。维护随舰毁减少是正常变化，不要求库存/预算跨月恒等。

生产依据：冻结`eep_startup_effects.txt:2–21`要求NOT startup_granted；97–123先置mothership_granted再create_fleet，缺global target不会重发；`eep_effects.txt:2`只在未initialized时绑定/清账；`eep_mothership_effects.txt:66–166`只有已存在且正确owner/独船juggernaut才迁移设计/同步组件，无create_fleet；`eep_on_actions.txt:2`的自然monthly事件eep.2同时initialize与sync，覆盖了月度修复路径。

来源哈希：本run effects.log `79570f3609d8fd34666565df2e1582e96f2cfb87bc7559c7610e52ad350bc6f5`；冻结startup `e1ec38f25535507d284a620ac864a6cbf1340712087ad430596f2b907dfde0f3`，mother sync `b4efb84032796adc1f87d0613a56e601926dca25ba645b7b2cd60dd13ea17ed5`。本页是待执行设计；只读源码不能替代两份真实after或宣称“不重生”已通过。

两条待执行片段分别626/114字符，均ASCII单行；既有open_kaishek lossless batch parser解析2/2、退出0、无诊断、roundTrip=true，仅静态文本通过。既有39命令资产原SHA `76adabaf82dc2c10894222bdb425ee1b994307233e1bccb2c251bdf2f07325c8`未变；未执行销毁或其它console effect。原版三个实例文件SHA依次为paragon `a1b6d030d3dbc4582b9412b86492d8c1f64d1b0b8799ee73e3c15dd3d247d4c8`、astral `9304465c7be91c7a08e19f08d7cc7e8a225c9ed89cddd358800bf9ea90b559ec`、arkship `838950f4ffa5a3d2eb48a03a8e45d757aab3fee8fb8130bbd51855e188541240`。
