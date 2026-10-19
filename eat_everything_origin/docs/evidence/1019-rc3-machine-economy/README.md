# RC3 Machine 全年原生经济子集

本目录归档run `20261019T092935Z` 已完成的Machine新局、干净基线重载、12个月自然经济和年末原生UI存档。只复制稳定的fm／fmm／fmyearui阶段文件，不包含后续fh Hive资料或活动日志，不称为整个run的freeze。

原生存档、audit、receipt、动作、HUD截图及OCR均逐源双读、按原字节复制。`archive-index-v1.json` 记录源路径、字节数、SHA256及取证时间；`.gitattributes` 禁止文本归一化。冻结Mod／静态门禁引用已验证的RC3硬件归档，旧机器基线引用原 `1019-baseline` 归档，各引用有独立哈希绑定。

`source-copy-receipt-v1.json` 保留先完成字节复制、当时尚待分析报告的历史阶段状态；最终完成状态以archive-index及archive-verification为准，原阶段记录未覆盖。

Machine新局及首月23项限定检查通过，12月经济14项限定检查通过：12个结算月净能量均正，首月+2.6589、年末+8.51705，库存200→267.60783逐月不降。年末autosave与原生UI存档的十类经济字段独立核对一致。所有月度原生档均无护盾探针变量，C／L／R及六核等级为0。

实际月度推进anchor是干净Jan1原生档 `fmm00reload`，每月只提交一次 `fast_forward 30`。首月第一次操作使用了加载前的目录anchor，但真正Feb1 autosave已产生；恢复过程没有再次推进。`fm-first-autosave-recovery.json`、最初命令、日期HUD与OCR原样保留。初始预算行仍保留原fmm00，并另核实际anchor的初始预算／库存完全相同。

旧0.3.1机器基线的负预算和原始缺失库存键均保留，未改写历史结果。这份归档不认证Hive／Lithoid／Purifier、自然随机奖励、巨像发射或完整Mod发布；十类经济字段一致也不代表全量gamestate零差异。
