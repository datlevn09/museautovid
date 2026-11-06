# Muse Auto

Gửi prompt, ảnh và video tham chiếu sang Muse, tự lấy video và ảnh về máy. Chạy trên máy của bạn (macOS, Windows). Chỉ cần danh sách tài khoản Muse của bạn.

**Tải về:** [Mac](https://github.com/datlevn09/museautovid/releases/download/v1.4.0/MuseAuto-1.4.0-mac.zip) · [Windows](https://github.com/datlevn09/museautovid/releases/download/v1.4.0/MuseAuto-1.4.0-windows.zip) · [Tất cả phiên bản](https://github.com/datlevn09/museautovid/releases)

## Tính năng

- **Tạo từ tham chiếu:** prompt + ảnh/video tham chiếu, chọn video, ảnh hoặc cả hai, tỉ lệ khung hình và độ dài. Gửi nguyên văn sang Muse, không có mô hình AI nào xử lý thêm.
- **Đổi khuôn mặt, trang phục** trong video mẫu: dán link video mẫu hoặc tải video lên, kèm ảnh.
- **Tạo ảnh** và **tạo hàng loạt** (nhiều prompt, nhiều tham chiếu, nhiều bản).
- **Clone kênh:** link video hoặc kênh, 1–10 phong cách, tự tải nguồn, gửi Muse, lấy file về.
- **Nhiều tài khoản Muse:** tự đăng nhập bằng link OTP, hiện trạng thái, cho nghỉ khi hết lượt và chuyển job sang tài khoản khác; tài khoản dính checkpoint tự bị bỏ.
- **Nhiều máy:** mỗi máy chạy độc lập và giữ video của nó; nối vào máy chủ quản lý riêng bằng mã ghép hoặc đăng nhập Google.

## Cài đặt

1. Giải nén vào một thư mục bất kỳ có quyền ghi.
2. Cần Python 3.10+ và FFmpeg. Mac: `bash Install.command`. Windows: chạy `Install.bat`.
3. Chạy `Start.command` (Mac) hoặc `Start.bat` (Windows), mở `http://127.0.0.1:18745`, vào **Tài khoản & cấu hình** để thêm tài khoản Muse.

Chi tiết trong `README.md` bên trong gói tải về.

## Lưu ý

- Cần tài khoản Muse của riêng bạn; mỗi tài khoản có giới hạn video mỗi ngày do Muse đặt ra.
- Chỉ dùng ảnh, video của người đã đồng ý hoặc nội dung bạn có quyền sử dụng. Muse có thể từ chối một số yêu cầu.
- Đã kiểm thử trên macOS (Apple Silicon). Bản Windows chưa được chạy trên máy Windows thật.
- Muse là sản phẩm của bên thứ ba; Muse Auto không thuộc về Muse.
