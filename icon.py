import math

from kivy.graphics import Callback, Color, Line, Triangle
from kivy.uix.widget import Widget

from myButton import text_color


class Icon(Widget):

    def __init__(self, icon='information', button_margin=6, color=text_color,  **kwargs):
        super().__init__(**kwargs)
        self.icon = icon
        self.canvas.add(Callback(self.draw_icon))
        self.instructions = None
        self.color = color
        self.buttonMargin = button_margin

    def draw_icon(self, instr):
        self.canvas.after.clear()
        pos_center = self.to_window(*self.center)
        pos = self.to_window(*self.pos)
        if self.width > self.height:
            size = self.height
            x = pos_center[0] - size / 2
            y = pos[1]
        else:
            size = self.width
            x = pos[0]
            y = pos_center[1] - size / 2

        with self.canvas.after:
            Color(rgba=self.color)
            if self.icon == 'exclamation':
                point_t1 = (x, y)
                point_t2 = (pos_center[0] - 0.1, y + size)
                point_t3 = (x + size, y)
                point1 = (pos_center[0], y + 8)
                point2 = (pos_center[0], y + 16)
                point3 = (pos_center[0], y + size - 16)
                Line(points=[point_t1, point_t2, point_t3], width=1.1, close=True)
                Line(points=[point1, point1], width=2)
                Line(points=[point2, point3], width=2)
            elif self.icon == 'pentagram':
                Color(rgba=[1, 0, 0, 1])
                cx1 = math.sin(2 * math.pi / 5)
                cx2 = math.sin(4 * math.pi / 5)
                cy1 = math.cos(2 * math.pi / 5)
                cy2 = math.cos(math.pi / 5)
                cx1 = cx1 * size / 2
                cx2 = cx2 * size / 2
                cy1 = cy1 * size / 2
                cy2 = cy2 * size / 2
                point1 = (pos_center[0], y)
                point4 = (pos_center[0] + cx1, pos_center[1] - cy1)
                point5 = (pos_center[0] - cx2, pos_center[1] + cy2)
                point2 = (pos_center[0] + cx2, pos_center[1] + cy2)
                point3 = (pos_center[0] - cx1, pos_center[1] - cy1)
                Line(points=[point1, point2, point3, point4, point5], width=1.1, close=True)
                Line(ellipse=(x, y, size, size), width=1.1)
            elif self.icon == 'uparrow':
                point_t1 = (x, y)
                point_t2 = (pos_center[0] - 0.1, y + size)
                point_t3 = (x + size, y)
                Triangle(points=(point_t1[0], point_t1[1], point_t2[0], point_t2[1],
                                 point_t3[0], point_t3[1]), width=1.1, close=True)
            elif self.icon == 'downarrow':
                point_t1 = (x, y + size)
                point_t2 = (pos_center[0] - 0.1, y)
                point_t3 = (x + size, y + size)
                Triangle(points=(point_t1[0], point_t1[1], point_t2[0], point_t2[1],
                                 point_t3[0], point_t3[1]), width=1.1, close=True)
            elif self.icon == 'close':
                point1 = (x, y)
                point2 = (x + size, y + size)
                point3 = (x + size, y)
                point4 = (x, y + size)
                Line(points=[point1, point2], width=1.2, cap='square')
                Line(points=[point3, point4], width=1.2, cap='square')
            elif self.icon == 'maximize':
                point1 = (x, y)
                point2 = (x, y + size)
                point3 = (x + size, y + size)
                point4 = (x + size, y)
                Line(points=[point1, point2, point3, point4], width=1.2, close=True)
            elif self.icon == 'restore':
                point1 = (x, y)
                point2 = (x, y + size - 4)
                point3 = (x + size - 4, y + size - 4)
                point4 = (x + size - 4, y)
                Line(points=[point1, point2, point3, point4], width=1.2, close=True)
                point1 = (x + 4, y + size - 4)
                point2 = (x + 4, y + size)
                point3 = (x + size, y + size)
                point4 = (x + size, y + 4)
                point5 = (x + size - 4, y + 4)
                Line(points=[point1, point2, point3, point4, point5], width=1.2)
            elif self.icon == 'minimize':
                point1 = (x + 2, pos_center[1])
                point2 = (x + size - 2, pos_center[1])
                Line(points=[point1, point2], cap='square', width=1.2)
            else:
                point1 = (pos_center[0], y + 12)
                point2 = (pos_center[0], y + size - 20)
                point3 = (pos_center[0], y + size - 12)
                Line(ellipse=(x, y, size, size), width=1.1)
                Line(points=[point1, point2], width=2)
                Line(points=[point3, point3], width=2)

        self.canvas.ask_update()

    def get_instr(self):
        self.draw_icon(None)
        return self.canvas.after.children
