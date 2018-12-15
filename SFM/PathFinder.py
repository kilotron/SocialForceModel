# 路径寻找算法
from SFM.BasicClasses import *


class AStartPathFinder:
    """
    在这里完成A*算法
    """
    def __init__(self):
        self.scene = 1

    @staticmethod
    def get_direction(scene, source):
        """ 寻找路径，获得下一步运动的方向
        scene是Scene类型，source是行人（Circle类型）
        :return: 返回期望方向e，类型为Vector2D，要求e是单位向量e.x^2 + e.y^2 = 1
        """

        return Vector2D(0, 0)