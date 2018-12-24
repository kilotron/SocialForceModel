#!/usr/bin/env python
# coding=utf-8

from GuiModel.Gui import SfmGui
from SFM import BasicClasses
from SFM.Scenes import *
import SFM.PathFinder

if __name__ == '__main__':
    '''
    boxes: 障碍物和墙们，Box类型的列表
    dests: 目标位置们，Box类型的列表，可以包含在boxes中
    peds: 行人们，Circle类型，可以是一个列表
    '''
    #BasicClasses.pf_test()
    """
    scene = BasicClasses.Scene()
    peds = []
    scene.peds = peds
    ped1 = BasicClasses.Circle(1.0, 3.0, 2.0, 0.0, 80, scene)
    ped1.radius = 0.25
    peds.append(ped1)
    ped2 = BasicClasses.Circle(2.0, 3.0, 1.0, 0.0, 80, scene)
    ped2.radius = 0.3
    peds.append(ped2)
    ped3 = BasicClasses.Circle(2.0, 2.0, 1.0, 0.0, 80, scene)
    ped3.radius = 0.35
    peds.append(ped3)

    scene.boxes = []
    scene.boxes.append(BasicClasses.Box(0.0, 4.0, 5.0, 5.0))
    scene.boxes.append(BasicClasses.Box(0.0, 0.0, 5.0, 1.0))
    scene.boxes.append(BasicClasses.Box(5.0, 3.5, 6.0, 5.0))
    scene.boxes.append(BasicClasses.Box(5.0, 0.0, 6.0, 1.5))

    scene.dests = []
    scene.dests.append(BasicClasses.Box(8.0, 0.0, 9.0, 5.0))
    scene.border = BasicClasses.Vector2D(10.0, 6.0)"""
    scene = get_scene1()
    #BasicClasses.pf_test()
    SFM.PathFinder.path_finder_init(scene)
    g_gui = SfmGui(scene, 10000)

    g_gui.root.mainloop()