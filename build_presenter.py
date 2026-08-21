#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dựng "Presenter View" cho deck claude-plugin.html:
  1. Trích 26 ghi chú từ kich-ban-noi.md (dùng notes_lib) -> nhúng vào deck.
  2. Gắn mảng SPEAKER_NOTES + cơ chế đồng bộ (postMessage) + nạp live từ notes_server.
  3. Sinh presenter.html (cửa sổ ghi chú + chế độ sửa/lưu vĩnh viễn).

Chạy lại script này sau mỗi lần sửa kich-ban-noi.md để làm mới ghi chú nhúng.
Ghi chú đã sửa qua notes_server được lưu thẳng vào kich-ban-noi.md (không cần build lại).
"""
import re, json, os, shutil

import notes_lib

HERE = os.path.dirname(os.path.abspath(__file__))
DECK = os.path.join(HERE, 'claude-plugin.html')
PRESENTER = os.path.join(HERE, 'presenter.html')

# ---------------------------------------------------------------------------
# 1) Parse kich-ban-noi.md -> 26 ghi chú
# ---------------------------------------------------------------------------
md = open(os.path.join(HERE, 'kich-ban-noi.md'), encoding='utf-8').read()
notes = notes_lib.notes_payload(md)
assert len(notes) == notes_lib.TOTAL, "expect %d notes, got %d" % (notes_lib.TOTAL, len(notes))

notes_json = json.dumps(notes, ensure_ascii=False).replace('</', '<\\/')

# ---------------------------------------------------------------------------
# 2) Inject vào claude-plugin.html
# ---------------------------------------------------------------------------
# Nguồn luôn là bản gốc (pristine) trong .bak — để script chạy lại được (idempotent)
bak = DECK + '.bak'
if not os.path.exists(bak):
    shutil.copy2(DECK, bak)
    print('backup ->', bak)
html = open(bak, encoding='utf-8').read()

# Edit A: broadcast trong show()
old_show = "        if (pageLabel) { pageLabel.textContent = pad(current + 1) + ' / ' + pad(total); }\n    }"
new_show = ("        if (pageLabel) { pageLabel.textContent = pad(current + 1) + ' / ' + pad(total); }\n"
            "        if (window.__presenter) { window.__presenter.broadcast(current); }\n"
            "    }")
assert html.count(old_show) == 1, 'show() anchor not unique/found'
html = html.replace(old_show, new_show)

# Edit B: expose show/getCurrent trước show(0)
old_init = "    show(0);\n})();"
new_init = ("    // Expose cho presenter-view\n"
            "    window.__goto = show;\n"
            "    window.__getCurrent = function () { return current; };\n\n"
            "    show(0);\n})();")
assert html.count(old_init) == 1, 'init anchor not unique/found'
html = html.replace(old_init, new_init)

# Edit C: thêm script presenter-view trước </body>
presenter_js = """
/* ============================================================
   PRESENTER VIEW — ghi chú người nói đồng bộ theo slide
   - Phím P: mở cửa sổ ghi chú (presenter.html) lên màn laptop
   - Ghi chú tự đổi theo slide đang chiếu; không hiện gì lên máy chiếu
   - Nếu notes_server.py đang chạy: nạp ghi chú mới nhất từ kich-ban-noi.md
   ============================================================ */
var SPEAKER_NOTES = %NOTES%;
var API_BASES = ['', 'http://127.0.0.1:8765'];
function apiFetch(path, opts) {
    return new Promise(function (resolve, reject) {
        var bases = API_BASES.slice();
        (function tryNext() {
            if (!bases.length) { reject(new Error('no notes server')); return; }
            fetch(bases.shift() + path, opts).then(function (r) {
                if (!r.ok) throw new Error('bad status');
                resolve(r);
            }).catch(tryNext);
        })();
    });
}

(function () {
    var WIN_NAME = 'claude-presenter';
    var win = null;

    function payload(i) {
        var n = SPEAKER_NOTES[i] || { section: '', title: '', note: '' };
        return { index: i, total: SPEAKER_NOTES.length,
                 section: n.section, title: n.title, note: n.note };
    }

    function broadcast(i) {
        if (win && !win.closed) {
            try { win.postMessage({ type: 'deck:slide', data: payload(i) }, '*'); } catch (e) {}
        }
    }

    function open() {
        if (win && !win.closed) { win.focus(); return; }
        win = window.open('presenter.html', WIN_NAME, 'width=640,height=940');
    }

    // Nạp ghi chú mới nhất từ notes_server (nếu đang chạy); ngược lại giữ bản nhúng.
    function refreshNotes() {
        apiFetch('/api/notes', { cache: 'no-store' }).then(function (r) {
            return r.json();
        }).then(function (data) {
            if (data && Array.isArray(data.notes) && data.notes.length) {
                SPEAKER_NOTES = data.notes;
                broadcast(window.__getCurrent ? window.__getCurrent() : 0);
            }
        }).catch(function () { /* server chưa chạy — dùng ghi chú nhúng */ });
    }
    window.__refreshNotes = refreshNotes;

    window.addEventListener('message', function (e) {
        var d = e.data;
        if (!d || !d.type) return;
        // Tự khôi phục tham chiếu presenter nếu bị mất (vd: deck bị reload -> `win` về null).
        if (d.type === 'presenter:hello' || d.type === 'presenter:goto' || d.type === 'presenter:refresh') {
            if (e.source && e.source !== window) { win = e.source; }
        }
        if (d.type === 'presenter:hello') {
            if (window.__getCurrent) broadcast(window.__getCurrent());
        } else if (d.type === 'presenter:goto') {
            if (window.__goto) window.__goto(Number(d.index));
        } else if (d.type === 'presenter:refresh') {
            refreshNotes();
        }
    });

    document.addEventListener('keydown', function (e) {
        if (e.target && e.target.getAttribute && e.target.getAttribute('contenteditable') === 'true') return;
        if ((e.key === 'p' || e.key === 'P') && !e.ctrlKey && !e.metaKey && !e.altKey) {
            e.preventDefault();
            open();
        }
    });

    window.__presenter = { open: open, broadcast: broadcast, refreshNotes: refreshNotes };

    refreshNotes();
})();
"""

presenter_js = presenter_js.replace('%NOTES%', notes_json)
assert html.count('</body>') == 1
html = html.replace('</body>', '<script>' + presenter_js + '</script>\n</body>', 1)

open(DECK, 'w', encoding='utf-8').write(html)
print('injected presenter-view into', DECK)

# ---------------------------------------------------------------------------
# 3) presenter.html
# ---------------------------------------------------------------------------
presenter_html = """<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Presenter — Claude + Plugin</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Source+Serif+4:ital,wght@0,400;0,600;1,400&family=DM+Sans:wght@400;500;700&family=IBM+Plex+Mono:wght@400;500;700&display=swap" rel="stylesheet">
<style>
:root {
    --bg: #111010;
    --panel: #1b1a19;
    --ink: #f4f1ea;
    --muted: #9a968f;
    --faint: #6b6863;
    --line: #2c2a28;
    --red: #ff3300;
    --serif: 'Source Serif 4', serif;
    --sans: 'DM Sans', sans-serif;
    --mono: 'IBM Plex Mono', monospace;
}
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { height: 100%; }
body {
    background: var(--bg); color: var(--ink);
    font-family: var(--sans); font-size: 17px; line-height: 1.65;
    display: flex; flex-direction: column;
}
.topbar {
    display: flex; align-items: baseline; gap: 16px;
    padding: 18px 24px 14px;
    border-bottom: 1px solid var(--line);
}
.slide-id { font-family: var(--mono); font-size: 15px; color: var(--red); font-weight: 700; }
.section { font-size: 13px; letter-spacing: .06em; text-transform: uppercase; color: var(--muted); flex: 1; }
.timer { font-family: var(--mono); font-size: 15px; color: var(--muted); cursor: pointer; user-select: none; }
.timer:hover { color: var(--ink); }

.title {
    font-family: var(--serif); font-size: 30px; font-weight: 600; line-height: 1.25;
    padding: 22px 24px 6px;
}

.note {
    flex: 1; overflow-y: auto;
    padding: 10px 24px 24px;
}
.note p { margin: 0 0 14px; color: #e7e2d8; }
.note ul { margin: 0 0 14px; padding-left: 4px; list-style: none; }
.note li {
    position: relative; padding-left: 22px; margin-bottom: 9px; color: #e7e2d8;
}
.note li::before { content: '—'; position: absolute; left: 0; color: var(--red); font-weight: 700; }
.note strong { color: #fff; font-weight: 700; }
.note em { color: var(--red); font-style: italic; }

.editor { flex: 1; display: flex; flex-direction: column; min-height: 0; padding: 10px 24px 24px; }
.editor textarea {
    flex: 1; width: 100%; resize: none; min-height: 200px;
    background: #141312; color: var(--ink);
    border: 1px solid var(--line); border-radius: 8px;
    padding: 16px; font-family: var(--mono); font-size: 14px; line-height: 1.6;
    outline: none;
}
.editor textarea:focus { border-color: var(--red); }
.editor .status { margin-top: 10px; font-size: 13px; color: var(--muted); min-height: 18px; }
.editor .status.ok { color: #4cd964; }
.editor .status.err { color: var(--red); }

.foot {
    display: flex; align-items: center; gap: 14px;
    padding: 14px 24px; border-top: 1px solid var(--line); background: var(--panel);
}
.foot button {
    font-family: var(--sans); font-size: 15px; font-weight: 500;
    padding: 10px 20px; border-radius: 8px; cursor: pointer;
    border: 1px solid var(--line); background: #232120; color: var(--ink);
    transition: border-color .15s ease, color .15s ease;
}
.foot button:hover { border-color: var(--red); color: #fff; }
.foot .hint { flex: 1; text-align: center; font-size: 12.5px; color: var(--faint); }
.foot .hint b { color: var(--muted); font-weight: 500; }

.offline {
    max-width: 520px; margin: 80px auto; padding: 0 24px; text-align: center; color: var(--muted);
}
.offline .big { font-family: var(--serif); font-size: 26px; color: var(--ink); margin-bottom: 10px; }
.offline code { font-family: var(--mono); color: var(--red); font-size: 15px; }
</style>
</head>
<body>
    <div id="app" style="display:flex;flex-direction:column;flex:1;min-height:0;">
        <div class="topbar">
            <div class="slide-id"><span id="idx">—</span> / <span id="total">—</span></div>
            <div class="section" id="section">chờ deck…</div>
            <div class="timer" id="timer" title="Bấm để reset đồng hồ">00:00</div>
        </div>
        <div class="title" id="title">Mở file <code style="font-family:var(--mono);color:var(--red)">claude-plugin.html</code> rồi bấm <b>P</b></div>
        <div class="note" id="note"><p style="color:var(--muted)">Cửa sổ này tự đồng bộ với slide đang chiếu.</p></div>
        <div class="editor" id="editorWrap" style="display:none;">
            <textarea id="editor" spellcheck="false" placeholder="Gõ ghi chú (markdown: **đậm**, *nghiêng*, - gạch đầu dòng)…"></textarea>
            <div class="status" id="status"></div>
        </div>
        <div class="foot">
            <button id="prev">← Trước</button>
            <div class="hint"><b>←</b>/<b>→</b> đổi slide &nbsp;·&nbsp; <b>✏️ Sửa</b> sửa ghi chú vĩnh viễn</div>
            <button id="next">Sau →</button>
            <button id="edit" title="Sửa ghi chú slide này (lưu vào kich-ban-noi.md)">✏️ Sửa</button>
            <button id="save" style="display:none" title="Lưu vĩnh viễn vào kich-ban-noi.md">💾 Lưu</button>
            <button id="cancel" style="display:none">Hủy</button>
        </div>
    </div>

<script>
(function () {
    var idxEl = document.getElementById('idx');
    var totalEl = document.getElementById('total');
    var sectionEl = document.getElementById('section');
    var titleEl = document.getElementById('title');
    var noteEl = document.getElementById('note');
    var timerEl = document.getElementById('timer');
    var prevBtn = document.getElementById('prev');
    var nextBtn = document.getElementById('next');
    var editBtn = document.getElementById('edit');
    var saveBtn = document.getElementById('save');
    var cancelBtn = document.getElementById('cancel');
    var editorWrap = document.getElementById('editorWrap');
    var editorEl = document.getElementById('editor');
    var statusEl = document.getElementById('status');

    var API_BASES = ['', 'http://127.0.0.1:8765'];
    function apiFetch(path, opts) {
        return new Promise(function (resolve, reject) {
            var bases = API_BASES.slice();
            (function tryNext() {
                if (!bases.length) { reject(new Error('no notes server')); return; }
                fetch(bases.shift() + path, opts).then(function (r) {
                    if (!r.ok) throw new Error('bad status');
                    resolve(r);
                }).catch(tryNext);
            })();
        });
    }
    var current = -1;
    var editing = false;
    var currentNote = '';   // nội dung ghi chú đang hiển thị (để điền ngay vào textarea)
    var userTyped = false;  // đánh dấu người dùng đã gõ (để không ghi đè bằng bản raw)

    function esc(s) { return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }
    function inline(s) {
        s = esc(s);
        s = s.replace(/\\*\\*([^*]+)\\*\\*/g, '<strong>$1</strong>');
        s = s.replace(/\\*([^*]+)\\*/g, '<em>$1</em>');
        return s;
    }
    function render(note) {
        var lines = String(note || '').split('\\n');
        var html = '', listOpen = false;
        function closeList() { if (listOpen) { html += '</ul>'; listOpen = false; } }
        for (var i = 0; i < lines.length; i++) {
            var ln = lines[i].replace(/\\s+$/, '');
            if (!ln.trim()) { closeList(); continue; }
            if (/^\\s*-\\s+/.test(ln)) {
                if (!listOpen) { html += '<ul>'; listOpen = true; }
                html += '<li>' + inline(ln.replace(/^\\s*-\\s+/, '')) + '</li>';
            } else {
                closeList();
                html += '<p>' + inline(ln) + '</p>';
            }
        }
        closeList();
        return html;
    }

    function pad(n) { return (n < 10 ? '0' : '') + n; }
    function apply(d) {
        var note = d.note || '';
        var changed = d.index !== current || note !== currentNote;
        current = d.index;
        currentNote = note;
        idxEl.textContent = pad(d.index + 1);
        totalEl.textContent = pad(d.total);
        sectionEl.textContent = d.section || '';
        titleEl.textContent = d.title || '';
        if (changed) {
            noteEl.innerHTML = render(note);
            noteEl.scrollTop = 0;
        }
    }

    function goto(i) {
        if (window.opener) {
            window.opener.postMessage({ type: 'presenter:goto', index: i }, '*');
        }
    }

    function setStatus(msg, ok) {
        statusEl.textContent = msg || '';
        statusEl.className = 'status' + (ok === true ? ' ok' : ok === false ? ' err' : '');
    }

    function enterEdit() {
        if (current < 0) {
            setStatus('Chưa có slide — mở deck rồi bấm P', false);
            return;
        }
        // Mở textarea NGAY lập tức từ nội dung đang hiển thị (không cần server)
        editing = true;
        userTyped = false;
        editorEl.value = currentNote;
        editorWrap.style.display = 'flex';
        noteEl.style.display = 'none';
        editBtn.style.display = 'none';
        saveBtn.style.display = '';
        cancelBtn.style.display = '';
        setStatus('Đang sửa — bấm 💾 Lưu để ghi vào kich-ban-noi.md');
        editorEl.focus();
        // (tùy chọn) nạp bản RAW từ server để sửa đúng markdown gốc (vd bảng Q&A)
        apiFetch('/api/notes/' + current, { cache: 'no-store' }).then(function (r) {
            return r.json();
        }).then(function (d) {
            if (editing && !userTyped && d && typeof d.note === 'string') {
                editorEl.value = d.note;
            }
        }).catch(function () { /* server chưa chạy — vẫn sửa được từ bản hiển thị */ });
    }

    function exitEdit() {
        editing = false;
        editorWrap.style.display = 'none';
        noteEl.style.display = '';
        editBtn.style.display = '';
        saveBtn.style.display = 'none';
        cancelBtn.style.display = 'none';
    }

    function refreshDisplay() {
        apiFetch('/api/notes', { cache: 'no-store' }).then(function (r) {
            return r.json();
        }).then(function (d) {
            if (d && Array.isArray(d.notes) && current >= 0) {
                var n = d.notes[current] || { section: '', title: '', note: '' };
                apply({ index: current, total: d.notes.length,
                        section: n.section, title: n.title, note: n.note });
            }
        }).catch(function () {});
    }

    function saveEdit() {
        var note = editorEl.value;
        setStatus('Đang lưu…');
        apiFetch('/api/notes/' + current, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ note: note })
        }).then(function (r) {
            return r.json();
        }).then(function () {
            setStatus('Đã lưu ✓', true);
            if (window.opener) {
                window.opener.postMessage({ type: 'presenter:refresh' }, '*');
            }
            refreshDisplay();
            setTimeout(function () { exitEdit(); }, 700);
        }).catch(function () {
            setStatus('Lưu thất bại — kiểm tra notes_server.py đang chạy', false);
        });
    }

    prevBtn.addEventListener('click', function () { goto(current - 1); });
    nextBtn.addEventListener('click', function () { goto(current + 1); });
    editBtn.addEventListener('click', enterEdit);
    saveBtn.addEventListener('click', saveEdit);
    editorEl.addEventListener('input', function () { userTyped = true; });
    cancelBtn.addEventListener('click', function () { exitEdit(); setStatus(''); });

    document.addEventListener('keydown', function (e) {
        if (editing) return;
        if (e.key === 'ArrowLeft' || e.key === 'ArrowUp' || e.key === 'PageUp') { e.preventDefault(); goto(current - 1); }
        else if (e.key === 'ArrowRight' || e.key === 'ArrowDown' || e.key === 'PageDown') { e.preventDefault(); goto(current + 1); }
    });

    window.addEventListener('message', function (e) {
        var d = e.data;
        if (d && d.type === 'deck:slide' && d.data) { apply(d.data); }
    });

    // Bắt tay: xin deck gửi slide hiện tại (kể cả khi mở lại)
    function hello() {
        if (window.opener) {
            window.opener.postMessage({ type: 'presenter:hello' }, '*');
        }
    }
    if (window.opener) {
        hello();
        // Heartbeat: nếu deck bị reload, biến `win` của deck về null và mất liên kết.
        // Cứ 2 giây xin lại slide hiện tại để deck tự khôi phục tham chiếu qua e.source.
        setInterval(hello, 2000);
    } else {
        // Mở trực tiếp presenter.html (không qua deck): tự nạp từ server, bắt đầu ở slide 0
        sectionEl.textContent = 'standalone — nạp ghi chú…';
        apiFetch('/api/notes', { cache: 'no-store' }).then(function (r) {
            return r.json();
        }).then(function (d) {
            if (d && Array.isArray(d.notes) && d.notes.length) {
                var n = d.notes[0];
                apply({ index: 0, total: d.notes.length,
                        section: n.section, title: n.title, note: n.note });
            }
        }).catch(function () {
            sectionEl.textContent = 'chưa kết nối deck / notes_server';
        });
    }

    // Đồng hồ bấm giờ (bấm để reset)
    var start = Date.now();
    function tick() {
        var s = Math.floor((Date.now() - start) / 1000);
        var m = Math.floor(s / 60), sec = s % 60;
        timerEl.textContent = pad(m) + ':' + pad(sec);
    }
    setInterval(tick, 1000); tick();
    timerEl.addEventListener('click', function () { start = Date.now(); tick(); });
})();
</script>
</body>
</html>
"""

open(PRESENTER, 'w', encoding='utf-8').write(presenter_html)
print('wrote', PRESENTER)
print('DONE')
