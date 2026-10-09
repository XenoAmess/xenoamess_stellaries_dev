# 吞噬之心：噬岩者优先续验

目标：执行用户最新顺序，先完成正式国策“噬岩者／蜂巢思维、石质”主路线，再验“铁心灭绝者／机械智能”。本轮使用已发布0.2.0，不改资格、产出或发布推荐；原有机种族洁癖留待两条优先路线后从2309.05.02稳定端点续验。

范围与前提：正式生产41文件、精确Stellaris4.5.2 exe、Steam离线、简体中文实机。先执行open_kaishek包级前检（priority-terravore-package-preflight-2026-10-09.json已PASS：18脚本、12DDS、73键），工具只认证解析和包资源。其它九语言只静态校验，不做实机。原有共享机制证据可以引用，但不代替本配置独立自然吞星、经营、完整灵飞／武灾、蜂巢世界和严格重载。

新局方案：独立RUN20261009T044016Z，原生合法石质蜂巢设计，起源origin_heart_of_devouring、civic_hive_devouring_swarm及civic_hive_ascetic、trait_lithoid／trait_hive_mind。仅用原生帝国设计文件，不载入probe Mod、不预置源星。UI已显示正式“噬岩者／禁欲主义”、石质、蜂巢思维、“吞噬之心”；政府显示“噬杀蜂群”按原游戏记录，不能把它改称噬岩者政府。星系设置实际UI为200恒星、椭圆、3电脑／0高级、尉官、铁人关闭，科技0.5／传统0.25，采用既有缩短自然组合门槛方案，不能据此称默认1倍率通过。S型增长上限5、增长需求0.25及其它默认设置另按实际SAV核验。

初始证据方案（实施前）：新通用priority_native_save.py只封装已存在的简中原生保存／审计，用唯一stage和明确预期日期，记录完整error-before/after、运行身份、原SAV SHA、依赖来源SHA及完整country0审计；不点击未审核事件、不给资源／科技／人口，不把OBSERVED保存输出当路线PASS。先保存2200.01.01原生开局，核SAV物种／国策／统治形式／实际起源和星系设置、C/G0／D2／made0／worlds0、唯一绑定母星与王庭／地貌、没有源任务或免费制造；初始女王事件按生产days2自然触发，首图与正常确认均独立保存，并严格区分开局叙事和实际奖励。初始“我们的征途是星辰大海！”为原版开场按钮，不当成EEP女王通知。

验收标准：逐项更新实际结论，所有原始FAIL／辅助错误和未过滤日志保留；生产与公共推荐只在证据满足时改变。自然殖民、付费种子搬运、原生噬岩损毁与随机收益、消化48月等节奏按实际Q/T核；新增母星容量不自动创建区划，正常付费建设后核实际矿物食性／维护和真实月预算。灵飞需实际完整虚境终点，武灾需正常AP／威慑与2／3／4阶段、真实矿物造舰及维护，女王通知用真实pending／正常选择／无二次收益；蜂巢转换完整费用、20年真实日历、地貌／唯一核心及重载检查独立记录。已有EAT-05／08分项只按其受控或自然范围引用。

12:40～12:49准备实际完成：正式41文件tree ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7，独立dlc_load仅mod/ugc_eep-local.mod，未seed_save／无定时命令；原生设计源与生成设计及包装原输出见[准备原件](evidence/priority-terravore-preparation-2026-10-09/source-snapshot.json)。PID23824，12:49正常点“开始征程”；首次实际画面2200.01.01暂停，原版开场显示石质蜂巢食性叙事，女王days2通知尚未触发。星系预览有原生unknown字样，记录但不据它推定实际政府缺失；初始SAV核实际government之后再判。本轮启动日志2670字节与首发既有21条缺工坊目录＋预期决议覆盖提示同类，不声称全局零错误；后续新增内容严格单列。

用户优先级及有机收尾完整经过见[发布后续验](post-release-acceptance-round-2026-10-08.md)。此次有机退出为FAIL_FORCED_STOP，归档保真通过不等于正常退出或重载通过；后续有机原生恢复独立验收，不回放已完成事件。

初始只读守卫实施前：独立priority_terravore_initial_guard.py严格核已保存2200.01.01／SAV SHA与观察文件一致、生产树和唯一Mod配置、无seed_save／定时命令／probe文本、实际government的gov_devouring_swarm／auth_hive_mind／上述两国策和起源、EEP初始收益全集预期、唯一绑定物理7／殖民地0／原尺寸18、d_eep_core唯一一份／capacity2／court永久、唯一己方母星和实际5300原生人口、石质蜂巢及陆地偏好原模板、无EEP源星任务／无本国待选、空传统AP；按SAV galaxy核200档、3／0电脑、科技0.5／传统0.25、尉官／铁人关。住房等首日缓存按实际记录，不声称已是完整稳定月预算。任何FAIL保留并暂停下一日历；本守卫PASS仅代表这个合法开局组件。

初始实际SAV a1d2284a9440956ed62e76d3c42e808bca1f2224faf9980b49164baa5edcd2e4，26项原检查25true／1FAIL保留：国策检查错误使用q.ids，后者只读取数字ID，给含引号国策名称的列表返回空。实际政府raw明确两个合法国策，与真实UI相符；不是资格拒绝或Mod缺陷。独立只读补核实施前：保留原FAIL及其它25true，绑定同一原SAV SHA，从原government.civics直接q.tokens并unquote得到精确两国策、有序／无额外条目，并核实际gov_devouring_swarm／auth_hive_mind／起源；UI原件同时含官方“噬岩者／禁欲主义”。补核通过才继续实际日历，不能改旧JSON消除失败、不能重复开局生成世界。q.ids只用于SAV数字引用，字符串命名列表须逐token解引号，此结论记录到群星研究文档，不推广CK3。

初始五项独立字符串补核已通过，原26项FAIL不变；实际本族5300、三系储备0、能源／矿物／合金／贸易各200／Unity50。正常原版开场确认后真实UI仍2200.01.01暂停，未漂移日期。

女王自然开局步骤（实施前）：复用formal_production_native_calendar.py从上述初件执行唯一真实fast_forward2到2200.01.03，包装保留原源码／输出，核完整2日回执、暂停日期和新error；若事件遮挡回执只保存实际端点／读旧行，不重发2日。SAV应有country0 eep.10待选和唯一母星绑定、C/G0／D2／made0／worlds0不变。拍摄原CG及中文正文，正常唯一选项“王座之外，皆可吞噬。”，同日另存且严格实际库存／科研／人口组岗位／源与母星物理原件／EEP／政府／传统AP／领袖／历史保持，唯一变化为对应pending删除和预期history记录；若原生初始日缓存另有变化先留FAIL、按实际raw分项调查，不宽泛豁免经济。只有正常确认和只读检查均完成才进入真实首月与自然殖民经营。

真实2日已到2200.01.03，完整Fast Forwarded 2 Days回执首轮核实，SAV b84856bce040c1c08e540fb98d7c77e2509e81b2361006f37fffac8e253c185b／新error0，EEP全部收益变量及实际人口5300保持；本国唯一pending1／eep.10，真正开局CG与正文已实拍priority-terravore-queen-opening-ui。SAV cheated_on_save=yes为本验收debug_mode和原生日历环境实际标记，不能称成就模式或无控制台环境；动作原件仅发送fast_forward2，没有任何经济／科技授予。

正常确认辅助实施前：priority_terravore_opening_ack.py读取唯一待选1/eep.10和对应实际UI唯一按钮，先核暂停日期和图片SHA，再正常点击一次、立即打开ESC菜单并唯一stage保存；所有真实stockpile/research、完整国家科技／EEP／AP传统／政府／拥有星球、人口组岗位与九实际对象集合、building/zone/construction/leader raw等严格保持；selected_history原记录严格前缀，只追加对应pending1／option0一次，实际human字段如实记录，不猜零基或一基人类引用。删除的pending范围须严格唯一原eep.10，源任务保持空，error字节保持。任何FAIL原件不改、不重放选项。原生player块的name实际unknown、country0，此为当前离线身份原文；星系预览的unknown暂不与生产本地化key泄漏混同，实际government有效已独立证明。

女王开局正常确认实际30项保持通过／新error0；后件da24991bd36981b2503367505d4db9e23450207ebbbe6f3e8bc2271806e4c614，仍2200.01.03暂停、无本国待选。实际全国家raw、库存／科研、人口组岗位、母星／地貌／核心／领袖／原生政府与EEP严格保持；仅删除pending1，history实际追加player_event1／human1／option0一次，未发容量、人口或资源。确认前原CG和正文原件已保留，尚未上传新的工坊截图。此为合法开局和开局叙事组件通过，不是完整噬岩者路线。

首月与自然经营后续方案（实施前）：先保持human_ai关闭，从01.03真实29日至02.02，保存首个实际月结算、资源收入支出、石质矿物食性及人口与EEP保持；再真实30日至03.02，以连续完整月核能源／矿物／食物／消费品／合金／凝聚／贸易／影响力八项实际库存差和当月分类净额，缺失资源键按实际0处理，不期待不存在的食物／消费品库存正数。新priority_terravore_native_month_guard.py为只读通用月守卫，核实际日期／无新增error／无本国待选、EEP初始账本和旗标、无源任务、原生物种及AP传统保持、唯一绑定母星／原尺寸和核心／王庭、物种人口守恒与非负库存；首月和随后完整月均严格尝试八项预算零残差，若原生初期初始化差异产生FAIL按实际另证，不用宽松余额掩盖。

经营授权与边界：复用既有原生human_ai自然自动经营方案，仍是玩家自动经营，不冒充is_ai真正AI分支；可以在首两月检查后正常启用，单次保留原生命令回执及同日不发奖励证明，再按每个真实360日保存1～5年检查点。AI可合法侦察、研究、付费建设和殖民，物种／gov／EEP奖励保持或新自然任务按实际核；不赠送科技、资源、人口或AP。每年检查实际AP／传统，若将选择与目标灵能路径互斥的路线则停止自动经营、从尚未选择的原字节检查点正常续局，不改SAV／不移除已选AP。当实际殖民源星可用时停AI、正常中文决议开始；后续长月与武灾／蜂巢转换另立端点计划，初步5年不能当完整路线通过。

首个实际月2200.02.02，后件72f8a98935e74a8484ed9f7d872bc597ce875c8aea6acd896af8b4a264f6d4f8，19项月守卫通过／新error0／无待选。8项库存预算残差全0；实际净能源29.5005、矿物8.22、合金16.223、凝聚18.3097、贸易53.625、影响力5.25384，食物／消费品0。石质人口特质实际矿物维护53／食物0，人口5300→5306自然增长，EEP0／D2、初始AP传统与唯一核心保持。该首月不是整个经济长期闭环，下一完整月和后期经营另核。

进度证据落地方案（实施前）：在明确无活动GUI辅助的端点，将当前RUN现有全部原件复制到独立checkpoint目录并逐字节核SHA，附partial-snapshot明确仍在活动、不是最终未过滤日志／正常退出证明；包括初始国策解析FAIL／补核、所有原SAV、日历回执／输出和源码。后续新端点使用新目录或精选新文件，不覆盖已归档的通用动作文件。每个checkpoint暂存后核raw Git blob，按仓库规则提交推送。

第二个完整月2200.03.02／6afa7949cbf6bc42bf3bc98835b732753499b06d7eb305753ad1c9c082dec5f0，19项月守卫再次通过、新error0／无待选，8项残差仍全0。净矿物8.16、矿物人口维护53.06、人口5312；能源29.5005／合金16.223／凝聚18.3097／贸易53.4850／影响力5.25384，食物消费品0。EEP初始账本、母星绑定、核心地貌及实际模板保持，首两月完成后允许上述原生自动经营。

启用原生玩家AI的执行顺序（实施前）：当前新进程尚未发过human_ai，先唯一一次打开console并发送human_ai、实拍原回执文字证明启用，然后只关闭console／可见Debug View，不发日历；同日原生另存terravore-player-ai-enabled。独立只读开关守卫绑定真实命令动作／原回执图片、2200.03.02和前后SAV SHA，核全部实际库存科研／人口组岗位／完整EEP与模板／母星和核心／建筑队列／原AP传统等同日保持，原生政府／实际研究差异如有必须留FAIL调查；不因启用文本就假定“真正AI国家”或忽略后续收费。只有这个开关及无待选守卫合格后推进首个实际360日。

只读开关守卫实现细节（实施前）：priority_native_player_ai_toggle_guard.py参数为前后stage／命令stage／回执stage／on或off，保存原始回执字样；OCR仅允许已实际观察的AI/Al单字符识别差异，仍须完整Human AI is now ON或OFF、唯一真实human_ai输入动作、日期与暂停、原图SHA。其它经济和全部对象严格保持，不把文本开关当成真正is_ai的判定，原生日历必须之后单独运行。

玩家AI开关实际32项保持通过，2200.03.02同日原生SAV与开关前件完全相同SHA6afa7949cbf6bc42bf3bc98835b732753499b06d7eb305753ad1c9c082dec5f0；原Console真实Human AI is now ON，OCR把I识别为l原字样保留，原图独立绑定。所有真实库存科研和完整国家／EEP／母星／人口组岗位／建筑队列原文保持，新error0、无待选；证明仅是全局玩家自动经营开关，不是假设开关状态被序列化进SAV。

新前检报告Git字节差异修复方案（实施前）：0cc7a7e5中仅旧有机全量档做了原字节核验；新priority-terravore-package-preflight报告工作区SHA764ade5d12dbbea4f5c8bf016d444ec12e948c1fdccaa7e4bc7b7081f4096b49，Git HEAD因CRLF转LF变为1d03e6527396f5702b6e7837f8e692d509dd4901b75073cb9201c4f8cf6d6200。报告数据相同，但准备manifest引用的是原raw SHA，跨检出引用不合格；给所有本任务priority-*.json加入binary属性并重新暂存原字节，不改报告结果或生产内容；随后严格核新preparation十原件、初始两月checkpoint全部文件和顶层priority报告的Git blob SHA。原HEAD差异记录在本文，不声称第一次提交已经核过新准备字节。

checkpoint工具实施前：archive_priority_checkpoint.py将无活动GUI辅助的当前RUN全部文件及当前未过滤日志／原生配置拷至独立first-months checkpoint，新增source-snapshot逐件绑定原字节；这是暂停端点快照，不是停止／最终日志证明。verify_priority_checkpoint_git.py使用单个git cat-file批量核source-snapshot中的原件、snapshot／binary属性、本轮preparation和顶层priority JSON；第一轮源SHA如有不一致停止提交，不覆写旧失败或扩大语义通过范围。

13:12首两月暂停端点已归档[source-snapshot](evidence/priority-terravore-progress-2026-10-09/first-months/source-snapshot.json)，327原件／16422003字节，包含原初始26项FAIL、五项补核、30项开局保持、两组19项预算及32项开关保持的原源码／输出／SAV／UI与当前未过滤日志。不是最终全量RUN或正常退出证明。正式0.2.0没有任何生产代码改动，也未更新工坊。

checkpoint首次暂存核验FAIL保留：327原件／准备输入已逐件读取，顶层前检报告仍不等于原raw SHA。原因是新binary属性后普通git add沿用未修改文件的索引缓存，没有重新清理旧blob；必须git add --renormalize仅该前检报告，再按同一只读helper重新核整套，不能仅看属性已设置或修改报告文本绕过。此处没有新的游戏操作，也不重跑已通过的初始／月度／开关；原失败观察与后续核验并列保存。

实际renormalize后[344文件Git原字节核验](evidence/priority-first-months-staged-verification-2026-10-09.json)PASS／16577777字节，前检报告恢复原SHA764ade5d12dbbea4f5c8bf016d444ec12e948c1fdccaa7e4bc7b7081f4096b49，与准备manifest绑定一致。首个Git核验FAIL观察另存priority-checkpoint-first-failure-observation-2026-10-09.json，未覆盖旧原件。接续从已验证的2200.03.02原生玩家AI开启端点按唯一360真实日推进第一年度到2201.03.02；实际殖民／科研／库存／AP／EEP与pending逐项记录，不预期AI零花费或无正常增长。
