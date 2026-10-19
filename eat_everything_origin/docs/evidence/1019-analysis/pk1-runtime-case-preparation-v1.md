# PK1真实订单与结算的只读检查准备

本设计仅检查已经存在的工具和校准证据，尚未读取queued／charging／cancel／fired未来存档。所有模板为PENDING，null必须由主线程确认的真实SAV或独立预期替换；不能运行模板失败后覆盖该失败报告。

## 已有来源和计算基线

当前checker SHA256为`ba17847049d050b2b76dc382e7e3e0a1796dc4976a80c77b16fef243bc612047`，inspector为`1ec3ad71f877be5704959134b76e59be077b756a906f7297f278613ee8bfbf92`。没有改旧严格比较门禁。校准报告`rc3-pk1-objective-calibration-v1.json` SHA256 `58416a43891a899cc7ded7982760cd1dfbe93180e78123937842de011bbba87a`，同日实际complete各一次，worlds750／empires600；两原生SAV、实际动作和17项保持检查已归档，校准本身不是发射。

当前Machine actor0／Mother159、997／core2／敌方target17。Jan2原生目标size19、零d_lithoid_devastation，有效q19、敌方人口5200；基线C0/G0/D2/made0/worlds0，母星人口4800。若实际发射前这些状态保持，普通材料结算预期C19、G19、D6、made300、worlds1、capacity增4、敌人口返还0；母星人口另加独立自然增量。实际临近完成SAV仍须重新读取，不把Jan2值硬套未来。

冻结武器CSV的min_windup为90、cooldown为30，真实充能／发射过程可能跨月。`expected_other_core_pop_delta`不可由after总人口倒推；建议在完成前最后一步保存`precomplete`，以尚未结算的原生账本和原生pop_group增长细节建立独立自然增量。若最后一步跨月且无法独立确定增量，该字段及人口检查继续PENDING。

## 同日排队／取消无收益

每一对都需要清场后、紧贴动作的真实同日before／after。使用`prequeue→queued`检查排队，`charging→cancelled`检查取消；保留实际destroy_planet_order、move子订单、source快照／活动标记的变化。Jan2基线到多日后充能档不能通过同日检查。清场若得到原生destroy_enemy_ships危机进度，早基线的crisis raw会变化，也不能把它当提前支付世界奖励。

现有`no-settlement`检查九项：同日、同候选树、C/G/D/made/worlds不变、核心人口与容量不变、源星类型／殖民地不变、五结算完成flag成员关系不变、完整危机progression不变；它嵌入完整严格比较，订单／路径／排队标记引起的严格FAIL必须保留。它不独自证明实际充能、战时目标、cancel动作、六core奖励或所有last收据不变；报告外另抽取完整EEP变量、Mother变量、source flags／q、原生订单、军队与战争，按具体scope陈述。

最少调用（从项目根目录，模板填写完成后，各输出必须为全新文件）：

```powershell
python -B eat_everything_origin/tools/check_1019.py --output <新的观察报告.json> observe <实际原生SAV> --world 17 --world 2
python -B eat_everything_origin/tools/check_1019.py --output <新的同日无收益报告.json> no-settlement <填写后的同日case.json>
python -B eat_everything_origin/tools/check_1019.py --output <新的结算报告.json> settlement <填写后的发射case.json>
```

无需单独再运行compare，no-settlement已内嵌strict_comparison，settlement保留all_differences并在填写reload时内嵌同日无重复结算检查。若需要独立严格报告，调用`compare BEFORE AFTER --world 17 --world 2`，输出路径另取新名；不要修改严格比较以消除native订单／缓存差异。

## 发射后结算字段

settlement case必需：schema、path、before、after、source_world、core_world、expected_q、native、expected_return、expected_other_core_pop_delta、expected_crisis_progress_delta、crisis_calibration_evidence、expected_crisis_empires_progress_delta；正empires预期还需crisis_empires_calibration_evidence，reload为可选真实SAV。`native=false`在这里指EEP材料收益分支不是噬岩者，并非说存档／武器不是原生。

worlds预期750。empires仅在发射前enemy最后殖民地且校准上下文保持时预期600，否则非灭国应显式0；灭国后的潜在C++归因奖励不能假设恰好再加600。若实际差值异常，保留FAIL后调查，不修改预期迎合结果。

现有settlement读取source实际pc_shattered、殖民地移除、五个完成flag（credit／return／population／crisis／destroy）、source eep_q、C/G/D/worlds/made、三条last收据、母星实际人口与capacity，以及两个objective独立progress。source原生损耗按真实d_lithoid_devastation计数扣减；普通任务的q取开工冻结值，巨像fresh q才按live size减损耗，两个入口不能混淆。

实际charge／fire与no_army仍需独立原生动作／截图／订单／时间线；settlement只证明持续结果，不替代发射。no_army精确含义为目标无actor入侵军队，保留母星五个machine_defense守军；teleport是测试准备，不能填active_jump。敌方发射通过也不能覆盖owned_noncore_colony_fire、普通拆星回归或其他守卫矩阵。
