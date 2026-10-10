# 噬岩者：完整灵能后的星海天罚验收

## 目标、范围与输入

继续用户授权的0.2.0简中离线实机验收。先完成[破境／女王通知／重复报告／完整稳定月](priority-terravore-psi-corps-and-breach-2026-10-10.md)的实际PASS及退出0，再通过正常UI使用第四个已由完整付费传统树取得的AP槽选择“星海天罚”（ap_become_the_crisis）。不授予AP、资源、科技、威慑、危机等级或舰船，不改SAV，不重发0.2.0。原有两颗已吞星球不追溯新增威慑；工坊推荐仍仅完整通过的纵火本能。

## 原版依据与分支

本机4.5.2的common/ascension_perks/00_ascension_perks.txt:194–267要求Nemesis、无其它玩家危机、独立、非监管人／皇帝、至少三个既有AP且无排斥思潮／国策；on_enabled设置became_the_crisis AI性格、隐藏timeline.69并activate_crisis_progression=nemesis_path。正式简中名从nemesis_crisis_l_simp_chinese.yml:3逐字提取“星海天罚”。

crisis_levels/00_crisis_levels.txt:16起，等级1原生要求0；等级2／3／4分别要求1000／2000／5000威慑及crisis_special_project_1／2／3_complete旗标，还要对应4120／4125／4130事件不活动。必须同时核项目真实研究、正常选择、等级与实际船型，不能只核威慑数字。

重要分支：nemesis_crisis_events.txt:904的crisis.4140优先检查is_psionic，当前完整灵能蜂巢应启用CRISIS_SPECIAL_PROJECT_PSIONIC_1，不是按蜂巢身份套HIVE_1或普通_1。后续同样先核实际事件分支／项目key。00_projects_nemesis.txt:198／324／450灵能版项目成本为3000社会／6000物理／12000社会，on_success分别设上述通用完成旗标并发4120／4125／4130。简中PSIONIC键引用普通项目名称：“凡外之物”“涌动暗潮”“万众一心”（nemesis_content_l_simp_chinese.yml:13／45／75及35／67／98）。沿用旧方案写普通CRISIS_SPECIAL_PROJECT_1/2/3仅能指代阶段，实际验收必须读上述准确PSIONIC对象，不能断言普通key本身出现。

crisis.4140“星海战栗”的immediate开始事件链；正常“这是我们的宿命。”选项增加阶段计数1并启用符合条件的首项目。项目和阶段事件的全部实际副作用须分步保存、源码互证，不沿用女王无收益ACK守卫。

## 实施方案与验收标准

1. 稳定月PASS后暂停归档完整生产原件。然后正常打开传统／AP界面，只读观察星海天罚可用条件、现有AP及槽位，采GPU/OCR。正常选取和确认一次，同日另存terravore-nemesis-ap-selected。新增只读priority_terravore_nemesis_ap_guard.py，绑定前稳定月PASS／实际0、两SHA、正常UI／保存回执与原生源码SHA；只允许第四AP及原生crisis progression／性格／事件链／timeline和唯一4140待选等源码对应变化。真实库存／bank／人口岗位／建筑区划／种族／EEP经济和女王旗标必须保持，未知差异FAIL原件保留再精确补证。
2. 4140实际待选和分支先取证，再正常唯一选项确认并同日保存terravore-nemesis-intro-ack。新增独立精确ACK守卫，核真实启用PSIONIC_1、事件链计数恰1和一次选择历史，真实收益保持；只按本次源定义的变化放行。通过后正常在情报日志启动项目，读取实际研究队列与3000成本；既有社会bank约4953可用于正常研究，是否即时完成以原件为准，不凭库存推定。
3. 威慑只用合法战争／征服／肃清／吞完新星球／其它原生目标取得。EEP eep_effects.txt:273–280只在当前有AP且星球未eep_crisis_done时完成一次crisobj_destroy_worlds。原版目标奖励受实际星系数及宜居倍率影响，destroy_worlds base150000／num_galaxy_systems、round_to50／min150；conquer_worlds base100000同样缩放；purge_pops base3000／星系／宜居、round／min3。201个galactic_object条目不必等同trigger:num_galaxy_systems，先用实际目标UI与变动验证，不预设每颗750或普通.185另发一份。
4. 扩张目标先核当前已知／已调查／可达和所属，再用正常工程船建前哨、正常付费殖民或运输舰侵占。不能把原SAV查到的未知星球当已知目标、不能瞬移、不能导入受控夹具。战争舰与运输舰均实际付费并逐笔核库存／队列；能源矿物维持正净收入，原合金−3.84925必须如实记录并正常经营修复。
5. 2／3／4各阶段分别核实际项目／威慑／等级、原生船型解锁及女王通知，正常矿物支付建造、装配、升级、超舰容／基地停泊维护入账；真实合金设施和经济不被Mod替代。采简中女王舰队通知和矿物舰队／母星图作为候选，只记录来源、SHA及当前验收限制，保持Steam离线。

各阶段都须有独立PASS＋实际退出0、无本国未处理待选及未解释新增错误，才推进下一日历。生产41文件仍不变时沿用已完成的open_kaishek包级验收；如发现生产或P引擎工具缺陷，先按仓库文档先行与对应仓库修复、验证、提交推送，再继续。本文件不宣告星海天罚或整条噬岩者路线已经通过。

## 结果

待上述稳定月与完整切点后实施。所有新增事实、精确许可、实际FAIL和后续证据回写此节。

15:19只读源码核验：08_scripted_triggers_shroud.txt:6的is_psionic为已采纳灵能传统或主体有灵能物种trait，当前两者都满足，PSIONIC项目分支据此成立。源SHA：AP文件0992582948a3ca199b30ab646720091e0207e2e58b688171d9cc501f266a720c；crisis_levels e4d8281f4cc68559f7c5c97d6e68668e5c647438c0df39d6d987857d4f34a04a；项目b09f648917aa4e91cdfe2d9a8af7a09901846f16212ba957a5606d3c82aa0a25；事件7c037b46e8b6cb8e31dab8dd69bbd34d5902cf212a5fb5c206d175aa676e7d13；objectives e5caaa3be22664c20ea341c2dac33d2d93b099abb4a2b4b361feb2e54915851b；简中crisis77a6374d7076b1c73ad64334cbb2e614599445116857c9f4bd458bf0f0f330ad／content bb7c4901ebad6da061e0791399c3ddb21eb7635e74e03a09ef11eeabda99e3ed。均为现场文件只读SHA，尚无选择AP的运行时证明。
