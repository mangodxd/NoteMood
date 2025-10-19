# NoteMood

Ứng dụng ghi chú kèm mood/thời tiết cá nhân dành cho desktop.

## Cách chạy
1. Cài đặt Python 3.x và PyQt6:
    ```
    pip install -r requirements.txt
    ```
2. Chạy ứng dụng:
    ```
    python src/main.py
    ```

## Cấu trúc thư mục
```
NoteMood_Pro/
├── README.md
├── requirements.txt
├── setup.py
├── .gitignore
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── ui.py
│   ├── weather_effects.py
│   └── music.py
├── tests/
│   ├── __init__.py
│   └── test_ui.py
├── assets/
│   ├── NoteMood_Icon.ico
│   ├── NoteMood_Icon.png
└── docs/
```

## Ghi chú
- Mặc định nhạc tải từ Internet, có thể chọn nhạc thủ công.
- Tự động lưu 2 phút/lần nếu có thay đổi.

## Đóng gói
- Đã build thử file thực thi tại `[here](https://github.com/mangodxd/NoteMood/releases/tag/v0.1.0)`.

