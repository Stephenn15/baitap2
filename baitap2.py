import psycopg2
from psycopg2 import sql
import tkinter as tk
from tkinter import messagebox

# Kết nối tới cơ sở dữ liệu
def connect_to_db(user, password, host, dbname):
    try:
        conn = psycopg2.connect(
            user='postgres',
            password='123456',
            host='localhost',
            dbname='tung'
        )
        return conn
    except Exception as e:
        print(f"Error: {e}")
        return None

# Hàm đăng nhập
def login():
    user = entry_user.get()
    password = entry_password.get()
    host = "localhost"  # Thay đổi nếu cần
    dbname = "tung"

    conn = connect_to_db(user, password, host, dbname)
    if conn:
        cursor = conn.cursor()
        # Kiểm tra xem tài khoản có tồn tại trong bảng users không
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (user, password))
        user_data = cursor.fetchone()

        if user_data:
            messagebox.showinfo("Login", "Login successful!")
            show_main_menu(conn)
        else:
            messagebox.showerror("Login", "Invalid username or password.")
    else:
        messagebox.showerror("Login", "Failed to connect to the database.")

# Hàm đăng ký
def register():
    def save_registration():
        username = entry_new_user.get()
        password = entry_new_password.get()

        if username and password:
            conn = connect_to_db("postgres", "123456", "localhost", "tung")
            if conn:
                cursor = conn.cursor()

                # Thêm thông tin người dùng mới vào bảng users
                try:
                    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
                    conn.commit()
                    messagebox.showinfo("Register", "Registration successful!")
                    reg_window.destroy()  # Đóng cửa sổ đăng ký sau khi thành công
                except Exception as e:
                    messagebox.showerror("Register", f"Error: {e}")
                finally:
                    cursor.close()
                    conn.close()
        else:
            messagebox.showwarning("Register", "Please fill in all fields!")

    # Cửa sổ đăng ký
    reg_window = tk.Toplevel(root)
    reg_window.title("Register")

    tk.Label(reg_window, text="Username:").pack()
    entry_new_user = tk.Entry(reg_window)
    entry_new_user.pack()

    tk.Label(reg_window, text="Password:").pack()
    entry_new_password = tk.Entry(reg_window, show="*")
    entry_new_password.pack()

    tk.Button(reg_window, text="Register", command=save_registration).pack()

# Chức năng thêm sinh viên mới
def add_student(conn):
    add_window = tk.Toplevel(root)
    add_window.title("Add New Student")

    tk.Label(add_window, text="Name:").pack()
    name_entry = tk.Entry(add_window)
    name_entry.pack()

    tk.Label(add_window, text="Email:").pack()
    email_entry = tk.Entry(add_window)
    email_entry.pack()

    tk.Label(add_window, text="Age:").pack()
    age_entry = tk.Entry(add_window)
    age_entry.pack()

    def save_student():
        name = name_entry.get()
        email = email_entry.get()
        age = age_entry.get()

        if name and email and age:
            cursor = conn.cursor()
            query = "INSERT INTO students (name, email, age) VALUES (%s, %s, %s)"
            cursor.execute(query, (name, email, age))
            conn.commit()

            messagebox.showinfo("Success", "Student added successfully!")
            add_window.destroy()
            cursor.close()
        else:
            messagebox.showwarning("Input Error", "Please fill in all fields!")

    tk.Button(add_window, text="Add", command=save_student).pack()

# Hiển thị menu chính
def show_main_menu(conn):
    main_window = tk.Toplevel(root)
    main_window.title("Main Menu")

    tk.Button(main_window, text="Search Students", command=lambda: search_students(conn)).pack()
    tk.Button(main_window, text="Add New Student", command=lambda: add_student(conn)).pack()


# Giao diện đăng nhập
root = tk.Tk()
root.title("Login")

tk.Label(root, text="Username").pack()
entry_user = tk.Entry(root)
entry_user.pack()

tk.Label(root, text="Password").pack()
entry_password = tk.Entry(root, show="*")
entry_password.pack()

tk.Button(root, text="Login", command=login).pack()
tk.Button(root, text="Register", command=register).pack()  # Nút đăng ký

root.mainloop()
