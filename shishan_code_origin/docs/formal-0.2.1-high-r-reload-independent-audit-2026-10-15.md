# 正式 0.2.1 高重复层重载的独立只读审计

## 目标、范围与验收标准（先行）

对比原 rc.6 `fb456_legacy25_reload.sav` 与主任务在正式 0.2.1 无夹具运行 run103709Z 真正重载后保存的 `formal021_legacy25_reload.sav`。复用既有原生 ZIP/P 数据解析器，独立按实际国内人口组和 species_db 谱系重算 P/W/U/R/T/B，检查唯一架构 modifier、旧四计数、migrated、n/CD/槽及票据，并逐个比较所有领袖完整记录（尤其白绮）、国内实际模板与外国引用模板的原始定义。

报告写入该 run 的 `independent-formal021-high-r-reload-audit.json`，记录双档路径、SHA、日期、独立数值、原始字段与差异；缺失槽保持 ABSENT/null。核心计数、历史、modifier 或白绮状态被非预期更改则 FAIL；自然重载的缓存重建、引用/序列化或预算变化按实际字段单列，不能宣称全世界字节相等。外国原始物种定义相等与外国人口/就业快照相等分别报告，不互相替代。

本审计不启动游戏、不操作 GUI、不改生产、发布文档或 ledger、不提交。主任务已完成的原生重载操作由其证据证明，本代理只审计保存结果，不能由两个快照推断完整调用轨迹。

## 结果

[独立 JSON 报告](evidence/feedback-redesign/remaining-2026-10-15/formal021-no-fixture-run103709/independent-formal021-high-r-reload-audit.json)的核心状态 **14 项 PASS**，整体记 **OBSERVED_WITH_RAW_DIFFERENCES**。源 rc.6 SHA=`fc6da734a763ad377b84db1729808055cab2d243e1c7510199494d5de2425d5e`，正式重载档 SHA=`59af0c64427e00f520b7d1c4ab84081f5a23cf5fd3e6989360b6a793f7c458b2`；两者均为 4.5.2、同日 `2227.04.19`、country 0。

独立实际人口 P=5567、正式键加权分子 W=239381、U=43；观察到的历史 R=25，故 T=68、B=3.4（岗位产出加算 +340%，M=4.4 仅诊断值）。所有即时缓存均 MATCH，架构 modifier 各只有一个实例、multiplier=68。旧四 k=7/5/11/4、migrated 保留，n=2、CD=2；全部 Mod 变量/flags 相等。三个槽两边都没有保存，报告维持 `present=false/value=null`；没有实体待领、窗口锁或未消费的维护/优化/清理/复发凭证。

全部 478 个原生 leader 记录逐个完整比较无变化；国内 11 名领袖各保存 before/after 完整字段。唯一 flagged 白绮 ID=16777367，所有字段不变，包括原生姓名「负疚者·白绮」、专属 portrait、species=855638017、owner=0、XP=317.52、level=5、4 次待选、现有 traits、两项候选、design 与 should_not_have_upkeep flag。本结论只针对本高层数来源，不把其它种子的 XP=25/重启证据套入本档。

国内实际模板只有 855638017，正式 trait 定义与全部实际人口组保持；founder、rights primary、owned_species_refs/default_species 原始字段都相等。整个 species_db、pop_groups、pop_jobs 数据库没有记录差异；外国实际引用模板及其祖先共 33 个定义逐一哈希一致，外国实际人口组状态亦相同。此档不复用个体机械来源已发现的外国就业移动或权利折叠结论。

仍有 10 个原生根区段原始哈希变化：country、last_created_design、last_event_id、market、open_player_event_selection_history、random_count、random_seed、ship_design、ships、starbase_mgr。报告记录这些区段的双哈希和关键标量，未因核心状态一致而隐去。actor budget 唯一递归差异是 `income_high_water_mark.length: 7→8`；current/last_month 的原始资源收入支出数组均没有差异，完整预算双边保存在报告中。没有把上述未知世界/序列化差异推断为全部无害，也没有将它们误报为架构或白绮状态变化。

最终报告 SHA-256=`5d9638094d43e806e887724194d75e667a544f9a791f21f8aa60c5b7b73915ad`。同目录保留一次性只读审计脚本，可复核所列两档；本轮未改生产、没有 GUI 或提交。
