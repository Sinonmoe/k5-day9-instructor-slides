# K5 Day 09: Instructor Slides (React)

Deck giảng viên **Evaluation & Failure Analysis (LogiX-VN)**, xây dựng trên cùng khung Vite + React + TypeScript với timer theo checkpoint và ghi chú giảng viên.

Nội dung lấy từ repo lab `VinUni-AI20k/K5-Day9-Evaluation-and-Failure-Analysis` (kết hợp overlay lên repo Lab 8 `K5-Day8-From-Workflows-to-Agents`). Logo Vingroup và VinUniversity cắt từ trang https://vinuni.edu.vn/aithucchien/.

## Live

https://sinonmoe.github.io/k5-day9-instructor-slides/ (thêm `?ca=sang` hoặc `?ca=chieu` để chọn ca)

## Sửa nội dung

Nội dung slide nằm trong `content/build_content.py` (HTML của từng slide và speaker notes). Sửa file này rồi sinh lại JSON:

```bash
python content/build_content.py
```

## Dev

```bash
cd app
npm install
npm run dev
```

## Build & Deploy (GitHub Pages)

```bash
cd app
npm run build
# output: app/dist, base path /k5-day9-instructor-slides/
# deploy tự động qua .github/workflows/deploy.yml khi push lên nhánh main
```

## Lớp sáng và lớp chiều

Deck tự chọn ca theo giờ máy lúc mở trang, và không tự đổi giữa buổi:

- Mở trước 13:00: **lớp sáng**, 08:30 đến 12:00.
- Mở từ 13:00: **lớp chiều**, 13:30 đến 17:00 (giờ gốc trong README lab; phần Advanced/Expert làm tiếp tới 23:59).

Lớp sáng dùng cùng lịch, dời sớm 5 tiếng: mọi mốc giờ trên slide và trong ghi chú tự đổi. Nút ca trên header đổi tay và ghi vào link (`?ca=sang` hoặc `?ca=chieu`) để reload hay chia sẻ vẫn giữ đúng ca.

Lớp sáng bắt đầu giờ khác thì sửa `MORNING_SHIFT_HOURS` trong `app/src/session.ts`.

## Phím tắt

| Phím | Việc |
|------|------|
| ← → / Space | Đổi slide |
| P / R | Dừng hoặc chạy timer / đặt lại |
| M | Âm báo |
| B | Nhạc nền |
| N | Ghi chú giảng viên |
| F | Toàn màn hình |

Timer tự chạy khi mở slide CP1 (30 phút), CP2 (45 phút), CP3 (45 phút), CP4 (45 phút), CP5 (60 phút). Âm báo và nhạc nền mặc định tắt. `prefers-reduced-motion` tắt chuyển động và nhạc.
