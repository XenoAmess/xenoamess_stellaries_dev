# RC7发布门禁精确来源适配（PENDING实机）

## 目标、范围与设计

2026-10-20主线程授权最小更新`publish_1019.py`及对应测试：组件最终树固定为真实RC7 `61b34f6dbdc277c44364889d5f1e1cd2773a4624786bbf0d538079fc6ba4feb0`，模型链在原四项后追加已封存v5 SHA `b761caa8b5e31cd2981588cc307e9d1da8840b69a4d3ab403454cd3a197c6f28`。v1～v4原件及其prefix历史保持，不将RC6 FAIL或旧来源改写为RC7通过。不增加跨树source bridge，不改变18组／EXE／语言／单Mod／数值／HP／原生SAV或归因判据。

源依据为`docs/evidence/1019-rc7-static/`真实59文件包、原gate／report，以及不可变v5。最终索引仍要求全部run／case／static同一RC7精确tree；旧RC6输入仅可作为已标明的fixture／baseline／历史参考。新模型或源码证书不等于RC7 runtime通过。

迁移身份适配由kaishek维护独立checker；待其稳定报告接口及新工具SHA交付后，发布端同步精确已知RC7版本／树及新checker pin。主线程已明确允许必要的`proof.version=0.4.0-rc.7`等适配，并要求RC6历史报告仍可审计；只能支持明确审阅的RC6／RC7源分支，不能放宽任意版本或tree。旧scope/report原字节不变，历史验证路径与最终RC7索引接受严格区分。

## 验收标准（实施前）

- 精确常量与v5／RC7完整静态归档实际指纹相同；前四模型SHA仍与原不可变证书一致。
- 拒绝RC6树／旧模型链混入最终RC7、缺失或未知v5、未知tree及实际生产字节变动；不能只相信手填tree。
- 既有数值／HP／六种非零RNG／18原生phase／普通舰控制和18组／metadata-only正式化测试保持。
- 迁移新source role的每个manifest／tree／版本必须实际RC7，原v1 FAIL及独立v2预算不变；历史RC6仅在明确历史分支验证。未知revision、错误producer工具SHA或混合role必须失败。
- 只写被授权发布工具／测试／本文，不改checker、生产、metadata、媒体、UI、Steam或Git写操作。全部RC7实机状态仍PENDING。

## 组件来源阶段验证

已只追加v5并将最终组件tree改为61b34…，没有改数值或归因函数。对应定向测试3／3通过（7.309s）：证书／历史prefix匹配，拒绝RC6或未知最终tree及实际源码改动，拒绝缺失／未知v5与其它模型。growth工具保留历史RC6 SOURCE_TREE默认；publish按最终RC7 SOURCE_REVISIONS条目查证，不改其历史含义。

对真实`1019-rc7-static/candidate-rc7-open-kaishek.json`执行现有`validate_static_report`通过；用`build_pending_index`只在内存盘点当前实际源，得到0.4.0-rc.7／59文件正确树／五模型／18组全PENDING，没有写progress或final-result。此检查只证明静态合同与来源绑定，不证明RC7成长、预算或任何实机case完成。

## 迁移精确身份适配设计（实施前）

kaishek交付新producer SHA `8a8cf5a52d0c4dfbdfeaa0506a0d8728539d80ca72b56ab875b081a94b8ee0aa`，工具TREE／template历史默认保留RC6，新增RC7_TREE及精确两版SOURCE_REVISIONS；validate_case仍返回原fixture字典。174／158检查键、数值／比较函数及policy不变，旧键fixed_rc6_tree／version只是兼容名称，实际expected来自case明确revision。

发布端据此使用独立固定RC6→rc.6／RC7→rc.7映射，不假定migration.TREE已改。当前执行的checker字节必须等于新producer pin；scope.checker及report.checker_sha256则绑定实际生产该报告的工具：新producer可针对两版，旧08b579…只允许历史RC6。原报告／case／旧checker原字节保留，不在RC7 finalcase里接受混合角色。

新producer还必须有typed scope.source_certificate analysis引用，SHA固定`29742bf394cf83d0b1fd3b9f8221bf06f0c359b40668afea30e3aaa82a946046`，实际文件位于`docs/evidence/1020-migration-rc7-source/source-certificate-v1.json`。报告及四个candidate原生角色（after／reload／repeat_before／repeat_after）的candidate_source_identity均须精确含对应已知tree／version／完整59文件表／共享design和layout helper／证书SHA；不从SAV hash反查其它role，也不接受少字段或改一个文件。fixture／before保留真实旧版本，不强制它们成为RC7。

最终18组仍由同一个RC7候选、static及run表约束；独立历史RC6迁移validator可审计旧报告，并不产生跨tree最终验收例外。正反测试须覆盖旧08b报告保留FAIL、明确新producer的RC6／RC7分支、RC7混入rc.6 role／manifest、旧producer冒充RC7、新工具或证书pin错误、59文件表未知字节／缺失／混合、未知revision，以及原预算／raw Decimal／队列／EXE约束不变。

## 实施结果与验收

已完成最小来源适配：组件最终tree为精确RC7／模型五链；迁移以固定两版tree→version映射区分历史和本轮来源，运行中的checker固定8a8cf5…，旧08b producer仅限历史RC6。新producer除原174／158全量检查外还须完整source identity／证书绑定。没有改数值比较、HP政策、component归因、其它case检查或exacttree总门禁。

2026-10-20执行：

- `python -m unittest discover -s eat_everything_origin/testing -p test_publish_1019.py -v`：**58 tests PASS**，66.836s。其中9项迁移门禁测试覆盖旧报告形状、新producer两版形状、旧版本role／repeat混入、完整59文件缺失／变动、bool计数、错误证书／producer，以及原v1 FAIL／Decimal预算等。
- `python -m unittest discover -s eat_everything_origin/testing -p test_runtime_index_1019.py -v`：**8 tests PASS**，3.616s。helper仍不能接受case、覆盖最终索引或改冻结来源。
- 另对真正RC6原typed scope做一次**仅内存**历史复核：把其指向已变化工作区工具的旧checker引用，换成已归档的同SHA 08b原字节路径后，现validator通过；原case仍PENDING、damage_preserved仍false。原scope／report／checker归档文件未被改写，未生成新runtime结论。

测试中RC7 report形状使用临时目录明确标注的synthetic字节，不是RC7原生存档或真实迁移成功证据。现有真实RC7 static report及source清单可通过来源校验；**RC7全部实机case仍PENDING，本文不建立final-result**。

封口工具SHA256：`tools/publish_1019.py`=`06c60c0a9bd406580314999ae6649365bb5c1fa6c7152c0b0a7fb5a420e06918`；`testing/test_publish_1019.py`=`19302251d7bc6e8b67d0663a767e1298aa73680c596d505eb25155474f80f7b8`。依赖checker8a／证书2974由kaishek独立交付，未在本任务修改。最终18组最小输入／helper命令和迁移typed字段详见`rc7-final-index-closeout-20261020.md`。

本轮未操作UI／Steam／Git，未改生产源、版本、正式CHANGELOG、descriptor、已封口媒体或任何旧证据文件。
