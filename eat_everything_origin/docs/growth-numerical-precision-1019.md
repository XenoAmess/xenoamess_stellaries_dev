# 成长大等级三防的事前精度判据

## 目标与调查边界

在任何RC4新成长矩阵SAV出现前，主线程要求评估C10000／20500（L1000／2050）下固定绝对0.01三防容差的误拒风险。本次只读已归档RC3与1015原生SAV和文档，计算既有源公式的数值尺度；没有读取未来RNG结果、没有改生产Mod或历史报告，也没有用观察误差拟合新阈值。

## 原始数据与不能证明的事项

- RC3 run092935Z的fmm00、hw0／hw1／hw2／hw2reload原始Mother ship997字段保存为44787.6装甲，盾分别167310／171492.75／175675.5；同档其他舰如ship118有3226.2336盾、3069.4028甲。读取的是原ZIP gamestate文本，不是UI格式化字符串。其SHA在既有硬件报告中固定。
- 原1015 `v13-shipyard-runtime/j13ten.sav`（SHA `834ea5325f93e3d3e92a44aabccd87195564cd4f1292d4439ae865eba5af8d2e`）原Mother ship822字段为24429.6装甲、48370.608盾。
- 主线程另指出44787.60156这类数值；它与44787.6的最近binary32值44787.6015625舍入到五位小数一致。但上述旧原始文本同时存在较短小数形式，所以不能仅凭这种吻合断言所有三防字段、所有计算环节、所有SAV序列化路径都已证为float32。
- 本机原生组件／效果／trigger文档说明字段语义与scope，没有公开这些闭源内部字段的位宽、累加顺序与完整序列化精度合同。本次未逆向出相应引擎字段结构，不把SAV外观当成引擎源码证明。

[Python官方struct文档](https://docs.python.org/3/library/struct.html#format-characters) 明确标准f编码采用IEEE754 binary32；本研究用它计算“如果存在binary32舍入”时的量化尺度，仅为可复现的工程参照，并非把Python实现视为Stellaris内部证明。

## 不依赖未来样本的反例

采用已经冻结的源增量与既有C0示例A0=44787.6／S0=167310，令对应核心tier=0（其他核心可承接R，不规定随机分布）：

| C／L | 源算术期望 | 最近binary32 | 仅最后一步舍入误差 | binary32 ULP |
| --- | --- | --- | --- | --- |
| 10000／1000，armor | 1331787.6 | 1331787.625 | +0.025 | 0.125 |
| 20500／2050，armor | 2683137.6 | 2683137.5 | −0.1 | 0.25 |
| 20500／2050，shield | 4454628.75 | 4454629 | +0.25 | 0.5 |

换成主线程示例A0=44787.60156，前两误差仍分别约0.02344与−0.10156，大于0.01。即使只有最终数值一次binary32量化，旧阈值也可能误拒；多次乘加还可能引入累计舍入。以上均是预先固定公式的数学分析，没有读取真实高等级SAV。

在源示例及0≤单类tier≤R范围，C10000／R200时三防ULP约0.125—0.25；C20500／R400或410时约0.25—0.5。不能无条件只预算0.125／0.25，较大的盾可能跨过2²²而达到0.5 ULP。

## 主线程已确认的事前工程合同

主线程在新矩阵执行前确认：仅三防HP量使用 `abs_tol=max(0.01,8*ULP32(expected))`、相对容差0。ULP由预先计算的expected决定，不根据实际误差选阈值。8ULP为覆盖数次乘加、截距与保存量化的保守工程预算，不是已经证明引擎只使用binary32，也不是闭源全部计算的形式化误差上界。源公式、真实tier与基线系数保持不变。

- 三防HP量包括原生current／max舰体、装甲、护盾、max hull／armor的trigger导出、普通舰最大三防，以及同日repeat／reload与startup稳定对照的相应HP字段。
- 十个modifier导出仍固定绝对0.01、相对0；其中ship_hull_add虽以HP为单位，但作为预定不变的十modifier频道仍按该固定规则，不与最大三防混用。
- C／L／B／R／P／tier、国家镜像、组件template／slot、身份、设计布局等离散检查仍精确，不引入浮点容差。
- 小HP的8ULP低于0.01时仍为原0.01底线；本轮高等级例的HP容差约1—4，远小于少整级的1287／1500／2091.375或少一核心的2574／3000／4182.75。
- 非有限数、缺字段、不能编码成有限binary32的expected不能获得无限容差而通过，应明确失败。此合同只服务本轮可分辨的数值尺度，不证明任意巨大等级仍能分辨每一级，更不证明数学无限精度。

## reporter实施设计与发布对接

只修改 `tools/check_growth_1019.py` 和必要定向测试，另设HP比较函数，不扩大普通modifier比较。保留top `absolute_tolerance=0.01` 表示固定频道基线；新增 `hp_tolerance_contract=max_0p01_or_8_binary32_ulp_expected_v1` 与hp_tolerance对象，明确floor0.01、8ULP、rel0和非引擎位宽证明分类。各数值检查记录expected、observed（兼容actual）、raw_delta、applied_tolerance、ulp32_expected及ulp_error，不只输出一个passed布尔值。

定向验证在新SAV前覆盖：L1000／2050的合理最后一步binary32舍入可接受；缺整级、缺一核心和错误modifier仍拒绝；小值仍按0.01；无穷／NaN／缺值不通过。既有固定预期公式与历史JSON完全保留。发布门禁文件由release_pipeline独占最小适配，只接受这条明确政策；不并发修改其文件。任何未来失败先保留原数据与误差报告，不能看过矩阵后继续加ULP倍数消除失败。

## 实施结果

授权后仅修改reporter与其定向测试：新增 `binary32_ulp`／`close_hp`，只在上述HP调用点启用8ULP，原 `close` 仍固定0.01；未改变源预测函数、collector或生产文件。数值row保留兼容actual并输出observed／expected／raw_delta／applied_tolerance／ulp32_expected／ulp_error，tolerance_kind明确区分 `hp_binary32_ulp_engineering` 与 `fixed_absolute`。非有限输入以明确字符串／缺失诊断记录且不通过，不输出无限容差。

`test_check_growth_1019.py` 的14项定向离线测试通过，包括5项新增精度场景：L1000／2050量化、少整级／少核心、大值modifier不借HP放宽、小值0.01及非法数拒绝、repeat／reload HP放宽不扩展到modifier。既有公式算术、预算与原生摘录回归继续通过。这是检查器验证，不是RC4 Mod成长实机结果；未读取未来矩阵、未改历史报告。release_pipeline已收到精确新增合同／字段命名，独自负责publish门禁适配。

Root independently reran python -m unittest discover -s eat_everything_origin/tools -p test_check_growth_1019.py -v: 14 tests passed. An earlier invocation against testing/ discovered zero tests and returned exit1; it is not counted as verification. The corrected location is tools/. No future RC4 growth SAV was used.
