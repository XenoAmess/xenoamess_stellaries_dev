# 旧损伤迁移：原生三防读数与比例恢复接口

本调查只读4.5.2原生生成文档和本体脚本，为潜在迁移差异提前准备接口边界；未操作UI、未执行导出或恢复、未改Mod。首先仍以真实old-profile hurt及RC4加载／同步SAV为准，不能因接口研究先认定存在生产缺陷。

来源为旧profile run20261019T130448Z的`logs/script_documentation/triggers.log`与`effects.log`，以及本体`events/000_how_to_use_variables_in_script.txt`和`events/grand_archive_events.txt`。精确SHA与摘录另存analysis来源报告。

| 读数 | 原生定义 | 当前证据边界 |
| --- | --- | --- |
| current hull | has_hp，trigger1212 | 文档示例>200，ship |
| current shield | has_shield_hp，1216 | 文档示例>200，ship |
| max hull | has_max_hp，1220 | 原版Grand Archive7940实际export |
| max armor | has_max_armor_hp，1224 | 原版Grand Archive7944实际export |
| hull fraction | has_hp_percentage，2201 | 文档示例>0.5，ship／fleet |
| armor fraction | has_armor_percentage，2205 | 文档示例>0.5，ship／fleet |
| shield fraction | has_shield_percentage，2209 | 文档示例>0.5，ship／fleet |

`export_trigger_value_to_variable`在effects557～564明确可导出单数值trigger，支持ship，rounded默认为no。原版变量指南26行称应适用于比较单一数值的trigger。因此这七项有直接文档支持；只有max hull／armor在本次找到的原版用例中实际export，不冒称七项已在当前Mother实机校准。

本生成catalog未找到`has_armor_hp`和`has_max_shield_hp`。可提出计算armorCurrent=maxArmor×armorFraction，以及shieldFraction>0时maxShield=currentShield÷shieldFraction；这是数学推导，必须先以真实原生SAV和export对照验证。shieldFraction为0时后一计算不可用，不能编造最大盾API。

主线程若需要独立诊断，可在已经真实保存的old-source hurt后对其actual Mother ship导出七项（以下未执行）：

```text
effect root={event_target:eep_mothership@this={every_owned_ship={export_trigger_value_to_variable={trigger=has_hp variable=eep_probe_old_hull_current} export_trigger_value_to_variable={trigger=has_shield_hp variable=eep_probe_old_shield_current} export_trigger_value_to_variable={trigger=has_max_hp variable=eep_probe_old_hull_max} export_trigger_value_to_variable={trigger=has_max_armor_hp variable=eep_probe_old_armor_max} export_trigger_value_to_variable={trigger=has_hp_percentage variable=eep_probe_old_hull_fraction} export_trigger_value_to_variable={trigger=has_armor_percentage variable=eep_probe_old_armor_fraction} export_trigger_value_to_variable={trigger=has_shield_percentage variable=eep_probe_old_shield_fraction}}}}
```

该诊断会写ship变量，需另命名原生SAV，不能替换未诊断的hurt原件。它可给受控夹具保存旧比例的独立旁证，但公开旧SAV原来没有这些变量，不能把手工预置比例当作通用自动兼容方案。

恢复方面，原生文档明确有正向`repair_amount`／`repair_armor_amount`／`repair_shield_amount`与对应percentage；有绝对`reduce_hp`／`reduce_shield`和相对`reduce_hp_percent`。没有直接set-current三防或reduce_armor的已找到接口。负repair符号语义未实机确认，damage_ship虽有原版armor注释，精确层次与溢出仍不能充当独立装甲设置器。

因此“切设计后按预存比例恢复”目前只能作为待校准算法：导出旧fraction、切换、读取新max／current、计算差额；正差额使用正向repair，负hull／shield差额使用各自reduce；负armor差额尚无本次可靠的独立实现。percentage repair到底按max还是其它基数恢复也须原生小额对照，不能凭函数名把完整算法宣告可用。

更关键的是load阶段：现有export读取当前runtime对象；本调查未找到能在P脚本中读取“加载前原SAV序列化的max/current”或旧source定义快照的原生API。若同key modifier已在load时重新解释最大值，不能先假定load后的fraction就是旧比例，也不能把新max逆算当原始事实。原设计名／旧flag可用于识别待迁移设计，但不是原损伤比例的证据。该能力保持UNKNOWN，实际oldhurt→RC4load的原生比较将首先确定是否真的发生比例变化。
