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

首两月原件与字节修复已提交推送c91db2a6。第一年度原生日历已完成／完整360日回执确认，2201.03.02实际SAV dcc41ff8dbbf6bac722e8c5578cc69c53f146f9dee39b5cabbfc3b696cb68ea6／新error0。实际尚只有母星、人口5483，矿物库存10.65而当月净8.45为正；能源286.852／净25.7055、合金107.184／净15.341、凝聚41.31914／净16.23286、贸易964.52375／净55.77375，影响力180.08488／净5.98678。原生发现传统已正常付费采纳两节点、无AP；三系真实研究队列均已开始并有部分进度，完成科技仍29（与开始相同），不能声称本年新完成科技或已经殖民。C/G0／D2／made0／worlds0均保持，尚无EEP任务。人口总增171不可一概称纯自然增长：原生石质障碍清理等需从实际deposits／人口原件核明，EEP制造仍0。

年度只读辅助实施前：priority_terravore_natural_year_guard.py核前后原SHA、真实calendar360日回执及预期年端点、无新增error／无待选、完整初始EEP收益与母星绑定／尺寸18／D2／唯一本族／唯一core地貌和永久王庭、原国策与起源／统治形式、无互斥AP、实际非负库存与原生矿物维护。研究队列实际原文、已完成科技增量、传统AP、每个殖民地实际人口和月预算原样记录，多年月不套一个月残差、不要求无正常建设／增长或无原生障碍清理。当前年度不得推进到下一年，除非此守卫通过且检查实际殖民源星／新任务；发现源星就接管按正常决议流程，发现新日志先按原脚本调查。辅助只读不自动点击消息／购买／开关AI。

第一年度20项只读守卫通过，无待选／无新增error／无源星候选。实际去除母星原生d_collapsed_burrows地貌271、无新增EEP地貌，母星唯一核心1573保持；不能把人口总增171全归为出生或EEP奖励，原native地貌变化完整记录。继续从本年实际端点唯一推进360日至2202.03.02，随后复用同一只读年度守卫；实际新源星一旦存在便停止年度续推并接管，不把未完成的科研、殖民或5年计划写成通过。

首年额外只读分类预算／人口核查：planet_pops_traits实际矿物维护54.77、food字段缺失按0，当前三个己方人口组实际物种全为3321888769。本次年度20项辅助并不单独断言维护或全部物种组唯一，这两项由完整audit数据只读另核，不虚增原20项数量。原生d_collapsed_burrows静态费用是energy300，清除会create_pop_group，非EEP免费制造；无法凭年度单一快照拆出全部实际付款时点或逐月出生数量，限制与原件并列。

第二年度2202.03.02／96667bb83c9df56ae25ed54326b1ece16ebb9fbefa343cdd935d2d6b9697de37，20项年度守卫通过／新error0／无待选、无源星候选。实际母星5554，原发现传统3节点／AP仍空，完成科技仍29而三队列持续有进度；矿物107.4／净7.74、能源569.318／净21.9555、合金116.276／净15.341、凝聚7.80964／净14.14904、贸易1640.6925／净56.82625。其它EEP／唯一核心仍保持，未结算、未制造。第一年度船坞订单50331652实际75合金／60基期／已30进度，不能误称殖民船、矿物船或完成造船；其type只见design1521尚未独立解码，按原件留存。继续按已列1～5年方案唯一推进第三年360日至2203.03.02，再核同一守卫和源星候选。

13:31第三年度2203.03.02：原SAV 2784876331a273d616e9f028b3de404343e275f4b5da1a7e38dbd77094ac8a63，完整360日回执和20项年度守卫通过；无新增error、无待选、无源星候选。人口5627，矿物732.55／净10.70，能源848.8475／净24.332，合金66.281／净14.900，凝聚26.30676／净12.48357；传统4节点、AP空。完成科技31，较第二年新增tech_doctrine_fleet_size_1与tech_powered_exoskeletons；三系新旧研究队列实际仍推进。EEP初始账本、尺寸18／额外容量2、唯一核心及原生合法政体保持。继续按既有五年检查方案单次360日至2204.03.02，随后运行同一守卫；发现真实殖民源星、待选或错误时停止后续年度推进。

13:34第四年度2204.03.02：原SAV ec4681fb7fe6b5dc79d585450ac2577337309163c77c6cbeb5c41f1850aafaee，完整360日回执／20项守卫通过，新增error0、无待选。实际母星5701、另一殖民地15人口6，源星候选首次非空，立即停止年度推进，不再执行第五年。完成科技32，新增tech_physics_1；矿物1704.346／净21.784、能源1117.4765／净17.1245、合金182.199／净14.459，初始EEP账本及核心保持。源星人口6不能直接宣称已建立完成或符合吞噬资格：先读实际Planet／Colony及殖民进度，再正常关闭human_ai、实拍OFF回执、同日原生另存并用既有32项开关保持守卫核对；然后按实际中文UI决定等待殖民完成或打开合法吞噬决议，不赠送或迁入免费种子。只读解码第三年ship_design1521的growth_stages.ship_size实际science，先前75合金订单可进一步归类为科研船订单；不追认完整付款时点或已造殖民船的成本证据。

13:36玩家AI关闭与接管完成：原生OFF回执d6fe2da5337f4d8f7487d5ef29192e0fa99708a754576f245c49e2d47c9145a0，32项保持通过，前后SAV均ec4681fb7fe6b5dc79d585450ac2577337309163c77c6cbeb5c41f1850aafaee。新特洛伊原生UI明确“正在殖民行星”（原图65c089b120bad927deb0b8704333d97622f3f22fcf7fb1746cbc914b6cb20982），实际Planet90／Colony15、Q17、colonize_date2204.01.21、人口6；上月GROWTH_CAT_COLONIZATION=3。原版defines中COLONY_POPS_REQUIRED100、COLONY_MONTHLY_GROWTH3，与当前建立阶段一致；不得此时启动吞噬，也不迁人口绕过建立期。先在无GUI辅助活动的暂停端点归档four-years-source checkpoint、核Git原字节、提交推送，再另行推进殖民等待与母星真实付费建设。

13:38[四年接管端点归档](evidence/priority-terravore-progress-2026-10-09/four-years-source/source-snapshot.json)完成，644份原件／27436026字节，包含每年真实日历／审计／20项结果和开关保持／源星UI，当前未过滤日志及原配置完整保留。这是活动暂停端点快照，不是正常退出、完整重载或全路线完成。[Git原字节核验](evidence/priority-four-years-source-staged-verification-2026-10-09.json)663个blob／27701408字节通过，范围另含准备原件和既有顶层priority凭证。

殖民等待与长局日历方案（实施前）：四年端点及优先级已提交推送75ef7f00。当前原生日历fast_forward仍采用逐日10ticks，既有研究已证实ticks_per_turn不加速该命令，因此不重复作无效参数对照。新priority_native_bounded_clock.py仅封装既有常规运行命令：从已保存且暂停的原生端点验证日期和原SHA，控制台ticks_per_turn10、game_paused false，先短段运行3秒，再明确game_paused true及恢复ticks_per_turn1，实拍最终暂停日期并正常另存。该短段不是精确日历边界，不承诺经过固定天数；以实际SAV日期为准，首探预期1～360真实日。保留全部命令／前后原日志、原图和SHA，任何超界或新增待选／错误均保留失败并停止后续推进，不重发同段。只改变模拟批量时间设置，不授予人口、资源、科技、进度或AP，不修改存档／脚本。与年守卫不同，此工具只证明常规时钟实际推进及恢复默认时间参数，不据此宣称殖民完成、经济闭环或完整路线通过。首次短段后另做只读检查：真实经过日数、殖民人口／月增长、完整EEP收益不变、政体／物种／核心保持、原生库存和三系科研、原生待选／新日志；只有检查合格才按实际增长继续等待。精确吞星有效月／最终边界仍使用既有fast_forward并核真实回执。

13:41短段原件保留但验证失败：OBSERVED_BOUNDED_NATIVE_CLOCK只检查了最终UI暂停与1～360日，没有核完整暂停命令回执。实际2204.04.30／b2ad3aa2f9ee9cb1e81fb9b7f7a494dfe5494d890a7314b59e056dbf1fd41cbd，经过58日／一次月界；源码b1a1f4c3780b98549d77a24faf54d26ee22ab03f53e03739603971bc5f231048的restored_commands字段仅表示已发送，不能声称均原生接受。图中Ticks per turn set to 10／1均完整，但有Unknown command，缺少Toggled paused state to true；不作为恢复成功，不继续批量运行。新增本国pending3／aianom.8，实际原版UI“物理学研究储备”，源星仍建立／人口9；EEP账本全部保持，新增error0。尚未独立确定Unknown command原因，不把焦点变化猜测写作事实。

恢复与原版事件方案（实施前）：先另发一次明确game_paused true并实拍完整接受回执，不重发任何日历／奖励；同日保存补核实际日期和状态。该新验证必须独立保留原v1观察，不改旧输出。然后正常确认pending3的唯一原版“确认”：anomaly_events_AI.txt:351的aianom.8选项在from Planet164随机新增d_physics_2／3／4，其incr_physicsdepoN_var在00_scripted_effects.txt:2956／2979／3002实际更新root.owner国家的aianom_physics_depoN（不是船变量）；按同日SAV逐项核真实矿藏／单项国家变量、仅删除该pending与追加一次history、所有真实库存／科研／人口／EEP／母星与任务保持。此为原版正常异常选项，不是控制台grant；有其它变化保留FAIL另查。本轮停止使用时钟v1，恢复后沿用既有逐日工具；不另实施v2，不以发出暂停命令代替接受回执。

13:44暂停恢复补证：完整原生Toggled paused state to true和Ticks per turn set to 1回执图efd04112f10d83029843cc018edb1321f37f7b59e25f4d9f2fb43d620d351966；terravore-clock-pause-recovered原生另存与原探针完全相同SHA b2ad3aa2f9ee9cb1e81fb9b7f7a494dfe5494d890a7314b59e056dbf1fd41cbd。此只证明补证时恢复，不追认v1暂停命令成功。

13:45正常确认一次aianom.8后，priority_terravore_physics_deposit_ack.py在native_save的预期日期检查FAIL：原预期2204.04.30，实际2204.05.01／SAV及audit均已留下，尚未走到自己的语义断言。不能把这次确认当同日隔离通过；不重放选项。实际无本国pending，EEP十变量保持，源星12人口。原保存工具在日期不符时未执行close-menu／native-save.json／history移动，当前ESC菜单保持暂停；先明确恢复全局暂停与ticks1、按实拍日期保存唯一新端点，再补核实际一次月界8类资源预算与人口／EEP保持、真实原生异常变化。audit_save仅收本国及EEP关联星球／地貌，foreign Planet164不在当前audit范围，原辅助后续未执行的全局added-deposit假设也不可用；补核必须从完整原SAV roots读取Planet164及全部deposit、国家全部variables，不修改审计范围或旧结果。新增辅助只做只读，允许真实1日月结并明确这不是原同日ACK验收。

13:48新稳定端点terravore-anomaly-stable保存成功，2204.05.01／8f20eb361b7eaebe6a177c290d7a1b6e4bd7f6c58605d9e3a4351da36b4cc274，与失败ACK保存原件字节完全相同；暂停回执再次完整接受，原待选已经移除。16项独立单日月界补核中14项true、2项FAIL保留：政府raw只把council_agenda_progress从2011.05推进到2077.05（+66），其余政府／AP传统保持，原辅助错误地要求整块不变；日志无新字节，实际本轮原日志从开始实验前已是2842，原辅助错误写死首发2670。当前run在12:43:58原生帝国设计界面另有172字节portrait_container缺失提示，完整原件已在此前checkpoint日志内；12:40启动2670是历史时点，后续本轮比较基线必须使用实际2842，不宣称全局零日志、也不把此172字节当作吞星脚本错误。新增只读corrections辅助须绑定原16项FAIL精确仅这两项／其余14true；只允许上述唯一agenda进度字段变化、AP传统严格保持；严格比较探针前日志与当前原日志全部字节一致（2842／SHA3ce09316fe6b09950153d044616cafe4a12fcbc7d7241c0dda92548bfb978671），并核稳定存档与ACK原字节相同。实际8类月预算残差全0、母星5707→5713／源星9→12、foreign Planet164新增150996490／d_physics_3、国家唯一新增aianom_physics_depo3=1，pending3／option0／human1一次，EEP账本与核心保持；不扩大为原同日ACK通过。

13:50六项严格只读corrections通过；原16项FAIL及原ACK日期FAIL仍保留。进入殖民等待：当前已明确源星仍处建立期，允许在玩家AI关闭、EEP尚未启动的前提下，从稳定2204.05.01单次真实360日至2205.05.01，复用20项年度状态守卫；预期仍不足100人口，实际月增长／殖民UI为准。随后每一段均先审待选／日志／AP／殖民人口；达到100或UI完成殖民就停止等待并检查合法决议，未达到则另记下一段。已有源星候选在本阶段是等待对象，不再以“候选非空”误称已可吞噬；不迁入人口绕过原版建立阶段。

13:54真实360日等待完成，当前原生2205.05.01／a723d7e55dc4915e9b9a876bf9720630aa27c7b72299d552685c623d20c61e70。母星5787／源星48，源星较前端点+36，与每月3增长相符；完整EEP仍初始账本、母星尺寸18／D2／唯一核心保持。当前矿物1985.086／净9.744、能源1327.882／净11.457、合金383.083／净18.209、凝聚313.67138／净13.23814，研究32项且原队列继续推进，AP空。20项守卫19true，no_country0_pending为FAIL，已按门槛暂停下一段：唯一待选4／cstorms.205，实际原生UI“仁善信号”，事件链“先驱者——阿达卡利亚”。它来自Cosmic Storms内容的先驱者文件，不是天气风暴事件；先前进度消息的风暴简称据此纠正。SAV2206.09.18是该待选到期日，不能当本次触发日。

续验端点与下一步：在此暂停原件归档colonization-wait checkpoint并提交推送，保留本轮所有原始FAIL及逐项补证、不修改生产0.2.0或公开推荐。先审precursor_events_cosmic_storms.txt:1855的cstorms.205唯一“很迷人。”正常选项：原版增加社会研究储备并在from创建site_adakkaria_the_propaganda_station，不能按纯叙事零收益断言，也不能计作EEP奖励。实施前须记录实际from、原生奖励公式和真实科研库存／考古对象，然后正常确认一次、按实际日期与月界核资源及EEP；无待选后继续殖民等待，不重发已完成360日、不重放pending3或4。首个源星完成殖民后再从正常中文决议进入真实Q17／预计ceil(17*2.4)=41有效月路径，实际损毁及Q以启动原SAV复核。

13:56[殖民等待暂停端点](evidence/priority-terravore-progress-2026-10-09/colonization-wait/source-snapshot.json)归档903份原件／35965936字节，完整保留被停止使用的时钟v1、异常确认日期FAIL、原16项FAIL／六项严格补证和当前年度待选FAIL及未过滤日志。[Git原字节核验](evidence/priority-colonization-wait-staged-verification-2026-10-09.json)923个blob／36324142字节通过；仍为活动端点快照，不是最终退出或完整路线验收。当前无活动GUI辅助，游戏PID23824暂停2205.05.01，玩家AI关闭，pending4尚未选择。

14:10继续执行前核查：同一PID、原生2205.05.01暂停、实际UI仍“仁善信号”。原SAV pending4的root Ship1055／from Planet388，原版脚本cstorms.205正常选项给owner社会研究并在388生成site_adakkaria_the_propaganda_station；00_scripted_variables.txt:87～89为18倍月产、最低350／最高100000。当前真实社会研究储备0，预算月收入12.475，乘18=224.55低于下限，因此预期正常奖励350，必须以实际tech_status.stored_techpoints核实。

正常选项与独立只读守卫方案（实施前）：新priority_terravore_precursor_ack.py只确认当前唯一“很迷人。”一次，实拍确认后的暂停日期，再按实际日期唯一原生保存；不预先假定同日。保存后严格绑定原SHA与原pending4／一次human1、option0历史，核社会研究储备仅增350、其余八类经济库存及另两系研究不变、完整EEP与人口组岗位／核心／AP传统／政府保持，完整原SAV的考古集合仅新增指定类型且在Planet388、原考古对象保持，日志原字节保持。允许真实日期为05.01或05.02但不跨月，若任何额外变化先保留FAIL再调查，不重放选项。确认成功后沿用现有真实360日到2206年同月同日、再180日的殖民等待，每段检查实际pending／人口及殖民UI；不修改存档或授予科技、人口、资源。

原版事件实际24项独立守卫全通过：仍2205.05.01、后件4b5d90b878d5e8b512c9a8631953ac88bb91ccfad22ad4f2713b0830133e727f；仅一次pending4／human1／option0、社会研究真实储备0→350、指定Planet388新增考古对象4，旧对象及EEP、人口岗位、核心、政体与其它实际库存严格保持，新error0。之前年度no_pending的原FAIL不修改，此处独立证明待选已正常清除。

母星付费经营方案（实施前）：真实UI检查可用空建筑槽，优先正常购买突触节点／研究实验室，目标使用维护工蜂剩余劳力而非授予科研或凝聚。原版building_hive_node和building_research_lab_1均base360日、minerals400，实际价格／时长以UI与订单为准；当前已完成tech_hive_node和tech_basic_science_lab_1。新通用priority_native_paid_building_guard.py只读绑定每次购买前后原生SAV，断言同日唯一新订单、真实扣矿及其它库存保持、paid_country0／正确母星colony0和指定zone／类型／进度、原EEP及AP传统／人口保持、无新增error；每次购买分别留证，不把排队当建成。建成后另核实际岗位、维护、月预算与EEP不变；如能源／矿物维护转负，使用正常区划或市场经营修正并记录付费证据。

第一座突触节点实际已购：2205.05.01／957d8a65ad2d6855de59d7e5acbf23cce907d4a4eb21be6d9a4619ff754ec274，矿物1985.086→1585.086，唯一母星zone2订单正确、0／360且无新error。原27项守卫26true、colonies_held一项FAIL：完整对比精确仅colony0新增last_building_changed="building_hive_node"，为本次真实建筑操作的原生记录，并非人口／核心／产出变化。保留原v1和FAIL，新增独立v2只读守卫明确要求母星此字段等于本次building，并仅在整殖民地严格比较时排除此字段；其它所有colony字段及原26项仍严格核。v2使用新proof文件，先补核同一SAV，不重购。随后按实际UI继续同zone2正常排研究实验室与第二突触节点，各自原生保存与独立v2核账。

14:17三笔真实付费订单分别28项v2守卫通过，原v1单项FAIL保留：突触节点1、研究实验室1、突触节点2，每笔400矿物／0进度／360基期、country0／colony0／zone2、原队列前缀及其它对象／EEP保持。第二后件263e28a95919903bfb7287d0532dd29caba6594f419fb9170740e29f16373c95，第三70ffb768742e065f9ac0e9dcf6a4230c8f9e74f27e5fa0684a1dcba59a22bc3a；总1200矿物实际扣除，剩785.086，不当作三建筑已完工。接着按既有殖民等待方案唯一360日至2206.05.01，逐项核源星人口／pending及首建筑实际完成。

不足一年等待的守卫方案（实施前）：新priority_terravore_natural_days_guard.py复用年度守卫的全部20项原标准，但将CLI加入days参数（1～360）、日期及真实回执严格绑定实际这段天数，验实际日期差也必须等于days；不能让180日流程冒充360日通过。其它初始EEP／国策／物种／核心／无待选／无新日志／非负库存保持；不强求殖民完成时人口仍每月只增3，完成端点的真实新人口与原版初始化按SAV和中文UI另核。此通用守卫只适用于EEP尚未启动，启动后不得继续套初始账本。

14:21第二段360日殖民等待完成，2206.05.01／97e76d0c5432fd30b56a78bb7d7e69319750c64fd172ba7a460389117bfd9ef5。母星5860／源星84；首突触节点实际building38、zone2，后续实验室及节点仍0进度排队，不能称全部完成。新增tech_power_plant_2／tech_planetary_unification／tech_mass_drivers_2，完成35项，当前三研究队列已空，须正常续选。凝聚净17.43599、矿物4.808／库存894.55、能源6.429。20项年度守卫19true，仅无待选FAIL：pending5/first_contact_critters.80与6/first_contact.1，EEP初始账本、核心、物种／合法政府保持、新error0。

第一次接触处理方案（实施前）：只经F1情报日志→“发现”→“显示第一次接触”访问真实待选，不用console event。当前实际window为first_contact_critters.80“活的星际碎片？”、唯一“我们一定搞错了什么……”；first_contact_NPC_country_types_events.txt:1070的正常option0将当前接触改为void_clouds_stage_2并after解锁调查，没有资源奖励。first_contact_events.txt:13的first_contact.1唯一INTERESTING没有经济effect。逐项实际UI确认一次，各自实拍，最后同日原生另存；新priority_native_first_contacts_guard.py只读核原pending5/6均清除、history仅相应正常option0各一次、实际FirstContact0阶段／解锁、其它接触对象保持、全国家真实库存科研／EEP／人口／核心／政体与科技保持、原日志字节保持。待选顺序按实际UI记录，不凭左侧选中条目猜对应pending；任何差异保留原FAIL，不重放事件。

14:27两项正常接触确认27项守卫全部通过，后件8237081441c8e38e00671d150e7f9ec9cdb563824364c8a687ab3359ece8ed5c。仍2206.05.01、无待选；contact0仅stage1→2／locked→in_progress／clues7→0、追加同日stage1完成历史及移除已选event，contact1仅移除已选event，所有其它接触和完整country0原文／EEP／人口／核心／库存科研保持、新error0。这是正常确认，尚未完成这些接触的全阶段。

原生研究自动化方案（实施前）：本机00_phys_tech.txt:7～18的起始tech_space_exploration已经提供unlocks_auto_research，不需要历史版本的后期科技；F4三系右下原生齿轮可正常自动选研究。保持human_ai关闭，先关闭当前研究候选面板，再分别点击物理／社会／工程的原生自动研究按钮，逐步实拍其启用状态；同日唯一保存后核实际自动化字段／真实研究队列、已完成科技未凭空增加、三系bank及经济库存／EEP／人口／核心保持、新error0。新只读priority_native_research_automation_guard.py按实际SAV字段严格核这三项开关和新队列，不能把自动研究冒充AP／传统自动化或免费研究。后续若自然刷到灵能理论，可正常接管社会研究；不靠科研grant追赶。

14:30三系原生自动研究23项守卫通过，后件6b4a7a3a74336742395bd807559b1067821e4849a10e2ebd81a98b742745ea04。完整country0原文精确仅tech_status.auto_researching_physics／society／engineering三个no→yes，真实经济与三系bank、已完成35科技、EEP、全部己方人口和核心等保持；当前暂停同日队列仍空，实际选题须看后续日历，不宣称已在开关当日投入研究。接续唯一180日到2206.11.01，独立days守卫与殖民UI确认后决定首星启动。

14:32真实180日已到2206.11.01，cc711e4695e9fe08d8bd45ce7b2f145d773bec548de8fc262518beddc21684ce，20项days守卫全部通过／无待选／新error0。母星5897，源星102；实际中文UI已是完整殖民地、殖民时间2206.11.01，Q17／1个蜂巢区划，不再“正在殖民”。三系正常自动选题始于05.02，真实进度物理117.593／社会150.955／工程144.664，社会储备440.972，不是免费研究。矿物920.242／净3.968、能源1499.364／净6.149，EEP初始账本仍保持。

首颗自然吞星启动方案（实施前）：在新特洛伊正常决议选原版“吞噬星球”，使用生产单key适配器，不用通用决议／console event，不造人口。启动前源星102本族已满足100种子，不应从母星迁入；原Q17且无d_lithoid_devastation，T=ceil(17×2.4)=41。正常确认并同日唯一另存，新priority_terravore_native_start_guard.py只读核同日原SHA、唯一EEP situation／owner0／目标source、progress0与Q17／T41、native／active／being_devoured及360日冷却、唯一母星绑定和C/G0／D2／made0／worlds0保持、真实两星人口组／种子无免费增加、库存三系bank及政体AP传统／科技保持、新error0。source载体记录或临时变量允许新增仅已读eep_begin字段，不能把启动当原版咬合或最终奖励。完成后单独实拍局势与吞星风味用于工坊素材候选，再按有效月逐段推进，12／24／36和40／41月边界独立核。

14:33真实“吞噬星球”点击后立即执行，未出现额外确认对话框；列表移除此项且源星出现被吞噬图标。此前stage名priority-devour-confirm-ui仅为预期名，实际原图是启动后的决议列表，不称其为已存在的确认弹窗；没有重复点击。正在同日另存首任务，按实际SAV核Q/T及原始收益保持后才推进。

14:39启动后件0f3445bc5eed268eadca3f6bafccbe10f082ecc92854c61646ffb355283aee88，30项独立守卫全部通过。唯一局势16777223，source Planet90、progress0、Q17/T41；源星102、母星5897保持，未迁入种子、未结算或制造。实际真实经济库存及三系bank保持；经济模块中的科研缓存镜像发生刷新，不能把该缓存当真实科研储备或宣称整模块不变。首张局势画面有鼠标提示遮挡CG，不作为干净图库来源。

有效月与原生咬合方案（实施前）：使用现有scroll命令的0滚轮量将鼠标移到右下空白，重新GPU实拍并人工查看；不点击取消方案。正常关日志后先唯一推进1日到2206.11.02（进度仍0），再分别360日到2207／2208／2209.11.02，对应12／24／36月，随后120日到2210.03.02为40月，30日到2210.04.02为41月结算；每段先检查完整原生日历回执、实际SAV和新日志／待选，再允许下一段，不重发已经完成的日历。新priority_terravore_active_month_guard.py只读绑定前后SHA、实际日差及回执，核指定有效进度、Q17/T41、唯一原任务／目标／合法石质蜂巢政体及物种、原母星绑定／核心／D2、C/G/made/worlds仍0和未提前通知、原AP传统保持；核源星真实d_lithoid_devastation数量，按一年一次预计12／24／36月为2／4／6、40月仍6，实际不符保留FAIL后查时序，不修改期望伪造通过。记录真实两星人口、岗位、原版吞噬消息、矿物／合金／科研及月预算，不能凭总人口变化推断纯自然增长或把原版随机人口计为EEP制造。结算另用独立守卫验证C17/G0、D6／增4、made0、worlds1、全部实际本族回迁、源星破碎及任务清理；本段活动期守卫不能套用结算。女王通知正常显示／确认与重载防重另留独立证据，不把首颗吞星完成当全路线验收。

14:45首日及第12月各26项活动期检查全通过：2206.11.02／aa747f2e86dc493280364268c34deddb6b7c6cd2d3c58ab9fe64a3fdd82a4b22仍progress0、无损毁；2207.11.02／2297a4a04d2fc11af99ead055673580b523d98a4d37a35d5fac0f88e249e8947实际progress12、source新增2个原版损毁地貌，冷却刷新359日、毁坏19.97882，EEP仍C/G0／D2／made0／worlds0且无待选／新error0。两星实际母星5848／源星227、总6075；不从这一个年端点推断确切自然增长、迁移或原版随机奖人口。自然完成tech_bio_reactor并自动续选tech_genome_mapping。矿物889.318／净−7.202、能源1541.292／净1.689、凝聚1125.17168／净22.59726，短期库存足够下一年与首吞结算，但矿物维护为负，不能称经济闭环；首星完成后必须正常付费补矿物生产并核稳定预算。继续按既有计划唯一360日第24月，不授予资源或额外收益。

14:49第24月实际2208.11.02／aadbd45b0ec57810673c058b0f3cdd74000f18c5c7ad12358a276458fafa2fab，进度24／原版损毁4／EEP未提前结算，活动守卫25true，仅无待选FAIL保留：pending13／first_contact_critters.85，root接触0／from国家20（虚空之云），正常UI唯一“远观而不要玩。”。矿物774.70136／净−11.877、能源1524.37736／净−4.216、凝聚1445.58018／净30.54359，母星5920／源星233；库存仍足首星剩17月，负维护如实保留，不宣称经营验收完成。

原生虚空之云接触完成方案（实施前）：first_contact_NPC_country_types_events.txt:1094的非唯心选项内部index1，启用母星CLOUDS_PROJECT并执行finish_first_contact_effect，不能当零收益叙事。first_contact_effects.txt:167与:773的效果包括first_contact_completed20／void_clouds_encountered原生flags、接触结束／情报及调查技能、正常影响力奖励；当前政策first_contact_attack_allowed，使用00_scripted_variables.txt:118～123的6个月收入、20～80上下限，当前6.1753预计37.0518。只正常选择一次、按实拍暂停日期唯一保存，读取真实影响力／项目／接触完成状态，原选项history仅pending13一次human1/index1；新priority_terravore_cloud_ack_guard.py只读核相应真实变化、其它全部实际库存科研／EEP变量flags／任务24进度／两星人口岗位与核心／科技AP传统严格保持、无新日志及待选。原第24月FAIL保留，不能重放日历或选项。接触完成后以新端点续推第36月。

14:53正常选项后仍2208.11.02／1888c8eef092ab6ca2a8887054bd383763ce0308a876cb92d30a28011dd9d5ce，pending13/index1/human1仅一次、项目启用、contact0.status=finished、全部EEP及真实其它库存科研／两星状态保持、新error0。27项中26true，原影响力精确小数预测FAIL：实际634.66874→671.66874，即+37整数，与未取整预测37.0518相差0.0518。不能把实际值改写37.0518，也不能由单个案例推定引擎通用向下取整规则。新增独立priority_terravore_cloud_ack_corrections.py只读绑定同一SHA及原FAIL精确仅此项，其余26true；核真实+37、位于原版20～80上下限、距离当前6月公式不足1且为整数、正常finished及项目source为母星Colony0。不追认原小数公式检查通过，仅补证真实原生整数奖励与EEP隔离，旧FAIL不改、不重放奖励。随后可从无待选真实端点继续第36月。

首星结算与真实边界进一步设计（实施前）：第40月端点先从完整SAV保存源星全部人口组及物种、本族原生岗位、两星last_month/current_month_growth_data、完整country0 budget和原版消息；第41月后新priority_terravore_first_settlement_guard.py绑定两个原件及30日日历回执，必须核C17/G0、D6/last_capacity4、made/last_manufactured0、worlds1、source eep_return_amount与国家eep_last_return相等且为真实本族数、源星pc_shattered/无殖民/无人口/无地貌、所有结算防重标志、active/native/being_devoured及对应modifier移除、原局势消失、唯一母星／尺寸18／永久容量6／王庭／核心地貌保持，母星人口接收与全国净变化结合真实增长及原版随机人口消息独立解释。原生咬合最终补齐6次（此前3年共6损毁，剩11槽需要ceil(11/2)=6）；最终清空地貌后不能由零损毁误称没执行原版效果。确切随机奖励数额和人口组变更若不能从原件严格归因，单列未完成项，不把EEP变量自报当独立经济证据。第41月可能只设置eep_notice_pending，按实际SAV决定是否再自然推进到下一国月脉冲显示eep.11，不用console触发。结算前后原生重新载入与通知确认防重须另存，未经完成不得写完整首吞回归通过。

边界隔离细化（实施前，替代最后一次整30日）：既有有机路线曾在月首达到进度、次日eep.21才结算；本次不预设相同时序，第40月之后改为28日至2210.03.30、1日至2210.04.01、1日至2210.04.02，总日数仍30。每次唯一保存并只读核实际进度／是否结算／待选及真实增长预算。如果04.01尚未结算，使用它作为结算前原生相邻日基线，独立核源星实际人口加最终原版随机奖励、母星精确接收和真实库存差；若04.01已经结算，则按实证保留包含月结的范围，不伪称次日隔离。原活动守卫仅允许progress<41，不能将它套在最终月首；这里新增边界观察仅记录实际，不用临时修改生产脚本强制结算时机。

14:59第36／40月各26项全部通过、无待选／新增error0。第36月2209.11.02／3ad1e817ba52ec52d7cabe30e199743e5231588d6f2cc261e1af7424751afe9a，损毁6、母星5997／源星339；完成tech_automated_exploration／tech_engineering_1／tech_genome_mapping。第40月2210.03.02／2af7b7efdfb31b1d2ac2885eb026a6964a8fa7736fb96c36121a16727fae6260仍损毁6、进度40，母星6024／源星340、EEP初始账本完整保持。新只读boundary_observation保存两星原始growth块、真实库存／预算、各物种人口及原版咬合消息，明确为观察、不单独作为结算PASS；按上述28+1+1日实际边界继续。

15:02月末2210.03.30／8fea6bb708761a304d74d35a37c9534b2b76973fabf4371aaa8aea73d6dd9d6b的26项守卫通过，仍progress40。月首2210.04.01／065fdc3fd989159b9dae0144bfc9cdbaa1c0a1b8cf195aeba05ee29e56a5581d实际progress41但未结算，EEP仍全部初始账本、无eep_pending／女王待选，源星340／母星6030。真实月结母星+6、矿物−13.92604／能源−2.75594／合金+18.473等已独立留证。该月首可作下一日结算前基线；继续唯一1日至04.02。独立结算人口核对使用本次真实原版POP消息数×100加月首源星340，对照实际return_amount和母星／全国净增，不凭EEP自报造人；原版合金／矿物消息与真实库存差逐项记录，非相关经济库存应保持，科研每月在2日正常投入需单列实际队列变化。

15:04结算观察2210.04.02／d44daf85c33e488e82bb70050d12f1d2c2c341466deed607ee2e19a3cf7b889e：C17/G0、D6／增4、made0、worlds1，return440、母星6470；原版最终POP消息1条／合金2条／矿物2条，均日期04.02／target90，真实库存+100人口／+200合金／+997矿物，其余实际库存含三系bank差0。此前“剩11槽补6次”为漏算原生已有区划和障碍的预测，已被真实5条咬合消息否定，不能照抄为结算结果：月首size17、损毁6、d_toxic_kelp原版−1、仍有1级district_hive，按剩9槽ceil(9/2)=5，与消息吻合。最终一槽的矿物分支value3、其余一次矿物分支value5，原收入124.588，623+374=997与两项逐笔四舍五入到整数相符；这里只作本例计算复现，不凭两个案例宣称通用引擎取整定律。独立结算守卫将核消息顺序／数目／日期、真实人口与库存差及这项公式复现。

原生清理语义补充（守卫实施前）：源星已无owner/controller、pc_shattered、地貌空、active/native/being_devoured及modifier已清，任务原对象带killed=yes。本机仍保留source.colony=15缓存引用与零人口Colony15对象（无拥有关系、pop_groups空、actual0）；不能用“Colony对象物理消失”作错误验收条件，也不伪称引用已移除。守卫要求country0拥有列表精确去掉15、任何实际source人口为0、全部六个结算防重标记完成、任务无active、母星原实建区划完整保持。后续重载／月脉冲继续验证这些原生残留不导致再结算。

15:07首星相邻日结算31项独立守卫全部通过：真实原版5消息与人口守恒／库存、C17/G0／D6／made0、原实建区划未自动增加及唯一核心均核实，仍不算完整路线通过。接续29日至2210.05.01，预期eep.2清除eep_notice_pending、设置eep_first_notice／触发eep.11；只读核实际事件与生产eep_report新增显示变量，不预先用“所有变量原文恒等”拒绝正常显示刷新。

女王待通知重载与确认方案（实施前）：新priority_native_checkpoint_reload.py仅封装既有r.native_load与r.native_save，把唯一已归档通知SAV原字节复制到新短别名后从原生简中读取、同日唯一另存；要求载入别名SHA与原件一致，全部真实库存bank、EEP账本／flags、AP传统／科技／政府、实际人口组岗位／母星及源星地貌区划、事件targets和原pending/history保持，记录完整未过滤日志、UI/OCR及所有原始差异。无工具grant、无重放日历或选项。正常通知唯一按钮确认前实拍，确认一次并同日另存；新priority_terravore_queen_notice_guard.py核原pending=eep.11仅一项被删除、history对应human1/option0仅一次、除待选与历史外所有上述真实游戏状态／经济保持。任何原始FAIL保留并严格补证，不能通过删去未知差异泛化通过。确认后的下一自然月另核无重复通知／EEP收益及真实负维护；正式经营仍待正常建设修正。

15:10待通知重载原严格24项中20true、4项FAIL，原件与全部差异保留。原件27a858a6f8239645aeb1fae162ee369ae88d05333d0bbc36ad1eafdb25cae968，载入别名SHA相同，后件5533ebff66daac20e33f301601b67585d049a869f5d8270c17693d9c4e84e368；同日2210.05.01、eep.11/pending18与选择历史、真实库存及bank／全部人口组岗位／EEP账本flags／AP传统科技／区划地貌核心保持、无新error。4项差异精确为：government.unlocked_civic_council_slots0→4；budget current_month部分贸易／维护工蜂及人口矿耗刷新、income_high_water_mark.trade100.62353→111.036／length6→7；母星amenities17341.2→19308、free_amenities13465→15431.8、civilian2498→2945，残留Colony15新增binary_flags24；Planet7及90的carrier_binary_flags1→3。预算矿耗64.70→64.77与月首新增7人口一致，但尚未独立证明所有刷新和议会槽位变化的引擎来源，不能统称已证实的原版警告或强行放宽后报严格重载PASS。当前仅可确认无二次发奖、待通知保存；全路线重载仍未通过。

同日二次重载对照方案（实施前）：从上述真实后件再次原生加载唯一短别名tpqueen2，复用不可变同一个24项严格辅助；没有选择pending18、不推进日历或重演收益。核实际gov／planet／colony及当前经济预算是否稳定，所有差异／原FAIL仍保留。如仅income_high_water_mark历史计数变化，也须记录确切路径与值、独立补证而不改原24项结果；如继续出现贸易／舒适度／实物资源或人口变化，则停止后续日历并按实际异常调查。此对照只定位重复性，不代替无Mod根因对照，不能因此宣布第一重载严格通过。

15:14二次重载后件3d9d717a0b0edd96a7bf2695e20b5962946618325e683061bd5b391fd8960241，原24项23true、budget一项FAIL保留；gov／舒适度／civilian／planet flags及全部实际库存／人口／EEP与通知均完全稳定。预算完整原文精确仅income_high_water_mark.length7→8，current_month／last_month及该high_water_mark的其它所有字段不变。新priority_terravore_second_reload_supplement.py只读绑定原FAIL精确此项及原SHA，核该唯一字段、整个budget其它原文严格恒等、原23项仍true、无二次奖励；不抹去两次原严格FAIL，不将首轮缓存／议会槽位变化追认成已根因证明。正常女王通知已有实拍唯一“余烬归于吞噬之心。”，允许从此第二真实端点确认一次再作24项同日保持核账。

15:15二次重载八项严格范围补证通过；首次缓存／槽位根因对照仍待补。正常确认女王pending18／option0／human1一次后仍2210.05.01，433682d68e5ba6a0791bff24e3682b21acc7bd8db6d82925c4135fb245f4d3fc，24项确认保持全部通过，真实预算／库存／两星对象和全部EEP不变，无二次发奖／新error0。

通知后首月方案（实施前）：从该真实确认端点唯一30日至2210.06.01，新priority_terravore_postsettlement_month_guard.py只读绑定实际日历和SHA，核C17/G0／D6／made0／worlds1及全部EEP变量flags严格保持、无待选／新EEP任务／新咬合消息、源星仍无拥有关系及实际人口、唯一原始母星核心／容量／实建区划保持。读取原生mother.last_month_growth_data的实际growth，独立要求母星与全国人口净变化精确等于此正常增长，不凭自报EEP变量排除造人；八类经济库存差与本次实际last_month.balance逐项核对，三系bank及科技／AP传统实证记录，不能将转正缓存或单月库存足够当长期经济闭环。若预算残差或通知／收益重复，保留原FAIL再调查，不跳过进入后续日历。完成这个稳定暂停端点后归档本轮首星全原件、更新清单并提交推送；后续仍优先修正真实矿物维护和继续噬岩者完整路线，铁心灭绝者保持下一优先级。

15:18通知后完整30日到2210.06.01／97b61a787f4fdde1c72452babc5410199af4fe2574de49b022117999dd814382，19项全部通过。真实母星6477→6484，等于原版last_month_growth_data的month_start6477／growth7；C17/G0／D6／made0／worlds1、flags、容量与核心保持，无新待选／通知／任务／咬合消息，八类预算残差全0／新error0。矿物1538.84734／净−11.682、能源1475.06106／净3.289、合金1908.616／净18.473、凝聚1995.41426／净24.71361；只证明本月真实预算闭合，矿物维护仍负，不是长期单球运营闭环。

当前稳定接续端点为上述terravore-postsettlement-month，玩家AI关闭／三系原生自动研究开启、无待选，生产0.2.0未修改、Steam持续离线。首星自然吞噬／女王确认与次月防重已完成分项，首次严格重载根因、真实付费增矿／能源岗位、正常传统与前两AP、完整灵飞／武灾／蜂巢母星及长期回归仍待做；不切换铁心灭绝者抢先验，不改变公开仅推荐纵火本能的范围。按既有归档工具生成first-swallow checkpoint，保存本轮所有原图、OCR、原SAV、执行源码、原stdout/stderr/rc、原FAIL和未过滤日志；此为活动暂停快照，不是正常退出或完整路线归档。

15:20[first-swallow活动暂停快照](evidence/priority-terravore-progress-2026-10-09/first-swallow/source-snapshot.json)已归档2256份原件／82771784字节；两张新增工坊候选、两轮重载原FAIL、原生事件及所有范围补证均保留。归档时没有活动GUI辅助，PID23824暂停于2210.06.01；未正常退出，不以本快照声称正常退出或最终运行归档。继续按原字节暂存核验后提交推送，生产文件／版本／changelog无改动，无Steam在线或UGC操作。

15:22[Git暂存原字节核验](evidence/priority-first-swallow-staged-verification-2026-10-09.json)2277个blob／83587983字节通过，范围包含本checkpoint、准备原件和既有顶层priority凭证；git diff --cached --check通过。原始失败与其后独立补证保持各自原文件，不通过改hash或覆写结果追认通过。
