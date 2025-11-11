import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error

# ==============================
# HÀM KẾT NỐI MYSQL
# ==============================
def connect_mysql():
    try:
        return mysql.connector.connect(
            host='localhost',
            user='root',
            password='',  # 🔹 thay nếu có mật khẩu
            database='qlthuocankhang'  # 🔹 thay bằng tên CSDL của bạn
        )
    except Error as e:
        messagebox.showerror("Lỗi MySQL", f"Lỗi kết nối CSDL: {e}")
        return None


# ==============================
# HÀM XỬ LÝ DỮ LIỆU
# ==============================
def load_danhmuc():
    """Tải dữ liệu từ MySQL lên TreeView"""
    connection = connect_mysql()
    if connection is None:
        return

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT MaDanhMuc, TenDanhMuc, MoTa, TrangThai FROM danhmuc")
        rows = cursor.fetchall()

        # Xóa dữ liệu cũ trong TreeView
        for item in tree.get_children():
            tree.delete(item)

        # Thêm dữ liệu mới
        for row in rows:
            tree.insert("", "end", values=row)
    except Error as e:
        messagebox.showerror("Lỗi", f"Không thể tải dữ liệu: {e}")
    finally:
        cursor.close()
        connection.close()


def them_danhmuc():
    """Thêm danh mục mới vào MySQL"""
    ten = entry_ten.get().strip()
    mota = entry_mota.get().strip()
    if not ten:
        messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập tên danh mục!")
        return

    connection = connect_mysql()
    if connection is None:
        return

    try:
        cursor = connection.cursor()
        sql = "INSERT INTO danhmuc (TenDanhMuc, MoTa, TrangThai) VALUES (%s, %s, %s)"
        cursor.execute(sql, (ten, mota, "Hoạt động"))
        connection.commit()
        messagebox.showinfo("Thành công", "Đã thêm danh mục mới!")
        load_danhmuc()
        entry_ten.delete(0, tk.END)
        entry_mota.delete(0, tk.END)
    except Error as e:
        messagebox.showerror("Lỗi", f"Không thể thêm danh mục: {e}")
    finally:
        cursor.close()
        connection.close()


def select_row(event):
    """Khi chọn dòng trong bảng"""
    selected = tree.focus()
    if not selected:
        return
    values = tree.item(selected, "values")
    entry_ten.delete(0, tk.END)
    entry_mota.delete(0, tk.END)
    entry_ten.insert(0, values[1])
    entry_mota.insert(0, values[2])


def sua_danhmuc():
    """Cập nhật danh mục"""
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Chưa chọn", "Vui lòng chọn danh mục để sửa!")
        return

    ten = entry_ten.get().strip()
    mota = entry_mota.get().strip()
    if not ten:
        messagebox.showwarning("Thiếu dữ liệu", "Tên danh mục không được để trống!")
        return

    values = tree.item(selected, "values")
    ma = values[0]

    connection = connect_mysql()
    if connection is None:
        return

    try:
        cursor = connection.cursor()
        sql = "UPDATE danhmuc SET TenDanhMuc=%s, MoTa=%s WHERE MaDanhMuc=%s"
        cursor.execute(sql, (ten, mota, ma))
        connection.commit()
        messagebox.showinfo("Thành công", "Đã cập nhật danh mục!")
        load_danhmuc()
    except Error as e:
        messagebox.showerror("Lỗi", f"Không thể sửa danh mục: {e}")
    finally:
        cursor.close()
        connection.close()


def xoa_danhmuc():
    """Xóa danh mục khỏi MySQL"""
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Chưa chọn", "Vui lòng chọn danh mục để xóa!")
        return

    values = tree.item(selected, "values")
    ma = values[0]
    ten = values[1]

    if not messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa danh mục '{ten}' không?"):
        return

    connection = connect_mysql()
    if connection is None:
        return

    try:
        cursor = connection.cursor()
        sql = "DELETE FROM danhmuc WHERE MaDanhMuc=%s"
        cursor.execute(sql, (ma,))
        connection.commit()
        messagebox.showinfo("Thành công", "Đã xóa danh mục!")
        load_danhmuc()
        entry_ten.delete(0, tk.END)
        entry_mota.delete(0, tk.END)
    except Error as e:
        messagebox.showerror("Lỗi", f"Không thể xóa danh mục: {e}")
    finally:
        cursor.close()
        connection.close()


# ==============================
# GIAO DIỆN TKINTER
# ==============================
root = tk.Tk()
root.title("QUẢN LÝ DANH MỤC SẢN PHẨM")
root.geometry("700x500")
root.resizable(False, False)

# --- Frame nhập liệu ---
frame_input = tk.LabelFrame(root, text="Thông tin danh mục", padx=10, pady=10)
frame_input.pack(fill="x", padx=10, pady=10)

tk.Label(frame_input, text="Tên danh mục:").grid(row=0, column=0, sticky="w")
entry_ten = tk.Entry(frame_input, width=40)
entry_ten.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_input, text="Mô tả:").grid(row=1, column=0, sticky="w")
entry_mota = tk.Entry(frame_input, width=40)
entry_mota.grid(row=1, column=1, padx=5, pady=5)

# --- Frame nút chức năng ---
frame_buttons = tk.Frame(root)
frame_buttons.pack(fill="x", padx=10, pady=5)

btn_them = tk.Button(frame_buttons, text="➕ Thêm", width=12, command=them_danhmuc)
btn_them.pack(side="left", padx=5)

btn_sua = tk.Button(frame_buttons, text="✏️ Sửa", width=12, command=sua_danhmuc)
btn_sua.pack(side="left", padx=5)

btn_xoa = tk.Button(frame_buttons, text="🗑️ Xóa", width=12, command=xoa_danhmuc)
btn_xoa.pack(side="left", padx=5)

btn_tai = tk.Button(frame_buttons, text="🔄 Tải lại", width=12, command=load_danhmuc)
btn_tai.pack(side="left", padx=5)

# --- Treeview hiển thị danh sách ---
frame_table = tk.Frame(root)
frame_table.pack(fill="both", expand=True, padx=10, pady=10)

columns = ("MaDanhMuc", "TenDanhMuc", "MoTa", "TrangThai")
tree = ttk.Treeview(frame_table, columns=columns, show="headings")

tree.heading("MaDanhMuc", text="Mã")
tree.heading("TenDanhMuc", text="Tên danh mục")
tree.heading("MoTa", text="Mô tả")
tree.heading("TrangThai", text="Trạng thái")

tree.column("MaDanhMuc", width=60, anchor="center")
tree.column("TenDanhMuc", width=200)
tree.column("MoTa", width=250)
tree.column("TrangThai", width=100, anchor="center")

tree.pack(fill="both", expand=True)
tree.bind("<ButtonRelease-1>", select_row)

# --- Tải dữ liệu ban đầu ---
load_danhmuc()

root.mainloop()
