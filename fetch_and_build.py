import requests
import json
import datetime
import os
import pandas as pd

# API Key 讀取方式（優先順序）：
# 1. 環境變數 DATABENTO_API_KEY
# 2. 同目錄下的 databento_config.json（不進版控，見 .gitignore）
def load_api_key():
    env_key = os.environ.get('DATABENTO_API_KEY')
    if env_key:
        return env_key
    cfg_path = os.path.join(os.path.dirname(__file__), 'databento_config.json')
    if os.path.exists(cfg_path):
        with open(cfg_path, 'r', encoding='utf-8') as f:
            cfg = json.load(f)
            return cfg.get('api_key')
    raise RuntimeError(
        '找不到 Databento API Key，請設定環境變數 DATABENTO_API_KEY，'
        '或建立 databento_config.json（可參考 databento_config.example.json）'
    )

KEY = load_api_key()
URL = 'https://hist.databento.com/v0/timeseries.get_range'

end_date = datetime.date.today()
start_date = end_date - datetime.timedelta(days=32)  # buffer for weekends/holidays -> ~1 month trading days

params = {
    'dataset': 'GLBX.MDP3',
    'symbols': 'HG.c.0',
    'stype_in': 'continuous',
    'schema': 'ohlcv-1d',
    'start': start_date.isoformat(),
    'end': end_date.isoformat(),
    'encoding': 'json'
}

def fetch():
    r = requests.get(URL, params=params, auth=(KEY, ''), timeout=60)
    r.raise_for_status()

    rows = []
    for line in r.text.strip().split('\n'):
        if not line.strip():
            continue
        d = json.loads(line)
        ts_ns = int(d['hd']['ts_event'])
        dt = datetime.datetime.utcfromtimestamp(ts_ns / 1e9).date()
        # Databento fixed-point price: scale 1e-9
        o = int(d['open']) / 1e9
        h = int(d['high']) / 1e9
        l = int(d['low']) / 1e9
        c = int(d['close']) / 1e9
        v = int(d['volume'])
        rows.append({'date': dt.isoformat(), 'open': o, 'high': h, 'low': l, 'close': c, 'volume': v})

    df = pd.DataFrame(rows).drop_duplicates(subset='date').sort_values('date').reset_index(drop=True)
    df.to_csv('copper_hg_daily.csv', index=False)
    print('ROWS:', len(df))
    if len(df):
        print('DATE RANGE:', df['date'].min(), 'to', df['date'].max())
        print('LAST CLOSE:', df['close'].iloc[-1])
    return df

if __name__ == '__main__':
    fetch()
