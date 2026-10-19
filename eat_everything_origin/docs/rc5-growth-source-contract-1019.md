# RC5六核心成长源合同适配

## 目标与范围

2026-10-19主线程要求在任何RC5真实成长数据前补齐精确源码绑定：现v1 selected source锁整个mothership effects旧字节，而RC5仅新增actual-layout修复helper及调用位置，六core RNG与evolution预测源没有变化。本轮新增不可变`six-core-source-expectations-v3.json`，将RC5完整冻结tree／59文件及selected新SHA与v1/v2公式、RNG、源body等价证据绑定；更新check_growth.package／报告模型指纹和publish对应tuple及必要正负测试。

不修改runtime_growth、economy、生产Mod、v1/v2或历史报告，不修改任何预测数值、成长节点、模型系数、HP工程容差合同或实际验收范围，不继承旧tree runtime PASS，不操作UI或Git。

## 设计与验收标准

先核对现有v1/v2、package实现、RC5冻结59文件和已生成源码差异审计。v3逐文件记录RC5选定源hash，并绑定v1/v2原SHA；对可变文件中的公式／RNG块按原始源码区间逐项核相等，明确只允许预先审阅的layout helper／designflag差异。未知tree、未知selected SHA、篡改模型／等价证明或缺v3必须拒绝；历史v1/v2字节不变。

报告显式使用v1/v2/v3模型SHA tuple；发布门禁用同一固定tuple。通过临时夹具和真实冻结源的只读package检查验证，测试包括精确RC5正例、旧锁冲突修复、未知树／选定源／被改模型拒绝。不得生成真实成长PASS或把旧报告重写成新合同。完毕后封口工具与模型SHA及CLI供主线程启动新数据采集。

## 调查与实施记录

已核对：v1/v2原SHA保持`bd3b4d48…2099f`／`a191eea4…71bc8`；v1六个selected中只有mothership effects整文件不同。RC3→RC5的完整RNG函数、L／entitlement／snapshot前段、scaled modifier／组件同步／pending后段三个原始源码区间完全相同；其余五个selected整文件相同。v3已新建并不可覆盖，SHA `942b98c2aea0022ff7ffa017944abbf873d36331fd26c89862f83a37e31e4dd2`，列出RC5树`1cc8b77c28f3d59b0d840982c7f039a209cb66f3e26d9c3280ad2dfa0f9dbd52`全部59文件和6个selected，直接保留v1/v2原公式对象及原HP政策字段，runtime状态PENDING。

实施采用独立无桌面的source package核对助手：先核相应模型原字节SHA，再精确匹配v3全部59文件／tree／selected，并保留原生来源SHA检查。新RC5使用三个模型；publish除了相同三模型tuple，也明确要求该模型对应的RC5 candidate tree；正式0.4.0仍通过原有metadata-only候选descriptor恢复机制匹配。合成guard测试可在临时隔离条件下替换预期tree；真实模型／树常量另与v3直接比较，不能把测试替换当实机证据。

实施期间kaishek线程指出既有economy默认RC4路径仍调用growth.package。为保留该已授权历史兼容，增加明确分支：仅原RC4树`06485dc540a88b30cef15c27c323ff21cd88f04ad57b79e4f5bc0590937ef468`、原v1/v2 selected与原始rc4-source-copy完整59文件索引（该文件SHA `4d948c9782197108c2703b89a4e65d3fc1e4636a322a9497a5ba88ca408b6a2d`）可走历史两个模型；RC4报告不写v3，旧报告不回填。所有其它tree均拒绝。package签名和返回manifest不变；该分支不允许RC4进入最终RC5发布验收。

后续主线程确认RC5实际二次load失败：designflag被序列化到root globalflags，使旧actual body被跳过；准备移除designflag并按current ship_growth_stage六core判据形成RC6。v3已封原字节，仍仅是RC5源码修订证书，不能改成RC6或解释为通过。实现先改为显式已知revision映射，每个tree只对应固定模型序列／证书字段／全量源索引；未知tree不能用传参或自动读新JSON注册。待主线程给实际RC6冻结tree与源后，另建不可变v4，并把最新发布合同切到v1/v2/v3/v4；不猜RC6哈希，数据采集前必须再封口。经济线程已进一步解耦growth.package；历史RC4精确分支仍保留API兼容，不改变经济规则。

主线程现已给出真实冻结RC6目录及树`cc181c8a27ede295e9fcebeffc5e10bb75e9cd643edec1d194b928993ffab33a`（59文件、0.4.0-rc.6）。按上述相同设计生成独立v4：再算全源tree、6selected和三个原始数值／RNG区间，明确继承v1/v2公式，v3仅为沿革；新guard以actual six-core stage判断，不再写designflag。open_kaishek尚在执行，v4只记录source-only，不能称静态或实机通过。

## 封口结果

v4原字节SHA为`6eb5ef0ef58fb353edd6e3f31b932ddc4bbf6b8b42b3bb6eaf2881fe51bd4c7f`；v1／v2／v3均再次核对原SHA不变。RC6 selected mothership effects整文件为`4e2d25004b917cd4b7c46bc13efe32765ba58fbd10aaa92a2728034a035da2cc`，其余5 selected整文件不变。RNG函数／L-entitlement-snapshot前段／modifier-RNG-pending后段分别仍为`36ee7d60…ae020`、`316c61b4…03df8`、`da942e22…2d3e5`；证书保留完整hash、原始区间字节数和逐项相等结果。

`check_growth_1019.py`增加精确已知revision路由和全源索引核对，package原签名及返回manifest不变。报告按实际tree输出2／3／4个模型；最终publish只接RC6树＋完整四模型tuple，RC4／RC5分支仅为历史工具兼容，不继承runtime通过。`prediction`、RNG期望、计数／HP比较函数及容差常量未改，`runtime_growth_1019.py`与经济工具未改。

验证：growth定向22项（4.128秒）、publish47项（59.906秒）、pending helper8项（3.859秒），共77项通过；定向diff空白检查通过。新增负例拒绝未知tree、selected及非selected变化、missing／duplicate源索引、篡改／缺证书、隐藏selected磁盘变化、改旧RC4索引／原生源、缺v3／v4或未知模型，以及模型应用到其它tree。真实RC4／RC5／RC6冻结59文件分别调用source助手通过纯文件核对；RC4 run112808和RC5 run143452的完整package（EXE／原static bytes）绑定亦通过；全程未导入desktop runtime。上述均是工具与源绑定验证，不是RC6静态或成长实机通过。

### 主线程调用

先等待RC6原生静态gate／manifest及真实干净C0 anchor；不要把RC5 FAIL fixture的结果文件当新RC6产物。现有CLI不变，实际路径由主线程真实新run代入：

```powershell
python eat_everything_origin/tools/check_growth_1019.py entry --anchor-receipt <RC6真实anchor.native-save.json> --prefix r6cg
```

entry会独立核package并返回dry_run_command／execute_command_for_root_only；其`--expected-tree`从已核manifest传入`runtime_growth_1019.py`，不需要改collector默认RC3常量。先执行返回的dry-run，再由主线程执行真实采集。十八phase与真实补样收齐后：

```powershell
python eat_everything_origin/tools/check_growth_1019.py report --receipt <新run/r6cg-growth-receipt.json> --repeat-receipt <真实same-day-repeat-receipt> --reload-receipt <真实same-day-reload-receipt> --budget-first-receipt <真实R400-P10-receipt> --budget-second-receipt <真实next-month-R410-P0-receipt> --budget-second-mode monthly --startup-receipt <真实startup-anchor-receipt> --output <尚不存在的新report.json>
```

尖括号为文档占位，必须替换真实路径，未运行这些采集／report命令。缺数据仍FAIL／INCOMPLETE，不能预置PASS。新receipt与报告应归档本次实际checker字节／v1-v4模型；既有旧工具源、manifest和报告不回填。本轮未读取RC6真实成长矩阵、未操作UI／Steam／Git或生产源。
