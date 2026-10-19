# RC6 Purifier 后置母舰UI证据检查点

## 目标与范围

新建独立 `docs/evidence/1019-rc6-purifier-mothership-ui-v1/`，不覆盖已封口migration checkpoint。仅选择固定run `20261019T150008Z` 中Purifier经济worker之后已完成的r6pu阶段UI：after-queen／mother／queen／contact／crisis／tutorial／advisor／designer／ship-maintenance等实际截图、OCR、actions，保留全部失败attempt。经济mNN／yearui原生保存及collector重复内容不复制，引用已存在 `docs/evidence/1019-rc6-economy/purifier/` canonical。

root交接实际母舰fleet150／ship1077／design1918，C0；年末UI SAV SHA前缀79c49…。维护hover原图视觉读数为energy10.07、alloys2.88、海军容量115/66。数值以原图和既有经济SAV交叉绑定，不据静态计算冒充UI读数。colossus_review正在独立整理实际50槽／6核心的冻结源推算供电余量+9743，等待作者文档／analysis及逐源hash封口后合入，必须标明source-derived，非UI供电取证。

## 设计与边界

先核明确阶段与经济worker界线，写固定selection白名单，再复制原字节并逐源／副本bytes／SHA核对。仅枚举r6pu相关文件，不读取r6hvc／Hive／活动日志，不操作UI、游戏、Git或Steam。manifest／Mod源复用本run既有canonical；已归档经济raw不重复拷贝。新analysis、文档及typed project-relative source引用按作者稳定白名单保存，不改原报告。

教程遮挡时的早期点击只能记录为受遮挡attempt；真正posttutorial hover／click后仍显示details、没有打开editor的现象须按原图描述，不能把早期遮挡图当作编辑器行为的证明。upkeep UI、actual design raw与供电源计算分别提供来源，不能互相替代。未知、截图／OCR不一致或失败都保留，不外推完整configuration／全Mod通过。

已核经济M12原回执 `observed_at_utc=2026-10-19T15:32:18.003661+00:00`，date2201.01.01，SAV完整SHA256 `79c49aaae6660f341c7f3e08751a415405e44c4d139d465367a8b07870b393b0`，与yearUI同字节。经济receipt副本mtime为15:36，晚于一部分真实后置UI，不能把这个后写mtime当作worker结束时间排除较早母舰图。选择固定已知post-M12阶段，另保存exit-console前后／exit-debug等实际早期探针；排除15:21–15:24的旧档退出／新局选择／启动、economy重复及一切Hive。

已只读查看三份本地原图：maintenance hover图清楚显示energy图标旁10.07、alloy图标旁2.88及顶部115/66，原OCR把两数合并为“维护费：10.072.88”，不改OCR文本；`actual-designer-result`存在“建议初始化完毕”教程覆盖，而`verified-designer-result`无该覆盖、仍是舰船详情窗口。这是对这些静态帧的视觉观察，不声称未捕获的后续行为。原图／OCR／click坐标一起保留。

power作者已封口31文件加delivery-index共32文件，root已严格逐byte／SHA核验并提交，明确允许新UI小包直接typedrefs引用 `1019-rc6-power-source`，无需重复复制。该bundle中的modifiers.log是已封存generated static documentation原始来源绑定（不是error／运行终态日志）；本包仅读取项目内封存副本，不读取当前run的任何活动log，保持作者report／index及全部来源事实原字节。新包payload因此仅85份UI，power32文件和既有经济源以canonical引用保存，另明确source-derived+9743非UI读数。

尝试将catalog绑定到旧RC5停止后副本时，SHA核对未通过，尚未复制任何payload即拒绝；因此不声称旧RC5 catalog与作者4bc7…副本同字节，也不拿旧版替代作者的实际生成来源。按root已授权的32文件canonical方案直接引用已封口project catalog，不读取活动run catalog，不改作者源或既有归档。

## 验收标准

只包含授权Purifier后置阶段；所有图／OCR／action原字节齐全，选择范围与排除经济重复明确；实际yearUI／母舰身份／维护hover可追溯；source-derived供电分析逐源hash和typedrelative refs一致；独立index／verify核对全部payload和canonical引用。已有migration／经济证据不修改，不收Hive或活动日志，不commit／push。完成后交root与release_pipeline可复用的精确路径及限定结论。

## 已完成结果

新小包 `docs/evidence/1019-rc6-purifier-mothership-ui-v1/` 已封口：仅85份UI原件、5,077,506字节、22组图片／OCR。完整selection SHA256 `a29119e07d59a686fd1dbe0d99d5d951a890de414436cb4e2af7dcfa0cfd8a84`；index SHA256 `1af328168e120469fa168a7bdeb4f50621e8ff53303c99221dfbc3c21309f661`；独立verify SHA256 `cac86b4342f84dc7043920bd30031ccd381f8ac0eece3fe557241e6db77edf6a`。全部后置图时间晚于真实M12 observed_at15:32:18，而不是按晚写collector receipt的mtime筛选。

32份power canonical与13份经济canonical共45引用逐hash一致；130个typed project-relative refs已核，清单SHA256 `59bd3f592e41bc7e2ee903d4a2d6d8352e53e3c7e08b72f31e9e138d672a63cd`。yearUI／M12同SAV与receipt／audit／gamestate绑定，设计1918全文及12段原生状态摘录存在于该原始SAV，raw `eep_c=0` 可核。实际50槽+6 required、56组件／22类全部source-bound，26份源副本逐SHA核对，独立重算14300−4557＝+9743。数据保持SOURCE_DERIVED_NOT_UI_MEASURED，未读取active catalog，只读root已封口project生成静态catalog；旧RC5 catalog不同SHA不混同。

维护10.07energy／2.88alloys、naval115/66由本地原图视觉独立确认；OCR原合并文字不改。教程遮挡的旧attempt与真正posttutorial hover／click仍details的帧均保留，不能把早期遮挡误当UI按钮结论。`observations.json`（SHA256 `0b9c67a4dbe8a54ae60c3e996faaa80633331c8bbf2181429a87386d9d549048`）明确区分这些事实、数值适用范围和源推算供电，不含Mod或UI power PASS。

未收Hive／r6hvc、活动logs、经济重复SAV，未操作UI／Git／Steam／生产或工具，既有canonical原字节不改。交root／release_pipeline引用后停止写新封口目录。
