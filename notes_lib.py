#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
notes_lib.py — nguồn chân lý duy nhất cho ghi chú người nói.

Đọc/ghi kich-ban-noi.md: 26 slide, mỗi slide một marker 【…】 theo đúng thứ tự slide.
Dùng chung cho build_presenter.py (nhúng ghi chú vào deck) và notes_server.py (API sửa + lưu).
"""
import re

# Marker nằm nguyên một dòng: 【tên】 (khớp đầu dòng để không dính câu văn chứa 【…】)
MARKER = re.compile(r'^【([^】]+)】[ \t]*$')

# 26 (section, title) theo đúng thứ tự slide 0..25
META = [
    ("Mở đầu",                 "Claude + Plugin"),
    ("Mở bài",                 "Mở bài — Luận điểm"),
    ("Mở bài",                 "Luận điểm cốt lõi"),
    ("Mở bài",                 "Điều cần nhớ"),
    ("Mở bài",                 "Mạch của buổi nói"),
    ("Khái niệm & phân loại",  "Khái niệm & phân loại"),
    ("Khái niệm & phân loại",  "Claude Code: Giới hạn"),
    ("Khái niệm & phân loại",  "Hai luồng xử lý một task khó"),
    ("Khái niệm & phân loại",  "4 giới hạn của Claude nguyên bản"),
    ("Khái niệm & phân loại",  "Kết luận"),
    ("Khái niệm & phân loại",  "Plugin là gì"),
    ("Khái niệm & phân loại",  "Kết luận"),
    ("Khái niệm & phân loại",  "Hệ sinh thái plugin — 3 loại"),
    ("Khái niệm & phân loại",  "Điểm nhấn với ban quản lý"),
    ("Cơ chế hoạt động",       "Cơ chế hoạt động"),
    ("Cơ chế hoạt động",       "Skills — làm thế nào?"),
    ("Cơ chế hoạt động",       "MCP server — có thể làm gì?"),
    ("Cơ chế hoạt động",       "Hooks — khi nào tự động làm?"),
    ("Cơ chế hoạt động",       "Sub-agent — ai làm phần nào?"),
    ("Cơ chế hoạt động",       "Giới hạn & rủi ro"),
    ("Giới thiệu 4 plugin demo", "Giới thiệu 4 plugin demo"),
    ("Giới thiệu 4 plugin demo", "4 plugin demo"),
    ("Demo",                   "Demo — một flow xuyên suốt"),
    ("Demo",                   "Kịch bản demo"),
    ("Demo",                   "Flow demo — 4 bước"),
    ("Q&A",                    "Q&A"),
    ("Q&A",                    "Q&A — hỏi đáp + QR điểm danh"),
]

TOTAL = len(META)


def _scan(md):
    """Trả về (lines, markers). marker = {'title','start','end'}; start/end là khoảng dòng của body."""
    lines = md.split('\n')
    markers = []
    i, n = 0, len(lines)
    while i < n:
        m = MARKER.match(lines[i])
        if m:
            start = i + 1
            j = start
            while j < n:
                ln = lines[j]
                if MARKER.match(ln) or ln.startswith('## ') or ln.startswith('### ') or ln.startswith('---'):
                    break
                j += 1
            markers.append({"title": m.group(1).strip(), "start": start, "end": j})
            i = j
        else:
            i += 1
    return lines, markers


def parse_notes(md):
    """26 ghi chú thô (raw markdown) theo thứ tự slide."""
    lines, markers = _scan(md)
    bodies = ['\n'.join(lines[mk["start"]:mk["end"]]).strip() for mk in markers]
    assert len(bodies) == TOTAL, "expect %d notes, got %d" % (TOTAL, len(bodies))
    return bodies


def qa_table_to_bullets(text):
    """Chuyển bảng markdown (Q&A) thành gạch đầu dòng để render được trong presenter."""
    out, rows, in_table = [], [], False
    for ln in text.split('\n'):
        if ln.strip().startswith('|'):
            cells = [c.strip() for c in ln.strip().strip('|').split('|')]
            if set(''.join(cells)) <= set('-:'):
                continue  # dòng ngăn cách header
            rows.append(cells)
            in_table = True
        else:
            if in_table:
                for r in rows[1:]:
                    if len(r) >= 2 and r[0] and r[1]:
                        out.append('- ' + r[0] + ' → ' + r[1])
                rows, in_table = [], False
            out.append(ln)
    if in_table:
        for r in rows[1:]:
            if len(r) >= 2 and r[0] and r[1]:
                out.append('- ' + r[0] + ' → ' + r[1])
    return '\n'.join(out)


def display_note(raw, index):
    """Ghi chú để hiển thị (slide Q&A cuối: bảng -> gạch đầu dòng)."""
    if index == TOTAL - 1:
        return qa_table_to_bullets(raw)
    return raw


def notes_payload(md):
    """Danh sách 26 {section,title,note} dạng hiển thị — cho deck nhúng / API GET."""
    bodies = parse_notes(md)
    return [
        {"section": META[i][0], "title": META[i][1], "note": display_note(b, i)}
        for i, b in enumerate(bodies)
    ]


def raw_note(md, index):
    """Ghi chú thô (raw markdown) của một slide — cho textarea sửa."""
    return parse_notes(md)[index]


def replace_note(md, index, new_note):
    """Ghi đè body của marker thứ `index` bằng new_note; trả về markdown mới."""
    lines, markers = _scan(md)
    assert len(markers) == TOTAL, "expect %d markers, got %d" % (TOTAL, len(markers))
    mk = markers[index]
    body = new_note.rstrip('\n')
    new_lines = body.split('\n') if body else []
    if new_lines:
        new_lines = [''] + new_lines  # một dòng trống sau marker cho dễ đọc
    out = lines[:mk["start"]] + new_lines + lines[mk["end"]:]
    return '\n'.join(out) + '\n'
