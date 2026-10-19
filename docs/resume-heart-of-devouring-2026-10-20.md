# 吞噬之心 RC7 恢复执行记录（2026-10-20）

## 目标、范围与设计

用户已要求阅读交接并继续遗留任务，恢复原“修改、测试、发布”工作。以
`handoff-heart-of-devouring-2026-10-20.md` 和子项目原 typed 验收合同为准。
优先恢复普通吞噬最后无阻断自然档，再依执行卡补保护条件、成长、Lithoid、
旧档迁移和进程重启，最后审计完整停机日志。已通过分支不重复执行。

继续使用 RC7 冻结生产树、简体中文、单生产 Mod。旧 run、失败原件及未执行
worker 准备目录均保留；新建隔离 run，实际加载后另存原生档，逐项核实来源。
先使用 `open_kaishek` 包级检查，任何工具缺陷先在工具仓库修复并验证、提交推送。
普通吞噬完成前独立固定返还人口及其它人口变化预期，不能按 after 残差拟合。
保护条件使用既有 v2 空星选择器，未来结果只依据真实原件登记。

## 验收标准

- 新运行 manifest、生产树、游戏 EXE、语言、单 Mod 和 seed 哈希与交接一致，
  实际新 PID、加载、另存均有记录。
- 普通吞噬自然完成及真实重载、重复回调通过原 settlement/no-settlement 合同；
  保留所有失败和严格差异，不手调进度或手工完成。
- 其余检查按原 18 组、138 项清单补证；缺证仍为 null/PENDING，最终日志单独审计。
- 正式发布必须满足交接的版本、CHANGELOG、静态及实机门槛，核验自有工坊
  `3815707212` 后才推送正式标签；上游 `3710613857` 只读。
- 本任务改动独立提交并推送，非中文仅静态验收，原噬岩者自然战役不恢复。

## 恢复前调查

- 当前 `main` 跟踪 `origin/main`，HEAD `c24c8799b`。唯一既有未跟踪目录为
  `eat_everything_origin/docs/evidence/1019-rc7-purifier-economy-worker-ui-v1/`，不纳入本任务。
- 未发现运行中的 Stellaris 进程。交接普通正例 seed 为
  `r7normalprecomplete3.sav`，预期 SHA256
  `0c872e2efdd2329ae021466955cc0fe1ab4813bf0b0c8233f011706bf8615772`。
- `open_kaishek` 无 AGENTS.md，已阅读 README 和包级验收说明；工作区干净。
- RC7 原静态报告为 PASS，36 P 脚本、12 DDS、131 键 × 10 语言。
  恢复时重跑检查，不将旧 PASS 冒充新执行。

后续发现与实际证据继续追加于此，并更新子项目对应验收记录。

## 新运行前置与启动观察

- 新静态报告：`eat_everything_origin/docs/evidence/1020-rc7-resume-v1/static-open-kaishek.json`，
  本轮实际运行 `open_kaishek/tools/accept_stellaris_mod.py`，PASS，36/36 P 脚本、
  12 DDS、131 本地化键。非中文九语言静态校验通过，运行时不在范围内。
- 新 run `20261019T201325Z`、PID `32348`，原生独立 userdir，唯一 seed 是交接
  `r7normalprecomplete3.sav`。`r8resume-provenance.json` 核对源/复制/工作区树、
  seed 原字节、单 Mod、简体中文、profile 和新进程；这只证明来源，尚不证明加载。
- 首次 F12 超时，桌面 GDI 图显示白窗；后续 Steam GPU 图实际得到加载 31%、
  81%、89%。原游戏启动中响应及截图可能间歇不可用，不能只凭白窗判定卡死。
  原截图和失败动作保留，继续等实际原生主菜单后加载。
- 用户再次明确要求验收完成后由本代理自行发布 Steam 更新；无需重复请求发布许可。

## 旧日志 nomads.94 初步归因（仍待完整日志审计）

已核本机原版 `events/nomads_events_1.txt:2268` 是 `nomads.94` trigger 的
`from = { is_nomadic = yes }`，由原版 `on_war_ended` 或 `on_becoming_subject`
调用；生产 Mod 没有定义或覆盖这些入口，也未引用 nomads 事件。

实际旧日志错误 03:45:39 与实际 `fast_forward 30` Enter（03:45:39.057）同秒。
只读原生 `r7normalstart`（2201.05.28）仍有 war0，attackers 含 country0，
defenders 列表已不在，原战争目标仍指此前已灭的 country1；
`r7normalm01`（2201.06.28）中 war0 已为 none。原日志 FROM 为无效国家 ID
4294967295。上述链支持“敌国灭亡后战争延迟清理触发原版事件”的解释，
不属于已证的 Mod 文件解析错误。精确引擎内部如何选择主胜者仍是推断，
不能仅据此把最终日志门槛设为通过；需封存源码哈希、战争前后和完整原始日志。

## 普通吞噬恢复结果与稳定窗口

- 新原生 `r8normalpre.sav`（2201.10.01，SHA256
  `81ebf2dcca03510bf8ba65c512df5e7e1053244c075d3cddad600b2123d59fb4`）
  核实源物理1、core2、fleet151；源112人口均为实际 founder species3305111553，
  非purge的complex_drone；core5150。Situation16777231进度5、未killed，源无
  pending或结算done旗。账本C/G21、D7、made300、worlds1与交接一致。
- 读取 after 之前已写 `r8normal-fixed-case.json` 和
  `r8normal-predeclared-expectations.json`：返还112、独立对照自然变化0、制造0、
  core5262、C/G23、D7、made300、worlds2、世界危机积分+750／灭国+0。
- 仅自然 FF1 到2201.10.02并原生保存 `r8normalimmediate`。原 settlement
  **25/26，通过数不等于整体通过**；所有人口、物质量、制造、容量、危机积分
  均命中。唯一失败是源旧殖民地18的pop_jobs列表尚未清理；实际owner/controller
  已无、实际pop/group为空、活人口计数无、pc_shattered和五个结算旗均在。
  完整 FAIL 与 strict 差异保存，不修改检查器或原件。
- 下一步固定再自然 FF1 到2201.10.03，检查日清理后的稳定态。期间不跨月、
  已无源人口，保持原事前人口／奖励预期不变；不从稳定 after 反推任何预期。
  完成后再执行已有重复回调和真实原生reload验证，整体验收仍PENDING。

次日stable（2201.10.03）旧岗位列表仍在，原settlement仍25/26 FAIL。进一步
读取全局表确认：23个岗位记录与before逐字相同，正workforce110/2的分配
均指已从全局表删除的group83886081；源colony18没有全局活人口，所有国家
的拥有／控制殖民地列表也不再含18。112人口已经实际返还，不能把历史岗位
ID当成活殖民地，但也不能只检查本地空人口列表。

已按文档先行新增[独立全局存活性检查设计](../eat_everything_origin/docs/rc7-owned-colony-history-liveness-1020.md)、
独立工具及10项正反测试。真实before→stable补强报告通过，原FAIL完整嵌入，
旧checker/inspector/receiver及生产包均不改。正在继续原重复回调和真实reload；
不因这份限定补强报告提前提升整体验收或发布。

## 月脉冲加载故障与第三进程恢复

同日重复原no-settlement9/9、严格零差异；同日reload后保存态比较也9/9，严格
44项差异原样保留。但后续月度R重载出现顶部资源／日期栏缺失、Esc与console
不响应。标题栏物理聚焦和已目视菜单按钮点击均未恢复；两次play0均被可见性
guard在输入前拒绝，未发送。不能把这些失败改写为成功。

新run `20261019T201325Z`／PID32348已正常退出，UTC20:40:29.690，forced=false、
running_after=false；19份日志5,881,419字节已冻结。日志只有一次原重复dispatch
marker，所以先前reload后9/9只证保存态无变化，尚不能单独认证那次回调已执行。

原生phase1（228文件／14,442,193字节）与phase2（122文件／11,324,203字节）
已原字节归档至`eat_everything_origin/docs/evidence/1020-rc7-normal-resumed-v1`，
两phase分别有独立copy索引，完整原FAIL、UI失败和停机日志全部保留。

已新建第三run `20261019T204055Z`／PID24520，唯一seed是前一进程真实保存的
`r8normalreload.sav`。从主菜单重新加载并另存核core5262/C23，随后原回调、FF29
到2201.11.02，与前一run已完成的月度I（core5267，账本不变）做原同日负例。
此链尚在执行，未提前填索引；最终需本进程实际dispatch日志marker闭合。
详见[加载恢复设计](../eat_everything_origin/docs/rc7-runtime-load-limbo-recovery-1020.md)。

后续加载优先先真实退出到主菜单，再调用旧loader，避免只凭同日旧帧误认加载
完成；先验证实际中文UI流程后才封装复用。最终日志范围因必要UI恢复增至三run。
高C积压补奖、四支guard、成长、Lithoid与旧档迁移仍待实测，原93true/45null索引
未因未封口新材料而自动提升。生产包与原三工具接口均不改。

## 普通吞噬封口与继续保护条件

第三进程成功真实加载C23完成档并另存，原9/9；实际回调日志marker已闭合，
自然FF29后的F与旧run的I同为2201.11.02／core5267，原9/9且奖励／成长不变量
全真、无活Situation。完整结算补强PASS，原27项诊断26真／1假仍原样保留。

普通新包三批464份源拷贝，最终472payload／32,858,016字节、8份SAV、93对
GPU/OCR，938个提案引用全部SHA闭合。原seed不改，新增normal三个原检查及
common本国主体返还单项：**当前97true／41null，18组及组件均PENDING**，普通
组仅缺最终日志审核。当前索引4,592处引用／2,644唯一文件SHA已核，历史操作
记录的旧reference-plan指纹保持原义；当前_scaffold指纹同步新可变plan。

已实际验证“退出到菜单→原文确认→无旧日期的主菜单→载入原件→原生另存”
流程。保护条件基线r9guardAbase真实日期2201.01.21、C/G0、core2／Mother151／
敌源17正确；现执行A组九持久无效目标＋当前core。新增主菜单加载薄包装只用
已观察中文UI，冻结原loader和回执不改，接下来用A组实际R/I/F验证该包装。

## 保护条件 A 已封口，B 继续

A的四份原生档、48对GPU/OCR和254份原件已归档，原receiver十任务全通过，
五项单独检查已合入，现为102 true／36 null；全部整组仍PENDING。提交
`0abe26472` 已推送。真实core可用及十目标前提在R/I/F持续，增长不变量一致。
详见[保护条件恢复记录](../eat_everything_origin/docs/rc7-guard-resumed-runtime-1020.md)。

B实际殖民中、foreign secondary及真实双方地战已经建立；长地战log探针两次
解析异常保留，原生战斗对象和短探针另证实际状态。复用r9gbDiag1作ready，
I为2201.01.23；重载列表OCR和滚动位置失败已安全停在读取前，选中同组滚顶后
原名可见，现用新stage原loader继续，不改原存档和旧回执。

Lithoid同预设人口基数缺少旧原生样本，已先记录
[独立初始基线方案](../eat_everything_origin/docs/rc7-lithoid-resumed-runtime-1020.md)，
将在候选功能分支全部保存、当前run停机后仅补一个0.3.1 Jan1隔离样本，不重跑全年。

B已由原receiver复算三任务通过，所有前提、EEP变量／Mother层数及growth检查
成立。391原件／20,771,236字节、84对截图OCR已原字节归档；新加三项后索引
105 true／33 null，仍为全部PENDING。当前5,256处引用／3,300唯一文件SHA
重新核验通过。C输入已真实载入May28，old/new refs实际日志marker闭合，下一步
原生UI迁移，无手工调用迁移效果。
