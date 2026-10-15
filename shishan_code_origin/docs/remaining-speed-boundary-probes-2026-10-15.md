# Q2 月速边界原生前置与隔离夹具

日期：2026-10-15。目标生产版 `0.2.1`；用户授权继续受控功能验收，未授权本协作者操作 GUI 或启动游戏。

## 目标与范围

为原 SP-01—04/JB-02 准备可审计的原生输入。优先解决实际已分配维护员劳动力 `J=99/100/199/200` 及跨殖民地 `50+50`，并提供确定的 `n=0/1/10、J=0` 前置。目标公式是 `max(0.2,1+0.25n-0.25*floor(J/100))`，但夹具只设置前提，不写局势月速、`last_month_progress`、预期减速或期望产出。

## 设计与验收标准

先核对当前 4.5.2 实际安装脚本和实际引擎生成的 effects/triggers 文档。岗位数量与已分配劳动力严格分开；没有原生依据的 workforce 字段不得构造。允许设置 n、原生人口数量和岗位容量，禁止编辑 gamestate 或直接写观测输出。

如 API 足以可靠实现，新增独占 `testing/mod/events/shishan_speed_probe_events.txt`，必要资产仅使用本夹具前缀；不改既有经济夹具、README、生产脚本或 runtime 工具。组合包放置 `_runtime/shishan_code/20261015-remaining/speed-fixture/mod`，由90文件正式生产拷贝和本夹具组成，先经 open_kaishek G1 后交主任务实际运行。

程序验收要求包括生产文件逐字节保持、夹具标记/输入 guard、禁止写预期输出、原生 API 来源和包级 G1。真实就业、连续三个月推进差、阶段与 UI 均需主任务实机及原生存档证明。不能用容量、fixture READY 日志或离线公式代替实际 J；尚未定位精确分配 API 时记录调查事实并继续可确定前置，不删除需求、不将工作难度直接记 BLOCKED。

## 调查记录

生产 `shishan_code_maintainer_reduction` 在局势 owner 国家作用域分别读取两种 `num_assigned_jobs`，相加后除100、floor并乘0.25；现有月速脚本不按建筑容量计减速。

### 已查明的 4.5.2 接口

依据实际运行 `20261015T090720Z/logs/script_documentation`：`effects.log:49–51` 的 `check_planet_employment=yes` 在 colony/planet/ship 上立即真实重算就业；384–395 的 `create_pop_group` 接受 species/category/size；480–488 的 `add_modifier` 支持 colony 与 multiplier；557–564 的 `export_trigger_value_to_variable` 可带参数导出原生 trigger 真实数值。`triggers.log:3059–3061` 的 `num_assigned_jobs` 支持 country/colony，参数为 job/value。`modifiers.log:44392/44400` 注册两种生产维护员的 Colony 容量键。未发现把任意劳动力数直接指定给岗位的 setter。

此外，原生支持 `remove_building`、`remove_all_buildings`、`remove_all_districts`、`every_owned_colony`、`is_capital` 和 `num_owned_colonies`。原版 `common/scripted_effects/pop_group_effects.txt` 使用 create_pop_group/category，`common/pop_categories` 定义 specialist 与 complex_drone。这里只把真实人口和容量作为输入，再由原生就业算法决定分配；不会声明容量=就业。

### 冻结的夹具实施方案

新增文件仅使用 `shishan_speed_probe` 前缀：events 入口、一个 scripted effects 文件、两个仅提供岗位容量的 static modifiers，以及十语只复用既有岗位本地化的别名文件。不修改既有测试文件。组合包仅复制正式90文件和本夹具文件，不混入经济/架构/旧档 probe。

- `.1/.2/.3/.4`：分别设 n=0/1/10/5；先在全部本国殖民地移除研究所和本夹具容量，再实际重算就业。只有两类真实维护员就业都为0，才设置 n 和 n-ready 标记。失败保留诊断，不假报 J0。
- `.99/.100/.199/.200` 等容量入口保留已选择的 n；仅在 n-ready、有效起源局势、无奖励或项目回调待结算时执行。先清理全国产生维护员的研究所/本夹具容量，再把资本上的建筑和区划清空，加入单一对应政体的生产维护员容量 modifier，并创建2000真实人口（specialist 或 complex_drone）作为足够的就业前提。原生就业重算后，只有实际国家两种岗位计数合计等于请求值，才 READY。
- 完整容量入口还包含299/300/399/400/499/500/700/800/899/900/1200，用于原SP01/02其余边界。这些数是输入容量，不是输出或已观察 J。
- `.50/.51/.52`：资本+已有第二本国殖民地分别提供50+50、99+1、50+0容量。入口在修改任何数据前要求至少两颗本国殖民地；不自动创建殖民地或挪用外国殖民地。两颗受控殖民地同样清建筑/区划并创建对应类别真实人口；READY同时核对两地实际就业和国家总数，防止只验证容量或只验证国家合计。
- `.9000`：仅重新导出真实 num_assigned_jobs 并复核所保存的输入，不创建岗位、不加人口、不重算就业。country 和带标记殖民地的 observed 变量必须由 export 原生值形成，不能复制 requested 值。所有条件不满足均打印明确诊断，不注册 runtime PASS。

这些准备会大幅改动**隔离受控存档**的人口、建筑与经济输入。主任务应从副本分支运行，不覆盖普通存档；每次容量准备会再创建2000人口，故比较前必须从相同原始种子重新加载，不能把多次准备串联当同人口经济对照。容量足够应仍以真实 J 验证。跨殖民地没有第二殖民地时，是输入尚未满足，后续可通过合法原生殖民补前提，不据此删除SP03或自动记环境BLOCKED。

程序检查增加本夹具独占测试，验证上述控制与观测隔离、原生API来源、两个政体、跨地前置、容量键和不修改生产。负例必须拒绝直接写last_month_progress/局势进度、伪造就业setter或把requested复制到observed。先执行组合包 G1，再执行这些基本检查；它们不模拟原生就业或月结算。

SP04的阶段起点可由主任务用原生 `set_situation_progress` 单独建立输入并保留前值，但本夹具不写局势进度，避免把月速实验与阶段跳转混合。JB02要求正常建设两座研究所并记录真实400矿物/360天/2能量维护；本夹具瞬时添加容量不能证明建设成本，仍须另行原生建设取证。原SP01中“有空容量但J0”也须从原生禁用岗位或无合资格人口前提另验，本夹具J0为撤销容量，不能冒充该项。

## 程序执行结果与交付

已实现23个隐藏、仅触发式 country events、4个 helper、2个容量 modifier 与十语各4条岗位别名。新增13个 fixture文件；生产90文件及正式版本身份均未改变。组合包共103文件，路径为 `_runtime/shishan_code/20261015-remaining/speed-fixture/mod`。没有复制其它 probe。

先执行首道包级检查：

```powershell
python -B C:/workspace/open_kaishek/tools/accept_stellaris_mod.py `
  --mod _runtime/shishan_code/20261015-remaining/speed-fixture/mod `
  --version-file shishan_code_origin/VERSION `
  --game 'C:/Program Files (x86)/Steam/steamapps/common/Stellaris' `
  --expected-exe-sha256 400df27c82ddc845aa9dce79bd468d81f18f060d299cd263e3afa93aef4f7a83 `
  --report _runtime/shishan_code/20261015-remaining/speed-fixture/package-open-kaishek.json
```

实测退出码0，PASS：28/28脚本、13DDS、十语273键；有限人口scope检查202项、零诊断。script value形状检查为NOT_APPLICABLE，不能据此宣称就业或新fixture API完整语义通过。报告JSON规范为UTF-8/LF，数值未改。

随后执行：

```powershell
python -B -m unittest discover -s tests -p test_shishan_speed_probe_fixture.py -v
```

9项通过，退出码0，0跳过。检查包含 n 必须在真实J0确认后才变更、两政体原生类别和容量、跨地必须已有第二本国殖民地并逐地检查、观察入口不创建/分配岗位、原生API文档存在及生产身份不变。故障负例确定性拒绝直接写月速/局势进度、虚构就业setter、requested复制到observed和移除原生export。没有用离线就业模型填充预期结果。

证据目录包含 `source-manifest.json`、`package-open-kaishek.json`、`fixture-static-tests.json`、`native-api-and-input-catalog.json` 及 `native-pop-job-schema.json`。后两者分别保存带原始行号/哈希的原生API和原生存档岗位记录例子。历史原生 `pop_jobs` 中确有 `workforce`、`max_workforce`、`pop_groups[].amount`、`planet` 等**观察字段**；字段存在不代表有合法script setter。本夹具不写这些字段、不生成sav。样例中工作岗位原始 workforce 与所属group amount求和也可能出现缓存/取整差，因此新边界须同时核对原生export、实际岗位原始记录及观察时点，不能挑一个字段拼成预期。

### 交给主任务的最小实机步骤

1. 新隔离运行加载组合包，G1身份见上述报告；选择已有起源局势、无奖励待领/回调待结算、无在研维护/清理/优化、无建筑队列即将完成的原生种子副本。两政体各自运行。保留源sav/包/版本哈希，暂停并从同一源分叉每个容量案例。
2. 执行 `event shishan_speed_probe.1`，检查 `SHISHAN_SPEED_PROBE_1_READY_N0_J0_INPUT_ONLY` 与 `SHISHAN_SPEED_PROBE_READY_NATIVE_EMPLOYMENT_ONLY`。原生保存起点；推进三个完整月分别保存并读取原生局势进度、last_month_progress及真实J。未满足READY时保留错误与实际export，不写测试PASS。
3. 从相同源分叉，先`.1`再`.99`，对应`.100/.199/.200`等。仅容量为输入；核对国家与资本原生export、原始jobs和人口。三个月中若自然组装/就业重排导致J改变，先保留事实，重新建立稳定前提再完成同J差分，不把错位时点当公式失败或通过。
4. n=1用`.2`、n=10用`.3`、n=5用`.4`，随后运行所需容量事件。n0/J0、99、100、199、200的独立纸面预期依次为1、1、0.75、0.75、0.5；n1/J0为1.25，n10/J0为3.5。预期只在报告中，不在夹具中写入。
5. 跨地种子必须已有第二本国殖民地。从源分叉`.1`后`.50`检查实际50+50，`.51`检查99+1，`.52`检查50+0。前两者n0月速应0.75，后一项应1；必须同时确认两地与国家的实际就业，防逐地floor错误。`.9000`仅刷新原生观察，可在各月保存前运行；它不会强制就业达到目标。
6. 关闭隔离运行后，在原生保存的输入状态下，以正式90文件、无本夹具重启重载，确认生产公式仍按实际就业工作。移除容量fixture会同时移除其岗位来源，应明确记录岗位已消失的输入变化；不得要求已移除fixture的容量仍存在。正式研究所来源就业的重载另用正常建筑种子验证。

本协作者没有操作GUI/显示、启动游戏、修改生产/运行工具或编辑gamestate。静态前置已交付；实际J的可构造性、三月差分、跨地分配、阶段边界、空容量和真实建设成本仍待主任务原生运行，当前均不登记SP/JB实机PASS。

## 可提交的原始证据

相关JSON已保字节沉淀到本目录的 `evidence/feedback-redesign/remaining-2026-10-15/programmatic/speed`：[组合包G1](evidence/feedback-redesign/remaining-2026-10-15/programmatic/speed/package-open-kaishek.json)、[9项静态/负例结果](evidence/feedback-redesign/remaining-2026-10-15/programmatic/speed/fixture-static-tests.json)、[原生API与输入目录](evidence/feedback-redesign/remaining-2026-10-15/programmatic/speed/native-api-and-input-catalog.json)、[原生岗位schema样例](evidence/feedback-redesign/remaining-2026-10-15/programmatic/speed/native-pop-job-schema.json)、[复制清单](evidence/feedback-redesign/remaining-2026-10-15/programmatic/speed/source-manifest.json)和[字节封口](evidence/feedback-redesign/remaining-2026-10-15/programmatic/speed/sealed-static-summary.json)。

[归档清单](evidence/feedback-redesign/remaining-2026-10-15/programmatic/manifest.json)保存源/目标与相同SHA256；原JSON内的_runtime路径保留作来源，不改写原文。未复制整个103文件组合包，测试源码位于 `testing/mod`；生产90文件未变。
