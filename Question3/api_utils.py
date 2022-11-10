import requests
import json
import pandas as pd
import datetime
from retry import retry
import time

@retry(tries=10, delay=5)
def getDataAtTimestamp(year, month, day, hour, min_str='01', sec_str = '00'):
    try:
        site = f'https://api.data.gov.sg/v1/transport/carpark-availability?date_time={year}-{month.zfill(2)}-{day.zfill(2)}T{hour.zfill(2)}%3A{min_str.zfill(2)}%3A{sec_str.zfill(2)}'
        t1 = time.time()
        response_API = requests.get(site)
        t2 = time.time()
        response_API.encoding = 'UTF-8'
        raw_data = json.loads(response_API.content)
        t3 = time.time()
        print("req time = ", t2-t1, "json time = ", t3-t2)
        core_list = raw_data['items'][0]['carpark_data']
        return core_list
    except:
        raise Exception()

def json2csv(raw_data, timestamp):
    header = ['timestamp', 'carpark_number', 'total_lots', 'lots_available', 'lot_type']
    res_df = pd.DataFrame(columns=header)
    for ele in raw_data:
        info = ele['carpark_info'][0]
        res_df = pd.concat([res_df, pd.DataFrame([[str(timestamp), ele['carpark_number'], info['total_lots'], info['lots_available'], info['lot_type']]], columns=header)])
        # res_df = res_df.append({'timestamp': timestamp, 'carpark_number': ele['carpark_number'], 'total_lots': info['total_lots'], 'lots_available': info['lots_available'], 'lot_type': info['lot_type']}, ignore_index=True)
    return res_df