# Changelog

## [0.1.1] - 2026-09-30

### Added

- 创意工坊说明扩充为包含阶段、月速、费用、奖励、复发和白绮规则的详细 BBCode 页面；穿插 8 张已归档的简体中文真机截图，并加入创意工坊截图画廊。BBCode 和截图清单均入库。

### Changed

- 将白绮尚未复活时「与白绮交谈」决议的失败条件改为明确的本地化提示。决议原有可用性和触发效果不变。

### Fixed

- 修复白绮待复活时决议提示泄漏内部旗标 `shishan_code_vivhite` 的 UI 问题。
- 修正公开页面中把已完成的高劳动力月速边界测试误列为待验的描述。

### Compatibility

- 兼容 Stellaris `4.5.*`。更新本项目已拥有的创意工坊物品 `3810136486`；只读上游 `3710613857` 不作为上传目标。

### Validation

- 简体中文单 Mod 实机：白绮待复活时决议禁用并显示正确中文，点击不弹出对话；复活后决议可用并正常弹出白绮对话。正式包 `open_kaishek PASS`：19/19 脚本、13 DDS、173 本地化键。已发布前完成的 SV-01 全状态存档重载仍有归档证据。
- 其余九种官方语言**静态校验通过，运行时不在范围内**；整体验收矩阵仍在继续。

### Known limitations

- 部分奖励池数值边界、项目取消/中断组合及长期平衡路线仍待补齐；第三方 Mod 兼容性尚未系统验证。详见 `docs/shishan-code-origin-acceptance-report-2026-09-27.md`。

## [0.1.0] - 2026-09-29

### Added

- 首次公开发布独立起源「屎山代码」：五阶段局势、可重复维护与持续优化、清理重构、维护研究所和白绮事件链。
- 提供 Stellaris 官方十种界面语言的完整文本，以及白绮的肖像、事件图和玩法图标。

### Changed

- 局势初始月进度为 `+5`；持续资源按来源各受一次阶段修正，岗位产出和同一收入不重复叠加。
- 「重构完成」给全帝国岗位产出 `+25%`，岗位维护费不随之上升。

### Fixed

- 修复白绮领袖界面的肖像布局、复活后的经验和已消费备份清理，以及持续优化未复发时的完成对白。
- 修复个体机械帝国的起始特质点数修正；维护与持续优化的结算事件现只接受各自项目成功时的一次性凭证，避免事件重放重复发奖。

### Compatibility

- 兼容 Stellaris `4.5.*`。这是新的创意工坊物品，不更新仓库其他 Mod 或只读上游物品。

### Validation

- 正式包 `open_kaishek PASS`：19/19 脚本、13 DDS、172 本地化键。简体中文单 Mod 实机已验证两类机械开局、五阶段与多种持续资源、项目自然完成及重载、白绮复活和本版重复结算防护等已归档场景。
- 其余九种官方语言**静态校验通过，运行时不在范围内**。整体验收矩阵尚未全部完成。

### Known limitations

- 局势月速在已分配维护员劳动力 `J=4800/5800` 的最低 `0.2` 边界、部分奖励池实机数值边界、剩余项目取消/中断组合及长期平衡路线仍待完成；进度与证据见 `docs/shishan-code-origin-acceptance-report-2026-09-27.md`。
- 第三方 Mod 兼容性尚未系统验证；简体中文之外的运行时界面不在本版验收范围内。

## [0.1.0-rc.1] - 2026-09-26

### Added

- Standalone Shishan Code origin, five-stage situation, repeatable society research projects, maintenance institute and jobs, machine-compatible reward traits, and Vivhite event chain with resurrection.
- Art assets and localisation for all ten supported languages.

### Changed

- Initial situation progress is now +5 per month. The Chinese origin text says “许多年前，创造者消失了”.
- Vivhite uses the revised V2 portrait with aligned hair ornaments and a static portrait texture in the leader UI; the A05 event art was regenerated from the V2 concept.
- Both machine government types now receive the intended starting trait budget change of 6 fewer points and 3 more selectable traits.
- Stage resource production now includes the independent monthly Trade resource; market orders remain separate from production.
- Refactored completion now grants +25% empire-wide job output for all species without raising job upkeep. Old refactored saves receive the national modifier at the next monthly pulse; relapse removes it.

### Fixed

- Vivhite's paid resurrection now preserves her level, traits, and current experience even when her experience-gain rate is zero. The short recovery sequence survives a save reload and a second accidental death; consumed exiled backups are removed.
- Corrected the machine trait point modifier key used by individual machine empires.

### Compatibility

- Targets Stellaris 4.5.*. Steam publication is not part of this development build.

### Validation

- `open_kaishek` package-level static acceptance passed: 19 scripts, 13 DDS assets, and 167 localisation keys.
- The nine non-Chinese languages passed static checks; their runtime is outside the test scope.
- Simplified Chinese runtime checks passed for the revised portrait, both machine empire starts, the five situation stages and ship attribute values, the five-stage job-upkeep matrix, maintenance project completion and cancellation, cleanup cancellation and natural fifth-stage completion, reward-pool transitions, Trade and rare orbital source isolation, a Dyson Sphere production sample, tributary tax and bilateral resource-transfer exclusion, and Vivhite's resurrection. The cleanup result persisted after removing the temporary research-speed fixture and reloading with the formal mod. The full scenario matrix remains incomplete.

### Known limitations

- Controlled combat damage, same-route travel time, commercial pact income, and long-range balance routes still require runtime checks. Bilateral monthly resource transfers were verified separately. See `docs/shishan-code-origin-acceptance-report-2026-09-27.md`. This release candidate has not been uploaded to Steam.
