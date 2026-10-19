# RC7原生订单与早期取消接收

本阶段在独立校准包封口后另建`evidence/1019-rc7-pk-native-cancel-v1`，不改旧包。固定run/tree/简体中文，复用原d4da receiver、681 checker、1ec3 inspector和06c publisher接口。只接收root逐阶段明确封口的原SAV/audit/native-save及对应操作图/OCR，原件双读稳定、SHA明确后observe，每个role仅物理world `[2,17]`；完成receipt metadata例外沿已记录授权。UI、Git、Mod、工具、活动日志均不在本agent操作范围。

初始已交接四role：queued Jan21（`8cffba65db094d10b4f652224515e7a1434036e3a352dc525d4312035ea9809e`）、day1 Jan22（`ec88ba87f6d849d608a39b9c127005c691ce6bd6cf33540f106101dd21b485a4`）、charge Jan27（`88cfe048183aefbfda9fcfc58947bd11e0528a7e8d202fce73b03a87436cdb36`）、cancel Jan27（`d54cb834d25f54a4513c5a9ab3ecb84adc00baf0b481f878b58081847fd3873a`），分别对应r7pkshotqueued、r7pkshotday1、r7pkshotday6、r7pkshotcancel同stem。

已授权操作前缀仅为`r7pkshot-first-actual-day*`、`r7pkshot-first-day-*`、`r7pkshot-select-mother*`、`r7pkshot-ready-target-visible*`、`r7pkshot-open-target-context*`、`r7pkshot-context-menu*`、`r7pkshot-click-native-dismantle*`、`r7pkshot-native-battle-five-days*`、`r7pkshot-battle-five-*`、`r7pkshot-stop-hover*`、`r7pkshot-select-charging-mother*`、`r7pkshot-stop-actual-charging-order*`、`r7pkshot-close-visibly-open-console*`。尚活动的cancelreload/reload-cancelled及其他新shot前缀不读，待另行明确交接再追加。

验收目标是验证真实右键原生destroy_planet_order指向17；区分移动子单、实际海战与windup，不能把海战或移动天数算充能天数。root实际FF5跨过最初充能帧，只观测到3/90，按早期取消记录，不补造0/1帧。核停止按钮tooltip与真实物理click，再核cancel订单空。charge→cancel同日用原no-settlement检查，保留完整strict差异；跨日仅独立核EEP账本/奖励/源存活，人口和预算自然变化如实记录，不能套同日严格不变。ground/war/己方陆军只读原生实际状态，不能仅凭原暂停基线延伸。

此包不验证90/30完整自然发射，不宣称取消后实际重载已经通过，18组最终矩阵仍null/PENDING。薄包复制完整明确白名单链，引用既有20source closure、原receiver及基线校准，不重复Mod。封口需独立字节/来源/ZIP/role/图OCR核验，限定结论与全部缺失项写清，再交root精确stage清单。

## 接收边界错误记录（尚未封口）

首次复制脚本把四个已授权同stem写成通配前缀，其中`r7pkshotcancel*`串入18份当时未交接的`r7pkshotcancelreload*`（含SAV/audit/receipt/UI链）。在启动receiver前通过复制清单发现，立即报告root并暂停；未observe、未语义解析该role，也未将其判PASS。原件完全未改。该错误属于接收授权边界错误，不能把“未observe”写成“未读原件”。原始复制回执保留真实记录，不追改成从未复制。后续同stem必须限定下一个字符仅`.`或`-`，其他显式操作前缀按授权匹配；reload只有获得明确完结交接后才能继续收件。

root收到诊断后明确确认reload已完成，正式交接第五role `enemy_cancel_reload=r7pkshotcancelreload.sav`，Jan27，SHA `895c2b1beb85b2ac688cf0c2271f28aaedeacdbf667ef35db4969147d91c9053`，以及仅同stem（后接`.`/`-`）和`r7pkshot-reload-cancelled*`。现重新双读稳定核SHA后接收；初次copy回执和intake-v1保持原bytes，新增post-handoff-copy-receipt和intake-v2，并在新metadata快照后启动原receiver。cancel→cancel_reload同日增加原no-settlement检查，不能把同日EEP不重复支付等同整个SAV只读。`r7pkfire*`仍活动，不读任何raw。

root授权完成后可独立提出cancel idempotence的限定部分，以及`unlimited.invalid_or_cancelled_no_growth`中取消半支的证据映射；invalid仍须guards，最终矩阵保持null，不以取消半支填完整项。

## 实际结果与封口

五个明确交接role原receiver首次observe，EXIT0、OBSERVATION_ONLY。复用基线restored缓存调用原no-settlement，restored→queued为PASS_SCOPED；charge→cancel、cancel→真实reload同日各9/9 PASS_SCOPED，完整strict分别FAIL1、FAIL25保留，未忽略差异。实际Load回执绑定cancel SHA，Load后另存的cancelreload才作为after。

原生queued/day1均为指向物理17的destroy_planet_order，子单仍move_to_system_point。Jan22实际与fleet4/7交战，起始Jan21；Jan27海战结束后首个存档才记录windup3/90。已看原始hover图及OCR确认“停止／停止并移除选中舰队的全部命令”和3%充能，真实Stop click为client69,339；cancel及真实reload均空订单。没有补造0/1充能帧，也未把移动/交战天数算充能。

全部五role的EEP变量（含C/G/level/made/worlds、组件entitled/pending/rewards及六rank）保持零，D2；source仍country1的pc_tundra殖民地，未支付worlds/empires目标。自然海战独立产生`crisobj_destroy_enemy_ships` progress45，charge/cancel/reload均保留45；这不是拆球奖励，不能把跨海战总危机原文强制当成零变化。实际五存档的ground_combat均空，actor均仅五支本土colony0的machine_defense。

实际type_text只包含FF1、FF5与五个保存名；截图中控制台旧校准文字跨Load保留，不能当本段新输入。已独立生成[部分提案](evidence/1019-rc7-pk-native-cancel-v1/authored/partial-native-cancel-proposal-v1.json)，仅queue_no_reward/cancel_no_reward/reload_no_reward三项限定支持；crisis_objective_once/repeat_event_no_reward仍待真实完成与重回调。unlimited.invalid_or_cancelled_no_growth仅取消半支有证，invalid未测，整项仍null。18组138项最终检查保持null/PENDING。

封口：160份正式交接后重新双读核实的原件，17份派生/缓存，共177 payload、11,905,598字节；31图/OCR、37 canonical引用。初始18份越界复制诊断和旧回执未覆盖，原件未改；正式接收在明确交接后用intake-v2启动。metadata75→76且前75项不变。独立verify 14/14限定通过，初次核验误把report.intake对象当字符串导致单项断言失败、未写verify，按实际path字段修正后全项重核；没有Mod或原receiver失败。

- [index](evidence/1019-rc7-pk-native-cancel-v1/index.json)：`389ea508b8b768ce18d1a6d18a0e80a1a38f2000988dd930a7af0b5709b72f8c`
- [verify](evidence/1019-rc7-pk-native-cancel-v1/verify.json)：`c0c5e2b43ab988287548d78d405be5f90f8a86828f1f4b6c8b519adc5e488436`
- [原生独立链](evidence/1019-rc7-pk-native-cancel-v1/authored/independent-native-cancel-chain-v1.json)：`0f4d362f67e6d41074bc72a3f25a7314149f0a3473cdec018bff065ff3cbd610`
- 部分提案SHA：`8f3492119b7a25f3520b0148da4384ab02e9b3a27060f287a142ef7a8b213149`

精确stage为本文和整个`evidence/1019-rc7-pk-native-cancel-v1/`（181文件），共182文件。包已封口，后续正例与invalid另包，不追加进本包。
