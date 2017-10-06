from .server import Server, get_devices
from .imaging import SoundScape
from .api import start_app

import cv2, sys

if len(sys.argv) < 2:
    print get_devices()
    sys.exit(0)

output_size = 1000
server = Server(idx=sys.argv[1])
scaper = SoundScape(server.channels)

app = start_app(scaper, server)

out = cv2.resize(scaper.get_sound_scape(), (output_size, output_size))
cv2.imshow('image', out)

#cv2.setMouseCallback('image', mouse_event)
mode = 0
size = 40
while True:
    k = cv2.waitKey(1000) & 0xFF
    if k == ord('p'):
        mode = 0
    elif k == ord('s'):
        mode = 1
    elif k == ord('b'):
        mode = 2
    elif k == 27:
        break

    out = cv2.resize(scaper.get_sound_scape(), (output_size, output_size))
    cv2.imshow('image', out)
    # size -= 5
    # ob.set('radius', size)
    # ob.draw()
    # server.set_mixer(ob_id, scaper.amp_from_image(ob.canvas))
    # out = cv2.resize(scaper.get_sound_scape(), (output_size, output_size))
    # cv2.imshow('image', out)

cv2.destroyWindow('image')
