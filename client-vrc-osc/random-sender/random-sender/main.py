import sys, os
import random
import time

sys.path.append(os.path.join('../..', 'core'))

import core
from core import vrc_osc_client

if __name__ == "__main__":
    client = vrc_osc_client.VrcOscClient('test')

    while True:
        num = random.random()
        print("send " + str(num))
        client.send_message(random.random())
        time.sleep(5)
