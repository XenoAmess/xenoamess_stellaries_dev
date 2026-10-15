# 白绮本人免维护：原生豁免入口

## 目标与失败证据

rc.5 真实个体机械领袖页中白绮等级5维护费1.0，其他四名各4.0。本人免费目标FAIL，截图rc5-white-before-leaders与natural_success原生存档保留。不能把-100%文本当实际0。

## 设计与范围

本机4.5.2 defines `MIN_ECONOMIC_MODIFIER_MULT=-0.9`，经济维护倍率有下限；增大负倍率不能解决。原生common/game_rules/00_rules.txt的should_pay_for_leader_upkeep以leader为This，排除has_leader_flag=should_not_have_upkeep；relics.txt已有create_leader后设置该flag的实例。使用该原生豁免，仅对白绮has_leader_flag=shishan_code_vivhite的本国领袖设置should_not_have_upkeep，覆盖初建、旧档刷新及重启。保留原有成长/头像/traits与其它领袖付费，避免重定义原版game_rule或经济script_value。

原生flag免除本人所有资源维护，当前个体机械白绮原本仅凝聚力；这是本人免费设计的明确范围，不能声称只影响凝聚力或其它领袖。原self -100%显示可保留兼容旧描述，但实际免费由native规则实现。不要给backup/外国非白绮无关领袖扩散豁免。

## 验收

新候选0.2.0-rc.6，工具先行且重新启动。原生旧档刷新后本人显示0，其他领袖费用保持；实际kill触发on_action、UI支付500能量/200合金重启，免费flag保留、白绮唯一、等级/经验/技能/选择/头像恢复。至少用非零经验前后实际保存核对；若只有XP0必须明确未覆盖非零。模板克隆后豁免保留。程序测试覆盖创建/刷新/重启调用链与个人限定，旧无关领袖不添加flag。
