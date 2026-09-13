# PR #109590 visual evidence

Captured from the production Desktop build for feature commit
`293f3f75d841b3faa25efa0b65a8e4e5ee7c5474` on macOS 26.2 arm64, using the
repository's isolated Electron fixture and its mock provider. The same Desktop
source was exercised before rebasing; the rebase changed no Desktop source.

- `quit-setting-options.png`: Advanced settings with all three choices visible.
- `quit-setting-narrow.png`: the same preference at a 760px-wide window size.

The review rehearsal used real main/preload IPC and verified keyboard selection,
Escape, focus retention, persisted changes, and refresh after an external native
preference change. No real provider credentials or personal session data were used.

`backend-continuity.json` records a separate final-commit rehearsal with a real
isolated `hermes serve` process: the same backend identity remains healthy during
the prompt and after cancellation, and acceptance later stops it and releases
ownership. This rehearsal made no model call.

This branch holds review artifacts only. It is not part of the product PR diff.
