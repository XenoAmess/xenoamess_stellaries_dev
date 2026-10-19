# RC7普通q2夹具未创建目标的离线调查

root明确交接诊断role r7normalready.sav（2201.05.28，SHA `c11216d66545c69aacf5686e80a0ad68fa049a8640ef3fbd25663f70e86d0cc6`），固定run164112Z、同RC7 manifest；该ZIP与敌星dupereload相同，eep_reg_owned_source不存在。原672字setup与637字inspect有实际Enter；root提供当前日志筛选事实：03:29:36只有EEP_REG_Q2_TARGET_MISSING，没有EEP_REG_Q2_CREATED。已执行旧重复回调marker完整，因此不能无证据归因于灭国弹窗拦截键盘。

本次只读当前已产生且root确认无活动normal worker的r7normal前缀快照、既有封口case来源、原命令、本机原版用法及生成scope文档，不读活动r7pkfire或当前活动日志，不UI/Git，不改Mod/原fixture/原工具/存档。目标是区分外层物理core2→solar_system、random_system_planet、各limit谓词的真实作用域和可选对象问题。先保留原失败，再给最小已有命令修改建议；根因未由引擎实测证明前，明确标为假设。

若静态原版/文档仍不足，可准备每条≤1000字符、纯log且不修改任何游戏对象的逐谓词probe；创建前先在本文记录设计与预期区分能力，并按D:/workspace/open_kaishek使用说明完成新P fixture静态验收。没有获得该工具实际通过不得把probe交作已验收；本agent不执行UI，只有root实际下令后的新证据才可确认运行根因。

验收为原输入/Enter及失败SAV绑定稳定、原版/生成文档引用精确、假设与已证事实分开，probe（如有）有实际静态验收记录且不含状态写入。仅调查结论及可审阅probe交root，不把失败ready当normal成功基线。

## 逐层纯日志probe设计（创建前）

当前诊断SAV仍有core2、Mother151及同一八个home候选；system5原生planet列表完整为0..9。原672/637输入逐字等原fixture且Enter真实，实际alias仍无；root补充error.log没有03:29新增parse/scope错误，旧02:45/02:53记录不归因于此段。原版advisor_events.txt:392起使用capital_scope→solar_system→random_system_planet；冻结生成effects.log:5368明确random_system_planet包含殖民与未殖民planet，支持scope galactic_object。triggers.log:1276/1923分别声明is_colony/is_under_colonization支持planet/ship/colony。因此先不能断言某个原谓词非法或原scope link错误。

准备隔离静态fixture `testing/normal_selector_probe_1020/`，仅用于Kaishek包级解析，绝不安装；JSON同时提供可复制的纯console effect文本。三条命令均≤1000 ASCII字符：A逐层log ROOT／CORE／SYSTEM，every无条件逐对象log并用一次无条件random log区分遍历器；B在every内分别log is_colony=no与NOT(is_colony=yes)、is_under_colonization=no与NOT(yes)、非星、非人工，marker次数给各谓词通过数量；C分别log非core／非reserved与原完整limit通过对象，再用原完整limit随机选一个只log。仅log与选择/条件，不set任何flag/alias/owner/资源/pop/进度，不创建殖民地或SAV编辑。random仅使用引擎正常选择，本probe不声称整个SAV字节只读。

A无CORE、无SYSTEM或无EACH可区分解析入口／目标／scope link／遍历器；B、C可定位原limit中实际排除全部对象的谓词。若every完整limit有候选而相同random body不进，再单独调查random行为。probe输出前根因仍待引擎确认；不直接改672原fixture，也不让失败重试污染后续成功基线。

## probe实际静态验收

已先读open_kaishek的README、Stellaris profile说明及包验收入口，然后使用其现成`tools/accept_stellaris_mod.py`，参数为隔离probe目录、真实游戏目录及本run EXE SHA `400df27c82ddc845aa9dce79bd468d81f18f060d299cd263e3afa93aef4f7a83`。实际EXIT0，PASS，2/2 P脚本解析和roundtrip通过、errors=[]，无本地化文件适用项。该入口声明syntax/package及有限scope切片边界，不能证明本probe的引擎scope或选择器运行语义；没有改工具或生产Mod。

可执行文本位于[console-commands.json](../testing/normal_selector_probe_1020/console-commands.json)，SHA `3b49b87667869efc4aeca27155de08882775237bf2268ea9f62f4890fb1b65ff`，A/B/C分别370/542/731字符。静态报告[rc7-normal-selector-probe-open-kaishek-1020-v1.json](evidence/1019-analysis/rc7-normal-selector-probe-open-kaishek-1020-v1.json)，SHA `912613768f10d5fcacddc36c79620ff83b9e10923305fafeee10d8d8fe7b4b7c`。这些只是待root下令的诊断probe，不是成功normal源，不修改原672/637，也不改变原幂等结论。

失败收件另建`evidence/1019-rc7-normal-fixture-failed-attempt-v1`：只复制首次明确交接时列出的精确文件名快照（SAV、audit、receipt、原输入/Enter与原UI链），不再以r7normal*通配把后续正在执行的probe吸入。实际数量以复制清单为准，原失败与原body不进的事实保持。manifest／frozen Mod／原命令和scope文档以明确来源引用；当前game/error日志只有root报告的筛选事实，未独立读取或伪造日志原件。

## 失败包封口与当前边界

失败SAV/audit/receipt双读稳定并精确绑定原path/date/SHA，ZIP CRC通过；45份明确白名单原件逐字节相同，2份派生摘要／复制回执，共47payload、2,437,103字节。9组原图/OCR绑定PID37300，11项canonical及5项外部只读来源SHA独立复核。实际原始输入与两个Enter均绑定；本失败没有运行normal settlement或把readiness标PASS。

原生成scopes.log:334–336明确solar_system支持planet并输出galactic_object；effects.log:5368–5377明确random_system_planet包含colony or not、输入galactic_object；triggers.log:1276–1278、1923–1925明确两个殖民谓词支持planet/ship/colony。原版an4_events.txt:119–126也使用random_system_planet加is_colony=no。本机静态资料尚未唯一定位失败根因，所有建议仍待root实际probe结果；没有先更改原672命令或归因旧错误／弹窗。

- [失败index](evidence/1019-rc7-normal-fixture-failed-attempt-v1/index.json)：`138d70a3b047629b3bb19acea7d1871da6472429acc639c72ab38a0430aca635`
- [失败verify](evidence/1019-rc7-normal-fixture-failed-attempt-v1/verify.json)：`bdade8904d5f621361354bdfc67c32e46146869f799414d663ca9f6f958d2f52`，9/9，限定PASS_BYTES_FAILURE_PRESERVED_ONLY。

当前可交root的文件集合：本文、失败包全51文件、隔离静态probe目录全4文件、Kaishek报告1文件，共57文件。失败包已封口；后续probe事实和成功修正必须另包／另补充文档，不改失败原件或本包的运行结论。旧只读候选复核只证明原生字段与静态选择器相容，不能据此声称引擎已选中八候选或反改其原报告。
