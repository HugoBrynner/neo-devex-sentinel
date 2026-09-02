# COZ Proof of Working — Submission Draft

## Contribution

**Neo DevEx Sentinel v0.1.0** — a local compatibility and documentation-drift checker for Neo developers and maintainers.

The tool compares two local Neo tooling snapshots, detects developer-facing changes such as target-framework drift and public API changes, maps those changes to local documentation, and generates severity-ranked Markdown and JSON impact reports.

## Proof of delivery

Repository: `<PUBLIC_GITHUB_REPOSITORY_URL>`

Release / commit: `<PUBLIC_COMMIT_OR_RELEASE_URL>`

Reproduction instructions: `docs/PROOF_OF_DELIVERY.md`

Included evidence:

- CLI source and packaging metadata;
- five automated tests;
- Neo-derived test fixtures with recorded provenance;
- generated reports for real Neo version transitions;
- Apache License 2.0.

## Verified examples

- Neo DevPack framework target drift: `v3.7.4 (net8.0) → v3.8.1 (net9.0)` mapped against docs still referencing `.NET 8.0`.
- Multi-release lag: `v3.8.1 (net9.0) → v3.9.0 (net10.0)` while the docs fixture still references `.NET 8.0`.
- Public API additions represented from `v3.10.0 → v3.10.1`, including `AccessControl`, `Ownable2Step`, `PausableOwnable`, and `RoyaltyNep11Token`.

## Scope honesty

v0.1 is a tested proof of concept, not a complete .NET binary-compatibility analyzer. The C# API extractor is intentionally heuristic and flagged docs are review candidates rather than automatically asserted defects.

## License

Apache License 2.0.

## Award address

`<NEO_AWARD_ADDRESS>`
