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

    def __init__(self, idx):
        self.channels = pyo.pa_get_output_max_channels(idx)
        self.server = pyo.Server(nchnls=self.channels).boot()
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

    def init_mixer(self, identifier, file_path, loop=False, amp=0.1):
        sf = pyo.SfPlayer(file_path, loop=loop)
        mixer = pyo.Mixer(outs=self.channels, chnls=1)
        mixer.addInput(0, sf)
        for o in range(self.channels):
            mixer.setAmp(0, o, amp)
        mixer.out()
        self.files[identifier] = sf
        self.mixers[identifier] = mixer

    def set_mixer(self, identifier, channels):
        m = self.mixers[identifier]
        for o in range(self.channels):
            m.setAmp(0, o, channels[o])
