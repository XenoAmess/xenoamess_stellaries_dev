# RC6 Purifier 后置母舰UI小包

仅保存固定run `20261019T150008Z` 的85份后置Purifier UI原件，共5,077,506字节、22组图／OCR。完整白名单见 `selection.json`，index SHA256 `1af328168e120469fa168a7bdeb4f50621e8ff53303c99221dfbc3c21309f661`。不含经济SAV副本、Hive、活动日志或最终run冻结。

`verify.json`独立核验85个源／副本、45个canonical引用及130个project-relative typed refs。32份已封口供电资料复用 `../1019-rc6-power-source/`；13份经济canonical复用 `../1019-rc6-economy/purifier/`，没有重复原始经济数据。yearUI与M12同SHA256 `79c49aaae6660f341c7f3e08751a415405e44c4d139d465367a8b07870b393b0`，日期2201.01.01，原生母舰country0／fleet150／ship1077／design1918、C0。SAV／receipt／audit／gamestate、实际设计全文及12段状态摘录已交叉绑定。

维护hover原图可见每月energy10.07、alloys2.88，顶部naval115/66。原OCR把两数连成“维护费：10.072.88”，原文件未改。该读数仅适用于这个Purifier日期／帝国状态，不代表通用基础维护费。

早期actual-designer-result图有“建议初始化完毕”教程遮挡，不能凭该次attempt判断按钮行为。posttutorial-details与verified hover／click／result完整保存：教程覆盖消失后，点击客户端(401,602)仍显示舰船详情，没有在所捕获结果中打开editor。原始受遮挡与未打开editor的attempt均保留，不推断隐藏原因。

供电作者原报告保持 `SOURCE_DERIVED_NOT_UI_MEASURED`；56行实际组件（50槽+6 required、22种组件）及26份原始源副本全部核验，独立加总14300−4557＝+9743，未知power项为空、实际适用power modifier声明为0。这是按原生component contract与冻结源计算，原图没有UI供电读数，不能称为UI power通过。

`typed-references.json`提供可复用的screenshot／actions／analysis／native_save项目相对路径及全SHA；`observations.json`区分UI视觉观察与源代码推算。generated modifier catalog仅引用root已封口的project静态文档副本，未读取当前run日志；旧RC5 catalog原字节SHA不同，未冒充同一来源。没有操作UI、Git、Steam、Mod或工具，未更改既有migration／经济／供电归档。
