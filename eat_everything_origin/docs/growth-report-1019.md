# RC4成长采集入口与独立报告工具

## 实施前目标、范围与门槛

当前RC4为run `20261019T112808Z`、树 `06485dc540a88b30cef15c27c323ff21cd88f04ad57b79e4f5bc0590937ef468`。主线程完成PK分支后，在同一已门禁的简中进程中建立Machine灭绝政体新局，先完成12个月经济验收，再从该同一局year1月初的C0／L0／R0／六tier0继续独立成长功能分支。只需一次原生UI保存建立year1新anchor，不额外newgame或载回原Jan1。主线程独占UI；本子任务只读复核与实施离线工具，不输入当前游戏、不改Mod或旧SAV、不直接提交。

现有 `native_save` 把实际UI文件移到history供加载列表与SHA归档使用；未reload时，引擎仍向 `receipt.written_at.parent` 保存自动档。因此collector默认修正为written_at.parent，anchor字节仍验证history SHA；已实际从history／其他路径加载时，应显式 `--autosave-dir` 指向经观察确认的活动campaign目录。不能根据归档目录存在与否猜测。错误目录等待失败后保留该次结果，新prefix重新开始，不自动检索别处旧档。

新增独立 `tools/check_growth_1019.py`，使用既有无副作用的SAV分词器与设计／timed_modifier解码器，直接重读原ZIP并核collector receipt的SHA／根日期，不依赖采集器生成的growth-observation JSON。可准备入口命令与离线验收；CLI全程不导入runtime／Win32、不写SAV。输出文件必须独占新建，已有报告不覆盖。

## 最少UI入口

1. 主线程在RC4的同一Machine新局完成12个月经济后，确认year1月初C0仍干净，保存一个新名称，例如 `growth4base`，保留原生receipt。由原生保存后的实际written_at目录继续采集，无需reload。Mother fleet／ship ID由anchor保存target与实际唯一舰船读取，不能沿用RC3的159／997假设。Jan1原始档保留，可用可选 `--startup-receipt` 比较其与year1C0 anchor的Mother及country0普通船最大三防；该稳定对照单列，不冒充成长属性基线或倒算系数。
2. 离线 `entry` 子命令读取新receipt、run manifest、source gate，验证实际包字节、简中、EXE、RC4树及新numeric／loader合同，检查clean anchor，输出准确collector参数与autosave路径。可复制其中collector命令先dry-run，再由主线程显式execute。
3. collector保持九节点C=0／9／10／19／20／49／50／200／10000，每节点严格两次fast_forward30：第一次刷新后导出十modifier与两最大值，第二次获得带导出的原生月存档。原始十八ZIP、日期／SHA／mtime、HUD与输入证据保留。两次30不得合成60。
4. 九节点后，在最终档同日先重复sync并导出原生UI保存一份repeat；对这份档实际同日重载，再同样导出／保存reload。两份补充receipt交独立报告工具，作用域业务字段一致与全gamestate一致分别报告。
5. 从C10000／R200继续同日设置C20500且sync一次，立即原生UI保存first（应R400／P10，不等月度／触发刷新）；再同日sync一次保存second（应R410／P0）。这是手动分批补差，不冒称月度补差。若验月度路径则额外分支保留first并在下月检查；不让月度先跑掉而丢失200预算边界。

所有country操作明确 `effect root={...}`，ship导出明确saved target，不依赖选中THIS。新Machine月初不能直接复用PK档去改C0。任何新游戏、保存、重载、控制台与Debug收尾都由主线程既有物理输入工具执行。

## 九节点判据与来源冻结

报告固定使用已写在未来SAV之前的 `six-core-source-expectations-v1.json`／v2（SHA分别 `bd3b4d48eeb5de98b34a8ba104f55c23f17cb43a723a216934f2c2a1c4a2099f`、`a191eea40464ef3fde5f7ec64f33ac2d7012ef74d6b6cdea900d441a16371bc8`）。RC4 PK时间修复不改变这六份成长／组件／装备来源；报告必须验证它们在实际copied_mod仍与v1记录SHA一致，否则拒绝固定模型。

每份SAV要求绑定Mother唯一且归属country0，六个真实core分别位于AUX6—AUX11（盾／甲／舰体／伤害／追踪／再生），保留完整装备签名，不能只看到本地化或fleet变量。L=floor(C/10)，next=10−C%10，B=floor(C/50)，R=sum六tier，P=max(B−R,0)，fleet与country六tier／R镜像一致、snapshot_state=0、临时预算变量已清除。九节点B均≤200，完成后R=B／P0；随机层数不预指定，但不得减少。

真实C0的独立最大三防及十modifier导出是固定截距。后续使用源固定增量：H=H0+1500L+3000Nh；A=A0+1287L+2574Na；S=S0+2091.375L+4182.75Ns；三个mult为原截距+0.05L+0.10对应tier；damage=D0+0.05L+0.05Nd；tracking=T0+3Nt；两fixed regen=各自截距+0.1L+0.2Nr。三个flat add保持截距。不会把Machine已知4.05小计强填为完整damage导出，不从后续SAV拟合tier或系数，不把固定回血导出称为实际治疗量。

同节点refresh与final原始SAV须C／L／tier／R及完整装备签名一致；十modifier与max H/A诊断虽存于final ZIP，诊断输入发生在refresh日期，两者时间须记录。模型预测同时核refresh及final的原生最大三防，并将max H/A导出核到refresh当天原生值，不把其标为final日新测。若出现其他适用国家／领袖／科技变化导致偏离，保留失败并调查，不能改系数消除失败。独立报告只限定已导出的频道，不能自动证明全部外部来源稳定。

L0不应有成长timed_modifier；L>0 fleet恰一条永久 `eep_mothership_evolution`，multiplier=L，不能堆叠或额外挂六类奖励modifier。六类非零tier覆盖逐项报告，未覆盖不声称已验证该类硬件增益。

数值容差在读未来九节点前固定为绝对0.01、相对0，沿用既有硬件报告的存档小数处理；C／L／B／R／P／tier、身份与槽位等离散字段精确比较。不得根据后续结果增加容差。

## 报告与验证设计

`entry`只输出PLAN_ONLY；`report`生成矩阵、repeat、reload、20500 budget四个独立范围的检查，缺补充样本明确NOT_PROVIDED。矩阵通过只能写PASS_SCOPED；整套所需样本不齐时总状态INCOMPLETE，有明确不匹配时FAIL。重载业务签名可通过，但strict_gamestate_equal单列实际布尔值，不因设计ID等已知变化把全档写成PASS。未把破舰不复活、普通舰负对照或报告UI覆盖纳入本工具的自动通过范围。

必要离线测试覆盖：原生摘录解析、预先构造的边界计数与固定预测计算、误差／缺导出拒绝、预算400／10和410／0、重复抽取失败、业务重载与严格全档差异分离、报告独占写入。这些测试不模拟Stellaris RNG、计时或实际组件；真实九节点SAV尚未产生时不能生成一份假通过报告。

## 使用命令

新anchor实际产生后，用它的真实路径替换占位名称：

```powershell
py eat_everything_origin/tools/check_growth_1019.py entry --anchor-receipt "C:\Users\1\AppData\Local\xenoamess_stellaries_dev\artifacts\1019-implementation\runs\20261019T112808Z\growth4base.native-save.json" --prefix growth4
```

完成采集后离线验收（补充样本可暂不传，此时总状态INCOMPLETE）：

```powershell
py eat_everything_origin/tools/check_growth_1019.py report --receipt "C:\Users\1\AppData\Local\xenoamess_stellaries_dev\artifacts\1019-implementation\runs\20261019T112808Z\growth4-growth-receipt.json" --repeat-receipt "C:\Users\1\AppData\Local\xenoamess_stellaries_dev\artifacts\1019-implementation\runs\20261019T112808Z\growth4repeat.native-save.json" --reload-receipt "C:\Users\1\AppData\Local\xenoamess_stellaries_dev\artifacts\1019-implementation\runs\20261019T112808Z\growth4reload.native-save.json" --budget-first-receipt "C:\Users\1\AppData\Local\xenoamess_stellaries_dev\artifacts\1019-implementation\runs\20261019T112808Z\growth4budget1.native-save.json" --budget-second-receipt "C:\Users\1\AppData\Local\xenoamess_stellaries_dev\artifacts\1019-implementation\runs\20261019T112808Z\growth4budget2.native-save.json" --output "D:\workspace\xenoamess_stellaries_dev\eat_everything_origin\docs\evidence\1019-analysis\rc4-growth-report-v1.json"
```

## 追加：优先实际月度自动补差，减少一次UI保存

主线程最新安排以更强的自动路径取代前述步骤5的默认手动第二次sync，但保留此前设计历史：C10000／R200同日设C20500并sync一次，立即原生UI保存first，确证R400／P10；之后只执行一次 `fast_forward 30`，不手动再次sync，在下个月1日取得原生autosave、归档原ZIP并写单条receipt（至少date／sha256／archived，保留输入与GPU／OCR）。第二份应R410／P0、六tier总增量10，从而覆盖真实跨月补差；此时新补的10层可能尚未完成触发修正刷新，因此只验计数，不用刚到月初的属性判核心失败。

reporter的 `--budget-second-receipt` 接受这种单条auto receipt，不要求written_at／history。默认 `--budget-second-mode monthly`，固定要求第二份根日期等于first的下个月1日；不把同日第二份自动解释成月度。仅明确另外测试手动路径时传 `--budget-second-mode manual` 并要求同日。报告保存所选路径、两份原始receipt引用与SHA；原生下一月保存和输入证据共同解释自动调度，不能把手动sync后过月的结果冒充本计划自动路径。前述示例第二个参数可直接换成 `growth4budget-auto.receipt.json`，不额外增加UI保存。

## 实施与离线验证结果

已实施collector目录修正与独立 `check_growth_1019.py`（entry／report）及测试，未修改生产Mod或既有helper。合计21项离线测试通过：collector12项覆盖两目录分离、原written_at文件已移走、显式reload目录、year1日历、原生fmm00结构与失败保留；reporter9项覆盖原生槽位／计数、独立固定数值例、400／10与410／0、monthly与manual日期不能互换、只含date／sha256／archived的auto receipt、幂等业务与严格全档区分、缺导出／错误数值和报告防覆盖。首轮固定算术测试曾把93960+1500000+60000的预期误写为1713960，已纠正为1653960；生产系数未改，也没有读取未来SAV拟合。

只读重新运行真实RC3 fmm00 collector dry-run成功，默认目录现为其真实UI写入目录 `eep03_-1033273808`，而非history；该检查未创建采集输出。对现有RC4 run112808的实际copied包完整59文件与原manifest比较、新静态报告／两共享载入来源门禁、原生来源与六个成长源文件SHA均检查成功，`runtime_1019`未导入。entry尚未对未来year1 anchor执行；九节点原生矩阵与补充SAV尚未产生，本次未生成任何成长运行时PASS报告，也未操作UI或直接提交。

报告还将原始计划独立核到anchor日历和九个固定C序列，逐条核实际命令／console frame SHA、HUD GPU SHA与OCR真实日期，再以原ZIP CRC／SHA／根日期计算检查，避免仅信任采集器自报状态。三防与导出数值（含repeat／reload）使用预先固定绝对0.01、相对0；所有账本和槽位离散字段仍精确比较。若六类中有一类仍未抽到非零层，整套状态保持INCOMPLETE并列出覆盖缺口。

## 发布门禁固定摘要合同

在未来RNG样本产生前，补充原生状态直接推导的摘要供发布门禁引用，不手填属性结果：`component_attribution_contract=source_separated_native_rng_v1`、`run_id`、`production_tree_sha256`、`C0_baseline`（C／L／六tier0、actual_native_intercept、十modifier实际导出、三个native最大值、原SAV路径／SHA／日期与诊断输入日）、`final_native_tiers`（六kind实际层数）及既有coverage／source_models／matrix。三防截距字段采用真实原生键，不把普通伤害小计写成实际截距。

新增 `ordinary_controls` 范围，要求C0至少有一艘同国普通舰，其身份集合与最大舰体／装甲／护盾在全部十八原生快照中保持；缺失或差异使普通舰范围失败，不再用空集合声称负对照。未导出普通舰D／tracking／regen，故该范围明确只限三防；其他频道的组件归属由真实装备与冻结的bound-Mother trigger源码及母舰实际增量共同说明，不伪称已导出普通舰全十频道。发布case须把本报告作为分析证据并校验SHA，不能只手填六个布尔值替代原始tier与C0截距。

普通舰三个最大值各须至少一项真实正数观测；仅有缺失字段或全零该频道，不能证明其没有变化。对应覆盖写 `native_maximum_channel_coverage`，每个频道都必须为true且参与普通舰范围检查。
