# RC5 run143452Z 最终归档

固定run `20261019T143452Z`／PID33260于UTC14:59:47.307906正常停止；独立CIM于UTC15:00:50.2872858确认该PID不存在后才复制。RC5实际tree为 `1cc8b77c28f3d59b0d840982c7f039a209cb66f3e26d9c3280ad2dfa0f9dbd52`，没有混入当前RC6。

完整白名单见 `selection.json`；356个原字节payload、24,555,646字节，包括全部303个run artifact、19个最终logs（5份script_documentation）、15份稳定分析／source报告、7份方案快照、3份source-index／gate及9份稳定工具源码hash绑定。index SHA256 `c13b953ade483aad3185ec8aaa7693e3730768676280710b5aa83cbe978c8d2c`。

独立 `verify.json`重新核对全部源／副本、83个canonical引用、59个actual copied Mod与冻结源码，按原协议重算tree；7SAV全部与receipt／audit／observer／manifest／gamestate绑定，63组图片／OCR和5个offline imports一致。root此前完整封存的RC5源码复用 `../1019-rc5-static/`，未重复拷贝Mod树。

7份原生SAV是r5pautoload、r5preload1、r5coreguard1、r5coreguard2、nchealthbefore、nchealthset、nchealthload，日期均2200.01.01。guard两份SAV都为SHA256 `44ebd953fa66ffb2a891db6e24bbe7a38f57ccb8024699a8de116e6aa120562e`。Welcome首次请求中文标签在内联worker中损坏为问号、拒绝点击的实际原图／OCR保留，没有第一次click receipt；UTF8重试实际click另存。未伪造failure JSON。

| 保存阶段 | 舰体 current/max | 装甲 current/max | 护盾 current/max |
|---|---:|---:|---:|
| nchealthbefore（原生corvette） | 162.87655 / 200 | 162.87655 / 200 | 41.34742 / 100 |
| nchealthset（NAME_Relic） | 16287.6 / 20000 | 25034.0412 / 30740 | 57204.60817 / 138352.5 |
| nchealthload（实际原生重载） | 16287.6 / 20000 | 25034.0412 / 30740 | 57204.60817 / 138352.5 |

原生ship3目标重载后的current/max精确保留是本次校准事实。setter三层原1e-6检查仍FAIL，Mother另有重载回退，health报告保持OBSERVATION_WITH_FAILURES（36/40，4项失败）；talon和旧nrelsrc分支未执行。迁移autoload/reload报告FAIL（31/40，9项失败）；guard仅PASS_SCOPED（26/26，同日期同SAV重复，没有重载保证）。root flags出现不能证明design-local marker或通用shared design-flag机制。

完整 `review.json`／`review-verify.json`覆盖22条error（21 baseline missing Workshop、1 consume override）、3条game信息、1条baseline debug building类别警告。具体building对象及影响未知；当前run无新增EEP错误或nomads.94，不消除历史nomads未解释状态，更不能推翻RC5实际FAIL。

`source-binding.json`明确这是事后hash绑定：prepare没有execution-source快照，没有内存loaded-source证明。runtime84b在prepare前封口，9份源码与此前canonical一致；期间间接导入的publish相关源码发生变化，不以当前磁盘版本回填历史worker；事后health checker v2排除。没有调用UI、Git、Steam或改生产源码。证据保存复核通过，Mod验收未通过。
