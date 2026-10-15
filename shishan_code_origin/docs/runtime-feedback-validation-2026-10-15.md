# 反馈修复在本机新版群星的实机验证

日期：2026-10-15。用户要求同步主分支、更新本机群星，更新完成后Steam保持离线，再实机测试此前反馈修复。该授权取代本线程此前禁止游戏/屏幕操作的范围限制；不包含Workshop发布。只用简体中文与隔离userdir，不改玩家真实存档。

## 本轮结果与范围

远端实际主分支为`main`（无master），已基于`origin/main`的6798155c3d082e375b800c97fb9ee69c6e845db5完整同步。群星本机与当时实时public均build25664273、4.5.2，安装验证结束后Steam一直离线。最终候选`0.2.0-rc.6`；107项程序回归、六合同、149场景745资格断言、19兼容映射，以及正式/测试包G1均通过。发现的引擎阻塞经逐轮修复和真实复验，旧失败证据保留。

| 项目 | 本轮结果 | 证据和边界 |
| --- | --- | --- |
| 同步、安装、离线 | PASS | 更新日志、公开build核对、离线窗口；最终Steam运行且WantsOfflineMode=1，游戏已正常退出 |
| 引擎加载 | PASS | rc6完整error.log只有21条禁用Workshop描述符不可用提示，其它错误0、空国家目标marker0；90生产文件与实机副本完全一致 |
| 初始局势速度 | PASS（样本） | rc5原生n0/J0=1，n0/J100=0.75，实际岗位分配核对；rc6对应数值脚本未变 |
| 月速下限与负面阶段 | PASS（受控边界样本） | rc6五院所真实分配J500、n1，月速0.2；III/IV/V中文界面产出惩罚分别12.5%/25%/37.5%、岗位维护同幅增加。九类country_base资源跨月预算一致；阶段进度为受控输入，舰船实战未执行 |
| 全特质5% | PASS（加算） | 正负/隐藏/身份/偏好等实际formal键纳入；人口加权U，领取后U精确+1，modifier唯一；独立乘算未实现 |
| 三选一、重抽和冷却 | PASS（跨候选复放） | rc3/4真实前缀3→2→1→0，第四票重抽回3；rc6同日清理后仍三合法选项，最后领取CD2，R不误增；不是同一run从头 |
| 模板、权利、领袖及外国隔离 | PASS（样本） | rc4权利UI全公民/体面、跨月500矿工保持；rc6仅新增两个实际模板、7名领袖含envoy迁移、旧定义与外国200人口哨兵保持。7组空派系字段正规化单列 |
| 普通维护科研 | PASS（旧档自然延续） | rc5正常UI研究，原生progress0→454.15171→成功n1，普通科技恢复；此前无console指令，不代表fresh2200或平衡时长通过 |
| 清理、优化、复发交叉 | PASS（受控输入） | rc6真实on_success清理/优化、n4→5一次；显式复发凭证后状态一换一、唯一progress0局势，待领奖励不丢；无凭证重放10/20/30不变，不是10%概率测量 |
| 白绮免维护、死亡和重启 | PASS（非零XP样本） | rc5费用1.0失败修复；rc6本人免费，其它4人各4.0；实际kill/on_action及UI重启，精确500能量/200合金，唯一白绮level5/XP25/技能和待选保留，跨月官员预算8 |
| 旧计数与重复层 | PASS（旧档分支） | 先前原生7/5/11/4→R23一次；rc6真实重载R24，受控维护R25、再次真实重载仍25，n1→2→2/CD2不动，U43，modifier67→68→68 |
| 长名称 | PASS（单显示配置正文） | 1600×900、请求缩放0.75，正文完整显示用户指定18字；标题栏仍由原生省略。其它分辨率/缩放NOT RUN |
| 非中文翻译 | 静态校验通过 | 九语键、BOM/header、引用、raw key及简中占位风险检查；运行时不在范围内 |
| 月内统计快照 | 已知边界，严格审计FAIL保留 | 月脉冲后人口增长与缓存P/W/U可能短暂不一致；后续奖励/刷新匹配，不把限定delta PASS覆盖原严格FAIL |
| 完整长期验收 | NOT RUN / 未实现 | 完整74用例、22自然新局、阶段III–V所有产出来源/战斗、全部显示矩阵未执行；独立乘算未实现 |

实际政体：早期混合模板与个体种子都是`auth_democratic/gov_moral_democracy`；旧耗尽档是`auth_machine_intelligence/gov_machine_empire`。机器格式塔仅覆盖旧档重载、受控维护与重复层，不能宣称其自然新局/完整路线通过。

精选原生存档、GPU截图/OCR、完整日志及独立审计见[证据索引](evidence/feedback-redesign/runtime-2026-10-15/README.md)。[最终环境](evidence/feedback-redesign/runtime-2026-10-15/rc6-numeric/final-environment.json)、[最终日志分类](evidence/feedback-redesign/runtime-2026-10-15/rc6-numeric/final-native-log-check.json)、[107项程序报告](evidence/feedback-redesign/runtime-2026-10-15/static/rc6-final-unit-agent-452.json)可直接复核。正式Mod不带夹具，未发布Workshop；仅提交本任务文件，保留用户console_history.txt。

## 输入与同步

开始时分支main为`c9112825440e8b126dff1e0512e7eed2ebb312db`，仅有用户未跟踪文件`console_history.txt`。远端HEAD指向main，没有master；按用户所指主分支同步origin/main，读取的目标为`6798155c3d082e375b800c97fb9ee69c6e845db5`。本次远端含近40万新增/更新文件，初次快进检出触及Windows长路径限制；启用仓库本地`core.longpaths=true`后完整恢复检出，最终提交及状态另记。不得因部分检出就宣告同步完成。

安装初查为Stellaris `Cygnus v4.5.2 (9776)`、Steam build `25664273`。SteamCMD匿名实时app_info中public同为`25664273`，更新元数据已刷新；客户端在线验证安装完整性，等待完成并记录结果，然后显式切回离线才进行测试。4.5.2 EXE初始SHA-256为`400df27c82ddc845aa9dce79bd468d81f18f060d299cd263e3afa93aef4f7a83`，验证后复核，不能沿用旧4.5.1哈希或旧生成文档身份。

## 目标与实施范围

先按`C:\workspace\open_kaishek`的README执行包级检查，显式传入本轮已核验游戏指纹与VERSION。现有入口支持`--expected-exe-sha256`，版本身份变化本身不是工具缺陷；如果实际发现工具缺陷，遵守项目规则先在该工具仓库修复/验证/提交推送后继续。

现有Mod为`0.2.0-rc.1`、supported_version为4.5.*；先冻结原候选，再记录实机发现与必要修复。不得把旧audit中的0.1.3数值预期套到新版，不覆盖历史报告。所有新程序/fixture实施均基于本记录的设计范围：

1. 新增本Mod独立运行适配器，复用仓库桌面harness，但明确配置游戏/Steam/DirectX/截图目录、此Mod路径与冻结指纹、简中、隔离userdir和独立run状态；不导入另一个Mod的入口或启动其夹具。默认窗口显示，实际物理像素及缩放入manifest；若GDI帧失效则使用带新文件时间戳证明的Steam F12帧，不用陈旧桌面当游戏证据。
2. 复用历史原生存档的副本进行旧档迁移与两类机械政体检查，原文件只读并记哈希；同时保留新局/自然项目路径。新存档须由游戏原生写出，确认真实日期/元数据/内容并实际重载，手写save不作为结果。
3. 必要时新增独立P语言验收fixture，仅在测试包中启用，先通过工具检查再运行。fixture可建立单变量边界、回调凭证和明确候选输入，但不得预写期望输出伪造验证；受控回调测试与自然科研成功分别报告。正式候选无测试事件、资源补给或必中概率。
4. 新增只读存档审计时按`player.country`定位实际国家，审计该国variables/flags/modifiers、国内人口组及物种实际键；预算按实际国家关联。输出到本轮证据，不写历史报告。脚本输出独立预期、实测、原生来源与限制。

## 验证顺序与通过标准

| 阶段 | 目标与通过条件 |
| --- | --- |
| 输入/工具 | 仓库完整同步；Steam public与本机build一致、安装验证完成；Steam已离线；候选/fixture先通过open_kaishek；32项程序回归及当前原版引用静态校验。 |
| 加载/数值 | 正式候选简中加载，检查本Mod错误；初始月速1、n增速0.25、劳动力减速0.25和下限0.2；岗位3社会学+1凝聚力，负面阶段减半；以实际面板/进度/存档核对。 |
| 架构/作用域 | 实际正式trait全键及人口权重、无主谱系人口/恢复、单一动态修正及加算数值；clone保留权利、国内人口/领袖迁移、外国共享模板不变。 |
| 选择/项目 | 三个不同合法候选、reroll至少替换可替换项、同票单次、3→2→1→0、重开不重抽、拒绝后可重开、成功只结算一次、待领交叉清理/复发与项目恢复。 |
| 旧档/成长 | 四旧计数7/5/11/4仅迁R=23一次、旧效果/计数保留；耗尽后R+1无硬上限且不减实体选择冷却；原生保存/重载后状态保持。 |
| 白绮/界面 | 科研正向、死亡/复活成长保留、本人维护与其它领袖隔离；长名实际修正/详情/奖励界面可达全文并不挡按钮，记录分辨率/缩放，简中截图与原生存档交叉证明。 |

5%当前是原生岗位产出加算，独立乘算未实现；不能给TS-06乘算目标记PASS。自身-100%维护不等于在所有正倍率组合下保证零费用。完整74用例、22局自然体验和全部分辨率矩阵按既有方案分项登记，尚未执行的部分不冒充通过；本轮重点是用户要求的已实现修复及真实引擎缺口，发现阻塞时先定位并完成相关修复/复验。

## 证据与收口

本地运行资料在`_runtime/shishan_code/20261015-runtime/`，精选证据归档到`docs/evidence/feedback-redesign/runtime-2026-10-15/`，保持在正式mod外。记录同步提交、Steam更新/离线状态、工具版本、游戏/Mod/fixture哈希、原生前后save、截图/OCR、原始日志与case状态。运行时操作只由主任务执行；辅助任务只读调查/程序检查，避免争用焦点。实际执行事实持续回写本记录，最后仅提交本任务改动并推送，不含用户console_history或其它Mod证据改动。

最终状态：本轮列明的核心简中功能回归已完成，候选为0.2.0-rc.6；安装验证与离线保持完成。完整74用例、22局自然体验、全部显示矩阵仍未执行，不宣称完整Mod验收完成。

## 执行记录

- `open_kaishek`首道检查已对4.5.2实际EXE指纹运行，退出0：25/25脚本、13DDS、268键、十语言，报告`_runtime/shishan_code/20261015-runtime/package-rc1-452.json`。语法/包级PASS，不是实机语义结论。
- 混合模板旧原生存档采用`rs04-variant-anchor-2203.09.24.sav`副本，源SHA-256为`0eb913bc6f7b38369ece69ef574469b90166c174c84fb6b2cb50bdaf1b8574d5`。独立预期：主5040人口×6键，子511人口×7键，P5551、W33817、U=33817/5551。耗尽档独立预期U43、历史R23、T66，两个来源不能混淆。
- 新只读save审计实施已单独记录`runtime-save-audit-2026-10-15.md`。原生pop_groups.planet关联的是colony ID，应经colony.carrier再读实际planet/ship所有权；禁止直接把它当物理星球ID。现有生成文档仍为9月旧文件，不把其当成4.5.2新导出。
- Steam客户端主游戏安装验证于14:46:46记录`App update changed: None`，scheduler结果`No Error`；随后客户端继续验证Workshop订阅缓存，等待结束再离线。实时public build仍25664273，未凭空升级版本号。

### 首次真实加载失败（rc.1）

4.5.2离线实机进程PID5812已到简中主菜单，F12实际GPU帧可获取；GDI返回黑帧，继续采用Steam截图，不能据黑帧宣告加载失败或成功。首次F12发生在加载未完成时无新图，第二次已成功得到主菜单。userdir的error.log归档到本轮`rc1-loading-failure/`，其中确认本Mod三类错误：人口组里`pop_amount`展开为不支持该scope的`count_owned_pop_amount`（3019条）；普通命名script value使用标量定义导致`Invalid script value`（51条）；scripted effects初始化深度5耗尽、约436468效果实例未初始化（CRITICAL）。原候选的LD/引擎闸门记FAIL，未加载存档或把主菜单当作功能通过。

根据项目规则暂停Mod验收，先在open_kaishek工具补充有明确边界的通用作用域/脚本值预检及回归，必须对原故障包复现失败、工具修复验证并提交推送，才能继续。Mod后续修复方案：仅人口组域改原生`pop_group_size`与`trigger:pop_group_size`；普通script value改`{base=0.05}`，保留数值；奖励生成器扁平化或按已验证原生机制预初始化，消除深度错误后重启实测，不能仅把CRITICAL过滤掉。新增候选使用`0.2.0-rc.2`并更新changelog，旧失败证据保留。

独立运行适配器还需同时覆写legacy与pdx图形设置，避免manifest写请求窗口而游戏实际沿用基础harness的borderless_fullscreen。实际分辨率始终以GPU帧/client rectangle为准。初次game进程已正常关闭，未强杀。

独立入口发现并修正转发退出码问题：基础harness的main返回1时，适配器必须`raise SystemExit(harness.main())`，不能忽略返回值而让截图失败的进程显示退出0。第一次早期F12捕获已在JSON明确ERROR，不登记为PASS；后续入口同时依退出码与结果字段判定。

同步恢复完成：首次checkout失败后保留工作树，将索引/分支快进到原定远端（mixed不覆盖工作文件），仅用长路径模式补回88个初次失败的远端文件。最终HEAD为`6798155c3d082e375b800c97fb9ee69c6e845db5`，`git diff --name-only`为空，只有用户console_history和本轮新文件未跟踪；未提交或覆盖其它Mod改动。Steam于14:48:20全部验证结束`No Error`，14:49切离线，配置`WantsOfflineMode=1`与客户端简中离线提示已记录。

### rc.2修复与工具闸门

open_kaishek以`47c3c4e`提交推送作用域与脚本值修复，45项相关测试通过。冻结rc.1正确失败：161处人口scope不匹配、1处普通脚本值标量错误、0 UNKNOWN，90源文件未变。生产rc.2通过25/25脚本、13DDS、268键检查。迁移计数助手四处内联，静态调用链最大由5降至4；真实初始化仍需重启日志证明，有限预检不覆盖此限制。

隔离fixture同文件保存global target后恢复使用的类型未能推断，工具明确UNKNOWN，没有跳过后置断言。再次暂停Mod验收，补充有限saved target推断并以`2b55996`提交推送，53项相关测试通过；歧义、未知、动态名和跨文件重定义仍UNKNOWN。主任务重跑实际fixture-rc2为PASS：26/26脚本、13DDS、268键，退出0；报告fixture-rc2-final-452.json。门禁解除后才启动游戏。

生产rc.2并行程序复核：50/50（38脚本+12读档）测试、validator五合同、奖励20原版机械/56候选组、19原版modifier/archetype及十语言引用静态检查通过。静态指纹f393c57d2120113634e25cfc9e1e14283183c9a4f6bdf84b53c999eac2a7d778；此算法与运行适配器的逐文件字节树哈希不同，不能互换。

### 存档前置条件与受控完成路径

Mixed种子已有维护员实际workforce=200、bonus_workforce=20，n=0，因此新版预期月速是0.5而非1；检验初始1必须实际禁用岗位至J=0，不能把容量或bonus_workforce当作assigned J。独立公式为max(1+0.25n-0.25floor(J/100),0.2)。

4.5.2原版存在complete_special_project用例，可强制完成既有项目并执行真实on_success链；优先用此路径检查结算和恢复，不预写success_pending。它仍是受控完成，不是自然科研时长/体验通过。无凭证重复event只证明拒绝重放，不能替代一次项目回调。保存使用中文菜单；4.5.1的save控制台命令曾返回Unknown command，不沿用旧版未证实写法。

### rc.2真实启动

run `20261015T071829Z`于15:20:55启动PID10624，91文件副本含90个未改生产文件及1个独立fixture事件，字节树指纹d79efdc3eeb247513310b748348780b9c91274dcac2e87997e622487ed7e16ea。实际GPU帧与client rectangle均1600×900，system.log明确Fullscreen=no，Steam保持离线。加载期间早期F12可能未产生新帧，入口如实失败而非复用旧图；15:23已到简中主菜单。

rc.2简中主菜单后完整日志检查：Wrong scope=0、Invalid script value=0、post-init depth=0、CRITICAL=0，本Mod命名错误=0。首次点载入被坐标边界保护拒绝：桌面仍为前次AltEnter后的1024×768，1600窗口居中产生负坐标；未发生误点。先通过Windows显示API恢复任务前1920×1080，移动窗口完整可见，再继续，不以屏幕外窗口作UI可操作通过。


### rc.2行为发现与rc.3修复范围

混合模板新原生保存fb452_mix0.sav（SHA8808fcef599e814f6e47883d71667fd35340b88f71d42933d7c83da976ddc677）已审计：P5551、W33817、U/T6.09205、R0、bonus0.3046、唯一修正multiplier6.09205，与独立预期在1e-4内一致。n0、实际J200，界面月速0.5；旧种子last_month=4.8是旧版同日缓存，必须跨月复查。种子到4.5.2首次保存有同物种worker/civilian重新分配（总人口不变），不能要求group分类完全相同或当成Mod丢人口。

详情标题在1600×900、请求gui_scale0.75下被原生省略，悬停无全文，正文也无完整名称；此显示用例FAIL。修复计划为十语言summary正文首段引用完整title，奖励/实体/重复结果共用正文并留空行；保留完整译名、动态token、BOM，不缩短用户名称。rc.3重启复测前不能改记PASS。

外国探针建立READY并原生保存sentinel0：实际外国country16777218/group18/size200共享旧主模板3321888769；本国模板/人口/7领袖及权利与mix0不变。维护项目由complete_special_project真正调用on_success，n0→1、一次凭证已消费、无R增加、待选期间只留CLEAN，说明项目下一循环保护生效；但pending1原生存档tier1、slots=[5,33,33]，跨tier且重复，UI仅两选项，三选一明确FAIL，未领取此故障票。

只读引擎trigger命令确认逻辑：NOT={always=yes always=no}返回FALSE；NOT={AND={always=yes always=no}}返回TRUE。新鲜GPU帧native-not-multiple-result.jpg与native-not-and-result.jpg，不能沿用离线解释器not(all)的假设。修复范围：生成器random_draw使用单子NOT包AND，234个权重屏蔽条件显式整组取反；程序解释器改NOT为not(any)并添加引擎真值表及确定性权重负例。

奖励选项悬停还自动展开clone、变量和刷新内部效果，长tooltip挡界面并泄漏key；rc.3把39领取、reroll及later内部执行体置hidden_effect，保留玩家需要的custom_tooltip和allow提示。刷新控制台effect本身会为描述先取未设置的临时变量而产生日志警告，须分清console tooltip评估与真实事件/月脉冲结果；不将这类警告从证据中删除。


旧档后续证据：legacy23原生P5561/U43/R23/T66；跨月2227.04.12人口自然增至5567，架构P/W仍是月脉冲采样的5561/239123，逐即时值审计明确FAIL，U43/R23/T66保持。不能将此报告改作全PASS；本机制月度刷新有月内缓存窗口。下一次项目真实on_success刷新后legacy24实际P5567/W239381/U43/R24/T67/bonus3.35，唯一修正multiplier67，四旧计数与43个特质保留，n0→1，控制前置CD2完成后仍2。原生source/调用及完整对照报告均归档。

完整日志另有mod_leaders_unity_upkeep_mult未本地化警告，白绮self modifier需要十语言兼容显示键。新增修复设计见leader-upkeep-localisation-fix-2026-10-15.md，键269前置静态检查后重新冻结rc.3。不将此警告归为无关原版噪声。

早期rc.3 run073806Z在加载期收到停止，30秒不响应后harness按记录结束进程（forced=true），尚未加载任何存档；保留该process/stop记录，不声称它完成实机。最终补键后的新候选另建run，不能沿用旧manifest指纹。

最终rc.3补键后生产与测试包已分别通过G1（25/25、26/26；13DDS、269键），run `20261015T074214Z`于15:42:15启动PID10904；90生产+1fixture，原样复制树指纹095996161f40881ccd9d8a312a1e4954c1c9664f3b54d9bea773e5c550ba1f03。从原生sentinel0奖励前基线重载，不沿用rc.2故障pending。其source SHA52bcdfb53958054fa0c0f2bef59feb55e352e4080c5baf57c485055861bfa512。


### rc.3原生行为与rc.4修复计划

最终rc.3源静态指纹f5aa60abc66f67f869b071b4fa5e1d08b50b6e65181339fe2e016684ceda6f1e；62项程序回归、五合同、十语269键及自动modifier key检查通过。真正重载legacy24并刷新保存后仍R24/n1/CD2；全文在正文显示，标题栏仍原生省略，此分辨率下正文与按钮不重叠。不是全部显示矩阵通过。

首张维护奖励原生slots=[19,6,18]/tier1，三个独立且合法。稍后保存fb453_pending1后真实重载，从首都「选择待领取的改进」决议重新打开，候选不变。重抽实际变为[17,12,1]，与旧组三项全部不同，CD3及同票已重抽flag正确；禁用提示显示还需3次实体选择。领取工程学核心17后slots清空、CD2、n1/R0；两个国内模板各加1，U精确增加1，外国旧模板、人口、领袖和权利均未变。提示已没有内部变量长列表。

独立原始存档也发现不能忽略的迁移回归：7名领袖仅5名常规领袖迁移，两名envoy留旧模板；白绮change_species后portrait由shishan_code_vivhite重置sd_hum_robot；新子模板49没有显式权利记录，而原48 full/normal、国家默认purge/subsistence，实际权利继承尚UNKNOWN。六条owner_main_species空scope错误中，未领取的06仅悬停也出现，提示预评估是强线索，但不能将所有错误假定无害。完整独立对照保留21 PASS/3 FAIL/1 UNKNOWN，不能只取+1统计宣称迁移通过。

下一张奖励实机提供了与已选工程学核心互斥的物理学核心，保存fb453_pending2core作为负例，未选择非法组合。原版44份traits文件审计补全20机械候选直接及反向互斥、17–20的Machine Age条件与ROBOT/MACHINE模板资格；保留既有个体经济过滤政策，不复制依赖编辑器FROM的species_potential_add。

rc.4的必要修复与验收标准：三类克隆显式inherit_parent_rights=yes；只迁国内envoy（须原生API确证）；白绮现有leader迁移后恢复专属portrait，保留ID/经验/技能；在解析奖励国家事件目标前exists守卫，真实claim和悬停日志均需无该scope错误。优先从原生fb453_reroll1（尚未领取17、CD3、头像正确）重新领取，独立核对所有7领袖、两国内模板显式权利、外国哨兵以及跨月can_fill_jobs/实际工作人口，随后完成2→1→0及第四张可重抽。必要修复后的新包必须重新G1，旧rc.3已正常关闭，证据只读归档。

项目恢复的真实时序：领取后下一维护安排在次日，原地暂停时立即complete不存在的项目不会结算；实际推进至2203.09.28后项目已恢复且on_success再次正常执行。此事实须与项目永久丢失区分，不在测试中跳过排队日。

rc.4完整源与夹具G1分别25/25及26/26通过（13DDS、269键），83项完整程序回归、149资格场景/596原版守卫断言及兼容映射通过，静态树98fe2c5ec6a3641d687083a9fa9858d1375af88ce04527a74b18d36098d0e366。最终run `20261015T080652Z`、PID14424于16:06:53启动，91文件副本字节树9c4a966962d024e41bf8d2bf5dce4a46f5f73ff483291628182c16efcc9b323a；原生source为fb453_reroll1 SHA dfbd57b69483888404d0dff327eae1379e088bb48dcfc5dff5320aba6caf2c83，7领袖/白绮头像尚未迁移，适于实际重领17复验。

子模板49（541人口）已在真实物种界面选中并打开权利详情：完整公民权、体面标准、完整军事服役、允许殖民，无人口/移民控制；未修改任何权利。rc4-sub49-resolved-rights.jpg与rc4-sub49-rights-detail.jpg交叉证明实际解析正常，原始重复50记录仍保留，不推断所有版本序列化语义。

只读getter调查中，首个trait_robot_engineers是操作者错写（实际key为trait_robot_artificial_engineers），其FALSE无效并产生两条控制台诊断，不归为生产Mod错误。后续canonical命令未获得可见结果，可能展开侧栏/输入焦点影响，不能记TRUE。适配器补先释放修饰键、请求英文布局、移开侧栏并显式点击本次1600×900/0.75已观察的控制台输入行；以新只读探针验证后再继续控制性命令，仍以原生存档确认实际执行。

原生 getter 已用正确键和确认后的控制台焦点复验：`owner_main_species = { has_trait = trait_robot_artificial_engineers }` 返回 TRUE，`trait_robot_learning_algorithms` 返回 FALSE。两者组合区分新主50、子49和旧主3321888769，与 `founder_species_ref=50` 一致。对应 focused-getter 两张 GPU 图和独立审计 JSON 保留；错误 key 的早期两条控制台日志保留且不算生产错误。完整程序回归现为89项通过、无跳过（增加6项主指针/序列化边界用例）。

### rc.4 同日清理待领交叉失败与 rc.5 设计

连续实体选择已到CD3→2→1→0，第四张票真实重抽后CD3、三个候选替换；clean_pending原生保存仍n4/R0/CD3且槽11/9/12保留。清理即时将国内53/54正确迁55/56，但国家owned_species_refs仍53/54。原地重开奖励误判实体池耗尽、R增为1，窗口只剩重选/稍后，FAIL；未把未发生的第四次领取记通过。独立调查与修复方案见[物种缓存修复](feedback-redesign-owned-species-cache-fix-2026-10-15.md)。根因探针、原始save与错误窗口保留；修复后需重新G1与启动，不在运行中替换脚本。

rc.4 根因只读原生探针已确认：`trigger any_owned_species = { has_trait = trait_shishan_refactored }` 返回FALSE；同帧/同日 `trigger any_owned_pop_group = { species = { has_trait = trait_shishan_refactored } }` 返回TRUE。前者枚举缓存、后者跟随实际人口的差异被原生结果支持，不再仅是存档推断。rc.4于16:41:49正常关闭（forced=false）；原始存档、两探针、空奖励窗口与日志归档到evidence/feedback-redesign/runtime-2026-10-15/rc4。

rc.5生产与实际隔离包G1重新PASS：25/25、26/26脚本，13DDS、269键。新run `20261015T084453Z` 于16:44:58启动PID10616，91文件字节树 `73af92e29f52685278d2ee71b724274e500b6a6370db6ba68004106fdd8d91a8`，正式脚本90份与冻结源逐字节相同；extra-seed-saves记录第四票和旧重复层24的只读副本。首先载入个体机械2203.05.22种子验证初始月速及普通科研，随后重放第四票清理交叉。

rc.5最终程序验证为99/99、0跳过；validator五合同通过，149资格场景745实际守卫断言及19兼容映射通过。新增10项直接覆盖真实stale ownedrefs、冻结rc.4错误R1负例、多group内层复检和真正耗尽不开空窗口；90源文件静态树21f327ecb3082d23eb7434e7a02e9376f890726d655b8bc72eeaee172dba42ec。与run91文件字节树采用不同算法，不混用。

### rc.5 初始月速与普通科研路径

在个体机械旧种子2203.05.22，实际UI禁用唯一研究所后跨月至2203.08.21，n0/J0、建筑disabled=yes、无维护员job，原生situation.last_month_progress=1；启用同建筑并跨月至2203.11.03，n0、岗位workforce100且真实人口分配100（不计bonus10），last_month_progress精确0.75。独立16项检查PASS，存档fb455_initial_j0与j100。种子既有局势进度保留，不称fresh2200自然新局。研究所原生建筑提示同时显示每100分配基础3社会学/1凝聚力，当前估计实际产出4.16/1.38；该估计已包含其它倍率，不拿来声称独立乘算。

普通维护在F4选择社会学「地面防御计划」，F1选择「维护屎山」后实际点击研究按钮，界面成本2000/预计42个月。本分支之后仅正常推进时间，不调用complete_special_project、不补资源或研究倍率，须以队列/中间progress/最终成功存档确认，不能从点击按钮即记成功。

### rc.5 白绮费用失败与 rc.6 方案

普通维护已自然成功：fb455_natural_success，2209.04.11，n1/R0/CD0，三个实体槽7/1/11，成功凭证与window清，pending保留；旧项目消失，普通社会科技恢复并有343.67827进度。此run到该档没有任何console命令，保存前后的自然队列/收入/库存独立审计通过。时间跨度是既有旧种子延续，不宣称完整自然新局或平衡时长通过。

领袖页直接证实白绮维护1.0而非0，其它四名4.0，本人免费FAIL。原生defines经济倍率最小-0.9，原先-100%被夹到-90%；现已查到原生should_pay_for_leader_upkeep排除should_not_have_upkeep，采用本人限定flag，不覆盖全局规则。先行设计见[个人免费修复](feedback-redesign-vivhite-free-upkeep-fix-2026-10-15.md)，新候选rc.6须重新G1并重启实测。自然成功档白绮level5但experience缺省0，不能用它声称非零XP恢复；正在通过正常治理取得实际经验后再测。

为避免XP=0的弱样本，rc.5用正常星球总督选择UI将白绮指派首都，正常跨月后保存fb455_white_xp（SHA8bbde052951b3854f8ad70e5d5fb3a948fc6d993d294f8e9ae830832143f49bd）。原生日期2209.08.18、level5、经验20、official、planet0、四次待选及原两个选择保留；运行中截图07.14早于实际暂停保存，不以截图日期覆盖存档日期。此run仍无console指令。实际rc.5于17:05:03正常退出（forced=false），精选45文件已归档rc5。

rc.6正式25/25与隔离包26/26重新通过G1，13DDS/269键；run `20261015T090720Z` 于17:07:33启动PID4376，91文件字节树fb55a9bfa5de4b4db2eb10eaf7aa606c60ee3d254b3a5de5301912fcbcdd2d4c，seed为真实白绮XP20原生存档。程序调用prepare时曾误把seed路径传为scheduled_commands位置参数，入口明确抛异常未启动该不完整尝试；随后使用已验证的--seed-save成功prepare，实际run/manifest分开，不把失败尝试记作加载通过。奖励/实际人口枚举生产文件与rc.5哈希相同；仅白绮原生豁免、备份flag移除和十语本人免费说明新增。

rc.6最终程序验证107/107、0跳过，validator六合同、149场景745资格守卫与19兼容映射通过；90文件静态树566030887c51815361b4a9d3d102258c821f7eaf89b1d219241b9a6b0f597b1d，十语言269键静态校验通过，九种非中文运行时不在范围内。

rc.6重载XP20种子后正常跨月至2209.09.30，fb456_white_before（SHA55867e1bbd89153cbf3c4bf9dcfc62147c789e8e4d5b3749da65002b77ce67ec）白绮XP25/level5/四次待选/原技能/专属头像保留，并获得should_not_have_upkeep；UI费用栏消失，其它四名仍4.0。预算current及last_month官员9仍是刷新时点快照，未伪报8；最终跨月费用另核。实际kill_leader触发正常on_action与备份剧情，未直接调用.40；保存fb456_white_dead。同日资源未推进，后续重启费用可严格对照。

白绮真实重启前后严格同日费用：能量7216.54875→6716.54875，合金3196.11119→2996.11119，精确500/200，其它实际货币未变；三科研伪资源缓存字段另有快照变化，未声称整个经济block相同。新active唯一ID16777294，level5/XP25/四次待选及两候选/正式trait恢复，原生免费flag存在，工程/社会三个国家bonus各1恢复。正常跨月至2209.11.28，XP仍25，current与last_month官员unity均8（其它官员4+4，白绮0）；本人中文姓名、专属头像正常，其它四人各4.0。旧backup global target即时清、white身份移除且非owned，跨月历史实体删除。中间备份freeflag仍在、name含replacement字符和portrait普通的原始事实保留，最终通过design正确渲染，不把这些中间字段误标为实际显示失败或声称remove语句已实际清掉flag。

## 最后收口

旧档rc6实际重载与重复层对照已完成：fb456_legacy24_reload → legacy25 → legacy25_reload，旧四计数和U43保持，R24→25→25、n1→2→2、CD2不变，唯一架构scale67→68→68；槽变量实际缺失而非观测0。OPT/relapse/replay独立18项通过，白绮重启19项通过、清理领取17项通过并保留序列化观察。UI自动化两次因悬停提示遮挡OCR、旧档位于列表下端保守停止，重新取帧定位后继续；相应失败帧保留，未当成Mod失败或通过。

此前核心回归run于17:33:21正常退出（forced=false），17:35:13复核Steam仍运行/离线、Stellaris无进程，安装StateFlags4/build25664273和EXE哈希未变，桌面恢复1920×1080。该run的error.log原始21行均为未启用Workshop描述符提示，其余错误0；原始日志完整归档，不删除历史失败来制造零错误。实际生产90文件逐字节匹配运行副本。随后补充数值边界，最终环境以下述新run为准。

### 补充基础数值的直接引擎证据（先行计划）

收口复核发现0.2下限和III–V新惩罚仍只有程序合同，作为本轮基础修复补做同候选rc.6实机受控边界，不改生产代码。新隔离run重载实际fb456_natural_claim（n1/J100/已赚特质/白绮free），通过已验证原生add_building向首都增加四所研究所作为岗位容量输入，正常推进至真实分配J500；不预写n、月速、trait统计或期望产出。核native last_month_progress=max(1+.25-.25*5,.2)=.2。此输入不验证建造成本或自然平衡。

使用本机原版证实的局势进度effect进入III/IV/V，正常tick后在中文局势UI和真实save检查stage、岗位生产/舰船/岗位维护惩罚恰为旧版一半；不直接添加期望modifier。保存各阶段原生档及tooltip/GPU帧，与原版经济输入区分。沿用已通过G1且逐字节相同90生产文件，记录新的manifest、seed和hash，正常退出并再次核Steam离线。完整74/22自然局不随本补充扩大。

### 补充数值实测结果与最终环境

run `20261015T094102Z`于17:41:04启动PID8976，仍为rc.6冻结包，91文件字节树`fb55a9bfa5de4b4db2eb10eaf7aa606c60ee3d254b3a5de5301912fcbcdd2d4c`，90生产文件逐字节一致。seed是本轮实际领取后的fb456_natural_claim，SHA`9ddcb31ce9dab6843758ac2f71e786b43a8242d1cdda4da3cb89e4d5844bbc4d`。原生只读trigger先确认首都至少四个空槽，再添加四所研究所；正常跨月后五院所enabled、实际workforce及分配人口都是500，bonus_workforce50不计入J，n1、原始公式0、native last_month_progress精确0.2。独立下限审计8/8通过，原生档为fb456_floor_j500。

阶段输入只使用`set_situation_progress=500/750/950`，不写效果或预算。中文详情中的III、IV、V分别为[500,750)、[750,950)、[950,1000]，每月资源产出-12.50%/-25%/-37.50%，岗位维护+12.50%/+25%/+37.50%。舰船伤害/亚光速的原生工具提示按整数显示-12%/-25%/-37%，生产脚本值分别为-0.125/-0.25/-0.375；没有开展战斗或航行计时，不能把UI取整声称数值变为-12%/-37%。三个阶段均正常跨月并原生保存，保留工具提示GPU帧、OCR和控制台输入记录。

[阶段独立审计](evidence/feedback-redesign/runtime-2026-10-15/rc6-numeric/independent-rc6-stage3-4-5-numeric-audit.json)48/48通过：III/IV/V原生stage索引2/3/4、progress500.6/750.4/950.4，日期分别2210.05.02、07.12、09.23。每档仍n1、J500、月速0.2；current与last_month的country_base能量由I阶段25变为17.5/15/12.5，九类country_base资源都对应基础量的0.875/0.75/0.625。生物学家消费品维护由I阶段6.93变为10.395/11.55/12.705，对应岗位维护倍率变化。该对照证实实际经济结算，不仅是描述文本；不代表所有资源生产方式与舰船实战都已覆盖。

初次启动截图尚在加载而无菜单OCR，未据其记主菜单通过。打开F1时曾把已打开的列表关闭，查找行保护随即停止；随后重新打开定位，未发生错误领取。失败帧`rc6-numeric-stage3-list`与后续成功详情均归档，不将操作保护错误归为Mod失败。

本run于17:56:18正常退出（forced=false）。17:56:48最终复核：Steam运行且WantsOfflineMode=1，Stellaris无进程，StateFlags4、build25664273和EXE SHA均未变，桌面1920×1080；完整error.log仍仅21条禁用Workshop描述符提示，其余错误0、空国家目标marker0。精选证据在`evidence/feedback-redesign/runtime-2026-10-15/rc6-numeric/`。此处的受控建造和进度输入只验证边界与效果，不代表自然建造平衡、完整经济矩阵或22自然新局通过。

归档提交时发现仓库`core.autocrlf=input`会规范化部分原始JSON换行，导致另一台机器检出后与SHA清单不一致。归档目录新增本地`.gitattributes`的`* -text`规则，保留所有证据原始字节；将原始CRLF声明为合法行尾，同时保留普通行尾空白、文件末尾空行和空格后tab检查。重新规范化暂存后核对索引Git blob与工作树字节哈希，不只核对当前磁盘。

最终归档完整性检查通过：400文件约55.4MB，276份JSON可解析，所有目录清单的字节数和SHA匹配；43份原生sav与各自来源JSON/meta/SHA一致，55对OCR与GPU图像SHA一致，7份日志ZIP的CRC通过。20份本任务Markdown的79个本地链接可达，VERSION与descriptor同为0.2.0-rc.6，`git diff --check`通过。源代码冻结后只追加运行证据和文档，未重复运行与改动无关的程序测试。
