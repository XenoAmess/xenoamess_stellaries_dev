# 1019成长功能分支：两步月度原生自动存档编排

## 实施前设计

逐节点原生UI手动存档约需两分钟；新增独立 `tools/runtime_growth_1019.py` 薄CLI，复用 `runtime_1019` 的h物理输入、GPU／OCR和既有原生 `fast_forward 30`／月度自动存档校验方式。不得修改生产包、现有runtime工具或已归档证据。本子任务只实现和dry-run测试，不运行真实UI；主线程审查后显式 `--execute` 才能连接当前隔离简中运行。

固定节点为C=0／9／10／19／20／49／50／200／10000。每节点严格为：设置country C并调用真实sync一次；实际fast_forward30，验证HUD日期和本次原生autosave；导出10个ship modifier＋已证最大舰体／装甲trigger；再fast_forward30，验证HUD日期与原生autosave并归档带导出值的原始ZIP。禁止把两次30合并为60，也不重置fleet六tier或R。20500预算边界必须同日counts-only另由主线程手动完成，本CLI不包含该节点。

控制台THIS会随当前选中planet／fleet变化，故所有C和sync操作明确包在 `effect root={...}`（玩家country0）内；仅支持country0，不使用裸set_variable。导出直接指向已保存的 `event_target:eep_mothership0`，不依赖THIS索引。每份真实自动档必须核对实际country0.eep_c，否则停止并保留失败观察。

导出发生在第一步30日结束，而含诊断的自动档发生在第二步30日结束；两者相隔30日，必须分别记录input HUD日期和ZIP保存日期，不能将诊断变量误标成最终保存日刚测值。首份refresh ZIP提供导出时同日最大三防；final ZIP提供诊断持久值，并可核查期间是否有外部属性变化。观察器不因两者不一致擅自改系数或宣称通过。

## 前置条件与输出

输入为干净C0的原生 `.native-save.json` receipt（不是编辑的SAV）、唯一ASCII prefix、期望country／Mother fleet／ship、候选树SHA。anchor必须月初且与receipt的SHA／根日期一致，C0、L0、R0、六tier0，实际gov为机器灭绝政体，绑定target、owner和六个真实core各一份均匹配。未设的零tier允许初始化，但任何已有非零tier都拒绝，防止把此前C0人工shield1／2硬件档混入自然成长。执行首个30日原生autosave再次核对clean C0，以捕获同日却错误载入了另一脏分支的情形。

默认autosave目录由receipt实际 `history` 文件所在目录导出，避免原 `written_at` 文件被原生UI保存流程移走后继续错误绑定旧目录；可显式指定当前原生加载目录，但必须位于当前隔离userdir的save games内。默认dry-run只读anchor／manifest，不导入Win32／桌面模块，不修改当前运行指针、桌面、目录或SAV。

执行时核验当前run_id、简中、EXE／候选树、已通过的open_kaishek报告及其SHA和回调／CSV门禁，保存目录和活跃run匹配。相同prefix的任何旧输出都使新运行拒绝，归档SAV／audit／状态JSON均独占新建；只更新本次新建的progress receipt并保留已完成snapshots，不覆盖历史证据。运行不支持隐式续跑，失败后保留全部结果，新试验使用新prefix并由主线程重新载入正确anchor。

每个30日阶段都保留HUD GPU／OCR、物理输入动作、命令与其已确认console frame引用、原autosave路径、前后mtime／size、原ZIP完整CRC／根日期、原始SHA、归档SHA与audit。第一阶段原始ZIP也保留，因此共18份观察快照、其中9份final已含12字段导出。输出一律OBSERVATION_ONLY，不执行成长PASS判定，也不把自动采集成功当玩法验收通过。

## 控制台与失败收尾

每次输入必须有已观察的1024×768可见console frame。对已知不会关闭控制台的连续命令，可复用该次确认frame；每次等待HUD返回的新frame更新确认记录，避免同一控制台状态反复GPU截图。若可见性或几何不匹配则重新观察／打开并核对，失败时停止输入。h原有ASCII物理输入、Enter扫描码与动作日志保持不变，不提高输入速度或注入引擎内存。

正常或异常退出都依次调用既有关闭console、关闭Debug View工具；最后不再F12截图重新打开debug。收尾错误写入本次progress而不抹去先前异常。程序不启动、停止、加载或保存UI游戏，不改语言，不创建新游戏；主线程须先用既有简中UI载入anchor并暂停。

## 必要dry-run验收

新增独立单元测试仅使用临时合成ZIP／receipt及fake输入后端，不导入或调用桌面。覆盖跨年日期的18个30日步骤、每节点恰好一次C+sync与一次12字段导出、拒绝60日／tier或R重置、脏C0拒绝、防覆盖、过期mtime／错误ZIP根日期／坏ZIP拒绝、最终档必须保存导出变量。测试证明编排与证据约束，不仿真或认证Stellaris效果。

## 实施与使用

新增CLI和独立 `test_runtime_growth_1019.py` 已实施；9项合成序列／失败边界测试通过，`--help`可运行，dry-run无桌面runtime导入、无输出文件。曾发现合成测试夹具f-string大括号不配对，已改用明确字符串模板后测试通过；不涉及生产包或真实SAV。未执行live路径，不能声称GUI采集已通过。

从仓库根目录先审查计划（此命令不输入UI、不创建观察文件）：

```powershell
py eat_everything_origin/tools/runtime_growth_1019.py --anchor-receipt "C:\Users\1\AppData\Local\xenoamess_stellaries_dev\artifacts\1019-implementation\runs\20261019T092935Z\fmm00.native-save.json" --prefix gcauto1 --fleet 159 --ship 997 --dry-run
```

主线程用原生简中UI载入相同干净anchor并暂停，审查后采用相同参数改为 `--execute`。可选 `--autosave-dir` 必须指向当前原生加载目录；不要为了绕过缺失新档改到任意搜到的旧autosave目录。默认树为本轮冻结RC3；若实际候选更换须先重新门禁并明确指定新 `--expected-tree`，不得以该参数跳过gate／EXE／实际copied tree一致性。

```powershell
py eat_everything_origin/tools/runtime_growth_1019.py --anchor-receipt "C:\Users\1\AppData\Local\xenoamess_stellaries_dev\artifacts\1019-implementation\runs\20261019T092935Z\fmm00.native-save.json" --prefix gcauto1 --fleet 159 --ship 997 --execute
```

每次输入前重新核对当前run pointer仍属于anchor的同run；仅复用console可见frame，不复用跨run输入授权。全部结果写入该run的唯一 `gcauto1-*` 文件；主进度为 `gcauto1-growth-receipt.json`。18份raw ZIP／audit和growth-observation可直接交只读检查器，不在此CLI修改正式验收状态。退出后不得追加F12“确认截图”而重新打开已关闭的Debug View。

## 真实原生结构校正设计

主线程首次对真实fmm00进行只读dry-run时，发现初版合成测试没有覆盖两项实际原生结构：fleet159没有 `owner` 标量，归属保存在country0的 `fleets_manager.owned_fleets` 匿名条目；ship997三防字段为 `hitpoints`／`max_hitpoints`、`armor_hitpoints`／`max_armor_hitpoints`、`shield_hitpoints`／`max_shield_hitpoints`，初版误用了其他命名并会得到空观察。此前9项合成测试只证明编排，不能证明真实SAV兼容，原失败不抹去。

修正方案先按既有只读 `testing/inspect_1019.py` 的实际归属来源读取所有country的 `fleets_manager.owned_fleets`，要求Mother fleet只归属于目标country一次；若另有owner标量也须一致。保留保存target、唯一船舰及ship.fleet双向检查。三防观察使用上述六个原生键，并明确拒绝字段缺失，避免输出空对象看似采集成功。

新增只读派生fixture `tools/fixtures/fmm00-growth-native-extract.json`，从原生fmm00（SHA256 `18cae5e75b189ee8739cdadd3fc63d5c2929fad7a1d892e5382d0750d36c33d9`）逐块复制原始country归属／政体／变量、完整Mother fleet159、ship997及design1379，不修改SAV。fixture记录来源与原块SHA，测试包装ZIP只用于解析回归，不称原生保存；以此覆盖缺owner、真实三防键、真实六核心及冲突归属拒绝。验收要求为新增原结构回归通过、现有编排测试继续通过、真实fmm00 CLI `--dry-run`成功且不导入桌面runtime／不创建输出。live仍未执行，等待RC4新包与新的静态载入门禁合同。

该修正已完成：10项测试通过（含原生摘录回归），真实fmm00 CLI dry-run退出0，观察计划为18阶段、2200.01.01至2201.07.01，绑定原生history目录 `eep-test-history`。fixture SHA256为 `aa5056b7e9e47c9df9fb99e6f4694ade154e2731212ed9720bd8355229d47415`。未执行live，不将该结果表述为GUI自动采集成功。

## RC4载入来源门禁适配设计

RC3任意命名CSV未证明被引擎读取，因此不能再要求“CSV文件数至少1”作为执行前置。RC4改用专属TXT数值后，0CSV是合法候选形态。LiveBackend保留报告状态／SHA、source tree与实际copied tree、EXE一致性核验，随后复用 `publish_1019.validate_weapon_csv_contract(report, copied_mod)` 与 `validate_planet_killer_contract(report, copied_mod)` 两个共享纯校验函数；不另造放宽规则。后者同时核numeric合同 `native_csv_or_literal_txt_v1` 的实际PK键与来源字节；前者核 `native_fixed_paths_v1`、未支持文件数0、0CSV的明确not_applicable。旧RC3报告不能因旧status=PASS而继续采集，新RC4必须重新open_kaishek并指定新tree。此适配仍仅开发和只读校验，不连接桌面。

共享合同适配已实施，10项collector测试再次通过。只读调用两个共享validator校验原RC3冻结包／原报告，分别因缺少受支持的CSV loader合同与numeric载入合同而明确拒绝。随后同进程对真实fmm00生成18阶段PLAN_ONLY计划，实际六health值为93960／93960、44787.6／44787.6、167310／167310，归属country IDs为 `[0]`；`runtime_1019`未导入，`gcauto1*`输出文件数量0。新RC4正向载入门禁及真实UI执行由主线程另验，此处没有宣称通过。
