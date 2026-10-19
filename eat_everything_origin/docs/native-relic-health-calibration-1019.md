# Native Relic health calibration

## Goal and fixed scope before execution

Observe a nonmobile native NAME_Relic ship's arithmetic current/max fractions and native fraction-trigger exports across the native same-body set_ship_design operation and actual reload. Production, all previous1e-6 policies/reports, shared checker and original SAVs remain unchanged. This calibration can establish a bounded observed native contract for one fixture/EXE/design; it cannot retroactively pass the failed Mother migrations or prove all engine-internal precision rules.

Reuse completed native r4relic6, run20261019T112808Z, dated2200.03.13, SHA256 `b067c749c7389dd830995aa8e1b14bdfae58ab10f8afa67c6cf4004e0ec70f81`. Its native audit/receipt and frozenRC4 source are verified. This is the already six-day-refreshed reference before later jump experiments, so no new reference spawn or calendar advancement is needed. Existing saved target `eep_relic_reference_1019` is fleet16777221, containing exactly ship16777223, owned by country0. Source fleet class is military; native design is NAME_Relic/npc_warship_01, with no attached mobile starbase. Source actual current/max values are hull20000/20000, armor30740/30740, shield138352.5/138352.5. These actual values, rather than a simplified aggregation formula, control the injury setup.

Only create an exclusive byte-identical import alias `nrelsrc.sav` in the current run's eep-test-history folder, with an explicit offline-copy receipt binding complete original SAV/audit/native receipt/manifest SHA provenance. This is not a native UI save receipt. Validate the old target and confirm no eep_test_health_h/a/s_before/set/load variables already exist; no source object is edited. Actual loading and all commands below belong exclusively to the parent UI workflow.

## Minimal native sequence

Keep country0 paused throughout. Load nrelsrc through the native UI. Use the existing exact fleet target, not every ship in the empire. Source shield exceeds100000, so use1000000 to deplete shield before the positive armor-damage probe. Do not use negative repairs.

1. Apply the following single command and save native `nrelbefore`.

```text
effect root={event_target:eep_relic_reference_1019={every_owned_ship={reduce_hp=1000 reduce_shield=1000000 damage_ship=120 repair_shield_amount=20000 export_trigger_value_to_variable={trigger=has_hp_percentage variable=eep_test_health_h_before rounded=no} export_trigger_value_to_variable={trigger=has_armor_percentage variable=eep_test_health_a_before rounded=no} export_trigger_value_to_variable={trigger=has_shield_percentage variable=eep_test_health_s_before rounded=no}}}}
```

2. Invoke the exact unchanged native design, export all three native getters again, save native `nrelset`.

```text
effect root={event_target:eep_relic_reference_1019={every_owned_ship={set_ship_design={design=NAME_Relic} export_trigger_value_to_variable={trigger=has_hp_percentage variable=eep_test_health_h_set rounded=no} export_trigger_value_to_variable={trigger=has_armor_percentage variable=eep_test_health_a_set rounded=no} export_trigger_value_to_variable={trigger=has_shield_percentage variable=eep_test_health_s_set rounded=no}}}}
```

3. Actually native-load nrelset. Export once more and save native `nrelload`.

```text
effect root={event_target:eep_relic_reference_1019={every_owned_ship={export_trigger_value_to_variable={trigger=has_hp_percentage variable=eep_test_health_h_load rounded=no} export_trigger_value_to_variable={trigger=has_armor_percentage variable=eep_test_health_a_load rounded=no} export_trigger_value_to_variable={trigger=has_shield_percentage variable=eep_test_health_s_load rounded=no}}}}
```

Do not advance time, repair any further, or inject resources. Require completed SAV/audit/immutable native receipt per stage. If the first SAV does not show all three native currents positive and below maxima, retain the failed fixture setup and stop inference from it.

## Independent analysis and acceptance boundaries

For every stage extract full original ship/fleet/design blocks and exact ship variables. Require the intended reference IDs, owner0, unchanged complete native43-slot/6-required design body/shape, nonmobile class and no starbase whose station is that ship. Compare native getters directly with arithmetic current/max for hull/armor/shield, using unrounded numeric source values; never manufacture an omitted export or replace its value with a computed fraction. Keep both channels and their exact deltas before→set→load. A native getter that differs from arithmetic current/max is evidence of that observed API result, not proof of a separately serialized canonical ratio or a universal truncation rule.

Keep Mother, all other owned ships, construction queues/payments/progress, positions, population/jobs/layout, stock and EEP settlement/growth ledgers fixed. Include the complete strict comparator output; intentional damage, exports and design-index renumbering remain visible. All original Mother fraction-policy and design-persistence FAILs remain unchanged. No new global tolerance may be chosen solely from these outcomes.

## Optional separate maximum-context branch

After the core three SAVs, the parent may add native `talon_power` directly to this reference ship, export new `_talon` getters and save `nreltalon`; do not contaminate the preceding same-design samples. Native19_static_modifiers_paragon.txt:8–12 defines additive hull5000/armor5000/shield2000; native paragon_events_3.txt:1445 applies it to the actual Talon ship. Record actual changed maxima rather than equating raw additive source values with a full aggregate formula. Modifier addition and design replacement are distinct native operations. An optional observed modifier branch cannot alone justify a universal design-setter precision policy. No talon branch is pre-marked as performed or passing.

## Native technical sources

Generated effects document export_trigger_value_to_variable (including rounded=no and ship scope), set_ship_design and the positive damage/repair effects. Generated triggers document has_hp_percentage, has_armor_percentage and has_shield_percentage; do not invent has_max_shield_hp. Native global_ship_designs/leviathans_designs.txt defines NAME_Relic; ship_sizes/11_leviathans.txt defines npc_warship_01 as shipclass_military. Source hashes/excerpts and the exact original target/ship/health context are bound in the import-source report. This document is an unexecuted plan until the parent's new native samples exist.

## Load-stage topbar/date-verification failure

The parent actually loaded nrelsrc but reported the complete resource/date topbar hidden while the rest of the Machine/Relic/system/paused interface remained visible. The native load helper therefore failed its date check; no injury or export command had yet executed. Preserve this failure and its actual GPU/OCR/action trail. Do not relax the helper or call the date check successful.

Independent raw source inspection finds the complete root player record `{ name="unknown" country=0 }`, meta2200.03.13/EEP03/Machine portrait, and country0 typedefault with normal owned fleet/reference data. There is no separately named observer/human-current-player field in the inspected source roots. `last_date_was_human="0.01.01"` is shared by all country records, so it is not evidence that only this country is an observer. Human1/-1 in event-selection history describes those recorded selections and is not a current-player binding. Leave the topbar causeUNKNOWN. A read at2026-10-19T14:29UTC found unchanged error.log7665bytes/SHA33375065... and game.log176bytes containing only version/define initialization, with no new logged load/render error. This is a live-log observation, not final freeze evidence or proof that no UI fault exists.

The parent may separately execute explicit native play0 to restore binding, then require a fresh actual date frame and a newly saved native baseline proving the intended source state. The observer does not execute UI or process actions and does not pre-certify that recovery. All later health stages remain pending until their own completed native receipts and raw fields exist.
