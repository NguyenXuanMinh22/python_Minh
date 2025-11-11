from aifc import Error

from ketnoi.ketnoi_mysql import connect_mysql


def get_all_danhmuc():
    """Lấy danh sách tất cả danh mục"""
    connection = connect_mysql()
    if connection is None:
        return []

    try:
        cursor = connection.cursor(dictionary=True)  # Trả kết quả dạng dict
        sql = "SELECT MaDanhMuc, TenDanhMuc, MoTa, TrangThai FROM danhmuc"
        cursor.execute(sql)
        danh_sach = cursor.fetchall()

        if danh_sach:
            print("✅ Danh sách danh mục:")
            for dm in danh_sach:
                print(f"- [{dm['MaDanhMuc']}] {dm['TenDanhMuc']} ({'Hiển thị' if dm['TrangThai'] == 1 else 'Ẩn'})")
        else:
            print("⚠️ Chưa có danh mục nào trong hệ thống.")

        return danh_sach

    except Error as e:
        print("❌ Lỗi khi lấy danh sách danh mục:", e)
        return []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()