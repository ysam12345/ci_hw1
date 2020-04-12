#!/usr/bin/env python
# coding:utf-8
import numpy as np
from tkinter import *
import tkinter as tk
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.lines as lines
from tkinter.filedialog import askopenfilename
from data import Data
from car import Car
from road import Road
from gui_utils import add_text, add_button, add_spinbox


class GUI(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.root = master
        self.grid()
        self.data = self.load_data()
        self.car, self.road = self.init_components()
        self.create_widgets()
        self.clean_fig()
        self.draw_road(self.road.finish_area, self.road.road_edges)
        self.draw_car(self.car.loc(), self.car.car_degree, self.car.radius)

    def load_data(self):
        case_file_path = '../cases/case01.txt'
        d = Data(case_file_path)
        return d.get()

    def init_components(self):
        c = Car(self.data['start_point'], self.data['start_degree'])
        c.update_sensor(self.data['road_edges'])
        r = Road(self.data['finish_area'], self.data['road_edges'])
        return c, r

    def create_widgets(self):
        # 標題
        self.winfo_toplevel().title("Yochien CI HW1")

        # 自走車位置、方向、感測器距離
        _, self.loc = add_text(self, 0, "Car Location", self.car.loc())
        _, self.fl = add_text(self,
                                   1, "Car Sensor Front Left", self.car.sensor_dist['fl'])
        _, self.f = add_text(self,
                                  2, "Car Sensor Front", self.car.sensor_dist['f'])
        _, self.fr = add_text(self,
                                   3, "Car Sensor Front Right", self.car.sensor_dist['fr'])
        _, self.cd = add_text(self,
                                   4, "Car Degree", self.car.car_degree)
        _, self.swd = add_text(self,
                                    5, "Car Steering Wheel Degree", self.car.steering_wheel_degree)
        # 更新車子
        _, self.next = add_button(self,
                                       6, "Move Car to Next Step", "Update", self.update_car)
        # 轉方向盤
        _, self.tswd = add_spinbox(
            self, 7, "Turn Steering Wheel Degree", -40, 40)
        _, self.tb = add_button(self,
                                     8, "Turn Steering Wheel", "Apply", self.turn_steering_wheel)

        # 地圖與道路
        self.road_fig = Figure(figsize=(5, 5), dpi=120)
        self.road_canvas = FigureCanvasTkAgg(
            self.road_fig, self)
        self.road_canvas.draw()
        self.road_canvas.get_tk_widget().grid(row=9, column=0, columnspan=3)

    def turn_steering_wheel(self):
        self.car.turn_steering_wheel(int(self.tswd.get()))

    def update_car(self):
        self.car.next()
        self.loc["text"] = self.car.loc()
        self.cd["text"] = self.car.car_degree
        self.swd["text"] = self.car.steering_wheel_degree
        self.clean_fig()
        self.draw_road(self.road.finish_area, self.road.road_edges)
        self.draw_car(self.car.loc(), self.car.car_degree, self.car.radius)
        self.road_canvas.draw()

    def clean_fig(self):
        # 清空並初始化影像
        self.road_fig.clf()
        self.road_fig.ax = self.road_fig.add_subplot(111)
        self.road_fig.ax.set_aspect(1)
        self.road_fig.ax.set_xlim([-20, 60])
        self.road_fig.ax.set_ylim([-10, 60])

    def draw_road(self, finish_area, road_edges):
        # 車道邊界
        for i in range(len(road_edges)-1):
            self.road_fig.ax.text(road_edges[i][0], road_edges[i][1], '({},{})'.format(
                road_edges[i][0], road_edges[i][1]))
            self.road_fig.ax.plot([road_edges[i][0], road_edges[i+1][0]], [
                                  road_edges[i][1], road_edges[i+1][1]], 'k')

        # 終點區域
        a, b = finish_area[0]
        c, d = finish_area[1]
        self.road_fig.ax.plot([a, c], [b, b], 'r')
        self.road_fig.ax.plot([c, c], [b, d], 'r')
        self.road_fig.ax.plot([c, a], [d, d], 'r')
        self.road_fig.ax.plot([a, a], [d, b], 'r')

    def draw_car(self, loc, car_degree, radius):
        # 車子範圍
        self.road_fig.ax.plot(loc[0], loc[1], '.b')
        circle = plt.Circle(loc, radius, color='b', fill=False)
        self.road_fig.ax.add_artist(circle)
        # 感測器
        self.fl["text"], self.f["text"], self.fr["text"] = self.car.update_sensor(
            self.data['road_edges'])
        for s in self.car.sensor_point:
            self.road_fig.ax.plot(
                [loc[0], self.car.sensor_point[s][0]],
                [loc[1], self.car.sensor_point[s][1]], 'r')
            self.road_fig.ax.plot(
                self.car.sensor_point[s][0], self.car.sensor_point[s][1], '.b')


if __name__ == "__main__":
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()
