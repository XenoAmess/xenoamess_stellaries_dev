# RC6 机械年末重复初始化验收

## 事前目标、范围与方案

仅在主线程本次 `r6mc` 十二月经济采集器完成并固定总回执后执行；不把探针混入经济序列。候选仍为 `0.4.0-rc.6`，run `20261019T150008Z`，精确生产树 `cc181c8a27ede295e9fcebeffc5e10bb75e9cd643edec1d194b928993ffab33a`。本方案不修改生产包、资源、人口、成长计数、岗位、队列或存档字节。

以真实机械年末 `r6mcyearui.native-save.json` 为 before。当前游戏须仍是这份机械局，日期 `2201.01.01`，C/L/R/六核心层数均为零。原生控制台以玩家国家 ROOT 连续调用两轮完整生产初始化、开局发放及母舰同步：

```text
effect root={eep_initialize=yes eep_startup=yes eep_sync_mothership=yes eep_initialize=yes eep_startup=yes eep_sync_mothership=yes}
```

不推进日期，再通过原生简中 UI 保存独立新名 `r6mcinit2`，保留输入动作、GPU/OCR、原生 ZIP、审计和保存回执。不得覆盖年末基准，也不得把只调用 layout-only helper 的旧档迁移重复检查充当本次完整初始化检查。

## 验收标准

独立比较 before/after，须保持同一唯一殖民地、母舰及全部自有舰船身份、民用和军用队列、原开局发放旗标、全部资源、人口/岗位/布局、经济五账本以及六核心计数。不得产生额外星球、舰船、奖励或民用队列。原生根日期相同；另报告两份原始 ZIP 是否逐字节相同，若不相同保留全部差异并按业务范围检查，不能改写为全档相同。

这是新局初始化幂等性，不能代替母舰损毁后不重生、跨进程重载、高等级成长或吞噬结算防重等独立检查。结果在真实样本完成前保持 PENDING；结束后仍原地接机械 C0 成长矩阵，成长入口使用实际年末 receipt 推导身份和活动 autosave 目录。

## 执行前守卫记录

2026-10-20 首次只读预检把 `check_growth_1019.receipt_save` 的政府字段误写为另一个 inspector 的 `government_raw`，在任何物理输入、console 或保存调用前以 KeyError 停止。已查原函数实际输出字段为 `government`；仅更正临时调用守卫，不修改检查器或生产包，不把这次工具调用错误记作 Mod 失败。尚无同名前缀游戏证据文件，可继续原定原生阶段。
