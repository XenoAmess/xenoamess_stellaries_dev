# RC7 long fast-forward: premature native save

## Goal, scope, design and acceptance

On 2026-10-20, continue the existing native planet-killer test without changing
production code, save bytes or acceptance rules. Observe the actual HUD date with
the existing `runtime_1015.wait_for_native_date` before opening the save menu after
a long fast-forward. Re-read native order counters at every phase boundary.
Do not submit additional fast-forward days until the current command's actual
completion and current date have been observed.

## Observed failed attempt

From `r7pkfirewind1` (2201.01.28, windup 1/90), root issued `fast_forward 88`
but opened the native save menu before observing completion. The attempted
`r7pkfirewind89.sav` actually contains **2201.03.22, windup 55/90**.
The existing save helper correctly rejected the expected-date mismatch, before
writing a native-save receipt. Its bytes and UI/actions/audit must remain intact.

Actual attempted SAV SHA256:
`784a0b3b9f38c4887713b5ea8e20099c7b2fc042cdd3f480e53b437b150b26bd`.

This file is diagnostic evidence, not a successful windup-89 role. Resume by
observing the current screen and date, closing the observed save/menu overlay,
then waiting for the original target 2201.04.26 if the command is still active.
If it has stopped earlier, calculate the remaining days from actual date and
native windup, and issue only that remainder. Use a new unique save name for
the actual boundary; never overwrite this attempt or synthesize its receipt.

Acceptance: actual HUD target date observed before saving; fresh native SAV
date and windup both match; failed attempt retained; subsequent fire boundaries
continue to use native counters rather than filenames or inferred timing.

## Recovery observation

After clicking the observed native Restore Game control and closing the visibly
open console, the existing date waiter observed 2201.03.22 in three separate
GPU/OCR frames over its 45-second interval and timed out for 2201.04.26.
No remaining date progression was observed. Root then issued only the actual
remaining **34 days**, with the existing HUD-date waiter before any save-menu
action. The intended successful boundary uses `r7pkfirewind89v2`, a new name.
Its result remains pending until both the native date and order are checked.

## Verified boundary

The existing HUD waiter observed 2201.04.26 on its second capture. The new native
`r7pkfirewind89v2.sav` has that same date and SHA256
`34fa1d3f632d60e80fb9ce960bbe49b395b9efe2498a69fc5f7da016213d5f6a`.
Root independently parsed its original ZIP: fleet151 has a reachable
`destroy_planet_order` for planet17, order_id2, with actual windup **89/90**.
This correct role does not replace or relabel the failed 55/90 attempt.
The next one-day phase also uses an observed HUD-date gate before native save.
