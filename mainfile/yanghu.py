import pymssql

class Care:
    def __init__(self):
        self.conn = pymssql.connect(
            server='localhost',
            user='sa',
            password='123456',
            database='plant',
            as_dict=True
        )
        self.cursor = self.conn.cursor()
        # 检查是否有待处理的EMI数据
        self.cursor.execute("SELECT * FROM EMI")
        emi_data = self.cursor.fetchall()

        if emi_data:
            print("发现待处理的EMI数据:")
    
            for row in emi_data:
                mpno = row['mpno']
                self.cursor.execute(f"SELECT [plants name] FROM Plants WHERE [plants number] = {mpno}")
                plant_data = self.cursor.fetchone()
                if plant_data:
                    print(f"mno: {row['mno']}")
                    print(f"mpno: {row['mpno']}")
                    print(f"plants name: {plant_data['plants name']}")
                    print(f"mplace: {row['mplace']}")
                    print(f"istemp: {row['istemp']}")
                    print(f"ishum: {row['ishum']}")
                    print(f"iscbc: {row['iscbc']}")
                    print(f"islight: {row['islight']}")
                    print(f"isdisease: {row['isdisease']}")
                    print("----------------------")
                if row['isdisease'] == '1':
                     # 输出MNO和mno相同的内容
                    mno = row['mno']

                    self.cursor.execute("SELECT * FROM drug_task WHERE MNO = %s", (mno,))
                    matched_tasks = self.cursor.fetchall()

                    # 输出匹配任务的内容
                    for task in matched_tasks:
                        print(f"MNO: {task['MNO']}")
                        print(f"Pest Name: {task['pest_name']}")
                        print(f"Drug ID: {task['drug_id']}")
                        print(f"Drug Name: {task['drug_name']}")
                        print(f"Effectiveness: {task['effectiveness']}")
                    choice = input("是否需要添加养护任务？(是/否): ")
                    if choice.lower() == "是":
                    # 在这里添加养护任务的代码
                        id = input("请输入任务id：")
                        name = input("请输入任务名称: ")
                        location = input("请输入执行地点: ")
                        execution_time = input("请输入执行时间: ")
                        description = input("请输入任务描述: ")
                        care_object = input("请输入养护对象: ")
                        object_id = input("请输入养护对象id:")
                        self.cursor.execute("SELECT * FROM plant_care WHERE task_id = %s", (id,))
                        existing_task = self.cursor.fetchall()

                        if existing_task:
                            print("任务ID已存在，请重新输入")
                        # 继续进行其他操作 或退出
                        else:
                        # 插入新数据
                            self.cursor.execute('''INSERT INTO plant_care (task_id,task_name, location, execution_time, description, care_object,object_id)
                                VALUES (%s, %s, %s, %s, %s, %s,%s)''', (id,name, location, execution_time, description, care_object,object_id))
                            self.conn.commit()
                        print("养护任务已添加")
                         # 删除对应的drug_task表数据
                        self.cursor.execute("DELETE FROM drug_task WHERE MNO = %s", (mno,))
                        self.conn.commit()
                        print("对应的drug_task表数据已删除")  
            # 删除EMI数据
                    self.cursor.execute("DELETE FROM EMI WHERE mno = %s and mpno = %s", (row['mno'], row['mpno']))
                    self.conn.commit()
                    print(f"EMI数据已删除")
                else:
                    print(f"跳过EMI数据 {row['mno']}")

                print()
    def __del__(self):
        self.cursor.close()
        self.conn.close()

    def add_task(self):
        id = input("请输入任务id：")
        name = input("请输入任务名称: ")
        location = input("请输入执行地点: ")
        execution_time = input("请输入执行时间: ")
        description = input("请输入任务描述: ")
        care_object = input("请输入养护对象: ")
        object_id = input("请输入养护对象id:")
        self.cursor.execute('''INSERT INTO plant_care (task_id,task_name, location, execution_time, description, care_object,object_id)
                        VALUES (%s, %s, %s, %s, %s, %s,%s)''', (id,name, location, execution_time, description, care_object,object_id))
        self.conn.commit()
        print("养护任务已添加")

    def delete_task(self):
        task_id = input("请输入要删除的任务ID: ")

        self.cursor.execute("SELECT * FROM plant_care WHERE task_id = %s", (task_id,))
        result = self.cursor.fetchone()

        if result:
            print(f"任务ID: {result['task_id']}")
            print(f"任务名称: {result['task_name']}")
            print(f"执行地点: {result['location']}")
            print(f"执行时间: {result['execution_time']}")
            print(f"任务描述: {result['description']}")
            print(f"养护对象: {result['care_object']}")
            print(f"养护对象id: {result['object_id']}")
            choice = input("是否需要删除该养护任务？(是/否): ")
            if choice.lower() == "是":
                self.cursor.execute("DELETE FROM plant_care WHERE task_id = %s", (task_id,))
                self.conn.commit()
                print("养护任务已删除")
            elif choice.lower() == "否":
                print("已取消删除操作")
        else:
            print("任务ID不存在")

    def update_task(self):
        id = input("请输入要更新的任务ID: ")

        self.cursor.execute("SELECT * FROM plant_care WHERE task_id = %s", (id,))
        result = self.cursor.fetchone()

        if result:
            name = input("请输入新的任务名称: ")
            location = input("请输入新的执行地点: ")
            execution_time = input("请输入新的执行时间: ")
            description = input("请输入新的任务描述: ")
            care_object = input("请输入新的养护对象: ")

            self.cursor.execute('''UPDATE plant_care
                                SET task_name = %s, location = %s, execution_time = %s, description = %s, care_object = %s
                                WHERE task_id = %s''', (name, location, execution_time, description, care_object, id))
            self.conn.commit()
            print("养护任务已更新")
        else:
            print("任务ID不存在")


    def search_task(self):
        keyword = input("请输入关键词进行查询: ")

        self.cursor.execute("SELECT * FROM plant_care WHERE task_name LIKE %s OR location LIKE %s  OR task_id = %s",
                    ('%' + keyword + '%', '%' + keyword + '%',keyword))

        results = self.cursor.fetchall()

        if results:
            for row in results:
                print(f"任务ID: {row['task_id']}")
                print(f"任务名称: {row['task_name']}")
                print(f"执行地点: {row['location']}")
                print(f"执行时间: {row['execution_time']}")
                print(f"任务描述: {row['description']}")
                print(f"养护对象: {row['care_object']}")
                print("----------------------")
        else:
            print("未找到相关任务")
    
    def compare_plant_care(self):
        query = '''
        SELECT p.[plants number]
        FROM Plants p
        LEFT JOIN plant_care pc ON p.[plants number] = pc.object_id
        WHERE pc.object_id IS NULL
        '''

        self.cursor.execute(query)
        results = self.cursor.fetchall()

        if results:
            print("更新了新的植物：")
            for row in results:
                print(row['plants number'])
                print(row['plants name'])
        else:
            print("没有更新新的植物")

        return results
def main_care():
    care = Care()
    while True:
            print("请选择操作：")
            print("1. 添加养护任务")
            print("2. 删除养护任务")
            print("3. 更新养护任务")
            print("4. 查询养护任务")
            print("5. 查询植物表是否新添加植物")
            print("6. 退出程序")
        
            choice = input("请输入您的选择: ")
        
            if choice == "1":
                care.add_task()
            elif choice == "2":
                care.delete_task()
            elif choice == "3":
                care.update_task()
            elif choice == "4":
                care.search_task()
            elif choice == "5":
                care.compare_plant_care()
            elif choice == "6":
                break
            else:
                print("无效的选择，请重新选择")
