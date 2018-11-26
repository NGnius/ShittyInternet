import logging, time, traceback
import requests

TIMEOUT=1
PERIOD=600 # period between pings, in seconds
TEST_URL="https://google.com"

def outageLogging():
    '''() -> Logger class
    set ups main log so that it outputs to ./main.log and then returns the log'''
    logger = logging.getLogger('outages')
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(filename='outages.log', encoding='utf-8', mode='w')
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)
    return logger

log = outageLogging()
while True:
    start_time = time.perf_counter()
    try:
        response = requests.get(TEST_URL, timeout=TIMEOUT)
        if response.status_code != 200:
            # probably a server issue, but still possibly shitty internet
            log.info('Internet failed with error code %s' %response.status_code)
        else:
            log.info('Internet working fine')
    except:
        # definitely shitty internet
        log.warning('Internet failed to be reached')
        # traceback.print_exc()

    time.sleep(PERIOD - (time.perf_counter()-start_time))
