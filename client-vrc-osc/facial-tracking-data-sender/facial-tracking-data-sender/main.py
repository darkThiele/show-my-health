from websocket_server import WebsocketServer
import sys, os
import dotenv
import logging
import json
sys.path.append(os.path.join('../..', 'core'))

import core
from core import vrc_osc_client

class Websocket_Server():

    def __init__(self, host, port):
        self.server = WebsocketServer(port=port, host=host)
        self.meme_base_line = MemeBaseLine()

        self.osc_ev = vrc_osc_client.VrcOscClient('eye_vertical')
        self.osc_eh = vrc_osc_client.VrcOscClient('eye_horizontal')
        self.osc_eb = vrc_osc_client.VrcOscClient('eye_blink')

        self.evl = 0.0 # 上下方向の目の状態
        self.evl_c = 0 # 上下のun状態の保持

        self.ehl = 0.0 # 左右方向の目の状態
        self.ehl_c = 0 # 左右のun状態の維持

    # クライアント接続時に呼ばれる関数
    def new_client(self, client, server):
        print(f"new client connected and was given id {client['id']}")

    # クライアントからメッセージを受信したときに呼ばれる関数
    def message_received(self, client, server, message):
        meme_val = MemeValue(message, self.meme_base_line)

        evl, ehl = meme_val.eyeMoveEvent()

        # 上下方向の目
        if (self.evl_c < 20):
            self.evl = self.evl + evl
            if not self.evl == 0:
                self.evl_c += 1
            else:
                self.evl_c = 0
        else:
            self.evl = 0.0
            self.evl_c = 0
        # self.osc_ev.send_message(self.evl)

        # 左右方向の目
        if (self.ehl_c < 20):
            self.ehl = self.ehl + ehl
            if not self.ehl == 0:
                self.ehl_c += 1
            else:
                self.ehl_c = 0
        else:
            self.ehl = 0.0
            self.ehl_c = 0
        self.osc_eh.send_message(self.ehl)

        # まばたきイベント
        self.osc_eb.send_message(meme_val.blinkEvent())

        print(meme_val.motion())
        print(f"send: 上下 {self.evl} 左右 {self.ehl} まばたき {meme_val.blinkEvent()}")

    def run(self):
        # クライアント接続時のコールバック関数にself.new_client関数をセット
        self.server.set_fn_new_client(self.new_client)

        # メッセージ受信時のコールバック関数にself.message_received関数をセット
        self.server.set_fn_message_received(self.message_received)
        self.server.run_forever()

class MemeBaseLine():

    def __init__(self):
        self.__roll_base = 0.0
        self.__pitch_base = 0.0
        self.__yaw_base = 0.0

        self.__base_line_point = 0
        self.__roll_base_list = []
        self.__pitch_base_list = []
        self.__yaw_base_list = []

    def getBase(self):
        return self.__roll_base, self.__pitch_base, self.__yaw_base

    def calcBase(self, roll, pitch, yaw):
        if self.__base_line_point < 100:
            # リストに追加
            self.__roll_base_list.append(roll)
            self.__pitch_base_list.append(pitch)
            self.__yaw_base_list.append(yaw)

            # 更新
            self.__roll_base = sum(self.__roll_base_list) / len(self.__roll_base_list)
            self.__pitch_base = sum(self.__pitch_base_list) / len(self.__pitch_base_list)
            self.__yaw_base = sum(self.__yaw_base_list) / len(self.__yaw_base_list)

            self.__base_line_point += 1


class MemeValue():

    def __init__(self, message, base_line):
        self.message = json.loads(message)
        self.base_line = base_line

    def eyeMoveEvent(self):
        # 各種上下左右イベント
        up_event = self.message['eyeMoveUp'] > 0
        down_event = self.message['eyeMoveDown'] > 0
        left_event = self.message['eyeMoveLeft'] > 0
        right_event = self.message['eyeMoveRight'] > 0

        # -1.0 | 0.0 | 1.0, -1.0 | 0.0 | 1.0
        # 上 1.0, 0.0 下 -1.0, 0.0 左 0.0, 1.0 右 0.0, -1.0
        return up_event - down_event, left_event - right_event

    def blinkEvent(self):
        blink_event = self.message['blinkStrength'] > 0
        # 0.0 | 1.0
        return blink_event

    def motion(self):
        roll = self.message['roll']
        pitch = self.message['pitch']
        yaw = self.message['yaw']

        self.base_line.calcBase(roll, pitch, yaw)
        base_roll, base_pitch, base_yaw = self.base_line.getBase()

        roll_float = (roll - base_roll) / 90
        pitch_float = (pitch - base_pitch) / 90
        yaw_float = (yaw - base_yaw) / 90
        if yaw_float < -2:
            yaw_float += 4

        return roll_float, pitch_float, yaw_float


dotenv.load_dotenv()
ip_addr = os.environ.get("IP_ADDR")
port = os.environ.get("PORT")

ws_server = Websocket_Server(ip_addr, int(port))
ws_server.run()