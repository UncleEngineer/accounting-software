from tkinter import *
from tkinter import ttk
import csv

############ SQL ##############################################
import sqlite3

conn = sqlite3.connect('company.sqlite3')

c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS customer (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            address TEXT,
            taxid TEXT,
            tel TEXT,
            email TEXT
            )""")

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
    
def find_customer_by_name(name):
    with conn:
        c.execute('SELECT * FROM customer WHERE name=?', (name,))
        result = c.fetchone()
        return result #ถ้าพบจะได้ tuple , ไม่เจอจะได้ None
    
#################### DB T2 ######################################

c.execute("""CREATE TABLE IF NOT EXISTS taxinvoice (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            bill_no TEXT,
            name TEXT,
            address TEXT,
            taxid TEXT,
            tel TEXT,
            email TEXT,
            remark TEXT,
            code TEXT,
            product TEXT,
            price TEXT,
            number TEXT
            )""")

def insert_taxinvoice(bill_no,name,address,taxid,tel,email,remark,code,product,price,number):
    with conn:
        command = 'INSERT INTO taxinvoice VALUES (?,?,?,?,?,?,?,?,?,?,?,?)'
        c.execute(command,(None,bill_no,name,address,taxid,tel,email,remark,code,product,price,number))
        conn.commit()
    print('save2')

# insert_taxinvoice('123456789','c','bangkok','987654321','022222222','','','','','','')
def view_taxinvoice():
    with conn:
        c.execute('SELECT * FROM taxinvoice')
        result = c.fetchall()
        return result

    
###################################################################

GUI = Tk()
GUI.title('โปรแกรมบัญชีลุง')
GUI.geometry('1500x700')

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

LH1 = Label(F1,text='โปรแกรมบัญชีลุง', font=(None,20,'bold'),fg='green')
LH1.pack(pady=20)

#---------------customer-------------------#
L1 = Label(F1,text='ลูกค้า',font=FONT1)
L1.pack()
v_customer = StringVar()
E1 = ttk.Entry(F1,textvariable=v_customer,font=FONT1)
E1.pack()

#----------------address---------------------#
L2 = Label(F1,text='ที่อยู่',font=FONT1)
L2.pack()
v_address = StringVar()
E2 = ttk.Entry(F1,textvariable=v_address,font=FONT1,width=40)
E2.pack()

#----------------taxid---------------------#
L3 = Label(F1,text='เลขประจำตัวผู้เสียภาษี',font=FONT1)
L3.pack()
v_taxid = StringVar()
E3 = ttk.Entry(F1,textvariable=v_taxid,font=FONT1)
E3.pack()

#----------------tel---------------------#
L4 = Label(F1,text='โทร',font=FONT1)
L4.pack()
v_tel = StringVar()
E4 = ttk.Entry(F1,textvariable=v_tel,font=FONT1)
E4.pack()

#----------------email---------------------#
L5 = Label(F1,text='อีเมล',font=FONT1)
L5.pack()
v_email = StringVar()
E5 = ttk.Entry(F1,textvariable=v_email,font=FONT1)
E5.pack()

def save():
    # get all variable
    customer = v_customer.get()
    address =  v_address.get()
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
    if not(customer == '' or address == '' or taxid == '' or tel == ''):
        insert_customer(customer,address,taxid,tel,email)
    result = view_customer()
    print('----------------')
    for r in result:
        print(r)
    print('----------------')
    update_table() # update table after saved

B1 = ttk.Button(F1,text='บันทึก',command=save)
B1.pack(pady=20,ipady=20,ipadx=10)

######################TREEVIEW1#######################
F2 = Frame(T1)
F2.place(x=50,y=50)

columns = ['ชื่อลูกค้า','ที่อยู่','Tax ID','เบอร์โทร','อีเมล์']
cw = [100,150,100,82,100]

table = ttk.Treeview(F2,columns=columns,show='headings',height=25)
for w,col in zip(cw,columns):
    table.heading(col,text=col)
    table.column(col,width=w)
table.pack()

def update_table():
    #clear data in table
    for item in table.get_children():
        # print('item in table : ',item,table.get_children())
        table.delete(item)

    result = view_customer()
    for r in result:
        table.insert('','end',values=r[1:])

update_table()

############# ใบกำกับภาษี ##################

F3 = Frame(T2)
F3.place(x=1300,y=20)

FONT2 = (None,14)
FONT3 = (None,12)
#### Toplevel เพิ่มรายการสินค้า #############
topright_button = ttk.Button(F3, text='+', width=3, command=lambda: open_toplevel_window())
topright_button.pack(pady=5)

# LH2 = Label(F3,text='ใบกำกับภาษี', font=(None,20,'bold'), fg='orange')
# LH2.pack(pady=10)

F4 = Frame(T2)
F4.place(x=650,y=0)

#---------- bill NO -------------------#
L2_0 = Label(F4, text='เลขที่ใบกำกับภาษี', font=FONT2)
L2_0.grid(row=0,column=0, sticky=W,padx=10)

v_bill2 = StringVar()
v_bill2.set('2568/08-001')
E2_0 = ttk.Entry(F4, textvariable=v_bill2, font=FONT3, width=13)
E2_0.grid(row=0,column=1, sticky=W)

#---------- Customer -------------------#
L2_1 = Label(F4, text='ลูกค้า', font=FONT2)
L2_1.grid(row=1,column=0, sticky=W,padx=10)
v_customer2 = StringVar()
E2_1 = ttk.Entry(F4, textvariable=v_customer2, font=FONT3)
E2_1.grid(row=1,column=1, sticky=W)

#---------- address -------------------#
L2_2 = Label(F4, text='ที่อยู่', font=FONT2)
L2_2.grid(row=2,column=0, sticky=W,padx=10)
v_address2 = StringVar()
E2_2 = ttk.Entry(F4, textvariable=v_address2, font=FONT3, width=40)
E2_2.grid(row=2,column=1, sticky=W)

#---------- taxid -------------------#
L2_3 = Label(F4, text='เลขประจำตัวผู้เสียภาษี', font=FONT2)
L2_3.grid(row=3,column=0, sticky=W,padx=10)
v_taxid2 = StringVar()
E2_3 = ttk.Entry(F4, textvariable=v_taxid2, font=FONT2)
E2_3.grid(row=3,column=1, sticky=W)

#---------- tel -------------------#
L2_4 = Label(F4, text='โทร', font=FONT2)
L2_4.grid(row=4,column=0, sticky=W,padx=10)
v_tel2 = StringVar()
E2_4 = ttk.Entry(F4, textvariable=v_tel2, font=FONT2)
E2_4.grid(row=4,column=1, sticky=W)

#---------- email -------------------#
# L2_5 = Label(F4, text='อีเมล์', font=FONT2)
# L2_5.grid(row=5,column=0, sticky=W,padx=10)
# v_email2 = StringVar()
# E2_5 = ttk.Entry(F4, textvariable=v_email2, font=FONT2)
# E2_5.grid(row=5,column=1, sticky=W)

# #---------- remark -------------------#
# L2_6 = Label(F4, text='หมายเหตุ', font=FONT2)
# L2_6.grid(row=6,column=0, sticky=W,padx=10)
# v_remark2 = StringVar()
# E2_6 = ttk.Entry(F4, textvariable=v_remark2, font=FONT2)
# E2_6.grid(row=6,column=1, sticky=W)

#----------- save Button -------------------#



FT2 = Frame(T2)
FT2.place(x=650,y=180)

columns = ['รหัสสินค้า','ชื่อสินค้า','ราคา','จำนวนสินค้า','รวม']
cw = [100,250,100,100,100]

table_taxinvoice = ttk.Treeview(FT2,columns=columns,show='headings',height=13)
for w,col in zip(cw,columns):
    table_taxinvoice.heading(col,text=col)
    table_taxinvoice.column(col,width=w)
table_taxinvoice.pack()



# ---------- Calculate -------------------#
F5 = Frame(T2)
F5.place(x=1000,y=500)

# v_ex_vat,v_vat,v_in_vat

L = Label(F5,text='ราคารวม').grid(row=0,column=0,sticky=W)
v_ex_vat = StringVar() # Ex Vat
v_ex_vat.set('')

L_ex_vat = Label(F5, textvariable=v_ex_vat, font=FONT2)
L_ex_vat.grid(row=0, column=1,sticky=E)

L = Label(F5,text='ภาษี 7%').grid(row=1, column=0,sticky=W)
v_vat = StringVar() # Vat
v_vat.set('')

L_vat = Label(F5, textvariable=v_vat, font=FONT2)
L_vat.grid(row=1, column=1,sticky=E)

L = Label(F5,text='จำนวนเงินรวมทั้งสิ้น').grid(row=2, column=0,sticky=W)
v_in_vat = StringVar() # Vat
v_in_vat.set('')

L_in_vat = Label(F5, textvariable=v_in_vat, font=FONT2)
L_in_vat.grid(row=2, column=1,sticky=E)

B2 = ttk.Button(F5, text='บันทึก', command=lambda: save_taxinvoice())
B2.grid(row=3, column=0)

#---- กด Enter แล้วเรียกดูข้อมูลลูกค้า ---------------#
def autofill_customer(event=None):
    name = v_customer2.get()
    result = find_customer_by_name(name)
    if result:
        v_address2.set(result[2])
        v_taxid2.set(result[3])
        v_tel2.set(result[4])
        v_email2.set(result[5])

E2_1.bind('<Return>',autofill_customer) # เมื่อกด Enter



#--------------- save taxinvoice -----------------------#
def save_taxinvoice():

    # get all variable
    bill2 = v_bill2.get()
    customer2 = v_customer2.get()
    address2 = v_address2.get()
    taxid2 = v_taxid2.get()
    tel2 = v_tel2.get()
    email2 = v_email2.get()
    remark2 = v_remark2.get()
    code = v_code.get()
    product = v_product.get()
    price = v_price.get()
    num = v_num.get()

    # clear
    v_bill2.set('')
    v_customer2.set('')
    v_address2.set('')
    v_taxid2.set('')
    v_tel2.set('')
    v_email2.set('')
    v_remark2.set('')
    v_code.set('')
    v_product.set('')
    v_price.set('')
    v_num.set('')
    v_ex_vat.set('')
    v_vat.set('')
    v_in_vat.set('')
    E2_0.focus()

    # save to sql
    if not(bill2 == '' or customer2 == '' or address2 == '' or taxid2 == '' or code == ''):
        insert_taxinvoice(bill2,customer2,address2,taxid2,tel2,email2,remark2,code,product,price,num)
    
    result2 = view_taxinvoice()
    print('--------------')
    for r in result2:
        print(r)
    print('---------------')

    update_table2()





#-------------- TopLevel -----------------------#
v_code = StringVar()
v_product = StringVar()
v_price = StringVar()
v_num = StringVar()

table_taxinvoice_list = []

def open_toplevel_window():
    top = Toplevel()
    top.title('เพิ่มรายการสินค้า')
    top.geometry('500x500+700+200')

    LT1 = Label(top, text='เพิ่มรายการสินค้า', font=FONT1, fg='red')
    LT1.pack(pady=20)
    # ['รหัสสินค้า','ชื่อสินค้า','ราคา','จำนวนสินค้า','รวม']
    LT2 = Label(top, text='รหัสสินค้า', font=FONT1)
    LT2.pack()
    ET2 = Entry(top, textvariable=v_code, font=FONT1)
    ET2.pack()

    LT3 = Label(top, text='ชื่อสินค้า', font=FONT1)
    LT3.pack()
    ET3 = Entry(top, textvariable=v_product, font=FONT1)
    ET3.pack()

    LT4 = Label(top, text='ราคา', font=FONT1)
    LT4.pack()
    ET4 = Entry(top, textvariable=v_price, font=FONT1)
    ET4.pack()

    LT5 = Label(top, text='จำนวนสินค้า', font=FONT1)
    LT5.pack()
    ET5 = Entry(top, textvariable=v_num, font=FONT1)
    ET5.pack()

    def submit_and_close():
        code = v_code.get()
        product = v_product.get()
        price = float(v_price.get())
        quantity = float(v_num.get())
        total = price * quantity

        data = [code,product,price,quantity,total]
        table_taxinvoice.insert('','end',values=data)
        table_taxinvoice_list.append(data)
        print('TABLE:',data)
        sum_subtotal = sum([ d[-1] for d in table_taxinvoice_list]) # รวมคอลัมน์สุดท้ายของตาราง
        cal_vat = sum_subtotal * 0.07
        total = sum_subtotal + cal_vat

        # v_ex_vat,v_vat,v_in_vat
        v_ex_vat.set(sum_subtotal)
        v_vat.set(cal_vat)
        v_in_vat.set(total)


        

        


    BT = Button(top, text='ยืนยัน', width=10, command=submit_and_close)
    BT.pack(pady=30)

#------------ TREEVIEW2 --------------#
F4 = Frame(T2)
F4.place(x=50,y=50)

columns2 = ['ชื่อลูกค้า','เลขที่ใบกำกับภาษี','Tax ID']
cw2 = [200,160,160]

table2 = ttk.Treeview(F4,columns=columns2,show='headings',height=25)
for w,col in zip(cw2,columns2):
    table2.heading(col,text=col)
    table2.column(col,width=w)
table2.pack()

def update_table2():
    #clear data in table
    for item in table2.get_children():
        # print('item in table : ',item,table.get_children())
        table2.delete(item)

    result2 = view_taxinvoice()
    for r in result2:
        table2.insert('','end',values=[r[2],r[1],r[4]])
    

update_table2()

GUI.mainloop()
