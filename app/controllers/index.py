from flask import Blueprint, jsonify, request
from app.services.SchedulerService import scheduler, create_job
from app.services.ScraperService import main_page_job
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


@bp.route('/add', methods=['GET'])
def add_job():
    t = create_job(name='main_page_job', func=main_page_job, args=['https://justjoin.it/', 10], seconds=15)
    s = f"Job {t.id} added. Execution scheduled time: {t.run_date}",
    return jsonify(data=s)


@bp.route('/add', methods=['POST'])
def add_custom_job():
    if request.content_type.lower() != 'application/json':
        return jsonify(error='Wrong Content-Type'), 415
    data = request.get_json()
    t = create_job(name='main_page_job', func=main_page_job, args=[data["service_name"], 10, data], seconds=15)
    s = f"Job {t.id} added. Execution scheduled time: {t.run_date}",
    return jsonify(data=s)


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
