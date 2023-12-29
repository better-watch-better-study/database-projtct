import abc
import pymssql
from dbutils.persistent_db import PersistentDB
import datetime

class Basic_Information:
    def __init__(self, Plants_number, Plants_name, Plants_value, Plants_character):
        self.__Plants_number = Plants_number
        self.__Plants_name = Plants_name
        self.__Plants_value = Plants_value
        self.__Plants_character = Plants_character

    @property
    def Plants_number(self):
        return self.__Plants_number

    @Plants_number.setter
    def Plants_number(self, Plants_number):
        self.__Plants_number = Plants_number

    @property
    def Plants_name(self):
        return self.__Plants_name

    @Plants_name.setter
    def Plants_name(self, Plants_name):
        self.__Plants_name = Plants_name

    @property
    def Plants_value(self):
        return self.__Plants_value

    @Plants_value.setter
    def Plants_value(self, Plants_value):
        self.__Plants_value = Plants_value

    @property
    def Plants_value(self):
        return self.__Plants_value

    @Plants_value.setter
    def Plants_value(self, Plants_value):
        self.__Plants_value = Plants_value

    @property
    def Plants_character(self):
        return self.__Plants_character

    @Plants_character.setter
    def Plants_character(self, mplace):
        self.__Plants_character = Plants_character







class DAO(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_conn(cls):
        pass

    @abc.abstractmethod
    def close_conn(cls):
        pass



class Base_DAO(DAO):
    POOL = PersistentDB(creator=pymssql, maxusage=10, closeable=False,
                        threadlocal=None, host='127.0.0.1', database='plant_system')

    @classmethod
    def get_conn(cls):
        return cls.POOL.connection()

    @classmethod
    def close_conn(cls, conn):
        conn.close()



class Basic_Information_DAO(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def insert(self, basic_infomation):
        pass

    @abc.abstractmethod
    def update(self, update_to, mes_to_update):
        pass

    @abc.abstractmethod
    def delete(self, basic_infomation):
        pass

    @abc.abstractmethod
    def select(self, mes_to_select):
        pass

    @abc.abstractmethod
    def show(self):
        pass




class Basic_Information_DAO_Impl(Base_DAO, Basic_Information_DAO):
    def __init__(self):
        self.connection = self.get_conn()

    def insert(self, basic_infomation):
        cursor = self.connection.cursor()
        if basic_infomation.Plants_value == "NULL":
            basic_infomation.Plants_value = None
        if basic_infomation.Plants_character == "NULL":
            basic_infomation.Plants_character = None
        try:
            cursor.execute("insert into basicPlants values (%s, %s, %s, %s)",
                            (basic_infomation.Plants_number, basic_infomation.Plants_name, basic_infomation.Plants_value, basic_infomation.Plants_character))
            self.connection.commit()
        except pymssql.IntegrityError as e:
            if e.args[0] == 2627:  # 主键重复的错误码
                print("主键" + basic_infomation.Plants_number + "重复，无法插入")
            else:
                print("发生其他数据库错误:", e)
        except pymssql.OperationalError as e:
            if e.args[0] == 8152:
                print("输入值不符合数据库对应属性数据结构")
            else:
                print("发生其他数据库错误:", e)
        cursor.close()

    def update(self, update_to, mes_to_update):
        k = mes_to_update[0].strip("'")
        v = mes_to_update[1].strip("'")
        cursor = self.connection.cursor()
        try:
            cursor.execute("select * from basicPlants where Plants_number=" + "'" + update_to + "'")
            result = cursor.fetchall()

            if not result:
                print("修改对象不存在！")
            else:
                cursor.execute("update basicPlants set " + k + "=" + "'" + v + "' where Plants_number=" + "'" + update_to +"'")
                self.connection.commit()
                print("更新成功！")
        except pymssql.IntegrityError as e:
            if e.args[0] == 2627:  # 主键重复的错误码
                print("主键" + v + "重复，无法修改")
            else:
                print("发生其他数据库错误:", e)
        cursor.close()

    def delete(self, pno):
        cursor = self.connection.cursor()
        cursor.execute("select * from basicPlants where Plants_number=" + "'" + pno + "'")
        result = cursor.fetchall()

        if not result:
            print("删除对象不存在！")
        else:
            cursor.execute("delete from basicPlants where Plants_number=%s ", (pno))
            self.connection.commit()
            print("删除成功！")

        cursor.close()

    def select(self, mes_to_select):
        sql = ""
        for name, value in mes_to_select.items():
            if name in ["植物编号", "植物名称"]:
                if sql == "":
                    sql = sql + name + "=" + "'" + value + "'"
                else:
                    sql = sql + " and " + name + "=" + "'" + value + "'"
            else:
                if sql == "":
                    sql = sql + name + " like " + "'%" + value + "%'"
                else:
                    sql = sql + " and " + name + " like " + "'%" + value + "%'"
        cursor = self.connection.cursor()
        cursor.execute("select * from basicPlants where " + sql)
        result = cursor.fetchall()
        if not result:
            print("没有匹配的数据！")
        else:
            print("植物编号 植物名称 植物应用价值 植物特征")
            for res in result:
                lres = list(res)
                print(lres)
        cursor.close()

    def show(self):
        cursor = self.connection.cursor()
        cursor.execute("select top 10 * from basicPlants")
        result = cursor.fetchall()
        if not result:
            print("没有数据！")
        else:
            print("植物编号 植物名称 植物应用价值 植物特征")
            for res in result:
                lres = list(res)
                print(lres)
        cursor.close()






def insert_BI(BI_DAO):
    while True:
        print("\n请输入监测数据（用空格隔开）:")
        print("格式：植物编号 植物名称 植物应用价值 植物特征")
        user_input = input()

        # 分割输入数据
        inputs = user_input.split(' ')

        # 检查输入的数据数量是否正确
        if len(inputs) != 4:
            print("输入格式错误，请确保输入了所有的 4 项数据。")
            continue
        break

    # 提取数据
    try:
        v1, v2, v3, v4 = inputs
        basic_information = Basic_Information(v1, v2, v3, v4)
        BI_DAO.insert(basic_information)
    except ValueError as e:
        print("数据类型错误，请按照正确格式输入。错误详情:", e)



def search_BI(BI_DAO):
    print("请选择查询条件：")
    print("1. 植物编号")
    print("2. 植物名称")
    print("3. 植物应用价值")
    print("4. 植物特征")


    field_choice = input("请输入数字选择: ").strip()
    field_choices = field_choice.split()

    # 字段映射，包括新增的监测设备
    fields = {
        '1': 'Plants_number',
        '2': 'Plants_name',
        '3': 'Plants_value',
        '4': 'Plants_character',
    }

    for fc in field_choices:
        if fc not in fields:
            print("无效的选择。")
            return

    query_value = {}

    for fcs in field_choices:
        query_value[fields[fcs]] = input(f"请输入 {fields[fcs]} 的查询值: ")

    BI_DAO.select(query_value)


def alter_BI(BI_DAO):

    record_id = input("请输入要修改的植物数据编号: ")
    # 获取用户选择的字段
    print("请选择要修改的字段：")
    print("1. 植物编号")
    print("2. 植物名称")
    print("3. 植物应用价值")
    print("4. 植物特征")
    field_choice = input("请输入数字选择: ")

    # 字段映射
    fields = {
        '1': 'Plants_number',
        '2': 'Plants_name',
        '3': 'Plants_value',
        '4': 'Plants_character',
    }

    if field_choice not in fields:
        print("无效的选择。")
        return

    # 获取新值
    new_value = input(f"请输入新的 {fields[field_choice]} 值: ").strip()

    BI_DAO.update(record_id, [fields[field_choice], new_value])


def delete_BI(BI_DAO):
    delete_to = input(f"请输入要删除植物数据的编号: ").strip()
    BI_DAO.delete(delete_to)



def basic_information_system():
    BI_sample = Basic_Information_DAO_Impl()


    while True:
        # 显示选项
        print("请选择操作：")
        print("1. 新增植物数据")
        print("2. 显示植物数据")
        print("3. 修改植物数据")
        print("4. 删除植物数据")
        print("5. 查询植物数据")
        print("6. 退出")

        # 获取用户选择
        choice = input("请输入选择: ")

        # 执行所选的功能
        if choice == '1':
            insert_BI(BI_sample)
        elif choice == '2':
            BI_sample.show()
        elif choice == '3':
            alter_BI(BI_sample)
        elif choice == '4':
            delete_BI(BI_sample)
        elif choice == '5':
            search_BI(BI_sample)
        elif choice == '6':
            BI_sample.close_conn(BI_sample.connection)
            break
        else:
            print("无效输入，请输入 1, 2, 3, 4, 5, 6, 7 或 8。")
