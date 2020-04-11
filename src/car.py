from numpy import sin, arcsin, cos, pi
from utils import line_intersec, dist

class Car():
    def __init__(self, start_point, start_degree, radius=3):
        self.start_poin = start_point
        self.start_degree = start_degree
        self.radius = radius
        self.x = start_point[0]
        self.y = start_point[1]
        self.car_degree = start_degree
        self.wheel_degree = 0
        self.sensor_dist = {
            "fl": 0,
            "f": 0,
            "fr": 0
        }
        self.sensor_point = {
            "fl": [0,0],
            "f": [0,0],
            "fr": [0,0]
        }

    def sensor(self):
        front_left_degree = self.car_degree + 45
        front_right_degree = self.car_degree - 45
        detect_range = 100
        # sensor detect point
        fl_x = self.x + cos(pi * front_left_degree / 180) * detect_range
        fl_y = self.y + sin(pi * front_left_degree / 180) * detect_range
        f_x = self.x + cos(pi * self.car_degree / 180) * detect_range
        f_y = self.y + sin(pi * self.car_degree / 180) * detect_range
        fr_x = self.x + cos(pi * front_right_degree / 180) * detect_range
        fr_y = self.y + sin(pi * front_right_degree / 180) * detect_range
        return [fl_x, fl_y], [f_x, f_y], [fr_x, fr_y]

    def update_sensor(self, road_edges):
        fl, f, fr = self.sensor()
        road_lines = [[road_edges[i], road_edges[i+1]] for i in range(len(road_edges)-1)]
        s_lines = {
            "fl": [self.loc(), fl],
            "f": [self.loc(), f],
            "fr": [self.loc(), fr]
        }
        s_p = {"fl":[],"f":[],"fr":[]}
        for sensor in s_lines:
            self.sensor_dist[sensor] = 100000
            for l in road_lines:
                p = line_intersec(l, s_lines[sensor])
                if p is not None:
                    s_p[sensor].append(p)
            for p in s_p[sensor]:
                if dist([self.x,self.y],p) < self.sensor_dist[sensor]:
                    self.sensor_dist[sensor] = dist([self.x,self.y],p)
                    self.sensor_point[sensor] = p
        return sensor_dist['fl'], sensor_dist['f'], sensor_dist['fr']

    def loc(self):
        return [self.x, self.y]

    def turn_wheel(self, wheel_degree):
        self.wheel_degree = wheel_degree

    def next(self):
        self.x += cos(self.wheel_degree+self.car_degree) + \
            sin(self.car_degree)*sin(self.wheel_degree)
        self.y = sin(self.wheel_degree+self.car_degree) - \
            sin(self.car_degree)*cos(self.wheel_degree)
        self.wheel_degree -= arcsin(2*sin(self.wheel_degree)/(2*self.radius))
