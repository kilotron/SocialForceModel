from SFM.BasicClasses import *


def is_valid(scene, ped):
    # 人的位置是否有效，如果有重叠返回False
    if ped is None:
        return False
    if ped.pos.x < 0 or ped.pos.x > scene.border.x or ped.pos.y < 0 or ped.pos.y > scene.border.y:
        return False
    for p in scene.peds:
        if ped.is_intersect(p):
            return False
    for b in scene.boxes:
        if ped.is_intersect(b):
            return False
    return True


def get_scene0():
    scene = Scene()
    Scene.scale_factor = 9
    scene.border = Vector2D(60.0, 60.0)
    scene.peds = []
    scene.peds.append(Circle(13.0, 3.0, 2.0, 0.0, 80, scene))
    scene.peds.append(Circle(2.0, 3.0, 1.0, 0.0, 80, scene))
    scene.peds.append(Circle(2.0, 2.0, 1.0, 0.0, 80, scene))

    scene.boxes = []
    scene.boxes.append(Box(0.0, 0.0, 50.0, 1.0))
    scene.boxes.append(Box(50.0, 0.0, 51.0, 47.0))
    scene.boxes.append(Box(0.0, 1.0, 1.0, 49.0))
    scene.boxes.append(Box(0.0, 49.0, 51.0, 50.0))

    scene.dests = []
    scene.dests.append(Box(52.0, 0.0, 60.0, 30.0))
    return scene


def get_scene1(person_num=10):
    scene = Scene()
    Scene.scale_factor = 18
    scene.border = Vector2D(30.0, 30.0)

    scene.boxes = []
    scene.boxes.append(Box(0.0, 0.0, 25.0, 0.5))
    scene.boxes.append(Box(25.0, 0.0, 25.5, 22.5))
    scene.boxes.append(Box(0.0, 0.5, 0.5, 24.5))
    scene.boxes.append(Box(0.0, 24.5, 25.5, 25.0))

    scene.peds = []
    scene.peds.append(Circle(13.0, 3.0, 2.0, 0.0, 80, scene))
    scene.peds.append(Circle(2.0, 3.0, 1.0, 0.0, 80, scene))
    scene.peds.append(Circle(2.0, 2.0, 1.0, 0.0, 80, scene))
    for i in range(person_num):
        ped = None
        while not is_valid(scene, ped):
            ped = Circle(random.uniform(0, 20), random.uniform(0, 20), 0.5, 0.5, 80)
        scene.peds.append(ped)

    scene.dests = []
    scene.dests.append(Box(26.0, 0.0, 30.0, 15.0))
    return scene


def get_scene2(person_num=10):
    scene = Scene()
    # 调整这个参数来适应GUI显示
    Scene.scale_factor = 36

    # 场景边界，下面的box和ped需要在此边界内
    scene.border = Vector2D(15.0, 15.0)

    # 墙以及障碍物
    scene.boxes = []
    scene.boxes.append(Box(0.0, 0.0, 10.0, 1.0))
    scene.boxes.append(Box(0.0, 1.0, 1.0, 14.0))
    scene.boxes.append(Box(0.0, 14.0, 10.0, 15.0))
    scene.boxes.append(Box(10.0, 0.0, 11.0, 7.5))
    scene.boxes.append(Box(10.0, 9.5, 11.0, 15))
    # 下面是障碍物
    scene.boxes.append(Box(6.0, 7.0, 7.0, 10.0))

    scene.peds = []
    for i in range(person_num):
        ped = None
        # 调用is_valid()函数来测试产生的行人是否合适：没有与其他人或墙重叠
        while not is_valid(scene, ped):
            # 行人的5个参数分别是初始x, y坐标，初始x, y方向速度，质量
            ped = Circle(random.uniform(1, 10), random.uniform(1, 14), 0.5, 0.5, 80)
        scene.peds.append(ped)

    # 目的地：目前只支持1个目的地
    scene.dests = []
    scene.dests.append(Box(13.0, 0.0, 15.0, 15.0))
    return scene


def get_scene3(person_num=10):
    scene = Scene()
    # 调整这个参数来适应GUI显示
    Scene.scale_factor = 36

    # 场景边界，下面的box和ped需要在此边界内
    scene.border = Vector2D(15.0, 15.0)

    # 墙以及障碍物
    scene.boxes = []
    scene.boxes.append(Box(0.0, 0.0, 10.0, 1.0))
    scene.boxes.append(Box(0.0, 1.0, 1.0, 14.0))
    scene.boxes.append(Box(0.0, 14.0, 10.0, 15.0))
    scene.boxes.append(Box(10.0, 0.0, 11.0, 7.5))
    scene.boxes.append(Box(10.0, 9.5, 11.0, 15))
    # 下面是障碍物
    scene.boxes.append(Box(5.0, 8.0, 8.0, 9.0))

    scene.peds = []
    for i in range(person_num):
        ped = None
        # 调用is_valid()函数来测试产生的行人是否合适：没有与其他人或墙重叠
        while not is_valid(scene, ped):
            # 行人的5个参数分别是初始x, y坐标，初始x, y方向速度，质量
            ped = Circle(random.uniform(1, 10), random.uniform(1, 14), 0.5, 0.5, 80)
        scene.peds.append(ped)

    # 目的地：目前只支持1个目的地
    scene.dests = []
    scene.dests.append(Box(13.0, 0.0, 15.0, 15.0))
    return scene
