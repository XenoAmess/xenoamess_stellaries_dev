# 无增长七分支经济预算补充审计

日期：2026-10-15。只读派生审计，等待run `20261015T113522Z` 的ecng七分支21档完整报告；不将旧自然增长21档纳入本轮通过结论。

## 目标与范围

保持冻结 `2bee9c8460e07a228d8d0f577aa8245792e2ecc936497c975e6bd422be0173a1` 主审计器、36项工具测试、116文件实验包及原生样本不变。主审计由architecture执行。本协作者仅从其完整JSON快照派生额外费用/收入检查，不操作GUI，不写sav、不写实验预期输出。

## 接口与来源方案

新增独占标准库工具 `tools/audit_additive_budget_supplement.py`，输入 `--matrix-report`、`--game`、`--report`。复用冻结主审计器的Decimal/固定epsilon与只读P数据解析，加载前核对其SHA；不修改或重跑既有36/43项测试。输出保留原报告SHA、主审计各状态、共同源/七支样本身份及原生预算路径。

准备阶段另用 `--prepare-sources --game ... --report ...`，与 `--matrix-report` 互斥；仅生成原版树及来源状态，不读取原生矩阵，状态为SOURCE_PREPARATION_ONLY。实际报告入口要求原manifest文件名为 `additive-no-growth-matrix-manifest.json` 且SHA匹配、原报告为原生读取、共同源和全部21档均来自run113522Z、21档名以ecng开头，并复核原sav字节数/SHA。冻结包如出现category覆盖文件则停止，不能假装仅原版树足够。

先只读本机4.5.2 `common/economic_categories/*.txt`，建立原版category→parent链，保存实际文件/行号/哈希及分类原文。重复定义、多parent、未知parent、循环、未知收入分类均不得自行解释。岗位收入须实际属于 `planet_jobs` 子树；station/building/deposit/country_base等以真实祖先链分类。位于岗位祖先的聚合类不能误当纯非岗位阴性。此原版树检查不证明未声明的额外Mod没有覆盖，实际包身份仍由主运行清单与G1交叉确认。

## 算法与验收标准

1. 输入必须含固定七支及input/warm/measured三阶段的完整compact快照、共同源与原主审计状态。所有派生观察使用measured的 `budget.last_month`。不从input变量或受控modifier反推预算输出，不填缺失行的0。
2. 对七支实际expenses的category/resource并集逐行比较；只有七支均有明确有限数字才可比较固定性。差异即FAIL；缺行/字段或来源不明为NOT COVERED。全零观测不能证明非零费用免疫；未出现的费用不声称通过。特别单列实际 `planet_pops` 子树人口维护及 `leader_officials`，无该行时明确未覆盖。
3. 对实际income并集逐行保留七支原值和祖先链。七支均明确存在且各支非零的行，以raw值计算 `Q0=(F10-F00)/0.4`、`Q1=(F11-F01)/0.4`，核两组B差=`0.35Q0`、FP/FN/FH相对F11差=`0.05Q0`及interaction=0。无需岗位基值或另设归一化，因为主合同已控制measured同日跨支就业；被测分类跨phase固定，其它岗位同phase跨支一致的原边界保留。
4. 岗位来源且正响应、上述差分通过，才登记本行有限+5%加算证据。Q≈0不得冒称岗位已验证+5%；已知非岗位、实际非零且七支固定可作有限阴性。来源不明、混合祖先或无法解释的响应保留NOT COVERED/FAIL及诊断，不推广至全部经济。
5. 保留原主审计状态。原INVALID/FAIL/NOT RUN/未覆盖不能由补充结果改成主合同PASS；派生算术可留诊断，验收资格须受原报告门禁。旧自然增长报告不允许混入新run。原报告未齐前只准备来源和开发算法，不执行新原生矩阵。
6. 开发验证使用显式内存JSON数据，覆盖遗漏费用行、费用漂移、未知分类/父链、错误独乘交互、Q0岗位及主状态失败保留；不产生或标作native存档。实现/检查脚本与派生JSON均归档自有programmatic子目录，结论链接可提交的实际文件。

补充的无增长前提还独立比较所有国内岗位语义签名跨21档固定；这比原主工具对非测量岗位只要求同phase跨支固定更严格，只用于本次明确冻结人口的ecng组，不回写旧自然增长结果。主状态与补充前提不满足时，派生数值只留诊断。新开发测试文件为 `tests/test_additive_budget_supplement.py`，只执行该新文件，避免重复36/43项。

## 当前状态

设计与原版来源准备中；ecng原生补充审计NOT RUN，待主任务/architecture通知完整新报告后执行。

开发首轮9项中新发现费用focus汇总的fallback误用：有正常非零PASS行仍被汇总为NOT COVERED。首轮回执保留为initial-failure，仅修本次新工具的空集合/非空集合fallback，再重跑这9项；未改原主工具、36/43项测试或原生数据。

## 首次真实报告与分类新事实（转换验证实施先行）

architecture通知原生报告READY后，先核SHA256=`c55fa0ff97453227153a2fb7bd9cba1ed572b8778769b16d16cebba47c926e42`、1521873字节，主合同limited/strict/setup均PASS，再运行本补充v1。首次真实报告为FAIL并保留原件：30项measured费用中29项固定，唯一变化为 `trade_policy.trade`；31项收入中29项满足原分类合同，trade_policy的energy/trade两项被错误套为独立非岗位阴性而失败。所有原始值保留，没有填0或删行。

原版 `common/economic_categories/00_common_categories.txt:1581` 将trade_policy定义为空根，只能证明它不是planet_jobs直接子类，**不能证明转换吞吐独立于上游岗位贸易**。实际 `common/policies/00_policies.txt:3660` 为该政策，default选项在3667，3675–3677明确 `set_trade_conversions` 的trade和energy系数各为0.5；该文件SHA256为 `3638e072772adf7e1987b9f065976cb3151544bd365c3504d5bf7664051f2042`。F00原始上游trade为岗位planet_civilians的40.86885加四个pop_category合计16.93，等于trade_policy费用57.79885；政策两项收入各28.89942，约为该吞吐一半。这是政策转换账，不是普通维护费减少或新增费用缺陷。

主任务授权新增独占 `tools/audit_additive_budget_conversion.py` 和新开发负例，v1工具及其首次真实FAIL报告不改。v2只将精确名为trade_policy、原版空根、当前三阶段/七支及共同源实际选default且已解析的默认转换表，归入独立derived-conversion验证；其它非岗位仍逐行不变性检查，不能泛化豁免。

转换合同：逐支从实际非trade_policy收入的trade行求和，保留岗位/非岗位分项；费用必须等于这份上游实际总量，输出必须分别等于从原版代码独立读出的0.5份额，并核份额总和和回账。再核岗位贸易raw Q的加算响应、转换输出Q与该实际岗位Q的0.5份额。缺行/来源不明/非default政策/未知输出键或额外trade消耗为NOT COVERED；算术错误、吞吐或份额不符为FAIL。普通29项费用不因转换类别变化被放宽；v2逐行列出保留的转换账和最终判定，且保留原主合同和v1状态。开发负例覆盖错误吞吐、错误份额、未知政策、缺转换行及普通费用差异不能被豁免。

## 最终执行与有限结论

v1新9项开发测试PASS，v2新7项开发测试PASS；未重跑原36/43项。v2测试首轮仅因Decimal的80和8E+1字符串形式不同而失败，改为数值比较后通过，首轮回执仍保留。v1和v2源码均独立保字节快照，原2bee主工具和116包未改。

实际执行：

```text
python -B -m unittest discover -s tests -p test_additive_budget_supplement.py -v
# exit 0：9项（0.063s）
python -B -m unittest discover -s tests -p test_additive_budget_conversion.py -v
# exit 0：7项（0.059s）
python -B tools/audit_additive_budget_conversion.py --matrix-report _runtime/shishan_code/20261015-runtime/runs/20261015T113522Z/additive-no-growth-native-audit.json --game "C:/Program Files (x86)/Steam/steamapps/common/Stellaris" --report shishan_code_origin/docs/evidence/feedback-redesign/remaining-2026-10-15/programmatic/additive-budget-supplement/native-budget-supplement-v2.json
# exit 0：PASS；原22份sav大小/SHA与主报告逐份一致，全岗位无增长检查无诊断
```

| 实际观测范围 | 结果 |
| --- | --- |
| 11项非零岗位收入 | raw Q加算全部PASS：消费品23.10；生物学社会学5.28、凝聚力1.10；官僚凝聚力3.96；平民贸易26.3670；工程学1.98；合金15.4；矿物40；物理学1.98；政治家凝聚力11；能量52.8。各自两组B差=.35Q，三个单键差=.05Q，interaction≈0。Q为实际预算响应，不是另设岗位基值。 |
| 18项非零独立非岗位收入 | country_base九资源、power_projection影响力、三项轨道矿藏/研究收入、四类人口贸易和starbase_modules能量均七支固定；未将政策转换收入当独立阴性。 |
| 29项普通费用 | 全部七支固定，包括planet_pops_traits能量60.467，四类人口消费品6.59175/2.2/8.25/3.85，leader_officials凝聚力8，以及实际出现的其它领袖、舰船、空间站、建筑/区划、岗位维护行；只覆盖这些实际非零行。 |
| 政策转换三行 | 一项trade费用与两项energy/trade收入单独核59项恒等式PASS。七支非岗位贸易均16.93；岗位贸易按架构增加，费用等于其和，两个输出各半，转换Q均13.1835=岗位贸易Q26.367×.5。保留原v1三条FAIL原观察，不改成普通费用PASS。 |
| 未覆盖 | 本次实际出现行的NOT COVERED数为0；未观测费用、外国经济、其它贸易政策、未出现的建筑收入及其它源/规模仍未覆盖，不能把0推广为全机制无未覆盖。旧自然增长21档的INVALID/P-W FAIL未纳入新PASS。 |

原v1 FAIL报告423481字节、SHA256 `2173086bb0dc8d3adddca78c659a06fd1213ec7875a3ed7681c42a20dd200241` 保持不变。v2报告454189字节、SHA256 `27203028d570c4d746983ead7ab8e2a72fa5d651a048f9cf905d4227842e7ee1`，保留主报告PASS状态、原v1 FAIL、全部三条政策原行和独立转换判定。结论是有限样本的岗位加算、已观测普通费用阴性与已确认政策转换正确，不能由此宣称独立乘算或全部经济路径已经验收。

必要证据均为仓库相对链接：[原v1 FAIL](evidence/feedback-redesign/remaining-2026-10-15/programmatic/additive-budget-supplement/native-budget-supplement.json)、[最终v2](evidence/feedback-redesign/remaining-2026-10-15/programmatic/additive-budget-supplement/native-budget-supplement-v2.json)、[实际命令回执](evidence/feedback-redesign/remaining-2026-10-15/programmatic/additive-budget-supplement/native-budget-supplement-v2-command.json)、[精确统计及七支原值](evidence/feedback-redesign/remaining-2026-10-15/programmatic/additive-budget-supplement/final-budget-summary.json)、[9项开发测试](evidence/feedback-redesign/remaining-2026-10-15/programmatic/additive-budget-supplement/development-tests.json)、[7项转换负例](evidence/feedback-redesign/remaining-2026-10-15/programmatic/additive-budget-supplement/conversion-development-tests.json)、[原版树270类/8文件](evidence/feedback-redesign/remaining-2026-10-15/programmatic/additive-budget-supplement/native-category-preparation.json)、[转换源代码行与哈希](evidence/feedback-redesign/remaining-2026-10-15/programmatic/additive-budget-supplement/native-conversion-source-facts.json)。该原版树准备报告保存的是开发初期生成身份，树原文未变；最终使用源码和各证据身份见[封口清单](evidence/feedback-redesign/remaining-2026-10-15/programmatic/additive-budget-supplement/archive-manifest.json)。此审计未操作GUI或写原生状态。
