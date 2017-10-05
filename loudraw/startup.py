from loudraw.server import Server, get_devices
from loudraw.imaging import SoundScape

import cv2

output_size = 1000
server = Server(idx=1)
scaper = SoundScape(server.channels)
ob_id = scaper.add_object()
server.init_mixer(ob_id, "/Users/alneuman/notification.wav", loop=True)

ob = scaper.objects[ob_id]
ob.set('center', (50, 50))
ob.set('radius', 40)
ob.set('blur', (20, 20))
ob.draw()
server.set_mixer(ob_id, scaper.amp_from_image(ob.canvas))


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
    # size -= 5
    # ob.set('radius', size)
    # ob.draw()
    # server.set_mixer(ob_id, scaper.amp_from_image(ob.canvas))
    # out = cv2.resize(scaper.get_sound_scape(), (output_size, output_size))
    # cv2.imshow('image', out)

cv2.destroyWindow('image')
