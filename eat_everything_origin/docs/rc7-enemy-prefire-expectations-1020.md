# RC7 enemy shot: expectations fixed before natural completion

## Goal, scope, design and acceptance

Before advancing the last native firing day, fix the settlement expectations
from the actual prefire SAV, the production formulas and the independently
restored crisis calibration. This is the existing enemy settlement test, not a
new fixture or production change. Any mismatch must fail for investigation;
do not infer other population changes from the after-minus-before residual.

## Actual prefire

`r7pkfireprefire.sav`, 2201.05.26, SHA256
`7ebbaff3d0af80b4e1adfffbdedc4a7c2065507bceb9d953292a66c570a52887`.
Fleet151/ship1044 has order2 for physical planet17, native fire29/fire_time30.
Source17 is pc_tundra, size21, owner1, colony1, population4966 and no
`d_lithoid_devastation`; core2 is pc_machine, owner0, colony0, population4877.
Global ground_combat is empty. Actor0 has C0/G0/D2/made0/L0 and six ranks0.

## Expected completion fixed now

q21, enemy founder return0, C21, G21, D7, cumulative manufactured300,
Mother L2 and no random rank reward (L<5). Core capacity multiplier changes
from2 to7. Expected other core-population delta is **0**, so core population
is expected to become **5177**. This zero is a pre-completion expectation:
prefire core groups have size/month_start_size2700/2700 and2177/2177,
empty current-month growth detail, and the transition May26 toMay27 is within
the same month. It is not fitted from any postfire result and is not asserted
as a general engine timing proof. Unexpected natural growth requires separate
evidence and a retained failure before revising a later test.

Independent calibration: one destroyed-world objective contributes750; one
destroyed-empire objective contributes600. Existing destroyed-enemy-ship
progress is separate and must not be counted as planet-killer reward.
Allow native last-colony country cleanup to stabilize before assessing the
empire objective. Then test duplicate callbacks and real reload without
another settlement. No postfire SAV has been created when fixing this plan.
