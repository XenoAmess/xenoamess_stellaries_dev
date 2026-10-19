# RC4 巨像长时序的原生月初存档采集

## 实施前目标、范围、设计与验收

RC4已原生确认Mar8充能0／90、Mar9为1／90；主线程已点击原生停止按钮并保存同日cancel。接下来重新以原生右键菜单下令，保存独立requeued作为同日基线；完整90／30时序仍待验。仅这一受控功能分支可使用下述采集，不混入开局经济。

为减少中间UI存档，复用既有月初原生autosave校准协议：从Mar9真实推进22日至Apr1，随后分别推进30日至May1、30日至Jun1。每一步保留物理输入、GPU／OCR实际日期，读取当前history目录本次新生成的autosave，复用runtime_growth_1019.fresh_native核对命令开始时间、旧／新mtime、完整ZIP CRC、原生日历、母舰归属及SHA，原字节独占归档，不编辑SAV。

采用单独的`pk2-monthly-autosave-receipt.json`观察记录，逐项保存source/date/SHA/bytes/mtime和实际动作；不得伪造UI保存receipt。缺失新文件、错误日期、错误归属或哈希不符立即停止，保留失败。长时序每一步都从实际日期前进，不把三次推进合并为一次跳月。

各步另存不可变的`<stage>-receipt.json`，总receipt只在三步全部完成后新建一次，避免增量追加改变已经引用的receipt哈希；中途状态使用不参与receipt匹配的progress文件。重新下令先用本次可见目标名称及原生菜单核对；未匹配的旗帜右键尝试保留为失败，未产生订单，不覆盖其截图。

随后根据真实Jun1订单进度决定进入发射阶段所需天数，再用原生UI保存fire阶段、临近完成和完成三档；完成档只要求仍存活的country0。若跨越下一个月初，可同样采集该月初原件。每份中间档均核目标仍存活、EEP账本无提前增长；windup_time与fire_time分别必须真实为90与30。最终人口差使用非月初的一日precomplete→fired对照，不能从结果倒推自然人口增量。

本计划不改变生产Mod、军队、资源或世界状态。取消、完整完成、重载及重复回调各自保留限定检查，月初自动采集成功本身不代表玩法通过。

## 2026-10-19 Apr1 collection recovery

The first collector reached Apr1 but stopped on FileNotFoundError before archiving: native autosaves remain in the actually loaded acceptance-fixtures folder. The history field is a manually retained copy, not proof of native autosave destination. Recover the fresh Apr1 original from acceptance-fixtures using the already recorded advance timestamp and actual HUD date; record missing-path failure and original file metadata explicitly. Do not advance Apr1 twice. Continue May/Jun in the observed native directory. The earlier source-selection assumption is withdrawn.

## Duplicate-callback attempt correction

The first post-fire probe incorrectly used on_destroy_planet_with_EEP_PLANET_KILLER_DISMANTLE, which does not exist. Native error.log at 20:05:42 explicitly rejected it. Preserve all physical commands, error and pk2dupe Jul10 raw bytes; this sample only proves a natural next-day state, never duplicate dispatch. The exact production on_actions key is on_destroy_planet_with_EEP_PLANET_KILLER_DEVOURER. Repeat twice with that exact key and explicit FROM Mother fleet, advance Jul10 to Jul11, and save pk2dupevalid. Then native-load the valid sample and dispatch once more before advancing to Jul12/save pk2dupereload. This corrects test input only, not production Mod.
