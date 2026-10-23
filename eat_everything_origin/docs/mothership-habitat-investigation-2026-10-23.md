# 母舰不能摧毁居住站：反馈调查（2026-10-23）

## 目标、范围与核查标准

用户反馈：“那个母舰爆不了居住站”。本次只读调查正式版 0.4.0 的饕餮解构光束，核对目标筛选、完成结算、原版居住站定义、既有需求与验收证据；不修改 Mod、版本或发布内容，不启动游戏。

调查完成标准：指出足以解释反馈的确定性条件，区分既定限制与实现偏差，记录正式标签一致性和可复核证据。另先使用 `D:/workspace/open_kaishek` 既有入口检查生产包；其结果仅认证工具覆盖的静态合同，不作为本次实机复现或完整 Mod 验收。

## 结论

反馈描述符合当前正式版行为。0.4.0 **主动排除居住站**，原因是两条独立的目标类型限制，不需要母舰损坏或存档异常就会发生：

1. [`eep_planet_killer.txt:12`](../mod/common/scripted_triggers/eep_planet_killer.txt#L12) 的 `eep_colossus_target_valid` 要求 `is_artificial = no`。本机 Stellaris 4.5.2 的 `common/planet_classes/00_planet_classes.txt:1584` 定义 `pc_habitat`，在 :1616 明确设置 `is_artificial_planet = yes`，因此原版居住站不满足该条件。
2. 同一目标触发器 :23 要求 `eep_digestible_world = yes`。[其定义](../mod/common/scripted_triggers/eep_triggers.txt#L41)只接受原版 `can_have_habitable_deposits` 名单及 `pc_hive`、`pc_machine`。本机 `common/scripted_triggers/00_scripted_triggers.txt:579–595` 的完整名单没有 `pc_habitat`，后两种类型也不包含居住站。因此只删除 `is_artificial = no` **仍不能放开居住站**。

上述条件同时用于原生武器目标判定、完成事件 `eep.50`、`eep_colossus_settle` 以及共享结算入口的复验。只放开下令入口而不处理复验，仍无法获得完整摧毁与结算行为。

按已记录的 0.4.0 需求，这是既定功能范围限制；若希望母舰也能炸居住站，应作为目标范围扩展处理，不能把本次调查描述成“已经修复”。用户未提供具体存档，本次没有声称复现其 UI、充能或发射过程。

## 设计、公开文案与历史证据

- [1019 需求第 4 项](requirements-2026-10-19.md#L26)明确写了“可吞噬天然殖民星”和“不允许……人工星”。实现符合这项既有约定。
- [简中组件说明及失败提示](../mod/localisation/simp_chinese/eep_l_simp_chinese.yml#L104)分别限定“天然殖民星”，并明确“不能攻击……人工天体”。
- [随仓库保存的工坊正文](../workshop/description.bbcode#L25)同样排除人工天体。2026-10-23 尝试在线读取工坊物品 `3815707212` 失败；本次公开文案结论仅指仓库副本，不宣称重新核验了当前远端页面。
- [恢复后的保护条件运行记录](rc7-guard-resumed-runtime-1020.md#L19)记载人工目标为物理 planet7、`pc_habitat`、colony23；[A 组结果](rc7-guard-resumed-runtime-1020.md#L46)通过不结算检查。[最终索引](evidence/1019-requirements/final-result.json)的 `artificial_rejected` 为 true。这是历史受控目标的拒绝证据，不等于完整建造的居住站被原生武器实际发射摧毁。
- 当前 HEAD `c6147155752c68eafdadd9dd168e410bdc8664e6` 与正式标签 `v0.4.0` 对目标规则、共用触发器、完成事件、巨像结算、共享结算及简中本地化进行原始 Git blob 比较；结果保存于下述调查证据。相同意味着此限制已在正式版存在。

## 若扩展支持，需要处理的内容（尚未实施）

本机原版 `events/planet_destruction_events.txt:292–299` 对 `pc_habitat` 单独调用 `spawn_habitat_cracker_effect`。该效果位于 `common/scripted_effects/00_scripted_effects.txt:1792–1833`，包含废墟生成、关联标记与居住站舰队清理、`remove_planet`。这表明原版脚本已有居住站毁灭处理，不能把本次拦截归因于“游戏统一禁止炸居住站”。本次未实际运行该原版分支。

当前 Mod 的[末端销毁](../mod/common/scripted_effects/eep_settlement_effects.txt#L125)统一使用 `destroy_colony`、`change_pc = pc_shattered`、`clear_deposits`，没有居住站分支。因此未来扩展至少需要：

- 只为计划支持的居住站类型增加专属目标分支，保留母星核心、交战关系、殖民中、地战、重复结算及取消保护；普通吞星与王座迁移的人工天体限制不能顺带全部解除。
- 明确居住站是否以及如何贡献有效物质、容量、人口和母舰成长；不能未经设计直接把可重复建造的人工站按天然星球收益发放。
- 在产生收益及防重凭证后，按原版居住站生命周期适配销毁与关联对象清理，核对共享结算在载体被移除后的作用域有效性。
- 更新提示及十语言静态合同，先通过 open_kaishek，再进行简中专用实机验证：真实建成的敌方与自有居住站、原生下令及 90/30 时长、取消、发射完成、关联对象清理、人口与收益、防重和重载；同时回归天然星球与其它人工天体拒绝。

以上为后续实现所需范围，未新增功能、测试夹具或验收工具，也未变更原有验收结果。

## 本次证据与检查状态

证据目录：[`evidence/2026-10-23-mothership-habitat-investigation/`](evidence/2026-10-23-mothership-habitat-investigation/)。[调查 JSON](evidence/2026-10-23-mothership-habitat-investigation/source-investigation.json)记录原生文件和 Mod 文件指纹、精确源码片段、正式标签比对及历史拒绝结果的索引位置。七份相关文件的 HEAD 与 `v0.4.0` Git blob 全部相同；本机 EXE SHA256 为 `400df27c82ddc845aa9dce79bd468d81f18f060d299cd263e3afa93aef4f7a83`。

本次实际运行 open_kaishek 的[生产包静态检查](evidence/2026-10-23-mothership-habitat-investigation/static-open-kaishek.json)：**PASS**，36/36 P 脚本、12 DDS、132 本地化键 × 10 语言；巨像三回调、90/30 数值来源、十语言通知引用检查通过。其它九语言**静态校验通过，运行时不在范围内**。该检查不认证居住站实机行为，也不意味着新增了对居住站的支持。

首次调用未传本多 Mod 仓库所需的版本文件，以及本机 4.5.2 的 EXE 指纹，出现 `GAME_EXE_IDENTITY` 和 `MOD_METADATA_MISSING`；[原 FAIL](evidence/2026-10-23-mothership-habitat-investigation/static-default-invocation-fail.json)保留。核实本机 EXE 与既有构建指纹一致后，补全上述参数重新执行，得到前述 PASS，未修改工具或生产包。正确调用：

```powershell
python D:/workspace/open_kaishek/tools/accept_stellaris_mod.py --mod D:/workspace/xenoamess_stellaries_dev/eat_everything_origin/mod --game C:/SteamLibrary/steamapps/common/Stellaris --version-file D:/workspace/xenoamess_stellaries_dev/eat_everything_origin/VERSION --expected-exe-sha256 400df27c82ddc845aa9dce79bd468d81f18f060d299cd263e3afa93aef4f7a83 --report D:/workspace/xenoamess_stellaries_dev/eat_everything_origin/docs/evidence/2026-10-23-mothership-habitat-investigation/static-open-kaishek.json
```

本次仅完成问题归因和静态检查，没有启动 Stellaris，没有执行新的实机测试，也没有修复或发布 Mod。
