# RC4 phase-A 正常退出后的全日志冻结方案

## 目标、范围与当前状态

本文件先记录执行前方案，现已按 root 正常退出信号完成。准备时 jump worker50773 仍在运行，因此当时没有复制活动 logs；root 后确认 PID36644 于 UTC `2026-10-19T13:04:30.124487+00:00` 正常退出。本线程核实原始停止证明与源进程已不存在后才冻结，不启动／停止进程、不操作 UI。

指定来源为 run `20261019T112808Z`、原始游戏 PID36644，简体中文 `l_simp_chinese`，RC4 copied tree SHA256 `06485dc540a88b30cef15c27c323ff21cd88f04ad57b79e4f5bc0590937ef468`。EXE SHA256 为 `400df27c82ddc845aa9dce79bd468d81f18f060d299cd263e3afa93aef4f7a83`。日志来源：

```text
C:\Users\1\AppData\Local\xenoamess_stellaries_dev\runs\20261019T112808Z\logs
```

运行证明来源：

```text
C:\Users\1\AppData\Local\xenoamess_stellaries_dev\artifacts\1019-implementation\runs\20261019T112808Z
```

目标为新目录 `docs/evidence/1019-rc4-phase-a-final-logs/`：仅复制退出后源 logs 的全部文件（包括全部 script_documentation）与同 run 的 manifest／process／stop 三份原始证明。原字节保存，不复制 SAV、59 个 Mod 文件、其它 run、旧 public031 profile 或后续 RC4 process 的日志。当前 run 不重用日志路径；旧版受伤夹具生成和后续迁移／经济／成长另属独立 profile／run，不能拼入此目录。

## 复用既有 canonical 来源

本归档引用 [RC4 v3 阶段索引](evidence/1019-rc4-pk2-duration/archive-index-v3.json) 与 [v3 独立复核](evidence/1019-rc4-pk2-duration/archive-verification-v3.json)，不重复归档 Mod 源码：

| 既有证据 | SHA256 |
| --- | --- |
| `1019-rc4-pk2-duration/archive-index-v3.json` | `1b371ae6e6c33bc1841af895bb94bb7e037d0a7b7da20bd689045d70e7afaf64` |
| `1019-rc4-pk2-duration/manifest.json` | `a83c605727f30a1d68db0e076348d814824d8ca56020ca2ab8864db8194f44f1` |
| `1019-rc4-pk2-duration/source_snapshot/source-copy.json` | `4d948c9782197108c2703b89a4e65d3fc1e4636a322a9497a5ba88ca408b6a2d` |
| `1019-rc4-pk2-duration/source_snapshot/gate.json` | `731928624a2a9761f8e0754967db3b5e06c28bb7570f40921e966adb1a99fe0d` |
| `1019-rc4-pk2-duration/source_snapshot/open-kaishek.json` | `2e249c08bb39a4e30ff9d2f3eea0983a5684b328bc5018b069002df38315f20d` |

v3 只证明阶段来源和限定单次敌星实发观察，原记录的 `complete_run_freeze=false`／`release_status=PENDING` 保持历史原样。新日志冻结不得改写 v3 索引或把其局部验收扩大为整个 Mod PASS。root 原运行仍绑定原始 `2e249c…` 门禁报告，既有 [报告身份链接](evidence/1019-requirements/rc4-open-kaishek-report-link-v1.json) 不作替换。

## 正常退出后的执行与验收顺序

1. 收到 root 正常退出信号后，读取同 run `stop.json`：核对 PID36644、`forced=false`、`running_after=false` 及实际 UTC，和 `process.json` 的 EXE／参数／userdir／启动时间一致。独立只读检查该源游戏进程已不存在；如果 PID 被新进程复用，须按启动时间／命令行说明身份，不把别的进程当作源仍活跃，也不未经核实声称源已停。没有可验证的停止证明就不复制、不标 frozen。
2. 停止后首次枚举完整源 logs 文件集合，逐文件记录相对路径、原始绝对路径、字节数及 SHA256；递归包括 script_documentation。已知同版引擎通常提供 effects／localizations／modifiers／scopes／triggers 五份目录，但不得按固定文件数静默漏掉新增文件。
3. 按原字节复制 logs 全集和 manifest／process／stop。复制前后再次枚举源集合并逐文件重算 SHA256，确认集合、源字节与目标字节全部一致；复制前后再次检查源进程身份。目标目录不得有 SAV／Mod 树或其它 run 载荷。
4. 生成独立 index：绑定 run／PID／停止证明、复制 UTC、EXE／tree、全部来源／副本逐 SHA256 和原始字节数，以及上述 canonical 引用。index 只列实际复制载荷，分析与验证文件另行列明，不把计划写成完成。
5. 单独验证程序重新读取全部源和归档：检查完整文件集、全部 hashes／字节数、三份运行证明、所有 script_documentation 和禁止的额外载荷，输出独立 verify。为原始日志及三份证明设 `-text`，另核对预期 Git blob 与原字节一致，防止换行归一化。
6. 完整审阅退出后 error.log／game.log，逐条记录分类及未知项，给出精确行号和原始来源，保留完整 scope 续行。该只读 CPU 归档可与 root 后续旧 public031 profile 的操作并行；本线程绝不打开 UI、启动／停止游戏或操作 Steam，也不提交。

## 已知分类与归因边界

下列是目前已有证据支持的分类清单，不是对最终日志计数的预先裁剪。退出后若多出其它记录，全部作为新增或未知项列出。

| 分类 | 已有来源与处理要求 |
| --- | --- |
| 启动 baseline | 缺失 Workshop 路径发现警告与原生 `decision_lithoid_swarm_consume_world`／EEP consume 覆盖提示，逐字符对比既有 baseline，仅时间不同才作对应分类；仍保留原文。不能说缺失 Workshop 已启用。 |
| 错误 DISMANTLE 试验输入 | 当前阶段前缀已记录20:05:42缺失 `on_destroy_planet_with_EEP_PLANET_KILLER_DISMANTLE`。必须链接实际试验输入 receipt 并确认归属后再标操作错误，不能当生产 DEVOURER 回调缺失，也不能静默过滤；若 receipt 未找到则保留来源未归因。 |
| EEP 真实实发后的 nomads.94 | 当前 B 前缀包含20:09:31的原版 `nomads_events_1.txt:2268` 无效 from。结合真实发射 case 证据作受限时间归属；原生 ROOT country0／FROM invalid country 的原文保留，不能断言具体 C++ hook 或无害。 |
| 原版 CRACKER 对照后的 nomads.94 | 稳定 P→Q `[3200,3575)` 精确375字节、20:20:06同一错误；B→P、Q→R均空。对应原版手动完成 callback＋两日推进，显式 Mother fleet FROM。见 [独立分析](rc4-native-cracker-control-analysis-2026-10-19.md)。不冒称实际原版武器发射或90日验收。 |
| 其它／未知 | 包括后续 Relic、jump 等同 run 阶段如有的新记录，按实际退出日志逐条列明；没有来源支持的记录保持未解释，不按原生文件名自动排除。 |

当前已观察的 nomads.94 两次分别落在 EEP 实发与原版完成 callback 对照；最终仍按全日志实际条数核对。复现只支持“该 native callback 路径也可出现”，不证明 EEP 没有缺陷或错误无害。原版对照 worlds750／empires0、EEP C0、目标17碎裂／country1删除／历史 colony 缓存的事实保持原报告边界，不替换为预期600。

本任务完成标准是指定停止后日志的完整字节冻结、可独立复核和诚实分类，**不是最终整个 Mod、迁移、经济、成长或公开发布验收通过**。

## 执行结果

已生成 [完整归档说明](evidence/1019-rc4-phase-a-final-logs/README.md)、[原字节索引](evidence/1019-rc4-phase-a-final-logs/index.json)、[独立复核](evidence/1019-rc4-phase-a-final-logs/verify.json) 和 [完整分类](evidence/1019-rc4-phase-a-final-logs/review.json)。19 日志（含全部5份脚本文档）＋3运行证明共22文件、5,908,410字节，源集合与所有源／副本字节／SHA256一致。索引 SHA256 为 `4005683aec3ae8c5a6e46b9b9501d19c449fe68c57076c57a49e6843d877b966`；六份 canonical 引用独立重读一致，无新增 Mod 树副本。22原文件另通过 Git原字节校验。

error.log全部53物理行／25记录已分类：21缺失发现、1consume覆盖、1错误DISMANTLE手输、2条nomads。错误DISMANTLE的原始提交回执现已找到，UTC12:05:41.730877确实调用错误名字两次，与v3冻结副本逐字节相同。完整game.log6记录均信息项；另完整检查debug.log1条，建筑类别警告与baseline仅时间不同，但无建筑key，具体对象／影响保留未知。

两个nomads分别在实发／后续清理分支20:09:31与原版完成callback控制20:20:06，精确因果仍未解。最终error.log与控制R副本完全相同，R后到停止0新增字节；无日志新增不能作Relic／jump／后续用例通过。没有不归类而丢弃的error/game记录，也没有把原生文件名或baseline相同当作无害证明。旧public031及新RC4 process日志没有并入。
