# RC7 高等级成长与报告 UI 的限定绑定

本页只接收 run `20261019T164112Z`、tree `61b34f6dbdc277c44364889d5f1e1cd2773a4624786bbf0d538079fc6ba4feb0`、版本 `0.4.0-rc.7` 的固定原生证据。主线程独占游戏、UI、日志、进程、Steam及Git；本分析不发射、不更改Mod、原checker、已sealed九节点报告或正式growth report。已固定 `r7evready.sav` SHA256 `e6f07c2c8b3b28908af8d4995fed2fcf41bbb7ed82afec1f7b28b0f8e492ec9b`，原生receipt日期 `2202.08.07`。这是人为设置C20500、经预算补月后再FF6刷新缓存的压力分支，不能当自然战役累积、干净新开局或全年经济。

先读取 ready 的实际 native-save receipt/audit/SAV，以及已完成 `r7ev-mother-details.jpg/.ocr.json`；hover清理图、eep.100 top/bottom图和关闭后 `r7evreport` SAV 仅在主线程确认固定后读取。不轮询或预读在写文件。每个新SAV完整observe一次，后续复用固定解析；若成长线程已有同SAV完整观察则验证其hash和完整source绑定后复用，避免重复CPU。

验收范围包括实际C/L/next10、B410/R410/P0、六country/fleet tier镜像与实际AUX6..11装备；唯一缩放成长modifier及倍率；原生三防current/max与同舰同国C0截距加预声明固定系数。H=H0+1500L+3000Nh，A=A0+1287L+2574Na，S=S0+2091.375L+4182.75Ns；来源模型和本轮C0原生截距分别绑定SHA，不按ready结果拟合。HP容差只沿既有 `max(0.01,8×binary32ULP(expected))` 工程合同，不重新扩大；原严格比较完整保留。ship export是上次采样时的变量，若其未在本次压力状态重新导出，只记录其时间边界，不能当新值。

详情UI逐项绑定实际图、fresh GPU/OCR metadata、PID、日期与截图SHA。原生SAV精度、UI整数/小数显示、OCR截断/误读分别报告；装甲数字被面板裁剪时不能伪造尾数。speed/evasion/平均damage只认证实际面板显示，不能把damage当战斗DPS或源modifier，把满血当已实测恢复。清理hover图如果仍缺项则保持PENDING。

eep.100报告要求实际top与scroll-bottom图覆盖C20500/L2050/next10/B410/R410/P0及六tiers；每个值与ready及关闭后report-SAV的原生字段绑定。只在实际close后save固定再比较，分别列完整rawZIP/gamestate/原strict差异；报告打开/滚动/关闭输入图绑定，不能由SAV同值推断UI真的显示。业务字段零变化可局部通过；若图、OCR、SAV不一致、截断、字段缺失，保留差异和PENDING，不补未来PASS。

最终仅输出新 immutable观察/限定报告/具体finalcheck提案材料。可能支持 `unlimited_growth.report_level_count_remainder` 的实际UI部分，以及高等级属性展示；不能自动补齐完整motherconfig、实际自然回复、真实jump/供电/维护、新局年测、全组件所有门槛/重载、整18case。原九节点/正式growth报告保持原字节。

## Ready与固定图的实际事实

ready完整observe已固定为 `evidence/1019-analysis/rc7-r7evready-ui-observation-v1.json`。实际Mother fleet125/ship809、design16777257、core物理4，C20500/L2050/next10、B410/R410/P0；六层按shield/armor/hull/damage/tracking/regen为63/74/76/63/56/78，合计410，country/fleet镜像一致。单个永久 `eep_mothership_evolution` 的multiplier2050，没有多个成长修正堆叠。

三防current均等于max：H3396960、A2873613.6、S4718142。以已sealed同舰C0原生截距93960/44787.6/167310加固定每级和对应core系数，三项预测与实际逐项精确相等。详情原图与清hover图均为PID37300、2202.08.07；显示H3396960/A2873613/S4718142、speed417/evasion22.1%/damage122780.71。A整数显示没有包含原生`.6`小数，不能从UI填出完整精度。两图均已独立view_image，不只根据主线程摘要填写。

ready船上`eep_probe_max_hull=1725960`、`eep_probe_max_armor=1427025.6`及十modifier exports仍是上一次C10000导出状态。本压力分支未承诺重新export，因此这些变量记录为旧诊断缓存，不能当本次20500的current modifier，也不能为迎合当前health改写它们。原生current/max字段独立用于本次三防断言。

主线程已确认报告单页足够，固定 `r7ev-report-top.jpg/.ocr.json` 已独立查看：C20500、L2050、next10、应得410/已发410/待补0，以及六层63/74/76/63/56/78全部可见，无需制造额外bottom滚动页。再生78正常换行，实际截图/OCR两行共同覆盖。打开/关闭后的SAV仍须等主线程确认后再读。

冻结源 `events/eep_events.txt` 中eep.100 immediate调用`eep_report`；`common/scripted_effects/eep_effects.txt` 的该effect重新计算展示用level/remainder、tasks/waiting、core人口/空余等缓存与report event targets。关闭后完整strict可能显示这些实际写入，届时原样保留，不设置ignored paths。界面“报告只读”不能解释为gamestate完全不写展示缓存；经济五账本、库存、人口实体/岗位、设计/健康、真实tiers与奖励业务状态另行精确核对，不把展示缓存改动自动当结算或实际回复。

## 已完成阶段的小包归档设计

主线程已确认`r7evreport.native-save.json`固定，原生SAV SHA256 `0d64de5652563ebbc2a453e47c7298ceecabe0392b95562cd5ed967060d42b97`，同日2202.08.07，worker退出0；整个r7ev前缀不再写入。现在才能读取report后SAV并生成完整独立报告。

本scope小包使用新目录 `evidence/1020-rc7-high-level-ui-v1`，只白名单该固定run的`r7ev*`已完成原始文件（ready/report两SAV、原audit/gamestate提取、精确native-save receipts、对应原生保存输入/动作、已完成详情/报告图与OCR），以及本分析新观察/报告/提案和本文。源文件逐个原字节复制，记录原绝对路径、相对归档路径、大小及SHA，复制前后源SHA/大小必须不变，独立重读全部目标验证文件集合/字节；`.gitattributes`强制`* -text`。不拷活动日志，不把原生源文件改名后宣称产生了新save，也不收root之后的新游戏数据。

原run manifest以原字节小文件绑定；59个copied Mod/source/static和已sealed九节点/正式growth大包只引用已有canonical包的实际项目路径/index/SHA，不再复制。如果canonical尚未固定，索引明确缺项，不造路径或捏造source闭包完成。不要把本局部压力UI小包当完整motherconfig或整18组最终证据。

归档前的附加全局gamestate LCS逐行diff在大量重复行上耗时过长，已中断该只读分析助手，未产生报告或改任何源文件。最终改为保存原生完整ZIP、gamestate SHA/字节相同性、原checker完整21条严格差异；不对原strict删项或修改判定，也不声称另做了全局原文LCS证明。

## 实施时发现并纠正的选帧错误

首份限定报告 `rc7-high-level-growth-ui-binding-report-v1.json` SHA256 `087c45dc5a468737b2494bf1dfffce9dd9abd8e7e414cbc4bfbca6874334db4e` 为55/56、FAIL，唯一失败是把`r7ev-report-exit.jpg`当作点击后的关闭证明。该图实际是`h.click_text/gpu_click_text`用于识别“退下”的点击前frame，显示报告是正确的，不能归因于Mod关闭失败。原图、原观察和v1错误FAIL全部保持原字节。

独立查看真正后继`r7evreport-menu-0.jpg`已无报告窗口：其fresh GPU capture UTC17:17:03.481827，晚于退下click action文件写出UTC17:16:56.465464；更早的匹配frame为17:16:55.713096。menu-0还早于nativeSave helper的esc-0输入17:17:03.567529，因此不是之后Esc关闭报告。后继menu-1和save-dialog也只显示原生菜单与保存窗口。新v2仅把关闭证明绑定到正确post-action帧、记录其顺序和原v1错误；原固定模型/业务断言、完整strict FAIL21条及其全部差异不变，不改阈值或增UI。

## 最终限定结果与发布映射

[v2限定报告](evidence/1019-analysis/rc7-high-level-growth-ui-binding-report-v2.json) SHA256 `e52bcb0355ee29db8552c3b95ff450da9c6b11bc9029104ed8c5ba71e598dd29` 为PASS_SCOPED，60/60检查；原strict仍FAIL21，v1选帧错误FAIL也保持原样。三个max预测误差分别为0/0/0，未用工程容差消除任何差异。报告前后全部fleet/ship、design/健康、基地、人口实体/岗位/布局、民军队列、原生库存/预算、国家原有变量/flags、危机目标、event targets均一致；核心人口4944、容量2保持不变。

完整strict21条为：8个新增country展示缓存在两套变量投影中出现16条；core实际人口4944/空余11在两套变量投影中出现4条；含这两项的新core原始块1条。实际新增country值为c_remainder0/chunks0/core_state0/crisis1/g_remainder0/psi0/tasks0/waiting0。event targets没有持久化变化。两SAV与gamestate均不字节相同；不把语义业务未变写成全档或全国家对象相同。

[发布partialcheck提案](evidence/1019-analysis/rc7-high-level-growth-ui-partial-case-proposal-v1.json) SHA256 `b4f787c9267d1b512c3568c71dc1a309ec541e5437ab4e624118e6271ad62b40` 只支持`unlimited_growth.report_level_count_remainder=true`，case总体仍PENDING。提案引用真实小包内的两SAV、receipt、图、OCR、输入、正确关闭帧，以及新v2与保留v1报告；所有其它check仍由其独立合同与实际证据填入。旧十项export缓存未变不构成20500新modifier测量，damage122780.71也不构成DPS认证。

canonical大包为`evidence/1019-rc7-growth-v1/index.json` SHA256 `fccfee53675528f2da413a70d3ba971e79d3cd5c8ccc169c0c9f63f616bc95c3`；verify为`262d25fb5775e3cfb7940ea76a6bca34dcac193c8b98d058f4390e8ff87c08ad`。正式growth报告`authored/rc7-growth-native-report-v1.json` SHA256 `4677e82c62ce30851f247691dad38703f52d6187ce26f2e63ea9fe0d7df9d1a3`、五source模型、59Mod静态包及19个纯源/执行器源码闭包均按原canonical路径绑定，不复制到本小包，不导入它们的整case结论。本分析及小包不含任何活动日志或新局经济数据。
