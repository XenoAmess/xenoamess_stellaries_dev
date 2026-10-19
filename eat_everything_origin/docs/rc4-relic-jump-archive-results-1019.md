# RC4 同国参照舰、真实跃迁与原版回调对照归档结果

目标、范围、设计和验收先记录于
[原版跃迁与参照夹具方案](juggernaut-native-jump-probe-1019.md)。本次只读分析与
归档已完成；该方案最初静态交付段落中的“待主线程实测”是当时状态，当前结果
以本说明和绑定证据为准。未操作UI、修改生产Mod或外部工具，未提交，交主线程
统一checkpoint。

Mar13、同国C0、刷新六天后的真实配置图显示Mother／Relic：船体93960／20000，
装甲44787／30740，护盾167310／138352，速度417／225，闪避22.1%／22.0%，
伤害字段5598.57／2373.28（斜线后原生时间图标）。维护和供电未显示，仍未验证。
夹具HUD365/69包含额外Relic250海容，不作为新局预算。旧Mother全景失败图和
两次中文搜索空框保留，不用于成功证据。

Mar14原生Mother159／997订单指向196，实际windup14天，Mar13开始、Mar27结束。
Mar27相同舰船实际位置origin196、订单完成、新增jump_drive_cooldown=yes和
last_jump_date=2200.03.27；原生悬停显示剩200天、武器伤害与亚光速各-50%。
三档C0与全部国家成长变量不变，11条国家队列逐字节相同且空；两舰身份、配置、
三防和账本保持。没有独立in_ftl瞬态或200天到期样本，旧last_ftl_jump缓存排除。

[独立归档](evidence/1019-rc4-relic-jump-native-control-v1/README.md)有449份载荷／
22,683,809字节；含元数据最终455文件／22,917,843字节。仅收指定五个前缀、5套
原生SAV及89对GPU／OCR、只读分析快照、明确primary来源；复用既有v3 canonical，
未重复59份Mod，也未复制无关UI或活动日志。原版CRACKER仅**手动完成回调**对照，
原有nomads错误及worlds750／empires0原文保留，不宣称原版武器实际发射。

| 证据 | SHA256 |
| --- | --- |
| [19项限定SAV断言](evidence/1019-analysis/rc4-relic-ui-jump-v1.json) | 5e849e167c16057d6f529f74ec0c7d491ebd1e28382844ffb846e17e7de85b64 |
| [归档索引](evidence/1019-rc4-relic-jump-native-control-v1/archive-index.json) | 2b984e60d900b13127628ec438885a4d0ee8cbb7b2ad01f9d195db2a4d396438 |
| [独立复核18项](evidence/1019-rc4-relic-jump-native-control-v1/verification.json) | 23d0238c72ca5d753236e55ae07a1e545f4b4fdc0df015830d01f983a586a215 |

18项复核均真：逐源与目标字节、精确前缀全集、ZIP CRC／receipt／audit／gamestate、
OCR原图、既有v3全部798份载荷、copied Mod59份、最终日志引用，以及归档Git属性
和过滤blob均保持原字节。verification自身另核-text与blob一致。结论限于上述
字节完整性与参照／跃迁观察，整体Mod、维护／供电、经济、迁移和发布仍未据此宣告通过。
