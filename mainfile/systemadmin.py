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
    
def mainsystemadmin():
    servername = 'localhost'
    username = 'sa'
    password = '123456'
    dbname = 'Plant_management'
    dao = DatabaseDAO(servername, username, password, dbname)
    dao.connect()
    if dao.is_connected():
        print("连接相关数据库成功\n")
    while True:
        print("系统管理员，欢迎您的登录！\n")
        print("1.查看系统人员\n")
        print("2.联合查看植物分类业务，养护业务和监测业务\n")
        print("3.退出\n")
        choicenumber=int(input("请输入您的选项"))
        if choicenumber==1:
            sql=f'select * from users'
            result=dao.execute_query(sql)
            print(result)
        if choicenumber==2:
            sql=f'select * from Plants join EMI ON Plants.plants_number=EMI.mpno join plant_care on Plants.plants_number=plant_care.object_id'
            result=dao.execute_query(sql)
            print(result)
        if choicenumber==3:
            break
