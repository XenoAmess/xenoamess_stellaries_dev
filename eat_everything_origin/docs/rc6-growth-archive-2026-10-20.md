# RC6 成长原始链与诊断失败归档

## 目标与范围

固定run `20261019T150008Z` 的已完成 `r6g*`：18个成长样本（9个C点各refresh／final）、repeat／原生reload与诊断probe原SAV、完整collector receipt、命令／输入动作、GPU截图／OCR、audit、原生保存／载入回执和原始growth-observation。新建独立 `docs/evidence/1019-rc6-growth-v1/`，不覆盖原报告、原样本、已封口progress-v1或经济／重复初始化包。经济年末与初始化before锚点复用已有canonical引用，不重复原SAV。

root已确认PID30812于UTC `2026-10-19T16:38:02.658777+00:00` 正常停止，forced=false／running_after=false。此包只收growth原始链；完整停后logs由独立并行线程归档，不在本目录复制。随后RC7用其它run，不读取current-run指针。

## 设计与边界

按固定artifact根的 `r6g*` 文件白名单逐byte／SHA封存，记录source与项目内路径；当前盘点455文件／22SAV。除18样本外，保留r6grepeat、r6gload、r6greload、r6gexport1、r6gbudget1全部已有阶段，不造不存在的回执。collector原receipt及18份growth-observation保持原字节，不把失败样本静默剔除。向growth作者确认已封口analysis／doc名单后原字节合入，源工具仅复制或引用可核的历史磁盘来源，不把当前工具代码冒充所有旧worker内存载入证明。

原n08七个旧export FAIL必须在独立摘要中明确保留。较晚 `r6gexport1`（预期SAV SHA `93e3f5826f10873f28a983f0660a446bdfba881d9dd6e82f8231085d5f0f4850`）只证明该诊断状态当前十个export相符，不能修饰早期失败。`r6gbudget1`（预期SAV SHA `983e06cd8af63e4b5e35b02d1fe8d639e321ea62ebb8ef0c02eaca263ecf3925`）实际R300／P110，设计预期R400／P10，保留100个补发差额为FAIL。repeat／reload的实际SHA、日期和结果从各自精确receipt及SAV分析取得，不按前缀或同SHA推断来源。

额外独立只读抽取四个post-matrix SAV的country／fleet／ship变量、日期、Mother身份、三防与design字段，复用既有冻结audit parser原语，不导入UI或运行采集器。摘要与作者原9报告分别保留；reload仅说明实际字段差异，不自行升级成完整重载验收。当前collector SHA仍为原receipt的cab98ce…，当前修正checker为原native-probe报告记录的0c31f764…，可复制这两个封口磁盘源并标明不构成历史进程内存证明。旧a66检查器及government限定修正补充、v1–v4事前模型复用canonical原件。

首次独立verify逐原source复核时，发现两份工作树source已在归档之后推进：root probe计划文档从10770bd9…变为f3f6ebfa…追加结果，当前checker从0c31f764…变为RC7的a8d70f10…。455原raw及所有原观察JSON未变；已复制的事前doc和0c31工具与selection匹配，不覆盖为后来版本。首轮verify在原source／copy比较断言停止，保留为本归档工具验证失败，不当作游戏错误。后续verify仍逐473冻结副本SHA、471现源原byte一致；明确记录两处source已推进及capture时完成的source／copy原byte核对边界，不假称两者当前仍相同。新RC7工具不复制进本包。

## 验收标准

原始payload逐字节／SHA与source一致，所有本包引用的原生SAV、audit、receipt和图／OCR绑定闭合；18样本及所有失败attempt／诊断完整保留，独立verify不启动游戏。摘要分清原始失败、后续probe观察、尚未解释的原因和source边界；不声称成长或整Mod通过，不生成final-result，不改UI／Git／生产／root工具代码。完成后回写实际数量、SHA、样本映射、失败结论与未解决项。

## 封口结果

`1019-rc6-growth-v1/` 已冻结473payload／27,154,271B，其中原r6g455件／26,146,209B、22个SAV；另有16件原报告／计划、2件工具快照。18个canonical引用复用来源，72组fresh GPU／OCR、36个矩阵输入／物理Enter（18个FF30）逐一核对。所有18矩阵样本及四个post-matrix原生保存角色、真实repeat载入回执均闭合，未重复经济锚点。独立verify11项通过原字节完整性与绑定范围；明确记录471当前source相同、两份已推进source边界和首次source复核失败，不将其隐去。

index SHA256 `0434a330904ce63ffe665cc5e6a207074f144b005efce052958086e89d06c54a`；独立verify SHA256 `40a7e2ed76ce1b77a6e1fdb884c2858f83735158f3f63b7b17f3bee8b75e9ab9`。新post-matrix观察 SHA256 `7a251f03f0c7a42bc53a9a78a6e9359c060e13fe78f19e0a5a03eb77bddee6c0`，只用冻结audit parser原语抽取原n08 final及四个后来SAV，未导入UI。

九原报告全部FAIL保留：检查数C0／C9各170，其余各174；24原失败包含17项旧跨月government判据与n08七项真实exports。n08原账本R200不改写为反推104。新export1十导出确实相符，不替代原失败；budget1原生记录C20500／B410／R300／P110，单次gain100而事前预期200（R400／P10），真实FAIL保持。

r6grepeat的命令仅两次 `eep_sync_mothership`，与n08 final ZIP逐byte相同，不能代替独立完整重复初始化case。r6gload实际载入r6grepeat，日期已核但原state_verified仍false。reload与repeat ZIP不同；独立抽取的所有country／fleet／ship变量、健康、日期、设计体SHA相同，design_id1527→16777235及government_raw SHA不同，仍为未解释差异，无完整重载通过宣称。

并行最终日志包 `1019-rc6-final-logs-v1/` 已单独封口：22payload／5,971,299B（19完整logs及3metadata），index SHA256 `10df4d1aa1eb45ae1bd9554da46e7c298303a6d638f342ad33df18e5a61c9a2f`，verify SHA256 `367466eb7d650a16592dd7cf66b166363ae333a8b94b50598092c545ed2c16a3`。其两次独立OS核查PID30812不存在，正常stop证明身份。完整error.log SHA256 `b8a0cc17158bf05ebde64f42ed71ec17bd12687d5488fb8d6e7d462ceaf740f6`，第24行是真实EEP while100次中止；全部24条error、1条debug原样保留且影响未被白名单消除。此run未检出nomads不改变历史两个nomads未解释项。

两包均无ModPASS／final-result，未修改旧progress、原报告／样本、游戏／Steam／Git或root生产／工具代码；后续RC7属于新run和新源，本包不代替其新验收。
