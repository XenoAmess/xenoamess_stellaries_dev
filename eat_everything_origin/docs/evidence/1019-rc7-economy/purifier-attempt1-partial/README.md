# RC7 Purifier 首次年度采集：前台调用失败

run `20261019T164112Z`，原prefix `r7pu`，root worker引用37801。原total receipt状态 `CLEANUP_REQUIRED`：完成4次FF30与m01..04，随后SetForegroundWindow报错，console／debug cleanup也同错。原receipt SHA `496323a628d8949410425de14cd4c3eb99446ee0059e9935cfa8614b20238625` 未改写；这是collector调用方失败，不能称Mod经济失败或完成年度。

146个payload／8,472,471B，包括144件该失败尝试原始链、manifest及原collector磁盘源：5份SAV（m00..04）、30组GPU／OCR、全部已有actions／wait／audit／monthly JSON／receipt。未生成m05..12或yearUI。此包单独保留，不覆盖后续完整purifier包，不混r7pumedia后置UI。

- index SHA256：`cd19be4012af8a992e99368bf40cb8c0df108b74d0d6d0386721ce12c777ab1a`
- verify SHA256：`483a3b803ac9d1beaea747086923de1d3201f71ca090452f8429521a9214e10a`

独立6项只验证原byte、来源、4个实际命令／Enter、5ZIP与30图OCR绑定。年度case仍PENDING，四项操作约束null；已有首月电力+40.63438不外推全年。未执行恢复、重试、UI、Git、Mod或工具代码操作，未收活动日志／其它活动分支或后置媒体，未生成final-result。
