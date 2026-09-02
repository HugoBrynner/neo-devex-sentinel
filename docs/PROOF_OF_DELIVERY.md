# Proof of Delivery — v0.1.0

Neo DevEx Sentinel v0.1.0 is a working local CLI proof of concept for detecting developer-facing drift between Neo tooling snapshots and local documentation.

## Reproduce

From the repository root:

```bash
python -m unittest discover -s tests -v
```

Expected result for v0.1.0:

```text
Ran 5 tests
OK
```

Generate the included runtime-drift report:

```bash
python -m neo_sentinel scan \
  --old fixtures/runtime/old \
  --new fixtures/runtime/new \
  --docs fixtures/runtime/docs \
  --old-label v3.7.4 \
  --new-label v3.8.1 \
  --out out/runtime
```

Expected high-level result:

```text
changes=1 high=1 medium=0 low=0
```

Generate the multi-release drift report:

```bash
python -m neo_sentinel scan \
  --old fixtures/runtime-next/old \
  --new fixtures/runtime-next/new \
  --docs fixtures/runtime-next/docs \
  --old-label v3.8.1 \
  --new-label v3.9.0 \
  --out out/runtime-next
```

Expected high-level result:

```text
changes=1 high=1 medium=0 low=0
```

Generate the public-API report:

```bash
python -m neo_sentinel scan \
  --old fixtures/api/old \
  --new fixtures/api/new \
  --docs fixtures/api/docs \
  --old-label v3.10.0 \
  --new-label v3.10.1 \
  --out out/api
```

Expected v0.1 fixture result:

```text
changes=10 high=0 medium=9 low=1
```

## Source provenance

The Neo-derived fixture provenance, tags, paths, and recorded blob SHAs are listed in [`../fixtures/PROVENANCE.md`](../fixtures/PROVENANCE.md).

The `signature` fixture is explicitly synthetic and is used only to test signature-change pairing logic.
