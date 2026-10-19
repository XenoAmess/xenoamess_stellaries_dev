# RC7 敌星开战与定位基线接收

root在 `enemy_selected` 后明确封口新增 `enemy_base`：`r7pkbase.sav`，2201.01.21，SHA `11a5be54afb00099824972109a85f3e6f4eb5148cecfe6c488e422d4beb22193`，同stem receipt/audit固定。白名单新增 `r7pkbase*`、`r7pk-declare-war*`、`r7pk-place-at-enemy*`、`r7pk-war*`、`r7pk-ack-*`、`r7pk-after-*`、`r7pk-center-*`、`r7pk-enemy-system-visible*`、`r7pk-target-local-visible*`、`r7pk-local-view-toggle*`、`r7pk-actual-local-system*`；只取已固定原件，不读calafter、independent-cal、restore或其他未交接raw/活动日志。

目标是独立核实际war参与国/war goal、source17仍活、core2仍归actor0、Mother151/1044及space combat真实状态、C/G0/D2/made0/六tier0，以及有效shot基线无地战/己方陆军参与。root交接Mother已到source对应origin81、wg_cleansing、无FF推进；这些均先作待原生核对事实。先只用原parser解析这一确定SAV的相关块，若真实space combat已锁定立即回报root，不把普通 `combat_action` 或UI军事图标当space combat。

随后继续按原receiver/intake接口生成新增基线role，复用 `enemy_selected` 同world集合 `[2,17]` 的已有cache，不重复observe已固定selected。原件双读稳定并记录确切receipt/audit SHA；metadata沿root已明确的provenance来源查找授权，未交接raw不读。原selected报告/缓存不改，基线另建版本/小包并只引用相同canonical原件。可以以同日selected→base的原no-settlement验证准备动作未支付EEP收益，保留其战争/定位等full strict差异；不当成排队/取消/发射证明。所有武器、结算与最终case结论仍null/PENDING。

## scratch校准与实际恢复的追加交接（实施前）

root随后明确封口 `enemy_calafter=r7pkcalafter.sav`，2201.01.21，SHA `efed92e3e59cf786b8be70d82492e9e3f849b48f660a0e7c1d616e22e671b5b7`；新增白名单 `r7pk-independent-crisis-calibration*`、`r7pk-cal-console*`、`r7pk-cal-debug*`、`r7pkcalafter*`。该scratch仅各调用一次原生complete worlds/empires，独立读取两个objective各自前后progress/point delta；不抄旧RC6奖励，不把总差反推分项，不当真实shot。同步核C/G/D/ranks/pop/source无EEP结算污染。

root再交接实际Load base后的 `enemy_restored=r7pkrestored.sav`，同日，SHA `2c31da28be5180f3a808d938ec1ba1997bb31b031018d7443e54670241262950`；新增 `r7pk-restore-calibration-base*`、`r7pkrestored*`。先独立原生摘要快速回报war/陆军/spacecombat和两奖励/恢复，再用原receiver对base/calafter/restored三个新SAV各observe一次，原selected缓存只引用并用于同日未付款比较，不复制/重跑selected。新包为 `evidence/1019-rc7-pk-crisis-baseline-v1`。实际恢复后若出现原生government unlocked_civic_council_slots 0→4，原strict结果完整保留，不宣称整SAV逐字节恢复。root接下来的 `r7pkshot*` 仍活动，完全不读其raw/screens/actions或日志，只有原授权完成receipt metadata例外。

## 收件结果与封口

原receiver三role均首次observe，EXIT0、`OBSERVATION_ONLY`。原base→restored no-settlement为9/9 `PASS_SCOPED`；复用已封selected缓存运行同一原检查函数，selected→base也为`PASS_SCOPED`。这仅证明EEP结算未重复支付。所有18组138项最终检查仍null/PENDING。

原生命名objective独立读取为worlds 750、empires 600；实际type_text逐字等原map的`r6_crisis_calibrate`，且有独立物理Enter。scratch前后EEP账本、六rank、source人口4954、core人口4859不变；实际Load回base后另存restored，两项objective均撤除，仍Nemesis level1。校准不是真实开火。

暂停基线原生war0由country0攻击country1，进攻目标`wg_cleansing`。source物理17/colony1在origin81；Mother151/1044也在origin81、move_idle、空订单，combat.start_date为0.01.01，无序列化的活动海战。全局ground_combat空，actor仅五支位于本土colony0的machine_defense，无己方登陆军在source参战。这些是Jan21暂停基线，不能延伸到后续推进日期。

完整恢复strict保留72项差异和`FAIL`，包括舰船original_owner、design index、军力缓存、movement raw、starbase update_flag及carrier flags等；Mother design_id 1844→16777234，但原checker的design_shape相等。原生government council slots另读为0→4。没有忽略路径或将严格比较改PASS。

归档含151份白名单原件、11份派生/缓存，共162个payload、9,848,583字节；33组原图/OCR、32项canonical引用。原件与来源逐字节复核，授权metadata72→73且原72项不变。独立verify 12/12，限定`PASS_BYTES_AND_CALIBRATION_SCOPED_ONLY`。

- [index](evidence/1019-rc7-pk-crisis-baseline-v1/index.json)：`0c62761bfaf7ec4d4e801052e19c02bd3b948fd1606a005212ce269c4eb37b23`
- [verify](evidence/1019-rc7-pk-crisis-baseline-v1/verify.json)：`7a36f10317bdff6163716f38ca5dc0d03a1a7378557a184e0763c076e989e740`
- [独立校准](evidence/1019-rc7-pk-crisis-baseline-v1/authored/independent-crisis-calibration-v1.json)：`13af0b201319b15fe7b4a8abb30ed3cb019e2488bd83a7e9e465529a4dff2840`

仅可stage本文及整个`evidence/1019-rc7-pk-crisis-baseline-v1/`（166文件，合计167文件）。后续queued/day1/day6/cancel等另包接收，不改本包。接收过程一次派生脚本误取缓存不存在的current_order_raw字段，在写校准文件前退出；修正为原生raw的current_order块后完成，原receiver与raw不受影响。
