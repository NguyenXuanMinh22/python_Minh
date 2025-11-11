import mysql.connector
from mysql.connector import Error

def connect_mysql():
    """Hàm kết nối đến cơ sở dữ liệu MySQL"""
    try:
        connection = mysql.connector.connect(
            host='localhost',       # địa chỉ máy chủ MySQL
            user='root',            # tên người dùng MySQL
            password='',            # mật khẩu MySQL (nếu có thì điền vào)
            database='qlthuocankhang' # tên cơ sở dữ liệu bạn muốn kết nối
        )

        if connection.is_connected():
            print("✅ Kết nối MySQL thành công!")
            return connection

    except Error as e:
        print("❌ Lỗi khi kết nối MySQL:", e)
        return None
