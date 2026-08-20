# Demo — User Management (FE + Go BE + Postgres)

Demo một flow xuyên suốt cho bài nói về plugin: **form → backend nhận request → call DB**.

## Cấu trúc

```
demo/
  index.html          # FE: form "Thêm người dùng" (do skill frontend-design tạo)
  server/
    main.go           # Go backend, stdlib net/http + lib/pq
    go.mod / go.sum
  db/
    init.sql          # schema bảng users + 1 seed record
  docker-compose.yml  # Postgres 16 alpine (nhẹ)
```

## Chạy

```bash
# 1. Bật DB (Postgres 16 alpine, ~cỡ nhỏ)
cd demo
docker compose up -d db          # đợi vài giây cho healthy

# 2. Chạy backend Go (port 8000)
cd server && go run .            # hoặc: go build && ./server

# 3. Mở trình duyệt
open http://localhost:8000       # FE ở /, API ở /api/users
```

## API

| Method | Path        | Mô tả                              |
|--------|-------------|------------------------------------|
| GET    | /health     | Health check (ping DB)             |
| GET    | /api/users  | Liệt kê user (mới nhất trước)      |
| POST   | /api/users  | Tạo user từ JSON (form submit tới đây) |

Body POST `/api/users`:

```json
{"name":"Trần Thị B","email":"b@company.com","role":"admin","dept":"design","start":"2026-08-01","note":"..."}
```

`name` và `email` là bắt buộc (thiếu → 400).

## Biến môi trường (có mặc định)

- `DATABASE_URL` — mặc định `postgres://demo:demo@localhost:5432/demo?sslmode=disable`
- `ADDR` — mặc định `:8000`
- `INDEX_PATH` — mặc định `../index.html`

## Dừng / dọn

```bash
docker compose down          # dừng container (giữ volume)
docker compose down -v       # dừng + xoá data
```
