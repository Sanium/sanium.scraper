from flask import Blueprint, make_response, jsonify
from app.services.SchedulerService import scheduler, create_task, test_job
from datetime import datetime, timedelta
from app.models.Job import Job

bp = Blueprint('index', __name__)


@bp.route('/')
def index():
    return "Hello world"


@bp.route('/jobs')
def print_jobs():
    jobs = scheduler.get_jobs()
    return make_response(f"{len(jobs)} jobs", 200)


@bp.route('/add')
def add_job():
    t = create_task(name='test_job', func=test_job, seconds=15)
    return make_response(f"Job {t.id} added. Execution scheduled time: {t.run_date}", 200)


@bp.route('/pause')
def pause():
    scheduler.pause()
    return make_response("Paused", 200)


@bp.route('/resume')
def resume():
    scheduler.resume()
    return make_response("Resumed", 200)


@bp.route('/job/<idx>')
def job(idx):
    t = Job.find(idx)
    if t is None:
        return make_response("Not Found", 404)
    return jsonify({
        'id': t.id,
        'name': t.name,
        'status': t.status,
        'run_date': t.run_date,
        'created': t.created,
    })

