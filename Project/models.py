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

class CalendarApptValidation(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    test_code = db.Column(db.String(100))
    test_date_from = db.Column(db.String(100))
    test_date_to = db.Column(db.String(100))
    pts_name = db.Column(db.String(100))
    pts_procedure = db.Column(db.String(100))
    pts_providers = db.Column(db.String(100))
    pts_appt_status = db.Column(db.String(100))
    pts_amount = db.Column(db.String(100))
    pts_date = db.Column(db.String(100))
    pts_status = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False)
    
class EodTestResults(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    test_code = db.Column(db.String(100))
    collection_main = db.Column(db.String(100))
    collection_bd = db.Column(db.String(100))
    collection_email = db.Column(db.String(100))
    adjustments_main = db.Column(db.String(100))
    adjustments_bd = db.Column(db.String(100))
    adjustments_email = db.Column(db.String(100))
    case_accpt_main = db.Column(db.String(100))
    case_accpt_bd = db.Column(db.String(100))
    case_accpt_email = db.Column(db.String(100))
    miss_ref_main = db.Column(db.String(100))
    miss_ref_bd = db.Column(db.String(100))
    miss_ref_email = db.Column(db.String(100))
    no_show_main = db.Column(db.String(100))
    no_show_bd = db.Column(db.String(100))
    no_show_email = db.Column(db.String(100))
    daily_coll_main = db.Column(db.String(100))
    daily_coll_bd = db.Column(db.String(100))
    daily_coll_email = db.Column(db.String(100))
    hyg_reapp_main = db.Column(db.String(100))
    hyg_reapp_bd = db.Column(db.String(100))
    hyg_reapp_email = db.Column(db.String(100))
    new_patient_main = db.Column(db.String(100))
    new_patient_bd = db.Column(db.String(100))
    new_patient_email = db.Column(db.String(100))
    sd_treat_main = db.Column(db.String(100))
    sd_treat_bd = db.Column(db.String(100))
    sd_treat_email = db.Column(db.String(100))
    pt_portion_main = db.Column(db.String(100))
    pt_portion_bd = db.Column(db.String(100))
    pt_portion_email = db.Column(db.String(100))
    booked_prod_main = db.Column(db.String(100))
    booked_prod_email = db.Column(db.String(100))
    daily_net_main = db.Column(db.String(100))
    daily_net_email = db.Column(db.String(100))
    daily_gross_main = db.Column(db.String(100))
    daily_gross_email = db.Column(db.String(100))
    sched_vs_goal_main = db.Column(db.String(100))
    sched_vs_goal_email = db.Column(db.String(100))
    general_main = db.Column(db.String(100))
    general_email = db.Column(db.String(100))
    ortho_prod_main = db.Column(db.String(100))
    ortho_prod_email = db.Column(db.String(100))
    perio_prod_main = db.Column(db.String(100))
    perio_prod_email = db.Column(db.String(100))
    oral_surgery_main = db.Column(db.String(100))
    oral_surgery_email = db.Column(db.String(100))
    num_prod_main = db.Column(db.String(100))
    num_prod_email = db.Column(db.String(100))
    adp_main = db.Column(db.String(100))
    adp_email = db.Column(db.String(100))
    specialty_main = db.Column(db.String(100))
    specialty_email = db.Column(db.String(100))
    total_pts_main = db.Column(db.String(100))
    total_pts_email = db.Column(db.String(100))
    total_office_main = db.Column(db.String(100))
    total_office_email = db.Column(db.String(100))
    appts_changed_main = db.Column(db.String(100))
    appts_changed_email = db.Column(db.String(100))
    appts_cancel_main = db.Column(db.String(100))
    appts_cancel_email = db.Column(db.String(100))
    hyg_reserve_main = db.Column(db.String(100))
    hyg_reserve_email = db.Column(db.String(100))
    hyg_cap_main = db.Column(db.String(100))
    hyg_cap_email = db.Column(db.String(100))
    react_calls_main = db.Column(db.String(100))
    react_calls_email = db.Column(db.String(100))
    res_apps_main = db.Column(db.String(100))
    res_apps_email = db.Column(db.String(100))
    endo_main = db.Column(db.String(100))
    endo_email = db.Column(db.String(100))
    clear_aligners_main = db.Column(db.String(100))
    clear_aligners_email = db.Column(db.String(100))
    guest_appt_main = db.Column(db.String(100))
    guest_appt_email = db.Column(db.String(100))
    unsched_treat_main = db.Column(db.String(100))
    unsched_treat_email = db.Column(db.String(100))
    recalls_main = db.Column(db.String(100))
    recalls_email = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False)

class FiguresMatching(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    test_code = db.Column(db.String(100), nullable=True)
    client_url = db.Column(db.String(100), nullable=True)
    test_type = db.Column(db.String(100), nullable=True)
    query_param = db.Column(db.String(100), nullable=True)
    test_date = db.Column(db.String(100), nullable=True)
    dash_netProd = db.Column(db.String(100), nullable=True, default='N/A')
    dash_grossProd = db.Column(db.String(100), nullable=True, default='N/A')
    dash_collection = db.Column(db.String(100), nullable=True, default='N/A')
    dash_adjusment = db.Column(db.String(100), nullable=True, default='N/A')
    dash_npt = db.Column(db.String(100), nullable=True, default='N/A')
    dash_pts = db.Column(db.String(100), nullable=True, default='N/A')
    cal_netProd = db.Column(db.String(100), nullable=True, default='N/A')
    cal_grossProd = db.Column(db.String(100), nullable=True, default='N/A')
    cal_npt = db.Column(db.String(100), nullable=True, default='N/A')
    eod_netProd = db.Column(db.String(100), nullable=True, default='N/A')
    eod_grossProd = db.Column(db.String(100), nullable=True, default='N/A')
    eod_collection = db.Column(db.String(100), nullable=True, default='N/A')
    eod_adjusment = db.Column(db.String(100), nullable=True, default='N/A')
    eod_npt = db.Column(db.String(100), nullable=True, default='N/A')
    eod_pts = db.Column(db.String(100), nullable=True, default='N/A')
    mh_netProd = db.Column(db.String(100), nullable=True, default='N/A')
    mh_grossProd = db.Column(db.String(100), nullable=True, default='N/A')
    mh_collection = db.Column(db.String(100), nullable=True, default='N/A')
    mh_npt = db.Column(db.String(100), nullable=True, default='N/A')
    mh_pts = db.Column(db.String(100), nullable=True, default='N/A')
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)


class TxMinerDefaultTest(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    test_code = db.Column(db.String(100))
    month = db.Column(db.String(100))
    mv_pending_sched = db.Column(db.String(100))
    mv_pending_unsched = db.Column(db.String(100))
    mv_active_production = db.Column(db.String(100))
    breakdown_pending_sched = db.Column(db.String(100))
    breakdown_pending_unsched = db.Column(db.String(100))
    breakdown_active_production = db.Column(db.String(100))
    pending_sched_status = db.Column(db.String(100))
    pending_unsched_status = db.Column(db.String(100))
    pending_active_production = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False)



    
    
