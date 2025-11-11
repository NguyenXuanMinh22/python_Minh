from aifc import Error

from ketnoi.ketnoi_mysql import connect_mysql


def update_danhmuc(ma_danhmuc, ten_moi=None, mo_ta_moi=None, trang_thai_moi=None):
    """
    Cập nhật thông tin danh mục:
    - ma_danhmuc: mã danh mục cần cập nhật (bắt buộc)
    - ten_moi, mo_ta_moi, trang_thai_moi: giá trị mới (có thể để None nếu không muốn đổi)
    """
    connection = connect_mysql()
    if connection is None:
        return

    try:
        cursor = connection.cursor()

        # Tạo câu SQL động tùy theo giá trị nào được truyền vào
        fields = []
        values = []

        if ten_moi is not None:
            fields.append("TenDanhMuc = %s")
            values.append(ten_moi)

        if mo_ta_moi is not None:
            fields.append("MoTa = %s")
            values.append(mo_ta_moi)

        if trang_thai_moi is not None:
            fields.append("TrangThai = %s")
            values.append(trang_thai_moi)

        # Nếu không có trường nào được cập nhật
        if not fields:
            print("⚠️ Không có thông tin nào để cập nhật.")
            return

        sql = f"UPDATE danhmuc SET {', '.join(fields)} WHERE MaDanhMuc = %s"
        values.append(ma_danhmuc)

        cursor.execute(sql, tuple(values))
        connection.commit()

        if cursor.rowcount > 0:
            print(f"✅ Đã cập nhật danh mục có mã {ma_danhmuc}")
        else:
            print(f"⚠️ Không tìm thấy danh mục có mã {ma_danhmuc}")

    except Error as e:
        print("❌ Lỗi khi cập nhật danh mục:", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
