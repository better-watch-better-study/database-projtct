import pymssql
import new2_monitoring
import yanghu
import drug_task
import basic_information
class Login_Register:
    def __init__(self):
        self.conn = pymssql.connect(
            server='localhost',
            user='sa',
            password='123456',
            database='plant'
        )
        self.cursor = self.conn.cursor()

    def register_user(self):
        userid = input("请输入用户id:")
        # 首先查询数据库中是否已存在相同的userid
        select_sql = f"SELECT * FROM users WHERE userid = '{userid}'"
        self.cursor.execute(select_sql)
        result = self.cursor.fetchone()

        if result:
            print("该用户id已存在，无法注册！")
            return

    # 如果userid不存在，则继续进行其他信息的输入和插入操作
        username = input("请输入用户名: ")
        usertype = input("请选择人员类型（系统管理员、养护人员、监测人员、上级主管部门、病虫害管理人员）:")
        age = int(input("请输入年龄: "))
        sex = input("请输入性别: ")
        password = input("请输入密码: ")
        if usertype not in ["系统管理员", "养护人员", "监测人员", "上级主管部门","病虫害管理人员"]:
            print("无效的人员类型！")
            return
        # 执行插入操作
        insert_sql = f"INSERT INTO users (userid,username,usertype, age,sex, password) VALUES ('{userid}','{username}','{usertype}', {age}, '{sex}', '{password}')"
        self.cursor.execute(insert_sql)
        self.conn.commit()
        print("注册成功！")
        self.login()
    def login(self):
        userid = input("请输入用户id: ")
        password = input("请输入密码: ")

        # 执行查询操作
        select_sql = f"SELECT * FROM users WHERE userid = '{userid}' AND password = '{password}'"
        self.cursor.execute(select_sql)
        result = self.cursor.fetchone()

        if result:
            print("登录成功！")
            # 获取用户类型
            usertype = result[2]
    
            # 根据不同的用户类型执行不同的操作
            if usertype == "系统管理员":
                # 执行系统管理员的操作
                print("1")
            elif usertype == "养护人员":
            # 执行养护人员的操作
                yanghu.main_care()
            elif usertype == "监测人员":
            # 执行检测人员的操作
                new2_monitoring.monitor_system()
                basic_information.basic_information_system()
            elif usertype == "上级主管部门":
            # 执行上级主管部门的操作
                print("4")
            elif usertype == "病虫害管理人员":
            # 执行病虫害管理人员的操作
                drug_task.drug_main()
            # 调用其他已封装的代码，进行接下来的操作
        else:
            print("用户名或密码错误！")

    def close_connection(self):
        self.cursor.close()
        self.conn.close()

def main():
    login_register = Login_Register()
    choice = input("请选择操作：(1) 注册  (2) 登录\n")

    if choice == '1':
        login_register.register_user()
    elif choice == '2':
        login_register.login()
    else:
        print("无效的选择！")

    login_register.close_connection()

if __name__ == '__main__':
    main()