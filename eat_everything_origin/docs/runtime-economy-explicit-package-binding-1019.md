# 经济采集器显式候选树与版本绑定

## 实施前目标、范围、设计与验收

仅修改 `tools/runtime_economy_1019.py` 和对应离线测试，支持root明确冻结的RC5。
不操作UI、启动／加载游戏、修改生产Mod、外部工具或Git，不改历史报告与采集证据。
既有CLI默认仍为RC4树06485dc…及0.4.0-rc.4；新增 `--expected-tree` 与
`--expected-version`，RC5必须显式传tree
`1cc8b77c28f3d59b0d840982c7f039a209cb66f3e26d9c3280ad2dfa0f9dbd52`
和version `0.4.0-rc.5`，不从manifest反推“期望值”。

期望值写入plan，make_plan、collect执行前和实际LiveBackend入口均用该指定值
核对manifest两个tree字段、实际59文件完整集合／SHA／树、descriptor版本、
static_gate的tree/version/files/report SHA，以及原始open_kaishek整包PASS与共享
CSV／PK来源合同。计划后manifest字节改变仍拒绝。缺失旧plan版本字段只按RC4
默认解释，不能把RC5树的旧plan当作RC5授权；显式错误tree/version、来源错配、
descriptor篡改或report字节改变必须在连接后端前失败。

调查发现旧经济validate_package复用growth.package，还额外锁定旧RC3六核心源码
模型；RC5修复迁移后eep_mothership_effects.txt已变化。纯经济采集不重新证明
成长源码系数，所有候选使用完整经济包来源绑定，不再调用growth.package；
默认期望值仍严格是RC4，不随manifest或成长模型变化。实际六核心各一件及AUX6—11槽位、
C／L／R／tier／奖励零污染、简中、唯一Mod、精确EXE、monthly autosave和十二次
独立真实月档、原始receipt防覆盖、年末同日auto/UI比较、失败留证与收尾均保留。
不修改成长工具或旧源码模型来适配RC5。

在原8项离线回归之外增加定向正反测试：RC4默认保持、RC5显式参数贯穿plan与
执行入口、未显式选RC5／只换单一参数拒绝；独立校验真实候选文件树和完整文件表，
不把validate_package本身全部mock掉来证明绑定有效。实际run143452Z可仅做纯文件
package核验，不运行collect、不虚构经济或UI通过。记录改前／改后工具和测试SHA、
测试命令／结果与root可执行的精确CLI。

## 实施结果与限定验证

实现已完成。期望tree/version由CLI传入并写入plan，make_plan、collect和
LiveBackend构造入口均传递原值；LiveBackend在父类桌面导入前再次验证。所有候选
独立完整绑定，不调用growth.package、不修改growth工具或源码模型。

实施中成长工具并行改为RC5模型后，额外默认RC4调用曾短暂拒绝旧包。主线程明确
要求经济完整绑定后彻底移除该模型依赖；先更新本设计再删除调用。RC4默认版本／
tree、实际包字节和经济零污染规则不变，不以新成长模型重新解释历史经济报告。

定向命令：

```powershell
python -m unittest discover -s eat_everything_origin/tools -p test_runtime_economy_1019.py -v
```

19项全部通过（原8项及11项补充）。新增包含真实文件／完整树／descriptor与报告
字节的正反绑定、只改一个CLI期望值拒绝、manifest计划后变化拒绝、执行错误版本
在后端创建前拒绝、显式参数贯穿CLI／plan／collect／LiveBackend，以及双文件表与
tree全部一致但descriptor版本错误仍拒绝。CSV／PK解析器只在文件绑定单元夹具中
隔离，其拒绝结果传播另有负例；真实候选纯文件检查使用未mock的两个共享合同。
合成输入和FakeBackend不证明引擎经济。

未导入runtime_1019或运行collect的实际纯文件结果：run112808使用RC4默认通过，
manifest SHA为a83c605727f30a1d68db0e076348d814824d8ca56020ca2ab8864db8194f44f1；
run143452Z显式RC5通过，manifest SHA为
864b7e768c694193b646a5ed1c277c9b370b1a7654514e4f41166da962ea013a，原报告SHA为
706f3b00d5b7447d3825bf7a2f7c7e55f7f20c28b530ce6a83f34b77b57bf7bf。
同一RC5 manifest不传显式参数按预期拒绝，不能由它自行授权RC5。

| 文件 | 修改前SHA256 | 修改后SHA256 |
| --- | --- | --- |
| runtime_economy_1019.py | 30029df9c21d4a851c9f02a473cc40d8e7fee3cfbd69df10290b9451402d2e2c | d5f6a21fd2408779ae7b6494bacb21d83e5cb3245644af1c69673006749d56f0 |
| test_runtime_economy_1019.py | 6ed60f9388f4811fb37a352d15304b22141b4b039fe0774c0e64100b751ce5bd | 359357906bae117088103f017ac4a2b1e38204239a236d314d841c55dc975e57 |

root在真实新游戏Jan1原生anchor完成后，令`$anchorReceipt`为该原始receipt路径，
执行以下完整CLI（不使用当前旧档迁移的r5pautoload或r5preload1）：

```powershell
python eat_everything_origin/tools/runtime_economy_1019.py --anchor-receipt $anchorReceipt --prefix r5mc --government machine --expected-tree 1cc8b77c28f3d59b0d840982c7f039a209cb66f3e26d9c3280ad2dfa0f9dbd52 --expected-version 0.4.0-rc.5 --dry-run
```

实际采集由root将末尾改为`--execute`；Hive／Purifier分别显式改government与
独立prefix，必要时加已观察到的`--autosave-dir`。本任务没有新Jan1anchor或真实
经济采集结果，不把包来源适配、离线测试或只读package通过写成经济实机PASS。

最终适配报告为 [economy-explicit-binding-rc5-v1.json](evidence/1019-analysis/economy-explicit-binding-rc5-v1.json)，
SHA256为3f0457863be2cabed4e96756e72b777df6da00d3871435f57e607f8c1fdc7994。
RC5因母舰旧档二次载入缺陷将被后续候选替代；这里的RC5正例只证明显式来源绑定
能力，不宣称Mod通过。后续RC6使用其实际新tree/version显式参数，不能沿用RC5期望。
