import logging, time, traceback
import requests
import twitter, configparser

TIMEOUT=1
PERIOD=600 # period between pings, in seconds
TEST_URL="https://google.com"

# load twitter credentials
credentials = configparser.ConfigParser()
credentials.read('credentials.config')
credentials=credentials['DEFAULT']
consumer_key=credentials['consumer_key']
consumer_secret=credentials['consumer_secret']
access_token_key=credentials['access_token_key']
access_token_secret=credentials['access_token_secret']

def outageLogging():
    '''() -> Logger class
    set ups main log so that it outputs to outages.log and then returns the log'''
    logger = logging.getLogger('outages')
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(filename='outages.log', encoding='utf-8', mode='a')
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)
    return logger

log = outageLogging()
was_offline = False

offline_beginning = None

def offline_start():
    if not was_offline:
        offline_beginning=datetime.datetime.now()
        was_offline=True

def offline_end():
    offline_duration=datetime.datetime.now()-offline_beginning
    duration_str = str(offline_duration).split('.')[0]
    # tweet about it
    try:
        # log in
        api = twitter.Api(consumer_key=consumer_key,
                      consumer_secret=consumer_secret,
                      access_token_key=access_token_key,
                      access_token_secret=access_token_secret)
        msg = 'Internet just went down for Whitehaven residents for %s again. Please look into this @Rogers @RogersHelps ' %duration_str
        # publish tweet
        api.PostUpdate(msg)
        print('Tweeted about internet %s outage starting at %s' %(duration_str, offline_beginning.isoformat()) )
        was_offline=False
    except:
        print('Failed to tweet about internet %s outage starting at %s' %(duration_str, offline_beginning.isoformat()) )
        traceback.print_exc()

while True:
    start_time = time.perf_counter()
    try:
        response = requests.get(TEST_URL, timeout=TIMEOUT)
        if response.status_code != 200:
            # probably a server issue, but still possibly shitty internet
            log.info('Internet failed with error code %s' %response.status_code)
            offline_start()
        else:
            log.info('Internet working fine')
            if was_offline==True:
                offline_end()
    except:
        # definitely shitty internet
        log.warning('Internet failed to be reached')
        offline_start()
        # traceback.print_exc()

    time.sleep(PERIOD - (time.perf_counter()-start_time))
