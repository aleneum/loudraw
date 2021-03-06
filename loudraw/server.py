import pyo
import logging
from time import sleep

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def get_devices():
    dev_list, dev_index = pyo.pa_get_output_devices()
    res = []
    for idx, dev_name in enumerate(dev_list):
        res.append(dict(idx=dev_index[idx], name=dev_name, channels=pyo.pa_get_output_max_channels(dev_index[idx])))
    return res


class Server(object):

    def __init__(self, idx, channels=None):
        self.channels = channels if channels is not None else pyo.pa_get_output_max_channels(idx)
        self.server = pyo.Server(nchnls=self.channels, ichnls=0).boot()
        self.server.start()
        self.mixers = {}
        self.files = {}

    def __del__(self):
        if self.server.getIsBooted():
            self.server.stop()
            # shutdown takes some time
            sleep(0.2)
            self.server.shutdown()
            del self.server

    def init_mixer(self, identifier, file_path, loop=False, amp=0.1, channels=None):
        sf = pyo.SfPlayer(file_path, loop=loop)
        mixer = pyo.Mixer(outs=self.channels, chnls=1)
        mixer.addInput(0, sf)
        for o in range(self.channels):
            mixer.setAmp(0, o, amp)
        self.mixers[identifier] = mixer
        self.files[identifier] = sf
        if channels is not None:
            self.set_mixer(identifier, channels)
        mixer.out()
        sf.play()

    def set_mixer(self, identifier, channels):
        m = self.mixers[identifier]
        for o in range(self.channels):
            m.setAmp(0, o, channels[o])
