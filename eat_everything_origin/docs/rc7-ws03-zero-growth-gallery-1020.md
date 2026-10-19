# RC7 WS-03 零成长母舰配置图候选

## 目标、范围与方案

2026-10-20主线程授权补齐WS-03：只读取已封存并提交的`evidence/1020-rc7-relic-configuration-v1`，选其`raw/r7cfgui-mother-details-clean-v2.jpg`作为真实C0／L0母舰配置图，另存全新Workshop本地候选文件。旧失败v1弹窗图与封存包保持原字节，不读取活动r7jump／r7pk或日志，不操作UI、Steam、Git或正式发布输入。

以已封proposed v2为前序，建立新的proposed v3；保留WS-00～06七ID与六图库结构、四历史inline URL／SHA、WS-04／05／06已有候选源／文件／SHA。WS-03标题明确2201.01.07、零成长和同国同日原生Relic对照，不能写成2200年Jan1新开局、免维护或战斗实测DPS。同步发布草案中的当前WS-03来源状态，最终18组验收与正式冻结仍PENDING。

## 验收标准

- 源图／GPU-OCR／native-save／audit与封存index、verification实际指纹一致；同国同日C0／L0和实际母舰身份有原生报告绑定。
- 新候选图逐字节等于clean-v2原图，JPEG1024×768且低于1MB，无裁剪、重绘、合成或覆盖旧文件。
- 原生H93960／A44787.6／S167310与UI整数显示分开；速度417及伤害面板5598.57只作当时显示值，不宣称战斗实测输出或无维护。
- v3仍PROPOSED／final_release_selection=false，三张既有新候选、历史v1／v2、四inline和正式发布输入字节不变；完整实机矩阵不自动晋级。
- 独立重读所有引用、前序与候选图片，保留验证回执、准确文件清单及SHA供主线程提交。

## 实施与验证结果

已独立查看已封存clean-v2母舰图和同国同日Relic参考图，使用前者作为WS-03。零成长状态由同包`raw/r7cfgui.audit.json`绑定C0／L0／六rank0；实际母舰fleet151／ship1044、原生参考fleet175／ship1068，日期2201.01.07。原生保存`r7cfgui.sav` SHA256为`c9d8907c2ebeee3380cc0668cd20e950ac73f48dd6646a3d8a83cd35b5a7caf5`。原始配置/UI报告保留已有故事事件、危机弹窗与完整原生差异，不把UI段称作全档只读，不导入其纯经济结论。

新候选[03-mothership-zero-growth-0.4.0-rc7-2201.jpg](../workshop/images/03-mothership-zero-growth-0.4.0-rc7-2201.jpg)为194006 bytes、JPEG1024×768，逐字节等于`raw/r7cfgui-mother-details-clean-v2.jpg`，SHA256 `05943ebe60152e07978eedaa8597c97a49fcebaf3152c81af251370de5da2f7f`。未使用被弹窗遮挡的v1，未修改原生图、OCR、SAV或封存包任何文件。

[proposed v3](evidence/1019-requirements/images-manifest-0.4.0-proposed-20261020-v3.json)为17253 bytes，SHA256 `51219e3de23c34f289b120b27a5740a2abf50d0a6e2b9736a4a87ba5451057d6`。WS-03现在有真实来源且LOCAL_READY_PENDING_CASE_REVIEW；WS-04／05／06及其它三槽与v2逐字段完全相同，四inline同序同指纹，七图SHA互异。v1／v2与旧RC6图保持原字节，v3仍PROPOSED／final_release_selection=false，未自动接受任何case或正式发布。

标题为“零成长母舰配置：C0／L0，2201.01.07；原生遗迹舰同国同日对照夹具”。notes记录实际H93960／A44787／S167310、速度417、面板伤害5598.57／日和舰体身份；原生装甲44787.6与UI整数显示区别明确，不称战斗实测DPS。原生维护tooltip在该参考舰夹具的海容上下文内为每月10.07电／2.88合金，不作免维护或新开局维护结论；额外Relic只是测试参考，不是赠品奖励。

新[选择回执](evidence/1020-rc7-ws03-gallery-v1/selection.json) SHA256为`369bcd18cdb070eb33700c24054dcf5e8c56eb9ff8fb8591c0729bcfc8d15535`，记录12个精确角色引用、12个保护输入和实际维护边界。[独立verify](evidence/1020-rc7-ws03-gallery-v1/verification.json) SHA256为`4161ad74e0d4e6a9b4257efeb91d9d06a234217e4baaad5f07dc2ed36c6927b5`；新Python进程重读16项全部通过，状态PASS_BYTES_AND_MEDIA_SCOPE_ONLY。

检查包括已封配置包164份payload大小／SHA和原index pin、原生ZIP CRC及audit／receipt／gamestate绑定、fresh GPU/OCR PID37300与Jan7日期、实际C0／L0／六rank0、同国同日参考身份、真实正维护、6图库结构、其它六槽／四inline逐字相同、12个正式输入／前序／旧候选保护以及全套图片实际source字节相同。正式VERSION／descriptor／CHANGELOG／description／manifest／item-id未变，没有读取活动r7jump／r7pk或日志，没有UI／Steam／Git／Mod／工具操作。

发布草案已将WS-03改为真实零成长母舰配置候选并链接v3；六类CHANGELOG与Note正文不变且仍逐字同源，description草案仍5461 UTF-8字节，Note仍3241字节。没有新增软件测试；本次为文档、不可变来源与候选素材校验。

## 精确stage清单

本子任务未操作Git；由主线程按以下9文件范围提交，整目录只有本次5份新证据作者／回执文件，不含原始配置大包副本：

```text
eat_everything_origin/docs/rc7-ws03-zero-growth-gallery-1020.md
eat_everything_origin/docs/release-0.4.0-notes-draft-1019.md
eat_everything_origin/docs/evidence/1020-rc7-ws03-gallery-v1/
eat_everything_origin/docs/evidence/1019-requirements/images-manifest-0.4.0-proposed-20261020-v3.json
eat_everything_origin/workshop/images/03-mothership-zero-growth-0.4.0-rc7-2201.jpg
```
