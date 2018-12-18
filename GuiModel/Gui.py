import math
import time
import threading
import copy

import tkinter

from SFM import BasicClasses

color_list = []
MAX_X = 300
MAX_Y = 300
MAX_COLOR = 50
CANVAS_BG = "white"


def color_list_init(num):
    n = int(256 / int(math.pow(num, 1 / 3) + 1))
    for i in range(0, 256, n):
        for j in range(0, 256, n):
            for k in range(0, 256, n):
                color_list.append("#%02x%02x%02x" % (i, j, k))


def get_color(index):
    return color_list[index % len(color_list)]


'''
def transform_coordinate(x, y):
    return [x, y]
'''


def move_box_left(gui):
    for i in range(20):
        for box in gui.boxes:
            gui.move_box(box, -2, 0)
        time.sleep(0.2)


def move_box_right(gui):
    for i in range(20):
        for box in gui.boxes:
            gui.move_box(box, 2, 0)
        time.sleep(0.2)


def move_box_left_btn(event, gui):
    th = threading.Thread(target=move_box_left, args=(gui, ))
    th.setDaemon(True)
    th.start()


def move_box_right_btn(event, gui):
    th = threading.Thread(target=move_box_right, args=(gui, ))
    th.setDaemon(True)
    th.start()


class SfmGuiTest:
    def __init__(self, scene):
        self.click_coordinate = {"x": -1, "y": -1, "box": None}
        self.boxes = []  # 障碍物
        self.dests = []  # 目标位置
        self.peds = []  # 当前所有人的位置，是一个列表

        self.default_scene = copy.deepcopy(scene)
        self.root = tkinter.Tk()
        self.root.title("社会力模型模拟")
        self.canvas = tkinter.Canvas(self.root, bg=CANVAS_BG, width=MAX_X+50, height=MAX_Y+50)

        self.canvas.pack(side=tkinter.LEFT)
        self.change_scene(scene)

        # 实现界面右边的功能
        self.frame = tkinter.Frame(self.root)
        self.frame.pack(side=tkinter.RIGHT)
        self.bind_btn()

    def get_click(self, event):
        # 在此函数中获取点击的位置信息，判断出是哪个元素被点击
        # print("clicked at ", event.x, event.y)
        x_now = event.x
        y_now = event.y
        for box in self.boxes:
            x0 = box[0].p1.x
            y0 = box[0].p1.y
            x1 = box[0].p2.x
            y1 = box[0].p2.y
            if ((x_now < x0) ^ (x_now < x1)) & ((y_now < y0) ^ (y_now < y1)):
                # print("true")
                self.click_coordinate['x'] = x_now
                self.click_coordinate['y'] = y_now
                self.click_coordinate['box'] = box
                return
            self.click_coordinate['x'] = -1
            self.click_coordinate['y'] = -1
            self.click_coordinate['box'] = None

    def click_release(self, event):
        # 画布中鼠标释放时，执行此函数将相应的box移动
        # print("Release at ", event.x, event.y)
        x_now = event.x
        y_now = event.y
        if self.click_coordinate['box']:
            x_change = x_now - self.click_coordinate['x']
            y_change = y_now - self.click_coordinate['y']
            '''
            box = self.click_coordinate['box']
            self.move_box(box, x_change, y_change)
            '''
            self.click_coordinate['box'][0].p1.x += x_change
            self.click_coordinate['box'][0].p2.x += x_change
            self.click_coordinate['box'][0].p1.y += y_change
            self.click_coordinate['box'][0].p2.y += y_change
            self.canvas.move(self.click_coordinate['box'][1], x_change, y_change)
        pass

    def reset_scene(self, event):
        # 重置场景
        scene = copy.deepcopy(self.default_scene)
        self.change_scene(scene)

    def change_scene(self, scene):
        # 改变场景
        self.canvas.delete(tkinter.ALL)
        self.boxes = [[x, -1] for x in scene.boxes]  # 障碍物
        self.dests = [[x, -1] for x in scene.dests]  # 目标位置
        self.peds = [[x, -1] for x in scene.peds]  # 当前所有人的位置，是一个列表
        self.init_canvas()

    def save(self, event, path):
        # 保存当前场景
        boxes = [x[0] for x in self.boxes]
        dests = [x[0] for x in self.dests]
        peds = [x[0] for x in self.peds]
        scene = BasicClasses.Scene(boxes=boxes, peds=peds, dests=dests)
        scene.save(path)

    def load(self, event, path):
        # 读取场景
        scene = BasicClasses.Scene()
        scene.load(path)
        self.default_scene = copy.deepcopy(scene)
        self.change_scene(scene)

    def init_canvas(self):
        # 向画布中加入各种元素
        color_sum = len(color_list)
        # 将传入的障碍物添加到画布中
        i = 0
        for box in self.boxes:
            # print(get_color(color_sum -1 - i))
            self.add_box(box, fill=get_color(color_sum - 2 - i))
            i += 1
        i = 0
        for ped in self.peds:
            # print(get_color(i))
            self.add_person(ped, fill=get_color(i))
            i += 1
        i = 0
        for dest in self.dests:
            self.add_dest(dest, fill=get_color(color_sum-1))
            i += 1

    def bind_btn(self):
        # 绑定函数
        self.canvas.bind("<Button-1>", lambda x: self.get_click(x))
        self.canvas.bind("<ButtonRelease-1>", lambda x: self.click_release(x))

        new_button = tkinter.Button(self.frame, text="让所有箱子左移")
        new_button.bind("<Button-1>", lambda x: move_box_left_btn(x, self))
        new_button.pack()

        new_button = tkinter.Button(self.frame, text="让所有箱子右移")
        new_button.bind("<Button-1>", lambda x: move_box_right_btn(x, self))
        new_button.pack()

        new_button = tkinter.Button(self.frame, text="重置场景")
        new_button.bind("<Button-1>", self.reset_scene)
        new_button.pack()

        new_button = tkinter.Button(self.frame, text="保存场景")
        new_button.bind("<Button-1>", lambda x: self.save(x, "D://save.p"))
        new_button.pack()

        new_button = tkinter.Button(self.frame, text="加载场景")
        new_button.bind("<Button-1>", lambda x: self.load(x, "D://save.p"))
        new_button.pack()

    def add_box(self, box, fill="black"):
        # 加入障碍物
        # print(self.boxes.index(box))
        x0 = box[0].p1.x
        y0 = box[0].p1.y
        x1 = box[0].p2.x
        y1 = box[0].p2.y
        box[1] = self.canvas.create_polygon(x0, y0, x1, y0, x1, y1, x0, y1, fill=fill)

    def add_person(self, ped, fill="black"):
        # 加入人的信息
        # print(self.boxes.index(box))
        x = ped[0].pos.x
        y = ped[0].pos.y
        r = ped[0].radius * 15
        ped[1] = self.canvas.create_oval((x-r, y-r, x+r, y+r), fill=fill)

    def add_dest(self, dest, fill="black"):
        x0 = dest[0].p1.x
        y0 = dest[0].p1.y
        x1 = dest[0].p2.x
        y1 = dest[0].p2.y
        dest[1] = self.canvas.create_polygon(x0, y0, x1, y0, x1, y1, x0, y1, fill=fill)

    def move_box(self, box, x, y):
        self.canvas.move(box[1], x, y)
        box[0].p1.x += x
        box[0].p2.x += x
        box[0].p1.y += y
        box[0].p2.y += y


if __name__ == '__main__':
    color_list_init(MAX_COLOR)
    '''
    boxes: 障碍物和墙们，Box类型的列表
    dests: 目标位置们，Box类型的列表，可以包含在boxes中
    peds: 行人们，Circle类型，可以是一个列表
    '''
    boxes = []
    dests = []
    peds = []
    boxes.append(BasicClasses.Box(5, 5, 250, 10))
    boxes.append(BasicClasses.Box(180, 40, 193, 160))
    boxes.append(BasicClasses.Box(5, 200, 250, 215))

    peds.append(BasicClasses.Circle(30, 30, 3, 3, 1))

    dests.append(BasicClasses.Box(230, 30, 240, 160))
    new_scene = BasicClasses.Scene(dests=dests, peds=peds, boxes=boxes)
    g_gui = SfmGuiTest(new_scene)

    g_gui.root.mainloop()
