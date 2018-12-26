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
    # BasicClasses.pf_test()
    scene = get_scene2(10)  # 横向障碍物
    # scene = get_scene3(15)  # 纵向障碍物
    SFM.PathFinder.path_finder_init(scene)
    g_gui = SfmGui(scene, 10000)

    g_gui.root.mainloop()