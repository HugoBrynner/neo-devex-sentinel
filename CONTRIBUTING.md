# Contributing

Contributions are welcome.

## Development

Use Python 3.10 or later.

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
```

Please keep changes focused and add or update a reproducible test fixture for detector behavior changes.

## Fixture policy

Do not vendor full third-party repositories. Keep fixtures minimal and record their origin in `fixtures/PROVENANCE.md` when they are derived from public Neo sources.

## Licensing

By contributing, you agree that your contribution is licensed under the Apache License 2.0 used by this project.
