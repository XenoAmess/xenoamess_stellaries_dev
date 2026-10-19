# 1019 旧母舰迁移：损伤、空队列与付费队列独立审阅

## 目标、范围与验收（实施前）

审阅现有 `eep_sync_mothership` 的 `set_ship_design` 迁移，提前发现损伤、移动船坞队列与重复奖励风险。只读本机 Stellaris 4.5.2 原版和原始存档；不操作桌面，不改 Mod、SAV、运行目录或外部 `open_kaishek`。本文不宣告旧档兼容实机通过。

主线程另授权修复独立 `tools/check_1019.py` 的 **migration 函数及对应测试**：原公共版空队列与历史真实付费队列必须使用不同前提。其它检查函数、历史报告和归档工具保持原字节；主仓库由主线程统一提交，本子任务不提交。

修复设计：案例可指定 `queue_mode = "empty"` 或 `"paid"`，省略仍为原有 `paid` 行为。`empty` 必须显式声明 `expected_queued_items = 0`，原始夹具、损伤前提存档和迁移后存档的母舰造船队列都为空。`paid` 必须声明正整数数量，原始队列身份和数量绑定不变，迁移前有真实记录的费用、付款国家与正进度。两种模式均保持全体队列、完整队列项、母舰／舰队／星基地身份、布局、库存和经济账本不变，不能把空队列变成“付费队列已验证”。

验收包括：默认付费正例；显式付费正例；显式空队列正例；空／付费案例与实际队列错配负例；空队列迁移后新增项负例；付费进度、费用、付款者、项身份变化负例；库存或奖励账本变化负例；非法模式和数量拒绝；重载仍保留所声明队列合同。测试使用明确标注的合成观察值验证检查器行为，不当作游戏实机证据。另验证除 migration 函数外源码字节不变，归档工具与历史证据不改。

修改前工作文件 `tools/check_1019.py` SHA256：`ba17847049d050b2b76dc382e7e3e0a1796dc4976a80c77b16fef243bc612047`。`acceptance_analysis` 已确认不并发修改 checker，并冻结自己的只读工具副本；先前 Machine／hardware 报告仍引用各自归档旧版本。

## 静态事实与风险

`mod/common/scripted_effects/eep_mothership_effects.txt:66` 的国家同步先计算成长与组件镜像，再约束绑定母舰属于当前国家、仅一船且为 juggernaut。对绑定舰队中的现存船，缺少 `eep_mothership_design_1019` 时在 127 行调用 `set_ship_design = { design = NAME_EEP_Baiqi_Mothership_1019 }`，128 行设置一次性船旗。该路径没有 `create_ship`、`create_fleet`、修复三防或清空／重建队列的显式命令。因此脚本层没有明显“主动治疗／主动重新付款排队”代码，但是否保持三防和移动船坞数据取决于原生 API，不能由未出现这些命令推导为已安全。

本机生成 `runs/20261019T092935Z/logs/script_documentation/effects.log:2575` 对 `set_ship_design` 只承诺改变 ship 或 fleet 中船所使用的设计，参数为 `design` 或 `random_existing_design`。没有记录 `preserve_health`、`repair=no` 或队列保留选项，也没有说明最大值改变时 current／缺失绝对值／百分比哪一个保留。不能追加未经证实的参数。

原版 `events/biogenesis_crisis_events.txt:2317,2358` 在 `biocrisis.215` 中对 `owner.random_owned_ship` 选出的 `behemoth_04` 换为 jump 或 cloaking 设计；这两处没有配套伤害恢复代码，也不是有付费移动船坞队列的示例。因此它证明调用语法，不能证明本 Mod 的损伤或队列政策。

一次性船旗紧跟设计切换且没有结果后置核验：若原生切换未成功，脚本仍可能标记完成。这里是静态可见的失败恢复风险，尚无本次实际失败证据。实测应同时核验实际设计体／槽位变化与旗标，不能只看到旗标便判迁移完成。保留旧 `eep_mothership_section`、新增 `_1019` 舰段的加载兼容措施已经存在，本审阅不重复要求改回槽位。

已确认的检查器缺口则可不等实机暴露：当前 migration 不分场景，无条件要求 `bool(mother_items)` 与至少一项 `progress > 0`。公共 0.3.1 原始空队列即便完全保留也必定 FAIL。仅把预期数量改为 0 不能消除这一矛盾；需要明确适用性模式，而不能关闭付费前提或把不适用条件硬记为 True。

## 两个原始夹具与不同承诺

| 案例 | 原始 SAV | 原始 SHA256 | 队列政策 |
| --- | --- | --- | --- |
| released 0.3.1 | `docs/evidence/1019-baseline/bmm00.sav` | `af5f64e2eaadb164e87796d2a9261ac97ef7d716cc3f8b3cec5f4a2f23f787f8` | `queue_mode=empty`，预期 0 项；原始、施伤前提、迁移后均保持空，不重新发开局奖励或扣费 |
| legacy-paid 0.3.0-rc.1 | `docs/evidence/1015-2026-10-15/v13-shipyard-runtime/j13ten.sav` | `834ea5325f93e3d3e92a44aabccd87195564cd4f1292d4439ae865eba5af8d2e` | `queue_mode=paid`，预期 **11** 项；不是 released 0.3.1 的替代证据 |

`j13ten` 名称中的 ten 是同时开工数，不是总排队项数。其舰队 146、船 822、星基地 13、造船队列 54：项 0–9 均为 10/60，项 10 为 0/60，每项记录 81 合金、付款国家 0、设计 1702、orbitable 星基地 13，记录费用总计 891 合金。原始施伤前须确认这些身份／进度仍真实存在；记录费用和迁移前后库存相同只能证明迁移没有再次收费／退款，最初排队的支付还须追溯原动作与审计。

本次另从原始 `bmm00.sav` 的 gamestate 只读提取，确认公共版舰队 128、船 1008、星基地 15、造船队列 50，其原生 items 确实为空，`simultaneous=10`。公共版案例应分别声明上述身份、`queue_mode="empty"` 与 `expected_queued_items=0`，不能借用 j13ten 的身份字段。

上述旧夹具原始字节始终只读。导入到隔离 userdir 的原字节副本不等于迁移成功，原始健康母舰也不能当作损伤保留证据。

## 最小真实损伤探针与预期政策

接口与原版 armor 调用依据沿用 [已有专项调查](armor-damage-migration-probe-1019.md)，不再次猜测负数 repair。两种队列场景各从自己的原始夹具副本独立执行：

1. 简中原生载入并暂停，先保存加载后干净基线。核验唯一绑定母舰、真实旧设计、三防 current/max、母舰船坞队列及库存。公共版仍为空；legacy-paid 保持 11 项、原身份与真实进度。
2. 对实际绑定母舰的 ship scope 单独执行已文档化、原版有 armor 意图的 `damage_ship = 120`，同日另存 damage-only。只有实际 armor 下降、船仍存活且队列／资源没变化，才承认 armor 前提；效果无变化或只伤 hull 时照实记为该层未覆盖。
3. 按需再分别 `reduce_hp = 120`、`reduce_shield = 120`，每一步保持暂停并核验非致死前提，再保存独立 pre-migration。它们是原生施伤接口，不编辑 SAV；不将施伤与设计同步合并成不可归因的一条命令。已有三层真实受伤才可宣告三层覆盖。
4. 事先声明损伤比较政策。现有需求要求保留损伤，[强化设计计划](mothership-strengthening-plan-2026-10-19.md)进一步要求生命百分比，故最终按该计划使用 `damage_mode=fraction`；所有 current/max、缺失绝对值和比例同时报告。历史通用模板允许其它政策，不应在看过结果后改用较容易通过的模式。新最大值下保持 current 绝对值或缺失绝对值的结果也不能被误写成百分比已保持。
5. 只调用既有迁移同步，立即同日保存 after，核验实际新设计／槽位、身份与坐标、三防、所有队列项、库存、经济账本和启动旗标；同日原生 reload 另存验证。重复同步也必须幂等，不能再次收费、发奖励或复制船。迁移自动满血、队列项消失／重建、付费进度改变均须保留 FAIL。

探针依赖主线程独占桌面的原生操作。本审阅不执行上述步骤，不将合成检查器测试或静态 API 推断写成实机 PASS。

## 实施与验证记录

已仅在 `tools/check_1019.py` 的 migration 函数实现上述模式；新增 `testing/test_check_1019_migration.py`，未改其它函数。`empty` 报告含 `original_mother_shipyard_queue_empty`／`before_mother_shipyard_queue_empty`／`after_mother_shipyard_queue_empty`，不输出不适用的 paid 检查；报告顶层显式记录 `queue_mode`。默认付费案例保留原检查名称、值与范围。

定向命令 `python -m unittest discover -s eat_everything_origin/testing -p test_check_1019_migration.py -v`：**17 测试通过**。除两个模式正例与错配负例，还覆盖付费项重编号、费用／进度／付款者／设计／orbitable 改变、母舰空队列时其它本国队列被改、收费／退款／奖励重复、护甲自动满血以及同日重载队列变化。首轮一处测试夹具把 tuple 当可变 list 使用，已改为局部 list；最终全部通过，该修正不涉及产品代码。

新工作文件 SHA256：`df147d247240c75bc0507cb1dda0bf88af299706841d3b72c140b083e96be777`。与已归档旧 `ba178470…` 工具逐字节比较，去掉 migration 函数后前后两部分完全相同。用同一合成空队列输入运行旧工具，仍因原 paid 两项前提得到 FAIL；新工具明确空队列模式得到 PASS_SCOPED。相同默认付费输入在新旧工具均 PASS_SCOPED，完整 checks 字典相同。它们都是检查器测试结果，**不是实际 Mod 迁移通过**。

验证报告与完整测试输出见 [verification.json](evidence/1019-analysis/migration-queue-mode-v1/verification.json) 与 [unit-tests.txt](evidence/1019-analysis/migration-queue-mode-v1/unit-tests.txt)。历史报告／归档工具没有重写；外部 open_kaishek、生产 Mod、桌面与当前 run 没有改动。本子任务未提交，交主线程统一处理。原版 `set_ship_design` 的实际损伤、队列及重复同步／重载行为仍待主线程探针确认。
