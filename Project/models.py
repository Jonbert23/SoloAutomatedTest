from flask_login import UserMixin
from . import db
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    role = db.Column(db.String(1000))

class TestCodes(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    test_code = db.Column(db.String(100), unique=True)
    client_name = db.Column(db.String(100))
    client_link = db.Column(db.String(100))
    client_username = db.Column(db.String(1000))
    client_password = db.Column(db.String(100))
    test_date_from = db.Column(db.String(100))
    test_date_to = db.Column(db.String(100))
    test_date = db.Column(db.String(100))
    test_month = db.Column(db.String(100))
    user_id = db.Column(db.Integer)
    test_modules = db.Column(db.String (100))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False)

class CalendarFilterUse(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    test_code = db.Column(db.String(100))
    filter_name = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False)

class CalendarFilterTesting(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    test_code = db.Column(db.String(100))
    filter_id = db.Column(db.Integer)
    search_provider = db.Column(db.String(100))
    patient_name = db.Column(db.String(100))
    procedure_code = db.Column(db.String(100))
    unsearch_provider = db.Column(db.String(100))
    status = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False)

class CalendarMetricTesting(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    test_code = db.Column(db.String(100))
    bd_sched_amount = db.Column(db.String(100))
    sd_sched_amount = db.Column(db.String(100))
    bd_goal = db.Column(db.String(100))
    sd_goal = db.Column(db.String(100))
    bd_production = db.Column(db.String(100))
    sd_production = db.Column(db.String(100))
    bd_appt = db.Column(db.String(100))
    sd_appt = db.Column(db.String(100))
    bd_npts = db.Column(db.String(100))
    sd_npts = db.Column(db.String(100))
    status_sched_amount = db.Column(db.String(100))
    status_npts = db.Column(db.String(100))
    status_goal = db.Column(db.String(100))
    status_production = db.Column(db.String(100))
    status_appt = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False)

class CalendarApptPerDayTest(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    test_code = db.Column(db.String(100))
    pts_name = db.Column(db.String(100))
    pts_appt_date = db.Column(db.String(100))
    appt_amount = db.Column(db.String(100))
    appt_procedure = db.Column(db.String(100))
    appt_date_search = db.Column(db.String(100))
    status = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False)


    