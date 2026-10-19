# RC6成长同日reload：government原文差异诊断

## 目标、范围与判据

主线程报告RC6 C10000同日`r6grepeat`→`r6greload`的selected country/fleet/ship变量和health相同，但government_raw SHA不同。本次只读两份固定原生SAV及现有`check_growth.read_save`提取定义，核完整government原文的字段、值、结构与精确差异。仅输出新诊断，不改checker/模型/历史报告，不放宽严格same-day business compare或回填任何FAIL。

输入优先`docs/evidence/1019-rc6-growth-v1/run`已封存副本，必要时只读固定external run150008Z。主线程另授权追加只读RC7固定`r7ganchor`的同一字段；不读collector任何新样本、不操作UI/Git。判据是绑定两份完整SAV SHA/日期/身份/C10000及government原文SHA，逐字段与统一diff记录实际变化，不猜测引擎缓存或因果。若字段/结构不止一处，全部保留；本诊断不把RC6差异自动转成RC7可接受范围。

## 实际差异

唯一变化是**`unlocked_civic_council_slots=0`→`4`**。不是议程进度变化：两档`council_agenda_progress`都为7039.5。九个direct字段的顺序和结构相同；仅替换这一处数字后，两份完整government原文逐字符完全相等。type、authority、civics、origin、council_positions、council_agenda、picked_council_types等均原样保持。这里不推断变化由什么缓存或引擎流程造成。

| 固定输入 | 日期/C/实体 | 完整SAV SHA256 | government原文SHA256 |
| --- | --- | --- | --- |
| `1019-rc6-growth-v1/run/r6grepeat.sav` | 2202.07.01/C10000/fleet125/ship809 | `5115fb184de72db0afe4ff5baf0b645013275a5a6df572f0d75dc086092243fa` | `8007a5f318e3a4c7763bf892e3b56d60aaec2683be7ed8aa04caf4e2b93c3957` |
| `1019-rc6-growth-v1/run/r6greload.sav` | 2202.07.01/C10000/fleet125/ship809 | `b23e00c98b5bd3ecf5fe3c496e500f0049ba7822ee030e49d102405c39d53c91` | `89f45d2cc2b998219f95436152138ed6048ebea8ad55c9d77060e430afcb9396` |

```diff
 council_agenda="agenda_infinite_opportunities_gestalt"
 council_agenda_progress=7039.5
-unlocked_civic_council_slots=0
+unlocked_civic_council_slots=4
 picked_council_types=
```

实际调用现有`check_growth_1019.read_save`读取两份已归档原生SAV，校验各自原始receipt SHA及ZIP CRC；它提取的是country0的完整government块。本次也独立确认country_variables、fleet_variables、ship_variables和health各自全等。其余全SAV差异不在本次诊断范围，不能把此结论称整SAV相同。

当前`business()`包括完整government原文；这处council解锁数量不是可忽略的时间进度。因此RC6同日严格business比较失败仍然成立；没有改checker、模型、忽略列表、历史报告或FAIL结果。

## 仅作入口观察的RC7固定锚点

按主线程追加范围，只读fixed run164112Z的`r7ganchor.sav`，原始SHA256 `aec53eeed736d23abb856b7a1c1696657ce55517124097f1ad6c69921f1d8385`，2201.01.01/C0。其实际`government.unlocked_civic_council_slots=4`。这只说明该新入口已有不同初值，不预测RC7真实repeat/reload一定通过。未读取collector新档，未来仍以独立真实RC7前后receipt/SAV作严格判定。

## 诊断载荷

[独立JSON](evidence/1020-rc6-government-reload-exactdiff-v1/diagnostic.json)，SHA256 `87575ad0a3a27965ed18a73c80f75a2f5cd8d66076f45b8428eb2e8928143fc5`，status=`OBSERVATION_ONLY_STRICT_RC6_FAILURE_RETAINED`。同目录保存两份RC6和一份RC7锚点的government原文、完整unified diff，均以UTF-8原始摘录字节落盘且有完整SHA；JSON绑定两个原生SAV/receipt及读取器源SHA。全部是新诊断文件，原始存档、历史报告和检查器未改。
