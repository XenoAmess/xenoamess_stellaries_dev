# RC4 phase-B run133314Z 最终证据

固定run `20261019T133314Z`／PID36912于UTC14:34:31.898945正常停止（forced=false、running_after=false）；独立CIM于UTC14:38:21确认PID不存在，随后复制。原字节白名单为 `selection.json`，108个payload、10,488,569字节；`index.json` SHA256 `c5bd429ccf088a36e41a6f9be43fb1122312ebc56c25cb6ae2f5d95d297d3227`。

- 19个完整日志，含5个script_documentation文件，共5,886,575字节。
- 3个原始manifest／process／stop。
- 38个rsizeonly文件，含唯一SAV、audit／native-save receipt与完整动作／UI／OCR。
- 40个nrel文件及1个增量ctrl+a动作；没有nrelbefore／nrelset／nrelload、成功load receipt或新nrelSAV。
- 4个稳定分析／source报告与3份设计文档快照。

`verify.json`独立复核108份源／副本、19个canonical引用、18组图片／OCR、rsizeonly的SAV／receipt／audit／observer／manifest／gamestate及Git原字节属性。rsizeonly SHA256 `715a8a4d168052ac06cb8867b0394ecac757c6bfd5b189bcf606dbc2b7e66678`，原生日期2200.01.12。phase-B较早11份SAV与462payload、中途工具源码补充、59文件RC4 Mod树均复用canonical，未重复拷贝或改写。

`review.json`／`review-verify.json`覆盖全部39条error、3条game和1条debug。error中21条baseline missing Workshop、1条consume override、17条EEP同步变量未设置告警（Machine12／Hive5）。17条属于真实EEP运行时告警，执行期变量解析原因仍未知；后续SAV中的显式0不能消除这些告警。debug为baseline原生building类别警告，具体对象与影响仍未知。本run没有portrait_container或nomads.94记录；历史nomads.94仍未解释。

rsizeonly保留4项FAIL。nrel只完成原字节source import；load在日期HUD guard失败，施伤／保存／导出未执行，两次play0 guard拒绝前未输入命令。后续直接观察图及动作已原样保留，不能据无新增engine错误外推为helper或Mod通过。此包仅证据保存复核通过，迁移及全Mod验收未通过。
