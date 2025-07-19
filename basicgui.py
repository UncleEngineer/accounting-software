from tkinter import *
from tkinter import ttk
import csv
#########################SQL#########################
import sqlite3

# สร้างฐานข้อมูล(กรณีที่ยังไม่มี) แล้วเชื่อมต่อกับฐานข้อมูล
conn = sqlite3.connect('company.sqlite3')

# สร้างตัวดำเนินการ
c = conn.cursor()

# สร้างตารางเก็บข้อมูลของรายชื่อลูกค้า
c.execute("""CREATE TABLE IF NOT EXISTS customer (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                address TEXT,
                taxid TEXT,
                tel TEXT,
                email TEXT)""")

def insert_customer(name,address,taxid,tel,email):
    with conn:
        command = 'INSERT INTO customer VALUES (?,?,?,?,?,?)'
        c.execute(command,(None,name,address,taxid,tel,email))
        conn.commit()
    print('saved')

def view_customer():
    with conn:
        c.execute('SELECT * FROM customer')
        result = c.fetchall()
        return result
##################################################
GUI = Tk()
GUI.title('โปรแกรมบัญชีลุง')
GUI.geometry('1200x700')

Tab = ttk.Notebook(GUI)
T1 = Frame(Tab)
T2 = Frame(Tab)
T3 = Frame(Tab)
Tab.pack(fill=BOTH,expand=1)

Tab.add(T1,text='ข้อมูลลูกค้า')
Tab.add(T2,text='ใบกำกับภาษี')
Tab.add(T3,text='ใบเสนอราคา')


F1 = Frame(T1)
F1.place(x=600,y=50)


FONT1 = (None,18)

LH1 = Label(F1,text='โปรแกรมบัญชีลุง',font=(None,20,'bold'),fg='green')
LH1.pack(pady=20)

# ------------customer-------------
L1 = Label(F1,text='ลูกค้า',font=FONT1)
L1.pack()
v_customer = StringVar()
E1 = ttk.Entry(F1,textvariable=v_customer,font=FONT1)
E1.pack()
# ------------address-------------
L2 = Label(F1,text='ที่อยู่',font=FONT1)
L2.pack()
v_address = StringVar()
E2 = ttk.Entry(F1,textvariable=v_address,font=FONT1,width=40)
E2.pack()
# ------------taxid-------------
L3 = Label(F1,text='เลขที่ประจำตัวผู้เสียภาษี',font=FONT1)
L3.pack()
v_taxid = StringVar()
E3 = ttk.Entry(F1,textvariable=v_taxid,font=FONT1)
E3.pack()
# ------------tel-------------
L4 = Label(F1,text='โทร',font=FONT1)
L4.pack()
v_tel = StringVar()
E4 = ttk.Entry(F1,textvariable=v_tel,font=FONT1)
E4.pack()
# ------------email-------------
L5 = Label(F1,text='อีเมล',font=FONT1)
L5.pack()
v_email = StringVar()
E5 = ttk.Entry(F1,textvariable=v_email,font=FONT1)
E5.pack()

def save():
    # get all variables
    customer = v_customer.get()
    address = v_address.get()
    taxid = v_taxid.get()
    tel = v_tel.get()
    email = v_email.get()
    # clear
    v_customer.set('')
    v_address.set('')
    v_taxid.set('')
    v_tel.set('')
    v_email.set('')
    E1.focus()
    # save to sql
    insert_customer(customer,address,taxid,tel,email)
    result = view_customer()
    print('------------------------')
    for r in result:
        print(r)
    print('------------------------')
    update_table() # update table after saved
    
    
B1 = ttk.Button(F1,text='บันทึก',command=save)
B1.pack(pady=20,ipady=20,ipadx=10)

#######################TREEVIEW##########################
F2 = Frame(T1)
F2.place(x=50,y=50)

columns = ['ชื่อลูกค้า','ที่อยู่','Tax ID','เบอร์โทร','อีเมล']
cw = [100,150,100,80,100]

table = ttk.Treeview(F2,columns=columns, show='headings',height=25)
for w,col in zip(cw,columns):
    table.heading(col,text=col)
    table.column(col,width=w)
table.pack()

def update_table():
    #clear data in table
    for item in table.get_children():
        table.delete(item)

    result = view_customer()
    for r in result:
        #print(r[1:])
        table.insert('','end',values=r[1:])


update_table()

GUI.mainloop()
