# RC3待验副本的填写步骤

工作副本为 [rc3-runtime-progress-v1.json](rc3-runtime-progress-v1.json)，不是最终验收索引。冻结树为 `178d3021fa53dd999b5537e1e58f7b59c7138232e7a7fe4fe53327b3dff8e116`，生产60文件；版本 `0.4.0-rc.3`，简中单生产Mod、精确EXE和静态三回调合同已绑定。18组全部PENDING，初始所有checks均为null，候选经济0月，成长观测为空。不要改成 `final-result.json`，也不要整体替换成脚手架重新生成，以免丢失已采集观察。

已导入的是公开0.3.1基线的三分支各12份原生预算，负电原值保留；不是RC3候选通过。蜂巢首两月没有独立economy文件，全部36条统一使用已提交聚合观察的date/balance/save_sha256，与实际SAV逐个核对。初始月2200.01.01不计入12月。

已挂硬件v2的真实限定结果：controlled shield hardware，56项PASS_SCOPED，实际输入hw0/hw1/hw2/hw2reload及相应分析；只说明护盾核心的受控0→1→2路径，case仍PENDING，未导入任何整组通过。原始遗漏设计层的预测FAIL继续归档；跨日／重载的原始严格差分FAIL仍在硬件报告里，不删除。自然RNG、其它五类实际属性、12月经济和完整配置／迁移均不能由此推断。

## 公共命令

从仓库根目录运行；`--index`、`--file`、`--analysis`、`--manifest` 都相对于 `eat_everything_origin`。以下变量只为减少手打路径：

```powershell
$idx = 'docs/evidence/1019-requirements/rc3-runtime-progress-v1.json'
$run = '20261019T092935Z'
python eat_everything_origin/tools/runtime_index_1019.py --index $idx missing
```

新候选run先归档真实manifest及完整原生证据包，再注册。不得把旧0.3.1基线manifest注册成RC3 run：

```powershell
python eat_everything_origin/tools/runtime_index_1019.py --index $idx add-run --manifest 'docs/evidence/真实目录/manifest.json' --case hive_startup --case hive_economy
```

每项来源用同一个命令挂入case；`kind`只能为 `native_save`、`screenshot`、`actions`、`log`、`analysis`。路径必须真实存在，工具计算SHA，不手写哈希。SAV要随实际audit/native-save receipt及来源包索引一并归档；最终检查器仍负责完整原生来源校验。

```powershell
python eat_everything_origin/tools/runtime_index_1019.py --index $idx attach --case random_components --run-id $run --kind screenshot --file 'docs/evidence/实际归档/实际截图.jpg'
```

同一真实证据可分别挂到多个适用case，但单个文件不能在同一case冒充多种类型。同路径字节改变会拒绝重新绑定；新版分析应另起文件名。

只对分析明确证明的单项记录true或false；未执行保持null。下例中的CHECK和ANALYSIS必须替换，命令不会把case或顶层改为PASS，也不会自行判断整份分析能证明哪些检查：

```powershell
python eat_everything_origin/tools/runtime_index_1019.py --index $idx observe-check --case random_components --run-id $run --check CHECK --result true --analysis ANALYSIS
```

`missing`给出所有尚未为true的检查名和缺失来源类型，不会输出通过结论。每次有效更新追加前一副本SHA、操作及参数；重复挂相同证据不产生无意义修改。工具禁止改冻结版本／树／文件／静态绑定，禁止操作任何非PENDING结果。

## 逐组最少需要补什么

每组最终都需要原生SAV、原始截图、动作、完整日志和分析五类来源；下表是组内仍需证明的事实，不是预置通过清单。先用 `attach --case <组名>` 归档，再按 `missing` 列出的精确check名逐项记录；完整case状态由最终审查另行处理。

| case | 最少真实输入／需要证明的范围 |
| --- | --- |
| hive_startup | 干净蜂巢新局初始、首月SAV与就业／母星界面；仅对应蜂巢母星、初始200、首月实际发电、人口／正常维护／自动默认关 |
| machine_startup | 相同机器新局起点与真实首月。现有fmm00可作起点，不能把人工硬件tier探针后的预算当干净开局通过 |
| purifier_startup | 普通洁癖干净遗落母星初始与首月；最终WS-06的截图和SAV也要挂在此case，run_id保持一致 |
| hive_economy | 干净最终蜂巢连续12个真实月初预算SAV及观察、完整行动记录；不注资源、补贴、关岗或拆舰；基线已填 |
| machine_economy | 同上，机器分支；必须从干净初始档走完整12月，不能使用被人工tier／资源／C探针污染的状态 |
| purifier_economy | 同上，普通洁癖分支；实际月净电逐月非负，原始失败或负值如实保留 |
| lithoid_hive_first_month | 石质蜂巢独立初始和首月来源，核正确母星、库存／就业／净电；不等于噬岩者自然战役验收 |
| mothership_configuration | 同国同日NAME_Relic与母舰的真实设计和面板；22大防御、五遗迹辅助组件保留、额外真实核心、供能／维护／优势、实际跃迁及十船坞；不授全帝国科技、其它主宰不受影响 |
| unlimited_growth | 原生C=0/9/10/19/20/200/10000对应L=0/0/1/1/2/20/1000，四项每级+5%、恢复与报告C/L/余量；重复同步／同日重载不叠加，毁舰不复生，无效取消不增长 |
| random_components | 当前仅受控护盾接口旁证。还需真实RNG阈值与跨级补差、六类正面效应／真实装配、R及六计数／应发／待发一致、重复及重载不重抽、无外部奖励modifier、其它舰队隔离。手改shield tier而C/R=0的探针不能代替这组 |
| colossus_enemy_fire | 战争敌方天然殖民星和本国非核心星的原生充能完整发射／销毁前后SAV、UI动作；无陆军、受益母星正确。排队图不等于已发射 |
| colossus_guards | 所有不合格目标的真实拒绝，包括未殖民／人工／任意母星核心／殖民中／地面战／吞噬中／中立友好／已结算；完成瞬间重验目标和母星归属 |
| colossus_cancel_idempotence | 原生排队、充能后取消、重复事件和同日重载前后；C/G/D／人口／容量／奖励计数不二次增长，危机进度只结算一次，奖励点须独立校准 |
| common_settlement | 分别有普通、本国巨像、敌国巨像及噬岩分支真实前后分析；q/C/G/D、原生损耗、人口返还／敌方不返还、材料制造人口／容量、危机与持久标记符合规则。单个路径数学通过不代表全组 |
| normal_dismantle_regression | 原有殖民拆解的种子、实际工期、正常结算及重载；不能直接调用结算effect冒充自然完成路径 |
| old_save_migration | 真正公开0.3.1来源；保留额外星／布局／民用队列，不发启动奖；真实受损及排队母舰的原生迁移前后／重载，核ID、名、位置、订单、队列、付费、声明的损伤口径。旧原型档不等同公开0.3.1 |
| candidate_reload | 最终候选的原生停止／重启／载入动作和同日保存，核账本、组件、奖励、绑定；仅两份同路径读取不能冒充重载 |
| repeat_initialization | 同一真实档的重复初始化前后SAV／动作／分析；无新增星、舰船、启动奖励或民用队列 |

## 月度预算字段由工具导入

候选每完成一个真实月初，先把SAV及其原始 `.economy.json` 观察归档，然后执行：

```powershell
python eat_everything_origin/tools/runtime_index_1019.py --index $idx budget --branch machine --role candidate --run-id $run --analysis 'docs/evidence/实际经济目录/fmm01.economy.json' --save 'docs/evidence/实际经济目录/fmm01.sav'
```

工具只从 `status=OBSERVATION_ONLY` 的 `date`、`energy.current_month.balance`、`save_sha256` 取值，并与实际SAV SHA核对，自动填写 `economy.machine.candidate_months` 的 `{date,net_energy,evidence,observation}`。负值原样写入并让case保持PENDING，不能改用库存变化、上月值或最后一月替代全12月。同日期不同结果拒绝覆盖，最多12份；不得把2200.01.01初始无有效预算月塞进去。

基线可重复校验／导入（当前副本已完成；重复不改变字节）：

```powershell
python eat_everything_origin/tools/runtime_index_1019.py --index $idx baseline --directory docs/evidence/1019-baseline
```

## 最终审查前仍需人工完成的少量字段

- `growth_samples`：填真实已证明的C/L列表，不能把 `_scaffold.required_growth_samples` 当观察自动复制。
- `component_rewards`：本副本固定PENDING。只有完整真实组件奖励通过后，正式索引才填写IMPLEMENTED及实际原因／证据；条件替代尚未采用，不能填DEFERRED略过。
- 各case和顶层status：本工具从不晋升。全部检查与原生证据经过最终审查后另建最终索引，再执行 `publish_1019.py check-runtime`；该命令当前预期拒绝尚未生成的最终索引。
- 活动日志不能宣称完整freeze。停止run后另行归档完整日志／索引，再挂 `kind=log`；已经归档的失败与有限范围差异继续保留。
