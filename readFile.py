#!/usr/bin/env python
import os


class ReadData:
    def __init__(self, time_span=0.05):
        # :param file_path: 输入一个测试集的路径
        self.time_span = time_span  # 每个数据的时间间隔
        self.persons = None
        self.per_num = 0
        self.speed_list = None
        self.remove_tuple = (1000000000.0, 1000000000.0)

    def get_para(self, person_index, time_index):
        """
        获取某个人某个时刻的坐标
        :param person_index: 想要获取坐标的人的标号
        :param time_index: 想要获取坐标的时间序号，从0开始
        :return: 返回的坐标，若人已到达出口则将返回值设置为self.remove_tuple
        """
        length = len(self.persons[person_index])
        if time_index >= length:
            return self.remove_tuple
        return self.persons[person_index][time_index]

    def get_speed(self, person_index, time_index):
        """
        获取某个人某个时刻的速度
        :param person_index: 人的序号
        :param time_index: 时间序号，序号0实际代表着  0-1时刻人移动的速度
        :return: 返回time_index至time_index+1时刻人的速度，若以到达终点，则速度为(0, 0)
        """
        length = len(self.speed_list[person_index])
        if time_index >= length:
            return 0.0, 0.0
        return self.speed_list[person_index][time_index]

    def add_train_data(self, file_path):
        """

        :param file_path: 训练样本的路径
        :return: 无
        """
        for root, dirs, files in os.walk(file_path):
            self.per_num = len(files)
            self.persons = {}
            self.speed_list = {}
            # print(self.per_num)
            for file in files:
                index = file.rfind('.')
                index = int(file[:index])
                self.persons[index] = []
                self.speed_list[index] = []
                with open(file_path+'/'+file, "r") as f:
                    pre_x = -1
                    pre_y = -1
                    i = 0
                    para = f.readline()
                    while para:
                        coord = para.split()
                        x = float(coord[0])
                        y = float(coord[1])
                        if i > 0:
                            if index == 1 and i == 1:
                                print(pre_x, x)
                            self.speed_list[index].append(((x - pre_x)/self.time_span, (y - pre_y)/self.time_span))
                        self.persons[index].append((x, y))
                        pre_x = x
                        pre_y = y
                        i += 1
                        para = f.readline()
                print(index, len(self.persons[index]), self.speed_list[index])


if __name__ == '__main__':
    input_data = ReadData()
    input_data.add_train_data(r'D:\11学习文件\2018下\数学建模\神经网络原始数据\Data_Set\#00001横向障碍物-窄门-无奖励-1_v5')
    print(input_data.get_para(8, 99))
