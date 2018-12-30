# 路径寻找算法
from SFM.BasicClasses import *
from numpy import source
import pandas as pd


class Node_Elem:
    '''''
    开放列表和关闭列表的元素类型，parent用来在成功的时候回溯路径
    '''''
    def __index__(self, x, y, dist):
        self.x = x
        self.y = y
        self.dist = dist


class AStarPathFinder:
    """
    在这里完成A*算法
    """
    def __init__(self):
        # 表示是哪一个人，

        self.open = [[]]
        self.close = [[]]
        self.path = [[]]

    @staticmethod
    def get_direction(scene, source, number):
        """ 寻找路径，获得下一步运动的方向
        scene是Scene类型，source是行人（Circle类型）
        :return: 返回期望方向e，类型为Vector2D，要求e是单位向量e.x^2 + e.y^2 = 1
        """
        self.number = number
        self.source = source
        self.scene = scene
                
        point = Node_Elem(self.source.pos.x, self.source.pos.y, 0.0)
        new_point = self.extend_round(point)
        
        return Vector2D(0, 0)

    def find_path(self):
        point = Node_Elem(self.source.pos.x, self.source.pos.y, 0.0)
        while True:
            self.extend_round(point)
#             如果这个节点的开放列表为空，不存在路径
            if not self.open[self.number]:
                return
            # 获取F值最小的节点
            idx ,point = self.get_best()
            # 找到路径，生成路径，返回
            if self.is_target(point):
                print("We have arrived the aim")
                return point
#             找到了下一点，就找到了方向
            # 把此节点压入关闭列表，并从开放列表里删除
            self.close[self.number].append(point)
            del self.open[self.number][idx]
            return point

    def is_target(self, i):
        large_x = self.scene.dests.p1.x if self.scene.dests.p1.x >= self.scene.dests.p2.x else self.scene.dests.p2.x
        small_x = self.scene.dests.p1.x if self.scene.dests.p1.x <= self.scene.dests.p2.x else self.scene.dests.p2.x
        large_y = self.scene.dests.p1.y if self.scene.dests.p1.y >= self.scene.dests.p2.y else self.scene.dests.p2.y
        small_y = self.scene.dests.p1.y if self.scene.dests.p1.y <= self.scene.dests.p2.y else self.scene.dests.p2.y

        if small_x <= i.x and i.x <= large_x:
            if small_y <= i.y and i.y <= large_y:
                return True

        return False

    def extend_round(self, point):
        xs = (-1, 0, 1, -1, 1, -1, 0, 1)
        ys = (-1, -1, -1, 0, 0, 1, 1, 1)

        for x, y in zip(xs, ys):
            new_x, new_y = x + point.x , y+ point.y
            # 表示每次向某个方向移动
            # 无效或者不可行走区域，则勿略
            if not self.is_valid_coord(new_x, new_y):
                continue
            new_point = Node_Elem(new_x, new_y, point.dist + self.get_cost(point.x, point.y, new_x, new_y))

            # 如果已经在close列表中
            if self.node_in_close(new_point):
                continue
            i = self.node_in_open(new_point)
            if i != -1:
                # 新节点在开放表，更新距离
                if self.open[self.number][i].dist > new_point.dist:
                    self.open[self.number][i].dist = new_point.dist
                    # 现在的路径到比以前到这个节点的路径更好~,则使用现在的路径
                    # 类似于Dijkstra算法
                continue
            self.open[self.number].append(new_point)
            # 新节点不在表中，加入开放表
        return 

    def get_best(self):
        best = None
        bv = 1000000
        # 设一个最大值
        bi = -1
        # 更新open 中的F的数值
        for idx, i in enumerate(self.open[self.number]):
            # 获取F的值
            value = self.get_dist(i)
            if value < bv:
                best = i
                bv = value
                bi = idx
        return bi, best
#     best是未选中表中的距离最近的

    def get_dist(self, i):
#         计算距离的公式,选择一个
        return i.dist + math.sqrt()


    def get_cost(self, x1, y1, x2, y2):
        if x1==x2 or y1==y2:
            return 1.0
        return 1.4

    def node_in_close(self, node):
        for i in self.close[self.number]:
            if node.x == i.x and node.y==i.y:
                return True
        return False

    def node_in_open(self, node):
        for i, n in enumerate(self.open[self.number]):
            if node.x == n.x and node.y == n.y:
                return i
        return -1
        # 表示没找到

    def is_valid_coord(self, source, node):
#         对于所有人，需要判断是否会相撞
        for i in source:
            if i.x == node.x and i.y == node.y:
                return False
            
#         获取障碍物的坐标，不能碰到障碍物
        large_x = self.scene.boxes.p1.x if self.scene.boxes.p1.x >= self.scene.boxes.p2.x else self.scene.boxes.p2.x
        small_x = self.scene.boxes.p1.x if self.scene.boxes.p1.x <= self.scene.boxes.p2.x else self.scene.boxes.p2.x
        large_y = self.scene.boxes.p1.y if self.scene.boxes.p1.y >= self.scene.boxes.p2.y else self.scene.boxes.p2.y
        small_y = self.scene.boxes.p1.y if self.scene.boxes.p1.y <= self.scene.boxes.p2.y else self.scene.boxes.p2.y
        
        if small_x <= node.x and node.x <= large_x and small_y << node.y and node.y << large_y:
            return False
        return True 
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            

