# RC7 保护条件 B 组

简体中文、单生产 Mod，run `20261019T204055Z`。原生 ready 是 `r9gbDiag1`，
日期 2201.01.22；idle/fired 均为 2201.01.23。ready 的 `r9gbR` 导入别名与
原件 SHA 相同，仅用于避开原名 1/l 的 OCR 混淆，不是新的原生保存。

真实殖民中对象为物理9/colony18，colonizing_species 为本国 founder；该版本
引擎同时认为它已是 colony。地战为物理17/colony1/ground_combat0，攻击军73
属于本国，守军10～18属于敌国；双方实际 combat 关联和血量已核。外国次级
核心为物理8，真实 owner/controller1、EEP core 标记和人口持续，本国实际受益
核心仍是可用的物理2。三档前提均成立，三段原 dispatch 的实际 marker 完整。

原 receiver 三个 no-settlement 任务全部通过，I/F 全部 EEP 变量、Mother 层数
一致，原 growth 两支均通过。完整 strict 差异、长地战探针解析异常、两次读取前
的列表识别失败和即时日志断言失败均保留；备用短 dispatch 没有执行。

391 份原件共 20,771,236 字节；三份 SAV ZIP CRC、audit/receipt SHA 与日期、
84 对 GPU 截图/OCR 及全部 source-copy SHA 已校验。完整停机日志仍待最终审计。
仅支持殖民中、地战和 A/B 合并的目标完成重校验；完整 core 拒绝仍等 C，核心
失主及全 invalid 无成长仍等 D，全部整组继续 PENDING。
