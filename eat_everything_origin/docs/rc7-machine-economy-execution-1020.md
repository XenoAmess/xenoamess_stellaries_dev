# RC7全新机械政体经济实机采集

沿用既有三政体方案，root 在 r7hvc 完整12月及年末对照 worker EXIT0 后，从
原生选择列表实际行 `EEP03铁心灭绝者` 创建 r7mc。显式 RC7 版本与59文件树
`61b34f6dbdc277c44364889d5f1e1cd2773a4624786bbf0d538079fc6ba4feb0`，
同 run `20261019T164112Z`、简中单Mod、200恒星／3AI／尉官。纯经济段仍只执行
new_game→make_plan→collect，不注资、交易补贴、关闭岗位或拆船。

m00实际单殖民地，SAV SHA256
`bfe002e7e4b0ce889ed529cd96c840eaa073b254a80f11ba8f297a5b5a8339cd`。
Jan1缓存净电+88.90835不是首月实收。m01（2200.02.01）SAV SHA256
`68dd7c57db53031b65498b98e76ca327caed1304e66fd0b7cbb71f70a6f7bf14`，
收入166.57320、支出163.71565、净电+2.85755、库存202.85755。实际核心物理2、
Mother fleet151；pop_jobs403为technician_drone，workforce905/max1800/
limit1800/bonus90.5。该job原生planet字段为0，保留原值，不把它当物理核心ID。

02:13已完成四月，净电为2.85755、3.40593、3.95420、4.50156，库存逐月增至
214.71924。正电余量较小，不能由初始缓存或首月通过推出全年结论；继续完成
十二份独立月初档、年末auto/UI和独立维护／岗位／操作约束审核。四项最终判断
仍以完整动作链与root受控worker交接为范围，不宣称全系统输入审计。全年和
最终停止日志目前PENDING。

## 完整年度原生采集与原v1分析

root交接session98202 EXIT0后才接收固定 `r7mc`。原v1以
`--branch machine --prefix r7mc` 正常EXIT0，生成新薄包
`evidence/1019-rc7-economy/machine/`：57原始payload、9,011,254 B，
报告PASS_SCOPED，7项startup均true，原四项操作约束仍null。
报告SHA为 `d6a253ef67f8f98018fdc581eae4cafe8f5fd3a0fafd09d5982a8f45d92d3dd1`。

初始实际core物理2、pc_machine、人口4800，Mother fleet151/ship1044。
首月岗位905/max1800/limit1800，正常原生维护存在；12个月净电依次为
2.85755、3.40593、3.95420、4.50156、5.04960、5.59752、6.14533、6.69303、
7.23978、7.78724、8.22547、8.77273，全部非负，能量200→270.22994。
m00缓存88.90835明确独立记录，不当首月实收。这里只覆盖该新银河首年，
不把较小的正电余量推广成后续所有人口/舰队状态均不负电。

m12/yearUI完整原ZIP相同，原SAV SHA为
`41a19510e73c8e92da7d0877dc29dfbcff6ccacda66457a6a34522a9d388d2db`；
yearUI native-save回执SHA为
`53537b73a903710631729ef8f77dc4573129d7845f37ad090c86c7e76e421bae`；
总经济receipt SHA为
`0a832e38bd1d158ec3876817446b80d0507b9d53427ee28c7bbab4027d04ea8a`。
这三个对象分别按真实路径绑定，没有混用回执与SAV。

## 独立原生、动作链与来源封口

独立第二进程的原生复核8/8，`independent-verify-v1.json` SHA为
`8ac0c752eaa9580da6796462df95efc8267f2d79f33755e9fe1db1fe5df82087`：
14份原生ZIP、两期预算/库存、岗位/人口、真实Machine authority/civic/founder、
实际六core装备和country/fleet零tier镜像、完整59文件tree、原生维护父链与旧新折扣均核过。
完整UI包 `evidence/1019-rc7-machine-economy-worker-ui-v1/` 封228 payload、
9,054,821 B，index SHA为
`c1e6b59267d545d7ad29e82d74300ada1564ff2afe77db55604a2476ad2cd3c0`；
独立verify11/11，SHA为
`7f2a1903f6bcf14f76b9f9973bc5fca46e4ff9dd295441053ce60a597f74d5b1`。
101个canonical引用、52对GPU/OCR、12个真实receipt HUD以及20件复用源全部匹配。
源与Mod无重复副本；原生已完整复核的相同原档只做SHA绑定，没有再跑全套解析。

独立四约束报告 `evidence/1019-analysis/rc7-r7mc-economy-operation-review-v1.json`
SHA为 `eeb5ca74bc549c5a1cd7dd44bd447800924a9406d10d01705093645672bc6db9`。
实际111 action中14个type_text仅12条FF30和两次存档名；26个鼠标动作只属新局、
保存、控制台聚焦。结合root纯经济worker明确交接和原生库存/岗位/舰船保持，
四约束在该独立限定报告为true，原分析报告null不改，不声称全系统输入审计。
月图有女王/接触/debug遮挡与旧FF历史；开始界面有unknown政府预览文字，
本次不声称所有UI文本无key泄漏，实际初始化的原生Machine政府及founder已独立核实。

新 `rc7-r7mc-startup-economy-partial-proposal-v1.json` 两组case仍PENDING，
待真实stop日志与root最终汇编。没有读取后续功能前缀或活动日志，没有改Pu/Hive/旧partial。
本次可stage：本页、`rc7-economy-completion-review-1020.md` 的本轮更新；
`evidence/1019-rc7-economy/machine/` 与
`evidence/1019-rc7-machine-economy-worker-ui-v1/` 完整目录；新操作审核和新partial提案两份JSON。
