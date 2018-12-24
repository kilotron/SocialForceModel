# 路径寻找算法
import SFM.BasicClasses
import math


class Node:
    def __init__(self, box, coord, id):
        self.f = None
        self.g = None
        self.parent = None
        self.next = None
        self.box = box
        self.occupied = False
        self.coord = coord
        self.id = id


class AStarPathFinder:
    """
    在这里完成A*算法
    """

    def __init__(self, scene):
        self.scene = scene
        self.nodes = None
        self.start = None
        self.goal = None
        self.scale_factor = 1 # an integer
        self.build_nodes()
        self.node_list = [self.nodes[i][j] for i in range(len(self.nodes)) for j in range(len(self.nodes[0]))]
        self.open = []
        self.close = []

    def build_nodes(self):
        """调用此方法来读取场景，初始化AStarPathFinder"""
        x_max = math.ceil(self.scene.border.x) * self.scale_factor
        y_max = math.ceil(self.scene.border.y) * self.scale_factor
        self.nodes = []
        for i in range(0, x_max):
            list = []
            self.nodes.append(list)
            for j in range(0, y_max):
                box = SFM.BasicClasses.Box(i, j, i + 1, j + 1)
                box.scale(1/self.scale_factor)
                node = Node(box, (i, j), j + i * y_max)
                list.append(node)
        for box in self.scene.boxes:
            x_max = round(box.p2.x * self.scale_factor)
            x_min = int(box.p1.x * self.scale_factor)
            y_max = round(box.p2.y * self.scale_factor)
            y_min = int(box.p1.y * self.scale_factor)
            for x in range(x_min, x_max):
                for y in range(y_min, y_max):
                    node = self.nodes[x][y]
                    if box.is_intersect(node.box):
                        node.occupied = True

    def update_nodes(self, start):
        """每推进一个时间步长调用此方法一次，更新行人的位置,start所在位置不设为occupied"""
        for i in range(len(self.nodes)):
            for j in range(len(self.nodes[i])):
                self.nodes[i][j].parent = None
                self.nodes[i][j].f = None
                self.nodes[i][j].g = None
                self.nodes[i][j].occupied = False
        for box in self.scene.boxes:
            x_max = round(box.p2.x * self.scale_factor)
            x_min = int(box.p1.x * self.scale_factor)
            y_max = round(box.p2.y * self.scale_factor)
            y_min = int(box.p1.y * self.scale_factor)
            for x in range(x_min, x_max):
                for y in range(y_min, y_max):
                    node = self.nodes[x][y]
                    if box.is_intersect(node.box):
                        node.occupied = True
        for ped in self.scene.peds:
            if ped == start:
                continue
            x_max = int((ped.pos.x + ped.radius) * self.scale_factor) + 1
            x_min = max(int((ped.pos.x - ped.radius) * self.scale_factor), 0)
            y_max = int((ped.pos.y + ped.radius) * self.scale_factor) + 1
            y_min = max(int((ped.pos.y - ped.radius) * self.scale_factor), 0)
            for x in range(x_min, x_max):
                for y in range(y_min, y_max):
                    node = self.nodes[x][y]
                    if ped.is_intersect(node.box):
                        node.occupied = True

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
        for node_id in open_set:
            node = self.node_list[node_id]
            if node.f < lowest:
                lowest = node.f
                lowest_node = node
        return lowest_node

    def construct_path(self, goal):
        node = goal
        while not node.parent is None:
            node.parent.next = node
            node = node.parent

    def node_in_set(self, node_set, node_id):
        low = 0
        high = len(node_set) - 1
        while low <= high:
            mid = (low + high) // 2
            if node_id == node_set[mid]:
                return True, low
            elif node_id > node_set[mid]:
                low = mid + 1
            else:
                high = mid - 1
        return False, low

    def insert_node(self, node_set, node_id):
        is_in, index = self.node_in_set(node_set, node_id)
        if not is_in:
            node_set.insert(index, node_id)

    def remove_node(self, node_set, node_id):
        is_in, index = self.node_in_set(node_set, node_id)
        if is_in:
            node_set.remove(node_id)

    def a_star(self, start, goal):
        """http://theory.stanford.edu/~amitp/GameProgramming/ImplementationNotes.html"""
        open_set = [start.id]
        closed_set = []
        start.g = 0
        start.f = start.g + self.heuristic_estimate(start, goal)
        num_out = 0
        num_in = 0
        while len(open_set) != 0:
            num_out = num_out + 1
            current = self.get_lowest(open_set)
            if current == goal:
                self.construct_path(goal)
                print(num_out)
                print(num_in)
                return
            self.remove_node(open_set, current.id)
            self.insert_node(closed_set, current.id)
            for neighbor in self.neighbors(current):
                num_in = num_in + 1
                cost = current.g + self.dist_between(current, neighbor)
                # g是None说明没有检查过，既不在open_set也不再closed_set
                if neighbor.g is None or cost < neighbor.g:
                    neighbor.g = cost
                    neighbor.f = neighbor.g + self.heuristic_estimate(neighbor, goal)
                    neighbor.parent = current
                    self.insert_node(open_set, neighbor.id)
        # 无路可走
        print(num_out)
        print(num_in)

    def get_node(self, pos):
        x = int(pos.x * self.scale_factor)
        y = int(pos.y * self.scale_factor)
        xs = (0, 0, 1, -1, 1, -1, 0, 1, -1)
        ys = (0, -1, -1, 0, 0, 1, 1, 1, -1)
        for i, j in zip(xs, ys):
            nx = x + i
            ny = y + j
            if not self.valid_coord((nx, ny)):
                continue
            node = self.nodes[nx][ny]
            if node.box.is_in(pos):
                return node


def path_finder_init(scene):
    global pf
    pf = AStarPathFinder(scene)


def get_direction(scene, source):
    """ 寻找路径，获得下一步运动的方向
        scene是Scene类型，source是行人（Circle类型）
        :return: 返回期望方向e，类型为Vector2D，要求e是单位向量e.x^2 + e.y^2 = 1
    """
    global pf
    pf.update_nodes(source)
    start = pf.get_node(source.pos)
    goal = pf.get_node(scene.dests[0].center())
    pf.a_star(start, goal)
    if start.next is None:
        return SFM.BasicClasses.Vector2D(0, 0)
    e = SFM.BasicClasses.Vector2D(start.next.coord[0] - start.coord[0], start.next.coord[1] - start.coord[1])
    return e / e.norm()
