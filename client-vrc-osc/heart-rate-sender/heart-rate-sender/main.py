from websocket_server import WebsocketServer
import sys, os
import datetime
import time
import dotenv
import math
import json
sys.path.append(os.path.join('../..', 'core'))
    
import core
from core import vrc_osc_client

class Websocket_Server():
    def __init__(self, host, port):
        self.server = WebsocketServer(port=port, host=host)

        self.vrcOscClients = []
        for sh_i in range(1, 17):
            self.vrcOscClients.append(
                vrc_osc_client.VrcOscClient('Char_' + str(sh_i))
            )

        self.last_five_minutes_data = []

    def message_received(self, client, server, message):
        try:
            decoded_msg = json.loads(message)
            last_heart_rate = decoded_msg["heartRate"]

            if not last_heart_rate:
                return

            if len(self.last_five_minutes_data) <= 300:
                self.last_five_minutes_data.append(last_heart_rate)
            else:
                self.last_five_minutes_data.pop(0)
                self.last_five_minutes_data.append(last_heart_rate)

            latest, minimum, maximum = get_heart_rate(self.last_five_minutes_data)

            val = f"[{latest:03}] >{minimum:03} <{maximum:03}"
            print(f"send: {val}")
            ascii_val = to_ascii_code_float(val)
            ascii_val.append(0.95)

            for oscClient, ascii in zip(self.vrcOscClients, ascii_val):
                oscClient.send_message(ascii)
        except:
            val = "Exception Occurred."
            print(f"send: {val}")
            ascii_val = to_ascii_code_float(val)

            for oscClient, ascii in zip(self.vrcOscClients, ascii_val):
                oscClient.send_message(ascii)

    def run(self):
        # メッセージ受信時のコールバック関数にself.message_received関数をセット
        self.server.set_fn_message_received(self.message_received)
        self.server.run_forever()

def get_percentile(values, p):
    length = len(values) # 全体の個数
    target_index = math.floor(length * p)
    return sorted(values)[target_index]

def get_heart_rate(data):
    latest = data[-1]
    return (latest, get_percentile(data, 0.005), get_percentile(data, 0.995))

def to_ascii_code_float(str):
    ret = []
    for ch in str:
        ret.append((ord(ch) - 32) / 100)
    return ret

if __name__ == "__main__":
    dotenv.load_dotenv()
    ip_addr = os.environ.get("IP_ADDR")
    port = os.environ.get("PORT")

    ws_server = Websocket_Server(ip_addr, int(port))
    ws_server.run()

