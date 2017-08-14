import requests


class IftttEventEmitter(object):
    def __init__(self, secret_key):
        self.secret_key = secret_key

    def emit(self, event_name):
        requests.get('https://maker.ifttt.com/trigger/' + event_name + '/with/key/' + self.secret_key)
