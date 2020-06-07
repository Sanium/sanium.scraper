from datetime import datetime as dt
from . import db


class Offer(db.Model):
    __tablename__ = 'offers'
    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.VARCHAR, nullable=True)
    description = db.Column(db.VARCHAR, nullable=True)
    experience = db.Column(db.VARCHAR, nullable=True)
    employment = db.Column(db.VARCHAR, nullable=True)
    technology = db.Column(db.VARCHAR, nullable=True)
    salary_from = db.Column(db.VARCHAR, nullable=True)
    salary_to = db.Column(db.VARCHAR, nullable=True)
    currency = db.Column(db.VARCHAR, nullable=True)
    city = db.Column(db.VARCHAR, nullable=True)
    street = db.Column(db.VARCHAR, nullable=True)
    remote = db.Column(db.VARCHAR, nullable=True)
    contact = db.Column(db.VARCHAR, nullable=True)
    website = db.Column(db.VARCHAR, nullable=True)
    created_at = db.Column(db.VARCHAR, nullable=True)
    updated_at = db.Column(db.VARCHAR, nullable=True)
    expired_on = db.Column(db.VARCHAR, nullable=True)
    employer = db.Column(db.VARCHAR, nullable=True)
    origin_url = db.Column(db.VARCHAR, nullable=True)

    def __repr__(self):
        return f"<Offer(id={self.id}, name={self.name}, description={self.description}, " \
               f"experience={self.experience}, employment={self.employment}, " \
               f"salary_from={self.salary_from}, salary_to={self.salary_to}, " \
               f"currency={self.currency}, city={self.city}, " \
               f"street={self.street}, remote={self.remote}, " \
               f"contact={self.contact}, website={self.website}, " \
               f"created_at={self.created_at}, updated_at={self.updated_at}, " \
               f"expired_on={self.expired_on}, technology={self.technology}, " \
               f"employer={self.employer}, origin_url={self.origin_url})>"

    @staticmethod
    def create(**kwargs):
        model = Offer(kwargs)
        db.session.add(model)
        db.session.commit()
        return model

    @staticmethod
    def find(idx=None, by=None):
        if idx is None and by is None:
            raise ValueError('One of both argument must be present')
        if by is None:
            return db.session.query(Offer).filter(Offer.id == idx).all()
        return db.session.query(Offer).filter_by(**by).all()

    @staticmethod
    def find_one(idx=None, by=None):
        if idx is None and by is None:
            raise ValueError('One of both argument must be present')
        if by is None:
            return db.session.query(Offer).filter(Offer.id == idx).first()
        return db.session.query(Offer).filter_by(**by).first()

    @staticmethod
    def all():
        return db.session.query(Offer).all()
