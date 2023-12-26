import pymssql
class DatabaseDAO:
    def __init__(self, servername, username, password, dbname):
        self.servername = servername
        self.username = username
        self.password = password
        self.dbname = dbname
        self.conn = None

    def connect(self):
        self.conn = pymssql.connect(self.servername, self.username, self.password, self.dbname)

    def is_connected(self):
        return self.conn is not None

    def execute_query(self, sql):
        cursor = self.conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result
    
    def execute_insert(self, sql, data):
        cursor = self.conn.cursor()
        cursor.execute(sql, data)
        self.conn.commit()
        cursor.close()
    
    def execute_delete(self, sql,plants_number):
        cursor = self.conn.cursor()
        cursor.execute(sql,plants_number)
        self.conn.commit()
        cursor.close()

    def execute_update(self, sql,plants_number):
        cursor = self.conn.cursor()
        cursor.execute(sql,plants_number)
        self.conn.commit()
        cursor.close()

    

print("1:增加植物分类信息\n")
print("2:删除植物分类信息\n")
print("3:修改植物分类信息\n")
print("4:查询植物分类信息\n")

controlnumber=int(input("请选择您想要执行的植物分类操作:\n"))

# 连接分类数据库的函数
servername = 'localhost'
username = 'sa'
password = '123456'
dbname = 'Landscape Plant Management System'

dao = DatabaseDAO(servername, username, password, dbname)
dao.connect()
if dao.is_connected():
    print("连接相关数据库成功\n")

    if controlnumber==1:
        print("请输入植物的编号，科名，属名，种名，名称以及别名\n")
        firstnumber=input("植物编号")
        first1=input("科名")
        first2=input("属名")
        first3=input("种名")
        first4=input("名称")
        first5=input("别名")
        print("接着输入植物的生长环境\n")
        second=input()
        print("接着输入植物的分布区域(省市县)\n")
        third=input()
    
        sql = "INSERT INTO Plants (plants_number, plants_name, other_name, growing_environment, distribution_area_number, belong_species) \
VALUES (%s, %s, %s, %s, %s, %s)"
        data = (firstnumber, first4, first5, second, third, first3)
        dao.execute_insert(sql,data)

        sql = "INSERT INTO Section (Section number,chinese_name,English_name) \
VALUES (%s, %s, %s)"
        data = (first1, "中文名","englishname")
        dao.execute_insert(sql,data)

        sql="select * from Plants"
        result=dao.execute_query(sql)
        print(result)

        sql="select * from Section"
        result=dao.execute_query(sql)
        print(result)

if controlnumber==2:
    print("请输出您想要删除的植物的编号")
    number=input("请输入四位的植物编号")
    sql=f"DELETE FROM Plants WHERE plants_number={number}"
    dao.execute_delete(sql,number)

if controlnumber==3:
    print("请输出您想要修改的植物的编号")
    number=input("请输入四位的植物编号")
    print("请输出您想要修改的植物的内容")
    sql=f"UPDATE plants SET plant_name = 'Rose' WHERE plant_number ={number};"
    dao.execute_update(sql,number)

if controlnumber==4:
    print("直接查询请按1\n")
    print("根据生长环境查询请按2\n")
    print("制定属性查询下属属性请按3\n")
    newnumber=int(input("请输入数字\n"))
    if newnumber==1:
        print("请输入您想要查询的植物的编号")
        plantnumber=input()
        sql=f"select * from plants where plants_number={plantnumber}"
        result=dao.execute_query(sql)
        print(result)

    if newnumber==2:
        print("请输入您想要查询的植物的部分生长环境")
        test=input()
        sql = f"SELECT * FROM plants WHERE environment_description LIKE '%{test}%'"
        result = dao.execute_query(sql)
        print(result)

    if newnumber==3:
        print("请输入相关内容")
        test=input()


