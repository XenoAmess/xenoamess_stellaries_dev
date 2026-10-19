# 历史nomads事件from错误：原版毁星回调来源调查

## 目标、范围与判据

本次只读调查RC4原版CRACKER手工完成回调控制中，`events/nomads_events_1.txt:2268`的`Invalid context switch [from]`。输入为已封存`1019-rc4-relic-jump-native-control-v1/native-control-analysis/analysis.json`及其原日志/命令、当前精确原版source和Mod回调源；不是缺失event诊断，也不是尚未开始的RC7真实PK新错误。

先重建原版on_action/完成事件链及每个ROOT/FROM/scopes约束，再区分手工`fire_on_action`与引擎真实90天发射可能提供的上下文。不能仅因原版控制也出错就称原版bug、无害或Mod已通过。输出新来源诊断和最小可分辨实测建议；不修改生产、fixtures、checker、历史报告、UI或Git。

## 已确认的scope合同

**不改PK的FROM：原版合同明确为开火fleet，不是planet。** `common/on_actions/01_planet_destruction.txt:1–3`写明THIS/ROOT是被射星球、FROM是开火舰队；同文件CRACKER完成块先调用`crisis.5015`，再调用`planet_destruction.100`等事件。`nemesis_crisis_menace_objective_events.txt:156`起的`crisis.5015`也明确重复该合同，并实际以`from.owner`取得开火国。旧控制的`scopes={from=event_target:eep_mothership0}`符合这份公开合同；没有源码依据将其改成FROM planet。

各层事件的FROM不是一个永久不变的对象：本机generated scopes说明FROM可指前一event的ROOT或引擎预设FROM。下游国家事件与武器完成回调的合同必须分别核对。

| 事件/回调 | ROOT/THIS | FROM | 来源 |
| --- | --- | --- | --- |
| 原生PK完成及`crisis.5015` | 被射planet/Carrier | 开火fleet | `01_planet_destruction.txt:1–3`、`crisis.5015`注释/实际from.owner |
| `on_country_destroyed` | 被消灭country | 可选destroyer country | `00_on_actions.txt:3601–3603` |
| `on_war_ended`→`nomads.94` | Loser country（原版注释） | Main Winner country | `00_on_actions.txt:2627–2640` |
| `on_becoming_subject`→`nomads.94` | Subject country | Overlord country | `00_on_actions.txt:4496–4500` |

## 报错的确切位置

`nomads_events_1.txt:2259`定义`country_event nomads.94`，仅触发事件。第2268行位于trigger，而非巨像完成代码：

```text
OR = {
    is_nomadic = yes
    from = { is_nomadic = yes }
}
```

该事件没有`exists=from`守卫；其immediate后来还会向root和from派发`nomads.96`以恢复方舟。可确认的脚本前提是FROM必须可用为country，不能把无效FROM安全当作false。这不等于已经证明是谁违反了前提或原版真实发射一定有bug。

扫描原版common/events的显式挂接，`nomads.94`只出现于`on_war_ended:2640`和`on_becoming_subject:4500`。它不在PK完成或`on_country_destroyed`列表中，也没有被本次EEP生产回调显式调用。`planet_destruction.100`实际杀死源星人口并改变星球类别；殖民地、国家、战争清理后的引擎on_action是另一层，不能假定继承手工PK的fleet FROM。

## 历史控制实际证明的范围

封存控制提交的原字节是：

```text
effect event_target:eep_colossus_probe_target={fire_on_action={on_action=on_destroy_planet_with_PLANET_KILLER_CRACKER scopes={from=event_target:eep_mothership0}}}
```

其后推进2日。P→Q原始日志新增375字节（SHA `b9979ba9c340db5e18766452a9c13284030b3306ddb1ff71464c18c5cf7f293a`），实际记录ROOT是EEP03 country0，FROM是`type=country/id=4294967295`，即该下游事件的无效country，而不是原始武器的fleet或被射planet。事件名字/错误性质明确是Invalid context switch，不是缺event。

本轮另外只读两份固定SAV：`pk2base`（2200.03.07，SHA `be5a344439dafe105d4959b4afa31143331b1daaaf915dba28bc70ee23f6f2e2`）的war0存在，主攻国0/主守国1；`pk2nativecontrol`（2200.03.09，SHA `49b3405d5265de6b9b471f778b67a573c521f2988499b6b7c7d4d45b7d6fe208`）中war0=none、country1=none。由“战争结束+敌国消失”及仅有两个显式挂接来看，**灭国后的结束战争路径是最接近事实的解释，但仍是推断**。错误ROOT0与原版Loser注释的关系、究竟哪个引擎hook产生无效赢家/宗主、是否另有引擎内部处理，现有源和日志不能定因。

手工`fire_on_action`文档只说明按指定scopes派发回调；没有原生武器订单、90/30实际流程或引擎毁星归责的等价保证。旧控制证明该手工原版完成路径也能产生同一诊断，因此错误不是EEP回调独有；它不能证明真实原版武器也会报、不能确诊原版bug或宣布无害，不能替代真实原生发射控制。

## 当前EEP生产与后续范围

固定RC7树`61b34f6dbdc277c44364889d5f1e1cd2773a4624786bbf0d538079fc6ba4feb0`的专属完成on_action只调用`eep.50`，carrier事件重验后以`from.owner`保存actor并共同结算；共同结算最终`destroy_colony`/`change_pc`。检查的5份冻结源都匹配manifest，没有新增调用`nomads.94`、`on_war_ended`或原版CRACKER完成。该源核对不排除引擎在灭国/结束战争时另发原生事件，也不是RC7实际PK结果。

主线程已明确：保持PK FROM=fleet，不改生产/fixtures/checker，历史FAIL及未解影响保留。**当前没有RC7实际PK样本，不新增控制夹具或实机要求。** 先由主线程完成真正RC7 EEP发射并审新日志；只有若同一错误再次出现，再决定是否需要真正完整90/30的原版CRACKER辅助控制。在匹配的末殖民地/战争条件下比较真实原版与EEP发射，才可能分辨手工回调限制与实际引擎路径；这里不提前安排或执行该测试。

## 来源与新诊断

[新来源链报告](evidence/1020-nomads-from-source-review-v1.json)，SHA `bc05d404be431a19e683877926800d0b47c8c8ea055c77866cf9198286ce60b0`，status=`SOURCE_CONTRACT_ESTABLISHED_CAUSAL_HOOK_NOT_PROVEN`。报告绑定原手工命令、原始P→Q错误、两份SAV战争/国家状态、全部scope合同及当前冻结5源；只复用既有封存primary，不重复复制包或改原报告。

历史控制分析SHA `06d32b4e80bf46c74e717e4304ded8f32d1d0d5544239ae4550fe03ccb0fbe7a`。已逐字核对封存primary与当前原版5文件相同，完整SHA都在新JSON：`nomads_events_1.txt`=`9706995838e51276c1348f5d0bb31e2a97b36e0a2c92a79de25b6065e091fb0a`，`00_on_actions.txt`=`7693e64fbe974f37db0c68969d10f7bdeec585ce59ca497b5e27ecd69ff8f306`。本轮没有UI、原生effects、生产/工具/夹具/原日志/存档或Git操作。
