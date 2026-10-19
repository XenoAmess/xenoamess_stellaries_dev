# RC7全新蜂巢经济实机采集

延续既有三政体经济方案，在洁癖纯经济与后置媒体保存完成后，root 从原生帝国
选择列表实际 OCR 行 `EEP 02有机吞噬.` 创建全新 r7hvc。树固定为 RC7
`61b34f6dbdc277c44364889d5f1e1cd2773a4624786bbf0d538079fc6ba4feb0`，
run `20261019T164112Z`、简中单 Mod、200恒星／3AI／尉官；没有从成长压力档接续。
执行链仅 new_game →显式RC7 tree/version的 make_plan→collect。全年验收仍按
十二个单独原生月份、年末 auto/UI 对照、四项受控操作约束及独立复核，不提前
把首月观察提升为全年通过。

原生初始 r7hvcm00 SAV SHA256：
`c2a8abdbad9c4a3f05af4e691095b122c1b8478d4d2a43e9cdd407620ab2d518`。
初始1殖民地、库存200；Jan1当前预算+65.48168仅为初始状态，不能当作首月
岗位重算后的收入。首月 r7hvcm01（2200.02.01）SAV SHA256：
`677ff9f49f2cc5d546b8a8e17d66cfcd4355a4e26f40e3dc9d17d7486f2a630c`。
实际当月收入80.98098、支出57.83632、净电+23.14466，库存223.14466。
原生 pop_jobs 182 的 technician_drone workforce=507、max_workforce=1200、
workforce_limit=1200、bonus_workforce=50.7、planet=0，已实际就业，不是零人。
这些是原生存档单位，不把它们改写成未核对的UI人数。未注资／交易补贴／闭岗／
拆船；最终四约束仍交接独立动作审核，不冒充全系统输入审计。

02:00（上海时间）已完成m01与m02，全年继续采集。后续完整包与报告独立封口，
不把尚未生成的月份或停止后日志填成存在。

## 完整年度已采集与原生独立复核

root明确交接session7895 EXIT0后，按事前审核方案接收固定 `r7hvc`，原v1分析器
以 `--branch hive --prefix r7hvc` 正常EXIT0，生成新的
`evidence/1019-rc7-economy/hive/`。57件原始payload、7,594,175 B，
原报告为PASS_SCOPED、7项startup全true，四项操作约束仍保留null，未修改原分析器。
报告SHA为 `a2786764d961aee288746e5a1e2d38cf55a16fbd5051d738572540daf58d6d60`。

实际核心物理11、pc_hive、m00人口5300，Mother fleet152/ship971；
原生government/founder确认是有机吞噬蜂群，没有Lithoid/Machine traits。
首月岗位仍为workforce507/max1200/limit1200，正常ships、components、
buildings及原生district子类别维护真实存在，母舰维护折扣与基线保持。
12个月实际净电为23.14466、23.76903、24.39361、25.10694、25.73086、26.35463、
27.06744、27.78042、28.49285、29.11597、29.73933、30.45124，全部非负；
能量200→521.14698。Jan1预算缓存65.48168保持原样记录，不算首月实际收入。

独立第二进程逐原生复核14份ZIP、两期完整budget、库存、岗位/人口、实际六core布局
及零成长、59文件RC7tree与原生维护父链，8/8通过；
`independent-verify-v1.json` SHA为
`87ce27514aa800715d4982d0a88ce5c692a63de1dc02538d2c11c3d553ad1916`。
m12/yearUI原ZIP逐字节相同，SAV SHA为
`9191c0e4ca368d09564a3f42693015bf4deef616234dd0bbdadab5306cb5d60b`。

交接“receiptSHA”字段已与root辨析：
`42bf7a730d70d4e78ba658f17159f36c74f1aabace85ecc472e0c23478c83a9d`
属于 `r7hvcyearui.native-save.json`；
`01c3f9106ad52f77ceec1f33211f37779b9da2572cb76b0d867ca04cd7b161ea`
才是总 `r7hvc-economy-receipt.json`。三对象分别按实际路径绑定；
最初拿yearUI回执SHA比总回执的指纹失败保留为对象辨析记录，没有源字节漂移。

## 完整动作链与四约束封口

原件白名单277件；221件UI原件另存
`evidence/1019-rc7-hive-economy-worker-ui-v1`，8,235,845 B，56件同前缀原件
加manifest共57件薄包原件只作canonical引用，不重复复制。index SHA为
`b2f8c6dbfa8f7e41e2666046b7353f4489bfc2f0cff936ffa07702768ea6d3eb`，
含99个canonical、50对GPU/OCR及12个实际receipt HUD；独立verify11/11，SHA为
`d4fdef5ba15e89fa8e7b3af4690b1357f379108809e5e16d43741e78c7b0539b`。
20件现执行源全部与Pu已封口canonical逐字节相同，以本Hive单独root交接与输入链绑定；
原生维护父链和旧新折扣也复用已验证原源，不重复Mod。

独立操作审核 `evidence/1019-analysis/rc7-r7hvc-economy-operation-review-v1.json`
SHA为 `5ac8062ec6cdeeb3d55962eaae10f81e90c10bb76fd67dbe18e8b7ce88986b89`。
实际108 action中的14个type_text仅12条FF30与两次存档名；25个鼠标动作只属于
新局/保存/控制台聚焦。结合root的纯经济worker范围和原生库存/岗位/舰船保持，
四项操作约束在独立限定报告内为true；原v1报告四个null不改，不称全系统输入审计。

新 `rc7-r7hvc-startup-economy-partial-proposal-v1.json` 的两组case仍PENDING，
尚缺真实停机日志与root最终汇编。没有读取r7mc或活动日志，没有改Pu或旧partial。
本次可stage：本页与 `rc7-economy-completion-review-1020.md` 的本轮更新；
`evidence/1019-rc7-economy/hive/`、`evidence/1019-rc7-hive-economy-worker-ui-v1/`
完整目录；上述新操作审核及新partial提案两份JSON。没有其它提交范围。
