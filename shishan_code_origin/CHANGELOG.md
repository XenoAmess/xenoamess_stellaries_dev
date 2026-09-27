# Changelog

## [0.1.0-rc.1] - 2026-09-26

### Added

- Standalone Shishan Code origin, five-stage situation, repeatable society research projects, maintenance institute and jobs, machine-compatible reward traits, and Vivhite event chain with resurrection.
- Art assets and localisation for all ten supported languages.

### Changed

- Initial situation progress is now +5 per month. The Chinese origin text says “许多年前，创造者消失了”.
- Vivhite uses the revised V2 portrait with aligned hair ornaments and a static portrait texture in the leader UI; the A05 event art was regenerated from the V2 concept.

### Fixed

- Vivhite's paid resurrection now preserves her level, traits, and current experience in the tested nonzero experience-gain case.

### Compatibility

- Targets Stellaris 4.5.*. Steam publication is not part of this development build.

### Validation

- `open_kaishek` package-level static acceptance passed: 19 scripts, 13 DDS assets, and 160 localisation keys.
- The nine non-Chinese languages passed static checks; their runtime is outside the test scope.
- Simplified Chinese runtime checks passed for portrait display, partial situation progression, one maintenance completion, and Vivhite's resurrection. The full scenario matrix remains incomplete.

### Known limitations

- The host currently stalls before the Stellaris main menu even with no mods. Resource-source isolation, later project and reward branches, exact stage boundaries, and the remaining runtime matrix still require testing. See `docs/shishan-code-origin-acceptance-report-2026-09-27.md`.
