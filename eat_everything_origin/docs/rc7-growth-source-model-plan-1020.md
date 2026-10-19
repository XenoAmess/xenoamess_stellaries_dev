# RC7六核心源模型与成长采集时序

## 目标与范围

RC6的原始18样本和独立观察全部保留。C10000首次矩阵中七项存储导出真实失败，随后主线程同日重新导出与v4相符；C20500单次同步主线程实际记录R300/P110，未达到事前要求R400/P10。后两项在本文件中仅作为主线程已报告的运行事实，不冒充本代理独立重新解析的结果。原版while契约、显式count实例及EXE字符串来源见既有 [原生来源归档](evidence/1020-native-while-primary-evidence-v1.json)，缓存反推边界见 [独立诊断](evidence/1019-analysis/rc6-growth-c10000-cache-while-diagnosis-v1.json)。

本轮只新增不可变 `six-core-source-expectations-v5.json`，在主线程给出RC7冻结目录与确切59文件树之后生成；不得预填未知树或继承RC6运行通过。保持v1–v4原字节、所有源系数、实际C0截距方法及数值容差不变。生产修复由其他代理负责：仅在随机发放while中显式指定literal `count = 200`；本代理不改生产、collector、UI、版本或Git。

获得单独授权后，冻结模型完成再仅给 `check_growth_1019.py` 的MODEL_HASHES追加v5 SHA、给SOURCE_REVISIONS追加确切RC7树映射 `(5, "frozen_rc7")`。原v1–v4绑定与旧tree映射保留；不改其他函数、government比较、属性预测、HP余量或采集器。定向回归限现有检查与新RC7身份拒绝，不能把新tree加入当作运行通过。

## 源证明设计

1. 逐byte核v1–v4 SHA，与v4记录的全部RC6 59文件相符的不可变候选作前件；不得用当前工作树重建旧源。
2. 对主线程指定的RC7不可变候选生成按相对路径排序的全部59文件清单，每项记录路径、byte数、SHA256；按现有runtime树清单算法独立重算tree，与主线程冻结tree完全相等才生成v5。
3. 比较RC6与RC7完整路径集合和逐文件字节。预期允许的差异只为 `common/scripted_effects/eep_mothership_effects.txt` 新增唯一literalcount200及 `descriptor.mod` 的rc.6→rc.7版本值。出现其他差异先报告，不自动扩大等价范围。
4. 六组件模板、script values、固定设计、section和static modifiers必须完整字节相同。成长L/B/next计算、母舰存在/归属/唯一性和布局修复guard、持久tier只初始化缺值、country镜像、待发计算及月度调用必须保持。
5. 不声称整个组件发放函数原字节相等。记录其前后SHA、唯一插入字节及精确位置；从新文件仅删除已确认的唯一count行后，必须与旧完整文件逐byte相同。另分别绑定等权六项random_list、每奖R+1/预算−1以及200工作预算的原字节；显式count提高单次原生循环预算属于有意运行行为修复。
6. 将v4的retained_v1_expectations、retained_v2_expectations、hp_policy_unchanged原结构直接保留，并记录这些子树规范序列化SHA相同；不是根据RC7运行结果重新推导。v5状态只能SOURCE_ONLY/运行待验，不读取未来RC7成长数据。

## collector高成长时序审阅

既有collector的每节点顺序是同日setC+同步一次、独立FF30产生refresh原生autosave，再导出十modifier和maxH/maxA trigger，随后独立FF30产生final原生autosave。原代码无需为了掩盖RC6失败而延长等待或改导出位置。

在新literalcount200确实生效的前提下，C200节点已R4，C10000应得B200，首次同步只需196次独立抽取，小于200；同一次调用应使R200/P0，六tier此后不再变化。随后的第一个30天已超过本机定义的5日triggered modifier更新间隔；下一个月度同步没有新应得奖励，因此不会在导出当日再把R104补成200。由此预期原18样本矩阵的C10000 final存储导出可与其同一实际六tier对应，不需修改collector。此处是修复后的源推论，必须由新RC7 refresh计数/实际属性/export证据验证，不提前记PASS。

源中count与现有limit共同约束循环：达到B或200工作预算时终止，不为凑满200额外发奖；九节点任一中间节点的所需补发量均不超过200。C20500补差另测：C10000/R200→同日一次sync应只补200至R400/P10；下一月原生回调应补10至R410/P0。该预算路径同时验证显式count实际覆盖默认上限及monthly调度，不能只以九节点最终R200代替。

## 验收标准与停止条件

- v1–v4 SHA精确不变；v5独占新建，不覆盖历史模型或失败报告。
- RC7全部59文件与冻结tree精确绑定；唯一生产语义差异为显式while count200，版本差异单列。
- 六属性源系数、C0截距方法与HP `max(.01,8*ULP32(expected))`/rel0、十modifierabs.01/rel0、账本和身份精确比较均不变。
- checker仅追加两个常量映射；现有29项检查通过，并覆盖RC7未知tree、完整文件变更和证书变更拒绝。
- 尚未冻结/未知差异/模型前件改变时停止生成并报告。静态验收、原生成长矩阵、同日重复、原生reload和20500自动补差全部需新证据，不从本证书继承。

## 冻结后实施与离线验证结果

主线程提供RC7冻结目录 `C:/Users/1/AppData/Local/xenoamess_stellaries_dev/artifacts/1019-implementation/candidate-rc7/mod` 后，独立重算完整59文件树为 `61b34f6dbdc277c44364889d5f1e1cd2773a4624786bbf0d538079fc6ba4feb0`，与指定值一致。全部RC6旧文件先与v4逐项精确核对；RC7只有两个完整文件变化：mothership effects（SHA `f704c30ea845d57dbad5bcb6c60ec657d5ae8d4ab6a55082055dccb38d7d5ec1`）第36行新增唯一20字节 `        count = 200\n`，及descriptor版本字面rc.6→rc.7。移除新effects这唯一一行后，完整文件与冻结RC6逐byte相等，其他57文件原样。

[six-core-source-expectations-v5.json](evidence/1019-analysis/six-core-source-expectations-v5.json) 已独占新建，SHA256 `b761caa8b5e31cd2981588cc307e9d1da8840b69a4d3ab403454cd3a197c6f28`。其source_equivalence明确区分“删除唯一授权count行后的原字节等价”与实际RNG函数原字节不同；实际函数前后SHA和byte数另列，不用一个true冒充完整运行语义无变化。保留v4的v1/v2预测子树与HP政策原结构，另外记录规范序列化SHA；v1–v4原文件SHA均未改变。证书状态仅SOURCE_ONLY，创建时没有读取RC7成长SAV。

`check_growth_1019.py` 只追加MODEL_HASHES的v5 SHA和SOURCE_REVISIONS的确切RC7 `(5, "frozen_rc7")` 映射；旧SOURCE_TREE及全部前件绑定保留。将这两处新增常量反向移除后，完整checker字节SHA精确还原原 `0c31f76491c39aff56fb054088d2a8fa4b592eb7f0ad186c5f1ec0c6625832bd`，证明未更改函数、数值、government规则或其他实现。当前checker SHA `a8d70f1015b6f1f4026ae811c38653997fd41a55bbca9b9b8fba391fb4070bf5`。

定向测试 `python -X utf8 -B -m unittest test_check_growth_1019` 共31项通过：保留原29项（证书变更测试明确选最新revision，避免默认保留的RC6树漏查新v5），新增RC7五模型链/历史前缀及未知树拒绝、RC7所选与末项非所选源文件变更拒绝。测试文件SHA `56ca64dcc255ea6f091be9be37d6748b8a8a3d3b921b911e4d90a9d99a6ea0b2`。另调用既有 `validate_source_package` 对真实冻结RC7全部59项及原生来源SHA纯离线核对成功；未导入UI、未进行新运行测试，不能据此宣称Mod运行验收通过。
