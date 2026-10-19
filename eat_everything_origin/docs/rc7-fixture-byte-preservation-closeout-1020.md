# RC7 收尾：测试夹具的 Git 原字节保全

## 目标、范围、方案与验收（修改前）

交接前只读核对发现，两个本轮夹具 JSON 的工作区 SHA 与 HEAD blob 不同：Git 的 `core.autocrlf=input` 在提交时把 CRLF 转成 LF，而封存报告引用的是原始工作区字节。这会使新检出无法复现引用 SHA，必须在交接提交中修复保全方式。

范围只限 `testing/normal_selector_probe_1020/`、`testing/empty_planet_selector_v2_1020/`、`testing/normal_population_control_1020/` 三组本轮夹具及子项目 `.gitattributes`。先记录本设计，再为这三目录设置 `-text`，按原始工作区字节重新暂存。不得修改夹具正文、原始报告、SHA引用或生产 Mod，也不修改 `open_kaishek`。

已观察到的例子：v2 `commands-v2.json` 工作区 SHA `7b90bc9d247b119f4ac66aac6771236b3cea64402defd95324bd5ffe2c38a99d`，旧 HEAD SHA `6def0583593476b7833d0baea8d1e9837e6e67301c5df09e1863d0db9ef4d2ba`；probe `console-commands.json` 工作区 SHA `3b49b87667869efc4aeca27155de08882775237bf2268ea9f62f4890fb1b65ff`，旧 HEAD SHA `f302de79e602070c15ba22008e6fc9b3fce38df4e20e341ed6ef4e870c92fc13`。相应中文设计文档的 HEAD 与工作区原字节相同。

验收：三目录所有实际文件的暂存 blob 与原工作区逐字节一致；保留原 SHA；59文件生产包树仍为 `61b34f6dbdc277c44364889d5f1e1cd2773a4624786bbf0d538079fc6ba4feb0`。保全校验记录写入 `evidence/1020-rc7-fixture-byte-preservation-v1.json`；这不是重新执行实机或提升 Mod 验收结论。

实际结果：13文件全部原字节一致，9个已有文件的旧HEAD曾被换行转换，现按原SHA保全。首次普通 `git add` 未刷新未改动文件的归一化缓存，断言失败且尚未写结果；随后在 `-text` 规则下执行 `git add --renormalize`，只刷新暂存blob，不修改工作区文件，全部断言通过。校验报告SHA为 `c856e5f17522a385695cb055eb801a00ab0daafa25396d4ff3aeb35f73574c20`。
