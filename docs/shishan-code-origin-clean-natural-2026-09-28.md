# 第五阶段自然研究清理验收（2026-09-28）

## 目标与范围

按[验收计划](shishan-code-origin-acceptance-plan.md)补足第五阶段「清理屎山」经普通社会学项目研究而完成的路径，核对成功回调只结算一次、局势真正结束、主体物种特质切换、后续「持续优化」项目费用与存档重载。此测试在简体中文、离线、单 Mod 的隔离用户目录执行。正式仓库 Mod 不添加测试修正。

## 方法与验收标准

从已归档的第五阶段存档加载，先通过 GUI 启动「清理屎山」并保存研究中基线。读取存档确认其 `society_queue` 进度与项目成本。为了避免在低研究产出下模拟几十年，可在**隔离用户目录的 Mod 副本**额外加入一次性静态修正，只提高国家社会学研究产出，不改项目成本、`on_success`、物种特质或局势；重启游戏后向玩家临时施加修正，使项目经过正常月结算完成。必须记录所用键值及存档；如修正不生效，改用自然时间或重新设计夹具，不用直接调用成功效果冒充普通研究。

完成后检查：项目实际从队列消失，玩家国家 `last_completed_special_project=SHISHAN_CODE_CLEAN`；「大厦将倾」局势从国家事件集合消失；主体物种仅有一个「重构完成」且不再有「屎山代码」；`n` 不因清理增长；「持续优化」可研究且成本按当时 `n` 为 `2×(2000+1000n)`；白绮对白/事件图正常；重新加载保持上述状态。若使用临时修正，结束后须退出游戏、删除该测试文件并恢复正式 Mod 副本再重载，确保结论不依赖临时文件。验收报告须明确区分临时加速的研究速度与正式 Mod 的长期可玩性。

## 执行与证据

- 基线 `assets/shishan-code-origin/evidence/clean-natural-preboost-2228.02.04.sav`，SHA-256 `AE3201C610925352FC4CAAFF372962176672642DF60530DDC2D031600AEA0F9D`。在第五阶段通过 GUI 启动成本 `8000` 的项目；存档 `society_queue` 已有 `5.90954` 进度，`SHISHAN_CODE_CLEAN` 仍在研究，局势 `1000/1000`，`n=0`。
- 最初在隔离 Mod 副本写入的静态修正文件有 UTF-8 BOM；4.5.1 把 BOM 算作修正键一部分，日志出现 `Failed to deferred read key reference`，科研并未加速。退出游戏后将同一文件改为**无 BOM UTF-8**，重启再加载基线。文件内容为 `shishan_test_society_boost = { country_society_research_produces_mult = 1000 }`；控制台回显确认 `+100000%` 社会学月研究，仅影响测试速度。
- 正常推进至 `2228.03.02` 时项目完成并弹出「清理屎山」事件，显示白绮的结尾对白与正确事件图。未执行 `complete_special_project` 或直接调用成功回调。局势从侧栏消失，情报日志仅留下「持续优化」，其 GUI 成本为 `4000`，符合 `n=0` 时 `2×(2000+1000n)`。
- 关闭事件后游戏继续运行至 `2229.06.22` 才暂停；随后以 `effect remove_modifier=shishan_test_society_boost` 撤销临时修正并保存。存档 `assets/shishan-code-origin/evidence/clean-natural-post-2229.06.22.sav`，SHA-256 `D9CB8027A1177E7BBF2E6FD9B91FAF3324C67BF5B86DDE91D49061153C5EDBCF`。其中 `last_completed_special_project="SHISHAN_CODE_CLEAN"`，`SHISHAN_CODE_CLEAN` 已不在待研究项目中，`SHISHAN_CODE_OPTIMIZE` 已出现；`situation_shishan_code` 从 1 条变为 0 条，主体物种从 1 个 `trait_shishan_code` 变为 1 个 `trait_shishan_refactored`，`shishan_code_maintenance_count` 仍为 `0`，临时修正键出现次数为 `0`。
- 退出游戏后删除隔离 Mod 副本的测试修正文件；重新启动时校验和恢复为正式单 Mod 的 `cb18`，日志不再报告该键。重新加载 `clean-natural-post-2229.06.22.sav` 后局势仍未出现，情报日志仍只有成本 `4000` 的「持续优化」，与存档中已重构状态一致。图像证据为 `clean-natural-event-2228.03.02.jpg`、`clean-natural-optimize-cost-2229.06.22.jpg` 与 `clean-natural-reload-optimize-cost-2229.06.22.jpg`，均位于 `assets/shishan-code-origin/evidence`。
