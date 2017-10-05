from unittest import TestCase, skipIf

try:
    from unittest.mock import MagicMock
except ImportError:
    from mock import MagicMock

import loudraw.server


class TestServer(TestCase):

    def setUp(self):
        self.server = None

    def tearDown(self):
        if self.server is not None:
            del self.server

    def test_get_devices(self):
        res = loudraw.server.get_devices()
        for device in res:
            assert 'idx' in device
            assert 'channels' in device

    def test_init(self):
        res = loudraw.server.get_devices()
        self.server = loudraw.server.Server(res[0]['idx'])
