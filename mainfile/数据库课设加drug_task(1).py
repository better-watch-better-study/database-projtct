import pymssql
from datetime import datetime

# 数据库连接配置
class Database:
    def __init__(self):
        self.conn = pymssql.connect(
        server='localhost',
        user='sa',
        password='123456',
        database='Pest Control',
        charset="cp936"
    )
        self.cursor = self.conn.cursor()
        # 检测EMI表中isdisease不为空的情况
        self.cursor.execute("SELECT isdisease,mno FROM EMI")
        isdisease_results = self.cursor.fetchall()

        if not isdisease_results or isdisease_results==1:
            print("无任务")
            input("请输入任意键查看下一个任务。。。")
            return

        for result in isdisease_results:
            isdisease = result[0]
            mno = result[1]
            if isdisease:
                pest_name = isdisease

                # 获取 pest id
                self.cursor.execute("SELECT [Pest Id] FROM [Pest control] WHERE [Pest name] = %s", (pest_name,))
                pest_id_result = self.cursor.fetchone()

                if pest_id_result:
                    pest_id = pest_id_result[0]
                    self.cursor.execute("SELECT [Drug ID] FROM [Pest-Drug] WHERE [Pest Id] = %s", (pest_id, ))
                    drug_id_result = self.cursor.fetchone()

                    if drug_id_result:
                        drug_id = drug_id_result[0]

                        # 通过 pest id 获取 drug id, drug name 和 Effectiveness
                        self.cursor.execute("SELECT [Drug ID], [Drug name], [Effectiveness] FROM drug WHERE [Drug ID] = %s", (drug_id,))
                        pest_drug_results = self.cursor.fetchall()

                        if pest_drug_results:
                            for pest_drug in pest_drug_results:
                                drug_id = pest_drug[0]
                                drug_name = pest_drug[1]
                                effectiveness = pest_drug[2]

                                # 将数据插入新表 drug_task
                                self.cursor.execute("INSERT INTO drug_task ( MNO, pest_name, drug_id, drug_name, effectiveness) VALUES (%s,%s, %s, %s, %s)",
                                            (mno,pest_name, drug_id, drug_name, effectiveness))
                                print(f"---------------编号：{mno}已写入--------------")
                                self.conn.commit()
                
                                # 将 isdisease 置为 1
                                self.cursor.execute("UPDATE EMI SET isdisease = 1 WHERE isdisease = %s", (pest_name,))
                                self.conn.commit()
                        else:
                            print(f"无法找到与病虫害 {pest_name} 对应的药物")
                            input("请输入任意键继续。。。")
                            print("--------------------------------")
                    else:
                        print(f"无法找到与病虫害 {pest_name} 对应的病虫害")
                        input("请输入任意键继续。。。")
                        print("--------------------------------")
                else:
                    print("无任务")
                    input("请输入任意键查看下一个任务。。。")
                    print("--------------------------------")
    # 添加病虫害
    def add_pest(self):
    
        pest_id=input("请输入病虫害编号: ")#病虫害编号
        pest_name=input("请输入病虫害名称: ")#病虫害名称
        control_method=input("请输入病虫害防治方法: ")#防治方法
        pesticide_id=input("请输入病虫害药剂ID: ")#药剂编号
        pesticide_name=input("请输入病虫害药剂名称: ")#药剂名称
        dosage=input("请输入病虫害药剂用量: ")#药剂用量
        effectiveness=input("请输入病虫害作用期限: ")#作用期限
        created_by=input("请输入添加人员ID：")#人员ID
        # 检查是否存在相同编号的病虫害
        self.cursor.execute('SELECT * FROM [Pest control] WHERE [Pest Id]=%s', (pest_id,))
        existing_pest = self.cursor.fetchone()

        if existing_pest:
            print("已存在相同编号的病虫害！")
            return

        # 检查是否存在相同名称的病虫害
        self.cursor.execute('SELECT [Pest Id] FROM [Pest control] WHERE [Pest name]=%s', (pest_name,))
        existing_pest = self.cursor.fetchone()
        self.cursor.execute('INSERT INTO [Pest-Drug] ([Pest Id], [Drug ID]) VALUES (%s, %s)', (pest_id, pesticide_id))
        existing_pest = self.cursor.fetchone()
        if existing_pest:
            print("已存在相同名称的病虫害！")
            return

        # 检查是否存在相同编号的药物
        self.cursor.execute('SELECT [Drug ID] FROM [drug] WHERE [Drug ID]=%s', (pesticide_id))
        existing_pesticide = self.cursor.fetchone()

        if existing_pesticide:
            print("已存在相同编号的药物！")
            return

        # 获取当前时间作为创建时间和更新时间
        now = datetime.now()

        # 执行插入语句
        self.cursor.execute('''
            INSERT INTO [Pest control] ([Pest Id], [Pest name], [Control method], [Create ID], [Create time], [Update time])
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (pest_id, pest_name, control_method, created_by, now, now))

        # 执行插入语句
        self.cursor.execute('''
            INSERT INTO drug ([Drug ID], [Drug name], Dosage, Effectiveness)
                VALUES (%s, %s, %s, %s)
        ''', (pesticide_id, pesticide_name, dosage, effectiveness))

        self.conn.commit()
        print("病虫害信息已成功添加！")
        print("--------------------------------")

    # 查询病虫害
    def get_pest(self):
        pest_id=input("请输入病虫害编号: ")#病虫害编号
        self.cursor.execute('SELECT * FROM [Pest control] WHERE [Pest Id]=%s', (pest_id,))
        pest = self.cursor.fetchall()
        if pest:
            for row in pest:
                print("--------------------------------")
                print(f"病虫害编号: {row[0]}")
                print(f"病虫害名称: {row[1]}")
                print(f"防治方法: {row[2]}")
                print(f"创建人员: {row[3]}")
                print(f"创建时间: {row[4]}")
                print(f"更新时间: {row[5]}")
                print("--------------------------------")
        else:
            print("未找到该病虫害！")
    # 修改病虫害
    def update_pest(self):
        pest_id=input("请输入病虫害编号: ")#病虫害编号
        new_pest_name=pest_name=input("请输入病虫害名称: ")#病虫害名称
        new_control_method=input("请输入病虫害防治方法: ")#防治方法
        updated_by=input("请输入添加人员ID：")#人员ID
        self.cursor.execute('SELECT [Pest Id] FROM [Pest control] WHERE [Pest Id]=%s', (pest_id,))
        existing_pest = self.cursor.fetchone()

        if existing_pest:
            now = datetime.now()
            self.cursor.execute('''
                UPDATE [Pest control] SET [Pest name]=%s, [Control method]=%s, [Create ID]=%s, [Update time]=%s WHERE [Pest Id]=%s
            ''', (new_pest_name, new_control_method, updated_by, now, pest_id))
            self.conn.commit()
            print("病虫害信息已成功更新！")
        else:
            print("未找到该病虫害！")
    # 删除病虫害
    def delete_pest(self):
        pest_id=input("请输入病虫害编号: ")#病虫害编号
        self.cursor.execute('SELECT [Pest Id] FROM [Pest control] WHERE [Pest Id]=%s', (pest_id,))
        existing_pest = self.cursor.fetchone()

        if existing_pest:
            self.cursor.execute('DELETE FROM [Pest control] WHERE [Pest Id]=%s', (pest_id,))
            self.conn.commit()
            print("病虫害信息已成功删除！")
        else:
            print("未找到该病虫害！")
    def __del__(self):
        self.cursor.close()
        self.conn.close()



# 主程序
date=Database()
while True:
    print("请选择操作：")
    print("1. 添加病虫害")
    print("2. 删除病虫害")
    print("3. 更新病虫害信息")
    print("4. 查询病虫害信息")
    print("5. 退出程序")

    choice = input("请输入操作编号: ")

    if choice == "1":
        date.add_pest()
    elif choice == "2":
        date.delete_pest()
    elif choice == "3":
        date.update_pest()
    elif choice == "4":
        date.get_pest()
    elif choice == "5":
        break;
    else:
        print("无效的操作编号！请重新输入。")

