# 1019 RC3 巨像六日内完成：时长与CSV载入调查

## 真实失败与调查范围

主线程在 RC3 单Mod简中运行 `20261019T092935Z` 中于2200.03.07真实点击专属巨像命令，随后只推进6日。原生 `pk1charge.sav`（2200.03.13）已显示目标planet17变为pc_shattered、星主country1消失、EEP结算receipts存在。故当前候选未满足完整90日充能/30日发射要求，不能因真实毁星和静态检查通过而宣告巨像验收完成。

本轮只读原版脚本、生成文档、EXE字符串与SAV；不改Mod、SAV或桌面。下列修复探针需主线程先确定方案、工具门禁、冻结新候选再执行，不热改RC3或抹掉失败。

## 已直接核实的事实

1. 本机只有 `common/component_templates/00_weapons_planet_killer.txt`，没有 `00_utilities_planet_killer.txt`。原生CRACKER是weapon_component_template，size/type均planet_killer、use_ship_main_target=no，包含component_set与planet_destruction_gfx；没有 `planet_killer={...}` 子块。本包专属模板同样具备这些结构，没有证据表明缺此虚构子块。
2. 本机 `weapon_components.csv:194` 的CRACKER、:384的MAW均为min_windup90、max_windup0、cooldown30；本包 `eep_weapon_components.csv` 专属行相同，power0沿用MAW。不是本包将max_windup写成90，也不是把原版90/30数值抄错。
3. `000_documentation.txt:138` 明说多数weapon数值在 **weapon_components.csv** 中，脚本模板提供其它结构。文档另列windup、total_fire_time字段，但全本机component_templates TXT未找到这两个字段的实际赋值用例。不能仅凭列字段就猜range/scalar格式和优先级。
4. 原版component_templates目录实际只有weapon_components.csv和mutation_weapon_components.csv两份CSV。原版存在第二个专名文件，并不证明引擎会任意遍历所有*.csv。
5. 精确EXE SHA256为`400df27c82ddc845aa9dce79bd468d81f18f060d299cd263e3afa93aef4f7a83`。只读ASCII字符串：完整字面路径`common/component_templates/weapon_components.csv`起始文件offset37569608（basename起始37569635）；`common/component_templates/mutation_weapon_components.csv`起始37569848（basename起始37569875）。附近还有utility_components.csv、strike_craft_components.csv专名及min_windup/max_windup。这是专名载入假说的二进制旁证，不等于已经反汇编并证明全部加载分支。
6. `pk1prequeue.sav` 是2200.03.07，SHA256 `67dad27edbefbe00565488c1058b8161fcad4903f19ea23bfd6e2b8dc009ffa2`，目标planet17仍pc_alpine/size19/owner1，country1存在。Mother实际武器有index33、template=EEP_PLANET_KILLER_DEVOURER、slot=PLANET_KILLER_GUN_01。`pk1charge.sav` SHA256 `156ac651eb5d8d268355c2281ce347670232bd4ffe0f419795d58d4b94095b77`，同一武器仍存在，但目标已shattered且五个EEP receipt存在。该档里worlds进度750、empires600，分别恰等于独立原生单位奖励校准；目前此个案不支持灭国双付。
7. 既有真正原生噬星者实验保存了windup89/windup_time90、fire1/fire_time30，证明这些原生订单字段可观测；当前专属武器也必须取得自己的字段，而不能仅引用旧原生武器替代。

## 首要假说与尚未证明项

首要检查“任意新命名的eep_weapon_components.csv是否被本机引擎加载”。模板与武器槽已经真实存在，不代表CSV数值已进入原生武器对象。小于6日的完成与未读到数值而使用默认时长相容，但当前没有逐日订单证明具体默认时长是多少，不能编造为1/1或2/1。

原生碎星炮也使用该90/0/30 CSV；这削弱“这只是普通战斗weapon windup，巨像另需planet_killer子块”的猜测。实际字段/载入仍须新探针确认。不能通过扩大CSV数字掩盖文件未加载，也不能调用完成事件模拟满足90/30。

CSV静态工具负责人已明确：现有任意CSV检查只认证表头/键/数值/引用合同，没有验证任意文件名被native加载。新运行事实必须扩展载入合同或明确unsupported；禁止把14条夹具的P语法PARSED或整包静态PASS当作CSV时长运行证据。

## 下一探针的最小设计与验收

选定修复路线前只保留本调查，不改生产包。可以由主线程比较两条候选：

- 采用引擎已经实际命名的CSV文件路径，保持该原生表全部已有行与表头原字节/数值不变，仅添加专属行。不得把仅有专属行的文件命名为weapon_components.csv覆盖全原生表，导致其它武器失去统计。选择weapon_components.csv或mutation_weapon_components.csv都要记录原始SHA、所有保留键及覆盖边界；第二个文件是否接受普通新PK键仍须实际验证。
- 若能从确切引擎接口或真实兼容Mod源确认TXT windup/total_fire_time等数值语法及优先级，可另立最小候选。文档列字段本身不足以猜实现，不先改生产脚本。

每条候选先通过适用的open_kaishek合同，冻结新字节；从同一未毁目标原生base实际重载后重新右键下令。保存真实queued订单，然后1日、接近90日及首个fire日的原生SAV：windup_time必须90、fire_time必须30，目标在未完成前保留、EEP账本和worlds/empires不提前变化。若1日就完成或time字段仍为默认，候选FAIL，不能跨过边界直接看最后结果。

取消测试和完整30日发射、完成后防重复需要在正确时长候选上重做；RC3这次≤6日完成只保留为真实失败和一次结算观察，不作为最终90/30验收。

## RC4 最小修复方案（先于实施）

主线程已选择TXT内联数值路线，禁止覆盖原版整份CSV。本次只改专属 `mod/common/component_templates/eep_planet_killer.txt` 并删除生产树中未获native载入证明的 `eep_weapon_components.csv`；不改结算、目标规则、回调、核心成长、本地化或版本。VERSION/冻结/外部工具新门禁由主线程统一处理，RC3运行和快照保留原字节。

内联语法已取得现代作者第一手源码：[Gigastructures固定提交的aeternum_components.txt](https://github.com/Pouchkinn-s-Gigastructures/Gigastructures/blob/436812fb3acd9dc7d6cb5e666268a3a1d8135aa7/common/component_templates/aeternum_components.txt#L466) 中，PLANET_KILLER_AETERNUM_SHROUD同时声明type/size=planet_killer，并直接使用windup的min/max块及total_fire_time。实际例为30/30和fire30；相同提交其它PK组件也使用同形内联。已独立读取作者raw原始512行文件，SHA256 `d2274c452717e1fb5b089e10480881d36804ebe64f0f26350ac780999b0d9256`，块在466–483行，两个时长字段在479/480行。浏览器抽取后的行号可能偏移，以上是原始文件行号。不是把普通激光组件类比成巨像。

本包采用 `windup = { min = 90 max = 90 }`，`total_fire_time = 30`，`power = 0`。TXT明确写固定上下界，遵照作者真实PK30/30结构；原生CSV行的90/0是该表所用形态，不将CSV中的max0机械搬入TXT范围。这里证明的是块语法及同类实际用法，尚未证明本机引擎将此数值转化为90/30日，最终仍以原生SAV的windup_time/fire_time判定。

同时把原专属行的零直接伤害显式写成 `damage = { min = 0 max = 0 }`，因为本机000_documentation:151记录damage缺省为1。保留range0、accuracy1、tracking0，零供能负担。组件仍无resources成本/维护块，不新增成本、资源、射线伤害、贯穿、光环或其它功能；已为零的直接伤害无须再写冗余伤害倍率或导弹字段。原有组件键、大小/类型、目标/潜在条件、组件集合及图形原样保留。

静态验收只认证修改后的专属模板能由open_kaishek解析、内联字段/数值合同满足、生产树不再有孤立专属CSV、不覆盖任何原版CSV或键；完整包门禁等待工具负责人修复通过。实机先保存queued→1日的字段，windup_time必须90；90边界后fire_time必须30，完成前零结算，然后重做完整完成、取消与重复回调。任何提前毁星继续FAIL，不以已改源码或作者例子宣称本机90/30已通过。

## 最小修复实施与静态核对

已按上述范围在专属TXT增加8行（含注释），删除5行独立专属CSV。TXT当前SHA256为 `0bf1314f69f410ffcbf14875680d2689453295ee317b16d47ae219920b62dd92`。既有open_kaishek lossless CLI仅对此文件返回exit0、PARSED、671bytes、221tokens、6blocks、diagnostics=[]、roundTrip=true，显式字段值与CSV删除检查通过；git diff --check无错误。尚未运行新的整包数值来源门禁，更没有RC4实机结果，不宣告90/30成功。
