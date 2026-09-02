# Neo DevEx Sentinel

**Neo DevEx Sentinel** is a local compatibility and documentation-drift checker for Neo developers and maintainers.

It compares two local snapshots of Neo developer tooling, identifies developer-facing changes, and maps those changes to local documentation so developers can quickly review what may be outdated after an SDK/framework update.

> Status: **v0.1 proof of concept — built and tested.** The current C# API extractor is intentionally heuristic; it is not presented as a complete .NET compatibility analyzer.

## Why this exists

Neo tooling evolves across framework, compiler, SDK, templates, and documentation. A developer can update one part of the stack while local setup instructions, examples, or API references still describe an older environment.

Sentinel turns that drift into an explicit review report.

## What v0.1 detects

- `.csproj` `TargetFramework` changes.
- Documentation that still references an older .NET runtime after a framework change.
- Added and removed public C# types.
- Added, removed, and changed public C# method signatures using a lightweight heuristic parser.
- Exact and related documentation references for changed API symbols.
- Severity-ranked Markdown and JSON reports.

## Quick start

Requirements: Python 3.10+.

```bash
python -m pip install -e .
```

Run a scan against local snapshots:

```bash
neo-sentinel scan \
  --old fixtures/runtime/old \
  --new fixtures/runtime/new \
  --docs fixtures/runtime/docs \
  --old-label v3.7.4 \
  --new-label v3.8.1 \
  --out out/runtime
```

The command writes:

```text
out/runtime/release-impact.md
out/runtime/release-impact.json
```

You can also run it without installing the console script:

```bash
python -m neo_sentinel scan \
  --old fixtures/api/old \
  --new fixtures/api/new \
  --docs fixtures/api/docs \
  --old-label v3.10.0 \
  --new-label v3.10.1 \
  --out out/api
```

## Verified Neo cases included

The repository contains minimal test fixtures derived from real Neo sources. Provenance is recorded in [`fixtures/PROVENANCE.md`](fixtures/PROVENANCE.md).

### Runtime drift

The included fixtures reproduce this progression in `neo-project/neo-devpack-dotnet`:

- `v3.7.4`: `net8.0`
- `v3.8.1`: `net9.0`
- `v3.9.0`: `net10.0`

The current-doc fixture still references `.NET 8.0`, allowing Sentinel to verify both a one-release drift and a multi-release lag.

Example reports:

- [`v3.7.4 → v3.8.1`](examples/reports/runtime/release-impact.md)
- [`v3.8.1 → v3.9.0`](examples/reports/runtime-next/release-impact.md)

### Public API surface

The `v3.10.0 → v3.10.1` fixture verifies detection of newly exposed public framework types such as `AccessControl`, `Ownable2Step`, `PausableOwnable`, and `RoyaltyNep11Token`, then maps them against a Neo Dev Portal excerpt.

- [`v3.10.0 → v3.10.1 report`](examples/reports/api/release-impact.md)

## Tests

```bash
python -m unittest discover -s tests -v
```

v0.1 currently includes tests for:

- runtime drift mapped to docs;
- multi-release runtime lag;
- newly added public types;
- paired public method signature changes;
- Markdown/JSON report generation.

## Design

```text
old local snapshot ─┐
                    ├─> change extraction ─> docs mapping ─> severity ─> report.md / report.json
new local snapshot ─┘
                            ^
local docs ─────────────────┘
```

The tool intentionally works on **local snapshots**. It does not require automatic GitHub downloading to be useful: a Neo developer or maintainer can point it at the versions and documentation they are already working with.

## Current limitations

- C# parsing uses a deliberately small regex-based extractor rather than Roslyn or assembly metadata.
- v0.1 is an impact/review detector; a flagged documentation page is not automatically asserted to be wrong.
- The checked-in Neo fixtures are minimal excerpts for reproducible tests, not full vendored repositories.
- v0.1 does not automatically patch documentation.

These limitations are deliberate so the proof of concept remains small, auditable, and reproducible.

## Proof of delivery

The v0.1 repository contains:

- working CLI source;
- five automated tests;
- reproducible Neo-derived fixtures with source provenance;
- generated Markdown and JSON example reports;
- Apache-2.0 licensing.

See [`docs/PROOF_OF_DELIVERY.md`](docs/PROOF_OF_DELIVERY.md) for the exact verification commands and results expected from this release.

## License

Apache License 2.0. See [`LICENSE`](LICENSE).
