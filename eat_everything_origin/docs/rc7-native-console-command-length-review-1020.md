# RC7 控制台1050字符导出的长度复核

## 目标、范围与验收标准

root要求先核已成功原生控制台动作及实际输入链的长度边界；只有没有1050以上成功证据时，才等义拆普通舰十getter命令。此页先记录设计：只读明确sealed的RC7 growth包及现有输入源码、既有控制台长度调查、原版console.gui，不读活动run或尚未授权raw/日志，不操作UI/Git，不改Mod、工具、原计划或原命令。

接收标准为既有原生action的完整text/长度/SHA、submitted物理输入与相应native SAV实际导出和原检查结果共同成立。不能仅凭action写了submitted=true就认定引擎完整接收，也不能把其它GUI控件的1000字符限制当console硬上限。若已有更长成功命令，保留原1050命令，并新增仅只读报告 `evidence/1019-analysis/rc7-native-console-command-length-review-v1.json`；不为不满足条件的拆分另造未来probe或新验收步骤。

## 只读发现

本次允许范围内，sealed `1019-rc7-growth-v1/run/` 的九条final-effect真实输入均为1177个ASCII字符，完整text与当前collector `export_command()` 逐字相同。它含原十modifier export及最后两条max hull/max armor trigger export。九条均保留物理输入action、提交记录、对应final native SAV及原matrix校验；原1850报告分别验证三防与十export、最后两项trigger。因此已有长于1050的完整原生生效记录，不需要为ordinary十getter追加拆分。

这里的“最长1177”限定为本次明确扫描的sealed growth动作集合，不声称是整个历史资料库的绝对最大值。证明1050输入长度已经落在已有成功长度以下，并不等于证明任意长控制台命令或所有作用域内容都有效；ordinary的新country.every_owned_ship语义仍按既定原生两分支真实导出确认。

既有 [护栏调查](colossus-native-guard-batch-1019.md) 已确认原版 `interface/console.gui:22–30` 的console_edit没有max_characters/max_text_length；100/1000来自其它控件，不能套给console。本轮再只读核实际文件和既有输入链。`runtime_1019.command_open`限制stage安全格式及单行、实际console可见和1024×768几何，不限制command长度；`runtime.py.physical_submit`逐字输入完整value并记录原text/物理回车，没有1000截断。基础harness也没有该数字限制。以上是当前源码可见边界，不替代引擎内部长度上限证明。

结论：原1050 ordinary命令和其静态PASS来源保持原字节。本轮不增加两次而非一次的console输入、不改先前最短执行动作数，不创建拆分fixture。精确JSON会绑定九个action、对应九个final native保存、receipt/index和原matrix末尾getter实际通过项；未新运行游戏。

## 封口与精确调用字段

新增 [只读长度报告](evidence/1019-analysis/rc7-native-console-command-length-review-v1.json) SHA `26784580189df0f69bea3323280b1d85dce0ad4ba3a18b579f2b161171462cf8`，明确扫描247份sealed growth action，九份>1000实际输入全部是同一1177字符命令；没有读取当前活动run。每条绑定九个final SAV和原collector receipt，逐项复核原matrix十export、两末尾max getter及实际诊断日期共13个原检查，九组全部通过。它们是原1850报告的已有检查子集，不能另算新增117项实机测试。

例如 `r7mx-n08-c10000-final-effect-command.action.json` SHA `3c1387e878a2530865df4b391ec2920132d6185037616abef0543feb2e9683f2`，完整1177字符且physical scan code0x1c提交；其实际final SAV SHA `f733e79be5cb9cac7ad9101fc171d5bf4ddfe5fdc7adce479c3b8dae6bd2eb52`。原报告证实最后两trigger分别实际导出1725960和1427025.6，不能以“输入action存在”替代实际尾部生效证明。

root可以直接从新报告的 `ordinary1050.command` 读取原样1050一行；`ordinary1050.command_utf8_sha256=b1dc9e5f73d388af4172f55f394fc1a2599201c2b30316d064762e161e8d3ccc`。它与原minimal plan中`commands`里name为`ordinary-ten-modifiers`的command逐字相同，原含LF文件SHA `90f6c0e9c7f07b0862a2c9a665e0fd18b5483d430f7446f38a34e5d209ba39b0`不变。未新建或执行两条拆分命令，既有三probe计划及最短顺序不变。

该长度结论仅针对1050已有更长先例；1426字符Mother14命令仍只有既有静态PASS，本报告不把1177实绩写成1426已实际校准或任意长度上限证明。若root另行选择将其控制在操作偏好范围，可单独指定；本次未擅自改它或扩大任务。
