import sys, os
import datetime
import fitbit
import time
import dotenv
import math
sys.path.append(os.path.join('../..', 'core'))
    
import core
from core import vrc_osc_client

def update_token(token):
    dotenv_file = dotenv.find_dotenv()
    dotenv.set_key(dotenv_file, "ACCESS_TOKEN", token.access_token)
    dotenv.set_key(dotenv_file, "REFRESH_TOKEN", token.refresh_token)

def get_percentile(values, p):
    length = len(values) # 全体の個数
    target_index = math.floor(length * p)
    return sorted(values)[target_index]

def get_heart_rate(datas):
    values = list(map(lambda x: x['value'], datas))
    latest = values[-1]
    return (latest, get_percentile(values, 0.005), get_percentile(values, 0.995))

def to_ascii_code_float(str):
    ret = []
    for ch in str:
        ret.append((ord(ch) - 32) / 100)
    return ret

if __name__ == "__main__":
    dotenv.load_dotenv()

    client_id = os.environ.get("CLIENT_ID")
    client_secret = os.environ.get("CLIENT_SECRET")
    access_token = os.environ.get("ACCESS_TOKEN")
    refresh_token = os.environ.get("REFRESH_TOKEN")

    fitbitClient = fitbit.Fitbit(client_id, client_secret,
                           access_token=access_token, refresh_token=refresh_token,
                           refresh_cb=update_token)

    today = datetime.date.today()
    formatted_today = today.strftime('%Y-%m-%d')

    vrcOscClients = []
    for i in range(1, 17):
        vrcOscClients.append(
            vrc_osc_client.VrcOscClient('Char_' + str(i))
        )

    while True:
        now = datetime.datetime.now() + datetime.timedelta(minutes=1)
        ten_prev_now = datetime.datetime.now() - datetime.timedelta(minutes=30)

        formatted_now = now.strftime('%H:%M')
        formatted_ten_prev_now = ten_prev_now.strftime('%H:%M')

        response = fitbitClient.intraday_time_series('activities/heart', formatted_today, detail_level='1sec', start_time=formatted_ten_prev_now, end_time=formatted_now)
        dataset = response['activities-heart-intraday']['dataset']

        if not dataset:
            continue

        latest, minimum, maximum = get_heart_rate(dataset)

        val = f"{latest:03} >{minimum:03} <{maximum:03}   "
        print(f"send: {val}")
        ascii_val = to_ascii_code_float(val)

        for oscClient, ascii in zip(vrcOscClients, ascii_val):
            oscClient.send_message(ascii)
        time.sleep(30)
