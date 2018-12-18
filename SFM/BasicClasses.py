import random
import math
import pickle

"""
    为了简化，我们对每个行人的参数A(N), B(m), desired_speed(m/s), mass(kg)取相同的值。
    肩宽的一半radius(m)服从U(0.25, 0.35)，也就是肩宽在区间[0.5m, 0.7m]服从均匀分布。
    特征时间ch_time是0.5s
"""
param = {
    'A': 2000.0,
    'B': 0.08,
    'desired_speed': 1.0,
    'mass': 80.0,
    'r_upper': 0.35,
    'r_lower': 0.25,
    'ch_time': 0.5
}


class Vector2D:
    """ 二维向量，表示力、速度、位置或者方向。
    Attributes:
        x: 横坐标
        y: 纵坐标
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2D(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        if isinstance(scalar, (int, float)):
            return Vector2D(self.x * scalar, self.y * scalar)
        else:
            return NotImplemented

    def norm(self):
        return math.sqrt(self.x ** 2, self.y ** 2)

    def __str__(self):
        return 'Vector2D(%.2f, %.2f)' % (self.x, self.y);


class Circle:
    """ Circle表示行人
    Attributes:
        pos: 位置向量
        vel: 当前速度
        mass: 质量
        radius: 圆的半径，或人肩宽的一半
    """

    def __init__(self, x, y, vx, vy, mass):
        self.pos = Vector2D(x, y)
        self.vel = Vector2D(vx, vy)
        self.radius = random.uniform(param['r_lower'], param['r_upper'])
        self.mass = mass

    def distance_to(self, other):
        """ 计算与参数other的距离
        根据other的类型（Circle，或墙或障碍物）分别计算
        :param other:
        :return:
        """
        return 0.0

    def ped_repulsive_force(self, others):
        """ 计算行人与其他行人间的排斥力

        使用公式:
            f_i = ∑(j)f_ij 结果
            f_ij = A * e^((r_ij - d_ij) / B) * n_ij
            r_ij = r_i + r_j 半径之和
            d_ij = ||r_i - r_j|| 圆心距离
            n_ij = (r_i - r_j) / d_ij 单位方向向量

        :param others: 其他的行人，是一个Circle的列表
        :return: 其他行人们对此人的合力f_i
        """
        return Vector2D(0, 0)

    def wall_repulsive_force(self, scene):
        """ 计算与障碍物或墙的排斥力

        使用公式:
            ∑(W)f_iW 结果
            f_iW = A * e^((ri-diW)/B) * niW
        注意niW是一个向量,niW的方向是由墙指向行人

        :param scene: 场景，包括障碍物和墙
        :return: 所有墙和障碍物对此人的合力
        """
        return Vector2D(0, 0)

    def desired_force(self):
        """ 计算期望力
        使用公式:
            m * (v * e - vc) / t_c
            m是质量，v是期望速度，e是期望方向(get_direction())
            vc是当前速度，t_c是特征时间
        :return: 期望力
        """
        return Vector2D(0, 0)

    def get_force(self, scene):
        """ 计算合力
        :param
        :return: 合力
        """
        return Vector2D(0, 0)

    def accleration(self):
        """
        调用get_force()得到合力，根据合力和质量计算加速度
        :return: 加速度
        """
        return Vector2D(0, 0)

    def update_status(self):
        """
        调用上面计算加速度的函数获得加速度，更新此人的位置和速度
        注意所有的行人应该同时更新位置和速度
        :return:
        """
        return None


class Box:
    """ Box表示障碍物或墙(矩形)
    Attributes:
        p1:
        p2: 矩形对角线上的两个点的坐标。
    """

    def __init__(self, x1, y1, x2, y2):
        self.p1 = Vector2D(x1, y1)
        self.p2 = Vector2D(x2, y2)

class Scene:
    """ Scene是一个场景，包括静态的墙、障碍物和动态的行人
    Attributes:
        boxes: 障碍物和墙们，Box类型的列表
        dests: 目标位置们，Box类型的列表，可以包含在boxes中
        peds: 行人们，Circle类型，可以是一个列表
    """
    def __init__(self, dests=None, peds=None, boxes=None):
        # 修改这个方法来初始化场景
        self.dests = dests
        self.peds = peds
        self.boxes = boxes

    def load(self, path):
        """ 从文件中加载场景
        :param path: 文件路径
        :return:
        """

        with open(path, "rb") as f:
            read_data = pickle.load(f)
            self.dests = read_data.dests
            self.peds = read_data.peds
            self.boxes = read_data.boxes

    def update(self):
        """ 推进一个时间步长，更新行人们的位置
        :return:
        """
        for ped in self.peds:
            ped.pos.x += 2
            ped.pos.y += 2

    def save(self, path):
        """ 保存场景到路径path
        :param path:
        :return:
        """
        with open(path, "wb") as f:
            pickle.dump(self, f)



