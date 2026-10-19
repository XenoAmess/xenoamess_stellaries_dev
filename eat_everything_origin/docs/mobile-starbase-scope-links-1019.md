# Native mobile-starbase scope links

## Goal and scope

Read-only source and native-SAV investigation of the Mother fleet/ship/mobile-starbase association. Do not operate UI, modify production, edit SAVs or infer an unsupported mutation API. Native runtime expression tests, if any, belong to the parent's separately documented probes.

## Exact supported native links

Run20261019T133314Z generated `scopes.log` documents:

- Lines266–268: `starbase` scopes an object to its starbase; accepted inputs include ship and fleet, output starbase.
- Lines94–96: `ship` scopes a starbase to its station ship; output ship.
- Lines58–60: `fleet` accepts ship and starbase and outputs fleet.
- Lines338–340: `space_owner` outputs country. Lines334–336: `solar_system` outputs galactic_object. Neither is an attached-starbase link.

Therefore the documented paths from an already bound Mother are `event_target:eep_mothership@this = { starbase = { ... } }` in country scope, or the more explicit existing-owned-ship traversal below. The native Arkship setup in `common/scripted_effects/nomads_effects.txt:321–327` uses `starbase` directly inside create_ship.effect to configure its mobile modules, giving a native positive source example for the ship path.

```text
effect root={event_target:eep_mothership@this={every_owned_ship={starbase={if={limit={ship={is_same_value=prevprev}} <CONTROLLED_STARBASE_EFFECT>}}}}}
```

This is a scope template, not an executable command while the placeholder remains. At the guard's nested `ship`, `prevprev` is the original Mother ship: original ship → starbase → station ship. The guard checks the round trip before any optional controlled effect. Do not substitute the system's central starbase or a space-owner country. Source support and raw associations do not, by themselves, certify an executed round-trip probe.

## Actual raw association

| Fixture | Fleet ship member | Ship fleet field | Mobile starbase station field | Native shipyard |
| --- | --- | --- | --- | --- |
| public031 | fleet128 → ship1008 | ships1008.fleet128 | starbase15.station1008 | queue50, build49 |
| paid | fleet146 → ship822 | ships822.fleet146 | starbase13.station822 | queue54, build53 |

All relevant bases have level`starbase_level_juggernaut` and construction_type`starbase_shipyard`. They also serialize an independent `ship_design_implementation`, whose mismatch with the ship implementation is preserved in [the raw source report](evidence/1019-analysis/rc4-mobile-starbase-design-pointer-source-v1.json). Native starbase level source maps to ship_sizejuggernaut; native juggernaut is classshipclass_starbase. Do not reduce this association to queue IDs alone.

## Observed same-level size probe

The parent invoked fleet.starbase.set_starbase_size with the existing juggernaut level, without production changes. Completed `rsizeonly` SHA256 `715a8a4d168052ac06cb8867b0394ecac757c6bfd5b189bcf606dbc2b7e66678`, dated2200.01.12, changes ship822 implementation from new1866 to old1909, matching the existing starbase13 implementation1909. The starbase's complete raw block itself remains unchanged. The actual referenced design becomes the old29-slot/5-required Mother with no six adaptive cores. Thus agreement is old-payload agreement and cannot pass new-loadout persistence.

All original11 paid queue records, ship/fleet/base/queue IDs, location, population/jobs/layout and stock remain unchanged. Strict29 differences are retained. This is direct evidence that this controlled size invocation affects the station ship's design state before reload; it does not establish engine load ordering or a valid API to install a different saved mobile-starbase design. Keep the earlier fraction, registration, name and fleet-scope FAILs unchanged.

## Evidence requirements

Preserve source SHA/excerpts, raw linked fleet/ship/base records and their hashes, actual command action, SAV/audit/receipt provenance and complete strict comparison in a new source/probe report. An observed starbase link or size effect does not authorize production changes or a migration PASS.
