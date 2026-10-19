# RC7迁移v2待执行case准备

## 目标与范围（生成前）

按主线程指定的固定run `20261019T164112Z` 和既有[执行清单](rc7-migration-restart-execution-1020.md)，提前生成public031/paid11两个独立CLI原始模板及对应待执行case、精确角色表，减少实机分支切换时的填写工作。本轮仅新建文档和独立准备包`docs/evidence/1020-rc7-migration-prepared-cases-v1/`，不改原清单、旧包、工具、Mod或引擎验收工具，不操作UI/Steam/Git，不读取活动r7pk或日志。

固定candidate tree为`61b34f6dbdc277c44364889d5f1e1cd2773a4624786bbf0d538079fc6ba4feb0`。CLI template必须显式传该值，不能使用默认RC6。只运行`template`，不执行`check`，不生成实机验收PASS。

## 设计

先让原`check_migration_1019.py`以CLI独占创建两个PENDING模板，保留其原字节和SHA。再各复制为新prepared case：只把已指定的未来路径按既有清单填入空字段，status明确`PREPARED_NOT_EXECUTED`；原fixture/旧before、身份、预算、EXE和candidate tree字段不变。这些路径是将执行的计划，不能视为已发生的SAV/load。

新role-map逐项列出六SAV角色、各自audit/native-save及实际load/helper动作的计划路径。旧fixture/before可核已封存来源，保留其真实SHA；所有未来角色的SAV/audit/native-save/load/action SHA一律`null`，状态`TODO_NOT_OBSERVED`。不扫描这些未来路径以“发现”实机结果，不用同SHA其它文件替代角色。

public计划`after=r7pautoload`、`reload=r7preload`、`repeat_before=r7prepeatbase`、`repeat_after=r7prepeat`，第三次load来源仍`after`，保留174项原checkset。paid计划`after=r7paidauto`、`reload=repeat_before=r7paidreload`、`repeat_after=r7paidrepeat`，无第三次load，保留158项原checkset。

模板、prepared case及role-map都只是准备材料。真实测试完成后另建complete-case/report，把实际存在的原生输出及精确回执绑定进去；不能把这些准备材料的状态直接提升为PASS。原v2每步固定预算与嵌套v1 FAIL、mobilebase限制不变。

## 验收标准

- 两次CLI template均退出0，输出仍PENDING、未来字段全null、精确RC7树与固定旧source绑定正确。
- prepared case仅改变status及八个未来路径/额外load字段，public/paid路径严格按既有清单，原固定字段及政策逐项不变。
- role-map只核旧source/已封存材料，不读取未来原生文件；全部未来SHA为null，没有生成check报告或PASS字段。
- 输出文件独占创建、记录CLI命令/返回值、工具/源证书/模板/准备case/角色表完整指纹。封口后不改写，后续实机接收另建文件。

## 生成命令

从仓库根执行，生成器为现有CLI，没有新工具代码：

```powershell
.venv/Scripts/python.exe -B eat_everything_origin/tools/check_migration_1019.py --output eat_everything_origin/docs/evidence/1020-rc7-migration-prepared-cases-v1/public031.template.json template public031 --candidate-tree 61b34f6dbdc277c44364889d5f1e1cd2773a4624786bbf0d538079fc6ba4feb0
.venv/Scripts/python.exe -B eat_everything_origin/tools/check_migration_1019.py --output eat_everything_origin/docs/evidence/1020-rc7-migration-prepared-cases-v1/paid11.template.json template paid11 --candidate-tree 61b34f6dbdc277c44364889d5f1e1cd2773a4624786bbf0d538079fc6ba4feb0
```

prepared case分别名为`public031.prepared-case.json`和`paid11.prepared-case.json`；后续实际完成后应另建`docs/evidence/1019-analysis/rc7-<kind>-migration-v2-complete-case-v1.json`并运行原执行清单中的check命令。运行前须先由主线程明确各阶段已完成且文件稳定。

## 准备结果

两次原CLI template均实际退出0，输出PENDING。已新建两份`PREPARED_NOT_EXECUTED`case及六角色表；public四个新SAV、paid三个新SAV的计划名称与原清单一致，paid的repeat_before按计划复用reload。所有31项未来文件引用的SHA均为null，未读取这些路径。旧source角色只从已封口输入清单读取并独立核其原字节SHA。

准备包另存`cli-template-receipt-v1.json`与`verification-v1.json`，记录原命令输出、固定工具/证书身份及各新文件指纹。这里的校验只确认准备材料一致，没有运行check、读取未来实机样本或改变任何旧结果。
