from datetime import datetime as dt
from . import db


class Job(db.Model):
    __tablename__ = 'jobs_status'
    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.VARCHAR, nullable=True)
    status = db.Column(db.INTEGER, nullable=False)
    run_date = db.Column(db.TIMESTAMP, nullable=False)
    created = db.Column(db.TIMESTAMP, nullable=False)

    SCHEDULED = 'scheduled'
    RUNNING = 'running'
    DONE = 'done'

    def __repr__(self):
        return f"<Job(id={self.id}, name={self.name}, status={self.status}, " \
               f"run_date={self.run_date}, created={self.created})>"

    def __str__(self):
        return f"Job: {self.id}, {self.name}, {self.status}, " \
               f"{self.run_date}, {self.created}"

    def dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'status': self.status,
            'run_date': self.run_date,
            'created': self.created,
        }

    def set_status(self, status):
        self.status = status
        db.session.commit()

    @staticmethod
    def create(name, run_date):
        task = Job(name=name, status=Job.SCHEDULED, run_date=run_date, created=dt.now())
        db.session.add(task)
        db.session.commit()
        return task

    @staticmethod
    def find(idx):
        return db.session.query(Job).filter(Job.id == idx).first()

    @staticmethod
    def all():
        return db.session.query(Job).all()
