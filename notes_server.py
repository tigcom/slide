#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
notes_server.py — local server để sửa + lưu ghi chú người nói vĩnh viễn.

  GET  /api/notes        -> 26 ghi chú dạng hiển thị (deck nhúng/refresh)
  GET  /api/notes/<i>    -> ghi chú thô (raw) của slide i (textarea sửa)
  POST /api/notes/<i>    -> body {"note": "..."} ghi đè vào kich-ban-noi.md

Chạy:  python3 notes_server.py [port]      (mặc định 8765)
"""
import json
import os
import re
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import notes_lib

HERE = os.path.dirname(os.path.abspath(__file__))
MD = os.path.join(HERE, 'kich-ban-noi.md')


# File tĩnh được phục vụ (để mở deck ngay từ chính server này, không cần Live Server)
STATIC = {
    '/': 'claude-plugin.html',
    '/claude-plugin.html': 'claude-plugin.html',
    '/presenter.html': 'presenter.html',
}


def read_md():
    with open(MD, encoding='utf-8') as f:
        return f.read()


def write_md(text):
    with open(MD, 'w', encoding='utf-8') as f:
        f.write(text)


class Handler(BaseHTTPRequestHandler):
    server_version = 'notes-server/1.0'

    def _cors(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def _json(self, obj, status=200):
        body = json.dumps(obj, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self._cors()
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_GET(self):
        m = re.fullmatch(r'/api/notes(?:/(\d+))?', self.path)
        if not m:
            # Phục vụ file tĩnh (deck + presenter) — cho phép mở thẳng từ server này
            fname = STATIC.get(self.path)
            if fname is None:
                self._json({'error': 'not found'}, 404)
                return
            try:
                data = open(os.path.join(HERE, fname), 'rb').read()
            except Exception as e:
                self._json({'error': str(e)}, 500)
                return
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(data)))
            self.end_headers()
            self.wfile.write(data)
            return
        try:
            md = read_md()
        except Exception as e:
            self._json({'error': str(e)}, 500)
            return
        idx = m.group(1)
        if idx is None:
            self._json({'notes': notes_lib.notes_payload(md)})
        else:
            i = int(idx)
            if not (0 <= i < notes_lib.TOTAL):
                self._json({'error': 'index out of range'}, 400)
                return
            sec, title = notes_lib.META[i]
            self._json({'index': i, 'section': sec, 'title': title,
                        'note': notes_lib.raw_note(md, i)})

    def do_POST(self):
        m = re.fullmatch(r'/api/notes/(\d+)', self.path)
        if not m:
            self._json({'error': 'not found'}, 404)
            return
        i = int(m.group(1))
        if not (0 <= i < notes_lib.TOTAL):
            self._json({'error': 'index out of range'}, 400)
            return
        length = int(self.headers.get('Content-Length', 0))
        raw_body = self.rfile.read(length) if length else b''
        try:
            data = json.loads(raw_body.decode('utf-8'))
        except Exception:
            self._json({'error': 'bad json'}, 400)
            return
        note = data.get('note', '')
        try:
            new_md = notes_lib.replace_note(read_md(), i, note)
            write_md(new_md)
        except Exception as e:
            self._json({'error': str(e)}, 500)
            return
        self._json({'index': i, 'saved': True, 'note': note})

    def log_message(self, fmt, *args):
        sys.stderr.write('[notes-server] ' + fmt % args + '\n')


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
    httpd = ThreadingHTTPServer(('127.0.0.1', port), Handler)
    print('notes-server đang chạy tại  http://127.0.0.1:%d  (CTRL-C để dừng)' % port)
    print('Mở deck:  http://127.0.0.1:%d/claude-plugin.html  (rồi bấm P)' % port)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
