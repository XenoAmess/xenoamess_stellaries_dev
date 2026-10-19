# RC7旧伤输入的实际文件导入复核

## 目标与范围（归档前）

主线程已完成两个真正旧伤SAV的文件导入，尚未执行原生加载。本轮只复核固定run `20261019T164112Z` 的实际`r7migration-imports.json`及其明确列出的两个source/copied文件；按两个精确文件名枚举隔离userdir的save games以检查唯一性。不读取游戏状态、活动r7normal/fire/logs或未来迁移输出，不操作UI/Steam/Git，不改已封口准备包、旧计划或case。

新的薄归档为`docs/evidence/1020-rc7-migration-input-imports-v1/`，只保存原始导入receipt及独立复核记录。旧SAV只引用仓库canonical三件套，不重新复制。原准备case的未来SAV/load/action SHA继续保持null。

## 已提供的导入记录

实际receipt位于`C:\Users\1\AppData\Local\xenoamess_stellaries_dev\artifacts\1019-implementation\runs\20261019T164112Z\r7migration-imports.json`，主线程给定SHA为`f968da8b4e14f7a725b1db7a7c9f385304978bd732b6023a17f21e673da8d0f9`。receipt schema为`eep.rc7.migration-imports.v1`，scope明确“no native load yet”。

两份source来自`...\artifacts\1019-legacy-damage\runs\20261019T130448Z\`，copied仅在`C:\Users\1\AppData\Local\xenoamess_stellaries_dev\runs\20261019T164112Z\save games\acceptance-fixtures\`：

| 文件 | 原SAV及copied应有SHA256 | 字节 |
| --- | --- | --- |
| p031before.sav | `d5921823d723d4eb0dec5d912ae0e586aac5b903643472d44062229b66b0b1e2` | 492290 |
| ppaidbefore.sav | `40c8f8dac9530594d501143132d55fef1205346d7f679f16c8858058ed392ff1` | 561795 |

这两个旧SHA与已封口`1020-rc7-migration-restart-preparation/input-inventory-v1.json`一致。最终引用可复用`docs/evidence/1019-legacy-damage-run-final/run/p031before.sav`和`ppaidbefore.sav`，不将复制后的文件当作新的native-save角色。

主线程报告在调用原`copy_seed_save`之前做过源SHA及目标不存在守卫，没有覆写。本次独立复核能证明当前receipt/source/copied的字节关系及当前路径唯一性；原receipt没有记录导入前目录快照，因此不能由本复核单独证明历史不存在状态，主线程操作描述应与独立观察区分。

## 设计与验收标准

1. 先核实际receipt完整SHA、schema及恰好两个预期记录，再复制其原字节到薄包，复制前后receipt的SHA/大小/mtime保持稳定。
2. 分别只读两个source及两个copied，确认源路径、隔离目标路径、完整ZIP字节大小/SHA、成员名称、解压gamestate大小/SHA与receipt一致；保留每个实际路径和原始读数。
3. copied解析后的绝对路径必须恰为当前隔离profile的`save games/acceptance-fixtures/<原名>`，不能仅凭相似字符串接受。递归枚举save games中相同文件名各恰一份，且正是receipt copied路径。
4. 新包只有receipt、复核记录及`.gitattributes`；不含SAV副本、不运行native_load/save/check、不改变任何prepared case的未来hash或状态。输出只能为文件导入的限定事实，不是迁移或重启验收通过。

## 独立复核结果

两个source及两个copied的完整字节、大小、ZIP成员及gamestate大小/SHA全部与原receipt和封存输入SHA一致；两个copied均恰在指定隔离profile的acceptance-fixtures下，递归同名文件各一份。四份SAV和原receipt在读取期间的大小/mtime保持稳定，归档receipt与原文件逐byte相同。

薄包已形成，状态仅为`IMPORT_BYTES_VERIFIED_ONLY`。原receipt SHA仍为`f968da8b4e14f7a725b1db7a7c9f385304978bd732b6023a17f21e673da8d0f9`；独立`verification-v1.json` SHA为`b72a36494612ea90c53c1d8a8e84542a3cecd7a3522027e8d1d190d36c4e6545`。未生成任何迁移check报告或native角色，没有修改已封口case的未来SHA。receipt中的“尚未native load”是导入时的记录，不用于推断本次交接后的游戏当前状态。
