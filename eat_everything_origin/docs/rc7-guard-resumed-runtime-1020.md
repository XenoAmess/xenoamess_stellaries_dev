# RC7 恢复后的保护条件运行记录

沿原四组三档执行卡，不增加矩阵。当前run20261019T204055Z、PID24520、简中单
生产Mod；已从主菜单真实载入原r7pkbase并另存。O/M/V命令仍按V同ID优先覆盖，
生产包及原checker/inspector/receiver不改。

## A组实际ready

十条既有构造命令已实际输入，r9gaR原生日期2201.01.21。核心物理2、Mother151，
九个不同源均存在，七个构造殖民地各有100真实人口且owner/controller0：

| 别名后缀 | 实际物理ID | 原生状态 |
| --- | --- | --- |
| guard_active | 1 | eep_active |
| guard_devouring | 5 | being_devoured |
| guard_credit | 8 | eep_credit_done，源仍活 |
| guard_destroy | 4 | eep_destroy_done，源仍活 |
| guard_secondary_core | 6 | eep_core，实际绑定仍为2 |
| guard_artificial | 7 | pc_habitat，实际殖民地23 |
| guard_qzero | 3 | size2、两个真实d_lithoid_devastation |
| r6_uncolonized | 1071 | pc_nuked，无owner/colony，人口0 |
| r6_neutral | 28 | pc_ocean，owner16777218，实际人口5357 |

中立owner实际type=default、capital字段2为colony ID，不是物理ID；war0只含
actor0和country1，未与该中立国交战。人工星判据来自本机构建原生
`00_planet_classes.txt`的pc_habitat段`is_artificial_planet=yes`；引擎生成
triggers文档明确is_artificial读取planet_classes设定，不靠测试flag命名推断。

下一步先逐项核ready前提，再自然FF1保存I（2201.01.22）；用新的主菜单薄包装
真实加载同一个R，执行原batch_dispatch、V uncolonized_dispatch、M neutral_dispatch、
原current_bound_core_reject，再FF1保存F同日比较。每源独立运行原no-settlement，
另核成长/奖励/六country与fleet层数及唯一增长修正；完整strict差异保留。
任何目标不存在、前提消失、未派发或日期不符均不得判拒绝成功。

B/C/D仍待执行，A构造成功也不代表负例已通过。所有结论按实际完成阶段追加。

首个A idle自然tick另出现原生`on_action_events_1.txt:8490`向
`EEP_GUARD_QZERO`添加district_city失败：该刻意size2＋两损耗deposit夹具只支持
1区划，殖民初始化的延迟原生布局事件尝试超出上限。保留完整错误和时间链；
须分别检查I/F的q0源仍有真实人口／殖民地、两损耗和size2，不能因总账未变就
忽略构造失效。此处不删日志、不归为生产脚本已通过，最终日志审计另逐项分类。

## A组完成与归档方案

R为2201.01.21，I/F均为2201.01.22。十个原no-settlement任务全部
PASS_SCOPED；原receiver也独立接收三档及base并复算十任务通过。各角色的
真实前提持续，核心可用、合格起源与灭绝机械政体均在；I/F的成长账本、
last三项、随机组件奖励和六层数及Mother对应字段一致，原growth检查两支均通过。
完整strict差异保留，不把作用域结果当作全存档相同。

现建立独立A包，仅复制已完成r9gaR/I/F、r9guardAbase及r9ga操作、精确输入
导入回执和receiver缓存。源文件先后SHA一致、SAV ZIP CRC、截图/OCR图SHA
及原生save/audit/receipt绑定逐项核验；归档原字节，索引引用项目内canonical
路径。活动日志仅保存明确标为诊断的摘录，最终停机日志另验。A可支持未殖民、
人工、吞噬中、已结算、中立五项；all_core仍等B/C，target复验等B，invalid
无成长等A/B/C/D及既有取消，不提前封整组。归档方案先于包及索引写入。

A包已复制254份原件（16,627,112字节）、四份原生档及48对截图/OCR，全部
SHA、ZIP CRC和图像绑定通过。原receiver十任务均PASS_SCOPED，原始前提与
增长补充报告均保留。仅将上述五项记true，索引现102 true／36 null，全部
18组与组件仍PENDING；未把活动日志附作final log。
