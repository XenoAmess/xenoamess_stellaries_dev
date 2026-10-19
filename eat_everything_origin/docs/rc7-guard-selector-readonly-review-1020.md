# RC7新Machine基线的既有选择器适用性复核

目标是在已封enemy_base原生SAV上只读核对既有guard批处理、uncolonized/neutral绑定、normal owned_q2_setup及迁移后备core选择器的先决条件。输入仅封口的r7pkbase.sav（SHA `11a5be54afb00099824972109a85f3e6f4eb5148cecfe6c488e422d4beb22193`）、原39命令、RC6执行map及`rc7-functional-next-execution-1020.md`，不读取活动fire、UI或日志。

范围是解析现有脚本的真实筛选条件和当前原生对象，列母星系origin5排除core2、已reserved与已有aliases后的精确候选IDs，判断既有绑定能否选择不同源，核普通owned q2与后备core选择范围。随机选择器只报告可能集合，不能将某个候选冒称未来实际抽中。若条件不足或冲突，先给最小调整建议，不执行设置或改fixture/命令/工具，不增加验收要求。

验收为source SHA稳定、物理planet与system origin/colony ID区分清楚、条件逐项对应原命令，并把当前事实、候选数量/ID、冲突和仍须实际执行核实项写入本文。全部运行结论仍待真实执行，不将只读适用性检查计作guards或normal实机PASS。

## 只读结果

本基线满足七批guard的数量先决条件。母星系origin5共有10个物理planet：恒星0、核心2，以及以下8个未殖民、无colonizing colony、非恒星、非人工、无eep_core/eep_guard_reserved标记的候选。已有所有eep_guard_*及eep_reg_owned_source别名均不存在。

| 物理ID | 当前类型 | size | 备注 |
| --- | --- | --- | --- |
| 1 | pc_molten | 26 | 可供既有change_pc夹具选择 |
| 3 | pc_barren | 9 | core2的卫星，物理对象仍独立 |
| 4 | pc_gas_giant | 28 | 既有batch/normal选择器没有digestible条件 |
| 5 | pc_gas_giant | 22 | 同上 |
| 6 | pc_toxic | 9 | 5的卫星 |
| 7 | pc_toxic | 8 | 5的卫星 |
| 8 | pc_barren_cold | 10 | 5的卫星 |
| 9 | pc_barren | 26 | 可供既有change_pc夹具选择 |

不能额外把物理7排除：现有`eep_jump_destination_1019=id7`的序列化type是galactic_object，指系统7，不是planet7。现有planet类型全局别名只有core2与敌源17；17位于origin81，未占用上述8个候选。其余别名是fleet151/175、country0/1等，不可把数值相同误作同一物理planet。

七个batch_setup_*使用相同选择器，选中后立即设置eep_guard_reserved并建立colony；后续选择器同时排reserved和已殖民，因而在本8候选基线能够逐个取7个不同目标，尚余1个。此处只证明当前对象与原选择器相容；实际七个random抽取ID必须从每步新SAV读取，不能按本表顺序预填，也不能把气态巨星现状误作它已经可吞噬。既有夹具先change_pc再create_colony的行为仍待实际执行。

## home外未殖民与中立源

`r6_uncolonized_bind`明确排除core母星系，同时要求真实未殖民、非人工、digestible、非reserved。基线存在充足自然宜居空球，例如physical46（pc_continental、size21、origin9）、56（pc_alpine、size25、origin3）、65（pc_continental、size13、origin38）等；它们均没有colony、owner和EEP保留标记。只读报告列出00_planet_classes支持的39个自然可殖民空球见证，不将该列表冒称对所有engine can_have_habitable_deposits谓词的穷尽执行。原生绑定后仍须按既有readiness核实际alias及谓词，当前没有“无候选”的阻碍。

基线只有war0，actor0与country1交战，故`r6_neutral_bind`会排除已绑定的敌首都17。有两个真实default非actor且未与actor交战的首都候选：

| country | capital字段（colony ID） | 首都物理planet | 类型／size | system origin | 实际人口 |
| --- | --- | --- | --- | --- | --- |
| 16777218 | 2 | 28 | pc_ocean／21 | 0 | 5357 |
| 16777219 | 3 | 37 | pc_alpine／19 | 1 | 4939 |

两国origin均不是本Mod起源；首都owner/controller等于本国，colony完整、无colonizing_species，无核心/active/devouring/credit/destroy标记，真实lithoid devastation为0，因此q分别21、19；全局ground_combat为空。这些物理ID不在home八候选中，也不能被is_colony=no的uncolonized选择器选中。九源的不同性在现有选择器下有实际对象依据，执行后仍核真实九个alias，不能以候选表当最终绑定。

## normal与迁移最小核对

本基线尚无eep_reg_owned_source，故不存在“已实际选中的normal源”。`owned_q2_setup`是未来random选择，候选恰为同一八个ID；不能只读预测具体抽中哪一个。执行路线从稳定敌星分支设置normal，敌源17在home外，不直接消耗home对象；但未来存档状态仍须重新检查，不能把Jan21候选当未来实测。按现有方案设置一次后暂停，读取新eep_reg_owned_source，确认它成为本国非核心pc_machine、size2、无损耗、恰50 founder人口，再用真实决议；无须改命令。

core2当前为owner/controller0、colony0、pc_machine、4859 founder人口（species3305111553），具备既有seed50补至100所需核心人口余量。原39文件内旧C19/G19/D6等只是历史执行上下文，不是本RC7当前输入；既有RC7路线已明确使用实际before账本，本次不改fixture或命令。

迁移应实际Load尚存源50人口的r7normalready，不能用已完成普通吞噬的stable档；先bind_physical_refs保留old_core2、新core为实际eep_reg_owned_source，再真实迁移决议。冻结RC7 eep_migrate_core代码只移除旧core的标记/deposit/modifier并绑定新core、set_capital，没有移动或删除旧core人口。因此旧物理2是现有方案的本国存活后备，不必另造后备殖民地。迁移after仍须按既有方案核旧2人口>0且普通、本国owner；新核心的物理ID/owner/flag/生产target与原生capital分别核。

core_owner_loss_bind_receiver当前可见的活default非actor为country1、16777218、16777219；normal分支在敌灭国之后，不能盲用country1，应按原random_country选择并从真实SAV读出仍活的receiver（基线支持16777218/16777219两名后备候选，未来状态待核）。转移新core后，old_core2仍需本国有pop，新core仍是生产绑定但由receiver持有；原生capital自动变化不能当EEP自动重绑。

## 结论与证据

未发现需要改选择器、fixture或命令的当前先决条件冲突。最小执行安排沿现有独立分支：guard实际Load r7pkbase恢复八候选；normal用稳定敌星后的独立分支；迁移实际Load r7normalready。无需把home外uncolonized移回home，也无需挪用真实core或新增后备球。任何未来随机绑定、引擎谓词、状态持续性与callback结果仍须原计划的实际SAV验收。

[只读原生摘要](evidence/1019-analysis/rc7-guard-selector-readonly-review-1020-v1.json) SHA `de2c39078367c25a234aacc431398697b4b4dcc53377237d11e27a0f2855a3d0`，绑定原SAV与canonical逐字节相同、完整eep aliases、home对象、两个中立首都/人口/deposits、原战争、旧core人口及输入SHA。为解释既有谓词，另只读冻结RC7 triggers/migration效果和本机00_planet_classes（SHA `24c5387795e22b3fa6ea5bc3f83b63b61d4990b77ec2ddb8e3e00483156672f5`）；未读活动fire或日志，未运行UI或写Git。只交付本文及该JSON两个文件。
