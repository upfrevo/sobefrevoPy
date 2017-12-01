import time, logging, logging.handlers, os, datetime
import envio_email

def log_info(msg):
    logging.info(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()) + " - " + msg)

def log_excecao(msg):
    logging.exception(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()) + ' - ' + msg)
    envio_email.envia_email("Erro no sistema", msg)

def init():
    handler = logging.handlers.WatchedFileHandler(
    os.environ.get("LOGFILE", "logs/LOG{}.log".format(time.strftime("_%Y_%m_%d"))))
    formatter = logging.Formatter(logging.BASIC_FORMAT)
    handler.setFormatter(formatter)
    root = logging.getLogger()
    root.setLevel(os.environ.get("LOGLEVEL", "INFO"))
    root.addHandler(handler)

