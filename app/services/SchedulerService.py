from flask_apscheduler import APScheduler

scheduler = APScheduler()


@scheduler.task('interval', id='do_job_1', seconds=3)
def job1():
    print('Job 1 executed')
