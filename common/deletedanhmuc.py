from aifc import Error

from ketnoi.ketnoi_mysql import connect_mysql


def delete_danhmuc(ma_danhmuc):
    """Xóa 1 danh mục theo mã MaDanhMuc"""
    connection = connect_mysql()
    if connection is None:
        return

    try:
        cursor = connection.cursor()
        sql = "DELETE FROM danhmuc WHERE MaDanhMuc = %s"
        value = (ma_danhmuc, )

        cursor.execute(sql, value)
        connection.commit()

        if cursor.rowcount > 0:
            print(f"✅ Đã xóa danh mục có mã {ma_danhmuc}")
        else:
            print(f"⚠️ Không tìm thấy danh mục có mã {ma_danhmuc}")

    except Error as e:
        print("❌ Lỗi khi xóa danh mục:", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
