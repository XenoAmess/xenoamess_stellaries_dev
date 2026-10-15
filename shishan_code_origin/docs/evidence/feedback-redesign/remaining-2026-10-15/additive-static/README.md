# 经济夹具与只读矩阵审计器的静态证据

本目录仅归档静态门禁和只读工具开发证据，不包含完整组合包或原生七分支经济矩阵。来源报告逐字节复制，见 [evidence-files.json](evidence-files.json) 的来源路径、大小、SHA-256 和双边相等检查；历史绝对路径是当时运行环境，不代表文档 checkout 必须具有相同绝对目录。

- [开发及复制合同](additive-fixture-development-contract.json)：正式 90 文件未改，14 个测试额外文件，共 104；含生产/测试逐文件哈希、结构负例及十语静态本地化结果。
- [组合包 G1](additive-fixture-open-kaishek.json)：29/29 P 文件、13 DDS、279 键/语及有限预检通过。此门禁不证明所有 opcode 或实际经济。
- [23 项开发测试](additive-matrix-development-tests.json)：保存实际 unittest 日志、Python 版本及审计器/测试/native parser 源码哈希；明确使用替身，不算实机经济 PASS。
- [七支 manifest 模板](additive-matrix-manifest-template.json)与 [pending 报告](additive-matrix-pending.json)：21 个实际快照均未填，**NOT RUN**。
- [读取器冒烟报告](additive-matrix-reader-smoke.json)：读取两份既有真实旧档，U 均为 7，floor 档 P/W 缓存严格 FAIL 保留；未拼成实验矩阵。

夹具源码位于 [testing/mod](../../../../../testing/mod)，审计器位于 [tools/audit_additive_runtime_matrix.py](../../../../../../tools/audit_additive_runtime_matrix.py)，设计与解释边界见[经济探针设计](../../../../remaining-additive-economy-probe-design-2026-10-15.md)。source_profile 只是声明的隔离包有限源表审阅，不自动求解全部原版动态 `_add`；外国经济等未纳入来源保持 NOT COVERED。非简中翻译静态校验通过，运行时不在范围内。
