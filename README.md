# D23_Lop4_Nhom16

## 1. Clone project

```bash
git clone <URL_REPOSITORY>
```

## 2. Vào thư mục project

```bash
cd D23_Lop04_Nhom16
```

## 3. Cài uv nếu máy chưa có

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## 4. Đồng bộ môi trường từ pyproject.toml + uv.lock

```bash
uv sync
```

## 5. Chạy project

```bash
uv run python src/d23_lop4_nhom16/main.py
```

Lưu ý: file `src/d23_lop4_nhom16/main.py` hiện chưa có trong dự án này. Script đang có sẵn trong repo là `src/d23_lop4_nhom16/preprocessing_video.py`, nên lệnh chạy thực tế hiện tại là:

```bash
uv run python src/d23_lop4_nhom16/preprocessing_video.py
```
