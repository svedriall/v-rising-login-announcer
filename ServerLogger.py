import logging
import time

logfileDir = "..\VRisingServer.log"



logging.basicConfig(filename="serverlogs.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')



logger = logging.getLogger()
 
# Setting the threshold of logger to DEBUG
logger.setLevel(logging.DEBUG)
 
# Test messages
logger.debug("Harmless debug Message")
logger.info("Just an information")
logger.warning("Its a Warning")
logger.error("Did you try to divide by zero")
logger.critical("Internet is down")


def follow(the_file):
    the_file.seek(0, 2)
    while True:
        file_line = the_file.readline()
        if not file_line:
            time.sleep(0.1)
            continue
        yield file_line

log_file = open(logfileDir, "r")
log_lines = follow(log_file)


for line in log_lines:
    logger.debug(line)
