# PR-03 混合机械物种重构岗位范围实机方案（2026-09-29）

## 目标与范围

用户已确定「重构完成」按全国岗位产出 `+25%`，岗位维护费不变；正式 Mod 已从旧物种劳动力修正改为国家 `planet_jobs_produces_mult=0.25`。先前实机以单一主体物种物理学家验证了产出与维护费，本轮在同一矿工岗位同时有两种机械模板的隔离夹具里复测，避免“只对主体物种生效”的范围错误。正式 Mod 和其他证据不改。

## 方法与验收标准

使用已归档的 RS-04 科技共同基线 `rs04-tech-anchor-2203.09.24.sav`，玩家国家为个体机械；首都矿工岗位有主体和子模板共 `2800` 劳动力，两者都未超过合法岗位容量。该基线局势应为第二阶段，阶段本身无生产修正。先正常月结算、保存清理前锚点；在同一锚点用游戏的真实清理项目完成回调切换重构，再推进到与对照分支同一天保存。清理后须只有一个 `shishan_code_refactored_jobs` 国家修正、一个「重构完成」主体物种特质、没有「大厦将倾」局势；第二个机械模板不应被改写。两支要有相同的两模板矿工人数、总有效劳动力、原版科技和其他固定加成。

检查玩家月预算 `planet_miners.minerals`：清理后比清理前增加矿工未修正基础矿物产出的 `25%`，且无第二层作用。此夹具的矿工没有单独的 `expenses.planet_miners` 条目，不能拿零值证明维护费不变；改用非零的 `expenses.planet_physicists.consumer_goods` 与同一物理学家岗位 UI 比较，维护费应相等。国家基础、采集站矿物不应因重构修正改变。存档与 Steam F12 截图、输入哈希、日志和正式 `open_kaishek` 结果入库。若分支岗位人数/科技变化，重新构造相同条件，不对有混杂的数值下结论。隔离夹具若具有额外测试矿工容量，必须在结果说明它只影响岗位容量，不改变正式清理回调。

## 执行结果

从[科技共同基线](../assets/shishan-code-origin/evidence/rs04-tech-anchor-2203.09.24.sav)在隔离局推进 15 日保存[清理前锚点](../assets/shishan-code-origin/evidence/pr03-mixed-before-2203.10.09.sav)；然后从该锚点独立推进 30 日成[未清理对照](../assets/shishan-code-origin/evidence/pr03-mixed-control-2203.11.09.sav)，另一支在相同锚点以游戏控制台调用正式 `shishan_code.20` 清理回调，白绮[清理弹窗](../assets/shishan-code-origin/evidence/pr03-mixed-clean-event-2203.10.09.jpg)实际出现，再推进相同 30 日成[已重构分支](../assets/shishan-code-origin/evidence/pr03-mixed-refactored-2203.11.09.sav)。这次受控调用验证正式回调与数值作用；第五阶段的**自然研究完成**另见[原项目验收](shishan-code-origin-clean-natural-2026-09-28.md)。本隔离 RS-04 副本额外提供合法的矿工岗位容量，原版科技 `tech_synthetic_thought_patterns`、`tech_space_mining_1` 在两支都存在；正式清理脚本未改。

两份 `2203.11.09` 存档中，主/子模板人口组大小均为 `2900/500`，均享完整公民权；同一个首都矿工岗位的已分配人数为 `2300/500`，岗位普通劳动力 `2800`、原版额外劳动力 `280`。主体物种 ID `3321888769` 在清理后由唯一一个 `trait_shishan_code` 改为唯一一个 `trait_shishan_refactored`；子模板 ID `48` 的特质列表原样保留，其中旧代码特质仍在。国家只出现一个 `shishan_code_refactored_jobs`，局势由一条变为零条。由于第二阶段没有阶段生产修正，两支数值可直接对照：

| 同日玩家月预算 | 未清理 | 已重构 | 差 |
| --- | ---: | ---: | ---: |
| 矿工岗位矿物 | 135.30809 | 166.10809 | +30.8 |
| 物理学家岗位物理学研究点 | 4.19078 | 5.18078 | +0.99 |
| 物理学家消费品维护费 | 1.98 | 1.98 | 0 |
| 国家基础矿物 | 20 | 20 | 0 |
| 轨道采集站矿物 | 11 | 11 | 0 |

矿工未修正基础产出是 `(2800+280)÷100×4=123.2`，其 `25%` 恰好为 `30.8`。这笔增量覆盖在同一岗位工作的**两种机械模板**，并且只作用一次。物理学家基础研究点 `3.96` 的 `25%` 为 `0.99`；消费品维护费在预算中保持 `1.98`。同日 Steam F12 [清理前矿物来源](../assets/shishan-code-origin/evidence/pr03-mixed-control-minerals-2203.11.09.jpg)/[清理后矿物来源](../assets/shishan-code-origin/evidence/pr03-mixed-refactored-minerals-2203.11.09.jpg)分别显示岗位约 `135.33/166.10`、基础与站点 `20/11`。其中实时 UI 的前值与已存储月预算 `135.30809` 相差约 `0.02`，因此精确的 `30.8` 增量以两支同日原生预算为准，截图仅佐证 UI 所见数量级及来源。修正后同一物理学家岗位实时 UI 的维护费不变已有[先前实机记录](shishan-code-origin-acceptance-report-2026-09-27.md)及其截图佐证；本轮以两个相同日期的非零预算精确核对。

[审计脚本](../tools/shishan_code/audit_pr03_mixed_refactor.py)对三份原生存档的日期、岗位混合分配、物种权利与特质、科技、唯一全国修正、局势及预算差值作严格断言，[JSON](../assets/shishan-code-origin/evidence/pr03-mixed-refactor-audit-2026-09-29.json) 返回 `PASS`，SHA-256 为 `9228294d7754e8b6992a86e8a44c973b2eee2fb51dc05dcdea23cc6a1f084c1d`。清理前锚点、未清理对照、已重构存档 SHA-256 依次为 `17b0253b80da697c084b9ba0c5c9d0d6c3543014721d5b31bd4e822028e2612e`、`325271c686e7a5fcc960b2e15d02319f50dfa752d48003f38bf9a77cccb8cd10`、`ee591d1d1bfa9697db335aa1e047da40052a51885a05da1f33fce3919462b7ba`；清理弹窗、对照矿物、重构矿物截图 SHA-256 依次为 `9ea31ad171fddeb6f324e62eee095bd6375ea5a139800feecd6253dce64a8bd8`、`7a6d98daa0caf71f8c50a01b61102a23a76bd62a12972c0b7ca4027ef1ebd40e`、`f19c583160ddd72bc4e05dfb36e0aa16bc637f4b397e2e1213315f799af81374`。

隔离 `error.log` 从商业协议测试的[归档快照](../assets/shishan-code-origin/evidence/rs03-commercial-error-2026-09-29.log)至本轮结束仍为 22 行，未新增 Mod 脚本报错。正式 Mod 再次经 `C:\workspace\open_kaishek\tools\accept_stellaris_mod.py` 检查为 `PASS`：19/19 脚本、13 张 DDS、172 个本地化键；非中文翻译静态校验通过，运行时不在范围内。混合物种的「重构完成」岗位范围及维护费子项通过，项目整体仍须按总矩阵判定。
