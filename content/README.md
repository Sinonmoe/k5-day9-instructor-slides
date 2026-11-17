# Nội dung deck

- `build_content.py`: HTML và speaker notes của từng slide. Chạy `python content/build_content.py` từ thư mục gốc để sinh `app/src/slides/content.json`.
- `icons.json`: SVG Lucide dùng trong slide, sinh bằng `node scripts/build_icons.mjs` (chạy trong `app/`).

## Nguồn sự thật

Deck lấy nội dung từ repo lab [VinUni-AI20k/K5-Day9-Evaluation-and-Failure-Analysis](https://github.com/VinUni-AI20k/K5-Day9-Evaluation-and-Failure-Analysis). Quy định chính thức nằm trong repo lab:

- `README.md`: hướng dẫn overlay lên repo Lab 8, lịch trình M0–M7, cấu trúc file
- `CHECKPOINTS.md`: các mốc kiểm tra M0–M4 trên lớp và M5–M7 sau 17:00
- `RUBRIC.md`: 100 điểm (Core 60 · Advanced 25 · Expert 15), bonus +5, và các mức trừ điểm
- `SUBMISSION.md`: PR từ `starter/d09` → `main` của repo Lab 8, deliverable, deadline 23:59 cùng ngày

Khi repo lab thay đổi, cập nhật `build_content.py` theo các file trên rồi chạy lại.
