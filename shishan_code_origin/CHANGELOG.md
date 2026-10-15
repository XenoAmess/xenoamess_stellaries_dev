# Changelog

## [0.2.1] - 2026-10-15

### Added

- 新增「基于低内聚高耦合的旧时代集成服务架构」：国内主体谱系的所有正式物种特质（正面、负面、隐藏、偏好及身份）按实际人口加权，每有效特质提供+5%岗位产出加算。保留旧特质效果与维护；实体池耗尽后转为无硬上限的重复层。
- 维护/优化奖励改为三个不同合法选项，可稍后领取；免费重抽每张票最多一次，冷却为三次实体选择。旧四类迭代计数一次性迁移，原有效果保留。

### Changed

- 局势基础月速改为1；每次维护/优化增加0.25，每100实际分配维护员减速0.25，下限0.2。
- 维护员每100实际分配的基础产出为3社会学与1凝聚力。III/IV/V负面阶段惩罚减半至12.5%/25%/37.5%，I阶段红利保留。
- 白绮社会学改为正向+5%、每次维护/优化再+2.5%，工程学保留+10%和每次+5%，成长无额外上限；本人免除全部资源维护，其它领袖正常付费。

### Fixed

- 修复4.5.2人口作用域、普通script value格式及效果初始化深度导致的引擎加载错误。
- 修复随机权重取反导致的候选重复/混层，补全机械特质互斥、DLC与模板资格。
- 修复国内模板克隆后的权利、主体指针、特使迁移和白绮专属头像；外国共享旧模板保持不变。
- 修复同日清理后物种列表缓存滞后造成的误耗尽、重复层误增和空奖励窗口。
- 修复白绮-100%维护仍被经济倍率下限收取费用的问题；真实死亡/付费重启保留等级、非零经验及技能。
- 长机制名补充正文全文；奖励提示隐藏内部变量和执行细节，补齐十语言显示键。

### Compatibility

- Stellaris 4.5.*，本机实测Cygnus4.5.2/build25664273。更新自有Workshop3810136486，不更新只读上游3710613857。
- 正式包不含测试夹具。正式0.2.1提升rc.6包版本身份并更正十语言“预发布”措辞，不改变其功能脚本。

### Validation

- 正式0.2.1已重新通过open_kaishek（25/25脚本、13DDS、269键）、六项合同及十语静态；rc.6的107项功能回归、745资格断言及核心实机证据可追溯，功能脚本未变。发布器另有13项门禁测试通过。
- 简中实机已覆盖三选一/重抽冷却、真实模板迁移、清理/优化/复发交叉、旧重复层保存重载、白绮个人免费及500能量/200合金重启恢复level5/XP25；初始1/.75、J500下限.2与III–V跨月预算通过。
- 其余九种语言静态校验通过，运行时不在范围内。更多功能边界、显示组合、资源/性能验收仍在继续，不声明全部新增需求已验收。

### Known limitations

- 本版每特质5%采用原生加算。独立乘算调查在全国岗位、维护/就业不变及兼容性约束下未找到已有充分证据的合适方案，采用用户允许的加算回退，不声称引擎普遍无法实现乘算。
- 统计按月刷新，月内人口变化存在缓存窗口；长名称在已验证配置的正文完整可读，原生标题栏仍可能省略。
- 22自然新局及长期路线按用户要求不纳入本轮继续验收；其它显示组合、所有资源来源、舰船实战和性能尚未全部覆盖。第三方完整Mod组合不保证。

## [0.2.0-rc.6] - 2026-10-15

### Added

- 白绮个人维护实际费用与死亡重启的简中实机对照。

### Changed

- 白绮本人免费使用原生领袖维护豁免开关，覆盖初建、旧档刷新和重启。该原生开关免除本人全部资源维护。

### Fixed

- 修复经济倍率最低-90%使白绮在-100%自身维护修正下仍收费的问题；其它领袖正常付费。

### Compatibility

- Stellaris 4.5.*；原生豁免规则已核对本机4.5.2。未发布Workshop，实机仅简中。

### Validation

- 正式/隔离包G1通过（25/25、26/26脚本，13DDS、269键）；107项程序回归、六项合同及745资格断言通过。
- 简中实机确认本人免费、其它领袖正常付费；实际500能量/200合金重启后level5/XP25及技能保留。清理保票/第四次领取CD2、优化复发交叉、旧R25真实重载通过。详细范围及历史失败见docs/runtime-feedback-validation-2026-10-15.md；完整自然新局与显示矩阵未执行。
- 同候选受控边界实测J500/n1时月速下限0.2；III–V中文详情的产出惩罚12.5%/25%/37.5%、岗位维护对应增加，保留原生跨月存档及预算审计；舰船战斗未执行。

### Known limitations

- 每特质5%仍采用原生岗位产出加算，独立乘算未实现；人口统计存在月内缓存窗口。完整自然新局及显示矩阵未覆盖，非中文运行时不在范围内。

## [0.2.0-rc.5] - 2026-10-15

### Added

- 同日清理/待领奖励交叉的原生失败证据，以及物种缓存滞后、多人口组模板的回归。

### Changed

- 资格、领取和状态替换按实际国内正人口定位模板，避免依赖延迟更新的国家物种列表。

### Fixed

- 清理后立即重新打开待领奖励时误判实体池耗尽、额外增加重复层和空窗口的问题。

### Compatibility

- Stellaris 4.5.*；本机简体中文4.5.2，未发布Workshop。

### Validation

- 工具、程序与原生交叉复验见 docs/runtime-feedback-validation-2026-10-15.md；rc.4失败原始证据保留。

### Known limitations

- 每特质5%仍为原生岗位产出加算；月内人口变化存在缓存窗口。完整自然局和显示矩阵尚未完成；非中文运行时不在范围内。

## [0.2.0-rc.4] - 2026-10-15

### Added

- 按本机原版AST独立核对机械奖励的互斥、DLC和模板资格；补充实际克隆的权利、特使与外国共享模板存档对照。

### Changed

- 机械候选沿用原有分层、冷却和数值，资格过滤补齐原版直接及反向互斥、Machine Age条件与机械模板限制。

### Fixed

- 领取科研核心后不再继续提供其互斥核心；补齐其余机械候选的漏配互斥条件。
- 克隆显式继承父模板权利，防止国内子模板回退到默认权利；补齐国内特使迁移。
- 模板迁移后恢复白绮专属头像，保留原领袖身份和成长。
- 在使用奖励国家事件目标前检查其存在，避免提示预评估时对空目标切换作用域。

### Compatibility

- Stellaris 4.5.*，本机基线4.5.2，未发布Workshop；非中文运行时不在范围内。

### Validation

- 包级检查、程序回归与简体中文实机结果见 `docs/runtime-feedback-validation-2026-10-15.md`。rc.3发现的错误及原生存档继续保留，不将修复代码本身记作实机通过。

### Known limitations

- 每特质5%为原生岗位加算；统计按刷新采样，月内人口变化存在缓存窗口。完整自然局、独立乘算及全部显示矩阵仍未完成验收。

## [0.2.0-rc.3] - 2026-10-15

### Added

- 实机确认的逻辑真值表和确定性奖励权重回归；保留旧候选混层、重复与标题截断的失败证据。

### Changed

- 奖励选项隐藏内部模板迁移和变量操作，保留特质说明、覆盖率和重抽可用条件。

### Fixed

- 随机候选屏蔽条件使用显式 `NOT = { AND = { ... } }`，修复引擎多条件 NOT 语义导致的跨层和重复候选。
- 十语言机制正文显示完整名称并分段，避免长标题被原生省略后无法阅读全文。
- 十语言补齐领袖凝聚力维护费修正的显示键，消除领袖提示内部 key 和加载警告。
- 离线解释器按实机真值表修正 NOT，防止相同脚本得到虚假的程序通过结果。

### Compatibility

- Stellaris 4.5.*，本机实测基线4.5.2；未发布Workshop。实机只用简体中文，其余语言运行时不在范围内。

### Validation

- rc.3包级、程序与简中实机复验结果见 `docs/runtime-feedback-validation-2026-10-15.md`，未执行项不继承旧候选的通过状态。

### Known limitations

- 每特质5%仍为原生岗位加算；独立乘算、完整自然局和显示矩阵未完成验收。

## [0.2.0-rc.2] - 2026-10-15

### Added

- 本Mod独立的简体中文隔离实机入口与原生存档只读审计；记录真实玩家国家、殖民地载体、人口加权特质及观察变量，明确区分旧档预期与本轮引擎结果。

### Changed

- 迁移四类历史重复计数时内联原有参数助手，将scripted effect最长调用链由5层降为4层，保持一次性迁移与计数规则。

### Fixed

- 人口组正人口条件和人口权重读取改为原生`pop_group_size`，修复`pop_amount`展开到不支持作用域的触发器所产生的加载错误。
- 每特质5%脚本值改为`{ base = 0.05 }`块定义，修复引擎`Invalid script value`；5%数值与加算合同保持。

### Compatibility

- 当前实机基线为Stellaris Cygnus 4.5.2，兼容声明仍为4.5.*；本候选未发布Workshop。实机仅简体中文，其余九语言仅静态校验。

### Validation

- rc.1在实际4.5.2加载暴露人口组作用域、脚本值与初始化深度三类失败，旧程序PASS不等于引擎通过。工具能力补强、rc.2包级及实机复验结果持续写入`docs/runtime-feedback-validation-2026-10-15.md`。

### Known limitations

- 每特质5%当前采用原生岗位产出加算，独立乘算未实现；白绮在其它正维护倍率叠加下严格零费用、完整自然局及全部显示矩阵仍须按实际证据单独判定。

## [0.2.0-rc.1] - 2026-10-04

### Added

- 「基于低内聚高耦合的旧时代集成服务架构」：所有正式特质正负均计，按国内主体谱系实际人口加权，每个有效特质增加 5% 岗位产出；有限池耗尽后固定增加重复层，无人为上限。此候选明确采用原生加算，独立乘算尚未实现。
- 同层最多三选一、免费重抽、三次实体选择冷却、持久候选及首都重新查看入口。选择结算只领取一次，自动重复层不推进重抽冷却。
- 架构详情入口和十语言完整文本；新增无游戏依赖的程序合同校验器与负例测试。

### Changed

- 初始局势月速 1，每次维护/优化增加 0.25；每全国完整 100 已分配维护员劳动力减速 0.25，最低 0.2。研究所基础社会学 3、凝聚力 1，原维护不变。
- III/IV/V 生产、舰船与岗位维护的惩罚减半；I 红利和重构岗位 +25% 保留。
- 白绮社会学速度改为 +5%、每次额外 +2.5%，移除旧负面上限；自身凝聚力维护修正 -100%，其它领袖不减免。
- 旧四类迭代保留既有效果并冻结新增计数；仅迁移每类首层以外的历史重复层（7/5/11/4 → 23），仅一次。

### Fixed

- 奖励与状态转换通过克隆模板，只迁本国精确匹配的人口/领袖，避免直接更改共享物种影响外国。
- 待选期间不恢复下一循环项目，清理交叉后恢复正确项目；清理、维护、优化和复发回调采用一次性凭证。
- 月脉冲恢复已保存的成功凭证，维护/优化跨清理或复发仍保留已赚取奖励；唯一奖励窗口锁防止正常入口重复开窗并消费后来票据。

### Compatibility

- 面向 Stellaris 4.5.*，静态依据为本机 4.5.1；本版为未发布的开发候选，没有启动游戏、修改 Workshop 或创建发布标签。
- 保留起源 -6 特质点/+3 栏、原研究费用和白绮复活成长流程。九种非中文语言运行时不在范围内。

### Validation

- 按用户范围仅执行 `open_kaishek` 包级解析、静态本地化和离线程序合同/负例。最终命令、报告与范围见 `docs/feedback-redesign-implementation-2026-10-04.md`；不继承旧版实机 PASS。

### Known limitations

- 当前每特质 5% 与既有岗位修正加算，不满足原独立乘算目标；详情与说明明确标注，不把统计系数视为实际收入倍率。
- 引擎的实际模板克隆、岗位经济、存档迁移重载、重抽交互及 18 字全名的宽度/换行尚未实机验证；长期自然体验与性能未执行。
- 白绮 -100% 自身凝聚力维护修正与其它正维护倍率组合后的精确归零尚未实机验证；不宣称所有组合下已保证免费。

## [0.1.3] - 2026-09-30

### Added

- 本版不新增玩法机制；公开包纳入已通过简中实机验收的项目中断恢复。

### Changed

- 月度检查在没有项目成功结算待处理标记时，复核起源应提供的特殊项目；正常项目和已重构后的持续优化保持唯一。

### Fixed

- 修复原版 `abort_special_project` 中断研究中的「维护屎山」后项目永久丢失。维护项目在下一次月脉冲重新可用，次数和奖励不被误计。

### Compatibility

- 兼容 Stellaris `4.5.*`；沿用创意工坊物品 `3810136486`，A02 起源插画与八张简中真机截图继续在详细页面内。

### Validation

- 正式 `0.1.2` 单 Mod 简中实机复现引擎中断后项目跨月仍缺失。本版脚本在缺陷存档的下一次月脉冲恢复唯一维护项目，连续三个月不重复，再次中断后也恢复为单项目；已重构分支跨七个月仍只有一个「持续优化」。十份原生存档审计 10/10 通过；RS 来源矩阵 26/26，奖励池 8/8，SC/RS/PR/WH/UI/SV 简中验收矩阵已收口。`open_kaishek` 19/19 脚本、13 DDS、173 键 PASS；其余九种官方语言静态校验通过，运行时不在范围内。

### Known limitations

- 长期平衡与第三方 Mod 组合尚未作为本版的兼容性验收范围；游戏或 DLC 更新后须复核经济来源与特质映射。

## [0.1.2] - 2026-09-30

### Added

- 按玩家指定，在创意工坊 BBCode 开篇插入已入库的 A02 起源原图；页面图片清单记录其来源、Raw URL 和 SHA-256。原有八张简体中文真机截图继续穿插在机制说明中，并保留在截图画廊。

### Changed

- 页面明确将 A02 标为起源插画，与真机截图区分；不改变 Mod 玩法数值或已发布的对白。

### Fixed

- 这次页面更新没有改动运行时脚本；此前 v0.1.1 的白绮待复活提示修复继续保留。

### Compatibility

- 兼容 Stellaris `4.5.*`。更新本项目已拥有的创意工坊物品 `3810136486`；只读上游 `3710613857` 不作为上传目标。

### Validation

- 用户指定 A02 原图与公开 GitHub Raw 图像字节数一致，Raw URL 返回 `image/png`；正式包 `open_kaishek PASS`：19/19 脚本、13 DDS、173 本地化键。简体中文 UI-01 已完成证据收口；本次页面更新后的远端显示、包哈希核验见发布记录。
- 其余九种官方语言**静态校验通过，运行时不在范围内**；整体验收矩阵仍在继续。

### Known limitations

- 资源来源全组合、奖励池逐项实机边界、项目中断及长期平衡路线仍待补齐；第三方 Mod 兼容性尚未系统验证。详见 `docs/shishan-code-origin-acceptance-report-2026-09-27.md`。

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
