# Changelog

## [0.1.0-rc.1] - 2026-09-26

### Added

- Standalone Shishan Code origin, five-stage situation, repeatable society research projects, maintenance institute and jobs, machine-compatible reward traits, and Vivhite event chain with resurrection.
- Art assets and localisation for all ten supported languages.

### Changed

- Initial situation progress is now +5 per month. The Chinese origin text says “许多年前，创造者消失了”.
- Vivhite uses the revised V2 portrait with aligned hair ornaments and a static portrait texture in the leader UI; the A05 event art was regenerated from the V2 concept.
- Both machine government types now receive the intended starting trait budget change of 6 fewer points and 3 more selectable traits.
- Stage resource production now includes the independent monthly Trade resource; market orders remain separate from production.

### Fixed

- Vivhite's paid resurrection now preserves her level, traits, and current experience in the tested nonzero experience-gain case.
- Corrected the machine trait point modifier key used by individual machine empires.

### Compatibility

- Targets Stellaris 4.5.*. Steam publication is not part of this development build.

### Validation

- `open_kaishek` package-level static acceptance passed: 19 scripts, 13 DDS assets, and 164 localisation keys.
- The nine non-Chinese languages passed static checks; their runtime is outside the test scope.
- Simplified Chinese runtime checks passed for the revised portrait, both machine empire starts, the five situation stages and ship attribute values, maintenance project completion and cancellation, cleanup cancellation, reward-pool transitions, Trade and rare orbital source isolation, a Dyson Sphere production sample, tributary tax exclusion, and Vivhite's resurrection. The full scenario matrix remains incomplete.

### Known limitations

- Controlled combat damage, same-route travel time, commercial pact transfer exclusion, and long-range balance routes still require runtime checks. See `docs/shishan-code-origin-acceptance-report-2026-09-27.md`. This release candidate has not been uploaded to Steam.
