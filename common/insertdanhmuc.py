from aifc import Error

from ketnoi.ketnoi_mysql import connect_mysql


def insert_danhmuc(ten_danhmuc, mo_ta=None, trang_thai=1):
    """Chèn thêm 1 danh mục mới vào bảng 'danhmuc'"""
    connection = connect_mysql()
    if connection is None:
        return

    try:
        cursor = connection.cursor()
        sql = """
            INSERT INTO danhmuc (TenDanhMuc, MoTa, TrangThai)
            VALUES (%s, %s, %s)
        """
        values = (ten_danhmuc, mo_ta, trang_thai)

        cursor.execute(sql, values)
        connection.commit()  # Lưu thay đổi vào DB
        print(f"✅ Đã thêm danh mục: {ten_danhmuc}")

    except Error as e:
        print("❌ Lỗi khi chèn dữ liệu:", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
