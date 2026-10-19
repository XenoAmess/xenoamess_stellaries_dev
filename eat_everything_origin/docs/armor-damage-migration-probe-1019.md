# 1019 旧母舰迁移：装甲损伤接口调查

## 目标、范围与验收

为旧版j13ten付费十船坞队列夹具寻找4.5.2可原生施加且可留存的装甲损伤。调查只读本机生成effects文档与原版脚本，不操作UI、不改Mod、不编辑旧SAV。母舰必须存活，不能改变付费队列或国家资源；任何实机尝试均由主线程在独立功能夹具完成。

优先寻找明确的装甲伤害／类型伤害接口，其次核查原版是否实际使用 `repair_armor_percent` 负值或可证明为负的变量。仅文档允许数值、解析允许负数，不足以证明负修复等于施伤。若没有原始有效用例，只交付可审查探针；不能在没有证据时将猜测写成可靠验收方法。无法取得稳妥装甲接口时，旧母舰损伤迁移可以明确限定为已证实的舰体与护盾损伤子集，装甲单独记未覆盖。

验收比较同日原生before／after的Mother身份、位置、三防current/max、paid queue逐项费用／进度／购买者与国家资源；施伤和迁移分成两个步骤分别保存，避免将修复失败、自动恢复或排队进展归因为设计迁移。旧SAV原始字节始终只读保留。

## 原生接口与准确名称

本机4.5.2启动生成的 `C:\Users\1\AppData\Local\xenoamess_stellaries_dev\runs\20261019T072723Z\logs\script_documentation\effects.log`：

该effects.log SHA256为 `f7fe1e0b3e5567597db5d39a3f36b847b36cbc2a45fd68935540f9e8bca552df`。关键原版调用 `events/infernals_crisis_events.txt` SHA为 `da6d18c2642d2a0fd3357adff8e247ade87ab3f712b21daa1ef152d695017dfd`，其变量文件 `common/scripted_variables/09_scripted_variables_infernals.txt` SHA为 `2d22619e51c886c8beb808bf76fedcf0c4f1e9c14114d448753849e928fa9c5e`；独立Grand Archive用例文件SHA为 `1e3f769c1693d1cee3c137708f84eafebbbfedd726bc730eb41999b49f1c5ccf`。

| 原生effect | 行号与支持scope | 文档承诺与边界 |
| --- | --- | --- |
| `reduce_hp`／`reduce_hp_percent` | 490／494；ship | 减少舰体绝对值／相对值 |
| `reduce_shield` | 498；ship | 减少护盾绝对值 |
| `damage_ship` | 502-506；ship／fleet | 数值或 `{ amount=120 attacker=<ship或country> }`，attacker可选；文档未说明伤害层次，也没有damage_type字段 |
| `repair_armor_percentage` | 1492-1494；ship／fleet | 恢复一定比例装甲；准确后缀是percentage，非repair_armor_percent |
| `repair_armor_amount` | 2820-2822；ship／fleet | 恢复一定数量装甲；文档未承诺负值施伤 |

对该生成目录的health／armor／damage接口检索没有找到 `reduce_armor` 或设置当前装甲的effect；`set_ai_armor_ratio`类字段是自动设计比例，不是当前装甲血量。这个有限结果不外推全部闭源引擎或未来版本。

## 更有依据的装甲候选：damage_ship

直接找到原版正面用例，优先级高于猜测负修复。`C:\SteamLibrary\steamapps\common\Stellaris\events\infernals_crisis_events.txt` 的country事件 `infernals.2020`，注释“Conduits do damage to hostile ships”，在1705-1709对同一艘敌船执行：

```text
damage_ship = {
    amount = @inf_conduit_ship_damage # armor
    attacker = event_target:conduit_attacker_ship
}
reduce_shield = @inf_conduit_ship_damage
```

原版 `common/scripted_variables/09_scripted_variables_infernals.txt:37` 给 `@inf_conduit_ship_damage=50`。原作者明确把damage_ship旁注为armor，并另行reduce_shield；这为“damage_ship可伤甲、且无需先清空护盾”提供直接脚本意图证据。它仍不是本次Mother的实测结论，不擅自补造 `damage_type=armor` 参数，也不宣称完整穿透／溢出算法已公开。

另一独立原版用例 `events/grand_archive_events.txt:7939-7961` 为死亡伤害导出max hull与max armor后合计，再乘伤害比例交给damage_ship，没有把max shield加入该伤害基数；这与上述甲／舰体通道意图一致。`events/ambition_events.txt:1223-1226` 等处又实际使用带attacker的amount形式，:1547使用纯数值250，确认这两种都是原版真实调用，而非只有生成文档。

## 负修复的调查结果

只读扫描原版 `common` 与 `events` 共2234个TXT文件中的实际调用（排除注释行）：

- `repair_armor_percentage`共3处：`ambition_events.txt:1302`为0.25；`biogenesis_crisis_events.txt:3311`引用原版 `@behemoth_healing_armor_percentage=0.30`；`grand_archive_events.txt:7860`引用 `root.local_heal_value`，该分支在7850明确要求值>0。
- `repair_armor_amount`共1处：`common/inline_scripts/ship_components/bio_weaver_healing_weapons.txt:32`引用 `@bio_healing_t$TIER$`，原版component_cost脚本变量t1～t6依次32／42／54／70／92／120，均为正。
- 未找到负值调用，准确键 `repair_armor_percent` 调用数为0。

因此不能把 `repair_armor_percentage=-0.1` 或 `repair_armor_amount=-120` 写成受支持的施伤方式。若damage_ship探针也不能伤甲，负修复至多是独立恢复点上的后备实验；不能直接用其未验证结果作为损伤迁移验收前置条件。

## 主线程最小原生探针（尚未执行）

推荐先只用文档支持且有明确原版armor注释的 `damage_ship=120`。旧j13ten候选原始SHA为 `834ea5325f93e3d3e92a44aabccd87195564cd4f1292d4439ae865eba5af8d2e`，路径与Mother／十付费队列真实基线见 [历史夹具清单](evolution-components-1019-old-save-candidates.json)。载入后的实际值须重新读原生SAV，不能拿旧档数值替代当前before。

1. 游戏保持暂停；先保存加载后的干净before，确认绑定唯一Mother存活且当前hull／armor均明显大于120，队列仍是原付费队列。记录实际三防current/max及库存。
2. 在country控制台effect中仅对绑定Mother的实际ship执行下列片段，省略可选attacker以不引入额外攻击者归因：

```text
event_target:eep_mothership@this = {
    every_owned_ship = {
        damage_ship = 120
    }
}
```

3. 同日、继续暂停，保存damage-only。只有实际current armor下降且Mother仍存活，才把该步骤作为有效装甲损伤夹具；若仅hull／shield下降或无变化，原样记录结果，不能称armor已伤。不清空护盾、不生成敌舰、不发动真实战斗，也不调用整个原版危机事件。
4. 分别使用已证实的reduce_hp和reduce_shield取得其它两层的非致死损伤；另存同日pre-migration，确保队列、库存和日期未变。不要把多种施伤与迁移合成一个无法归因的命令。
5. 只执行既有设计迁移，立刻保存post-migration，逐项比较身份／位置／current/max及归一化损伤比例、paid queue完整项、库存；再做同日reload检查。max变化时不能只比较current绝对值而忽略比例，也不能用自动修复到满血当作保伤成功。

120只是在已确认大血量Mother上的小额非致死探针，不保证damage_ship不触发其它原生伤害回调；付费队列和国家资源保持不变仍须真实before／after证明。若无有效装甲探针，则报告仅覆盖舰体＋护盾损伤保留，装甲损伤迁移明确未覆盖，不能宣称三防损伤全部通过。

## 当前结论

找到原版明确标armor的 `damage_ship` 正向调用，足以支持优先做小额原生探针；没有找到负装甲修复的原版用例，故不推荐将负修复直接当可靠接口。本子任务没有执行探针、修改生产Mod／UI／旧SAV，也没有取得装甲受伤或迁移成功的实机证据。
