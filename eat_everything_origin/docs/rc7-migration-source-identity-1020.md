# RC7迁移v2报告的精确源身份扩展

## 目标与范围（实施前）

RC7完整Mod树为61b34f6dbdc277c44364889d5f1e1cd2773a4624786bbf0d538079fc6ba4feb0，
canonical完整59源位于`docs/evidence/1019-rc7-static/candidate-rc7/mod`，VERSION、
gate／report与source-index均已封存。只扩展`tools/check_migration_1019.py`对这一
确切源版本的识别，保留原RC6历史链及默认语义，不从manifest或自报树放宽规则。

仅改该checker、对应testing测试、本文与新source certificate。不得修改v2损伤
预算、defense／ratio_step／context／layout／receipt／repeat比较、政策、旧fixture、
历史报告、v1旧checker、publish或其它工具、生产Mod、UI或Git。root负责后续真实
public031与paid11在RC7的load／reload／repeat；离线正例只证明源绑定支持。

## 设计

先冻结现有checker原字节并记录SHA。核RC6／RC7完整59索引，RC7差异应严格限于
descriptor版本和母舰while增加literal count200；设计文件与迁移guard helper如果
字节相同则复用原绑定，差异单列，不改公式拟合新数据。新证书绑定完整两版清单
及RC7源归档、设计／guard helper的原SHA，并由checker固定证书SHA。

按显式case的candidate_tree选择已注册源revision。RC6保持原版本约束；RC7必须
精确版本、全59实际源清单／字节与源树一致，设计来源与实际观察manifest相连。
未知树、已知树下变异源、缺文件／重复索引、RC6／RC7包互换或错误版本都拒绝。
不把新包自报manifest当独立真值；source certificate本身不得由输入指定。

## 验收标准

- 原有离线v2测试保持通过，新增确切RC7全源正例、未知树／变异／来源互换负例。
- 源证书由原冻结RC6与RC7字节推导，非身份函数源码与全部政策／fixture常量
  精确保持；旧报告与旧工具原字节保留。
- 实际candidate-rc7完整包离线源绑定通过，RC6完整历史源仍可检查；不读取新run
  的未完成SAV，不产生任何实机迁移PASS。
- 新checker完整SHA交release_pipeline更新其exactpin，不修改publish文件。

## 源证书与接口结果

原checker完整SHA为`08b57969060c037c4e03829f0075f8e7314f262527215e991595bd4778456d38`，
原字节保存于`evidence/1020-migration-rc7-source/old-tool/check_migration_1019.py`。
[源证书](evidence/1020-migration-rc7-source/source-certificate-v1.json) SHA为
`29742bf394cf83d0b1fd3b9f8221bf06f0c359b40668afea30e3aaa82a946046`，在checker中
固定，不允许case指定替代证书或注册任意新树。它完整列出RC6与RC7各59文件。
两版唯一差异为descriptor的rc.6→rc.7版本字节，以及母舰effect新增唯一literal
count200行；去掉该行后effect整文件精确等于RC6。设计文件SHA仍为
`0e1bc46c7d1d534e0a9d3619cef1d93e366ddc7d5a4d2fde766b0ca111929123`，
`eep_repair_existing_mothership_design` helper body SHA仍为
`433730ede08b00c45f656b14657e230e5e3bf80f4b64ea920151d00ead50da14`，均复用原来源。

`TREE`与`template(kind)`默认仍为历史RC6；新常量`RC7_TREE`及`SOURCE_REVISIONS`
只登记这两个精确树／版本。`validate_case`仍返回原FIXTURES的known dict。
新包需显式生成模板：

```powershell
python -B eat_everything_origin/tools/check_migration_1019.py --output <新的case.json> template public031 --candidate-tree 61b34f6dbdc277c44364889d5f1e1cd2773a4624786bbf0d538079fc6ba4feb0
```

paid模板将`public031`换成`paid11`。仍是PENDING，须由root填真实新after／reload／
repeat和各load回执。不能把原RC6报告改标签当RC7结果。

`load_native`对已登记候选源调用完整源校验：实际copied_mod全部59文件、tree、
manifest完整清单、static gate完整清单／版本／tree及原report SHA须相符；另核
设计和guard helper原SHA。`evaluate`按case显式指定revision核对actual身份，RC6／
RC7来源互换拒绝，不从manifest自行选择更宽政策。历史序列化键
`fixed_rc6_tree`／`fixed_rc6_version`保留名称以保持174／158 checkset兼容，它们对
RC7使用明确RC7 expected值，不能从旧键名推断报告实际revision。

checks外新增`candidate_source_identity`，且每份candidate的native proof包含同名
字段：schema=`eep.migration.candidate_source_identity.v1`、tree_sha256、version、
file_count59、files完整59条path／bytes／sha256、copied_mod真实路径、
source_certificate的path／固定SHA，以及shared_migration_sources设计／helper。
release_pipeline可按证书全表绑定来源，不需要改变检查数量或数值政策。

## 验证与封口

新checker SHA为`8a8cf5a52d0c4dfbdfeaa0506a0d8728539d80ca72b56ab875b081a94b8ee0aa`。
执行`python -B -m unittest discover -s eat_everything_origin/testing -p '*migration*.py' -q`，
41 tests／2.603s全部通过，包括旧17项队列迁移契约。新增负例覆盖unknown tree、
selected／unselected源变异且自改manifest、两已知源包互换、缺文件／重复索引、
错版本、改证书／原静态report SHA、伪源身份和同名历史默认保持；CLI显式RC7
模板也独立调用成功。离线合成结果的RC6与RC7检查键和值集合一致，原v1 FAIL
保持，不冒充真实新迁移通过。

11个原数值／比较／读取helper函数源码逐字相同，全部原模块赋值AST相同；对
evaluate只剥除源检查新增expected参数、范围文案与新身份输出字段后，AST与旧
函数完全一致。真实run150008Z及164112Z的manifest／copied完整59源均独立绑定
通过；本任务没有读取新run未完成SAV。原公开完整／paid CLI报告原SHA仍匹配。
详细记录在[验证记录](evidence/1020-migration-rc7-source/verification-v1.json)。

新tool SHA与精确identity schema已交release_pipeline，由该线程同步publish的
producer pin及已知树→版本判断，本线程未改publish。源码、测试、证书与本文
至此封口，root统一提交；RC7真实public／paid load／reload／repeat仍须实际重跑。
