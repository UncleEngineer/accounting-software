from tkinter import *
from tkinter import ttk
import csv
import re

GUI = Tk()
GUI.title('โปรแกรมบัญชีลุง')
GUI.geometry('700x500')

FONT1 = (None, 18)

LH1 = Label(GUI, text='โปรแกรมบัญชีลุง', font=(None, 20, 'bold'), fg='green')
LH1.pack(pady=20)

# ------------customer-------------
L1 = Label(GUI, text='ลูกค้า', font=FONT1)
L1.pack()
v_customer = StringVar()
E1 = ttk.Entry(GUI, textvariable=v_customer, font=FONT1)
E1.pack()

# ------------address-------------
L2 = Label(GUI, text='ที่อยู่', font=FONT1)
L2.pack()
v_address = StringVar()
E2 = ttk.Entry(GUI, textvariable=v_address, font=FONT1, width=40)
E2.pack()

# ------------taxid-------------
L3 = Label(GUI, text='เลขที่ประจำตัวผู้เสียภาษี', font=FONT1)
L3.pack()
v_taxid = StringVar()
E3 = ttk.Entry(GUI, textvariable=v_taxid, font=FONT1)
E3.pack()

# ------------tel-------------
L4 = Label(GUI, text='โทร', font=FONT1)
L4.pack()
v_tel = StringVar()
E4 = ttk.Entry(GUI, textvariable=v_tel, font=FONT1)
E4.pack()

# ------------email-------------
L5 = Label(GUI, text='อีเมล', font=FONT1)
L5.pack()
v_email = StringVar()
E5 = ttk.Entry(GUI, textvariable=v_email, font=FONT1)
E5.pack()

# ข้อความแจ้งเตือนสำหรับการกรอกข้อมูลที่ไม่ถูกต้อง
error_tel = Label(GUI, text='* หมายเลขโทรศัพท์ไม่ถูกต้อง', font=FONT1, fg='red')
error_tel.place(x=150, y=230)  # ตั้งตำแหน่งของข้อความแจ้งเตือนโทรศัพท์
error_tel.place_forget()  # ซ่อนข้อความเริ่มต้น

error_email = Label(GUI, text='* อีเมลไม่ถูกต้อง', font=FONT1, fg='red')
error_email.place(x=150, y=280)  # ตั้งตำแหน่งของข้อความแจ้งเตือนอีเมล
error_email.place_forget()  # ซ่อนข้อความเริ่มต้น

# ฟังก์ชันตรวจสอบรูปแบบของอีเมล
def validate_email(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

# ฟังก์ชันตรวจสอบรูปแบบของหมายเลขโทรศัพท์
def validate_tel(tel):
    tel_regex = r'^\d{10}$'  # โทรศัพท์ไทย 10 หลัก
    return re.match(tel_regex, tel) is not None

def save():
    # get all variables
    customer = v_customer.get()
    address = v_address.get()
    taxid = v_taxid.get()
    tel = v_tel.get()
    email = v_email.get()

    # ตรวจสอบอีเมล
    if not validate_email(email):
        error_email.place(x=150, y=280)  # แสดงข้อความเตือนอีเมลไม่ถูกต้อง
    else:
        error_email.place_forget()  # ซ่อนข้อความเตือนอีเมลเมื่อถูกต้อง

    # ตรวจสอบหมายเลขโทรศัพท์
    if not validate_tel(tel):
        error_tel.place(x=150, y=230)  # แสดงข้อความเตือนโทรศัพท์ไม่ถูกต้อง
    else:
        error_tel.place_forget()  # ซ่อนข้อความเตือนโทรศัพท์เมื่อถูกต้อง

    # ถ้าทั้งอีเมลและโทรศัพท์ถูกต้อง
    if validate_email(email) and validate_tel(tel):
        # clear fields
        v_customer.set('')
        v_address.set('')
        v_taxid.set('')
        v_tel.set('')
        v_email.set('')
        E1.focus()

        # save to csv
        with open('customer.csv', 'a', newline='', encoding='utf-8') as file:
            fw = csv.writer(file)
            data = [customer, address, taxid, tel, email]
            fw.writerow(data)
            print('บันทึกสำเร็จ')

B1 = ttk.Button(GUI, text='บันทึก', command=save)
B1.pack(pady=20, ipady=20, ipadx=10)

GUI.mainloop()
