# 国内模板克隆的权利、使节与白绮肖像修复

## 目标与范围

2026-10-15，冻结候选 rc3 的实机运行 `20261015T074214Z` 发现：奖励克隆实际生效，外国共享旧模板未变，但新国内子模板没有显式物种权利；5 名常规领袖迁移，2 名使节仍引用旧模板；白绮在 `change_species` 后丢失专用肖像。奖励悬停和领取还记录 `Invalid context switch [owner_main_species] from [(invalid scope / scope not set)]`，调用链进入国内模板应用效果时 country event target 为空。

本次只改 `mod/common/scripted_effects/shishan_code_architecture_effects.txt` 的三个克隆 helper 及其共用国内迁移 helper。不修改奖励生成器、候选池、数值、外国模板或外国人口，不创建领袖。实机基线由主任务使用 `run074214Z/fb453_reroll1.sav`，领取前 n=1、重抽冷却=3、候选为 17/12/1。

## 原版依据与设计

本机原版为 Stellaris 4.5.2 (9776)。以下依据均为该版本本机原版源码：

- `common/scripted_effects/biogenesis_effects.txt:1573` 和 `events/biogenesis_events.txt:5811` 在 `modify_species` 内使用 `inherit_parent_rights = yes`，与 `change_scoped_species = no` 同级。因此新增特质、重构和复发三个克隆都显式继承父模板权利，避免国内子模板落入国家默认的清洗/低生活标准。
- `common/scripted_effects/00_scripted_effects.txt:870` 的国家内物种变更同时遍历 `every_owned_leader` 与 `every_envoy`，两者都可在 `is_exact_same_species` 筛选后 `change_species`。本次在国家 helper 内追加同样的使节遍历，只迁移该国旧模板对应使节。
- `common/scripted_effects/02_machine_age_effects.txt:286` 使用 `if` 的 `exists = event_target:...` 守卫，随后才切入对应目标。三个克隆 helper 在切入保存的奖励国家前采用同一模式；目标缺失时输出明确诊断 `SHISHAN_CODE_TEMPLATE_COUNTRY_TARGET_MISSING`。这修复无目标路径，不改变真实奖励由调用方保存国家的约定。
- 本 Mod `events/shishan_code_events.txt` 已使用原生 `change_leader_portrait = shishan_code_vivhite`。常规领袖迁移后，若仍有 `has_leader_flag = shishan_code_vivhite`，立即恢复该肖像；保留原领袖 ID、经验、等级与技能。

rc3 本次原生生成的 `C:/Users/Administrator/AppData/Local/xenoamess_stellaries_dev/runs/20261015T074214Z/logs/script_documentation/effects.log:5164` 明确说明 `every_envoy` 遍历该国可用使节且支持 country；同文档 `:1665` 的 `change_species` 支持 leader，`:1669` 的 `change_leader_portrait` 支持 leader。`inherit_parent_rights` 的依据是上述当前 4.5.2 原版源码，不将文档未列参数视为不支持。普通用户目录内 2026-09-27 的旧生成文档不作为当前版本的唯一依据。

`hidden_effect` 的文档承诺是隐藏提示文本，没有承诺跳过全部提示预评估。原生错误确认入口为 none；修复后必须同时检查 `error.log` 中无该 scope 错误、`game.log` 中真实领取没有缺失目标诊断，不能只通过消除错误日志宣称成功。

## 验收标准

开发检查：三个 `modify_species` 均含 `inherit_parent_rights = yes`；三个目标切换均有 exists 守卫与缺失诊断；使节迁移限定为当前国家、精确旧模板；白绮肖像恢复位于原领袖迁移后且有其专属 flag 守卫；不新增 scripted effect 调用层级。

主任务先执行 P 语言工具 G1，再从领取前存档实测：悬停与真正领取均无 none/owner_main_species 错误；新国内主/子模板完整继承各自旧模板权利，跨月无清洗、生活标准或岗位资格回归；5 名常规领袖和 2 名使节迁移且保持各自 ID；白绮仍用专用肖像且保留原成长数据；外国旧模板、人口与领袖不变。重构和复发共用同一修复，也须由既有覆盖验证。

本文件只记录开发与静态结果；游戏运行、存档和桌面操作由主任务统一执行。非中文运行时不在范围内。

## 实施与开发检查

已完成三个克隆节点的权利继承与国家目标守卫；共用迁移节点已补使节遍历与白绮肖像恢复。只增加原生语句块，没有新增 scripted effect helper 或额外调用层级。

以独立只读 AST 检查生产文件：3 处权利继承、3 处 exists 守卫、3 处明确诊断、人口/常规领袖/使节三个精确旧模板筛选、白绮迁移后的 flag 肖像守卫均通过；未出现全国家遍历、虚构 `every_owned_envoy`、领袖创建/删除或共享物种定义修改。源文件 SHA-256：`009b8e2728b4372665f35ecffe094da295f97c0801920554e565b39b39726c68`。

这是开发静态检查通过，尚不等同于原生权利继承、使节迁移或预评估修复验收；G1 与 rc4 简体中文实机回归由主任务继续。程序性验证代理另行补充有意义的结构与负例检查，不以无条件复制权利的测试替身证明原生行为。
