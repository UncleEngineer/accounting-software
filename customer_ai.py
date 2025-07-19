import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

# ฟังก์ชันสำหรับเชื่อมต่อกับฐานข้อมูล SQLite3 และสร้างตารางถ้ายังไม่มี
def create_table():
    conn = sqlite3.connect('customers.db')
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        address TEXT,
        taxid TEXT,
        phone TEXT,
        email TEXT
    )
    ''')
    conn.commit()
    conn.close()

# ฟังก์ชันสำหรับเพิ่มข้อมูลลูกค้าในฐานข้อมูล
def insert_data():
    name = entry_name.get()
    address = entry_address.get()
    taxid = entry_taxid.get()
    phone = entry_phone.get()
    email = entry_email.get()

    if name and address and taxid and phone and email:
        conn = sqlite3.connect('customers.db')
        c = conn.cursor()
        c.execute('''
        INSERT INTO customers (name, address, taxid, phone, email) 
        VALUES (?, ?, ?, ?, ?)
        ''', (name, address, taxid, phone, email))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "ข้อมูลลูกค้าถูกบันทึกแล้ว")
        clear_fields()
        load_data()
    else:
        messagebox.showwarning("Input Error", "กรุณากรอกข้อมูลให้ครบถ้วน")

# ฟังก์ชันสำหรับโหลดข้อมูลลูกค้าจากฐานข้อมูลมาแสดงใน Treeview
def load_data():
    for row in tree.get_children():
        tree.delete(row)
    
    conn = sqlite3.connect('customers.db')
    c = conn.cursor()
    c.execute("SELECT * FROM customers")
    rows = c.fetchall()
    for row in rows:
        tree.insert("", tk.END, values=row[1:])
    conn.close()

# ฟังก์ชันสำหรับเคลียร์ข้อมูลในฟอร์ม
def clear_fields():
    entry_name.delete(0, tk.END)
    entry_address.delete(0, tk.END)
    entry_taxid.delete(0, tk.END)
    entry_phone.delete(0, tk.END)
    entry_email.delete(0, tk.END)

# สร้างหน้าต่างหลัก
root = tk.Tk()
root.title("Customer Information")
root.geometry("1000x700")  # กำหนดขนาดหน้าต่าง

# สร้าง Frame หลักที่แบ่งเป็นสองส่วน: ด้านซ้ายสำหรับ Treeview และ ด้านขวาสำหรับฟอร์ม
main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)

# สร้าง Frame สำหรับ Treeview (ด้านซ้าย) ขนาดกว้าง 500px
left_frame = tk.Frame(main_frame, width=500)
left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

# สร้าง Treeview สำหรับแสดงข้อมูล
columns = ("Name", "Address", "Tax ID", "Phone", "Email")
tree = ttk.Treeview(left_frame, columns=columns, show="headings")
tree.pack(fill=tk.Y, expand=True)

# กำหนดชื่อหัวตาราง
for col in columns:
    tree.heading(col, text=col)
    tree.column(col,width=120)

# สร้าง Frame สำหรับฟอร์ม (ด้านขวา)
right_frame = tk.Frame(main_frame)
right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

# สร้างฟอร์มสำหรับกรอกข้อมูลลูกค้า
tk.Label(right_frame, text="Name").grid(row=0, column=0, padx=5, pady=5)
entry_name = tk.Entry(right_frame)
entry_name.grid(row=0, column=1, padx=5, pady=5)

tk.Label(right_frame, text="Address").grid(row=1, column=0, padx=5, pady=5)
entry_address = tk.Entry(right_frame)
entry_address.grid(row=1, column=1, padx=5, pady=5)

tk.Label(right_frame, text="Tax ID").grid(row=2, column=0, padx=5, pady=5)
entry_taxid = tk.Entry(right_frame)
entry_taxid.grid(row=2, column=1, padx=5, pady=5)

tk.Label(right_frame, text="Phone").grid(row=3, column=0, padx=5, pady=5)
entry_phone = tk.Entry(right_frame)
entry_phone.grid(row=3, column=1, padx=5, pady=5)

tk.Label(right_frame, text="Email").grid(row=4, column=0, padx=5, pady=5)
entry_email = tk.Entry(right_frame)
entry_email.grid(row=4, column=1, padx=5, pady=5)

# ปุ่มสำหรับบันทึกข้อมูล
btn_save = tk.Button(right_frame, text="Save", command=insert_data)
btn_save.grid(row=5, columnspan=2, pady=10)

# โหลดข้อมูลเริ่มต้นจากฐานข้อมูล
load_data()

# เรียกฟังก์ชันสร้างตารางฐานข้อมูลเมื่อเริ่มโปรแกรม
create_table()

# เริ่มโปรแกรม
root.mainloop()
