import cv2
import numpy as np


class UndirectedSource(object):
    draw_func = cv2.circle
    params = dict(thickness=-1)
    _blur = (1, 1)

    def __init__(self, canvas_size, color, center=(0, 0), radius=0.1, blur=(0, 0)):
        self.canvas_size = canvas_size
        self.canvas = np.zeros((canvas_size, canvas_size, 3), np.uint8)
        self.color = color
        self.center = center
        self.radius = radius
        self.blur = blur
        self.draw()

    @property
    def color(self):
        return self.params['color']

    @color.setter
    def color(self, color):
        self.params['color'] = color

    @property
    def center(self):
        return self.params['center']

    @center.setter
    def center(self, center):
        self.params['center'] = (int((center[0] / 2 + 0.5) * self.canvas_size),
                                 int((center[1] / -2 + 0.5) * self.canvas_size))

    @property
    def radius(self):
        return self.params['radius']

    @radius.setter
    def radius(self, radius):
        self.params['radius'] = int(self.canvas_size * radius)

    @property
    def blur(self):
        return self._blur

    @blur.setter
    def blur(self, blur):
        self._blur = tuple(max(1, int(b * self.canvas_size)) for b in blur)

    def draw(self, reset=True):
        if reset:
            self.canvas.fill(0)
        self.draw_func(self.canvas, **self.params)
        if self.blur[0] > 0 and self.blur[1] > 0:
            self.canvas = cv2.blur(self.canvas, self.blur)

    def set(self, param, value):
        setattr(self, param, value)


class DirectedSource(object):
    draw_func = cv2.fillConvexPoly
    params = dict(points=[(0, 0), (-0.1, 0.1), (0.1, 0.1)])
    _blur = (1, 1)
    _radius = 1
    _center = (0, 0)
    _angle = 5
    _rotation = 0

    def __init__(self, canvas_size, color, center=(0, 0), radius=0.1, blur=(0, 0), angle=15, rotation=0):
        self.canvas_size = canvas_size
        self.canvas = np.zeros((canvas_size, canvas_size, 3), np.uint8)
        self.color = color
        self.center = center
        self.radius = radius
        self.angle = angle
        self.blur = blur
        self.draw()
        self.rotation = rotation

    @property
    def color(self):
        return self.params['color']

    @color.setter
    def color(self, color):
        self.params['color'] = color

    @property
    def center(self):
        return self._center

    @center.setter
    def center(self, center):
        self._center = (int((center[0] / 2 + 0.5) * self.canvas_size),
                        int((center[1] / -2 + 0.5) * self.canvas_size))
        self._calculate_points()

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, radius):
        self._radius = radius
        self._calculate_points()

    @property
    def blur(self):
        return self._blur

    @blur.setter
    def blur(self, blur):
        self._blur = tuple(max(1, int(b * self.canvas_size)) for b in blur)

    def draw(self, reset=True):
        if reset:
            self.canvas.fill(0)
        self.draw_func(self.canvas, **self.params)
        if self.blur[0] > 0 and self.blur[1] > 0:
            self.canvas = cv2.blur(self.canvas, self.blur)

    def set(self, param, value):
        setattr(self, param, value)

    def _calculate_points(self):
        p_y = int(self._radius * self.canvas_size)
        a = int(p_y * np.tan(np.deg2rad(self._angle)))
        points = np.array([self._center,
                           (self._center[0] - a, self._center[1] - p_y),
                           (self._center[0] + a, self._center[1] - p_y)])
        if self._rotation != 0:
            points[1] = rotate(self._center, points[1], self._rotation)
            points[2] = rotate(self._center, points[2], self._rotation)
        self.params['points'] = points

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, angle):
        self._angle = angle
        self._calculate_points()

    @property
    def rotation(self):
        return self._rotation

    @rotation.setter
    def rotation(self, rotation):
        self._rotation = rotation
        self._calculate_points()


def rotate(origin, point, angle):
    ox, oy = origin
    px, py = point
    angle = np.deg2rad(angle)

    qx = ox + np.cos(angle) * (px - ox) - np.sin(angle) * (py - oy)
    qy = oy + np.sin(angle) * (px - ox) + np.cos(angle) * (py - oy)
    return qx, qy
