# RC7原生跃迁接收：本轮5→7

## 目标、范围、设计与验收

2026-10-20 root明确本run `20261019T164112Z`全部`r7jump*`已封口，允许本线程离线接收。只新增本页与`docs/evidence/1020-rc7-native-jump-v1/`；不修改已提交配置／初始化／source-scope文档和包，不操作UI／Steam／Git，不读取新`r7pk*`原生内容或活动日志。仅按root授权读取同run已完成receipt metadata以满足原inspector provenance扫描。

候选固定0.4.0-rc.7、59文件树`61b34f6dbdc277c44364889d5f1e1cd2773a4624786bbf0d538079fc6ba4feb0`、简中单Mod及精确EXE。源图／动作、SAV／receipt／audit原字节归档，canonical manifest／现有源码／配置包复用引用，不重复59文件或原版安装。

| 本轮角色（root封口交接） | 日期 | SAV SHA |
| --- | --- | --- |
| ready `r7jumpready` | 2201.01.07 | `87b40d759d0da5340b117f1a917f34cf1f85834260b1b8e5f2d8767496f99c4c` |
| wind1 `r7jumpwind1` | 2201.01.08 | `5d26ee990b421c9eb4744040122b55bc345fcc4eca071f3837fd4ca00739f727` |
| arrived `r7jumparrived2` | 2201.01.21 | `325808af0d1efb9ae1f6c529dadcefb674aea5c818609efce2e5fc9e0ff8f25c` |

事前验收：同Mother fleet151／ship1044／design1844、core物理2；ready／wind1 origin5，目标实际system7；wind1真实`jumpdrive_order.system=7`及14天预热Jan7→Jan21、can_reach=yes；arrived同Mother实体位置origin7、订单完成、last_jump_date及jump_drive_cooldown原生状态；reference175／1068始终在5。不能把set_location／旧galaxy origin0／system196当成本次实际jump。

GPU须保留真实绿色有效目标／实际物理下令、到达后`r7jump-cooldown-hover.jpg`原生200天／伤害−50%／速度−50%说明、日期／帧SHA及动作。14天从实际订单读，不从菜单点击日猜；FF1＋13只推进已有订单，不能伪造到达。独立native解析结合原mother checker核装配／10yard保留，成长账本与q/C/G/D不因jump增加；跨日自然研究／人口进度变化不要求伪同日恒等。

root已说明首次`r7jumparrived-menu0..3`因console/debug遮挡未保存SAV；失败原GPU／动作全部归档，实际有效after只有`r7jumparrived2`。不补造失败SAV或receipt。报告只支持`actual_jump=true`的本次限定事实，整配置case等待完整终态logs及共同审查；源隔离提案另行引用，不把其SOURCE_SCOPED结论冒称跃迁实机。

## 执行结果

本轮接收完成。实际跃迁报告25项检查全部通过，原`check_1019.py mother`到达存档检查14／14通过；独立归档复核18／18通过，318个带类型引用逐件解析并核对字节SHA。以上均为限定范围结论，未把原RC6结果或旧母舰ID带入本轮。

实际三存档均绑定country0、Mother fleet151／ship1044／design1844、核心物理星球2。Jan7起点5、Jan8仍在5，原生订单指向7，`jumpdrive_windup`明确`windup_time=14`、`start_date=2201.01.07`、`end_date=2201.01.21`、`can_reach=yes`。Jan21同舰队和舰船实际抵达7、订单清空，舰船直接字段`jump_drive_cooldown=yes`及`last_jump_date=2201.01.21`同时存在；这两个字段不是flags块。原生Relic参考fleet175／ship1068始终在5，未跟随母舰移动。

已直接目视原始GPU绿色有效目标、启动跃迁和实际目标点击后的“准备跃迁至EEP_JUMP_TARGET：14天”，以及到达后Jan21原生悬浮提示：冷却200天、武器伤害−50%、亚光速速度−50%。物理输入动作及四条实际已提交命令原字节全部保留：绑定邻接星系并命名、`survey`、`fast_forward 1`、`fast_forward 13`。本阶段不存在`set_location`命令。14天来自实际订单；这只证明此目标可达及实际冷却提示，没有测最大距离或等待200天验证冷却终止。

三存档的母舰设计原始文本、10个船坞与全部EEP国家成长变量逐项完全相同：C0／G0／D2／made0／worlds0／L0／reward0／pending0及六类随机强化计数均保持0。跨日普通资源／人口／研究自然进度不作全存档恒等断言。C0母舰的此轮跃迁不补成高等级成长样本的`unlimited_growth.jump_and_shipyards_preserved`。

首轮`r7jumparrived-menu-0..3`失败图与操作完整保留；原生console／debug覆盖导致菜单识别失败，没有生成SAV或receipt。原生恢复后的`r7jumparrived2`是唯一有效到达角色，报告未把失败帧补成成功证据。

## 封存与合并接口

新包`docs/evidence/1020-rc7-native-jump-v1/`共195文件，其中193个payload合计9,381,357字节、185个原始阶段文件合计9,165,078字节，并引用28个既有canonical对象。20生产源逐件复核当前字节后引用既有Machine source闭包，只复用源文件，不继承其全年经济执行事实。既有配置／初始化包及所有原件未改动。

| 对象 | SHA-256 |
| --- | --- |
| `archive-index.json` | `2b0a727f7e8f4fd0868ecb7bc36449315e37d16db8bc0b66486523562a523c61` |
| `verification-v1.json` | `232269e2060883cb3a7d0f89d634ed165def986dd930663f6184dfb79b7b89d3` |
| `actual-jump-report-v1.json` | `76500a18a3bbca7bf3a44680cb005aff01836652ebe265a0c535aff265fdc046` |
| `native-jump-observation-v1.json` | `0699bcdd0d8dd318b9f470b452fcfb57ff3ea0a7d8e3afb19b331693d2d36a10` |
| `partial-case-proposal-v1.json` | `8ce2de79a060220775393a957220fbdb34a0ec0e7aa8777589fe137851903dac` |

合并接口精确为`case_id=mothership_configuration`、`supported_checks.actual_jump=true`、`case_status=PENDING`。原配置partial里的`actual_jump=null`保留为历史阶段快照，由此新partial补充；普通主宰隔离继续引用独立SOURCE_SCOPED提案，不冒称实舰对照。完整case仍缺本run停机后的完整日志和共同终审。本接收没有读取新`r7pk*`原生内容或活动日志，也没有操作UI／Steam／Git。
