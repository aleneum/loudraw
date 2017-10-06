import cv2
import numpy as np

from .object import DirectedSource, UndirectedSource

HUE_ROT = 16
HUE_CYCLE = 180


class SoundScape(object):

    object_cls = dict(undirected=UndirectedSource, directed=DirectedSource)

    def __init__(self, channels_num, resolution=100, radius=0.25, center=(0.5,0.5)):
        self.objects = {}
        self.resolution = resolution
        channels_distance_angle = 360 / float(channels_num)
        self.channels_angles = [idx * channels_distance_angle for idx in range(channels_num)]
        self.channels_pos = [get_point(a, resolution * radius,resolution * center[0],
                                       resolution * center[1]) for a in self.channels_angles]
        self.channels_pos = self.channels_pos[::-1]
        self.channels_idx = [(y, x) for x, y in self.channels_pos]
        self.hue_cursor = 0

        self.ring_image = np.zeros((resolution, resolution, 3), np.uint8)
        for x, y in self.channels_pos:
            cv2.circle(self.ring_image, (x, y), 2, (255, 255, 255), -1)

    def amp_from_image(self, image):
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        result = [hsv[c][2] / 255.0 for c in self.channels_idx]
        return result

    def add_object(self, cls='undirected', **kwargs):
        obj_id = self.hue_cursor
        color = cv2.cvtColor(np.uint8([[[self.hue_cursor, 255, 255]]]), cv2.COLOR_HSV2BGR)[0, 0]
        # color needs to be converted to np.int64 otherwise opencv returns an error
        self.objects[self.hue_cursor] = self.object_cls[cls](self.resolution, color=color.astype(np.int64, copy=False),
                                                             **kwargs)
        self.hue_cursor = (self.hue_cursor + HUE_ROT) % HUE_CYCLE
        print(obj_id)
        return obj_id

    def get_sound_scape(self):
        res = self.ring_image.copy()
        for o in self.objects.values():
            res += o.canvas
        return res


def get_point(a, r=1, cx=0, cy=0):
    rad = np.deg2rad(a)
    x = cx + r * np.cos(rad)
    y = cy + r * np.sin(rad)
    return int(x), int(y)

