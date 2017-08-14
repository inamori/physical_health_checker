import fitbit
import os
import time
from ast import literal_eval


class FitbitClient(object):
    def __init__(self):
        self.client_id = os.getenv('FITBIT_CLIENT_ID')
        self.client_secret = os.getenv('FITBIT_CLIENT_SECRET')
        token_file_name = os.getenv('TOKEN_FILE_NAME')
        tokens = open(token_file_name).read()
        token_dict = literal_eval(tokens)
        self.access_token = token_dict['access_token']
        self.refresh_token = token_dict['refresh_token']

        def refresh_call_back(token):
            with open(token_file_name, 'w') as f:
                f.write(str(token))
            self.access_token = token['access_token']
            self.refresh_token = token['refresh_token']

        self.client = fitbit.Fitbit(
            self.client_id, self.client_secret,
            access_token=self.access_token, refresh_token=self.refresh_token,
            refresh_cb=refresh_call_back
        )

    def request_heart_beats(self, date, limit=30):
        data_sec = self.client.intraday_time_series('activities/heart', date, detail_level='1sec')
        heart_sec = data_sec['activities-heart-intraday']['dataset']
        heart_sec = heart_sec[-limit:]
        seconds = map(self.fetch_sec, heart_sec)
        beats = map(lambda data: data['value'], heart_sec)
        return seconds, beats

    @staticmethod
    def fetch_sec(data):
        t = time.strptime(data['time'], '%H:%M:%S')
        return t.tm_hour * 3600 + t.tm_min * 60 + t.tm_sec
