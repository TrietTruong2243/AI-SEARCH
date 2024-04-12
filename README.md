# AI-SEARCH

# Kịch bản chính của Project 1 Robot Tìm Đường
 + B1	Chạy Menu.py
 + B2  Chạy các level cần thiết
- Nhấn phím Space để chạy chương trình
- Nhấn phím E để quay lại Menu khi đang ở trong giao diện chạy Map

# NOTE
 + Không thể chạy trực tiếp các file mà phải chạy qua menu 
 + Đã update giao diện
 + Đổi format screen 1024 X 768
 + Chỉnh sửa phần của mình cho giống bài ở Level 1
 + Đối với level 3, quy trình: kiểm tra các điểm mà từ start có đi qua được hết những điểm cần qua hay không, nếu ko đi qua được thì loại điểm đó khỏi đường đi -> sau đó kiểm tra từ start có đi đến được goal hay không, nếu ko được thì result = Target Not Found -> nếu đi tới được goal thì Target Found! (nếu có điểm đón thì xài thuật toán hoán vị để xét mọi trường hợp đường đi)
 + Phần tô màu trong level3 chỉ tô các path xét để tìm path nhỏ nhất, không tô màu phần tính đường đi ngắn nhất (A*), và thời gian chủ yếu là để tô màu phần path (khác mức 1,2 là tô màu quét tìm đường đi ngắn nhất)
 + Mức 1,2,3 xài chung 3 file input1, input2, input3
 + Do mức 3 xài hoán vị nên xét ít điểm đón (nếu ko nó chạy n! vòng lặp với n là số điểm đón)
 + Chưa sửa chọn map cho mức 4,5
# FOMAT CHUNG CHO VIỆC HIỂN THỊ CÁC CHƯƠNG TRÌNH LEVEL 1, LEVEL 2
![image](https://github.com/TrietTruong2243/AI-SEARCH/assets/95559644/0fa734bc-d8ef-48f1-99a2-8cd182bb3acc)

# ĐÃ HOÀN THIỆN LEVEL 1 VÀ LEVEL 2
# LEVEL 3 CẦN CHECK LẠI
