# RC7 护栏分支最短执行卡

## 目标、范围与验收

本卡只读整理已核的selector review、原39条postfire计划、RC6执行map与独立`empty_planet_selector_v2_1020`修复，给主线程提供既有命令的最短顺序和same-date idle/fired收件要求。本线程不执行游戏/UI/Steam/Git，不改Mod、工具、旧命令源、旧fixture或存档，也不读取当前run未来raw。所有未由主线程实际交付的本轮guard结论均PENDING。

验收是每条推荐命令能准确回溯现有路径/ID/SHA，空物理星选择器必须使用已静态验收的v2替换片段；原有有效性和invalid checks不删减。明确九持久目标可共享的三SAV、colonizing/ground共享的独立三SAV、实际核心迁移与核心失主的独立最小路径；不额外逐目标保存，不把失败构造或缺目标当拒绝成功，不把跨日自然变化混进same-date比较。

数字ID只作为已sealed `r7pkbase` 的历史候选依据，未来实际绑定一律从新的receipt/SAV取type明确的target；system ID、colony ID与physical planet ID不得混用。当前普通吞噬与所有后续guard样本由主线程独占，本文不预读或预测其实际对象。

## 先选对既有命令版本

三份命令资产不修改：

| 代号 | 路径 | SHA256 |
| --- | --- | --- |
| O | [原39条](../testing/colossus_1019_postfire_plan.json) | `76adabaf82dc2c10894222bdb425ee1b994307233e1bccb2c251bdf2f07325c8` |
| M | [RC6 map补充16条](../testing/colossus_1019_rc6_execution_map.json) | `c9b81e616bc3bc2b79c240f8889fe668d296e5035c80b4cbcb7a9ba18f935650` |
| V | [空物理星选择器v2](../testing/empty_planet_selector_v2_1020/commands-v2.json) | `7b90bc9d247b119f4ac66aac6771236b3cea64402defd95324bd5ffe2c38a99d` |

V中同ID优先覆盖O/M，不能把三份直接拼接后再按ID选首条。可在[既有Send-R7Effect入口](rc7-functional-next-execution-1020.md)定义前，只替换其`$R7Rows`装载为以下内容；不新建工具或执行器：

```powershell
$R7Old = Get-Content -LiteralPath 'eat_everything_origin/testing/colossus_1019_postfire_plan.json' -Raw -Encoding UTF8 | ConvertFrom-Json
$R7Map = Get-Content -LiteralPath 'eat_everything_origin/testing/colossus_1019_rc6_execution_map.json' -Raw -Encoding UTF8 | ConvertFrom-Json
$R7V2 = Get-Content -LiteralPath 'eat_everything_origin/testing/empty_planet_selector_v2_1020/commands-v2.json' -Raw -Encoding UTF8 | ConvertFrom-Json
$R7V2Ids = @($R7V2.commands.id)
$R7Rows = @((@($R7Old.commands) + @($R7Map.commands)) | Where-Object { $_.id -cnotin $R7V2Ids }) + @($R7V2.commands)
```

实际命令仍按原样单个参数送现有`runtime_1019.py console-open`；每段stage/output使用新名，结束后按既有console关闭流程保存。O/M的历史run/tree/旧绝对C19/G19和旧物理ID不能带入。

V只把未殖民选择器中`is_under_colonization = no`改为`NOT = { is_under_colonization = yes }`。本机4.5.2已观测空物理planet前者不通过，后者通过；[v2修复依据](rc7-empty-planet-colonization-selector-v2-1020.md)保留原失败，不能泛化所有布尔trigger。**尤其`r6_uncolonized_bind`和`r6_uncolonized_dispatch`都取V**，只修bind会让旧dispatch停在派发前。`colonizing_reserve_split/start_split`、七条batch setup也取V；已殖民neutral/ground/core串保持原文。

已核V16条均为原串唯一指定片段替换；本卡推荐的所有命令都小于1000字符，最长`core_owner_loss_dispatch`936。V现有Kaishek报告为静态PASS（SHA `912613768f10d5fcacddc36c79620ff83b9e10923305fafeee10d8d8fe7b4b7c`），不是原生构造成功。不要输入旧`batch_inspect`2539、`colonizing_setup`1279/1290、`ground_setup`1544字符长串；使用下面既有split步骤和原SAV检查。

## 统一的三SAV对照：所有支路相同

1. 所有构造/转手完成且指定无效状态真实成立后，暂停原生保存 **R ready**。读取精确native-save receipt/audit/SAV，确认实际ID与前提。
2. R上只推进1日，保存 **I idle**，核该无效状态仍成立。若状态已消失或地战结束，停止此分支，保留夹具未建立事实。
3. **真实Load同一个R**，派发该分支已有完成负例串（THIS实际planet，FROM实际唯一Mother fleet）；所有guard状态保持，不清flag、不重建对象。推进同样1日，保存 **F fired**。
4. 只用 **I→F** 的同日、同一源/core运行原`no-settlement`，并附完整strict。R用来证明构造和实际reload来源，不能拿R→次日F代替同日对照。

已有角色能由同一实际SAV承担就不重存；不用逐目标造三档。若负例回调已实际处理且有同日I/F样本可复用，按真实receipt角色复用，不为文件名再操作UI。下面“ready/idle/fired”都是语义角色，建议prefix不是已存在文件或未来PASS。

## A：九持久源＋当前核心，同一组三档

**入口：真实Load已sealed的`r7pkbase`，不要用敌国已灭或home已reserved的normal完成档。** [selector review](rc7-guard-selector-readonly-review-1020.md)已核原base home有8个物理候选，足够七批；但这只是该base的原始对象依据，不能预测随机ID。原只读字段复核曾未体现空对象trigger行为，本卡已明确取V补正。

按以下ID顺序输入，不额外执行较长`batch_split_bind`：

```text
O state_guard_bind
V r6_uncolonized_bind
M r6_neutral_bind
V batch_setup_active
V batch_setup_devouring
V batch_setup_credit
V batch_setup_destroy
V batch_setup_secondary_core
V batch_setup_artificial
V batch_setup_qzero
```

`state_guard_bind`455字符提供与batch相同的actor/species别名；七setup都立即reserve并建立不同的真实殖民源。home外uncolonized和真实中立首都独立选，避免占用home七批候选。实际R必须有九个不同`type=planet`别名；七人工夹具都真实有colony/人口，各自唯一拒绝状态保留。

| 原生目标别名 | 必须在R/I/F持续成立 |
| --- | --- |
| `eep_guard_active` | 真实殖民源且`eep_active` |
| `eep_guard_devouring` | 真实殖民源且`being_devoured` |
| `eep_guard_credit` | 真实殖民源且`eep_credit_done` |
| `eep_guard_destroy` | 真实殖民源且`eep_destroy_done`，不能因此预先真毁星 |
| `eep_guard_secondary_core` | 本国非绑定源真实带`eep_core`，生产bound core另在并可用 |
| `eep_guard_artificial` | 原生类型实际满足artificial，不是同名flag |
| `eep_guard_qzero` | 原生size2和两个真实`d_lithoid_devastation`实体，effective q0，不写eep_q冒充 |
| `eep_r6_uncolonized` | home外自然digestible未殖民对象，无owner/colony/殖民过程，V派发前提真实成立 |
| `eep_r6_neutral` | 真实default非actor自然殖民首都，owner与actor不交战，目标非core/active/settled |

保存A-R→A-I，真实Load A-R后按序：

```text
O batch_dispatch
V r6_uncolonized_dispatch
M r6_neutral_dispatch
O current_bound_core_reject
```

再推进1日存A-F。`current_bound_core_reject`与其余九源共享这三档，不额外开支路；source=实际bound core、core=同一物理core时原no-settlement允许同ID，不能套用positive settlement的source≠core限制。每源分别核拒绝，不能因九源总账没动就省掉某个目标的存在/状态/实际派发证明。

## B：真实colonizing＋ground，可同批带外国secondary core

**入口：另一次真实Load `r7pkbase`。** 不沿A已占七球的夹具继续，不把本支军队混入先前“无陆军”有效发射证据。

```text
O state_guard_bind
V colonizing_reserve_split
V colonizing_start_split
O ground_bind_split
O ground_armies_split
O colonizing_inspect
O ground_inspect
```

殖民对象需原生`is_under_colonization=yes`及真实colony/进度/owner；同时记录实际`is_colony`。若它为no，只能认证真实殖民中联合拒绝，不能声称单独隔离了其中一个谓词。`start_colony`日志或同名flag不能替代真实进度。

地战目标需原敌源仍为有机owner、与actor真交战；actor已有`tech_assault_armies`。`ground_armies_split`只创建两支真实defense_army和一支machine_assault_1，**创建本身不证明地战已开始**。如需一个真实tick才能形成，先等实际双方进入ground combat再保存B-R；B-I和B-F仍须有`has_ground_combat=yes`、actor攻击方与原owner守方。提前结束/驻扎/仅占领均保留为夹具未建立，不派发或不给该guard PASS。运输＋真实登陆仅在既有直接建军路线确实失败后使用已有后备，不预先增加。

为保留A自有secondary覆盖且不另增外国core三档，可在本支B-R之前再输入：

```text
V batch_setup_secondary_core
O foreign_secondary_core_transfer
```

确认该源实际由仍活着、正交战的`eep_colossus_probe_victim`持有且`eep_core`保留，生产bound core仍是另一个本国可用核心。该setup在fresh base只取一颗未reserved home候选，不与殖民中对象重合。实际状态不冲突时，三个拒绝目标共享B三档。

保存B-R→B-I，核三种状态均仍真；实际Load B-R后：

```text
O colonizing_dispatch
O ground_dispatch
O foreign_secondary_core_reject
```

推进1日存B-F。若不合并foreign core，colonizing/ground仍用这同一组三档；外国core另需自己转手后的R/I/F，不能把转手前后owner变化塞进一个所谓同前提对照。优先合并不会删掉A自有secondary、当前bound core、后续迁移core任何覆盖。

## C：真实迁移新core，再独立失主；各三档

**入口：真实Load实际v2成功档`r7normalready2`，源仍活且恰50主体人口、未active。** 原`r7normalready`是无source的失败尝试，必须保留，不能用来迁移。主线程已明确交付ready2：5月28日（完整native日期以receipt为准），SHA256 `b3644338f5f4f82522fe2d52cb7f939bdee59458b81440e649e8a1475ea2427b`；source physical1/colony18/pop50，core physical2/colony0/pop5177。此处仅引用主线程交付事实，不另读该分支raw；精确来源由functional_intake及后续canonical接收绑定。实际执行仍按新receipt的type明确targets取ID。不用已经吞噬完成或normal-start档；旧核心仍有人是本路径现成保命备份，不需另造殖民地。

```text
O migration_bind_physical_refs
真实原生决议 decision_eep_migrate_core（迁移王座至此）
O migration_inspect
```

迁移后新绑定与人口/标记/容量正确才保存C-R；迁移前直接复用已存在normalready2作身份/经济基线，不额外保存“bind前”副本。C-R→C-I；真实Load C-R→`O migrated_bound_core_reject`→FF1→C-F，验证新bound core完成时也拒绝。

随后在仍正确迁移的状态执行：

```text
O core_owner_loss_bind_receiver
O core_owner_loss_apply
O core_owner_loss_inspect
```

receiver必须从实际仍活default非actor国家取，不写死已可能灭亡的country1。确认EEP绑定仍指新物理core，但owner已变receiver；old core仍owner0、有真实人口、无EEP core标记，actor保留`eep_initialized`且core_available=no。此时保存D-R→D-I；真实Load D-R→`O core_owner_loss_dispatch`→FF1→D-F。

失主dispatch的THIS是**旧core这个现已普通的本国源**，FROM仍Mother；`core_world`必须填当前EEP实际绑定的外国new core，而非原生自动选回的capital。它证明完成时重新检查受益核心owner，不是只重测source带core标记。必须到D-I/D-F仍保持这些前提；若EEP实际重绑/目标丢失/初始化状态改变，先保留事实，不能由无收益给owner重校验PASS。

上述最小合并共A/B/C/D四组三档（12份角色SAV）；所有真实已有同角色保存可直接复用。只有构造/状态实际不成立才分拆失败项，不给每颗星再造before/after或重启进程。

## 原生字段和离线判据

| 范围 | 必留原生事实 |
| --- | --- |
| 来源 | 精确native-save/auto receipt角色、SAV/audit/gamestate SHA、实际date/run/manifest/tree/EXE/中文；Load实际来源receipt；原始命令/Enter/派发marker，不把NOT_READY或missing目标当派发 |
| 全局身份 | `event_targets`中name/type/id；`eep_mothership0`→实际fleet→ship；`eep_core0`→当前physical；所有guard/source/old/new/receiver别名。`coordinate.origin`是system，country.capital是colony ID，各自另记 |
| source/core | `planets.<physical>`完整native owner/controller/class/size/colony/flags/variables；相应colony的原始块、实际pop_groups/jobs与总人口、实体deposits type计数、core容量modifier/d_eep_core。七批先证有colony/人口，空星先证真无colony；两者不是同一种省略 |
| 殖民中/地战 | planet/colony原始殖民状态/进度/owner/species；`ground_combat`完整原始对象和关联`army`的owner/species/type/planet及真实双方。实际成员键以本次SAV为准，不凭命名猜造；原生inspect的布尔结果与对象联合核对 |
| 外交/核心失主 | 原生war participants与owner实际国家；old/new physical标记/deposit/容量、EEP生产绑定、旧核心population>0、actor flags、receiver存活、实际capital与EEP绑定分别读 |
| 无奖励 | C/G/D/made/worlds及last三项、L/next、B/R/P与六country/fleet tiers、唯一growthmodifier；core实际人口/容量、源原class/colony/once receipts；独立`crisobj_destroy_worlds`与`crisobj_destroy_empires`progress，不用总menace替代 |

对每个目标的I/F建现有no-settlement case，填实际`before/after/source_world/core_world`。该负例函数不需要positive settlement的q/R/单位奖励预期；它要求同日，直接比较原生危机raw和原五账本，内含完整strict。

```powershell
python -B eat_everything_origin/tools/check_1019.py --output '<新观察.json>' observe '<实际I或F.sav>' --world <实际source> --world <实际bound-core>
python -B eat_everything_origin/tools/check_1019.py --output '<新同日负例报告.json>' no-settlement '<填实case.json>'
```

已有receiver也可用一份intake的world_ids=全部实际source/core union，各SAV只完整解析一次，再为每源设no-settlement task。仅角色/输入/receipt已固定后离线接收，不自动发现未来raw；receiver状态不是最终guard PASS。原checker/inspector仍为681836/1ec3ad SHA，不修改任何函数或忽略路径。

完整strict及全部差异始终保留；同日无二次结算PASS不等于全档PASS。只有每种invalid前提真实持续、THIS/FROM正确、完成回调确实派发且原生无收益/未毁源时，才分别提案对应`colossus_guards`字段。colonizing、ground、任意core与owner-loss各缺一项即保留PENDING，不能由总账零差或其它目标成功补齐。

原no-settlement的top checks只直接覆盖五账本、core人口/容量、源class/colony/receipts及crisis raw；L/next、B/R/P和六tier仍须读实际变量作独立补充检查。不能只看其top PASS而跳过这些growth/随机奖励不变量，亦不能把嵌套strict的变化删掉。

## 本卡只读核查结果

本次只读取上述固定文档/命令资产/冻结RC7 trigger与既有checker源；没有读当前normal/guard未来raw。已核V16条均仅一个指定替换，所有推荐ID唯一，顺序存在且小于1000字符，旧O/M SHA保持原样。产物仅本文；所有实际构造、dispatch与guard结果仍PENDING，不生成新fixture、模板、报告PASS或final-result。
