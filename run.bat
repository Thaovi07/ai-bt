@echo off
chcp 65001 > nul
echo =====================================================================
echo  HỆ THỐNG AI AGENT PHÂN TÍCH HIỆU QUẢ KINH DOANH - PHÚC AN RETAIL CHAIN
echo =====================================================================
echo Đang khởi động Web Dashboard tại: http://localhost:8000
echo Mở trình duyệt và truy cập: http://localhost:8000
echo Nhấn Ctrl+C để dừng hệ thống.
echo ---------------------------------------------------------------------
python server.py 8000
pause

