# 路径寻找算法
import SFM.BasicClasses
import math

class Node:
    def __init__(self, box, coord):
        self.f = None
        self.g = None
        self.parent = None
        self.next = None
        self.box = box
        self.occupied = False
        self.coord = coord


class AStarPathFinder:
    """
    在这里完成A*算法
    """
    def __init__(self):
        self.scene = None
        self.nodes = None
        self.start = None
        self.goal = None

    def build_nodes(self, start_pos):
        """start_pos is a Vector2D"""
        scale_factor = 1 # an integer
        x_max = math.ceil(self.scene.border.x) * scale_factor
        y_max = math.ceil(self.scene.border.y) * scale_factor
        nodes = []
        for i in range(0, x_max):
            list = []
            nodes.append(list)
            for j in range(0, y_max):
                box = SFM.BasicClasses.Box(i, j, i + 1, j + 1)
                box.scale(1/scale_factor)
                node = Node(box, (i, j))
                list.append(node)
                if box.is_in(start_pos):
                    continue # 自己占据的位置不设置为occupied
                for ped in self.scene.peds:
                    node.occupied = True if ped.is_intersect(node.box) else node.occupied
                for box in self.scene.boxes:
                    node.occupied = True if box.is_intersect(node.box) else node.occupied
        self.nodes = nodes
        return nodes

    def valid_coord(self, coord):
        return 0 <= coord[0] < len(self.nodes) and 0 <= coord[1] < len(self.nodes[0])

    def neighbors(self, node):
        xs = (-1, 0, 1, -1, 1, -1, 0, 1)
        ys = (-1, -1, -1, 0, 0, 1, 1, 1)
        neighbors = []
        for x, y in zip(xs, ys):
            nx = node.coord[0] + x
            ny = node.coord[1] + y
            if self.valid_coord((nx, ny)) and not self.nodes[nx][ny].occupied:
                neighbors.append(self.nodes[nx][ny])
        return neighbors

    def heuristic_estimate(self, start, goal):
        return abs(start.coord[0] - goal.coord[0]) + abs(start.coord[1] - goal.coord[1])

    def dist_between(self, node1, node2):
        """ distance between neighbors"""
        if node1.coord[0] == node2.coord[0] or node1.coord[1] == node2.coord[1]:
            return 1.0
        return 1.4

    def get_lowest(self, open_set):
        lowest = float("inf")
        lowest_node = None
        for node in open_set:
            if node.f < lowest:
                lowest = node.f
                lowest_node = node
        return lowest_node

    def construct_path(self, goal):
        node = goal
        while not node.parent is None:
            node.parent.next = node
            node = node.parent

    def a_star(self, start, goal):
        """http://theory.stanford.edu/~amitp/GameProgramming/ImplementationNotes.html"""
        open_set = {start}
        closed_set = set()
        start.g = 0
        start.f = start.g + self.heuristic_estimate(start, goal)
        while len(open_set) != 0:
            current = self.get_lowest(open_set)
            if current == goal:
                self.construct_path(goal)
                return
            open_set.remove(current)
            closed_set.add(current)
            for neighbor in self.neighbors(current):
                cost = current.g + self.dist_between(current, neighbor)
                if neighbor in open_set and cost < neighbor.g:
                    open_set.remove(neighbor)
                if neighbor in closed_set and cost < neighbor.g:
                    closed_set.remove(neighbor)
                if neighbor not in open_set and neighbor not in closed_set:
                    neighbor.g = cost
                    neighbor.f = neighbor.g + self.heuristic_estimate(neighbor, goal)
                    neighbor.parent = current
                    open_set.add(neighbor)
        # 无路可走

    def get_node(self, pos):
        for i in range(len(self.nodes)):
            for j in range(len(self.nodes[i])):
                node = self.nodes[i][j]
                if node.box.is_in(pos):
                    return node

    def get_direction(self, scene, source):
        """ 寻找路径，获得下一步运动的方向
        scene是Scene类型，source是行人（Circle类型）
        :return: 返回期望方向e，类型为Vector2D，要求e是单位向量e.x^2 + e.y^2 = 1
        """
        self.scene = scene
        self.build_nodes(source.pos)
        start = self.get_node(source.pos)
        goal = self.get_node(scene.dests[0].center())
        self.a_star(start, goal)
        if start.next is None:
            return SFM.BasicClasses.Vector2D(0, 0)
        e = SFM.BasicClasses.Vector2D(start.next.coord[0] - start.coord[0], start.next.coord[1] - start.coord[1])
        return e / e.norm()
