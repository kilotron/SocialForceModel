# 路径寻找算法
import SFM.BasicClasses
import math
import random

class Node:
    def __init__(self, box, x, y, id):
        self.f = None
        self.g = None
        self.h = None
        self.parent = None
        self.next = None
        self.box = box
        self.occupied = False
        self.x = x
        self.y = y
        self.id = id
        self.closed = False
        self.open = False


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
                node = Node(box, i, j, j + i * y_max)
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
        """每推进一个时间步长调用此方法一次，更新行人"""
        for i in range(len(self.nodes)):
            for j in range(len(self.nodes[i])):
                self.nodes[i][j].parent = None
                self.nodes[i][j].f = None
                self.nodes[i][j].g = None
                self.nodes[i][j].closed = False
                self.nodes[i][j].open = False

    def is_walkable_at(self, x, y):
        return 0 <= x < len(self.nodes) and 0 <= y < len(self.nodes[0]) and not self.nodes[x][y].occupied

    def jump(self, cx, cy, dx, dy, start, goal):
        nx = cx + dx
        ny = cy + dy
        while True:
            if not self.is_walkable_at(nx, ny):
                return None
            if nx == goal.x and ny == goal.y:
                return goal
            # check for forced neighbors
            if dx != 0 and dy != 0:
                if (self.is_walkable_at(cx, ny + dy) and not self.is_walkable_at(cx, ny)) \
                        or (self.is_walkable_at(nx + dx, cy) and not self.is_walkable_at(nx, cy)):
                    return self.nodes[nx][ny]
                if self.jump(nx, ny, dx, 0, start, goal) is not None \
                        or self.jump(nx, ny, 0, dy, start, goal) is not None:
                    return self.nodes[nx][ny]
            # horizontally/vertically
            else:
                if dx != 0:
                    if (self.is_walkable_at(nx + dx, ny + 1) and not self.is_walkable_at(nx, ny + 1)) \
                            or (self.is_walkable_at(nx + dx, ny - 1) and not self.is_walkable_at(nx, ny - 1)):
                        return self.nodes[nx][ny]
                else:
                    if (self.is_walkable_at(nx + 1, ny + dy) and not self.is_walkable_at(nx + 1, ny)) \
                            or (self.is_walkable_at(nx - 1, ny + dy) and not self.is_walkable_at(nx - 1, ny)):
                        return self.nodes[nx][ny]
            cx = nx
            cy = ny
            nx = cx + dx
            ny = cy + dy
        #return self.jump(nx, ny, dx, dy, start, goal)

    def find_neighbors(self, node):
        cx = node.x
        cy = node.y
        neighbors = []
        if node.parent is not None:
            px = node.parent.x
            py = node.parent.y
            dx = (cx - px) // max(abs(cx - px), 1)
            dy = (cy - py) // max(abs(cy - py), 1)

            if dx != 0 and dy != 0:
                if self.is_walkable_at(cx, cy + dy):
                    neighbors.append(self.nodes[cx][cy + dy])
                if self.is_walkable_at(cx + dx, cy):
                    neighbors.append(self.nodes[cx + dx][cy])
                if self.is_walkable_at(cx + dx, cy + dy):
                    neighbors.append(self.nodes[cx + dx][cy + dy])
                # forced neighbors:
                if not self.is_walkable_at(cx - dx, cy):
                    neighbors.append(self.nodes[cx - dx][cy + dy])
                if not self.is_walkable_at(cx, cy - dy):
                    neighbors.append(self.nodes[cx + dx][cy - dy])
            else:
                if dx == 0:
                    if self.is_walkable_at(cx, cy + dy):
                        neighbors.append(self.nodes[cx][cy + dy])
                    if not self.is_walkable_at(cx + 1, cy):
                        neighbors.append(self.nodes[cx + 1][cy + dy])
                    if not self.is_walkable_at(cx - 1, cy):
                        neighbors.append(self.nodes[cx - 1][cy + dy])
                else:
                    if self.is_walkable_at(cx + dx, cy):
                        neighbors.append(self.nodes[cx + dx][cy])
                    if not self.is_walkable_at(cx, cy + 1):
                        neighbors.append(self.nodes[cx + dx][cy + 1])
                    if not self.is_walkable_at(cx, cy - 1):
                        neighbors.append(self.nodes[cx + dx][cy - 1])
        else:  # no parent
            neighbors = self.neighbors(node)
        return neighbors

    def neighbors(self, node):
        xs = (-1, 0, 1, -1, 1, -1, 0, 1)
        ys = (-1, -1, -1, 0, 0, 1, 1, 1)
        neighbors = []
        for dx, dy in zip(xs, ys):
            nx = node.x + dx
            ny = node.y + dy
            if self.is_walkable_at(nx, ny):
                neighbors.append(self.nodes[nx][ny])
        return neighbors

    def identify_successors(self, node, open_list, start, goal):
        neighbors = self.find_neighbors(node)
        for neighbor in neighbors:
            dx = neighbor.x - node.x
            dy = neighbor.y - node.y
            jump_node = self.jump(node.x, node.y, dx, dy, start, goal)
            if jump_node is not None and not jump_node.closed:
                cost = node.g + self.dist_between(node, neighbor)
                if not jump_node.open or cost < jump_node.g:
                    jump_node.g = cost
                    jump_node.h = self.heuristic_estimate(jump_node, goal)
                    jump_node.f = jump_node.g + jump_node.h
                    jump_node.parent = node
                    if not jump_node.open:
                        open_list.append(jump_node)
                        jump_node.open = True

    def heuristic_estimate(self, start, goal):
        return abs(start.x - goal.x) + abs(start.y - goal.y)

    def dist_between(self, node1, node2):
        """ distance between neighbors"""
        if node1.x == node2.x or node1.y == node2.y:
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
        open_list = [start]
        start.g = 0
        start.f = start.g + self.heuristic_estimate(start, goal)
        start.open = True
        while len(open_list) != 0:
            current = self.get_lowest(open_list)
            if current == goal:
                self.construct_path(goal)
                return
            open_list.remove(current)
            current.open = False
            current.closed = True
            self.identify_successors(current, open_list, start, goal)
        # 无路可走

    def get_node(self, pos):
        x = int(pos.x * self.scale_factor)
        y = int(pos.y * self.scale_factor)
        xs = (0, 0, 1, -1, 1, -1, 0, 1, -1)
        ys = (0, -1, -1, 0, 0, 1, 1, 1, -1)
        for i, j in zip(xs, ys):
            nx = x + i
            ny = y + j
            if not (0 <= nx < len(self.nodes) and 0 <= ny < len(self.nodes[0])):
                continue
            node = self.nodes[nx][ny]
            if node.box.is_in(pos):
                return node
        return None


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
    d = scene.dests[0]
    dest = SFM.BasicClasses.Vector2D(d.p1.x, d.p1.y)
    #dest = d.center()
    goal = pf.get_node(dest)
    if start is None: # 出界
        return SFM.BasicClasses.Vector2D(0, 0)
    pf.a_star(start, goal)
    if start.next is None:
        return SFM.BasicClasses.Vector2D(0, 0)
    e = SFM.BasicClasses.Vector2D(start.next.x - start.x, start.next.y - start.y)
    return e / e.norm()
