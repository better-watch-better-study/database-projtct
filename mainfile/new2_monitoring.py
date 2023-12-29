import abc
import pymssql
from dbutils.persistent_db import PersistentDB
import datetime
from datetime import datetime


class Monitoring_Information:
    def __init__(self, mno, mpno, mdno, mtime, mplace, cperson, temperature, humidity, cbc, disease, light):
        self.__mno = mno
        self.__mpno = mpno
        self.__mdno = mdno
        self.__mtime = mtime
        self.__mplace = mplace
        self.__cperson = cperson
        self.__temperature = temperature
        self.__humidity = humidity
        self.__cbc = cbc
        self.__disease = disease
        self.__light = light

    @property
    def mno(self):
        return self.__mno

    @mno.setter
    def mno(self, mno):
        self.__mno = mno

    @property
    def mpno(self):
        return self.__mpno

    @mpno.setter
    def mpno(self, mpno):
        self.__mpno = mpno

    @property
    def mdno(self):
        return self.__mdno

    @mdno.setter
    def mdno(self, mdno):
        self.__mdno = mdno

    @property
    def mtime(self):
        return self.__mtime

    @mtime.setter
    def mtime(self, mtime):
        self.__mtime = mtime

    @property
    def mplace(self):
        return self.__mplace

    @mplace.setter
    def mplace(self, mplace):
        self.__mplace = mplace

    @property
    def cperson(self):
        return self.__cperson

    @cperson.setter
    def cperson(self, cperson):
        self.__cperson = cperson

    @property
    def temperature(self):
        return self.__temperature

    @temperature.setter
    def temperature(self, temperature):
        self.__temperature = temperature

    @property
    def humidity(self):
        return self.__humidity

    @humidity.setter
    def humidity(self, humidity):
        self.__humidity = humidity

    @property
    def cbc(self):
        return self.__cbc

    @cbc.setter
    def cbc(self, cbc):
        self.__cbc = cbc

    @property
    def disease(self):
        return self.__disease

    @disease.setter
    def disease(self, disease):
        self.__disease = disease

    @property
    def light(self):
        return self.__light

    @light.setter
    def light(self, light):
        self.__light = light


class Monitoring_Devices:
    def __init__(self, mdno, mdn):
        self.__mdno = mdno
        self.__mdn = mdn

    @property
    def mdno(self):
        return self.__mdno

    @mdno.setter
    def mdno(self, mdno):
        self.__mdno = mdno

    @property
    def mdn(self):
        return self.__mdn

    @mdn.setter
    def cn(self, mdn):
        self.__mdn = mdn


class Error_Monitoring_Information:
    def __init__(self, mno, mpno, mplace, istemp, ishum, iscbc, islight, isdisease):
        self.__mno = mno
        self.__mpno = mpno
        self.__mplace = mplace
        self.__istemp = istemp
        self.__ishum = ishum
        self.__iscbc = iscbc
        self.__islight = islight
        self.__isdisease = isdisease

    @property
    def mno(self):
        return self.__mno

    @mno.setter
    def mno(self, mno):
        self.__mno = mno

    @property
    def mpno(self):
        return self.__mpno

    @mpno.setter
    def mpno(self, mpno):
        self.__mpno = mpno

    @property
    def mplace(self):
        return self.__mplace

    @mplace.setter
    def mplace(self, mplace):
        self.__mplace = mplace

    @property
    def istemp(self):
        return self.__istemp

    @istemp.setter
    def istemp(self, istemp):
        self.__istemp = istemp

    @property
    def ishum(self):
        return self.__ishum

    @ishum.setter
    def ishum(self, humidity):
        self.__ishum = ishum

    @property
    def iscbc(self):
        return self.__iscbc

    @iscbc.setter
    def iscbc(self, iscbc):
        self.__iscbc = iscbc

    @property
    def islight(self):
        return self.__islight

    @islight.setter
    def islight(self, islight):
        self.__islight = islight

    @property
    def isdisease(self):
        return self.__isdisease

    @isdisease.setter
    def isdisease(self, isdisease):
        self.__isdisease = isdisease


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


class Monitoring_Information_DAO(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def insert(self, monitoring_infomation):
        pass

    @abc.abstractmethod
    def update(self, monitoring_infomation, mes_to_update):
        pass

    @abc.abstractmethod
    def delete(self, monitoring_infomation):
        pass

    @abc.abstractmethod
    def select(self, mes_to_select):
        pass

    @abc.abstractmethod
    def show(self):
        pass

    @abc.abstractmethod
    def statistic(self, plant, which):
        pass


class Monitoring_Information_DAO_Impl(Base_DAO, Monitoring_Information_DAO):
    def __init__(self):
        self.connection = self.get_conn()

    def insert(self, monitoring_infomation):
        cursor = self.connection.cursor()
        if monitoring_infomation.disease == "NULL":
            monitoring_infomation.disease = None

        now = datetime.now()
        formatted_datetime = now.strftime("%Y-%m-%d %H:%M:%S")
        try:
            cursor.execute("insert into MI values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                           (monitoring_infomation.mno, monitoring_infomation.mpno, monitoring_infomation.mdno,
                            monitoring_infomation.mtime, monitoring_infomation.mplace,
                            formatted_datetime, formatted_datetime, monitoring_infomation.cperson, monitoring_infomation.temperature,
                            monitoring_infomation.humidity, monitoring_infomation.cbc, monitoring_infomation.disease,
                            monitoring_infomation.light))
            self.connection.commit()
        except pymssql.IntegrityError as e:
            if e.args[0] == 2627:  # 主键重复的错误码
                print("主键" + monitoring_infomation.mno + "重复，无法插入")
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
        now = datetime.now()
        formatted_datetime = now.strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute("select * from MI where mno=" + "'" + update_to + "'")
        result = cursor.fetchall()

        if not result:
            print("修改对象不存在！")
        else:
            cursor.execute("update MI set " + k + "=" + "'" + v + "' where mno=" + "'" + update_to + "'")
            self.connection.commit()

            cursor.execute("update MI set utime='" + formatted_datetime + "' " + "where mno=" + "'" + update_to + "'")
            self.connection.commit()
            print("更新成功！")

        cursor.close()

    def delete(self, mno):
        cursor = self.connection.cursor()
        cursor.execute("select * from MI where mno=" + "'" + mno + "'")
        result = cursor.fetchall()

        if not result:
            print("删除对象不存在！")
        else:
            cursor.execute("delete from MI where mno=%s ", (mno))
            self.connection.commit()
            print("删除成功！")
        cursor.close()

    def select(self, mes_to_select):
        k = mes_to_select[0].strip("'")
        v = mes_to_select[1].strip("'")
        cursor = self.connection.cursor()
        cursor.execute(
            "select mno, MI.mpno, Plants_name, mdno, mtime, mplace, ctime, utime, cperson, temperature, humidity, cbc, disease, light from MI inner join basicPlants on MI.mpno=basicPlants.Plants_number where " + k + "=" + "'" + v + "'")
        result = cursor.fetchall()
        if not result:
            print("没有匹配的数据！")
        else:
            print("监测编号 监测植物编号 监测植物名称 监测设备编号 监测时间 监测地点 创建时间 创建人员 温度 湿度 二氧化碳浓度 病虫害信息 光照强度")
            for res in result:
                lres = list(res)
                lres[4] = lres[4].strftime("%Y-%m-%d %H:%M:%S")
                lres[6] = lres[6].strftime("%Y-%m-%d %H:%M:%S")
                lres[7] = lres[7].strftime("%Y-%m-%d %H:%M:%S")
                print(lres)
        cursor.close()

    def show(self):
        cursor = self.connection.cursor()
        cursor.execute(
            "select mno, MI.mpno, Plants_name, mdno, mtime, mplace, ctime, utime, cperson, temperature, humidity, cbc, disease, light from MI inner join basicPlants on MI.mpno=basicPlants.Plants_number")
        result = cursor.fetchall()
        if not result:
            print("没有数据！")
        else:
            print("监测编号 监测植物编号 监测植物名称 监测设备编号 监测时间 监测地点 创建时间 创建人员 温度 湿度 二氧化碳浓度 病虫害信息 光照强度")
            for res in result:
                lres = list(res)
                lres[4] = lres[4].strftime("%Y-%m-%d %H:%M:%S")
                lres[6] = lres[6].strftime("%Y-%m-%d %H:%M:%S")
                lres[7] = lres[7].strftime("%Y-%m-%d %H:%M:%S")
                print(lres)
        cursor.close()

    def statistic(self, plant, which):
        cursor = self.connection.cursor()
        cursor.execute("select max(" + which + ") from MI where mpno=" + "'" + plant + "'")
        result = cursor.fetchall()
        print("最大值: " + str(result[0][0]))
        cursor.execute("select min(" + which + ") from MI where mpno=" + "'" + plant + "'")
        result = cursor.fetchall()
        print("最小值: " + str(result[0][0]))
        cursor.execute("select avg(" + which + ") from MI where mpno=" + "'" + plant + "'")
        result = cursor.fetchall()
        print("平均值: " + str(result[0][0]))
        cursor.close()


class Error_Monitoring_Information_DAO(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def show(self):
        pass


class Error_Monitoring_Information_DAO_Impl(Base_DAO, Error_Monitoring_Information_DAO):
    def __init__(self):
        self.connection = self.get_conn()

    def show(self):
        cursor = self.connection.cursor()
        cursor.execute("select mno, EMI.mpno, Plants_name, mplace, istemp, ishum, iscbc, islight, isdisease from EMI inner join basicPlants on EMI.mpno=basicPlants.Plants_number")
        result = cursor.fetchall()
        if not result:
            print("没有数据！")
        else:
            print("监测编号 监测植物编号 监测植物名称 监测地点 温度差 湿度差 二氧化碳浓度差 光照强度差 病虫害信息")
            for res in result:
                lres = list(res)
                print(lres)
        cursor.close()


def insert_MI(MI_DAO):
    while True:
        print("\n请选择操作：")
        print("1. 手动录入监测数据")
        print("2. 一键导入监测数据")
        print("3. 退出")

        choice = input("请输入选择 (1, 2 或 3): ")

        if not choice in ["1", "2", "3"]:
            print("无效选择，请重新输入！")
            continue

        if choice == '1':
            while True:
                print("\n请输入监测数据（用空格隔开）:")
                print(
                    "格式：监测编号 监测植物编号 监测设备编号 监测时间 监测地点 创建人员 温度 湿度 二氧化碳浓度 病虫害信息 光照强度")
                user_input = input()

                # 分割输入数据
                inputs = user_input.split(' ')

                # 检查输入的数据数量是否正确
                if len(inputs) != 11:
                    print("输入格式错误，请确保输入了所有的 11 项数据。")
                    continue

                # 提取数据
                try:
                    mno, mpno, mdno, mtime, mplace, cperson, temperature, humidity, CO2, disease, light = inputs
                    mtime = mtime.replace(",", " ")
                    temperature = float(temperature)
                    humidity = float(humidity)
                    CO2 = float(CO2)
                    light = float(light)
                    monitoring_information = Monitoring_Information(mno, mpno, mdno, mtime, mplace, cperson,
                                                                    temperature, humidity, CO2, disease, light)
                    MI_DAO.insert(monitoring_information)
                    break
                except ValueError as e:
                    print("数据类型错误，请按照正确格式输入。错误详情:", e)
                    continue
        elif choice == '2':
            filename = input("请输入要导入的文件名称：")
            with open(filename, 'r') as f:
                lines = f.readlines()

            rows = [line.strip().split(' ') for line in lines]

            for row in rows:
                mno, mpno, mdno, mtime, mplace, cperson, temperature, humidity, CO2, disease, light = row
                mtime = mtime.replace(",", " ")
                temperature = float(temperature)
                humidity = float(humidity)
                CO2 = float(CO2)
                light = float(light)
                monitoring_information = Monitoring_Information(mno, mpno, mdno, mtime, mplace, cperson,
                                                                temperature, humidity, CO2, disease, light)
                MI_DAO.insert(monitoring_information)

        elif choice == '3':
            print("退出录入监测数据操作。")
            break
        else:
            print("无效输入，请重新输入 1, 2 或 3。")
            continue


def search_MI(MI_DAO):
    print("请选择查询条件：")
    print("1. 监测编号")
    print("2. 植物编号")
    print("3. 监测设备")
    print("4. 监测时间")
    print("5. 监测地点")

    field_choice = input("请输入数字选择: ")

    # 字段映射，包括新增的监测设备
    fields = {
        '1': 'mno',
        '2': 'mpno',
        '3': 'mdno',
        '4': 'mtime',
        '5': 'mplace',
    }

    if field_choice not in fields:
        print("无效的选择。")
        return

    query_value = input(f"请输入 {fields[field_choice]} 的查询值: ")
    MI_DAO.select([fields[field_choice], query_value])


def alter_MI(MI_DAO):
    record_id = input("请输入要修改的监测数据编号: ")
    # 获取用户选择的字段
    print("请选择要修改的字段：")
    print("1. 植物编号")
    print("2. 监测设备编号")
    print("3. 监测时间")
    print("4. 监测地点")
    print("5. 创建人员")
    print("6. 温度")
    print("7. 湿度")
    print("8. 二氧化碳浓度")
    print("9. 病虫害信息")
    print("10. 光照强度")
    field_choice = input("请输入数字选择: ")

    # 字段映射
    fields = {
        '1': 'mpno',
        '2': 'mdno',
        '3': 'mtime',
        '4': 'mplace',
        '5': 'cperson',
        '6': 'temperature',
        '7': 'humidity',
        '8': 'cbc',
        '9': 'disease',
        '10': 'light',
    }

    if field_choice not in fields:
        print("无效的选择。")
        return

    # 获取新值
    new_value = input(f"请输入新的 {fields[field_choice]} 值: ").strip()

    MI_DAO.update(record_id, [fields[field_choice], new_value])


def delete_MI(MI_DAO):
    delete_to = input(f"请输入要删除监测数据的编号: ").strip()
    MI_DAO.delete(delete_to)


def statistic_MI(MI_DAO):
    print("请选择统计字段：")
    print("1. 温度")
    print("2. 湿度")
    print("3. 二氧化碳浓度")
    print("4. 光照强度")
    field_choice = input("请输入数字选择: ")

    # 字段映射
    fields = {
        '1': 'temperature',
        '2': 'humidity',
        '3': 'cbc',
        '4': 'light'
    }

    if field_choice not in fields:
        print("无效的选择。")
        return

    field_name = fields[field_choice]

    plant = input("请输入查询的植物编号: ").strip()

    MI_DAO.statistic(plant, field_name)


def monitor_system():
    MI_sample = Monitoring_Information_DAO_Impl()
    EMI_sample = Error_Monitoring_Information_DAO_Impl()


    while True:
        # 显示选项
        print("请选择操作：")
        print("1. 录入监测数据")
        print("2. 显示监测数据")
        print("3. 修改监测数据")
        print("4. 删除监测数据")
        print("5. 查询监测数据")
        print("6. 显示异常数据")
        print("7. 退出")

        # 获取用户选择
        choice = input("请输入选择: ")

        # 执行所选的功能
        if choice == '1':
            insert_MI(MI_sample)
        elif choice == '2':
            MI_sample.show()
        elif choice == '3':
            alter_MI(MI_sample)
        elif choice == '4':
            delete_MI(MI_sample)
        elif choice == '5':
            print("1. 一般查询")
            print("2. 统计查询")
            query_choice = input("请选择查询类型: ")
            if query_choice == '1':
                search_MI(MI_sample)
            elif query_choice == '2':
                statistic_MI(MI_sample)
            else:
                print("无效输入，请输入 1 或 2。")
        elif choice == '6':
            EMI_sample.show()
        elif choice == '7':
            MI_sample.close_conn(MI_sample.connection)
            EMI_sample.close_conn(EMI_sample.connection)
            break
        else:
            print("无效输入，请输入 1, 2, 3, 4, 5, 6, 7 或 8。")
