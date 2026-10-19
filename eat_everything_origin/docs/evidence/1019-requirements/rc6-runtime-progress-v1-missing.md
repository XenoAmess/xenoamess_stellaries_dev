# RC6 PENDING进度缺口

18组均PENDING；表中数量为已记录单项观察，不是case验收。全部组仍缺最终运行log；缺项详细原名见相邻missing JSON。

| Case | true | false | null | 缺少证据类型 |
|---|---:|---:|---:|---|
| hive_startup | 7 | 0 | 0 | log |
| machine_startup | 7 | 0 | 0 | log |
| purifier_startup | 7 | 0 | 0 | log |
| hive_economy | 3 | 0 | 4 | log |
| machine_economy | 3 | 0 | 4 | log |
| purifier_economy | 3 | 0 | 4 | log |
| lithoid_hive_first_month | 0 | 0 | 8 | actions, analysis, log, native_save, screenshot |
| mothership_configuration | 3 | 0 | 9 | log |
| unlimited_growth | 0 | 0 | 10 | actions, analysis, log, native_save, screenshot |
| colossus_enemy_fire | 0 | 0 | 6 | actions, analysis, log, native_save, screenshot |
| colossus_guards | 0 | 0 | 10 | actions, analysis, log, native_save, screenshot |
| colossus_cancel_idempotence | 0 | 0 | 5 | actions, analysis, log, native_save, screenshot |
| common_settlement | 0 | 0 | 8 | actions, analysis, log, native_save, screenshot |
| normal_dismantle_regression | 0 | 0 | 4 | actions, analysis, log, native_save, screenshot |
| old_save_migration | 1 | 1 | 11 | log |
| candidate_reload | 0 | 0 | 4 | actions, analysis, log, native_save, screenshot |
| repeat_initialization | 0 | 0 | 4 | actions, analysis, log, native_save, screenshot |
| random_components | 0 | 0 | 13 | actions, analysis, log, native_save, screenshot |

三分支startup各7项true，需root对完整证据和PENDING状态作最终review；经济各3项true、4项null，后四项仅受控worker链等待root审查，不能称系统输入审计。

母舰仅维护观察、源推算power非负、22大防御槽三项true；同国同日Relic参考、实际跃迁、10船坞、技术/其它主宰负对照等仍待独立证据或review。source-derived+9743不是UI供电数值。

迁移原严格damage_preserved=false保留，独立v2预算true；其它11项顶层映射尚待root审核，底层174/158 scoped报告和真实重复样本已在合同中。缺口不等于必须重做已有样本。

其余成长/RNG、三组巨像、共用结算、普通拆解、Lithoid首月、候选restart/reload与repeat初始化等当前未合并证据/观察。活动r6g和最终日志没有读取，待各线程封口后另追加。

独立repeat-initialization报告／proposal已由acceptance线程封口：`docs/evidence/1019-analysis/rc6-r6mc-repeat-initialization-report-v1.json`（SHA256 `d2ad24b26236b28b2d4f472da0047a3455cc3ef0c7730a759628878f9fd2cc66`）与 `rc6-r6mc-repeat-initialization-case-proposal-v1.json`（SHA256 `d0bf82634785c5b2afcdf7e2660e9f4a554db3da520f349a4b900031cd1d9ab1`）。本轮未读取其原生r6mcinit2操作／存档链；缺口是独立项目归档、引用绑定与审核，不等于需要重做已有41项限定观察。该probe不属于经济12个月链，首次driver在任何输入前的government_raw KeyError也应随独立归档保留。

所有缺结果保留null；未生成final-result、未将任何case改PASS。

公开／paid原生loaded代表图、原OCR与F12动作已从既有migration checkpoint绑定，无重新操作UI；完整失败／重试链仍由原checkpoint index引用。
