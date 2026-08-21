# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A self-contained HTML slide deck for a ~70-minute internal technical talk (in Vietnamese) titled "Claude + Plugin: từ công cụ tự vận hành đến nền tảng mở rộng". It has two distinct halves that work together:

1. **The deck** — `claude-plugin.html`, a single self-contained HTML file with a hand-rolled JS slide engine (27 slides, fixed 16:9 stage, red `#f73500` accent on a Swiss/editorial layout).
2. **The presenter-view system** — speaker notes that sync to the projected slide, plus live editing that writes notes back to disk.

There is no build system, package manager, or test suite. Everything is Python 3 stdlib plus static HTML/CSS/JS.

## Commands

```bash
# Run the local notes server (default port 8765). Serves the deck + presenter
# and exposes a notes API so you can edit notes live and persist them.
python3 notes_server.py            # or: python3 notes_server.py <port>
# -> http://127.0.0.1:8765/claude-plugin.html  (press P to open presenter)

# Rebuild the presenter view: parses kich-ban-noi.md and injects speaker notes
# + sync JS into claude-plugin.html, then regenerates presenter.html.
python3 build_presenter.py

# Quick sanity check that the marker count matches the META table
python3 -c "import notes_lib; print(notes_lib.TOTAL)"
```

Open the deck by double-clicking `claude-plugin.html` (works standalone) or through `notes_server.py`. Navigate slides with arrow keys / PageUp / PageDown. Press `P` to open the presenter window.

## Architecture: the speaker-notes pipeline

The core system is a round-trip between one markdown file and the deck. Reading these four files together is what makes the design clear:

- **`kich-ban-noi.md`** — the single source of truth for speaker notes. Each slide has one `【name】` marker alone on a line (at line start), followed by its raw-markdown note body. The marker order must match slide order.
- **`notes_lib.py`** — the shared library. Holds `META`, a list of 27 `(section, title)` rows in slide order, and `TOTAL`. Parses `kich-ban-noi.md` into notes (`parse_notes` / `notes_payload`) and rewrites a single note (`replace_note`). Any change to slide count/order must be mirrored here.
- **`build_presenter.py`** — build step that consumes `kich-ban-noi.md` + `notes_lib`, does three string replacements on the deck (expose `show`/`getCurrent`, add a `broadcast` call, inject a presenter-view `<script>` containing the embedded `SPEAKER_NOTES`), and writes `presenter.html`. It asserts the marker count equals `notes_lib.TOTAL`.
- **`notes_server.py`** — a stdlib `ThreadingHTTPServer` that serves the static deck/presenter and exposes `GET /api/notes`, `GET /api/notes/<i>`, `POST /api/notes/<i>`. POSTing a note writes it straight back into `kich-ban-noi.md`.
- **`presenter.html`** — the presenter window (speaker notes, elapsed timer, `✏️ Sửa` / `💾 Lưu` editing). Syncs with the deck over `window.postMessage` (`deck:slide`, `presenter:goto`, `presenter:hello`, `presenter:refresh`).

The two editing workflows are equivalent in outcome but differ in mechanism:

- **Edit `kich-ban-noi.md` directly**, then run `build_presenter.py` to bake the notes into the deck.
- **Run `notes_server.py`**, open the deck, press `P`, and edit via the presenter's ✏️ button — the POST persists directly to `kich-ban-noi.md` (no rebuild needed), and the deck refreshes live.

### Important gotchas

- **`claude-plugin.html.bak` is the pristine deck source.** `build_presenter.py` always reads from `.bak` and overwrites `claude-plugin.html`, so re-runs are idempotent. If you hand-edit `claude-plugin.html` directly, your edits are lost on the next build unless you apply them to `.bak` (or to the build script) instead.
- **Marker format is strict:** `【name】` on its own line, anchored at line start (regex `^【([^】]+)】[ \t]*$`). The names need not match `META` titles — only count and order matter.
- **The docstrings that say "26 notes" are stale** — the current count is 27 (`notes_lib.TOTAL`), matching 27 `<section class="slide">` in the deck and 27 markers in `kich-ban-noi.md`. Trust `notes_lib.TOTAL`, not the comments.

## Content-authoring files (not wired into any script)

These feed the deck's content but are referenced by no `.py`/`.html` file — they are source material and drafts:

- **`noi-dung.md`** — the master outline: thesis, per-section goals, tables (4 limitations, plugin taxonomy, 4 demo plugins, demo flow, Q&A fallback answers).
- **`slides.json`** — slide content spec (sections, layouts: `statement`/`bullets`/`table`/`flow`/`countdown`). This is the structured content that was authored into `claude-plugin.html`; it is not regenerated from this file.
- **`ver1.md`–`ver4.md`** — earlier drafts of the training program design.
- **`images/`** — robot-themed 3D illustrations (`images/mo-ta-anh.md` documents each one); **`undraw-svg/`** — undraw SVG icons used by the deck.
