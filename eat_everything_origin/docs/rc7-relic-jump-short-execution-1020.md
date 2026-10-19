# RC7：C0同日Relic参照与真实跃迁短步骤

## 范围与事前判据

仅给主线程复用RC4已成功的原生命令/界面步骤；作者不操作UI/Git/Mod。成长结束后实际Load本RC7 C0 `r7ganchor`，不用C20500支线或旧RC4/RC6档。Relic是公开的功能参照夹具，会增加真实海容/维护，不能计入干净经济。保留同日两舰详情、真实jump订单/到达/冷却；不是set_location移动Mother，不重复供电getter调查。

已只读核固定run `20261019T164112Z`：tree `61b34f6dbdc277c44364889d5f1e1cd2773a4624786bbf0d538079fc6ba4feb0`，`r7ganchor.sav` SHA `aec53eeed736d23abb856b7a1c1696657ce55517124097f1ad6c69921f1d8385`，2201.01.01、country0为Machine、C0/六tier0，`eep_mothership0`→fleet125→唯一ship809→actualdesign16777235，`eep_core0`→物理4，Mother所在system0。实际Load后仍须核同一身份和C0。

**本银河没有`legendary_leader_1st_system`。** 不能照抄旧RC4带该旗标的selector，更不能沿用旧system196。按主线程授权，本页只新增最小邻居绑定：Mother.solar_system→random_neighbor_system，改ASCII名并保存目标，不改位置/冷却。原生generated effects:6324–6334明确该迭代接收galactic_object；scopes:334–336说明fleet.solar_system输出galactic_object。官方`ancient_relics_arcsite_events_1.txt:1733–1737`已有system→random_neighbor_system→save_event_target_as的无limit实例。新短串先静态解析，再交主线程实际执行；静态通过不等于目标实际绑定或jump成功。

## 一条原样Relic命令与一条最小替代

先确认锚点未已有`eep_relic_reference_1019`，再用原RC4 action里的**原字节**（只执行一次）：

```text
effect create_fleet={name="EEP_Native_Relic_1019" effect={set_owner=event_target:eep_mothership0.owner create_ship={name="NAME_Relic" design="NAME_Relic" graphical_culture="npf_01"} set_location={target=event_target:eep_mothership0.solar_system.star distance=30 angle=0} save_global_event_target_as=eep_relic_reference_1019}}
```

原来`set_location`只定位新建Relic，不能碰Mother。既有原样`fast_forward 6`给缓存刷新窗口，随后存`r7relic6`并读实际日期/新Relic fleet+ship、归属/设计、C0和两舰光环。两张配置截图都取该同国同日暂停状态。

目标绑定的**新短串，仅待主线程实际执行**：

```text
effect event_target:eep_mothership0.solar_system={random_neighbor_system={set_name="EEP_JUMP_TARGET" save_global_event_target_as=eep_jump_destination_1019}}
```

再执行RC4原样`survey`以揭示地图，然后关闭console。保存`r7jumpready`，从原生SAV核`eep_jump_destination_1019`恰绑定一个实际非system0邻居，实际名`EEP_JUMP_TARGET`、坐标未改，Mother仍125/809在原地。无绑定、重复名、阻断或UI目标无效均不算完成；不向旧196补flag。

主线程可直接调用现有`runtime_1019.py console-open '<上述单行>' <唯一stage>`；`console 'help' <唯一stage>`关闭已观察console后才进行Save/Load。`native-save <唯一名称> '<真实HUD日期>'`，不把Jan1+6写死为所有步骤日期。

## 最少截图与原生存档

1. **同日配置两图**：实际选唯一Mother，点其真实舰船行的详情放大镜；RC4成功点为client(360,709)，但本次以新GPU上实际控件为准。必须确认已打开详情、舰名/舰型正确，采`r7mother-details`；关闭详情后，选择实际`EEP_Native_Relic_1019`舰队并用同样入口采`r7ref-details`。记录三防/速度/闪避/伤害与日期/海容，不拿全景图或军力替代伤害。SAV同时绑定两实际设计、Mother50+6/Relic43+6，以及共享43槽；不预设本次面板数值等于RC4。
2. **真实UI下令**：银河视图按原成功路线搜索ASCII `EEP_JUMP_TARGET`（旧搜索框client(665,142)、结果(630,166)仅供定位），点真实结果再选回Mother。悬停确认按钮文字为“启动跃迁”，旧成功位置client(145,339)，不是Move；点按钮进入目标模式，再点实际目标星绿色有效框。保留issued图；旧(512,386)属于旧镜头，不能照抄。
3. **预热锚点**：用原样`fast_forward 1`，存`r7jumpwind1`并核实际`jumpdrive_order.system=新目标`、`jumpdrive_windup.windup_time/start_date/end_date/can_reach`。RC4实际为14天；本次只能从真实订单读14，不能按按钮日期猜。剩余若为13天，才原样`fast_forward 13`；否则按实际end_date计算。
4. **到达与冷却**：存`r7jumparrived`，采实际“启动跃迁”按钮hover，确认原生200天冷却及伤害/速度-50%文字。SAV核同一Mother的fleet/ship位置origin均为新目标、jump订单完成、ship新增`jump_drive_cooldown=yes`/实际`last_jump_date`，Relic留在原地，C0/成长账本未变。旧RC4 `last_ftl_jump.to`缓存曾未更新，不用该单字段否定或虚构路径；以真实windup、实体位置、订单清除、冷却联合证明。

整个路线只需2张同日配置图、1张实际下令/目标状态图、1张到达冷却图，以及刷新/ready（同日可复用）/wind1/arrived的真实SAV。若尚未到达，保留事实再按实际订单推进；不用固定旧target numbers，也不声明最大范围或200天到期测试。

## 原成功来源与静态状态

RC4原始动作位于`docs/evidence/1019-rc4-relic-jump-native-control-v1/raw/`：`r4relic-create-native-command.action.json`（SHA `193a9922758a80fd9eb8e249a34f5598de15c311fc99664db1fbb5389b4b9d56`）、`r4relic-refresh-six-days-command.action.json`、`r4jump-survey-visible-systems-command.action.json`、`r4jump-windup-one-day-command.action.json`、`r4jump-to-native-end-date-command.action.json`。原成功配置/真实跃迁限定报告为[rc4-relic-ui-jump-v1.json](evidence/1019-analysis/rc4-relic-ui-jump-v1.json)，SHA `5e849e167c16057d6f529f74ec0c7d491ebd1e28382844ffb846e17e7de85b64`。这些只证明原路线曾实际成功，不继承为RC7通过。

两条effect均已使用既有open_kaishek JAR `6ac143ebf03f3e1a041dff01b2d808e60de8e289d18cebf9855682f0a80b6d82`做lossless静态解析：旧Relic控制台串325字符（P-body318字节/69tokens/4blocks），新邻居串156字符（P-body149字节/22tokens/2blocks），均exit0、PARSED、diagnostics=[]、roundTrip=true；控制台前缀`effect `不属于P-body。旧串又与封存action.text原字节相等。新串仍是PENDING，未执行控制台或UI。

原生依据完整SHA：`ancient_relics_arcsite_events_1.txt`=`4a0b6e744395b286ba89dcd2f21508a411fafd5b7b45220b613689af033ae3a0`；引用的RC6停止后封存generated `effects.log`=`985c95672f491f0458fcd34232743e2c2a1b9e1862743e2b156eea7e9ca5a773`、`scopes.log`=`57bb260cf11be3cf4257d22a9b583beadfb75639045f831fde31318f960b931f`（同精确EXE）。`set_name`支持galactic_object见effects:468–470，未使用CK3方言。
