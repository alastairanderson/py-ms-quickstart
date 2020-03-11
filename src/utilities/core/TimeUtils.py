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

#region sandbox
# print("hello")
# TimeUtils.sleep_for_time_period(5)
# print("world")

# print("hello")
# TimeUtils.sleep_for_random_time_period(2,4)
# print("world")
#endregion
