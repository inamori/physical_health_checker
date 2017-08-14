#!/usr/bin/env python
import os
import numpy as np
from datetime import datetime

from ifttt_event_emitter import IftttEventEmitter
from fitbit_client import FitbitClient


class PhysicalHealthChecker(object):
    def __init__(self, provider, event_emitter):
        self.event_emitter = event_emitter
        self.heart_beat_provider = provider
        seconds, beats = self.heart_beat_provider.request_heart_beats('today')
        expected_beat = np.polyval(np.polyfit(seconds, beats, 1), seconds[-1] + 60)
        if self.is_alive(expected_beat):
            print 'still alive.'
        else:
            timestamp_file_name = 'death_time.txt'
            death_time = open(timestamp_file_name, 'r').read()
            if not death_time:
                print 'dead.'
                self.event_emitter.emit('death')
                with open(timestamp_file_name, 'w') as file:
                    file.write(datetime.now().strftime("%Y/%m/%d %H:%M:%S"))

    @staticmethod
    def is_alive(heart_beat):
        return heart_beat >= 10


if __name__ == '__main__':
    ifttt_key = os.getenv('IFTTT_WEB_HOOK_KEY')
    fitbitHealthChecker = PhysicalHealthChecker(FitbitClient(), IftttEventEmitter(ifttt_key))
