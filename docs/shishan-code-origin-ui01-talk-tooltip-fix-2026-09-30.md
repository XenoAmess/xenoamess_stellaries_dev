# UI-01 白绮交谈决议提示修复（2026-09-30）

## 目标与范围

正式 `0.1.0` 单 Mod 简体中文实机中，白绮死亡待复活时，首都决议「与白绮交谈」被正确禁止，但鼠标悬停的失败条件直接露出内部领袖旗标 `shishan_code_vivhite`。这违反 UI-01 的原始 key 不泄漏标准。复现锚点为 `vivhite-zero-xp-pending.sav`，日期 `2203.06.03`；复活后的同日锚点用于正向对照。用户要求的 Steam 发布已完成，本修复属于发布后的补丁，不改写已发布的 `0.1.0`。

## 设计

沿用原决议的受雇白绮逻辑，不改变可执行条件。把 `allow` 内的检查包装成 Stellaris 4.5.1 原版决议已经使用的 `custom_tooltip = { fail_text = <本地化键> ... }`，使失败提示直接说明「白绮尚未复活，无法与她交谈」，而不展示脚本旗标。新增本地化键覆盖全部十种官方语言；按仓库既定 MiniMax 工作流翻译非简体中文文案，再人工审校和静态校验。兼容范围仍由 `supported_version` 表示。

## 验收标准

1. `open_kaishek` 检查正式包通过。简体中文待复活存档中，决议不可执行，提示显示通顺的中文且无 `shishan_code_vivhite` 或其他内部 key；点击不可触发交谈事件。
2. 同日已复活存档中，决议可执行，仍正常出现白绮交谈弹窗；死亡/复活状态与费用不变。
3. 十种语言均有新键，九种非简体中文语言仅做静态校验，明确报告“静态校验通过，运行时不在范围内”；旧键完整性、文件头、编码、引用和无占位泄漏继续通过。
4. 为已公开发布的 Mod 使用新补丁版本、发布前 changelog、创意工坊远端核验和同名 Git 标签；不更新只读上游物品 `3710613857`。

## 执行记录

旧版失败画面归档为 `assets/shishan-code-origin/evidence/ui01-talk-pending-raw-flag-2203.06.03.jpg`。隔离简中单 Mod 校验和 `0305` 下，载入 `2203.06.03` 待复活原生存档后，决议仍不可用，悬停显示「白绮尚未归来，无法与她交谈。」且不泄漏内部旗标；点击该决议不触发弹窗，见 `ui01-talk-pending-fixed-2203.06.03.jpg` 与 `ui01-talk-pending-disabled-click-2203.06.03.jpg`。同日复活存档中决议可用且正常弹出「与白绮交谈」对话，见 `ui01-talk-revived-enabled-2203.06.03.jpg` 与 `ui01-talk-revived-dialogue-2203.06.03.jpg`。游戏 `error.log` 未检出本 Mod 相关错误。

翻译沿用用户指定 MiniMax 工作流，两轮翻译原文、输出及提示上下文归档于 `assets/shishan-code-origin/evidence/ui01-talk-tooltip-minimax-2026-09-30.json`。简中及其余九种官方语言均新增同一键；非中文翻译静态校验通过，运行时不在范围内。正式包 `open_kaishek PASS`（19/19 脚本、13 DDS、173 本地化键），v0.1.1 已发布并完成远端校验，见[页面改版与发布记录](shishan-code-origin-workshop-page-v0.1.1-plan-2026-09-30.md)。
