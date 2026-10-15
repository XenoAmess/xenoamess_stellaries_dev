# 原生物种缓存延迟与待选清理交叉修复

## 目标与证据

rc.4 在 4.5.2 同日清理后，原生 fb454_clean_pending 中实际国内人口已迁移到55/56，founder=56，待领槽11/9/12和R0保留；country.owned_species_refs仍53/54。立刻重新打开时以any_owned_species驱动的资格枚举遗漏新模板，误判耗尽，将R增至1并留下空选项窗口。该路径FAIL，不能以跨日正常掩盖。

## 实施范围和设计

候选资格、领取克隆与清理/复发的国家模板枚举改由真实正人口every/any_owned_pop_group驱动，再进入species作用域检查原版archetype、trait互斥及执行现有clone helper；国家谱系条件保留。使用已验证的domestic exact-template apply一次迁移所有同模板组；后续group读取已更新species，已有新增trait或已替换state trait的模板不再重复克隆。不依赖缓存owned_species_refs，也不修改缓存字段。保留外国共享模板、main pointer、7领袖与头像、权利继承、原版资格和已有奖励凭证。

pending存在且池真正耗尽时，关闭旧窗口锁并提供正确结果，不留只有reroll/later的假待选窗口；需以现有状态机和原生证据决定是否需要额外修改，不能在没有凭证时加R。

新增候选0.2.0-rc.5，先跑open_kaishek，再重启实机；rc.4原始失败存档/截图/日志只读归档。程序模型补充滞后ownedrefs且实际人口新模板、同模板多group、同日clean/reopen与claim后重复进入负例。

## 验收标准

清理前后U不变、n4/R0/CD3及三个槽保留；清理后原地重开仍三项合法，同票reroll受限；实体领取一次后CD2/R0；实际国内克隆与全部领袖/权利正常，外国哨兵不变。原生save/重载保持；维护、优化、复发立即交叉同样能找到实际模板。静态资格149场景及现有完整回归继续通过；程序PASS不能代替原生同日复验。

原生缓存探针已确认前FALSE后TRUE（rc.4两张GPU图）。空窗口的真正耗尽边界也需修复：open helper发隐藏country_event .1004，先refresh；仅仍pending时再发可见.1000。锁按既有清理语义处理，不把refresh直接加进open helper扩大scripted初始化链；可见事件在槽已验证后才出现。普通科研及J0/J100数值路线见[自然维护路线](feedback-redesign-natural-maintenance-route-2026-10-15.md)。
