# 吞噬之心 0.4.0-rc.7 假期交接（2026-10-20）

## 当前决定与现场

用户最新要求是“平稳收尾手上的每件事，不用太急。梳理交接文档到docs中”。因此本轮在已有操作结束后停止实机和发布，不再自动继续后续测试。原先“修改、测试、发布”的目标保留为待恢复工作，**本轮没有发布 0.4.0，也没有宣告整体验收完成**。

- 工作仓库：`D:\workspace\xenoamess_stellaries_dev`，子项目 `eat_everything_origin`，分支 `main` 跟踪 `origin/main`。
- 当前版本源：[VERSION](../eat_everything_origin/VERSION) 为 `0.4.0-rc.7`；[descriptor.mod](../eat_everything_origin/mod/descriptor.mod) 同版，兼容范围为 `supported_version="4.5.2"`。恢复时须重新核对，不能把 RC 上传公开工坊。
- RC7 生产包共 59 文件，树 SHA256：`61b34f6dbdc277c44364889d5f1e1cd2773a4624786bbf0d538079fc6ba4feb0`。
- 游戏 EXE SHA256：`400df27c82ddc845aa9dce79bd468d81f18f060d299cd263e3afa93aef4f7a83`。所有本轮实机为简体中文、单生产 Mod。
- 最后 run：`20261019T164112Z`，PID `37300`；北京时间 **2026-10-20 04:00:25** 正常退出，`forced=false`、`running_after=false`。未留下继续推进日期的游戏进程。
- 19 份完整日志已在停机后冻结，共 `5,977,753` 字节；冻结与字节校验不等于最终日志验收通过。日志警告、失败尝试及完整 strict 差异均保留。
- Steam 持久配置的 `WantsOfflineMode=1` 已只读核对；收尾没有切换在线、上传或改动远端内容。该配置记录不冒充实时联网检测。

停机原件与校验见 [停机说明](../eat_everything_origin/docs/rc7-vacation-stopped-run-1020.md) 和 [封包](../eat_everything_origin/docs/evidence/1020-rc7-vacation-stopped-run-v1/)。当前收尾不涉及 `open_kaishek` 或 CK3 仓库修改；新确认的空星谓词差异是 Stellaris 4.5.2 特有实测，未推广成 Paradox 通用规则。`open_kaishek` 现有HEAD为 `9a286b9321a4d1ecacc0680a8bb0d914e0679b99`，工作区干净，与跟踪远端无领先／落后。

收尾另修复了三组本轮测试夹具的 Git 原字节保全：关闭这三目录的换行转换，重新暂存原始字节，13文件全部与暂存blob一致；原SHA和夹具正文不变。否则新检出会因CRLF→LF破坏封包引用。见 [设计与校验](../eat_everything_origin/docs/rc7-fixture-byte-preservation-closeout-1020.md)。生产59文件树未改。

停机日志初查另发现 **03:45:39 `events/nomads_events_1.txt:2268` 的 `Invalid context switch [from]`**（country0、from无效）。归因尚未完成，恢复后须核源码与实际触发链，不能先称为已知夹具噪声或宣称生产日志无错误。原绑定输入解析错误、原生无owner物理星改机器世界时的timeline告警及无效deposit清理也保留在完整原始日志中，逐项分类见停机封包。

## 用户需求与已实现行为

原始范围见 [1019 需求](../eat_everything_origin/docs/requirements-2026-10-19.md)。实现已在 RC7 中，剩余工作主要是补齐实机证据、旧档迁移和正式发布：

1. 新开局删除额外殖民地，保留蜂巢／机械／合格普通政体对应母星。旧档已有殖民地不删除。
2. 修复开局母星布局和就业，避免只删除赠品球后仍然负电。
3. 母舰对齐原版遗迹级无畏舰的 43 个共同武器／防御配置，保留母舰优势；具备真实跃迁引擎和对应最高推进器。
4. `L=floor(C/10)`，每级伤害、舰体、装甲、护盾各增加 5 个百分点，同类修正加算；没有预设等级上限。
5. 每 5 级随机升级一个实际装备的共生核心。方案已做到 **六个原生 AUX 组件及其动态触发修正**，并非把船体外加成冒称装备。层数永久累计；单次最多处理 200 次补奖，积压持久化并在后续同步／月度处理。
6. 原生巨像“拆解星球”武器与普通吞噬共用结算，包括有效物质量、人口回收、母星容量和防重复记录；无需登陆陆军。

旧母舰的原生移动基地／船坞缓存仍有兼容限制，不能承诺旧档立刻得到新缓存；多人即时加载修复未完成实测。发布文案须保留这些边界。

## 已完成的验证

下表是已有证据范围，不表示 18 个发布用例全部通过。

| 范围 | 已核结果与证据入口 |
| --- | --- |
| RC7 静态前置 | `open_kaishek` 检查通过：36 个 P 脚本、12 个 DDS、131 个本地化键 × 10 语言；见 [静态报告](../eat_everything_origin/docs/evidence/1019-rc7-static/candidate-rc7-open-kaishek.json)。工具报告的有限语义边界保留。 |
| 三类开局经济 | 各一局干净开局、各 12 个连续月度原生样本全部电力为正，均只有一个殖民地；见 [经济原件](../eat_everything_origin/docs/evidence/1019-rc7-economy/)。蜂巢首月／第12月约 `+23.14466/+30.45124`，机械 `+2.85755/+8.77273`，合格普通（净化）`+46.23969/+46.75291`。不能推广为全部政体组合均已验收。 |
| 重复初始化 | 实际重复完整初始化／启动／同步，没有多送星球、母舰或收益；见 [初始化封包](../eat_everything_origin/docs/evidence/1020-rc7-repeat-initialization-v1/)。 |
| 母舰与原版参照 | 同国 C0 实际配置比较：母舰 H93960／A44787／S167310，参照 H20000／A30740／S138352；六核心及完整原生槽位已核。维护费仍为正，不得宣传免维护。见 [配置封包](../eat_everything_origin/docs/evidence/1020-rc7-relic-configuration-v1/)。 |
| 真正跃迁 | 原生 14 天跃迁、舰队身份不变及 200 天冷却界面已核；见 [跃迁封包](../eat_everything_origin/docs/evidence/1020-rc7-native-jump-v1/)。 |
| 无限成长／随机组件 | C0～10000 的九节点、18 原生档及 1850 项检查；另有 C20500、L2050、410 次随机强化与积压补发的实际档和 UI。高等级仍有真实六核心和十船坞配置。见 [成长原件](../eat_everything_origin/docs/evidence/1019-rc7-growth-v1/) 与 [高等级 UI](../eat_everything_origin/docs/evidence/1020-rc7-high-level-ui-v1/)。自然受伤恢复、死亡不再生及普通舰完整十 getter 负对照仍欠。 |
| 敌方巨像完整射击 | 实际 90 天充能／30 天发射、取消／重载取消、自然摧毁敌星、无陆军、稳定结算、重复及真实重载防重复已核。原结算稳定25项／含重载26项通过；两段幂等各9项通过。危机世界750、灭国600独立校准，敌舰积分单独计。见 [敌星完成接收](../eat_everything_origin/docs/rc7-pk-enemy-completion-reception-1020.md)。首个 immediate 两项失败和重载 strict47项差异原样保留。 |
| 旧档输入准备 | 两份真实旧伤档已原字节导入隔离目录，哈希和唯一性核实；**RC7 原生迁移尚未运行**。见 [导入复核](../eat_everything_origin/docs/rc7-migration-input-import-review-1020.md)。 |

非中文九语言只能表述为“静态校验通过”；运行时不在范围内。原已停止的噬岩者自然战役继续保持停止，不因恢复本批任务而重启。

## 最后恢复锚点：普通吞噬尚未完成回调

外部原始目录必须保留，不能清理后只剩 Git 中的摘要：

```text
artifact:
C:\Users\1\AppData\Local\xenoamess_stellaries_dev\artifacts\1019-implementation\runs\20261019T164112Z
isolated userdir:
C:\Users\1\AppData\Local\xenoamess_stellaries_dev\runs\20261019T164112Z
```

**恢复时首先使用 `r7normalprecomplete3.sav`，不要加载人口控制支继续正例。** 对应 `.native-save.json` 保留 `history` 原生路径；canonical 副本与接收报告见 [普通吞噬封包](../eat_everything_origin/docs/evidence/1020-rc7-normal-native-v1/)。

| 原生档 | 日期与 SHA256 | 用途 |
| --- | --- | --- |
| `r7normalprecomplete3` | 2201.10.01；`0c872e2efdd2329ae021466955cc0fe1ab4813bf0b0c8233f011706bf8615772` | 最后**无测试阻断旗**自然档。source物理1／colony18／owner0，pc_machine、size2、founder112；core物理2／colony0／owner0，人口5150。Situation16777231，target1，原生progress5、尚未killed；source q2、T5、cached progress1，无destroy_done/pending。C21/G21/D7/made300/worlds1/L2，六核心层数0。未推进真实10月2日完成。 |
| `r7normalprecomplete2` | 2201.09.30；`640ac4bfbed583ccf895471beb737bc68c4bde1e27a47f0a346d52bb2428af5c` | 独立对照与自然支共同加载输入；Situation4，source110／core5145。 |
| `r7normalcontrol` | 2201.10.01；`a7106e91515e3b552ae5fe2d7c6ab265fdbbbb15c47b7ab8670b7da251b067ce` | 仅注入source `eep_destroy_done` 的人口控制；source112／core5150，Situation5。月界自然增量 source2、core5，账本无变化。不是正例完成。 |
| `r7normalcontrol2` | 2201.10.02；`66c0ad74de664da133eb8ebfa538cd02a1f5dcae9cc361050fe7e97fd75bb1a8` | 控制支原生回调已到，Situation有killed=yes，source仍活、人口112／core5150。证明此对照10月1→2日无额外人口增长；不得拿它冒充自然结算或guard整体验收。 |
| `r7normalready2` | 2201.05.28；`b3644338f5f4f82522fe2d52cb7f939bdee59458b81440e649e8a1475ea2427b` | 50人口的有效源，core5177，尚未启动任务；后续核心迁移测试须恢复此档。 |

决议原生输入已证明：source50→100、core5177→5127，50人口真实迁移且总量守恒，q2/T5/seed_need0；同一任务的真实进度为开始0→6月28日1→9月28日4→10月1日5。source上的 `eep_progress=1` 是缓存，不得改写为原生 Situation 的5。

恢复后，先真实加载最后锚点并另存新的原生档，核对身份、无阻断旗、人口、ledger与新run来源，再事前固定下一日结算预期。当前独立对照支持候选 R112、other_core_pop_delta0，即无制造时 core5262；但仍须以新加载后的真实 founder groups 核实。预期 C23/G23/D7/made300/L2、容量增量0、世界积分增量750／灭国0。**这些是待实际验证的预期，不是通过结果。** 随后自然推进、保存 immediate／必要stable，运行原 settlement，再做重复回调和实际重载防重复。不能手调progress或手动调用完成。

必须保留的失败／经验：

- 旧 `r7normalready` 无目标别名，不能当有效ready；旧 `r7normalprecomplete`（10月27日，SHA `796eb00c6c7fbb84c6863923c9b3979d45dd506d2dd48dd3f9710b15f2d41dfb`）已经完成，不能当before。读取其 Situation 时的KeyError发生在写预期之前，没有伪造pre期望或回执。
- 原生任务按月度脉冲更新，完成回调存在处理窗口，不能把T5硬套为150天。现有m01／m04采样合同未要求m02／m03，不需重跑三类全年矩阵。
- 空物理星上 `is_under_colonization=no` 与 `NOT={is_under_colonization=yes}` 的实际结果不同；已做纯log对照并修复**测试夹具**。恢复guard/Li必须用 [v2命令覆盖](../eat_everything_origin/testing/empty_planet_selector_v2_1020/commands-v2.json)，尤其uncolonized的bind和dispatch都要覆盖。生产两处先要求is_colony=yes，RC7包未因此修改。
- 独立人口控制只加 `eep_destroy_done`，不是 `eep_credit_done`。后者只跳积分段，仍可能转移人口与摧毁源。见 [控制设计](../eat_everything_origin/docs/rc7-normal-independent-population-control-1020.md)。

## 待恢复工作与执行入口

完整原check逐项映射见 [原46项与可共用分支](../eat_everything_origin/docs/rc7-remaining-check-branch-map-1020.md)。该卡按本次seed封口前的92true／46null编制；seed已在收尾补齐，当前余45null，普通吞噬余其余3项。不要为恢复而重做已经封口的经济矩阵、敌星射击、取消或高等级真实跃迁。

1. 核对收尾封包、最新索引与最后自然档；建立**新的隔离run／新PID**，不覆盖已冻结run，不启动已停止自然战役。继续上述普通吞噬自然结算与幂等。
2. [Guard执行卡](../eat_everything_origin/docs/rc7-guard-minimal-execution-card-1020.md) 定义四组三档：九持久无效源＋当前core、殖民中／地战／外国secondary core、真实迁移core、core失主。必须同日idle→fired；不能把缺目标当拒绝成功。迁移入口是成功的ready2。另见 [接收规则](../eat_everything_origin/docs/rc7-guard-native-reception-1020.md)。
3. [成长余项最短顺序](../eat_everything_origin/docs/rc7-growth-remaining-execution-order-1020.md)：同银河普通舰十getter负对照→高等级自然受伤恢复→直接接真实死亡、月脉冲及已毁档重载不复活。死亡after不能调用要求活Mother的growth reader。
4. 独立Lithoid预设干净首月及已有损耗的自有非core原生PK。一条真实射击链可共用owned-return／native-G0／loss等证据，不需Machine再打一颗自有星。保持随机原生吞岩奖励与Mod制造人口分开计。
5. [旧档迁移与跨进程重启](../eat_everything_origin/docs/rc7-migration-restart-execution-1020.md)：public031和paid11两旧伤档实际load／重复修复／reload；高C积压持久与自动补奖；非零成功结算账本的进程重启后幂等。迁移严格 `damage_preserved=false` 的原义及v2数值预算必须保留，不能为追求全部true篡改旧FAIL。
6. 新run正常停机，独立审核两run完整日志，归档后完成原typed合同。现有停机日志只有保全和初步分类，不能自动把最终日志门槛补为true。

准备新隔离run可复用现有入口（仓库根、**仅在用户恢复任务后执行**）：

```powershell
.venv/Scripts/python.exe -B eat_everything_origin/tools/runtime_1019.py prepare-single candidate-rc7 'C:\Users\1\AppData\Local\xenoamess_stellaries_dev\artifacts\1019-implementation\runs\20261019T164112Z\r7normalprecomplete3.sav'
.venv/Scripts/python.exe -B eat_everything_origin/tools/runtime_1019.py launch --timeout 180
```

必须核新manifest/tree/profile/language及唯一seed来源，实际load后原生另存，不用仅有manifest证明重启。游戏窗口若被锁定需先解决可交互桌面；鼠标在角落时可由主线程移到中间，不再要求用户代移。仅主线程操作游戏桌面，离线读件／分析可并行。

## 索引、发布和文件边界

当前索引为 **93 true／45 null，18组及组件全部PENDING**。本次只新增普通吞噬的 `normal_seed_preserved=true`，自然完成、最终耗时和重载幂等其余3项仍null。以 [pending索引](../eat_everything_origin/docs/evidence/1019-requirements/rc7-runtime-progress-v1.pending.json) 和 [装配说明](../eat_everything_origin/docs/rc7-index-assembly-1020.md) 的最终封口内容为准；不使用百分比替代验收结果，也不创建伪final-result。

在子项目目录查看欠项：

```powershell
python -B tools/runtime_index_1019.py --index docs/evidence/1019-requirements/rc7-runtime-progress-v1.pending.json missing
```

发布草稿见 [0.4.0文案](../eat_everything_origin/docs/release-0.4.0-notes-draft-1019.md)、[发布准备](../eat_everything_origin/docs/rc7-release-copy-preparation-1020.md) 与 [六图提案v3](../eat_everything_origin/docs/evidence/1019-requirements/images-manifest-0.4.0-proposed-20261020-v3.json)。这些均未发布；历史1015图和高等级压力测试图的标注不得删掉。

实际发布仍须：全部所需验收有依据→更新正式VERSION/descriptor及六类别CHANGELOG→同版本 `[v0.4.0]` Change Note／文案／图库→正式静态检查与提交推送→上传自有物品 **3815707212**→远端内容及图片逐项核验→最后创建并推送 `v0.4.0` 标签，再恢复Steam离线。上游 **3710613857只读，禁止上传覆盖**。本轮未执行这一串操作，也未创建正式标签。

`docs/evidence/1019-rc7-purifier-economy-worker-ui-v1/` 是此前未执行worker的遗留准备目录，不是全年PASS证据；本次不提交、不删除、不冒用。未来所有stage/输出名独占创建，失败原件、raw日志、SAV、OCR和回执不得修改。只提交本任务文件，不覆盖用户其他改动。
