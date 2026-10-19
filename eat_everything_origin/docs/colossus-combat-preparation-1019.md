# 1019 母舰巨像的太空战前置调查

## 目标与范围

主线程在 RC3 中真实下令准备时，Mother fleet159 与约727军力敌星基地交战，报告 fast_forward5 后敌方损耗约18%。本轮只读调查原生时间推进、战斗接口和受控清场方案，避免把战斗等待误当巨像底盘或命令失败。不修改生产包，不编辑 SAV，不操作桌面；任何清场命令仅为独立武器功能夹具准备，不能计作正常战斗胜利或经济验收。

验收关注：原生敌殖民地、星主、战争、Mother、实际武器和完成回调均保留；清场若执行，先归档清场前后，再以清场后原生 SAV 建立新基线，之后仍须真实右键下令、完整90/30充能发射、实际完成。本文方案尚未由本分支执行。

## fast_forward 与战斗进度的证据边界

本机原版 TXT/GUI 和自动生成 effects/triggers 文档不包含 fast_forward 的 C++ 实现；没有取得4.5.2官方材料承诺其对所有战斗物理子步骤的逐帧等价性。互联网检索没有找到可支持该具体结论的第一方资料，官方 Wiki 页面返回401、论坛正文受robots限制；第三方命令列表只说推进天数，不能据此证明或否定战斗物理更新。

主线程报告5日后敌方已有损耗，这至少不支持“完全不推进战斗”。但5日/18%也不能单独证明卡死：需要比较同一敌舰的原生 shield_hitpoints/armor_hitpoints/hitpoints、战斗双方、Mother武器/动作与实际日期，而不是仅比较军力比或UI百分比。可先以既有原生 fast_forward 再推进一个短窗口并保存；若实际损耗和战斗订单继续变化，保留自然战斗即可。真正判断 fast_forward 与普通最快速度是否等价，需要从同一原生 base 分别推进相同日数比较，不能从一个窗口猜测 C++。

未找到可靠的公开 stop_combat/end_combat effect；不编造此接口。set_fleet_stance、clear_orders、set_location 也没有文档保证解除已经成立的 combat 对象。

## 本机精确接口

精确 EXE SHA256 `400df27c82ddc845aa9dce79bd468d81f18f060d299cd263e3afa93aef4f7a83`，自动文档来自 run `20261019T092935Z/logs/script_documentation`。

| 原生接口 | 文档 | 实际语义与本用途限制 |
| --- | --- | --- |
| damage_ship=数值，或 {amount=数值 attacker=ship/country} | effects.log:502 | 对ship或fleet全部船施加伤害；可设置击杀归因。星基地可能进入disabled/占领流程，不能保证等价于删除敌战斗对象；会污染战斗/危机其它目标，故不是首选。 |
| destroy_fleet={target=目标 kill_leader=no destroy_template=no} | effects.log:766 | 删除目标fleet，有死亡图形；默认kill_leader=yes，明确no减少领袖副作用。可用于限定对象清场，仍需等待战斗清理tick并核对原生对象消失。 |
| destroy_ship=目标 | effects.log:1657 | 删除单船，不如整个敌方fleet清场明确。 |
| set_fleet_stance=aggressive/passive/evasive | effects.log:1272 | 设姿态，未保证强行脱离已交战对象。 |
| clear_orders=yes | effects.log:598 | 清除舰队订单，会丢失已有PK订单，未保证结束战斗。 |
| set_event_locked=yes | effects.log:594 | 禁止玩家操作舰队，与需要真实UI下令的目标冲突。 |
| set_disabled=yes/no | effects.log:3893 | 仅ship scope，未保证停止fleet战斗。 |
| set_mia、order_forced_return | effects.log:2331、:602 | MIA/返回可能影响位置和订单，不适合保留原地充能。 |
| set_location={target=... distance=... angle=...} | effects.log:351 | 可用于明确的预先定位；没有依据把在战斗中传送当作可靠stop_combat。 |
| is_in_combat=yes/no | triggers.log:1780 | 支持ship/fleet，用于清场后的只读状态判定。 |

原版 `events/planet_destruction_events.txt:289` 在销毁星球时实际使用 destroy_fleet=orbital_defence；`common/scripted_effects/nomads_effects.txt:735`、:3217 实际使用 destroy_fleet=this。这些只是接口和目标语法先例，本文不会调用原版毁星事件来冒充本包发射。

## 精确敌方对象与最小清场配方

只读 `pk1base.sav`（SHA256 `dccb1e17d6f76c915e3f0a916e627f068c559d381e7a6962becc21c77093b38a`）：Mother159/ship997 的 combat.in_combat_with 为fleet4/5/6/7，system8；country1 的目标是物理planet17。

- fleet4 是727军力星基地，ship6，HP10000、装甲5800、护盾1800，starbase_mgr.starbases1.station=6。
- fleet5 是科研船ship7、fleet6是建造船ship8，均evasive；fleet7是3艘护卫舰ship9/10/11，约223军力。
- 这些ID只对该原生档适用，不能把其它新局或重开档按此硬编码清理。

scopes.log:266 支持 galactic_object→starbase，:58 支持 starbase→fleet；应从真实目标星的 solar_system.starbase 找敌基地，并同时核对owner和排除Mother。最小限定命令为：

```text
effect event_target:eep_colossus_probe_target = { solar_system = { starbase = { fleet = { if = { limit = { exists = owner owner = { is_at_war_with = event_target:eep_mothership0.owner } NOT = { is_same_value = event_target:eep_mothership0 } } destroy_fleet = { target = this kill_leader = no destroy_template = no } } } } } }
```

该命令只定位目标系统的原生固定starbase，不遍历所有移动starbase，所以不会因为Mother也是主宰星堡而被同一遍历匹配。执行前仍须主线程核当前星基地实际owner及fleet，命令的防护是附加条件，不替代确认。

若余下普通敌舰仍困住Mother，可在原始输入和SAV确认其属于country1且确为combat对手后，仅对这些明确的fleet逐个执行相同destroy_fleet，不扩展为全银河/全国清空。也可以让Mother自然消灭约223军力护卫舰并等待科研/建造船逃离。禁止对target colony、country、Mother、player ships 或global on_action做替代性销毁。

清场可能产生死亡/归因事件、其它危机目标、AI重新造舰、失去星基地后的领土或战斗状态刷新；不会仅凭命令推定这些不发生。必须保存清场后原生SAV，确认planet17仍为殖民地且owner1、country1仍存在、country0仍与1交战、EEP账本及worlds/empires未提前增长、Mother159/997仍在且不再is_in_combat。记录其它原生objective的实际变化，新的武器差值从这个清场后基线算。

如果删除固定星基地导致引擎重建或领土状态异常，保留失败分支并原生重载base；不修改生产包补救，也不把清场成功当作武器通过。若清场后PK订单被清理，必须重新真实右键下令并保存新订单。

## 同轮奖励校准旁证

只读 `pk1calafter.sav` 对 `pk1base.sav`，country0.crisis_progression 的 native worlds 从缺项变为750、empires从缺项变为600。这是本轮独立complete_crisis_objective命令的单位奖励观察，不是武器完成。最终真实发射仍比较各自objective，不看总menace或战斗击杀目标。

当前没有本分支执行的清场结果或普通速度/fast_forward等价测试；本文不宣称战斗模拟或清场验收已经通过。

## 原生地图目标辨识

Mar7 基线确认 source17 是 giant15 的卫星，当前缩放不显示其名称。主线程先用原生 `help survey` 核对勘探命令；若存在，再在独立功能分支勘探使目标可辨。必要时只给 source17／parent15 设置明确的夹具名称，然后重新保存同日下令前基线。地图可见性或名称变化不用于经济验收，不改变人口、q、星主、战争或 EEP 账本；下令后必须用真实订单中的 planet ID 再核对17，不能仅凭画面名称认定命中。
