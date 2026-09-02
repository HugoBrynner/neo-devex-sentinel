# Neo DevEx Sentinel — Release Impact Report

**Release:** `v3.8.1` → `v3.9.0`

**Detected:** 1 developer-facing changes — 1 high / 0 medium / 0 low

## HIGH — target_framework_changed — `Neo.SmartContract.Framework`

Source: `Neo.SmartContract.Framework.csproj`
- Before: `net9.0`
- After: `net10.0`
- Exact docs hits: `develop.md`
- Related docs hits: none
- Note: Runtime/framework requirement changed; docs mentioning the old runtime require review.
