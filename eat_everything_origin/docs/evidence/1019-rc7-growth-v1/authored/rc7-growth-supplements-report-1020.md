# RC7成长补充原生观察与正式报告

## 目标、范围和封存边界

RC7九节点/18原生样本的独立逐对观察、方法、总结及其原文档全部封口，后续不追加或重写。本文件单独记录补充与正式report。既有独立总结SHA为 `5a4c28e85dcf10ab79f3d1feac7817f4da66b09262c1c438e71927f2c056aae1`，原观察md SHA为 `fc79c318afaf43f3d211e898ec9bc3d3dcafdc2ff081ad63bd63c7b708b811b7`；本轮不把旧RC6失败改成通过。

运行 `20261019T164112Z`，RC7 tree `61b34f6dbdc277c44364889d5f1e1cd2773a4624786bbf0d538079fc6ba4feb0`，简体中文，Mother125/809。主线程独占UI执行补充worker83762；本代理不操作UI、不读活动日志，也不在worker活动时读取回执内容。仅待主线程明确通知worker结束且四份预声明native-save回执全齐、对应原生SAV及audit稳定后执行既有纯离线checker。

范围为九节点成长矩阵、相同日期两次同步幂等、真实原生UI加载后的业务幂等、20500单次200预算与下月原生自动补差。当前入口为RC6干净C0导入RC7，因此不提供startup receipt，不把其解释为RC7新开局全年。三政体新局全年、报告UI、实际回血和面板DPS、完整gamestate相等仍分别验收。

## 事前补充设计

以C10000/R200/P0、六tier合计200的已完成矩阵尾端为前件：

1. `r7grepeat.native-save.json`：同日两次 `eep_sync_mothership`，C/L/B/R/P、六tier、实际设计载荷、业务资源/政府原字段和属性不应新增或损失；same-day政府raw继续精确比较。
2. `r7gload.load.json` 与 `r7greload.native-save.json`：主线程原生UI加载repeat后同日再次保存；业务成长、装备、属性应保持。designID、native默认字段补写等完整gamestate差异另列，不用业务通过冒充完整原字节相等。
3. `r7gbudget1.native-save.json`：同日只setC20500并同步一次，L2050/B410，原R200只补200应R400/P10，六tier合计400，无人工重置tier或追加第二次手动同步。
4. `r7gbudget2.native-save.json`：第一段之后只独立FF30，下一月原生调度应补10至R410/P0，六tier合计410。正式checker指定 `--budget-second-mode monthly`，不把手动路径当自动调度。

数值规则完全沿现checker与源模型v1–v5：属性源系数不变，HP量abs=max(.01,8*ULP32(expected))/rel0，十modifierabs.01/rel0，账本/tiers/身份精确。预算样本只检账本和对应业务范围；不使用20500未重新导出的旧modifier变量强判新等级属性。

## 正式report入口与验收标准

固定工具 `tools/check_growth_1019.py` SHA `a8d70f1015b6f1f4026ae811c38653997fd41a55bbca9b9b8fba391fb4070bf5`。在主线程完成通知后，先核原九份观察和总结SHA仍封存、当前checker和五模型SHA不变、所有输入回执/原生ZIP稳定；再只运行既有report，不改工具代码或生产包。

```powershell
python -X utf8 -B tools/check_growth_1019.py report `
  --receipt C:/Users/1/AppData/Local/xenoamess_stellaries_dev/artifacts/1019-implementation/runs/20261019T164112Z/r7mx-growth-receipt.json `
  --repeat-receipt C:/Users/1/AppData/Local/xenoamess_stellaries_dev/artifacts/1019-implementation/runs/20261019T164112Z/r7grepeat.native-save.json `
  --reload-receipt C:/Users/1/AppData/Local/xenoamess_stellaries_dev/artifacts/1019-implementation/runs/20261019T164112Z/r7greload.native-save.json `
  --budget-first-receipt C:/Users/1/AppData/Local/xenoamess_stellaries_dev/artifacts/1019-implementation/runs/20261019T164112Z/r7gbudget1.native-save.json `
  --budget-second-receipt C:/Users/1/AppData/Local/xenoamess_stellaries_dev/artifacts/1019-implementation/runs/20261019T164112Z/r7gbudget2.native-save.json `
  --budget-second-mode monthly `
  --output docs/evidence/1019-analysis/rc7-growth-native-report-v1.json
```

命令工作目录为 `eat_everything_origin`。输出独占新建，若FAIL或工具异常原样保留，不修改输入、容差、模型或覆盖输出。只有报告定义的全部已有checks通过才报告其PASS_SCOPED，且保留缺失startup_stability与其他明确范围限制。需要另写解释或新探针时另建证据，不能重写此v1。

## 固定输入与正式结果

主线程明确通知worker83762已正常结束exit0之后，本代理才读取补充内容并执行上述命令。所有四份native-save回执、load回执、各原SAV/audit和已完成growth receipt在报告前后元数据完全相同；封存九pair/方法/总结/原md、当前checker与五模型SHA复核均未变化。没有读取活动日志或UI。

| 阶段 | 原生日历日期 | 原ZIP SHA256 |
| --- | --- | --- |
| repeat | 2202.07.01 | `f733e79be5cb9cac7ad9101fc171d5bf4ddfe5fdc7adce479c3b8dae6bd2eb52` |
| reload | 2202.07.01 | `a1458045bc7b9bb18ea7ef91b539617a3f0b8e731b0911d8a06a33884a1390aa` |
| budget first | 2202.07.01 | `bf7eeee89794dcdec2fa88adfdcca2053abe30cfd5e26aab2489974980e5733f` |
| budget second | 2202.08.01 | `4819bbc06040c8af28e6ed8f6e53f8a7286f82c2dfac43ffba4c7f5eca11d8aa` |

原生load回执 `r7gload.load.json` SHA `19c6053c18ada6fc9b6fa7d5771e613a2c7a866935212ae2d73419eb2b8b5257`，source指向repeat真实history文件、source SHA与repeat原ZIP一致，`ui_date_verified=true`。回执本身保留 `state_verified=false` 和随后另存audit要求，不将它擅改为成功状态；后续reload原生保存与正式业务比较提供独立状态证据。

正式输出 [rc7-growth-native-report-v1.json](evidence/1019-analysis/rc7-growth-native-report-v1.json)，SHA256 `4677e82c62ce30851f247691dad38703f52d6187ce26f2e63ea9fe0d7df9d1a3`，schema `eep.six-core-growth-report.v1`，命令exit0、状态PASS_SCOPED。全部定义范围共1850项checks通过：matrix1125、ordinary_controls616、repeat20、reload20、budget69；六核心正tier覆盖齐，实际最终层数shield28/armor37/hull44/damage25/tracking27/regen39。

重复同步的原ZIP SHA与C10000 final完全相同，正式报告 `strict_gamestate_equal=true`。reload的业务20项通过，实际设计body SHA仍为 `be9562535dd559dbc4c74de4b8687d2075bbdd1b41b897e6b771ac98627129d9`，designID由16777235变16777257，报告如实保留 `strict_gamestate_equal=false`；不能把该业务通过表述为全gamestate相等或移动starbase旧缓存已修复。

预算第一段独立记录R400/P10、六tier合计400、相对原R200增加200；第二段在下一个月2202.08.01记录R410/P0、合计410、再增加10。正式budget路径为 `native next-month automatic compensation`、属性范围明确Counts only，不以旧导出强判新奖励属性。它给显式while count200与月度补差提供本轮真实证据，原RC6的R300/P110失败仍原样保存。

`startup_stability` 为NOT_PROVIDED，未传startup receipt。此报告不覆盖RC7实际三政体新开局全年、报告UI、实际回血、面板DPS或完整gamestate相等。所有报告原字节现已封口；本代理未修改既有工具、collector、生产、历史证据或进行Git操作。
