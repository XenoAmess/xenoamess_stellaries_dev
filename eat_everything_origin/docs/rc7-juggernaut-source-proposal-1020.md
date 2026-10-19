# RC7其它主宰SOURCE_SCOPED部分提案

## 目标、范围、设计与验收

2026-10-20按root指示，把已提交的[主宰隔离范围判定](rc7-juggernaut-isolation-scope-1020.md)转为独立、可合并的部分提案。只新增本页及`docs/evidence/1019-analysis/rc7-juggernaut-source-isolation-report-v1.json`、`rc7-juggernaut-source-isolation-partial-proposal-v1.json`；不修改已封口两个包或已提交旧文档，不操作UI／Steam／Git，不读取尚活动的`r7jump*`／日志，不生成普通主宰或新测试矩阵。

事前验收：七份精确RC7生产源均与已封存static副本同SHA；原版juggernaut定义当前与既有canonical同字节；descriptor／完整59文件manifest确无替换原版ship_size；专属基线、设计迁移、成长和六组件再次限定已绑定Mother。新报告引用现有配置包及scope文档，明确原生友军光环保留、没有普通主宰实舰样本、原mother14项不含本check。

拟交付语义为`other_juggernauts_unchanged=true`、证据模式`SOURCE_SCOPED`，只说明未全局覆盖普通主宰定义且EEP专属装配／基线／成长绑定Mother；不把它说成普通主宰运行时对照。部分case仍`PENDING`，`actual_jump=null`。其它case检查由各自已封证据和后续真实jump／终态logs共同审查；本页不会创建或修改final-result。

## 来源与具体覆盖

候选0.4.0-rc.7、59文件树`61b34f6dbdc277c44364889d5f1e1cd2773a4624786bbf0d538079fc6ba4feb0`；配置run `20261019T164112Z`，Jan7 Mother151／1044／design1844、native Relic175／1068／design16779116。七生产源从`docs/evidence/1019-rc7-static/candidate-rc7/mod/`引用；原版`18_juggernauts.txt`从已封供电source引用，不复制新原版数据。

报告逐项绑定：`eep_startup_effects`专属create_fleet；`eep_mothership_effects`绑定Fleet＋owner＋独船＋juggernaut的设计／成长路由；六core各自的Fleet guard；独立section／设计键；专属静态modifier；无replace_path的descriptor。原14check列表从已封原mother报告引用，不能把其通过作为这一新来源检查自动通过。

原光环不是专属成长：`SHIP_AURA_INSPIRING_PRESENCE`仍可使附近友舰射速+5%，实际Relic图已有此表现；本项不排除该原生范围，也不赋予零维护结论。

## 执行结果

已核七生产源与冻结副本同字节、原版船体定义同SHA、完整59文件无ship-size定义、descriptor无replace_path；六真实组件guard逐一解析，原mother14列表明确不含本项。12个来源范围检查通过，35个typed refs逐SHA复读通过。

- [来源隔离限定报告](evidence/1019-analysis/rc7-juggernaut-source-isolation-report-v1.json)，SHA `ac037a88b450ac1ccef012daa57cc62c9d814a9ab07f3d3050a6c317c1451e35`，status PASS_SCOPED／evidence_mode SOURCE_SCOPED。
- [部分提案](evidence/1019-analysis/rc7-juggernaut-source-isolation-partial-proposal-v1.json)，SHA `baeb7f512ac15534f0480102db469ab45b2bd8101a307c6feb0daf009f54e5d8`，只新增支持`other_juggernauts_unchanged=true`，actual_jump仍null、case仍PENDING。

scope明确允许原生光环影响友舰，未声称普通主宰实舰负对照。旧配置包、旧null提案、旧14项报告和已提交scope文档全部保持原字节；没有读取jump／活动日志，没有UI／Git／Mod／工具变动。
