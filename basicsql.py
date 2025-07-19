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


# with conn:
#     c.execute('INSERT INTO customer VALUES (?,?,?,?,?,?)',(None,'ลุง2','พหลโยธิน สามเสนใน กรุงเทพ','0107778889999','0812345678','loong@gmail.com'))
#     conn.commit()
def insert_customer(name,address,taxid,tel,email):
    with conn:
        command = 'INSERT INTO customer VALUES (?,?,?,?,?,?)'
        c.execute(command,(None,name,address,taxid,tel,email))
        conn.commit()
    print('saved')

# insert_customer('สมชาย','เชียงใหม่','0108889997777','0809876543','somchai@gmail.com')

# with conn:
#     c.execute('SELECT * FROM customer')
#     result = c.fetchall()
#     print(result)


def view_customer():
    with conn:
        c.execute('SELECT * FROM customer')
        result = c.fetchall()
        return result
    
result = view_customer()
# print(result[0])
for r in result:
    print(r)