from multiprocessing.context import Process

from app.config import LOTTERY_DATA
from app.lottery_util import start_check_lottery


def lottery_job_run():
    p = Process(target=start_check_lottery)
    p.start()
