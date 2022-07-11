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

class EodBreakdownTest(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    test_code = db.Column(db.String(100))
    collection_main = db.Column(db.String(100))
    collection_bd = db.Column(db.String(100))
    adjustments_main = db.Column(db.String(100))
    adjustments_bd = db.Column(db.String(100))
    case_accpt_main = db.Column(db.String(100))
    case_accpt_bd = db.Column(db.String(100))
    miss_ref_main = db.Column(db.String(100))
    miss_ref_bd = db.Column(db.String(100))
    no_show_main = db.Column(db.String(100))
    no_show_bd = db.Column(db.String(100))
    daily_coll_main = db.Column(db.String(100))
    daily_coll_bd = db.Column(db.String(100))
    hyg_reapp_main = db.Column(db.String(100))
    hyg_reapp_bd = db.Column(db.String(100))
    new_patient_main = db.Column(db.String(100))
    new_patient_bd = db.Column(db.String(100))
    sd_treat_main = db.Column(db.String(100))
    sd_treat_bd = db.Column(db.String(100))
    pt_portion_main = db.Column(db.String(100))
    pt_portion_bd = db.Column(db.String(100))



    