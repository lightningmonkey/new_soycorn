import logging


class SoycornLogger(object):
    def __init__(self, file_name, verbose=False):
        if verbose:
            level = logging.DEBUG
        else:
            level = logging.INFO
        self.logger = logging.getLogger()
        self.logger.setLevel(level)
        formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
        # create file handler
        fh = logging.FileHandler("/var/log/soycorn/{0}".format(file_name))
        fh.setLevel(level)
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)
        # create console handler with a higher log level
        ch = logging.StreamHandler()
        ch.setLevel(level)
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warn(self, message):
        self.logger.warn(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)

    def start(self):
        self.logger.info("========== START ==========")

    def end(self):
        self.logger.info("=========== END ===========")

