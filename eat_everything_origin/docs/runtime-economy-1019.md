# RC4三政体十二月原生经济采集器

## 实施前目标、范围与验收

新增独立 `tools/runtime_economy_1019.py`，减少既有每月console开关和重复GPU截图造成的等待。默认dry-run，只有主线程明确 `--execute` 才连接当前简中UI；本实现代理及测试子代理均不操作桌面。保持每月独立一次 `fast_forward 30`、十二次真实HUD日期与新鲜原生自动档核验，不合并360日、不新建矩阵或调整生产Mod、经济资源、C、tier、工作岗位或舰队。

仅接受本轮RC4树 `06485dc540a88b30cef15c27c323ff21cd88f04ad57b79e4f5bc0590937ef468`、59文件、游戏EXE SHA `400df27c82ddc845aa9dce79bd468d81f18f060d299cd263e3afa93aef4f7a83`、单独Mod profile、唯一enabled_mod与简中run；共享publish两项原生numeric／CSV来源门禁必须通过。三类政体显式传 `--government machine|hive|purifier`，按原生government中的真实对应civic核对，不从prefix或role猜政体，也不对Hive／Purifier套用Machine检查。

输入为新游戏2200.01.01真实UI保存的receipt；archive与history字节核原SHA／ZIP／根日期，Mother fleet与唯一ship由saved target发现，不硬编码ID。C／L／R／六tier／B／P始终0、country与fleet镜像一致、实际六核心装在专属槽位；每月重新核对，污染则先保留实际原始ZIP与audit／receipt，再停止，不继续造成样本混杂。只读取原生存档；合成测试不宣称实际引擎经济通过。

## 目录、命名与防覆盖

默认原生auto目录为新Jan1receipt的 `written_at.parent`；history是工具移动归档后的anchor字节来源，不决定引擎当前campaign目录。若已原生reload，应显式 `--autosave-dir` 指向已观察到的活动目录。目录必须在当前隔离userdir的save games内，不自动搜索其他目录或旧auto以掩盖错误路径。

root计划prefix为 `r4mc`／`r4hv`／`r4pu`。已存在的同prefix `m00.sav`、audit与native-save receipt作为只读anchor允许保留，不因任意prefix文件已存在而误拒。未来 `m01`—`m12`、`yearui`、总receipt及auto/UI comparison有任何同阶段旧产物就拒绝，既有原始receipt绝不更新或覆写。每月独占新建 `<prefix>mNN.sav`、`.audit.json`、`.economy.json`、`-receipt.json`；逐份receipt包含archive/date/SHA、source路径／mtime／原ZIP日期、GPU／OCR及真实命令记录。每份月receipt写完即固定，供独立代理及时分析；最后一次独占写总receipt与原manifest／anchor SHA绑定。失败也写一次总receipt保留已完成月度索引，不修改此前月receipt。

## UI与采集顺序

借用既有growth LiveBackend的物理输入、可见console frame复用、HUD日期等待与active-run guard。连续12次已知不会关闭console的单月命令之间保持console；每次HUD新观察更新frame，下一输入只有在观察确认console仍可见且1024×768时复用，不反复开关。只复用可见状态，不绕过前台窗口或活动run检查。

每月命令前记录目标auto旧mtime与开始时刻；推进30日后核实际HUD日历，读取稳定的新ZIP（前后mtime／size、完整CRC、根日期、SHA均绑定），归档原字节，不编辑SAV。写audit、经济摘要和不可变月receipt后逐月stdout输出OBSERVATION_ONLY进度；C／tier污染或其他失败同样保存已见事实后停止。

第12月结束关闭console与Debug，再用现有原生 `native_save(<prefix>yearui, 2201.01.01)` 同日保存，对比auto与UI原始经济字段：country budget_categories／stockpile／variables／flags／owned_colonies，以及districts／pop_jobs／pop_groups／planets／colonies。保存独立比较JSON，任何差异都保留且停止，不把自动档“采到了”当成经济PASS。最终无论成功或失败再次使用既有收尾工具关闭console／Debug，之后不再F12截图重新打开Debug。程序不新建游戏、不reload、不调整语言或profile。

## 测试与使用计划

少量离线测试覆盖三真实government civic结构、默认无UI导入／无输出、written_at与history目录分离及显式override、既有m00合法／未来阶段拒覆盖、恰12次FF30与逐月receipt不变、中途污染实际档留存后终止、yearui同日对照与失败收尾。默认dry-run与报告工具均可读取实际RC4包做纯文件门禁检查；没有新Jan1anchor时不伪造一份实际采集成功报告。

主线程新游戏Jan1原生anchor完成后，例如：

```powershell
py eat_everything_origin/tools/runtime_economy_1019.py --anchor-receipt "C:\Users\1\AppData\Local\xenoamess_stellaries_dev\artifacts\1019-implementation\runs\20261019T112808Z\r4mcm00.native-save.json" --prefix r4mc --government machine --dry-run
```

主线程审查计划且当前游戏仍为该anchor时，将末尾改为 `--execute`。Hive／Purifier分别传对应真实receipt与prefix／government；不额外create/load，不添加非中文实机分支。程序输出的最后yearui原生receipt可作为同一Machine后续成长工具的year1干净C0 anchor。

## 实施与离线结果

工具已实施，复用growth LiveBackend；每月归档后再独立读取实际设计槽位，确认六core真正在AUX6—AUX11，不能仅数六个template各一件。纯文件前置也读取实际 `dlc_load.json` 与 `settings.txt`，核唯一Mod、简中与monthly autosave，不只相信manifest声明。每月receipt写完后固定不改，总receipt在正常或异常收尾只新建一次；yearui比较仅报告原经济字段是否相同，采集状态始终OBSERVATION_ONLY／COLLECTED_NOT_ACCEPTED，不生成经济玩法PASS。

测试由获授权的并行子代理在独立新 `test_runtime_economy_1019.py` 实施，8项离线测试全部通过：原fmm00块派生的三政体／不同Mother ID（fleet271／ship1401）、无UI dry-run、目录／覆盖保护、十二单月与月receipt不变、月3污染保留实际原ZIP后停止、yearui差异留证与异常收尾，以及六core仍各一件但盾核心错放AUX1时拒绝。政体替换、预算与输入后端均明确属于合成测试，不是三政体真实实机证据。

另外只读验证现RC4 run112808实际copied59文件、新open_kaishek报告／原生数值与CSV来源合同、EXE、唯一Mod和简中／monthly设置均匹配；该进程未导入 `runtime_1019`。未操作UI、未生成真实新Jan1采集结果、未改生产Mod或旧工具、未直接提交。真实GUI采集、三政体十二月经济判定与yearui对照仍由主线程执行和独立只读审查。
