""" Android phone
"""
import logging
import signal
import os
import time
import queue
from volta.common.interfaces import Phone
from volta.common.util import popen, Drain, execute
from volta.common.resource import manager as resource
from volta.Boxes.box_binary import VoltaBoxBinary


logger = logging.getLogger(__name__)


lightning_apk_fullname = "net.yandex.overload.lightning"


class AndroidPhone(Phone):
    def __init__(self, config, volta):
        Phone.__init__(self, config, volta)
        self.volta = volta
        self.source = config.get('source', '00dc3419957ba583')
        self.lightning_apk_path = config.get('lightning', 'binary/lightning.apk')
        self.lightning_apk_fname = None

    def prepare(self):
        """
        pipeline:
            install lightning
            install apks
            clean log
        """
        # test
        self.lightning_apk_fname = resource.get_opener(self.lightning_apk_path).get_filename

        logger.info('Uninstalling lightning...')
        execute("adb -s {dev} uninstall {apk}".format(dev=self.source, apk=lightning_apk_fullname))
        logger.info('Installing lightning apk...')
        execute("adb -s {dev} install {apk}".format(dev=self.source, apk=self.lightning_apk_fname))


    def start(self):
        """
        pipeline:
            unplug device
            volta.start
            start lightning flashes
        """
        pass

    def run_test(self):
        """
        run apk
        """
        pass

    def end(self):
        """
        volta.stop
        plug device
        get logs from device
        """
        pass





# ==================================================

def main():
    logging.basicConfig(
        level="DEBUG",
        format='%(asctime)s [%(levelname)s] [Volta Phone Android] %(filename)s:%(lineno)d %(message)s')
    logger.info("Volta Phone Anroid ")
    cfg_volta = {
    }
    cfg_phone = {
        'source': '00dc3419957ba583'
    }
    volta = VoltaBoxBinary(cfg_volta)
    worker = AndroidPhone(cfg_phone, volta)
    logger.info('worker args: %s', worker.__dict__)
    worker.prepare()
    time.sleep(10)
    logger.info('test finished')

if __name__ == "__main__":
    main()