# Stella V5 — Source review package (verified fixes included)

This is a **trimmed source-review snapshot**, not a runnable, tested production distribution.
It starts from the October 29, 2026 Stella V5 review archive and incorporates four focused, source-verified audit repairs. See [docs/VERIFIED_PATCHES.md](docs/VERIFIED_PATCHES.md) for details.

## Included
- Python application code (`mako/`), including prompts, voice, Discord, memory/RMA, and Great Sage.
- App entrypoints (`main.py`, `Mako.pyw`), backend prototype, Electron avatar **source** files, and dependency manifests.
- Source-level unit/regression tests and technical architecture documents.
- Public-safe example configuration without real credentials.

## Intentionally excluded
- Private Discord calls, runtime memory, user data, account databases and logs.
- Voice recordings, avatar models, animation clips, image/audio assets, node_modules, caches, and bundled tools.
- Compiled recovery bytecode and stale/bulk diagnostics.

## Known source mismatch — important
The supplied `mako/dialogue.py` source predates its newer October 29 compiled Python artifact. The current production behavior of that module **cannot** be established from this source snapshot, and some tests expect interfaces not present in it. The compiled artifact is not included. **Do not copy this package over your live Stella installation.**

## Local source tests
With a compatible Python environment and dependencies installed, run:

```bash
python -m unittest tests.test_sage_host tests.test_conversation_pacing_contract tests.test_long_call_response_contract tests.test_prompt_security
```

These tests verify source contracts; they do not measure conversation quality or prove compatibility with the live providers.

See [UPLOAD_TO_GITHUB.md](UPLOAD_TO_GITHUB.md) for GitHub Desktop instructions.

## Privacy and public GitHub
Before publishing, personally inspect **every file**. A basic automatic scan is not a guarantee that project details, usernames, or other private information are safe to publish. If unsure, keep the repository private and grant the reviewer access instead.

No license is granted by this review package. Repository visibility does not change copyright or third-party asset license terms.
