from . import SchedulerService
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ADDED, EVENT_JOB_SUBMITTED, EVENT_JOB_ERROR, EVENT_JOB_MISSED


def init_app(app):
    SchedulerService.scheduler.init_app(app)
    SchedulerService.scheduler.add_listener(SchedulerService.job_added_listener, EVENT_JOB_ADDED)
    SchedulerService.scheduler.add_listener(SchedulerService.job_executed_listener, EVENT_JOB_EXECUTED)
    SchedulerService.scheduler.add_listener(SchedulerService.job_submitted_listener, EVENT_JOB_SUBMITTED)
    SchedulerService.scheduler.add_listener(SchedulerService.job_error_listener, EVENT_JOB_ERROR)
    SchedulerService.scheduler.add_listener(SchedulerService.job_missed_listener, EVENT_JOB_MISSED)
    SchedulerService.scheduler.start()
