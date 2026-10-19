# RC7 洁癖图库接收与候选素材冻结

## 目标、范围与设计

2026-10-20主线程确认run `20261019T164112Z` 的全部 `r7pucmedia*` 已固定且已离开该分支。先按`rc7-purifier-native-gallery-1020.md`接收设计封存这些原生图、OCR、动作、SAV、audit和native-save角色回执到新`evidence/1020-rc7-purifier-gallery-v1`，逐文件记录原路径／字节数／SHA并独立重读验证。只读取该固定前缀，不读取活动Hive或日志；通过已封canonical RC7 manifest、static和前置洁癖yearUI引用来源，不重复复制59份Mod。

对照前置纯经济yearUI与后置媒体SAV，量化实际弹窗确认造成的状态变化。后置展示不冒充yearUI完全相同或纯经济采样；父脚本保存后因大小写断言退出的事实保留，媒体独立角色成功不推导父脚本exit0。

原字节复制三个候选图到新`workshop/images/04-mothership-growth-stress-0.4.0.jpg`、`05-growth-report-stress-0.4.0.jpg`、`06-purifier-single-homeworld-0.4.0-rc7-2201.jpg`，不覆盖任何旧文件。WS-04／05来自sealed高成长UI压力分支，WS-06来自本新媒体分支。新proposed manifest v2保留v1历史，WS-03继续PENDING，不改正式manifest／VERSION／descriptor／CHANGELOG／description，不操作UI、Steam、Git或Mod／工具。

## 验收标准

- 原生媒体SAV实际SHA为`d170383d77f516a21da859e606a4061e6b0ffcc245b69c61ed267ee346263574`，receipt／audit／日期与图绑定；封存范围只包括真实已存在的固定文件。
- 选图`r7pucmedia-single-colony-clean.jpg`实际展示2201.01.01、遗落母星、殖民地1、约+46电与空建造队列；标题明确实机验收预设。全年正电须引用独立纯经济报告，不由截图独自证明。
- yearUI差异逐字段量化，未变的日期、世界、人口、舰船与经济账本等按实际观察报告；任何差异不隐藏，完整原件保留。
- archive index和独立verify逐个重读大小／SHA，引用真实canonical源且不复制59Mod；三个候选图与原图逐字节相同且互异、低于1MB，OCR／同日native-save绑定可复用。
- v2仍PROPOSED／final_release_selection=false，WS-03和最终18组验收仍PENDING，正式发布输入不变；草案同步真实WS-06来源并保留旧RC6历史。

## 接收结果

已建立[媒体小包](evidence/1020-rc7-purifier-gallery-v1/index.json)，67文件，其中58份原始payload共3,342,604 bytes，14组fresh GPU／OCR；另有两个完整分析JSON、三份可复现离线封存／素材准备／独立检查脚本及index／verify／本地选择回执。`.gitattributes`保留所有原字节。11条canonical引用核对已封RC7 run manifest、static、压力UI与纯经济yearUI／report，不复制59份Mod，不含活动日志或Hive数据。

- index SHA256：`03f25af162663a14a172217921440d6423e4bb363ea8dda21ed8c66abf3670d4`。
- [独立verify](evidence/1020-rc7-purifier-gallery-v1/verify.json) SHA256：`3d8a05ad96a04b2298b93882a0acb9fadae133ec36ff127a9a160d978f0a6db5`，新Python进程重读16项检查全部通过，状态PASS_BYTES_AND_MEDIA_SCOPED_ONLY，整case仍PENDING。
- [媒体限定观察](evidence/1020-rc7-purifier-gallery-v1/media-observation.json) SHA256：`eae08f051b097642e0c3dd250404278a4be7ec8c97a1b7e0957e5f531aac9651`。
- [完整原生字段与audit差异](evidence/1020-rc7-purifier-gallery-v1/native-differences.json) SHA256：`578133339b141f2c19c3ae23aefb649047c78552753b34fbf2a8cac5c0142851`；重复键按出现次数保留，列表／顺序／空白变化均记载，未使用数值容差或忽略路径。

已独立查看三张原图。新WS-06显示2201.01.01暂停、遗落母星EEP-Core、一个殖民地条目、空建造队列与顶栏757+46。对应原生人口4859，能源库存757.88612；current month能源收入91.61163、支出44.85872、净值46.75291。画面不能独自证明全年；该标题的全年正电来自已封纯经济报告十二样本46.23969～46.75291，四项输入操作约束仍原样为null，由主线程另审。

yearUI原生ZIP SHA为`e036f3594d980c2e7797623d948fbd7f7be0cf042b120593504a4dd627c03eaf`，媒体ZIP为`d170383d77f516a21da859e606a4061e6b0ffcc245b69c61ed267ee346263574`，两者ZIP／gamestate都不同。全audit有10条差异，其中4条为文件路径／SHA／字节元数据；业务投影6条包含同一真实矿物变化在stockpile／effective_stockpile／modules中的重复展示和三项研究库存。实际库存变化如下：

| 库存 | yearUI | 媒体 | 实际增量 |
| --- | --- | --- | --- |
| 矿物 | 446.98542 | 448.98542 | +2 |
| 物理研究 | 151.3606 | 154.4505 | +3.0899 |
| 社会研究 | 151.3606 | 154.4505 | +3.0899 |
| 工程研究 | 187.3606 | 191.1705 | +3.8099 |

完整原生递归比较另保留23条字段／结构差异：危机说明确认后country events新增`CRISIS_SPECIAL_PROJECT_1`（id1、next id2）与`crisis_level_reached=1`计数；新增`tutorial_level_picked`，非殖民行星9移除`tutorial_anomaly_planet`、binary_flags576→584；随机计数8274052→8274054；原生2条消息和4个待选事件（crisis.4140／advisor.1／eep.10／tutorial.2111）被确认／移除，相应选择历史记录变化。差异数量包含结构键列表，不等同于23个独立玩法效果。所有完整before／after原字段均保留，不据摘要声称全档相同。

日期、能源库存／预算、所有EEP成长／结算账本／六核心等级、原生人口实体／岗位／殖民地布局，以及完整construction／ships／fleet／ship_design／starbase_mgr块均保持。没有将媒体新增矿物／研究回填到经济样本。父脚本保存后跟进断言失败的事实保留；媒体角色只按独立native-save回执成功表述，未称父脚本exit0。

## 三个本地候选与文案

三图已复制到主线程指定的新文件，合计569766 bytes，分别逐字节等于原sealed源图，SHA互异，均JPEG1024×768且低于1MB。源图、OCR、SAV／audit、所有旧图片均不改。

| 图 | 新候选文件 | SHA256 | 标题范围 |
| --- | --- | --- | --- |
| WS-04 | `workshop/images/04-mothership-growth-stress-0.4.0.jpg` | `3a976a78c078417f0074703f762c085fe606721b318b3cad10c3839d20963025` | 成长压力测试：L2050母舰实际面板；人为构造，非开局数值。 |
| WS-05 | `workshop/images/05-growth-report-stress-0.4.0.jpg` | `f38882b9c4eaa37ad8906dc17a450d06cc3df19a3d9c5276013b2b12f9d8f736` | 成长压力测试：C20500／L2050，累计410次随机核心升级、待补0。 |
| WS-06 | `workshop/images/06-purifier-single-homeworld-0.4.0-rc7-2201.jpg` | `86bbe9b5e435fae8667e44a3cca349c2e9eef97c8c3f8c7c932b9d416de3fa6e` | 实机验收预设：种族洁癖单母星、首年12月正电、2201.01.01殖民地1。 |

[新proposed v2](evidence/1019-requirements/images-manifest-0.4.0-proposed-20261020-v2.json) SHA256 `16244a7d2489aadc5b563216a4cfebea0c6ee319da001fe028841ea6dd1ce440`；仍PROPOSED／final_release_selection=false，三图LOCAL_READY_PENDING_CASE_REVIEW，WS-03仍PENDING_NATIVE_SOURCE。原v1及旧RC6 WS-06文件原样保留；v2附其历史选择，未用它满足RC7 gate。正式manifest、版本、descriptor、CHANGELOG、description和四条正文inline均未更改，独立verify重核实际指纹。[选择回执](evidence/1020-rc7-purifier-gallery-v1/local-media-selection.json) SHA为`acce2189e213f7507849b4e0514e6eb5252e61d23e4eb10063e72a59f669009e`。

发布草案已填入新WS-06来源与独立经济证据边界，并将WS-04／05文件名同步为实际新候选名；未消除最终PENDING。最终WS-06需在共同审查中将本图及媒体SAV加入`purifier_startup`真实证据，才能满足发布gate。

最后定向复核15项全部成立：三文档无行尾空格／Unicode替换字符且以换行结尾，六类Note仍逐字同源，description5461字节仍低于上限，七个正式输入／历史v1／旧RC6图片指纹不变，三个新候选逐字节等于各自原件。Note仍3241字节，本次未修改玩家正文草案代码块，仅同步来源与状态说明。

## 本任务精确stage清单

本任务不操作Git。主线程可将以下文件与目录作为本轮交付范围；不包含其它线程活动文件或任何正式发布输入：

```text
eat_everything_origin/docs/rc7-purifier-gallery-reception-1020.md
eat_everything_origin/docs/release-0.4.0-notes-draft-1019.md
eat_everything_origin/docs/rc7-release-copy-preparation-1020.md
eat_everything_origin/docs/evidence/1020-rc7-purifier-gallery-v1/
eat_everything_origin/docs/evidence/1019-requirements/images-manifest-0.4.0-proposed-20261020-v2.json
eat_everything_origin/workshop/images/04-mothership-growth-stress-0.4.0.jpg
eat_everything_origin/workshop/images/05-growth-report-stress-0.4.0.jpg
eat_everything_origin/workshop/images/06-purifier-single-homeworld-0.4.0-rc7-2201.jpg
```

root原先写的`docs/rc7-purifier-native-gallery-1020.md`属于原生操作记录，未由本子任务修改，由主线程按其自身待提交范围一并处理。一次PowerShell正则引号解析引发的仓库内只读搜索已立即停止，未用于验收，未读取任何活动run日志或Hive前缀；后续只用精确路径与Python读取固定对象。
