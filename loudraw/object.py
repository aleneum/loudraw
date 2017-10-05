import cv2
import numpy as np


class SoundObject(object):
    draw_func = cv2.circle
    params = dict(center=(0, 0), radius=5, thickness=-1)
    blur = (1, 1)

    def __init__(self, canvas_size, color):
        print(color)
        self.params['color'] = color
        self.canvas = np.zeros((canvas_size, canvas_size, 3), np.uint8)

    def draw(self, reset=True):
        if reset:
            self.canvas.fill(0)
        self.draw_func(self.canvas, **self.params)
        if self.blur[0] > 0 and self.blur[1] > 0:
            self.canvas = cv2.blur(self.canvas, self.blur)

    def set(self, param, value):
        if param in self.params:
            self.params[param] = value
        else:
            setattr(self, param, value)
