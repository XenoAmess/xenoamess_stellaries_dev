# SC-01/02 非起源帝国隔离检查（2026-09-29）

## 目标与验收口径

补齐「屎山代码」只向机械主体帝国提供起源、只在选中起源时初始化局势/项目并开放研究所的负向对照。现有格式塔及个体机械正向开局、特质预算和同星球多座研究所已有归档；本轮不重复该正向路径。正式 Stellaris 4.5.1、简体中文、单独启用已发布 Mod，Steam 离线。

从正式 Mod 脚本核对：起源 `possible` 的机械物种原型条件；初始化事件的 `has_origin` 守卫及防重复旗标；研究所 `potential` 的拥有者起源条件；局势的非起源终止条件；项目不由全局自动授予。再用一名非本起源的普通有机帝国正常开局，读取原生存档与简中 UI：玩家没有本起源、主体物种没有 `trait_shishan_code`、没有 `situation_shishan_code`、没有本 Mod 的维护/清理/优化项目，首都可建列表没有 `building_shishan_code_institute`。有机起源不可选需从创角 UI 或脚本资格条件独立核对，不把非起源新局自动视为该条件的实机证明。

保留有效存档、截图、SHA-256、Mod 文件核对、`open_kaishek` 结果和脚本/原版日志；若普通帝国意外获得任何专属内容，按 FAIL 追查。通过负向对照后，SC-01/02 仍须与已归档的正向开局证据结合判断整行。

## 执行结果

**PASS。**在简体中文 Stellaris 4.5.1、`fe44`、仅启用正式 Mod、Steam 离线的现有隔离目录中，直接用预设有机帝国「地球联合国」开局。开局 UI 显示原版「繁荣一统」；首都建筑菜单仅列出当前可建的研究实验室、行政办公室，没有「屎山维护研究所」。[开局截图](../assets/shishan-code-origin/evidence/sc01-une-nonorigin-opening-2200.01.01.jpg)、[建筑菜单](../assets/shishan-code-origin/evidence/sc02-une-nonorigin-building-menu-2200.01.01.jpg)。

原生 [2200.01.01 存档](../assets/shishan-code-origin/evidence/sc01-une-nonorigin-2200.01.01.sav) 的 SHA-256 是 `f210779d669828f997bea0f53ed4bbcb9fe8dd79b9ebaa2bfa687e1e4c70f7a6`。玩家起源 `origin_default`，主体物种 ID `1191182337`，特质仅 `trait_organic`、`trait_adaptive`、`trait_nomadic`、`trait_wasteful`、`trait_pc_continental_preference`；整个 `gamestate` 的 `shishan` 字符串数为 `0`。这同时排除本 Mod 的起源特质、局势、项目、建筑和白绮初始化对象。[可复查审计 JSON](../assets/shishan-code-origin/evidence/sc01-nonorigin-audit-2026-09-29.json) 的七项检查全为 true；执行 `py tools/shishan_code/audit_sc01_nonorigin.py` 返回 0。

随后回到创角界面编辑同一有机帝国，滚动至「屎山代码」。[悬停提示](../assets/shishan-code-origin/evidence/sc01-organic-origin-locked-tooltip.jpg)在「具有物种类型：机械」前显示红叉；实际点击灰色起源卡片后，[右侧仍是「繁荣一统」](../assets/shishan-code-origin/evidence/sc01-organic-origin-still-default-after-click.jpg)。因此「有机主体不可选」有独立实机证据，不仅依赖开局结果。脚本资格条件为 `species_archetype = { value = MACHINE }`。

静态复核确认初始化事件以 `has_origin = origin_shishan_code` 守卫，建筑 `potential` 限定拥有者起源，局势对非本起源终止。正式 Mod 与隔离部署逐文件 SHA-256 比较为 **64/64 完全一致**；`open_kaishek` 再次 **PASS：19/19 脚本、13 DDS、172 本地化键**。本次 `error.log` 仅列出离线状态下已卸载的旧 Workshop 路径，没有本 Mod 脚本错误。结合先前机械智能和个体机械的正向开局证据，SC-01、SC-02 的既定验收口径均满足。

测试只覆盖一个标准有机预设帝国的负向对照；资格脚本对所有非机械物种使用同一 `MACHINE` 条件。没有保存或发布被编辑的测试帝国。
