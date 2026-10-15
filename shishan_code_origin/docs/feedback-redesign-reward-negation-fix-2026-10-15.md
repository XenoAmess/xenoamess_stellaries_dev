# 奖励权重的复合否定修复

日期：2026-10-15。实施前记录。修复对象是本轮真实运行发现的三选一跨层与重复候选，不把离线模拟的旧 PASS 当作引擎证据。

## 原生证据与根因

主任务在冻结 rc.2 运行中原生保存 `fb452_pending1.sav`，观察到 `n=1`、奖励层 `tier=1`，三个槽却为 `[5,33,33]`。界面只出现逻辑引擎和强壮两项，证实有跨层与重复。原始存档、截图和日志由主任务统一归档。

本机 4.5.2 原版 `common/scripted_effects/biogenesis_effects.txt` 的 `generate_evolutionary_predator_choices`（约 360–374 行）直接使用 `random_list` 条目的 `modifier={factor=0 条件}`，故权重容器本身不是错误。生成器原先把 `eligible`、层检查、三个槽排除及重抽的旧槽排除同时塞入 `NOT={...}`，意图表达“并非全部条件满足”。

主任务在新鲜 GPU 帧中实际运行两个无副作用的控制台 trigger 探针，run `071829Z`：

```text
trigger NOT = { always = yes always = no }
→ FALSE

trigger NOT = { AND = { always = yes always = no } }
→ TRUE
```

证据名为 `native-not-multiple-result.jpg`、`native-not-and-result.jpg` 及对应 `console.json`。这组真假混合输入能区分两种语义：本机 Stellaris 的多子 `NOT` 不等同于 `not(all(children))`；当前结果符合逐项否定的 NOR 行为。第二个表达式明确只有一个 `AND` 子条件，能够得到所需的复合取反。

旧离线解释器把 `NOT` 当作 `not(all(children))`，恰好替生产错误补出了原本想要的逻辑，因此奖励模型得到假阳性。解释器修复及工具门禁由另一任务负责，本任务不改它们。

## 最小实现与范围

只修改 `tools/shishan_code/generate_rewards.py` 的 `random_draw`，从：

```text
modifier = { factor = 0 NOT = { <available 的多个条件> } }
```

改为：

```text
modifier = { factor = 0 NOT = { AND = { <available 的多个条件> } } }
```

每个权重守卫只有一个 `AND` 子条件；其它条件、层顺序、权重、候选槽、冷却、旧组选项、生产发奖与 balance 已完成的 `hidden_effect` 均保持。

重新生成 `common/scripted_effects/shishan_code_rewards.txt`。在内存中同时生成 triggers 和 events 并确认它们与现有文件完全一致，只写发生改变的效果产物；不运行会重写本地化等其它文件的生成器 `main()`。不修改 VERSION、CHANGELOG、事件、本地化、现有 runtime 文档或游戏加载副本。

## 静态验收与实机回归线

- 当前六个 draw 路径（3 槽 × fresh/fallback）各含 39 条，总计 234 个权重否定守卫；修复后每个都应是 `NOT → 唯一 AND → 原 5 或 8 条条件`。
- 生成效果文件中不再存在多子 `NOT`；生成的 triggers/events 内容与修复前相同。架构及候选 scripted triggers 原本没有多子 `NOT`，不扩大修改。
- 生成器重新生成的三产物与磁盘对应文件一致；程序解析、文本编码和 whitespace 检查通过。原离线奖励检查必须等解释器语义修正后重跑，不能继续引用旧模型的 PASS。
- 主任务重启新冻结候选后，从原共同基线重新完成一次项目，原生保存三个同层、不重复且合法的候选；再验证延期重开不洗牌、重抽至少替换可替换项并优先取旧组外、CD 按 3→2→1→0、确认只给一次。既有错误票据 `[5,33,33]` 不作为新抽签成功证据。
- G1 与新实机回归均由主任务统一登记。本任务只开发和静态检查，不启动或操作游戏。

## 方言边界

上述实测只确证本机 Stellaris 4.5.2。CK3 使用 Clausewitz/Jomini 脚本，但不能仅凭同属 Paradox 推定其多子 `NOT` 语义相同；是否存在本机 CK3 的明确 primary 文档依据将单独记录。没有这样的证据时，不把 Stellaris 实测写成 CK3 已运行或共同引擎语义结论。

本次另作 CK3 本机 primary 只读调查：实际项目位于 `C:\workspace\ck3_eternal_recurrence`；游戏本体的 `game/common/council_tasks/00_steward_tasks.txt`（约 931 行）等确有原生 `NAND` 使用，Jomini 的 `trigger_system_l_english.yml` 仅含触发器提示行的显示文本。检查的原版文件及现有本机文档没有给出上述多子 `NOT` 真值表；也没有启动 CK3 或取得 CK3 原生同探针回显。`NAND` 名称存在不能单独证明多子 `NOT` 的具体含义。因此本轮只确认 Stellaris，暂不登记为 Paradox 共性，不改写或提交 CK3 知识库以免写入未经证实的方言结论。

## 实施结果

已只修改生成器 `random_draw` 的一处格式字符串，并重新生成一个效果产物。原效果文件 SHA-256 为 `93589b9d972b937859a7296859587a15381b9a57514424c50db51194d5834607`，新值为 `3fb79150a831d3314198e259265d11f1fd33f7e621d0db1278d19ae5187c07e2`。其它两个生成产物与内存输出字节一致，没有写入；未运行生成器 `main()`，未写其它脚本或本地化。

2026-10-15 静态结构检查通过：六个 draw 分支各 39 条，共 234 个权重守卫，fresh 与 fallback 各 117 个；每个守卫都是 `NOT` 的唯一 `AND` 子项，保留原 5/8 条资格、层及槽排除条件；候选 ID 与目标槽映射一致。当前奖励效果文件中的多子 `NOT` 数为 0。生成器 Python AST、P 语言受限 AST 解析、UTF-8/无 BOM/无替代字符和 whitespace 检查通过。

离线解释器及完整奖励合同由主任务所分配的独立工作负责；上述检查不冒充其结果或原生引擎验收。原 rc.2 已保存的错误票据不会仅因修复后续 draw 而自动成为合法票据，实机复验必须从抽签前的基线重新触发；当前 refresh 没有额外加入跨层/重复历史票据迁移策略。新候选的游戏运行结果仍为 **NOT RUN**。
