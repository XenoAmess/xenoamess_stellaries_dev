# 旧版真实受伤存档与跨版本迁移前置

目标是保留完整跨版本的原生损伤证据。公开0.3.1 `bmm00`／导入名`legacy031m`和旧付费队列`j13ten`／导入名`legacypaid`原件都满三防；在0.4加载后才施伤只能覆盖局部set_ship_design，不能认证原旧损伤跨版本。原SAV、历史baseline gate与当前RC4 run始终只读，不启动／停止游戏，不操作UI，不提交Git。

先调查1019与相关旧队列artifacts中的真实SAV、原生audit／receipt／manifest／冻结源，按实际Mother舰船ID抽取current／max三防及队列；现成损伤夹具必须来源链和旧源码版本均成立。仅小船受伤、缺来源、0.4原型或加载后才施伤的档不能替代旧受伤Mother夹具。报告明确调查范围与缺项，不能外推整个磁盘不存在。

若没有合格旧受伤档，独立建立`artifacts/1019-legacy-damage/public031/`，原字节复制已冻结公开0.3.1的mod／VERSION，以当前已修复open_kaishek重新静态验收并记录tool／CLI／EXE／源树指纹；0个PK应适用为零或不适用，不能强要求DEVOURER。新report／gate／profile独立命名，历史baseline source／gate绝不覆盖，也不改当前run指针。此步骤只准备可供主线程稍后启动的源码和门禁，不创建或宣称未来原生run／SAV／PASS。

最短原生后续入口是主线程稍后在旧profile分别加载两真实原件，暂停同日保存clean-before；只对绑定Mother实际ship执行可核原生绝对施伤并保存old-damaged。`reduce_hp=1000`、`reduce_shield=500`以生成effects文档为准；`damage_ship=120`已有原版armor注释用例，但仍须实际原生current armor下降确证，不能推断120必然精确伤甲。若无甲损伤，负`repair_armor_amount`只能另作未验证后备探针，不能用解析通过认证接口语义。三步施伤和同步分开保存，队列费用／进度／ID／库存／日期必须保持。

随后恢复冻结RC4，原生加载真正旧damaged SAV，先保存载入观察档，再在明确country scope执行已有同步并保存after，最后同日重载。比较旧damaged→RC4加载→同步→重载完整链的三防current/max及损伤比例、舰队／船／位置、布局人口、空队列或11付费项；max在load阶段已因同key modifier重新解释也必须记录，不能只比较载入后的局部before。

`on_game_start_country`与load语义先核原生on_actions源码、生成文档与已有真实输入／存档证据。脚本注册本身不能证明其在reload执行；若没有直接原生证据就保留UNKNOWN，并给出独立最小加载诊断设计。不得依赖猜测或把原生`fire_on_action`手工触发当作load自动触发的证明。

扩充调查范围为`single-homeworld-20261019/runs`中43份公开0.3.1原生档，以及`1015-implementation/runs`中所有旧0.3.0-rc.1原生档，另列对应j13ten源树的子集；当前1019原型与RC3／4均不作为旧损伤夹具。新增独立只读scanner只核已完成旧run：manifest／audit／receipt／SHA／ZIP CRC、原生Mother fleet target→实际ship ID、三防current/max，原始全字段保留。找不到来源链即列为未核而不判PASS，JSON结论只标OBSERVATION_ONLY，不改公共checker或历史候选表。

已找到原生独立加载入口：`common/on_actions/00_on_actions.txt:80-83`明确`on_single_player_save_game_load`为无scope，且因OOS原因不在MP读档执行；`on_game_start_country`在31行，没有同样load承诺。这足以要求将两个入口区分，不能据此推断未实测的country hook一定在load跑或绝不跑。其自动加载行为若影响迁移，需独立原生诊断或明确手动country同步证据。

调查已逐份覆盖150个旧原生SAV：137份原生来源链与Mother身份都核验成功，三防均满；其中42份公开0.3.1、11份真实j13ten同源树。其余13份保持缺口：12份有原生来源但没有绑定Mother target，1份公开月度校准副本缺自身audit。不能把它们悄悄计入通过。初版scanner将后来的v16／v17源树误标为“对应paid”；v2从j13ten已绑定原始报告更正到`eafb0b26b4832c1c395ce3870cdf5dfb3ce74839b70d16e017cd9049d833ce53`，所有原生三防读数不变、初版不改。

独立旧profile已真实通过修复版工具静态检查：47份mod文件同原公开0.3.1树`abca9b4195a991d98ca25336ed7807e0306d30e2c33021e4d307f78e1db864d8`，24P／12DDS／101keys；0CSV／0PK／0callbacks数目全匹配，numeric和callback applicability均为not_applicable_no_planet_killer_components。新gate／profile位于`artifacts/1019-legacy-damage/`，没有准备userdir、没有写run指针、没有launch、没有生成受伤SAV。旧baseline源和旧gate原字节保留。

13份缺口补充检查已完成后停止扩搜：12份无绑定／同名Mother；缺audit的`monthly-native-calibration-april.sav`与已验证`bmm03.sav`原始SHA完全相同，其Mother也满。原缺audit状态保持，不补造audit。最终已知范围没有能直接复用的合格受伤Mother档。清单v2 SHA256 `5d0a92857963bdec89c54ad9a3fbfdde4f67d7b54aefc112c769bd5069198ad5`，缺口复核SHA256 `73b2d3d439b822e329e8c82e33c5fcf7ec80e71400f3fefdd01347877d51c665`。

## 主线程后续最短实施入口（本文未执行）

当前RC4结束后，使用全新Python进程配置既有runtime，不导入`runtime_1019`，避免继承它的0.4门禁包装或写当前RC4指针：

```python
import sys
from pathlib import Path
sys.path.insert(0, r"D:\workspace\xenoamess_stellaries_dev\eat_everything_origin\tools")
import runtime_single_homeworld as b
b.ARTIFACTS = Path(r"C:\Users\1\AppData\Local\xenoamess_stellaries_dev\artifacts\1019-legacy-damage")
b.h.RUNTIME_ROOT = b.ARTIFACTS / "runs"
b.h.CURRENT_RUN = b.ARTIFACTS / "current-run.json"
b.h.WORKSHOP_ID = "eep-legacy-damage-public031"
b.h.PROFILE_ID = "eep-legacy-damage-public031"
prepared = b.prepare("public031")
```

后续启动／等待中文原生UI／载入／保存由主线程既有UI流程执行。把profile JSON绑定的原始`bmm00`、`j13ten`分别原字节导入新userdir；不要用修改过SAV替代。前者原始fleet128／ship1008、日期2200.01.01，后者fleet146／ship822、日期2200.01.12／11付费项；真实加载后重新核target、身份、队列与三防，不能把原始IDs当加载后已验证事实。

每个来源保持暂停，同日保存`ld031clean`／`ldpaidclean`。一条明确country ROOT、绑定Mother actual ship的原生命令可同时施加三层探针，再保存`ld031hurt`／`ldpaidhurt`：

```text
effect root={event_target:eep_mothership@this={every_owned_ship={reduce_hp=1000 reduce_shield=500 damage_ship=120}}}
```

reduce_hp／reduce_shield分别为绝对量。damage_ship文档只承诺一般伤害，armor是否下降按实际old-source SAV核对；由于其它两effect只改hull／shield，实际armor下降可归入damage_ship这次原生探针。若未伤armor，保留首结果，再另保存独立恢复点后考虑：

```text
effect root={event_target:eep_mothership@this={every_owned_ship={repair_armor_amount=-120}}}
```

后备负repair在本机原版无负值实例，标为未验证符号语义，仅实际SAV显示降低装甲后方可纳入damaged fixture；不能称这条命令已通过。本任务没有执行任一施伤命令。

暂停可避免11项队列推进和自动再生。受伤old-source SAV需保留完整native audit／receipt、旧copied_mod和来源manifest，再停旧profile恢复冻结RC4并载入它。分别保存`m031load`／`mpaidload`，记录同key modifier在load时重算带来的全部current/max变化；随后单独执行`effect root={eep_sync_mothership=yes}`并保存`m031sync`／`mpaidsync`，最后同日原生reload另存。旧受伤原件→RC4 load→sync→reload的完整链逐对保留strict差异。

现migration checker允许不同源树before／after，只要求after为0.4，因此可以直接把真实old-source受伤档作为before，`fixture_source`仍指原bmm00或j13ten，并以`queue_mode=empty,expected_queued_items=0`或`queue_mode=paid,expected_queued_items=11`验证完整跨版本。预先声明fraction或lost_absolute损伤政策，不按after结果改比较模式；自动修满不能判保伤。若只在RC4 load之后才制造损伤，结果必须限定为局部设计切换。

若按fraction验收，建议事前显式`damage_tolerance=0.000001`（比例绝对误差，rel_tol=0）；若按lost_absolute则用0.001HP。两种单位不同，不能无意共用0.001比例而允许几十HP漂移。这个建议未读取未来受伤或迁移SAV，不是按结果调阈值。

本次静态准备与资料绑定16项全真，报告`evidence/1019-analysis/legacy-damage-preparation-report-v1.json` SHA256 `a0643dfcaa51d85d5d54d341442c11650a101436653ec0dc68a7aebe1c60f4b6`。64份原字节准备包共5,392,251字节，`legacy-damage-preparation-v1/archive-index-v1.json` SHA256 `f8d13956ba987b12d6c0f676862b1d05f1614202d5f645e2a118a6be8053d1b1`，verification SHA256 `ccc8bf2ad99c337bef59386b7285823d2a503feeb10b51cd9ed1c003b63afcb3`。包内含完整公开0.3.1源码、独立新静态报告／gate／profile、旧baseline gate／report保真副本、当前工具源码与原生effects／on_actions、旧档清单和实施计划；全部只代表静态校验与准备通过，受伤生成和跨版本实机仍PENDING。

如果还需独立裁定on_game_start_country的load行为，最小原生设计是另建诊断副本，分别把country事件日志marker挂on_game_start_country，把无scope全局事件marker挂on_single_player_save_game_load；新游戏一次／同一原生SAV读档一次，按原生日志时间比较两个marker。该诊断不能放进当前public031精确源树、也不能用其改变过来源的SAV冒充公开版本受伤夹具。本任务没有创建该诊断Mod或执行任何hook。

## 原生旧profile执行阶段的只读检查设计

主线程已启动旧profile `20261019T130448Z`／PID5216，manifest原始树仍abca9b、版本0.3.1、简中、单Mod、无scheduled_commands，静态report仍46b24c53。等实际`ld031clean`／`ld031hurt`、`ldpaidclean`／`ldpaidhurt`各SAV／audit／immutable receipt完整才解析；不读取未完成原ZIP，也不碰UI／进程。

预先选定跨版本fraction损伤比较，ratio绝对误差0.000001、rel_tol=0，不改变公共checker门槛或按结果调整。旧profile clean→hurt的施伤验收独立报告同日同源、actual current三防下降／Mother存活／max不变，以及fleet／ship／starbase／shipyardqueue身份与完整队列已付费成本／进度／全部owned库存和core人口／布局不变；完整strict差异原样记录。damage_ship若没有实际伤甲则该层明确FAIL／未覆盖，后备探针另案保存，不伪造三层全通过。

迁移case模板先设PENDING，新RC4 after／reload未知保持null；真正before必须指这次旧0.3.1来源下生成的hurt原生档，fixture_source仍原始bmm00／j13ten。待新RC4加载后逐对比较oldhurt→loaded→sync→reload，不能把载入后已经重解释过static modifier的状态作为唯一before。

旧兼容section静态前提已独立核11／11：RC4在独立`eep_mothership_legacy.txt`保留旧key与public031／j13ten的15个明确weapon slot、12L utility／2AUX，与新`eep_mothership_section_1019`区分；新增hidden prerequisite不改旧槽。报告`legacy-section-migration-prerequisites-v1.json` SHA256 `d90b8f4a6bee81e286536f18314d02c1680979ce24c098d6b6f247102169be70`。这只是载入槽位前提，不宣称原生跨版本三防比例已保留。

`ld031clean`与`ld031hurt`已由原生完整保存Jan1，SHA分别7dcff806a7f6c20cd9a2a607c646f2d96ec2b31d07f88ebbaa5fc9086d6838fd／f2d2742aa321b43ec153aa56fd210bce5f3c3828518e4fc63be3987d37f18ebd。实际H93960→92960、A24429.6不变、S48370.608→47750.608，loss为1000／0／620。23项检查22真，仅armor_really_damaged失败，报告SHA256 `073fa4b55beda161834c8d7e0b05f72554d8153b338f91593130de90187636ad`，strict10原样保留。所有max、128／1008／starbase15／q50、空队列及所有owned queue项、位置／12舰船ID、两world人口4800＋100、pop groups／jobs、布局、库存energy200与全部EEP账本／母舰变量／modifier均不变。首hurt明确不是三层受伤fixture。

后续以主线程新增正向路线为准：在首hurt基础`reduce_shield=100000`后`damage_ship=120`，另存ldpaidarmor／ld031armor。必须原生SAV盾为0且非负、armor真实下降、Mother仍存活并保持其它不变量后，才能作为完整三层before。负repair本轮暂不执行；所有失败hurt保留。原生导出／恢复接口的支持与UNKNOWN边界另见[三防接口调查](legacy-health-export-restoration-1019.md)，没有修改生产实现。

### Predeclared cross-version damage policy

Before creating either old damaged fixture, select fraction preservation for hull, armor and shield across old-source damaged → RC4 load → sync → reload; absolute ratio tolerance 0.000001, relative tolerance zero. Automatic healing or a mode change chosen from observed results is a failure. Queue, identity, date and population checks remain independent.

### Armor prerequisite after the first real damage observation

ld031hurt preserves the initial attempted three-layer probe: hull lost 1000, shield lost 620, armor unchanged. This is not three-layer coverage. Before trying undocumented negative repair, prefer a second independent native damage probe: retain that SAV as recovery point, reduce only shield by 100000 (both original fixtures have less than this maximum), then damage_ship=120, paused on the same date; save separate ld031armor / ldpaidarmor. The effect is documented to reduce shield alone; actual native SAV must show nonnegative zero shield, surviving hull and actual armor loss, with unchanged queues/resources/population/identity. Do not infer armor damage from parsing. If successful these separate armor SAVs, not the failed hurt attempts, become the migration before inputs. No production modification or acceptance-threshold change.

### Paid-queue first probe: observed armor prerequisite failure

Native `ldpaidclean` SHA256 `5290bdd14f078a5b3b75902bb9231a94dce793ae8363e65066a5e235cd7f2360` and `ldpaidhurt` SHA256 `fa0bceedd33ef8957bf200d8ccd97cdde23cbf2e43f2984099f891ae22eb21a0` are both dated 2200.01.12 under the public 0.3.1 tree `abca9b4195a991d98ca25336ed7807e0306d30e2c33021e4d307f78e1db864d8`. The original paid queue came from the 0.3.0-rc.1 `j13ten` fixture, but these two newly saved files were produced by public 0.3.1.

Actual hull is 101460 → 100460, armor stays 24429.6, and shield is 48370.608 → 47750.608. This again fails the three-layer fixture requirement. Fleet 146, ship 822, attached starbase 13, queue 54, every owned ship ID, position, queue item, paid cost, progress, population/layout and stock remain unchanged in the damage pair. Relative to original j13ten, all 11 paid items still have 81 alloys each, items 0–9 remain 10/60 and item 10 remains 0/60; original Mother design index 1725 became 1837 during native load, while its definition body SHA and complete slot/component shape are identical. Preserve that raw difference rather than treating an index renumbering as a component change.

The independent first-probe report will retain its armor FAIL and the full strict comparison. The separate zero-shield armor probe remains pending until its own immutable receipt and audit exist. No checker policy, tolerance or production source changes are needed for this observation.

### Partial shield needed for the cross-version ratio check

The separate zero-shield armor probe isolates armor damage, but a shield fraction of zero cannot detect whether a changed maximum preserves a nonzero shield ratio. After confirming ld031armor/ldpaidarmor, use documented positive repair_shield_amount=20000 while paused, save separate ld031partial/ldpaidpartial, and require all three currents positive and below maxima with the same armor/hull damage. Only successful partial SAVs become final cross-version before inputs; the zero-shield and first failed-armor probes remain unchanged. This deliberate fixture-only partial restoration changes no resource/queue/date and adds no production healing behavior. Fraction tolerance remains the previously declared 0.000001.

### Actual paid armor probe and omitted current-shield field

`ldpaidarmor` is now a completed native save, SHA256 `4391254b50c1e1fabe975dbcaf9bf30caf0d17ece14bb8d8e9ff8b2c63c67373`, dated 2200.01.12. Hull remains 100460 and armor decreases from 24429.6 to 24309.6, an actual additional 120 armor damage. All three stored maxima remain unchanged. The native ship record omits `shield_hitpoints` entirely and adds `shield_recharge_time=20`; `max_shield_hitpoints=48370.608` remains present. Record this as a missing serialized field rather than inventing an explicit raw zero. It is consistent with the submitted shield depletion command and damage reaching armor. The subsequent separate positive shield repair should provide a stored positive current for the final ratio fixture.

The existing `damage_readings` helper rejects the omitted shield current with `ValueError: native current/maximum defense missing: shield`. Keep that diagnostic; do not weaken the checker or synthesize a native value to make this intermediate probe pass. Its observation/report can still compare the complete raw records, queues, construction items, stocks, population and design. Final migration uses only the later genuinely partial three-layer fixture with all numeric native currents present. The primary paid hurt report is stable at 27/28 checks, armor FAIL, SHA256 `c7ebfffb325e8a1b3440d1cebb056b1a96a40fab7ea11e3d7f23f23eed3ea165`.

### Native load recovery and final fixture names

The attempted native load of `ld031hurt` failed when OCR read its initial lowercase l as uppercase I; it produced no `ld031armor` save. Preserve the failed input/OCR trail and do not claim that intermediate public armor SAV exists. The parent prepared byte-identical aliases `src031hurt` and `srcpaidarmor`, bound in the run's `partial-source-aliases.json`. Independent reads confirm both original and alias SHA256 equal `f2d2742aa321b43ec153aa56fd210bce5f3c3828518e4fc63be3987d37f18ebd` and `4391254b50c1e1fabe975dbcaf9bf30caf0d17ece14bb8d8e9ff8b2c63c67373`, respectively. These aliases change only native menu selection names, not save bytes.

The final planned native outputs are now `p031before` and `ppaidbefore`. On the public source, combine the positive shield-depletion/armor-damage/partial-shield-repair operations after loading the actual first hurt SAV. On the paid source, load the already observed armor SAV and perform only the positive shield repair. Both final outputs must independently show hull loss1000, armor loss120, shield current20000 with all three currents positive and below unchanged maxima. Compare the public final output to its actual hurt ancestor, and the paid output to its actual armor ancestor; both must preserve all identities, position, queue payments/progress, population, stock and native date. No final output or cross-version PASS is asserted before its own completed native receipt/audit and raw data exist.

### Completed public 0.3.1 partial fixture

`p031before` is complete with native audit/receipt, dated 2200.01.01, SHA256 `d5921823d723d4eb0dec5d912ae0e586aac5b903643472d44062229b66b0b1e2`. Its actual current/max values are hull 92960/93960, armor 24309.6/24429.6 and shield 20000/48370.608. All three layers have positive partial damage. The frozen predeclared fractions are respectively 0.9893571732652192, 0.9950879261224089 and 0.4134742321204646. Its source is the actual public 0.3.1 tree, not a new-version in-memory fixture.

Compared with its real `ld031hurt` ancestor, all queue/paid-item records, fleet128/ship1008/starbase15/queue50, ship inventory, coordinates, population groups/jobs, colony layout, stock and EEP variables remain unchanged. Native reload renumbers the Mother design index1559→1575 and a control design, with identical complete Mother definition body and component/slot shape. The raw strict comparison retains all 26 differences including these indices and cached military power refresh. Keep strict FAIL separate from the scoped fixture qualification. Create a new pending migration template that binds this genuine before path/SHA and all three observed fractions; leave RC4 loaded/sync/reload paths null until their own native receipts exist. The paid final fixture is still pending at this point.

### Completed paid partial fixture

`ppaidbefore` is complete with native audit/receipt, dated 2200.01.12, SHA256 `40c8f8dac9530594d501143132d55fef1205346d7f679f16c8858058ed392ff1`. Actual hull is 100460/101460 (fraction0.9901438990735265), armor24309.6/24429.6 (fraction0.9950879261224089), shield20000/48370.608 (fraction0.4134742321204646). All three currents are positive and below maxima; actual hull/armor currents remain identical to the proven `ldpaidarmor` ancestor. The source is public0.3.1. Only the original queue provenance is 0.3.0-rc.1.

All 11 originally paid queue items, costs, progress, orbitable, design shape, identity, coordinates, ship inventory, stock, population/jobs/layout and EEP variables remain unchanged. The native load renumbers the Mother design1837→1851 with identical body/shape; the strict ancestor→final comparison retains20 differences. Record separate fixture qualification and a new paid v2 pending template bound to this before path/SHA/fractions. Both final before fixtures are now available; neither has yet provided RC4 load/sync/reload evidence. The checker remains unchanged, including its explicit refusal to invent a missing current-shield value for the intermediate zero-shield SAV.

### RC4 cross-version execution plan, run 20261019T133314Z

The parent stopped public0.3.1 and started an independent RC4 run `20261019T133314Z`, source tree `06485dc540a88b30cef15c27c323ff21cd88f04ad57b79e4f5bc0590937ef468`, 59 files, single production Mod, simplified Chinese. The test preset's ruler gender change is outside that production tree and separately bound by manifest SHA256 `4ce9d9217a7ed804776a41e8ac73410bd70d5073bc3379aa55c2c46181938646`. The run's `candidate-phase-b-imports.json` binds raw-byte aliases. Independent reads verified `mig031src` and `migpaidsrc` equal the genuine old `p031before` and `ppaidbefore` SHA values; the restart/cancel source aliases were also byte verified. No imported SAV is edited.

Public-case order is paused same-day `m031load` before any explicit manual sync, then the separately recorded `effect root={eep_sync_mothership=yes}` and `m031sync`, then a real native load of the sync SAV and `m031reload`. Inspect only completed SAV/audit/receipt triples. For every stage compare to the genuine old-source `p031before`, keeping hull/armor/shield fraction tolerance0.000001 and rel0; also compare adjacent stages to locate the first divergence. Run the unchanged existing migration checker when sync/reload inputs exist. Keep all strict differences and all failed stage/checker reports. Native load behavior is observed rather than inferred from on_game_start_country or static sources. The paid case follows independently with original11 paid queue records. No future stage is prefilled or passed.

### First RC4 load: shield fraction FAIL at the predeclared tolerance

Completed native `m031load` SHA256 `5c6fd6b0f36eca37c63963c6af5ca56e86638864ac172bf6f08827a29adb091e` is dated2200.01.01 before the manual sync. Hull92960/93960 and armor24309.6/24429.6 remain identical. Shield becomes25542.52272/61776, whose ratio is exactly0.41347. The genuine old-before ratio20000/48370.608 is0.4134742321204646; the difference is -0.000004232120464575662. This exceeds the previously declared absolute ratio tolerance0.000001 and must remain a failed shield-preservation result. Do not adjust that threshold or retrofit a passing report. The observed ratio is consistent with a five-decimal quantization, but one pair does not establish an undocumented closed-source engine algorithm.

The old component/section design shape and body remain unchanged during this load; its design index is renumbered. Same-key static modifier source changes can explain a different maximum context, but they do not excuse the measured ratio mismatch. All identities, queues/items, coordinates, population/jobs/layout, stock and country EEP ledger remain unchanged; no new evolution modifier is present at this stage. Keep the complete21 strict differences alongside a separate stage report with per-layer ratios. Later sync/reload must still be inspected against the genuine old before rather than replacing this failed baseline with the already changed loaded state.

### Raw normalized-ratio investigation and explicit-sync observation

Independently reopening both native ZIPs and extracting the complete `ships.1008` block reproduces each observation's raw block exactly. Both ship blocks have28 top-level fields. Neither contains another named hull/armor/shield normalized ratio, health percentage or health state block. Actual old fields are `hitpoints=92960`, `shield_hitpoints=20000`, `armor_hitpoints=24309.6`, `max_hitpoints=93960`, `max_shield_hitpoints=48370.608`, `max_armor_hitpoints=24429.6`; the loaded block changes only shield current/max among those six. Both have `shield_recharge_time=20`. Old gamestate SHA256 `6341d38d13f31546253a73891405d40810e11ec699d76e1a72e42e077a06ef8f`; loaded gamestate SHA256 `6610154d813c8aea8ff7dfb2f42f2ba40297b9d05dbd965c7b23703702b460f4`. Preserve complete blocks, field names and context in a separate raw-source report. This cannot certify that the old native SAV already stored a canonical0.41347 field, nor expose unsaved engine-internal representations. Do not conclude this is a Mod healing bug.

Completed `m031sync` SHA256 `2b62a53aaa8326ecc6b3a6d3c4a7e45dafa65e9ab48d182efabd77fb30a12ceb`, sameJan1, installs the new Mother design. Hull92960/93960 stays identical. Armor44567.245/44787.6 gives ratio0.9950799998213792, a -0.000007926301029748117 difference from the genuine old before; shield69177.6657/167310 remains0.41347 with the already observed -0.000004232120464575662 old-before difference. Thus both armor and shield fail the original1e-6 ratio policy after sync. All queue records, identity, position, population/jobs/worlds and stock remain intact; C/G/D/made/worlds remain0/0/2/0/0 while zero-valued component and level mirrors are initialized. Preserve strict old-before→sync69 and load→sync63 differences. Reload is still pending at this observation; neither absence of full healing nor apparent decimal truncation changes the original failed ratio checks.

### Completed public reload: design reference differs from entity section

`m031reload`, SHA256 `dddc4a2f300c4d14e5bc4326d97da3d85d3629f041f229104fef925cfccf8a17`, remainsJan1. Hull92960/93960 is unchanged. Armor24309.16207/24429.6 has fraction0.995069999918132, a -0.000017926204276874635 difference from the old before and an additional -0.000009999903247126518 from sync. Shield25542.52272/61776 remains0.41347. Retain both original-policy armor/shield FAILs.

The ship's `ship_design_implementation.design` is1608, whose actual top-level `ship_design.1608` body is the old Mother name/configuration SHA256 `2e2b4a1f0e9d1d990334152808d280abad6175b9ab7ed1997549773ccfffabb0`. The new global design1592 and its `_1019` cache binding remain in the same SAV. The ship's own runtime `section.design` is still `eep_mothership_section_1019`, and its `eep_mothership_design_1019` flag, fleet six component levels/reward/applied-level variables and country mirrors all persist from sync. Thus distinguish the reverted referenced-design table/configuration and defense maxima from the still-new entity section/flag. Do not claim that every entity field reverted, or that the target was simply an old source mistakenly loaded. Raw design IDs have no duplicate keys in either table.

The actual GPU load-window image places the genuine `m031sync` list row at x530..959/y357..395; recorded click822,382 lies inside that row's filename, while `m031load` is the next row at y398..435. This is a real list row, not hover-tooltip text. No independent image after the row click and before Load exists; retain that limit. The native-load receipt binds history/m031sync to SHA2b62a53a... and explicitly leaves `state_verified=false`; the newly saved reload's sync-only state provides additional evidence. Preserve strict sync→reload31, old-before→reload61, and load→reload comparisons unchanged. The original-policy complete-case report must remain FAIL; source/API investigation is separate and production/checker/threshold remain unchanged.

### Independent paid-queue chain reproduces both original-policy failures

Native `mpaidload` SHA256 `52a6cff2ee681bfab7ea2eefd142525c571b6fac9b8a728bd8bd6759487f6839`, `mpaidsync` SHA256 `e41db7f200fd6074bce40685fda29db5d80f53a0fea6bd032d137b6d4c787948`, and `mpaidreload` SHA256 `5d1ca99d708c60c18cf273bb83aa583efbbf715214cd5b9d0b155e0253f0b070` are all2200.01.12 under the same frozen RC4 source. Hull100460/101460 remains constant. Armor values exactly repeat the public chain:24309.6/24429.6 on load,44567.245/44787.6 after sync,24309.16207/24429.6 after reload. Shield values likewise repeat25542.52272/61776,69177.6657/167310,25542.52272/61776. Relative to genuine `ppaidbefore`, the original1e-6 policy therefore fails shield on load and armor/shield after sync/reload.

The new design1866 is installed by sync; reload references old Mother design1880 while preserving entity section`eep_mothership_section_1019` and the migration flag. All original11 already paid construction items retain their complete normalized payment/progress/queued-design/orbitable records at every stage; all queue IDs, ship identities/position, population/jobs/layout and stock remain unchanged. Keep all strict differences: old-before→load21, old-before→sync69, old-before→reload61. Produce a separate actual paid complete case and run the unchanged checker, with raw registry/reference/flag evidence and per-stage damage deltas. This independent reproduction supports the observation, not an unproven engine algorithm or a modified acceptance policy. Public complete checker report remains original-policy FAIL (32checks,30true), SHA256 `7541f5a8e4d07c8078f6b2da081a2ceeb17b324415f33f92321b6285a52822e9`; public six-pair series report SHA256 `a558ed74c66d17a1a8dade1da2c9952c67c8b6dd9041a1db6e5e5e264254118c`.

### Migration warning log snapshot and source-scope review

The still-active RC4 run's error.log contains native unset-variable warnings at21:37:54 for the public sync and21:46:01 for paid sync. Preserve a single read-bytes snapshot with explicit UTC observation time, byte count and SHA256, together with the frozen exact `eep_mothership_effects.txt` source and source-line excerpts. This is an observation of a live log, not a complete stopped-run freeze, and does not overwrite the original log or previous reports. A later full archive must retain these warnings as well as existing startup messages.

The reported lines include country reads of level at72 and146; fleet while37 reads `owner.eep_component_entitled`; owner-mirror53–59 reads `prev` fleet six component levels/rewards; country156–157 reads entitled/rewards. Source69–71 and76–78 already contain the preceding country set/divide/floor sequence; fleet6–31 contains explicit is_variable_set guards and zero setters before the owner mirror. Bind each full native stack and actual reported scope to these exact source lines. These observations do not by themselves establish whether variable lifetime, expression timing or another native mechanism causes the warnings. In particular, the logged locations are not simply the OR check_variable guard at135, and they do not prove why the design reference changes after reload. Leave production, checker and original fraction policy unchanged.

Direct native raw checks now confirm that public load lacks the new country/fleet variables, while both sync and reload explicitly serialize country `eep_mothership_level=0`, `eep_component_entitled=0`, `eep_component_rewards=0` and fleet `eep_applied_level=0`, all six component levels=0 and rewards=0. `inspect_1019` reads these blocks directly with audit_save.scalars, which only iterates existing scalar fields; `inspect_1015` uses the native audit and adds no EEP zero defaults. This rules out observer-generated zero values in these observations, and does not support a claim that all zero entries are removed from the final save. Execution-time availability remains unproven. Generated native effects docs explicitly permit numeric/variable/scope.variable operands for set_variable and distinguish clear_variable. Vanilla overlord effects297–317 use zero initialization followed by arithmetic/check/reference; other zero-initialization examples exist. Source conventions establish valid syntax, not why this particular native warning fires.

### Controlled country-registration probe also fails native persistence

Follow the separately predeclared [registration probe](mothership-design-registration-probe-1019.md), without altering production. `rdesignsync` SHA256 `c223bdb5ea8cacbb51a75af9b1358d6497add923b6e3b61a04ee2a0358f901f4` actually adds one country0 registered design1881 (13→14 entries), and ship822 references1881 with all50 slots,6 required components and six real AUX6–11 cores. This confirms that the create/add/set command executes the intended registration experiment.

`rdesignreload` SHA256 `d679d4b4bf2d66a2af9f9daa8e7b6a84f65db1d112b9df2c0e59f0c8e1a5788c`, sameJan12, retains country-registered1881 but ship822 references new1895 with the old29-slot/5-required-component Mother body and no six cores in that referenced design. Entity section/flag remain1019; armor/shield maxima again regress to24429.6/61776. All11 paid queue records, population/jobs/layout, stock, identities and location remain unchanged. Strict sync→reload31 is retained. Thus adding a country registration alone does not prove or fix persistence; the probe must report FAIL with distinct successful registration and failed implementation-reference checks. All previous fraction-policy failures remain untouched. Do not implement this three-effect chain as a claimed production fix based on registration success alone.

### Independent mobile-starbase implementation pointer

The complete associated `starbase_mgr.starbases` records contain their own nested `ship_design_implementation`, distinct from the actual ship record. Public sync points ships.1008 to new1592 while starbase15 still points to old1591; after reload both reference old1608. Paid sync points ship822 to new1866 while starbase13 retains old1865; reload points both to old1880. The registration probe likewise points ship822 to new registered1881 while starbase13 remains old1880; reload points both to old1895. Save all complete blocks, body hashes and referenced design table records, not only queue IDs or a normalized migration snapshot.

These starbase blocks otherwise contain only level`starbase_level_juggernaut`, build_queue49/53, shipyard_build_queue50/54, station1008/822, emptyorbitals and construction_type`starbase_shipyard`. There is no other global-design/name/template/size field in these records. Native starbase_levels/01_juggernauts.txt maps the level to ship_sizejuggernaut; native ship_sizes/18_juggernauts.txt defines shipclass_starbase, construction_type and ten shipyard capacity. These are source inputs, not proof of an undocumented load ordering. The observed dual implementation mismatch supports investigating mobile-starbase reconciliation; it does not yet prove a native causal algorithm or a valid API that updates both pointers. Preserve existing registration-only and fraction FAILs while the parent performs separate controlled probes.

### Controlled internal-name probe does not preserve the new design either

The parent's separately documented probe sets the actual ship design to the exact1019 key and changes only the ship's internal name key to the equivalent localized1019 alias. `rnamesync` SHA256 `503c50053cea010b43eca3b23536479d9b78f49fb383af5c703bae6bc623a56d`, Jan12, confirms ship.name.key`NAME_EEP_Baiqi_Mothership_1019` and implementation1866/new body, while starbase13 still points to old1895. `rnameload` SHA256 `c1c9b452a07c7d3f2b9da6d06a7f44dc5ca66ee7e219bf049b6e17b45831c21f`, sameJan12, preserves the new internal name key but ship and starbase implementations both reference old1909/body2e2b4a1f..., with armor/shield maxima24429.6/61776 again. Thus the intended name change actually persists but alone does not resolve design binding.

All11 paid queue records, identity/location, population/jobs/layout and stock remain intact; strict sync→reload31 is retained. Create a separate name-probe FAIL report with raw ship name, both implementations, actual collection and full loadout references; do not claim that the original raw name was preserved, that native reconciling order has been proven, or that the original fraction policy passed. Keep all prior registration-only, load/sync/reload and ratio FAIL reports unchanged.

The initial name-probe reportv1 used a literal-string equality test for the two localization values. All ten actual new values are the explicit `$NAME_EEP_Baiqi_Mothership$` reference, so that literal comparator incorrectly marked the static alias fact false. Preserve v1 and its exact bytes. A separate v2 report must resolve this exact single reference to the existing nonempty original entry and check each language independently; do not alter any SAV-derived design/core/persistence failures, numeric tolerances, Mod files or shared checker. This corrects the local analysis assertion rather than claiming a new runtime result. Non-Chinese aliases remain static-only evidence.

### Fleet-scope set_ship_design leaves the independent starbase pointer unchanged

The parent's next predeclared probe invokes set_ship_design directly in the bound fleet scope, rather than inside every_owned_ship. Completed `rfleetsync`, SHA256 `df1c501844f00823b979c0a064251fa091cab4716cbc0205034ae3cccb1e28c6`, remainsJan12. Actual ship822 implementation becomes1866/new1019 complete50-slot/6-required design with six real cores; actual starbase13 implementation remains1909/old Mother body. Thus the required dual-pointer agreement already fails in this single saved stage. Record FAIL without requiring another reload for this probe.

Hull100460/101460, armor44565.90138/44787.6 and shield69177.6657/167310 remain partial; original fraction-policy failures are unaffected. All original11 paid queue records, stock, population/jobs/layout, identities/location and country/fleet counters are preserved. Keep strict29 differences from its actual `rnameload` ancestor. This rules out the tested fleet-scope invocation as sufficient for dual-pointer synchronization; it does not establish unsupported starbase mutation syntax or an alternative production fix.

### Native list OCR recovery and efficient final partial sequence

ldpaidarmor actually loses 120 armor, but native omits the zero shield current field; retain this raw absence and do not fake zero. Generic native_load then refuses ld031hurt because the actual list OCR reads its initial lowercase l as capital I. Preserve that failure. Import byte-identical source aliases src031hurt and srcpaidarmor into the same isolated history folder, bind original SHA, close/reopen the native load dialog and use existing strict loader. Public branch may perform documented shield-clear, damage120 and positive shield repair20000 in one paused command then save p031before; the final actual armor decrease and all three positive damaged currents are required, no separate public zero-shield SAV is claimed. Paid branch loads its actual armor probe and repairs only shield20000 then saves ppaidbefore. This avoids a redundant public zero snapshot without weakening the final damage or queue contract; earlier initial hurt and paid zero-shield evidence remain immutable.
