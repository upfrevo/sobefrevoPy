import logging
import logging.handlers
import os
import time
 

 
try:
    exit(main())
except Exception:
    logging.exception("Exception in main()")
    exit(1)
