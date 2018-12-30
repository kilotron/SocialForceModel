from GuiModel.Gui import SfmGui
from SFM import BasicClasses
from SFM.BasicClasses import *
import SFM.QuickPathFinder


def path_finder_test():
    BasicClasses.pf_test()
    scene = BasicClasses.Scene()
    BasicClasses.Scene.scale_factor = 60
    peds = []
    scene.peds = peds
    ped1 = BasicClasses.Circle(1.0, 3.0, 2.0, 0.0, 80, scene)
    ped1.radius = 0.25
    peds.append(ped1)

    scene.boxes = []
    scene.boxes.append(BasicClasses.Box(0.0, 4.0, 5.0, 5.0))
    scene.boxes.append(BasicClasses.Box(0.0, 0.0, 5.0, 1.0))
    scene.boxes.append(BasicClasses.Box(5.0, 3.5, 6.0, 5.0))
    scene.boxes.append(BasicClasses.Box(5.0, 0.0, 6.0, 1.5))
    scene.boxes.append(BasicClasses.Box(3.0, 2.0, 4.0, 3.0)) # 障碍物

    scene.dests = []
    scene.dests.append(BasicClasses.Box(8.0, 0.0, 9.0, 1.0))
    scene.border = BasicClasses.Vector2D(10.0, 6.0)
    SFM.QuickPathFinder.path_finder_init(scene)
    g_gui = SfmGui(scene, 10000)


def social_force_test():
    scene = Scene()
    peds = []
    scene.peds = peds
    ped1 = Circle(1.0, 3.0, 2.0, 0.0, 80, scene)
    ped1.radius = 0.25
    peds.append(ped1)
    ped2 = Circle(2.0, 3.0, 1.0, 0.0, 80, scene)
    ped2.radius = 0.3
    peds.append(ped2)
    ped3 = Circle(2.0, 2.0, 1.0, 0.0, 80, scene)
    ped3.radius = 0.35
    peds.append(ped3)

    scene.boxes = []
    scene.boxes.append(Box(0.0, 4.0, 5.0, 5.0))
    scene.boxes.append(Box(0.0, 0.0, 5.0, 1.0))
    scene.boxes.append(Box(5.0, 3.0, 6.0, 5.0))
    scene.boxes.append(Box(5.0, 0.0, 6.0, 2.0))
    """
    对于ped1,f21 = (-7.2131, 0), f31 = (-0.0538, 0.0538), f21 + f31 = (-7.2669, 0.0538)
    f1W1 = (0, -0.1696), f1W2 = (0, 6.3e-7), f1W3 = (-8.7e-8， 0)
    f1W4 = (1.828e-18, 4.57e-19), f1W = (0, -0.17)
    """
    print(ped1.ped_repulsive_force())
    print(ped1.wall_repulsive_force())