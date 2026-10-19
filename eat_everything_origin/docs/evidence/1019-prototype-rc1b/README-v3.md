# prototype-rc1b 原生接口调查归档 v3

最新索引为 `archive-index-v3.json`，SHA256 `891936b7e513e013f9dbe332ba47aaa0f6acc78be1b7b4807481e22d593d4cf2`。该索引绑定v2，v2绑定v1；所有既有索引及副本未覆盖。累计680个源文件、42,310,475字节，复制文件逐源路径／字节长度／SHA／读取时间可追溯，Git属性为 `text: unset`。

运行ID为 `20261019T081638Z`，冻结生产树为 `e3c4c176c9b6d0fa6d43cab461d6f7dd9161cc4828ff800d78bdfc33ee7df526`。这是有已知action locale／科技图标缺陷的未发布原型，不是最终候选验收或发布证据。

v3已包含pmm00、aurafleet1、auraship1、auranative1、aurarebuild1、pkbefore、pkqueued七份原生SAV／audit／receipt，以及相应动作、截图、OCR、静态报告、冻结源快照绑定和只读分析。run manifest与receipt里的原绝对路径没有改写。

`pkbefore`与`pkqueued`均为2200.01.06。真实war0为country0对country1、wg_cleansing；排队后Mother138／ship808出现目标planet15的destroy_planet_order及移动子订单。C/G仍为0、D为2、worlds/made为0，目标仍为敌国殖民地且没有credit/destroy标记。这只证明原生命令排队，不能证明已完成充能、发射或结算。完整严格对照保留3项订单差异并维持FAIL，专项分析为OBSERVATION_ONLY。

`stop-final-log-freeze-v3.json`记录pid29844于2026-10-19 09:08:33 UTC自然退出、running_after=false，并经只读进程核查。随后 `logs-frozen/stop-final/` 完整19文件、5,904,024字节双读SHA一致，属于进程退出后的字节freeze。此前 `logs-single-read/` 两次活动快照仍然不是freeze，不能混用。

`failure-classification-v3.json`指向原始完整error.log：早先WrongScope控制台探针Current=fleet、原始ROOT=country1，属于探针scope错误；17:05:52缺少专属PK的queued on_action是单独的原生回调警告。两类原文均保留，没有删日志或合并原因。

初始自生成 `README.md` 与 `README-v2.md` 的中文曾因PowerShell管道编码变成问号。这只影响这两份生成说明，SAV、源文件复制、英文索引结构及JSON数据未受影响。为保持历史字节，两份文件不重写；以本UTF-8说明和v3索引为准。

后续rc2加载pkqueued并迁移属于未发布原型接口调查，不能替代公开0.3.1旧档兼容验收。
