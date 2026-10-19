# RC7 成长余项恢复执行记录

沿既定最短执行卡，run20261019T204055Z、PID24520，简体中文单生产Mod，
完整59文件RC7树保持。仅补普通舰十getter、实际受伤自然恢复、母舰死亡后
完整初始化／月脉冲／已毁档重载不复活，不重做九节点矩阵或实际跃迁。

## 已完成的普通舰控制与归档设计

实际加载r7ganchor和r7evreport，分别在原日期2201.01.01、2202.08.07输入原
ordinary-ten-modifiers；高档另输入原mother-fourteen-modifiers。两份新原生
SAV r9growthlow/high已保存，原growth检查分别C0／C20500通过。
11普通舰0～5、804～808均实际属于同国，fleet相同，原生design body SHA及
装备shape完全相同；110个getter成对一致，未将缺项补0。

高Mother新十getter与三项native max按原prediction及原0.01／HP8ULP工程政策
全部通过。预期在新high SAV形成前记录，来源为已封C0-final和原C20500输入；
四个新regen percent/mult均实际导出为0。旧eep_probe_max_*未由本次14getter
刷新，只作为历史诊断保留，不当作当前原生最大耐久。

现建立独立1020-rc7-ordinary-control-resumed-v1，只归档已完成r9growth-low/high
输入、r9growthlow/high三件套及观察、精确导入回执、事前来源预测与已完成
两份控制报告。排除正在写入的damage/hurt/day/death阶段及活动日志。核原件
双SHA、两档ZIP/audit/receipt、截图OCR与全部getter和原生max投影后，仅合入
random_components.other_fleets_unchanged，整组与component_rewards仍PENDING。

## 恢复与死亡的后续边界

高档确认H/A>200000、S<10000000、核心可用、无订单、combat起始为0.01.01后，
已按原115字正伤害命令执行；先保存暂停日hurt、核真实H/A下降，再仅FF1采day。
恢复须有实际增加、相同Mother身份／max、无修复输入及原账本／六层数不变。
完成后才执行原destroy/dead_sync、下一真实月脉冲和已毁档重载，死亡after不调
要求活Mother的growth reader；全表与国家所属列表共同排查替代Mother。

本记录不预填尚未产生的恢复／死亡结果，全部失败及严格差异保留，完整日志
只有当前进程正常停机后才能冻结和最终验收。

正伤害后r9growthhurt已真实保存于Aug7。首个只读分析直接索引shield_hitpoints
出现KeyError，该native字段实际被省略；代码在FF之前停止，未产生v1损伤报告。
按原卡“省略保留缺失、不伪造显式0”改用present/value记录护盾，不重复伤害，
也不认证数值护盾差。继续用实际存在的H/A及max、身份、账本证明损伤和一天
自然恢复，另存v2报告；原SAV/观察及失败事实保持。此为分析脚本读取缺陷，
不改生产、冻结原checker、原数值政策或受伤恢复验收范围。

普通舰包已核167原件／8,157,515字节、两档ZIP/audit/receipt及36对GPU/OCR。
仅将other_fleets_unchanged合入，当前109 true／29 null；全部整组及组件仍PENDING。

伤害与恢复v2已实际通过：Aug7舰体3396960→3296960、装甲2873613.6→2773613.6，
原生max、Mother125/ship809、EEP账本及六层数不变，护盾字段缺失原样记录。
仅FF1至Aug8，实际舰体+18094.76、装甲+29849.576，同身份／max／账本，无修复
订单及回血输入，原growth通过。原strict差异留证，不拟合闭源恢复公式。
现执行原destroy/dead_sync及下一月、已毁档重载；待死亡链完成后独立封存。

死亡链已实际完成：Aug8真实destroy后执行原完整initialize/startup/sync，FF24至
Sep2（跨Sep1月脉冲及一日窗口），再真实title load该已毁Sep2档，重复同一完整
初始化并FF1保存Sep3。两档均无命名Mother舰队、无本国或original_owner0的
全局Mother式实际舰船，旧125/809不在所属表，绑定未指向新活舰；国家／core
存活且grant flags齐备，C20500/L2050/R410/P0与六层数保留，snapshot_state=1。
不使用要求活Mother的growth reader给死亡after造接口失败。

现建立1020-rc7-restoration-death-resumed-v1，仅封已完成damage/hurt/day、destroy、
deadmonth/deadload及相关操作和报告，before高档引用ordinary-control包，不重复
复制。排除当前pending分支和活动日志全文。核4份SAV的ZIP/audit/receipt、
图OCR/原字节稳定性后，仅合入daily_regeneration和destroyed_mother_not_respawned，
原strict、护盾字段读取KeyError和v2边界保留，整组仍待最终日志。
