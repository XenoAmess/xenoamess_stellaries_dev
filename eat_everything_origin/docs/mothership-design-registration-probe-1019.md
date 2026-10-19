# Controlled native design registration probe

## Goal, scope and acceptance before execution

RC4 public031 and paid migration samples preserve actual new entity sections, ship flag and zero-level mirrors but native reload points implementation to a newly copied old design body and old defense maxima. The new global design still exists in both registries; the player country design collection contains neither old nor new event design. Actual native load row/action and unique post-sync state exclude a simple old-file misload. These are observations, not a proven registration root cause. All original fraction tolerance 0.000001 failures remain.

After mpaidreload, while paused on 2200.01.12 in run133314Z, test the existing native APIs create_ship_design ? add_ship_design ? set_ship_design using last_created_design. Native generated effects document create at3240, country add at1146 and ship/fleet set at2575. Original grand_archive_effects9?17 and crisis effects4618?4622 use create/add; the exact three-effect chain is a controlled hypothesis, not already proven by those examples. Use exact production global key NAME_EEP_Baiqi_Mothership_1019, same bound Mother and original ship identity. No Mod/source/technology/flags/counter reset or SAV editing. The expected test-only side effect is one additional country-registered design.

Native save rdesignsync, actual native reload it, then save rdesignreload on the same date. Require country design collection really owns the new design object, actual implementation references its real 50-slot/6-core body, and new entity section, Mother IDs, all 11 paid queue records, stock, population, location and EEP ledgers remain unchanged across reload. Compare all native raw fields and retain differences. A flag alone does not pass; unchanged visible section with old referenced body fails. This probe certifies only registration/persistence if successful; it does not declare old damage fraction preservation, normal upkeep, economy or the complete Mod passed. Production changes require a separate documented design and fresh gate first.

Exact command:

```text
effect root={create_ship_design={design=NAME_EEP_Baiqi_Mothership_1019} add_ship_design=last_created_design event_target:eep_mothership@this={every_owned_ship={set_ship_design={design=last_created_design}}}}
```

Root web search used exact set_ship_design reload/save queries and forum.paradoxplaza.com / GitHub ship_design_implementation queries. Results were mainly mirrors of effect-introduction patch notes and did not establish persistence semantics; no secondary mirror is used as proof of a fix. Local native effect documentation and original source remain the probe syntax basis.

## Follow-up name-key binding probe before execution

Registration alone failed: country keeps new1881 but Mother again references old1895 after reload; all paid queues remain. Investigate event-ship name binding as a separate hypothesis. Actual Mother name key remains NAME_EEP_Baiqi_Mothership while its requested design is _1019; both old and new named global designs remain cached. All ten production localizations already define NAME_EEP_Baiqi_Mothership_1019 as the exact old-name alias, so changing only this fixture ship name key preserves its displayed localized name. Native set_name is documented for ship. On current rdesignreload, explicitly assign the new global design and then set ship name to its _1019 localized alias. Save rnamesync, real native reload, save rnamereLOAD (actual stage rnameload), same Jan12. Require actual new implementation/table/50slots/6cores/max defenses persist; country design collection/11 paid queues/resources/pop/identity/position/EEP unchanged. Record raw name-key change and all raw differences, do not claim raw-name equality or original health-policy PASS. No production changes yet. This tests binding only; it does not prove a general native mechanism or custom player-name behavior.

## Fleet-scope setter probe before execution

Independent native records now show starbase_mgr.starbases.13/15 keeps a separate ship_design_implementation pointing at the old body while ships.822/1008 points at the new body; reload aligns both to the old body. This identifies the state mismatch, not closed-source causality. After the name probe has completed, call the native documented set_ship_design directly on the bound fleet, without every_owned_ship. Supported fleet scope is documented at effects2575–2580; no original fleet-scope use was found, so this is still a controlled combination. Preserve the current name key and collection. Save only rfleetsync first on Jan12. Require BOTH actual ship and associated mobile-starbase implementations to reference new 50-slot/6-core body with unchanged IDs, 11 paid queue records, stock, population, location, EEP variables and flags. If starbase remains old, record failure immediately and do not waste an additional reload; only if both are new proceed to an independently documented reload check. No production change, unsupported starbase setter or starbase rebuilding.

`	ext
effect root={event_target:eep_mothership@this={set_ship_design={design=NAME_EEP_Baiqi_Mothership_1019}}}
`

## Same-size mobile-starbase probe before execution (22:16 local)

The fleet-scope sample rfleetsync failed its prerequisite: ship822 references new1866 while mobile starbase13 still references old1909. Do not reload that failed variant. Test the documented starbase effect `set_starbase_size=juggernaut` on the existing bound fleet's `starbase` scope, while paused on Jan12. The generated effects1850–1852 and scopes266–268 support this syntax; no native example proves that a same-size call rebuilds its design or preserves its paid queue. This is a controlled hypothesis, not an established fix. No source or save-file editing.

Exact command: `effect root={event_target:eep_mothership@this={starbase={set_starbase_size=juggernaut}}}`. Save rsizeonly first. Require actual ship and attached starbase IDs unchanged, both implementation bodies new50-slot/6-core, all11 paid queue records and native resources/pop/jobs/location/EEP ledger unchanged. Retain all absolute health differences and original fraction-policy failures. If both bodies are new, reload and save rsizeload; otherwise record this variant's failure without reload. If this effect overwrites the ship with an auto-generated body, a subsequent explicitly documented size-then-set sequence would be a separate probe and cannot be assumed successful.
