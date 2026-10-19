# RC7普通拆解检查点数量的只读合同复核

root拟将普通q2的采样从每月保存改为start→FF30 m01→FF90 m04→临界前precomplete→1日自然完成，以减少重复SAV；本页仅核既有合同，不读取尚活动normalready或任何未来normal输出，不改已sealed接收文档、命令、工具或矩阵，也不创建未来角色。

## 原合同依据

- `tools/publish_1019.py:49`的normal_dismantle_regression仅要求normal_duration_preserved、normal_seed_preserved、normal_completion、normal_reload_idempotent四项。`:789`的通用case校验要求这些检查和证据引用，但没有normal月度SAV计数。`:804`起的12个连续且不同native月度SAV硬要求，明确只用于hive/machine/purifier economy，不适用于普通拆解。
- `tools/receive_functional_1019.py:23`仅列normal建议角色ready50、decision_start、precomplete、immediate、stable、duplicate、reload，没有m02/m03。`:278`起要求实际roles非空并逐role做原始来源绑定，不限定normal角色名或数量。`:235`的task执行只转调原checker。
- `tools/check_1019.py:187`的settlement读取before/after和可选reload；`:246`normal分支核持久q、实际owner0、before存在对应target Situation，没有m02/m03或月度样本计数。该检查器本身不替代duration和UI决议证据。
- `testing/colossus_1019_postfire_plan.json:218`有FF30并记录实际checkpoint的原执行安排，但`:232`的native_saves列表是normal-start、normal-month-1、normal-month-N、normal-prefinish、normal-done、normal-repeat，没有指定m02/m03文件。`:62`的ordinary_duration明确要求started SAV中的T，calendar_days_not_fixed=true及next-day threshold check。
- 当前`rc7-functional-next-execution-1020.md:139`确实写了FF30逐月保存，因此采样变化仍应由root在执行前另行docs记录；这是对既有执行安排的调整，不需要改validator或验收四项。

## 建议

可以省去m02/m03原生SAV。保留真实ready50/start（种子与原生T5）、m01和m04的真实Situation身份/target/progress、precomplete仍活的源及真实founder groups、自然完成immediate/stable、重复回调和真正Load后新SAV。m01/m04的progress必须照实读，不凭文件名推定；中间FF90保留实际输入、HUD日期等待和之后的原生状态。现有重复／重载及迟到月脉冲检查不因本次省采样自动删除。

FF29可作为m04之后的候选推进量，不能预定它一定恰好到precomplete或把T5改写成严格149／150日合同。先读m04实际progress和日期，按原门槛定位最后未完成状态，必要时只用更小自然推进；确认该SAV仍有原Situation、source尚活、q/T不变后，再1日自然完成。若实际未在该1日完成，就保留实际结果并继续按既有边界策略定位，不写progress、不手动调用完成、不中途追改期望来迎合after。

减少中间保存不改变Return或人口核对：仍只从precomplete合格founder groups独立求R；other_core_pop_delta在读取自然完成after前固定独立依据，不能以少了m02/m03为由用after残差拟合。三类开局12月经济矩阵保持不动。

结论是“原validator无m02/m03数量硬合同；可在root先记录采样调整后采用m01/m04与真实完成边界的证据路线”，不是已经通过normal运行验收。没有读取normalready、active fire/logs或操作UI/Git。

本次核对原源码SHA：publisher `06c60c0a9bd406580314999ae6649365bb5c1fa6c7152c0b0a7fb5a420e06918`，receiver `d4daa66a575fa8c0ce5bba9796b6c6d4eef0b0573184ec9b6c4e5102fd033ca5`，checker `681836d2da9c6b28ee9bfd583c87e5ced96f06543901e71d3dc35fa226f3afdc`，原39计划 `76adabaf82dc2c10894222bdb425ee1b994307233e1bccb2c251bdf2f07325c8`。仅交付本文一个新文件。
