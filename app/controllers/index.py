from flask import Blueprint, jsonify
from app.services.SchedulerService import scheduler, create_task, test_job
from app.models.Job import Job

bp = Blueprint('index', __name__)


@bp.route('/')
def index():
    return "Hello world"


@bp.route('/jobs')
def print_jobs():
    jobs = Job.all()
    data = {}
    for j in jobs:
        data[j.id] = j.dict()
        pass
    return jsonify(data=data)


@bp.route('/add')
def add_job():
    t = create_task(name='test_job', func=test_job, seconds=15)
    return jsonify(data=f"Job {t.id} added. Execution scheduled time: {t.run_date}")


@bp.route('/pause')
def pause():
    scheduler.pause()
    return jsonify(data="Paused")


@bp.route('/resume')
def resume():
    scheduler.resume()
    return jsonify(data="Resumed")


@bp.route('/jobs/<idx>')
def job(idx):
    j = Job.find(idx)
    if j is None:
        return jsonify(error="Not Found"), 404
    return jsonify(data=j.dict())

