# Growth跨月政体身份比较修复

## 目标与范围（实施前）

独立原生C0／C9 refresh→final pair只有government原始整块跨月相等检查失败，
其中直层`council_agenda_progress`分别6750.75→6808.5、6866.25→6924；实际
government/type/authority/civics/origin与其它字段、成长计数和属性均未变。
这是本仓库`tools/check_growth_1019.py`矩阵报告的比较模型缺陷，不是Mod或
open_kaishek问题；原生collector继续运行，不修改其输入或source模型拟合观察值。

只修改该工具及对应`test_check_growth_1019.py`，新增本记录与不可变证据。
不修改生产Mod、HP／modifier容限、计数／槽位、四版source模型、collector、
其它报告、UI或Git。主线程统一提交。本次规则只适用于矩阵跨日期政体身份，
同日repeat／reload的business snapshot继续逐字比较government原raw。

## 设计

先确认当前工具SHA为
`a66a949b3d967eb3a8739568ed2e53d8400fb244d86e3ced245c25f2db60e29b`，
原字节保存到`docs/evidence/1020-growth-government-identity/old-tool/check_growth_1019.py`，
新目录设置`-text`并索引SHA。原C0／C9 FAIL报告只读绑定，不改写：

- `docs/evidence/1019-analysis/rc6-growth-pair-n00-c0-observation-v1.json`，SHA
  `8073d947e1901ab28a21f0c9d49944656c7455864ef72c2b820114bd535a6021`。
- `docs/evidence/1019-analysis/rc6-growth-pair-n01-c9-observation-v1.json`，SHA
  `66f0e65be8e9ac8adcfc314155180f7f31e480f4fb05f5e58671ebfcb86ec3e2`。

使用现有原生直接字段解析器保留字段顺序、名字、object标志与各body原值。
仅将唯一、直层、有限数字scalar `council_agenda_progress`分离为时间观察；
重复、object、非数字或非有限值必须拒绝。未出现时记录absent，不捏造0。
其它已知或未知字段全部保留；嵌套同名字段不递归剥除。报告继续输出两端
government原raw、结构身份、直层进度原值与差异，且不能把同日进度改变豁免。

## 验收标准

- 跨日期只有直层有限progress变化通过；真实政体、authority、civics、origin、
  其它scalar／object／嵌套同名progress变化失败；重复／object／NaN／Inf拒绝。
- 同日repeat／reload只有progress变化仍失败，原始business函数语义不变。
- 有意义正反单元测试及原growth checker与collector离线测试通过；四source模型
  SHA、HP容限和其它函数源码保持原值。
- 在固定pair的原FAIL raw基础上仅追加补证，保留旧失败和旧工具SHA；只声明
  government身份检查的受限结果，不把未完成18节点／repeat／reload当总PASS。
- 报告新旧tool SHA、测试与固定原生pair结果给root及独立observer；由root在
  修复通过后继续真正验收。不得覆写历史报告或读取仍在写入的采样状态。

## 实施与验证结果

新增`government_identity`与`matrix_government_comparison`两个小函数，矩阵的
`stable government`检查使用结构身份；输出独立`government_observations`、
`government_comparisons`与合同
`cross_date_direct_finite_agenda_progress_observation_v1`。观察数据没有塞入
`matrix.checks`，其中原始raw、unified diff和进度变化均可复核。同日期矩阵
比较仍选原raw；repeat／reload的business／comparison函数也完全没有修改。

源码逐函数对照旧工具：20个其它既有函数逐字相同，仅`report`接入新检查与
观察输出；全部模块赋值AST完全相同，四source模型、公式、容限、counts／
slots、collector入口与导入行为保持。新工具SHA256为
`0c31f76491c39aff56fb054088d2a8fa4b592eb7f0ad186c5f1ec0c6625832bd`，测试文件为
`7f45879fb95979e9ca2a8cc86b2343bf9c80bd59efa2f03cbe096ac0a3c42f57`。

在`eat_everything_origin/tools`运行
`python -m unittest test_check_growth_1019 test_runtime_growth_1019`，41 tests全部
通过。正反例覆盖直层progress单独跨月、实际type／authority／civics／origin、
未知scalar／object、嵌套同名进度、重复未知字段保留、重复／object／NaN／Inf／
溢出进度拒绝，以及同日矩阵、repeat、reload的progress改变仍FAIL。

固定原生C0／C9仅从原FAIL中已经绑定的government raw追加
[受限补证](evidence/1020-growth-government-identity/fixed-native-pairs-supplement-v1.json)，
SHA为`9a4e721f22a32a7785df6dab64cb39bf9c323412e771b2c89989c7b4e2cd947f`。
C0为6750.75→6808.5，C9为6866.25→6924，均+57.75；两pair及其原失败的跨月
基线比较结构身份均通过，其余原检查值未改写。原FAIL报告和a66工具字节SHA
再次匹配；未重读SAV，也没有将这两pair改称完整growth验收通过。

[修复验证记录](evidence/1020-growth-government-identity/verification-v1.json) SHA为
`515af446e9634ef036773a11ab8bf3961e77b28c5d37d2333c77ed6e8d45ba6c`；记录上述
源码范围、测试命令与旧新工具／补证引用。root与growth_components已获新旧SHA，
observer可以继续固定原a66快照独立保留旧FAIL；root在完整原生采样后再执行
正式18节点及repeat／reload／budget报告。此修复不产生UI或全Mod PASS。

root随后在正确`tools`目录独立运行`test_check_growth_1019.py`，29 tests／3.853s
通过；其先前在`testing`目录误discover得到的0 tests没有作为PASS。本线程41项
为29个checker与12个collector测试合计。旧快照import产生的Python字节缓存不属
证据；交接名单仅含明确列出的源码、JSON与文档，observer后续禁写bytecode。

主线程提交检查发现新增测试调用行末多余空格，将仅清除此格式问题；参数、逻辑、
检查器及验收政策不变，不为纯格式重复运行测试。原交付测试源码 SHA 仍描述原先
实际执行版本，验证记录不回写；清理后的源码由后续 Git 提交记录。
