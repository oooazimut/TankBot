import asyncio
import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()


async def mailer():
    print(datetime.datetime.now(), 'sometext')

# job =  scheduler.add_job(mailer, 'interval', hours=2, next_run_time=datetime.datetime.now(), id='warn_mailer')


async def main():
    scheduler.start()
    scheduler.add_job(mailer, trigger='interval', hours=2, next_run_time=datetime.datetime.now(), id='mailer')
    await asyncio.sleep(1)
    scheduler.remove_job('mailer')
    print(datetime.datetime.now(), 'paused')
    await asyncio.sleep(5)
    print(datetime.datetime.now(), 'end_paused')
    scheduler.add_job(mailer, trigger='interval', hours=2, next_run_time=datetime.datetime.now(), id='mailer')
    scheduler.print_jobs()


if __name__ == '__main__':
    asyncio.run(main())
