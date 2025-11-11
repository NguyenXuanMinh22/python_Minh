from common.update_danhmuc import update_danhmuc

def test_update():
    while True:
        madm = input("Nhập mã danh mục cần cập nhật: ")
        ten = input("Nhập tên danh mục mới: ")
        mota = input("Nhập mô tả mới: ")

        update_danhmuc(madm, ten, mota)

        con = input("Tiếp tục cập nhật (y), thoát thì nhấn ký tự bất kỳ khác: ")
        if con.lower() != "y":
            break

# Gọi hàm test
test_update()
