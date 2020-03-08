import time
from random import randint


class TimeUtils:

    @staticmethod
    def sleep_for_random_time_period(start_second, end_second):
        random_sleep_period = randint(start_second, end_second)
        time.sleep(random_sleep_period)


    @staticmethod
    def sleep_for_time_period(seconds):
        time.sleep(seconds)