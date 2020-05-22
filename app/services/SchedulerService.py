from flask_apscheduler import APScheduler
from datetime import datetime, timedelta
from app.models.Job import Job
from time import sleep

scheduler = APScheduler()


def create_task(name, func, args=None, seconds=0, minutes=0):
    run_date = datetime.now() + timedelta(seconds=seconds, minutes=minutes)

    job = Job.create(name=name, run_date=run_date)

    if args is None:
        args = [job.id]

    scheduler.add_job(id=str(job.id), func=func, args=args, trigger='date', run_date=run_date)

    return job


def job_added_listener(event):
    print(f"Listener: job {event.job_id} added")


def job_submitted_listener(event):
    job = Job.find(event.job_id)
    print(f"Listener: job {event.job_id} started")
    job.set_status(Job.RUNNING)


def job_executed_listener(event):
    job = Job.find(event.job_id)
    print(f"Listener: job {event.job_id} executed. Task {job.name} finished")
    job.set_status(Job.DONE)


def test_job(*args, **kwargs):
    sleep(5)
