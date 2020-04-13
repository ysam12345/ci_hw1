from numpy import sin, arcsin, cos, pi
from utils import line_intersec, dist
from shapely.geometry import Point, Polygon


class Road():
    def __init__(self, finish_area, road_edges):
        self.finish_area = finish_area
        self.road_edges = road_edges
        self.finish_poly = self.get_finish_polygon()

    def get_finish_polygon(self):
        a, b = self.finish_area[0]
        c, d = self.finish_area[1]
        coords = [(a, b), (c, b), (
            c, d), (c, b), (a, b)]
        return Polygon(coords)

    def is_finish(self, car):
        loc = car.loc()
        p = Point(loc[0], loc[1])
        return self.is_in(p, self.finish_poly)

    def is_crash(self, car):
        for i in self.dist(car, self.road_edges):
            if i + 0.01 <= car.radius:
                return True
        return False

    def is_in(self, point, polygon):
        return point.within(polygon)

    def edge(self, car):
        detect_range = 100
        u_x = int(car.x + cos(pi * 90 / 180) * detect_range)
        u_y = int(car.y + sin(pi * 90 / 180) * detect_range)
        d_x = int(car.x + cos(pi * 270 / 180) * detect_range)
        d_y = int(car.y + sin(pi * 270 / 180) * detect_range)
        r_x = int(car.x + cos(pi * 0 / 180) * detect_range)
        r_y = int(car.y + sin(pi * 0 / 180) * detect_range)
        l_x = int(car.x + cos(pi * 180 / 180) * detect_range)
        l_y = int(car.y + sin(pi * 180 / 180) * detect_range)
        return [u_x, u_y], [d_x, d_y], [r_x, r_y], [l_x, l_y]

    def dist(self, car, edges):
        u, d, r, l = self.edge(car)
        road_lines = [[self.road_edges[i], self.road_edges[i+1]]
                      for i in range(len(self.road_edges)-1)]
        s_lines = {
            "u": [car.loc(), u],
            "d": [car.loc(), d],
            "r": [car.loc(), r],
            "l": [car.loc(), l]
        }
        s_p = {"u": [], "d": [], "r": [], "l": []}
        side_dist = {}
        side_point = {}
        for side in s_lines:
            side_point[side] = [0, 0]
            side_dist[side] = 100000
            for l in road_lines:
                p = line_intersec(l, s_lines[side])
                if p is not None:
                    s_p[side].append(p)
            for p in s_p[side]:
                if dist([car.x, car.y], p) < side_dist[side]:
                    side_dist[side] = dist([car.x, car.y], p)
                    side_point[side] = p
        return side_dist['u'], side_dist['d'], side_dist['r'], side_dist['l']
