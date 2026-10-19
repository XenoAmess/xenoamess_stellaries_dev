# RC7 三新局经济与石质蜂巢接收计划

只使用简中，由root独占原生UI执行；本次仅离线计划，不启动UI、不读活动日志、不写工具或夹具、不提交。RC7完成独立静态门禁并绑定真实run manifest后，三个政府全部重新开局并各采12个月，不采用RC6 source bridge。

| 顺序 | 原生帝国 | prefix／government | 复用0.3.1基线 |
|---|---|---|---|
| 1 | EEP 04 种族洁癖 | `r7pu`／`purifier` | `1019-baseline/bpm00..12` |
| 2 | EEP 02 有机吞噬蜂群 | `r7hvc`／`hive` | `1019-baseline/bhm00..12` |
| 3（最后） | EEP 03 铁心灭绝者 | `r7mc`／`machine` | `1019-baseline/bmm00..12` |

复用现有 `runtime_single_homeworld.new_game` 的新局流程与 `runtime_economy_1019` 采集器。每局确认实际选择、200星／3AI／尉官配置及2200.01.01原生m00保存；只从该局真实 `<prefix>m00.native-save.json` 解析国家、Mother身份、history与 `written_at.parent` autosaveDir。helper遇截断／模糊标签应保留失败图并由root用实际观察行处理，不猜坐标或未来ID。

采集器最短现有入口（模板中的路径、tree由该次RC7冻结gate与实际m00回执确定）：

```text
py -B eat_everything_origin/tools/runtime_economy_1019.py --anchor-receipt <真实m00.native-save.json> --prefix <r7pu|r7hvc|r7mc> --government <purifier|hive|machine> --expected-tree <已核RC7冻结SHA> --expected-version 0.4.0-rc.7 --execute
```

必须显式传tree／version，采集器默认仍是RC4；省略 `--autosave-dir` 即从真实回执解析，不猜新银河目录。采集器原生只推进12次独立 `fast_forward 30`，逐月固定m01..12的autosave、audit、HUD／OCR、输入／Enter和receipt，最后原生另存 `<prefix>yearui` 并比较m12。不要改为一次360天。自新局到总receipt完成只运行此受控链，不注资／贸易补贴／关岗位／拆舰；后置功能另起prefix和分支，四项操作约束由root结合实际动作链审核，不称全系统输入审计。

基线仍用 [baseline-economy-observations.json](evidence/1019-baseline/baseline-economy-observations.json)（SHA `c9aca4b4aa60390df421b0f89e808590916c53cb7c6cabc07273a09e9eb61c87`）；39份m00..12原SAV已确认存在。每局接收m00＋12monthly＋yearUI及总receipt，以真实日期／SHA配对同政府基线；独立读取前期／本期完整budget parent与categories、stock、真实岗位／人口／殖民地与启动flags，保留原始值和所有异常。完成的月份可立即并行只读分析，原始文件原byte／SHA冻结；新RC7索引按真实manifest／候选tree独立建立，未齐或未审的case保持PENDING，不改旧FAIL或final-result。日志只在真实stop后另封。

## EEP05 首月与本国非核心PK

当前 [preset](../testing/single-homeworld-user-empires.txt) SHA为 `4ce9d9217a7ed804776a41e8ac73410bd70d5073bc3379aa55c2c46181938646`，与已封口 `fixture-after-gender-repair.txt` 逐byte相同；EEP05 `ruler.gender=female`，species层的 `gender=not_set`未误当统治者字段。原生LITHOID/lith11、trait_lithoid＋trait_hive_mind、hive authority、吞噬蜂群＋苦行 civic 的既有六份主要规则文件此次SHA均未变，与[原生来源调查](evidence/1019-eep05-design/native-sources.json)一致；[单字段修复记录](evidence/1019-eep05-design/fixture-gender-repair-v1.json)保持。已知“统治者性别未选定”缺陷已在静态夹具消除，无新增静态冲突；实际选择／DLC资格仍由本次原生新局确认，不扩展或修改fixture。

EEP05单独新局（建议 `r7lh`）保存真实m00；一次 `fast_forward 30` 后固定首月原始档／HUD，按既有8项要求核单母星、正确类型、人口、初始能量200、自动吞噬关闭、发电岗位、首月电力非负和正常维护。不要把这局混入三政府12月序列或改成第四份年度基线。

首月证据封好后再转独立owned-PK功能分支，沿用[现有Li接收设计](rc7-functional-offline-receiver-1019.md)：真实本国非核心天然殖民星、size3／原生旧损耗deposit1／q2／founder300；对象ID与Mother/core均从该局实际SAV取得。保留ready、该银河原生objective校准／恢复、实际武器订单及90／30分段、prefire、即时与稳定完成、重复／reload；预期C+2／G0／D2／made0，损耗只扣一次，人口收益按prefire资格独立算，原生随机奖励图／消息分开记录。全部命令与UI动作仍由root依既有方案执行，不在本页新增夹具接口或用手工callback代替实际发射。

本轮只核现源／静态映射：经济采集器SHA `d5f6a21fd2408779ae7b6494bacb21d83e5cb3245644af1c69673006749d56f0`，newgame helper SHA `cb0d2d2469c47183eac3211148bbf6c9e51b263bc719c35bfb9981e18326ea34`。执行时以root新worker实际封口来源为准；没有读取未来RC7样本或预填结果。
