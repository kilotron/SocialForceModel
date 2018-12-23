from SFM.BasicClasses import *


def is_valid(scene, ped):
    # 人的位置是否有效，如果有重叠返回False
    for p in scene.peds:
        if ped.is_intersect(p):
            return False
    for b in scene.boxes:
        if ped.is_intersect(b):
            return False
    return True


def get_scene0():
    #global scale_factor
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