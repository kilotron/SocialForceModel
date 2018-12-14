
class Vector2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar):
        if isinstance(scalar, (int, float)):
            return Vector2D(self.x * scalar, self.y * scalar)
        else:
            return NotImplemented

    def __str__(self):
        return 'Vector2D(%.2f, %.2f)' % (self.x, self.y);


class Circle:
    '''
    Circle表示行人，pos是位置坐标，vel是当前速度，mass是质量
    '''
    desired_velocity = 1

    def __init__(self, x, y, vx, vy, mass):
        self.pos = Vector2D(x, y)
        self.vel = Vector2D(vx, vy)
        self.radius = 0 # 改一下，这个是肩宽
        self.mass = mass

    def get_ped_force(self, others):
        """
        使用公式fij = Ai * e^((rij-dij)/Bi) * nij(公式第一项)计算和其他行人间的作用力
        注意nij是一个单位向量,nij = (ri - rj) / dij，其中dij = ||ri - rj||
        :param others: 其他的行人，是一个Circle的列表
        :return: 其他行人们对此人的合力
        """
        return Vector2D(0, 0)

    def get_wall_force(self, scene):
        """
        使用公式fiW = Ai * e^((ri-diW)/Bi) * niW(公式第一项)计算与墙的作用力
        注意niW是一个向量,niW的方向是由墙指向行人
        :param scene: 场景，包括障碍物和墙
        :return: 所有墙和障碍物对此人的合力
        """
        return Vector2D(0, 0)

    def get_desired_force(self):
        """
        计算期望力（自己编的名字），使用公式m *(v * e - vc) / t_c，m是质量，v是期望速度（上面那个变量），
        e是调用A*的get_direction(scene, circles)获得的单位方向向量，即期望的方向，vc是当前速度，t_c是特征时间
        取0.5s
        :return: 期望力
        """
        return Vector2D(0, 0)

    def get_force(self, scene):
        """
        使用get_ped_force()和get_wall_force()和get_desired_force()计算合力
        :param circle:
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
    '''
    Box表示障碍物或墙(矩形)，p1和p2是矩形对角线上的两个点的坐标。
    '''
    def __init__(self, x1, y1, x2, y2):
        self.p1 = Vector2D(x1, y1)
        self.p2 = Vector2D(x2, y2)

class Scene:
    """
    Scene是一个场景，包括静态的墙、障碍物和动态的行人
    boxes 是障碍物和墙们
    target是目标位置
    peds是行人们，Circle类型，可以是一个列表
    """""
    def __init__(self):
        self.target = None
        self.peds = None
        self.boxes = None

    def load(self, path):
        """
        从文件中加载场景, 文件的格式待设计
        :param path: 文件路径
        :return:
        """

    def update(self):
        """
        推进一个时间步长，更新行人们的位置
        :return:
        """

    def save(self, path):
        """
        保存场景到路径path，只含有墙和障碍物，不含人
        :param path:
        :return:
        """



