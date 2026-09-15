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
## 6. External - Video Feature Extraction

Project sử dụng repository `video_features` để trích xuất các đặc trưng từ video bằng các model như CLIP, I3D, R(2+1)D, S3D, VGGish, RAFT, ResNet và TIMM.

Phần `external/video_features` được chạy bằng **Docker riêng**, không sử dụng môi trường `uv` của project chính.

### 6.1. Clone `video_features`

Từ thư mục gốc của project:

Sau khi clone, cấu trúc project sẽ có dạng:

```text
D23_Lop4_Nhom16/
├── pyproject.toml
├── uv.lock
├── src/
├── dataset/
├── features/
│
└── external/
    └── video_features/
        ├── main.py
        ├── models/
        ├── configs/
        └── ...
```

> `external/video_features` có môi trường dependency riêng và không được cài dependency của repository này vào môi trường `uv` của project chính.

---

### 6.2. Cài Docker

Kiểm tra Docker đã được cài hay chưa:

```bash
docker --version
```

Nếu Ubuntu chưa có Docker:

```bash
sudo apt update
sudo apt install docker.io
sudo systemctl enable --now docker
```

Thêm user hiện tại vào group `docker`:

```bash
sudo usermod -aG docker $USER
```

Sau đó đăng xuất và đăng nhập lại hoặc chạy:

```bash
newgrp docker
```

Kiểm tra:

```bash
docker ps
```

---

### 6.3. Pull Docker image của `video_features`

```bash
docker pull iashin/video_features
```

Chỉ cần pull image lần đầu tiên.

Kiểm tra:

```bash
docker images | grep video_features
```

---

### 6.4. Chuẩn bị dataset và thư mục feature

Video cần trích xuất feature được đặt trong:

```text
dataset/
```

Ví dụ:

```text
dataset/
├── dog001.mp4
├── dog002.mp4
└── dog003.mp4
```

Feature sau khi trích xuất sẽ được lưu vào:

```text
features/
```

---

### 6.5. Tạo Docker container

Đứng tại thư mục gốc:

```bash
cd D23_Lop4_Nhom16
```

Tạo container:

```bash
docker run -it \
  --name video-features \
  --mount type=bind,source="$(pwd)/external/video_features",destination="/home/ubuntu/video_features" \
  --mount type=bind,source="$(pwd)/dataset",destination="/home/ubuntu/video_features/dataset" \
  --mount type=bind,source="$(pwd)/features",destination="/home/ubuntu/video_features/output" \
  --shm-size 8G \
  iashin/video_features \
  bash
```

Ba bind mount trên tương ứng với:

```text
HOST PROJECT                         DOCKER CONTAINER

external/video_features  ────────>  /home/ubuntu/video_features

dataset/                 ────────>  /home/ubuntu/video_features/dataset

features/                <────────  /home/ubuntu/video_features/output
```

Do đó Docker có thể đọc video từ `dataset/` và feature được tạo trong container sẽ xuất hiện trực tiếp trong `features/` của project chính.

---

### 6.6. Vào lại container

Container chỉ cần tạo **một lần** bằng `docker run`.

Sau khi container đã tồn tại, không chạy lại `docker run`.

Kiểm tra container:

```bash
docker ps -a
```

Nếu container `video-features` đang dừng:

```bash
docker start -ai video-features
```

Nếu container đang chạy:

```bash
docker exec -it video-features bash
```

Không cần bind mount lại khi vào lại container cũ.

---

### 6.7. Kiểm tra dataset bên trong container

Sau khi vào container:

```bash
cd /home/ubuntu/video_features
```

Kiểm tra:

```bash
ls dataset
```

Ví dụ:

```text
dog001.mp4
dog002.mp4
dog003.mp4
```

---

### 6.8. Trích xuất CLIP feature

Ví dụ trích xuất CLIP feature cho:

```text
dataset/dog.mp4
```

Chạy bên trong container:

```bash
python main.py \
  feature_type="clip" \
  model_name="ViT-B/32" \
  device="cpu" \
  extraction_fps=1 \
  video_paths="[./dataset/dog.mp4]" \
  on_extraction="print"
```

`on_extraction="print"` dùng để in feature trực tiếp ra terminal để kiểm tra.

Nếu muốn lưu feature:

```bash
python main.py \
  feature_type="clip" \
  model_name="ViT-B/32" \
  device="cpu" \
  extraction_fps=1 \
  video_paths="[./dataset/dog.mp4]" \
  on_extraction="save_numpy" \
  output_path="./output"
```

Do thư mục `output` đã được bind mount với `features/`, kết quả sẽ được lưu ở project chính:

```text
D23_Lop4_Nhom16/features/
```

---

### 6.9. Sử dụng các extractor khác

Repository `video_features` hỗ trợ nhiều loại feature extractor.

Ví dụ:

```bash
python main.py \
  feature_type="r21d" \
  device="cpu" \
  video_paths="[./dataset/dog.mp4]" \
  on_extraction="save_numpy" \
  output_path="./output"
```

Các extractor có thể sử dụng bao gồm:

```text
clip
i3d
r21d
s3d
vggish
raft
resnet
timm
```

Cấu hình của từng model có thể khác nhau. Tham khảo repository `video_features` khi thay đổi extractor.

---

### 6.10. CPU và GPU

Nếu máy không có NVIDIA GPU, sử dụng:

```text
device="cpu"
```

Ví dụ:

```bash
python main.py \
  feature_type="clip" \
  device="cpu" \
  video_paths="[./dataset/dog.mp4]"
```

Một số model video như I3D, R(2+1)D, S3D hoặc RAFT có thể chạy khá chậm trên CPU.

---

### 6.11. Thoát Docker container

Để dừng và thoát container:

```bash
exit
```

Lần sau vào lại bằng:

```bash
docker start -ai video-features
```

Không cần tạo container hoặc bind mount lại.

---

## 7. Workflow tổng thể

Project sử dụng hai môi trường độc lập:

```text
                    D23_Lop4_Nhom16
                           │
             ┌─────────────┴─────────────┐
             │                           │
             ▼                           ▼
       Main Application          Feature Extraction
             │                           │
             ▼                           ▼
            uv                         Docker
             │                           │
             ▼                           ▼
     pyproject.toml             external/video_features
       + uv.lock                        │
                                        ▼
                              CLIP / I3D / R21D /
                              S3D / VGGish / RAFT
                                        │
                                        ▼
                                   features/
                                        │
                   ┌────────────────────┘
                   ▼
            Similarity Search
                   │
                   ▼
                  Top-K
```

Project chính:

```bash
uv sync
uv run python src/d23_lop4_nhom16/preprocessing_video.py
```

Feature extraction:

```bash
docker start -ai video-features
```

Hai môi trường được tách biệt để tránh xung đột dependency.