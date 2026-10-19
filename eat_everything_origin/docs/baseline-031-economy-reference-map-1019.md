# 公开0.3.1经济基线：最终发布引用映射

## 目标、范围与方案

只读整理`docs/evidence/1019-baseline`的历史三分支×12月原生SAV，为当前publish_1019.py的`runtime.economy.<branch>.baseline_months`生成精确可复用引用。新报告放`docs/evidence/1019-baseline-reference-map/baseline-031-economy-map-v1.json`；不改旧档/旧报告、不执行UI、不模拟、不改生产/Git、不创建RC6候选数据或PASS。

按hive=bhm、machine=bmm、purifier=bpm映射。m00是2200.01.01启动锚点，m01～12应为2200.02.01至2201.01.01连续12个实际月初，只将后12份放入最终baseline_months。SAV原字节计算完整SHA，并直接读取native country0政府、origin、current_month能源income/expenses；净额按原生当前月预算两者差计算，与旧观察/audit逐一比对，不能把m00旧缓存算成首月。

原manifest/profile/descriptor、语言和EXE/静态包绑定分别保留原义。每份保存引用采用当前schema的date/net_energy/evidence，其中evidence={path,sha256,kind:native_save}，path从eat_everything_origin根使用POSIX相对路径；完整报告另列receipt或归档来源。缺独立receipt必须写明缺失，只引用真实存在的native-monthly集合、audit及archive-index，不补造保存动作。

## 验收标准

报告必须包含恰三组有序12月、每组12份不同SAV、36份完整SHA、原始ZIP完整性和native日期/政府/预算；所有导出引用能在项目根解析并哈希匹配。核对manifest为公开0.3.1基线、Stellaris精确EXE、简中和单Mod，逐项指出原始receipt/索引来源及缺项。记录实际负预算，基线赤字不是新候选失败或通过；RC6没有数据时不生成candidate_months、candidate PASS或对应检查boolean。

## 已确认定位（实施前）

历史run `20261019T053917Z`，manifest.role=baseline、static_gate.version=0.3.1，EXE SHA256 `400df27c82ddc845aa9dce79bd468d81f18f060d299cd263e3afa93aef4f7a83`，language=l_simp_chinese、单Mod。profile_id保留历史eep-0.3.2-single-homeworld标签，不将其误作实际Mod版本。已归档39份SAV包含三个m00；独立`*.native-save.json`只覆盖Hive全部、Machine m00～03、Purifier m00，其它月度来源需继续核原始集合与归档索引，不视为同名receipt已存在。

## 来源补全与实施结果

缺独立receipt的21个月均有已归档的真实集合凭证：`bm-monthly-autosave-receipt.json`覆盖bmm04～12（9），`bp-monthly-autosave-receipt.json`覆盖bpm01～12（12）。报告逐月绑定集合文件SHA、实际snapshot index、原生source路径/mtime/bytes/date/SHA及其anchor/method，未补造独立receipt。其它15个月走原有逐份native-save.json。39份SAV都与archive-index、旧观察、旧audit和原始artifact SAV字节SHA吻合；ZIP CRC、native meta/gamestate日期、Cygnus v4.5.2及唯一Mod均复核。

原冻结baseline/mod的全部文件逐一核path/bytes/SHA，path-NUL-bytes树重算与manifest同为`abca9b4195a991d98ca25336ed7807e0306d30e2c33021e4d307f78e1db864d8`。实际VERSION与descriptor都为0.3.1，历史profile/scope中的0.3.2标签保留，不改成当前版本。最终profile的settings与pdx_settings均记l_simp_chinese，dlc_load只启该Mod。

为使新报告自身的schema/读取器来源不随以后工具修改漂移，实施末尾把当前publish_1019.py、audit_save.py、旧baseline VERSION/descriptor的输入原字节作为非执行`.txt`证据副本存入新报告目录的`source`。这些副本只作来源，不改工具、Mod或旧证据；报告记录原始路径及副本reference。

| 分支 | native government / authority | 首月净电 | 第12月净电 | 负净电月数 |
| --- | --- | ---: | ---: | ---: |
| hive / bhm | gov_devouring_swarm / auth_hive_mind | -38.90665 | -36.05486 | 12 |
| machine / bmm | gov_machine_terminator / auth_machine_intelligence | -161.26091 | -153.60543 | 12 |
| purifier / bpm | gov_purity_order / auth_dictatorial | 32.64322 | 31.03125 | 0 |

每分支政府/authority/origin/civics在本组13份原生档中一致。净额直接将原生current_month各energy收入与支出按十进制文本求和；旧观察浮点尾数另列，例如-38.187239999999996与原生文本净额-38.18724，同原生5位小数吻合，不改旧观察文件。缺失的原生stock energy字段仍写ABSENT/null，未填0，也不把库存耗尽后的预算赤字隐藏。

最终JSON的`economy_baseline_payload.<branch>.baseline_months`就是可交给publish的12行数组；各行仅date、net_energy、evidence，其中evidence的path从eat根起、kind=native_save、SHA全64位。使用时只赋值该数组，保留主线程真正的候选月度字段。report.branches保留各原始样本/凭证、3个排除的m00锚点及来源详情。报告status=OBSERVATION_ONLY，未生成candidate_months或任何候选PASS/检查boolean。

本轮离线核对完成：36份不同且连续的月度SAV、3份独立启动锚点；39份CRC、原始artifact SHA、capture凭证、旧audit/gamestate SHA及原始预算全部匹配，无差异项。新报告185227字节，SHA256 `07e2c61203d350d40c5ef1b4600622a1b4d3d135ed5c27624ad2a6342cced847`。4个输入原字节副本均在新`source`目录，未复制/更改SAV。所有文件留给主线程统一审查提交；本线程未执行Git操作。
