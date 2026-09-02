# Fixture provenance

Minimal excerpts only; these are test fixtures, not vendored repositories.

- `runtime/old`: neo-project/neo-devpack-dotnet `v3.7.4`, `src/Neo.SmartContract.Framework/Neo.SmartContract.Framework.csproj`, GitHub blob SHA `f661df4addee680d1b57acfa2bcc2a3a39e21484`.
- `runtime/new`: same path at `v3.8.1`, blob SHA `6d213d9e7cb38298f0b56a1731f8aacf17d1b17c`.
- `runtime/docs/develop.md`: neo-project/neo-dev-portal `master`, `docs/n3/gettingstarted/develop.md`, blob SHA `6d15afd6d452b9c520b5bb9bf379af0a1bbe7b5f`.
- `api/new`: public declarations from neo-devpack-dotnet `v3.10.1`: `AccessControl`, `Ownable2Step`, `PausableOwnable`, `RoyaltyNep11Token`.
- `api/docs/nep11.md`: Neo Dev Portal NEP-11 page excerpt, blob SHA `0185d67d7336741f8a5572ec419139a73b4ecfd0`.
- `runtime-next/old`: v3.8.1 `net9.0`; `runtime-next/new`: v3.9.0 `net10.0`. Current docs fixture intentionally remains `.NET 8.0` to verify multi-release lag detection.
- `signature`: synthetic fixture for testing signature-pairing logic only; it is not claimed as a tagged Neo release fixture.
