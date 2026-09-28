# 个体机械帝国实机验收补充（2026-09-28）

## 目标与范围

在 Stellaris Cygnus 4.5.1、简体中文、仅启用正式「屎山代码」Mod 的隔离用户目录中，验证非格式塔个体机械政体可以创建并进入游戏，且开局特质预算、局势、项目和研究所岗位按设计生效。Steam 保持离线。本轮只验证该政体，不以这次新局替代其他未完成的验收矩阵。

## 设计与验收标准

- 创角时选择民主制、机械主体物种与本起源；相对普通起源，可用特质点数少 6、可选特质上限多 3。
- 开局存档主体物种带 `trait_shishan_code`，国家起源为 `origin_shishan_code`；「大厦将倾」初始月进度为 `+5.0`，维护与清理项目均可见。
- 「屎山维护研究所」开局可建；建成后只新增自身的 100 维护员岗位劳动力，原有生物学家岗位仍存在；100 劳动力实际分配后，局势月进度为 `+4.9`。
- 本 Mod 的岗位定义相对于 4.5.1 原版 `biologist` 的社会学基础产出为 `2` 对 `3`，消费品维护费仍为 `1.5`；界面最终产出受各类修正和劳动人口影响，不能只据同屏两项最终数值反推基础值。
- 保存后的局势、建筑、岗位和领袖能在存档结构中识别；从游戏内重载后仍显示研究所的维护员 `100` 劳动力、原有生物学家 `60` 劳动力与局势月速 `+4.9`。

## 结果

创角界面显示机械物种可选择起源，特质预算为 `-5` 点与 8 项上限；起源效果解释为相对于机械默认预算少 6 点、多 3 项。[起源创角](../assets/shishan-code-origin/evidence/individual-machine-origin-selected.jpg)、[特质预算](../assets/shishan-code-origin/evidence/individual-machine-trait-budget.jpg)。使用测试用负面特质把预算配平后，民主制机械帝国成功进入游戏；开局有起源和简中事件链，[开局截图](../assets/shishan-code-origin/evidence/individual-machine-opening-2026-09-28.jpg)。

开局局势月进度为 `+5.0`、两项特殊项目可见，[局势截图](../assets/shishan-code-origin/evidence/individual-machine-start-situation.jpg)。研究所在建筑列表中开局可建，提示新增 `+100` 维护员岗位，并说明仅替换该建筑自身的岗位，[建筑截图](../assets/shishan-code-origin/evidence/individual-machine-building-unlocked.jpg)。正常消耗资源并等待建造后，建筑出现在首都槽位，岗位页同时存在原版生物学家 `60` 劳动力和维护员 `100` 劳动力；后者的界面产出/维护费见[岗位截图](../assets/shishan-code-origin/evidence/individual-machine-maintainer-job.jpg)，原版生物学家另见[对照截图](../assets/shishan-code-origin/evidence/individual-machine-biologist-job.jpg)。此时局势显示 `+4.9`，符合每满 100 已分配劳动力减速 `0.1`。

[可重载存档](../assets/shishan-code-origin/evidence/individual-machine-2203.05.22.sav)由游戏 UI 于 `2203.05.22` 保存，SHA-256 `3bff62df806073a10e53364cd0150dee8f9af61815675050e34038ffd4ba88e8`。解包 `gamestate` 可见民主制国家的 `origin="origin_shishan_code"`、主体物种 `trait_shishan_code`、建筑 `building_shishan_code_institute`、已分配的 `shishan_code_maintainer` 岗位 `workforce=100`/`max_workforce=100`，以及 `situation_shishan_code` 的月进度 `4.9`。在正常事件链中获得的白绮亦在该存档中，等级 5，带本 Mod 的白绮特质。

从游戏内选择该存档的「读取最新存档」后，首都经济页仍显示生物学家 `60` 与维护员 `100`，局势侧栏仍为 `+4.9`；[重载截图](../assets/shishan-code-origin/evidence/individual-machine-maintainer-reloaded.jpg)。因此个体机械的建筑、岗位分配和局势速度持久化通过。

在重载后的局内启动「维护屎山」，让游戏自然跨过一次月结算后取消。启动中[截图](../assets/shishan-code-origin/evidence/project-cancel-maintain-started.jpg)与取消后[截图](../assets/shishan-code-origin/evidence/project-cancel-maintain-cancelled.jpg)分别显示“研究中”与重新“可用”；取消后项目仍为 `2000` 社会学。取消后于 `2203.06.03` 保存[存档](../assets/shishan-code-origin/evidence/project-cancel-maintain-2203.06.03.sav)，SHA-256 `3729d2afb9b7f1ca4e6c9592ddc0e4af86a194f0432b4a212ad681382ffd3a41`。与前一份 `2203.05.22` 存档相比，`shishan_code_maintenance_count` 都为 `0`；局势进度由 `199` 到 `203.9`，正好跨月增加 `4.9`，没有被取消操作归零。该存档不含运行中的维护项目。

同一暂停日随后启动「清理屎山」并取消；[启动截图](../assets/shishan-code-origin/evidence/project-cancel-cleanup-started.jpg)显示“研究中”，[取消截图](../assets/shishan-code-origin/evidence/project-cancel-cleanup-cancelled.jpg)显示再次“可用”，费用仍为 `8000` 社会学，局势侧栏仍为 `+4.9`。这一项仅通过 UI 验证取消后的即时状态，未另存第二份取消后的存档。

本轮控制台曾在中文输入法状态下把带空格的 `resource minerals 500` 误输入为连写字符串；无证据表明该命令执行成功。建筑使用正常收入和正常建造完成。关闭调试界面需要 `Shift` 加物理 `0x29` 键；调试窗口未影响存档可读性。原版生物学家与维护员岗位的同屏最终产出分别为 `2.74` 与 `3.04`，不能当作基础产出差值的验收证据，原因需通过原版岗位和 Mod 岗位定义中的 `3` 对 `2` 确认。

## 第二座同星球研究所的补测方案

从已归档的个体机械帝国首都一座研究所基线打开空建筑槽位，检查建筑列表仍允许「屎山维护研究所」，使用正常 GUI 和 `400` 矿物将第二座加入建造队列。为缩短等待，可以在这个**隔离验收存档**临时使用原版控制台 `instant_build`，但只作为完成已经由 GUI 正常准入的建造队列的加速器，完成后立即关闭；最终必须由 UI 和存档确认同一星球**两座已完成建筑**及 `200` 维护员劳动力，不能把队列中的第二座算成建成。保存并重载后再确认不会被上限规则清除。测试副作用只留在隔离存档，不进入正式 Mod。

## 第二座同星球研究所的结果

`2203.07.08` 的个体机械首都已有一座研究所，空槽位再次列出「屎山维护研究所」，以正常建造菜单花 `400` 矿物排入队列。控制台回显 `Instant build mode is ON`，推进数日后第二座建成；随后再次执行命令，回显 `Instant build mode is OFF`。[建成截图](../assets/shishan-code-origin/evidence/individual-machine-second-institute-built.jpg)可见同星球两个研究所图标及局势月速 `+4.8`，[岗位截图](../assets/shishan-code-origin/evidence/individual-machine-two-institutes-200-jobs.jpg)显示维护员 `200` 劳动力，原版生物学家 `60` 仍在。项目完成和特质奖励不参与这一支。

关闭加速模式后保存[ `2203.07.11` 存档](../assets/shishan-code-origin/evidence/individual-machine-two-institutes-2203.07.11.sav)，SHA-256 为 `4f0b7b39ff814383b8cda42467c6eccf61ce9ef77e0461031672ead185067df1`。`gamestate` 有两个独立 `type="building_shishan_code_institute"` 建筑条目，维护员岗位记录为 `workforce=200`、`max_workforce=200`。从游戏菜单重新载入后，[建筑截图](../assets/shishan-code-origin/evidence/individual-machine-two-institutes-reloaded.jpg)与[岗位截图](../assets/shishan-code-origin/evidence/individual-machine-two-institutes-200-jobs-reloaded.jpg)仍见两座研究所、已分配 `200` 劳动力及局势 `+4.8/月`。因此本起源在同一普通首都可建至少两座，建成、岗位和局势速度均经重载保持；理论“无限座”仍受原版建筑槽位约束，脚本中没有自定义单星球上限。

## 后续

武器及航速面板、领袖零经验复活和资源基础/空间站来源隔离已有独立证据文档；实际战斗伤害、同段航行时间、其余资源来源、稀有资源和长程平衡样本仍待完成。只有这些硬门槛及 `open_kaishek` 最终检查完成后，才可宣告整体验收完成。
