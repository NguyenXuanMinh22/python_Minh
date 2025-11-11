from common.insertdanhmuc import insert_danhmuc

while True:
    ten = input("Nhập vào tên danh mục: ")
    mota = input("Nhập vào mô tả: ")

    # Gọi hàm thêm danh mục
    insert_danhmuc(ten, mota)

    con = input("Tiếp tục (y), thoát thì nhấn ký tự bất kỳ khác: ")
    if con.lower() != "y":
        break
