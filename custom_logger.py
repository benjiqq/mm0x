import logging
import colorlog
import os

#format="%(asctime)s [%(threadName)-12.12s] [%(filename)-18s] [%(name)s] [%(levelname)-5.5s]  %(message)s",        

#def setup_logger(logger_name, log_file, level=logging.DEBUG):
def setup_logger(logger_name, log_file, level=logging.DEBUG):
    l = logging.getLogger(logger_name)

    formatter = logging.Formatter('[%(name)s] %(asctime)s : %(message)s')

    logdir = "./log/"
    if not os.path.exists(logdir):
        os.makedirs(logdir)
    fileHandler = logging.FileHandler(logdir + log_file, mode='w')
    fileHandler.setFormatter(formatter)

    l.setLevel(level)
    l.addHandler(fileHandler)

    handler = colorlog.StreamHandler()
    colorformat = colorlog.ColoredFormatter('%(log_color)s[%(name)s] %(message)s - (%(asctime)s) %(lineno)d')
    handler.setFormatter(colorformat)

    l.addHandler(handler)

