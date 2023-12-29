import pymssql
import basic_information
import monitoring
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

class PlantDB:
    def __init__(self):
        self.conn = pymssql.connect(
        server='localhost',
        user='sa',
        password='123456',
        database='Plant_management'
    )
        self.cursor = self.conn.cursor()

    def add_picture(self):
        picture_number = input("请输入图片编号：")
        picture_people = input("请输入图片拍摄人员：")
        picture_place = input("请输入图片拍摄地点:")
        picture_description = input("请输入图片描述：")
        load_place = input("请输入图片加载地点：")
        self.cursor.execute('SELECT * FROM Plants_picture WHERE [picture_number]=%s', (picture_number,))
        existing_number = self.cursor.fetchone()

        if existing_number:
            print("已存在相同编号的图片！")
            return
        self.cursor.execute('''
        INSERT INTO Plants_picture (picture_number, picture_people, picture_place, picture_description, load_place)
            VALUES (%s, %s, %s, %s, %s)
        ''', (picture_number, picture_people, picture_place, picture_description, load_place))
        self.conn.commit()
        print("图片信息已成功添加！")
        print("--------------------------------")

    def get_pictures(self):
        picture_number=input("请输入图片编号: ")
        self.cursor.execute('SELECT * FROM Plants_picture WHERE picture_number=%s', (picture_number,))
        picture = self.cursor.fetchall()
        if picture:
            for row in picture:
                print("--------------------------------")
                print(f"图片编号: {row[0]}")
                print(f"图片拍摄人员: {row[1]}")
                print(f"图片地点: {row[2]}")
                print(f"图片描述: {row[3]}")
                print(f"拍摄地点: {row[4]}")
                print("--------------------------------")
        else:
            print("未找到该图片！")


    def __del__(self):
        self.cursor.close()
        self.conn.close()

# 使用示例
def picture():
    plant=PlantDB()                              #添加植物图片信息
    while True:
        print("请选择操作：")
        print("1. 添加图片")
        print("2. 查询图片")
        print("3.退出")
        choice = input("请输入操作编号: \n")
        if choice == "1":
            plant.add_picture()
        elif choice == "2":
            plant.get_pictures()
        elif choice=="3":
            break


def classfication():
    servername = 'localhost'
    username = 'sa'
    password = '123456'
    dbname = 'Plant_management'
    dao = DatabaseDAO(servername, username, password, dbname)
    dao.connect()
    if dao.is_connected():
        print("连接相关数据库成功\n")
    while True:
        print("1:增加植物分类信息\n")
        print("2:删除植物分类信息\n")
        print("3:修改植物分类信息\n")
        print("4:查询植物分类信息\n")
        print("5:退出")
        controlnumber=int(input("请选择您想要执行的植物分类操作:\n"))
        if controlnumber==1:
            print("由于录入信息过多，请您耐心录入\n")
            
            Section=input("请输入科名\n")
            Sectionnumber=input("请输入科编号")

            Genus=input("请输入属名")
            Genusnumber=input("请输入属编号")

            Species=input("请输入种名")
            Speciesnumber=input("请输入种编号")

            plant_number=input("请输入植物编号")
            plant_name=input("请输入植物名称")
            plant_othername=input("请输入植物别名")

            print("接着输入植物的生长环境\n")
            
            temperature=input("请输入温度")
            humidity=input("请输入湿度")
            Carbon_dioxide=input("请输入二氧化碳浓度")
            Light=input("请输入光照强度")

            print("接着输入植物的分布区域(省市县)\n")
            place_number=input("请输入分布区域的编号")
            place_province=input("请输入省份")
            place_city=input("请输入市")
            place_county=input("请输入县")
        
            sql = "INSERT INTO Plants (plants_number, plants_name, other_name, distribution_area_number, belong_species) \
        VALUES (%s, %s, %s, %s, %s)"
            data = (plant_number, plant_name, plant_othername,place_number, Speciesnumber)
            dao.execute_insert(sql,data)

            sql = "INSERT INTO Section (Section_number,chinese_name) \
        VALUES (%s, %s)"
            data = (Sectionnumber, Section)
            dao.execute_insert(sql,data)

            sql = "INSERT INTO Genus (Genus_number,chinese_name,belong_Section) \
        VALUES (%s, %s, %s)"
            data = (Genusnumber, Genus,Sectionnumber)
            dao.execute_insert(sql,data)

            sql = "INSERT INTO Species (Species_number,chinese_name,belong_Genus) \
        VALUES (%s, %s, %s)"
            data = (Speciesnumber, Species,Genusnumber)
            dao.execute_insert(sql,data)

            sql = "INSERT INTO Growing_environment (Plants_number,temperature,humidity,Carbon_dioxide_concentration,Light_intensity) \
        VALUES (%s, %s,%s,%s,%s)"
            data = (plant_number, temperature,humidity,Carbon_dioxide,Light)
            dao.execute_insert(sql,data)

            sql="INSERT INTO distribution_area(province,city,county,distribution_area_number) VALUES(%s,%s,%s,%s)"
            data=(place_province,place_city,place_county,place_number)
            dao.execute_insert(sql,data)

            sql="INSERT INTO SectiontoGenus(number,content) VALUES(%s,%s)"
            data=(Sectionnumber+Genusnumber,Section+"科"+Genus+"属")
            dao.execute_insert(sql,data)

            sql="INSERT INTO GenustoSpecies(number,content) VALUES(%s,%s)"
            data=(Genusnumber+Speciesnumber,Genus+"属"+Species+"种")
            dao.execute_insert(sql,data)

            sql="INSERT INTO SpeciestoPlants(number,content) VALUES(%s,%s)"
            data=(Speciesnumber+plant_number,Species+"种"+plant_name)
            dao.execute_insert(sql,data)

        if controlnumber==2:
            print("请输出您想要删除的植物的编号(由于可能存在重名的情况，所以推荐您输入编号哦)")
            number=input("请输入四位的植物编号")
            sql=f"DELETE FROM Plants WHERE plants_number={number}"
            dao.execute_delete(sql,number)
            sql=f"DELETE FROM Growing_environment WHERE plants_number={number}"
            dao.execute_delete(sql,number)
        

        if controlnumber==3:
            print("请输出您想要修改的植物的编号")
            number=input("请输入四位的植物编号")
            print("请输出您想要修改的植物的内容")
            sql=f"UPDATE plants SET plant_name = '温水' WHERE plant_number ={number};"
            dao.execute_update(sql,number)

        if controlnumber==4:
            print("根据植物编号查询请按1\n")
            print("根据生长环境查询请按2\n")
            print("指定属性查询下属属性请按3\n")
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
                temperature = test.split(":")[1]
                sql = f"SELECT plants_number FROM Growing_environment WHERE temperature = '{temperature}'"
                result = dao.execute_query(sql)
                plant_number=result[0][0]
                print("该科下面的植物的基本信息如下所示")
                sql = f"SELECT * FROM Plants WHERE plants_number ='{plant_number}'"
                result=dao.execute_query(sql)
                plantnumber=result[0][0]
                print(result)
                print("分布区域为：\n")
                sql = f"SELECT * FROM distribution_area WHERE distribution_area_number ='{result[0][3]}'"
                result=dao.execute_query(sql)
                print(result)
                print("生长环境为：\n")
                print("温度，湿度，二氧化碳，光照强度如下\n")
                sql = f"SELECT * FROM Growing_environment WHERE plants_number ='{plantnumber}'"
                result=dao.execute_query(sql)
                print(result)

            if newnumber==3:
                print("请输入指定的属性")
                Sectionserch=input("请输入指定的科的名称")
                sql = f"SELECT Section_number FROM Section WHERE chinese_name ='{Sectionserch}'"
                result=dao.execute_query(sql)
                number=result[0][0]
                sql = f"SELECT number FROM SectiontoGenus WHERE number like '{number}%'"
                result=dao.execute_query(sql)
                Genusnumber=result[0][0][-4:]
                sql = f"SELECT number FROM GenustoSpecies WHERE number like '{Genusnumber}%'"
                result=dao.execute_query(sql)
                Speciesnumber=result[0][0][-4:]
                sql = f"SELECT number FROM SpeciestoPlants WHERE number like '{Speciesnumber}%'"
                result=dao.execute_query(sql)
                Plantsnumber=result[0][0][-4:]
                print("该科下面的植物的基本信息如下所示")
                sql = f"SELECT * FROM Plants WHERE plants_number ='{Plantsnumber}'"
                result=dao.execute_query(sql)
                plantnumber=result[0][0]
                print(result)
                print("分布区域为：\n")
                sql = f"SELECT * FROM distribution_area WHERE distribution_area_number ='{result[0][3]}'"
                result=dao.execute_query(sql)
                print(result)
                print("生长环境为：\n")
                print("温度，湿度，二氧化碳，光照强度如下\n")
                sql = f"SELECT * FROM Growing_environment WHERE plants_number ='{plantnumber}'"
                result=dao.execute_query(sql)
                print(result)
        if controlnumber==5:
            break

