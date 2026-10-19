# RC4 全新 PENDING 运行时索引 v1

## 目标、设计及验收（实施前）

为 `0.4.0-rc.4` 新建 `rc4-runtime-progress-v1.json`，使用既有scaffold／pending helper，源为59文件、树 `06485dc540a88b30cef15c27c323ff21cd88f04ad57b79e4f5bc0590937ef468`、唯一run `20261019T112808Z`。不从RC3 progress复制任何case、预算、成长、组件结论或单项true。初始18组检查全部null，case／组件／顶层全部PENDING；所有基线及候选月度数组、growth_samples为空。RC3仅可在显式historical archives留痕，不作为当前case evidence。

静态门禁必须绑定root自己冻结的2e249c报告、RC4新CSV-loader／numeric来源合同及三回调合同；不把external7c的LF规范化报告替换进既有run。manifest／gate／source-copy／SAV／输入全部只读，未来阶段包的manifest仅登记一次作为canonical。同一run的其它manifest副本只放archives，不再次add-run。

当前实际存在的受限报告是：

- `rc4-pk2base-configuration-report-v1.json`，SHA `b626422942b18cee6883d586fcf002e6f455a3c78547c991fa18ea916419effe`，20项仅证明RC3未发射fixture载入RC4后的来源、基线、安装组件与配置；不是新开局、旧正式0.3.1兼容或实际时长通过。
- `rc4-pk2-queued-day1-report-v1.json`，SHA `8efe970dee9bbe59d259b3500c2f46ef67b96ff174dfbf5765144b54a0558be5`，18项仅证明真实订单接受、首次采样原生windup_time90／progress0及未提前结算；还没有完整90天／30天阶段或真实毁星结论。
- `rc4-pk2-base-queued-no-settlement-report-v1.json`，SHA `1eb7e5232d1348fce36907eb5dba5677cdaf5e8315a26850ec0c4a180a8aba82`，9项同日未再次结算事实；不把day1跨日strict差异转换为无差异PASS。

等待验收线程完成实际项目内RC4阶段包后，再将其原字节三SAV、audit／receipt、真实输入／截图／分析挂到相应巨像观察组。若阶段包尚不存在，只写有实际文件的静态／报告草稿和缺口，绝不填写将来的项目SAV路径。报告中的PASS_SCOPED只在 `_progress.scoped_observations`保留原checks／scope／limitations，不自动映射完整case checks为true；实际发射、90／30天、取消、守卫、统一结算等仍待后续证据。

验收要点：独立核阶段包索引／源及loaded59文件／三SAV解压gamestate／audit／receipt／原始输入；全部index引用必须实际存在并通过SHA，manifest的单Mod、简中、精确EXE、新tree及2e静态报告必须一致。runs只有1项且run_id唯一；case checks真值数0、18组PENDING，所有预算与growth为空；旧RC3索引／报告／原型、root新run／gate／manifest均不改。最终check-runtime应拒绝该PENDING进度。本轮不改工具或生产，不操作UI／Steam／提交。

## 后续归档后的最少更新方式

从仓库根目录先把现版进度复制为下一版，保留本版SHA。下面路径均相对 `eat_everything_origin`；`$archive`只能设置为已经落盘、独立核验完成的实际阶段目录。尚未给出此变量的值时，不运行依赖它的命令。

```powershell
$current = 'eat_everything_origin/docs/evidence/1019-requirements/rc4-runtime-progress-v1.json'
$next = 'eat_everything_origin/docs/evidence/1019-requirements/rc4-runtime-progress-v2.json'
if (Test-Path -LiteralPath $next) { throw 'Preserve the existing next version; choose a new version.' }
Copy-Item -LiteralPath $current -Destination $next
$helper = 'eat_everything_origin/tools/runtime_index_1019.py'
$idx = 'docs/evidence/1019-requirements/rc4-runtime-progress-v2.json'
$run = '20261019T112808Z'
$archive = 'docs/evidence/1019-rc4-pk2-duration'
# 已登记该run：不重复add-run，只追加真实证据并自动计算SHA。
python $helper --index $idx attach --case colossus_cancel_idempotence --run-id $run --kind native_save --file "$archive/phase2/pk2charge1.sav"
python $helper --index $idx attach --case colossus_cancel_idempotence --run-id $run --kind native_save --file "$archive/phase2/pk2cancel.sav"
python $helper --index $idx attach --case colossus_cancel_idempotence --run-id $run --kind analysis --file "$archive/phase2/analysis/rc4-pk2-charge1-cancel-report-v1.json"
python $helper --index $idx missing
```

每个新增真实文件只需case、同一run-id、kind与file四个参数。当前三个native阶段已经收录后不必重复执行；同路径同SHA幂等，字节不同必须归档新版本，不能覆盖。后续90／30天或守卫／取消分析必须先独立审查实际范围，再用observe-check填写明确对应的单项；不把一个报告的所有PASS自动导入。完整活动logs等最终停止冻结后另版补入，RC3 logs不充作RC4 logs。

## 实施及独立核对结果

阶段包 `docs/evidence/1019-rc4-pk2-duration/archive-index-v1.json` SHA `b82cc8fb9ad0ab8fd67c4b9df2454837fb9f91ecdc452930e57d0286329d2712` 已完成并独立核验：265份／15,174,376字节全部和当前原来源一致，source／copied各59文件精确对应，三SAV的audit／receipt／CRC及gamestate逐一匹配，20项集合验证成立。canonical manifest SHA为 `a83c605727f30a1d68db0e076348d814824d8ca56020ca2ab8864db8194f44f1`，唯一run `20261019T112808Z`，静态报告仍为原始2e249c；没有改动任何root gate／报告／manifest。

通过既有scaffold和pending helper生成全新 [RC4 progress-v1](rc4-runtime-progress-v1.json)，SHA `2cf16f8eebd1c4f09ee9d21c25c5b7f146e0a15ee36b88fd1aed23b224d6d36a`；[实际引用计划](rc4-runtime-reference-plan-v1.json)无预测或不存在路径。69次引用／38个唯一文件全部匹配，0个case单项true，18组／组件／顶层均PENDING，所有预算和成长样本为空。仅保存本轮20／18／9项限定报告及原生观察：首次采样日期2200.03.08，windup=0／windup_time=90；native fire_time字段尚无，30仅是TXT配置。queue→day1的strict FAIL、早期缺帧及索引构建路径假设失败材料保留，未扩成完整玩法通过。6条RC3引用只在显式historical archives，均不用于当前case。

[独立字节审核](rc4-runtime-progress-v1-byte-audit.json) SHA `6eb0645622403e6250b5e7a12ea38a3e6fefb820ec268020107aaefa15f0e34e`；最终运行时验收器仍按预期拒绝PENDING。所需新代码／测试修改为0，本轮执行的是实际归档核对、既有helper绑定和最终门禁的预期拒绝检查。

收口期间验收线程另行交付archive-v2的charge1／同日Stop材料；本v1保持仅base／queued／day1，不追加后续阶段。上方最少更新命令现使用真实存在的phase2路径，需先审查独立archive-v2与报告范围，再另建progress-v2执行；这些命令只挂证据，不晋升任何case。若要把新集合索引一并纳入archives，可通过既有 `update_progress`／`add_reference`／`collect_reference` API登记真实index及verification文件，无需手填SHA，也无需再次add-run。

主线程最新执行安排是本v1封版即止，不为每个小采样反复创建索引或大包；上方只是既有helper接口示例，后续集中收齐完整shot、成长、经济等批次后再更新。真实充能／取消的新材料独立保留，不因本v1尚未挂载就重复实机。
