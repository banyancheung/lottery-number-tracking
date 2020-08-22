#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from app import lottery_job_run
from apscheduler.schedulers.blocking import BlockingScheduler


def main():
    scheduler = BlockingScheduler()
    scheduler.add_job(lottery_job_run, id='lottery_job', trigger='cron', hour='22', minute='0')
    try:
        scheduler.start()
    except SystemExit:
        print('exit')
        exit()


if __name__ == '__main__':
    main()
