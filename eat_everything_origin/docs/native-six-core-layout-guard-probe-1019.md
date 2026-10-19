# 当前设计六核心检测：原生重复调用探针

## 目标、范围与方案（先于执行）

RC5 首次自动加载将旧母舰换成新设计，但第二次加载又回旧设计。`eep_mothership_layout_1019` 唯一出现于根 flags，不在引用 design 的原始块中；不推断闭源旗标内部机制。当前暂停于 2200.01.01，原生 `r5preload1` 为 before：fleet128 / ship1008 / mobile base15，ship implementation1608，旧设计无六核心。原 `1e-6` 损伤政策及 RC5 重载 FAIL 保留。

在这个独立功能分支，仅对已绑定舰队的原船执行条件：当前 `ship_growth_stage` 没有同时具备六个 `EEP_ADAPTIVE_{SHIELD,ARMOR,HULL,DAMAGE,TRACKING,REGEN}_CORE` 时，调用原生 `set_ship_design={design=NAME_EEP_Baiqi_Mothership_1019}`。不用 designflag，不创建船或设计、不写变量、不补资源、不初始化或发随机奖励。六核心均检查当前实际 design 的成长阶段，不采用实体 section 或历史 shipflag 代替。

先原生保存 `r5coreguard1`，再次执行完全相同命令后保存 `r5coreguard2`，保持同日暂停。第一次要求实际 implementation 完整换到 50 槽／6 required／六真实核心；第二次要求正确配置能跳过 setter，三防 current/max、完整设计形状、所有身份／位置／队列、资源、人口、布局及 EEP 账本精确不变。两次操作的 action、GPU/OCR、native receipt 和 SAV 均保留。星基地旧缓存不作为已修复，第一步损伤差异继续如实列出，不借重复幂等通过覆盖旧损伤政策 FAIL。

该探针若通过，只证明当前检测与重复跳过；下一候选仍须重新冻结、open_kaishek、独立进程，以及真实读档回调、付费队列、新局与成长回归。失败不得继续声称此 guard 有效。

## 独立实际结果

`r5coreguard1` 与 `r5coreguard2` 均为2200.01.01，各有独立原生保存动作/审计/回执，SAV 字节 SHA256 相同：`44ebd953fa66ffb2a891db6e24bbe7a38f57ccb8024699a8de116e6aa120562e`；gamestate SHA256 同为 `ff60c841fdde4d77be1d1d2923e81455bebcf6f52f475237c4e2469727bfccce`。两次实际提交的 guard 命令文本完全相同。

第一次确实将 ship1008 指向新1592，50槽/6required/六个真实核心齐全；H92960/93960、A44566.34925/44787.6、S69177.6657/167310。第二次保存的完整 ship/base/raw、实际设计形状、所有 current/max、身份/位置/队列/库存/人口/岗位/布局/全部 country 和 fleet 变量都精确相同，严格比较零差异。原生 SAV 本身字节相同提供了额外的完整状态一致证据。base15 仍旧1608，未声称修复独立缓存。

新 [rc5-six-core-layout-guard-report-v1.json](evidence/1019-analysis/rc5-six-core-layout-guard-report-v1.json) SHA256 `e64b36b8e5f801284ba9e3fd0851d4d11d2c44816925ca3c44f22fcfa2397d02`，限定26项检查全部为真，PASS_SCOPED。首次安装保留严格29项差异、再次调用0项；首次设置的装甲比例变化及全部原损伤政策 FAIL 仍独立保留。此结果只支持这条当前六核心 guard 的重复幂等性，不证明尚未冻结新候选的自动读档恢复。

## RC6 静态门禁结果

修订后的 59 文件包已冻结为 `0.4.0-rc.6`，树 `cc181c8a27ede295e9fcebeffc5e10bb75e9cd643edec1d194b928993ffab33a`。open_kaishek 实际返回 PASS：36/36 P 脚本、12 DDS、131 键 × 10 语言。完整冻结源码、原始报告、gate 及逐文件索引保存在[RC6 静态证据](evidence/1019-rc6-static/source-index.json)。当前进程仍是 RC5；静态通过不代替 RC6 新进程的真实加载、损伤与队列验收。非中文仅静态校验通过，运行时不在范围内。
