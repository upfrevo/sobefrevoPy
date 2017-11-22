import logging
import logging.handlers
import os
import time
 
handler = logging.handlers.WatchedFileHandler(
    os.environ.get("LOGFILE", "LOG{}.log".format(time.strftime("_%Y_%m_%d"))))
formatter = logging.Formatter(logging.BASIC_FORMAT)
handler.setFormatter(formatter)
root = logging.getLogger()
root.setLevel(os.environ.get("LOGLEVEL", "INFO"))
root.addHandler(handler)
 
try:
    exit(main())
except Exception:
    logging.exception("Exception in main()")
    exit(1)
