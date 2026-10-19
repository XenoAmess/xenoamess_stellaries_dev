# 原生议程进度修复与发布归因合同的只读评估

## 目标、范围与验证方法

2026-10-20主线程授权只读判断：成长checker跨月将整个government raw作为政体不变量，导致自然council_agenda_progress增加被误判；预定修复只把government直层scalar议程进度单列时间观察，其余字段仍严格，同日repeat/reload原raw仍严格，numeric／HP／四源模型／collector均不改。检查发布组件归因门禁是否硬绑定旧a66工具或矩阵字段，从而需要同步。本文不改gate、checker、测试、旧FAIL报告、生产、媒体或运行中的collector，不执行UI／Steam／Git写操作。

读取`publish_1019.validate_component_attribution`和已有发布夹具，逐项核对消费者字段。必要时复用现有临时合成guard夹具做少量内存兼容探针，验证新工具指纹／独立时间观察可保留，FAIL与不完整checks仍被拒绝；不生成native证据、不写最终索引、不重复完整54项测试。调查及探针结论仅为发布接口兼容性，不认证修复后的checker或本轮成长矩阵通过。

## 只读结论

**无需同步修改当前publish组件归因代码。** `publish_1019.py`被评估字节SHA为`50185608b9bb0bc60a57ce8bb10717c388c52119c2619fb9ef75114fbc5558f6`。

`validate_component_attribution`没有读取成长报告的`tool_sha256`，没有硬绑定旧`check_growth_1019.py` a66工具SHA，也没有固定`stable government`行名、check数量或government raw结构。这里的四个`source_models_sha256`是v1～v4预声明生产公式／RNG源码模型，不是checker SHA；只修跨月government比较不需要更换模型或生产tree。

| 消费字段／行为 | 本次修复的影响 |
| --- | --- |
| schema=`eep.six-core-growth-report.v1`、source_separated_native_rng_v1、顶层PASS_SCOPED | 保持；原FAIL不会因议程说明自动被接受。 |
| RC6精确tree、case中run_id、四模型tuple、C0实际截距 | 保持严格；不能把其它tree或拟合系数混入。 |
| matrix／repeat／reload／budget／ordinary_controls | 每组仍必须PASS_SCOPED、非空checks、每行passed为真正bool True；新修复必须保留这些结构。 |
| matrix的稳定政体行名／actual／expected内容 | 发布端不固定其名字或raw结构；按修复后的独立checker生成严格非议程字段比较即可。 |
| 新增议程时间观察 | 独立report／matrix附加字段可兼容。不能直接把不带passed的观察对象塞入matrix.checks，否则发布门禁按“不完整check”拒绝。 |
| numeric rows／HP | 原固定0.01与预声明HP ULP政策、raw delta重算仍检查；议程变化不能借该修复扩大数值预算。 |
| 六种非零真实tier、普通舰负对照、18个不同native SAV与phase | 保持；单个C0／C9 pair观察不是完整归因报告。 |

旧checker `business()`把government raw保留在同日重复／重载比较中；主线程要求该范围不改。只将跨月直层scalar议程进度分离，不等于忽略government任意其他字段、同名嵌套值、缺项、重复或非数值形状。这些修复边界由checker自身定向测试证明，发布端不以新增豁免重写判断。

原a66工具与原始FAIL继续原字节保留。未来修复后的报告必须采用新文件名、新`tool_sha256`及对应source snapshot／receipt解释；不能修改旧报告passed、status或原raw来“恢复通过”。最终case.analysis引用新报告真实SHA，原FAIL可留archives；门禁仍因旧FAIL的顶层／matrix status或false check拒绝它。修复工具测试完成前，正式成长验收继续等待；collector原始样本可继续按主线程授权采集。

## 合成接口探针结果

使用既有`testing/test_publish_1019.py`中的`Release1019Guards`／`implemented_components`夹具，仅在系统临时目录建立显式synthetic bytes与报告；直接调用现有`validate_component_attribution`。未写项目evidence结果或原生存档，退出时清理临时夹具。

| 探针 | 实际结果 |
| --- | --- |
| tool_sha256改为另一合成SHA | 接受，证明没有a66 pin |
| 添加独立agenda_time_observations | 接受，证明扩展观察字段兼容 |
| 政体strict行更名并保留passed=true | 接受，证明消费者不固定raw结构或名字 |
| 顶层原FAIL | 拒绝 |
| matrix原FAIL | 拒绝 |
| 政体／任意matrix check.passed=false | 拒绝 |
| 把无passed的时间观察塞matrix.checks | 拒绝 |
| 四source model改为未知值 | 拒绝 |

8／8实际结果与预期相符，约1.5秒；这是消费者接口验证，不是native PASS。探针后发布工具SHA仍为50185608…，未改任何发布／成长代码、测试、旧报告或已封口媒体。没有重新运行整个54项套件，也没有执行Steam／UI／生产／Git操作。
