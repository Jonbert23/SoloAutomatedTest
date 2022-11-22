#Importing Flask Dependecies
from flask import Blueprint, render_template, url_for, request, redirect,flash
from flask_login import login_required, current_user
import time
import datetime
import uuid
#Importing Selenium Dependecies
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

#Importing  File Classes 
from Project.Controller.Global_Controller.Login import GlobalLogin
from Project.Controller.PP_Controller.Filters.Age import AgeFilter
from Project.Controller.PP_Controller.Filters.Balance import BalanceFilter
from Project.Controller.PP_Controller.Filters.PrimariInsuranceRemaining import PIRFilter
from Project.Controller.PP_Controller.Filters.SecondaryInsuranceRemaining import SIRFilter
from Project.Controller.PP_Controller.Filters.RemainingBenefits import RemainingBenefitsFilter
from Project.Controller.PP_Controller.Filters.Gender import GenderFilter
from Project.Controller.PP_Controller.Filters.Status import StatusFilter
from Project.Controller.PP_Controller.Filters.Schedule import ScheduleFilter
from Project.Controller.PP_Controller.Filters.Uninsured import UninsuredFilter
from Project.Controller.PP_Controller.Filters.SingleDatePicker import SinglePicker
from Project.Controller.PP_Controller.Filters.FirstSeen import FirstSeenFilter
from Project.Controller.PP_Controller.Filters.LastSeen import LastSeenFilter
from Project.Controller.PP_Controller.Filters.FutureVisit import FutureVisitFilter
from Project.Controller.PP_Controller.Filters.FutureHygVisit import FutureHygVisitFilter
from Project.Controller.PP_Controller.Filters.LastHygVisit import LastHygVisitFilter
from Project.Controller.PP_Controller.Filters.PerioCareFilter import PerioCareFilter
from Project.Controller.PP_Controller.Filters.Visit import VisitFilter

from Project.models import PpTestcodeLogs
from Project.models import PpAgeFilter
from Project.models import PpPIRFilter
from Project.models import PpBalanceFilter
from Project.models import PpSIRFilter
from Project.models import PpRemainingBenefits
from Project.models import PpGenderFilter
from Project.models import PpStatusFilter
from Project.models import PpScheduleFilter
from Project.models import PpUninsuredFilter
from Project.models import PpFirstseenFilter 
from Project.models import PpLastSeenFilter
from Project.models import PpFutureHygVisitFilter
from Project.models import PpFutureVisitFilter
from Project.models import PpLastHygVisitFilter
from Project.models import PpPerioCareFilter
from Project.models import PpVisitFilter


from Project import db


pp = Blueprint('pp', __name__)

@pp.route("/patient-portal", methods=['POST','GET'])
def patient_portal():
   
    test_code = 'no_test'
    if request.method == 'POST':
        filters = request.form.getlist('Filter[]')
        client_url = request.form['client_url']
        client_username = request.form['client_username']
        client_password = request.form['client_password']
        test_code = uuid.uuid4().hex
    
        #Declaring Selenium driver--------------------------------------------------------------------
        
        options = Options()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
        
        #Calling Login Global Test -----------------------------------------------------------------
        GlobalLogin.Login(driver, client_url, client_username, client_password)
        
        #Saving Test Logs
    
        save_test_logs = PpTestcodeLogs(
            user_id = current_user.id,
            test_code = test_code,
            client_url = client_url,
        )
        db.session.add(save_test_logs)
        db.session.commit()
        
        driver.get(client_url+'/patient-portal')
        
        for pp_filter in filters:
            if pp_filter == 'age':
                greater = request.form['age_greater']
                less = request.form['age_less']
                equal = request.form['age_equal']
                between_first = request.form['age_between_first']
                between_second = request.form['age_between_second']

                AgeFilter.Age_filter(driver, greater, less, equal, between_first, between_second, test_code)
                
            if pp_filter == 'balance':
                greater = request.form['balance_greater']
                less = request.form['balance_less']
                equal = request.form['balance_equal']
                between_first = request.form['balance_between_first']
                between_second = request.form['balance_between_second']

                BalanceFilter.Balance_filter(driver, greater, less, equal, between_first, between_second, test_code)
                
            if pp_filter == 'primary_insurance_remaining':
                greater = request.form['pir_greater']
                less = request.form['pir_less']
                equal = request.form['pir_equal']
                between_first = request.form['pir_between_first']
                between_second = request.form['pir_between_second']

                PIRFilter.PIR_filter(driver, greater, less, equal, between_first, between_second, test_code)
                
            if pp_filter == 'secondary_insurance_remaining':
                greater = request.form['sir_greater']
                less = request.form['sir_less']
                equal = request.form['sir_equal']
                between_first = request.form['sir_between_first']
                between_second = request.form['sir_between_second']

                SIRFilter.SIR_filter(driver, greater, less, equal, between_first, between_second, test_code)
                
            if pp_filter == 'remaining_benefits':
                greater = request.form['rb_greater']
                less = request.form['rb_less']
                equal = request.form['rb_equal']
                between_first = request.form['rb_between_first']
                between_second = request.form['rb_between_second']

                RemainingBenefitsFilter.RB_filter(driver, greater, less, equal, between_first, between_second, test_code)

            if pp_filter == 'gender':
                GenderFilter.Gender_filter(driver, test_code)
                
            if pp_filter == 'status':
                StatusFilter.Status_filter(driver, test_code)
                
            if pp_filter == 'scheduled':
                ScheduleFilter.Schedule_filter(driver, test_code)
                
            if pp_filter == 'uninsured':
                UninsuredFilter.Uninsured_filter(driver, test_code)
                
            if pp_filter == 'firts_seen':
                after = request.form['fs_after']
                before = request.form['fs_before']
                on = request.form['fs_on']
                between_first = request.form['fs_between_first']
                between_second = request.form['fs_between_second']
               
                FirstSeenFilter.FirstSeen_filter(driver, test_code, after, before, on, between_first, between_second)
                
            if pp_filter == 'last_seen':
                after = request.form['ls_after']
                before = request.form['ls_before']
                on = request.form['ls_on']
                between_first = request.form['ls_between_first']
                between_second = request.form['ls_between_second']
               
                LastSeenFilter.LastSeen_filter(driver, test_code, after, before, on, between_first, between_second)
                
            if pp_filter == 'future_visit':
                after = request.form['fv_after']
                before = request.form['fv_before']
                on = request.form['fv_on']
                between_first = request.form['fv_between_first']
                between_second = request.form['fv_between_second']
               
                FutureVisitFilter.FutureVisit_filter(driver, test_code, after, before, on, between_first, between_second)
                
            if pp_filter == 'future_hyg_visit':
                after = request.form['fhv_after']
                before = request.form['fhv_before']
                on = request.form['fhv_on']
                between_first = request.form['fhv_between_first']
                between_second = request.form['fhv_between_second']
               
                FutureHygVisitFilter.FutureHygVisit_filter(driver, test_code, after, before, on, between_first, between_second)
            
            if pp_filter == 'last_hyg_visit':
                after = request.form['lhv_after']
                before = request.form['lhv_before']
                on = request.form['lhv_on']
                between_first = request.form['lhv_between_first']
                between_second = request.form['lhv_between_second']
                
                LastHygVisitFilter.LastHygVisit_filter(driver, test_code, after, before, on, between_first, between_second)
            
            if pp_filter == 'perio_care':
                PerioCareFilter.PerioCare_filter(driver, test_code)
                
            
            if pp_filter == 'visit':
                greater = request.form['visit_greater']
                less = request.form['visit_less']
                equal = request.form['visit_equal']
                between_first = request.form['visit_between_first']
                between_second = request.form['visit_between_second']
                
                VisitFilter.Visit_filter(driver, greater, less, equal, between_first, between_second, test_code)
                
            
        driver.quit()
        
        flash('Your Test Code: '+test_code, 'info')
        
    latest_test = PpTestcodeLogs.query.order_by(PpTestcodeLogs.id.desc()).first()
    #print(latest_test.test_code)
    
    all_test = PpTestcodeLogs.query.all()
    
    for test in all_test:
        print(test.test_code)
    
    all_test = ''
    if latest_test:
        latest_test = latest_test.test_code
        all_test = PpTestcodeLogs.query.order_by(PpTestcodeLogs.id.desc()).first()
    else:
        latest_test = "No Data"
    
    age_filter_exist = 'No'
    age_filter = PpAgeFilter.query.filter_by(test_code=latest_test).first()
    
    pir_filter_exist = 'No'
    pir_filter = PpPIRFilter.query.filter_by(test_code=latest_test).first()
    
    balance_filter_exist = 'No'
    balance_filter = PpBalanceFilter.query.filter_by(test_code=latest_test).first()
    
    sir_filter_exist = 'No'
    sir_filter = PpSIRFilter.query.filter_by(test_code=latest_test).first()
    
    rb_filter_exist = 'No'
    rb_filter = PpRemainingBenefits.query.filter_by(test_code=latest_test).first()
    
    gender_filter_exist = 'No'
    gender_filter = PpGenderFilter.query.filter_by(test_code=latest_test).first()
    
    status_filter_exist = 'No'
    status_filter = PpStatusFilter.query.filter_by(test_code=latest_test).first()
    
    sched_filter_exist = 'No'
    sched_filter = PpScheduleFilter.query.filter_by(test_code=latest_test).first()
    
    uninsured_filter_exist = 'No'
    uninsured_filter = PpUninsuredFilter.query.filter_by(test_code=latest_test).first()
    
    firstseen_filter_exist = 'No'
    firstseen_filter = PpFirstseenFilter.query.filter_by(test_code=latest_test).first()
    
    lastseen_filter_exist = 'No'
    lastseen_filter = PpLastSeenFilter.query.filter_by(test_code=latest_test).first()
    
    fhv_filter_exist = 'No'
    fhv_filter = PpFutureHygVisitFilter.query.filter_by(test_code=latest_test).first()
    
    fv_filter_exist = 'No'
    fv_filter = PpFutureVisitFilter.query.filter_by(test_code=latest_test).first()
    
    lhv_filter_exist = 'No'
    lhv_filter = PpLastHygVisitFilter.query.filter_by(test_code=latest_test).first()
    
    perio_care_exist = 'No'
    perio_care_filter = PpPerioCareFilter.query.filter_by(test_code=latest_test).first()
    
    visit_filter_exist = 'No'
    visit_filter = PpVisitFilter.query.filter_by(test_code=latest_test).first()
    
    if age_filter:
        age_filter_exist = 'Yes'
        age_filter = PpAgeFilter.query.all()
        
    if pir_filter:
        pir_filter_exist = 'Yes'
        pir_filter = PpPIRFilter.query.all()
        
    if balance_filter:
        balance_filter_exist = 'Yes'
        balance_filter = PpBalanceFilter.query.all()
        
    if sir_filter:
        sir_filter_exist = 'Yes'
        sir_filter = PpSIRFilter.query.all()
    
    if rb_filter:
        rb_filter_exist = 'Yes'
        rb_filter = PpRemainingBenefits.query.all()
        
    if gender_filter:
        gender_filter_exist = 'Yes'
        gender_filter = PpGenderFilter.query.all()
                
    if status_filter:
        status_filter_exist = 'Yes'
        status_filter = PpStatusFilter.query.all()
    
    if sched_filter:
        sched_filter_exist = 'Yes'
        sched_filter = PpScheduleFilter.query.all()
        
    if uninsured_filter:
        uninsured_filter_exist = 'Yes'
        uninsured_filter = PpUninsuredFilter.query.all()
   
    if firstseen_filter:
        firstseen_filter_exist = 'Yes'   
        firstseen_filter = PpFirstseenFilter.query.all()
        
    if lastseen_filter:
        lastseen_filter_exist = 'Yes'
        lastseen_filter =  PpLastSeenFilter.query.all()
        
    if fhv_filter:
        fhv_filter_exist = 'Yes'
        fhv_filter = PpFutureHygVisitFilter.query.all()
        
    if fv_filter:
        fv_filter_exist = 'Yes'
        fv_filter = PpFutureVisitFilter.query.all()
        
    if lhv_filter:
        lhv_filter_exist = 'Yes'
        lhv_filter = PpLastHygVisitFilter.query.all()
        
    if perio_care_filter:
        perio_care_exist = 'Yes'
        perio_care_filter = PpPerioCareFilter.query.all()
        
    if visit_filter:
        visit_filter_exist = 'Yes'
        visit_filter = PpVisitFilter.query.all() 
        
         
    return render_template('PP_Template/PP_index.html', 
        all_test = all_test,
        latest_test = latest_test,
        age_filter_exist = age_filter_exist, age_filter = age_filter, 
        pir_filter_exist = pir_filter_exist, pir_filter = pir_filter,
        balance_filter_exist = balance_filter_exist, balance_filter = balance_filter,
        sir_filter_exist = sir_filter_exist, sir_filter = sir_filter,
        rb_filter_exist = rb_filter_exist, rb_filter = rb_filter,
        gender_filter_exist = gender_filter_exist, gender_filter = gender_filter,
        status_filter_exist = status_filter_exist, status_filter = status_filter,
        sched_filter_exist = sched_filter_exist, sched_filter = sched_filter,
        uninsured_filter_exist = uninsured_filter_exist, uninsured_filter = uninsured_filter,
        firstseen_filter_exist = firstseen_filter_exist, firstseen_filter = firstseen_filter,
        lastseen_filter_exist = lastseen_filter_exist, lastseen_filter = lastseen_filter, 
        fhv_filter_exist = fhv_filter_exist, fhv_filter = fhv_filter,
        fv_filter_exist = fv_filter_exist, fv_filter = fv_filter,
        lhv_filter_exist = lhv_filter_exist, lhv_filter = lhv_filter,
        perio_care_exist = perio_care_exist, perio_care_filter = perio_care_filter,
        visit_filter_exist = visit_filter_exist, visit_filter = visit_filter,
    )




@pp.route("/patient-portal/search", methods=['POST','GET'])
def patient_portal_search():
   
    test_code = 'no_test'
    if request.method == 'POST':
        test_code = request.form['test_code']
        
    all_test = PpTestcodeLogs.query.all()
    #print(latest_test.test_code)
    
    if all_test:
        latest_test = PpTestcodeLogs.query.filter_by(test_code=test_code).first()
        latest_test = latest_test.test_code
        all_test =  PpTestcodeLogs.query.filter_by(test_code=test_code).first()
        
        if not latest_test:
            flash('Search test code not exist', 'info')
            return redirect('/patient-portal')
    else:
        flash('No data to search', 'info')
        return redirect('/patient-portal')
    
    age_filter_exist = 'No'
    age_filter = PpAgeFilter.query.filter_by(test_code=latest_test).first()
    
    pir_filter_exist = 'No'
    pir_filter = PpPIRFilter.query.filter_by(test_code=latest_test).first()
    
    balance_filter_exist = 'No'
    balance_filter = PpBalanceFilter.query.filter_by(test_code=latest_test).first()
    
    sir_filter_exist = 'No'
    sir_filter = PpSIRFilter.query.filter_by(test_code=latest_test).first()
    
    rb_filter_exist = 'No'
    rb_filter = PpRemainingBenefits.query.filter_by(test_code=latest_test).first()
    
    gender_filter_exist = 'No'
    gender_filter = PpGenderFilter.query.filter_by(test_code=latest_test).first()
    
    status_filter_exist = 'No'
    status_filter = PpStatusFilter.query.filter_by(test_code=latest_test).first()
    
    sched_filter_exist = 'No'
    sched_filter = PpScheduleFilter.query.filter_by(test_code=latest_test).first()
    
    uninsured_filter_exist = 'No'
    uninsured_filter = PpUninsuredFilter.query.filter_by(test_code=latest_test).first()
    
    firstseen_filter_exist = 'No'
    firstseen_filter = PpFirstseenFilter.query.filter_by(test_code=latest_test).first()
    
    lastseen_filter_exist = 'No'
    lastseen_filter = PpLastSeenFilter.query.filter_by(test_code=latest_test).first()
    
    fhv_filter_exist = 'No'
    fhv_filter = PpFutureHygVisitFilter.query.filter_by(test_code=latest_test).first()
    
    fv_filter_exist = 'No'
    fv_filter = PpFutureVisitFilter.query.filter_by(test_code=latest_test).first()
    
    lhv_filter_exist = 'No'
    lhv_filter = PpLastHygVisitFilter.query.filter_by(test_code=latest_test).first()
    
    perio_care_exist = 'No'
    perio_care_filter = PpPerioCareFilter.query.filter_by(test_code=latest_test).first()
    
    visit_filter_exist = 'No'
    visit_filter = PpVisitFilter.query.filter_by(test_code=latest_test).first()
    
    if age_filter:
        age_filter_exist = 'Yes'
        age_filter = PpAgeFilter.query.all()
        
    if pir_filter:
        pir_filter_exist = 'Yes'
        pir_filter = PpPIRFilter.query.all()
        
    if balance_filter:
        balance_filter_exist = 'Yes'
        balance_filter = PpBalanceFilter.query.all()
        
    if sir_filter:
        sir_filter_exist = 'Yes'
        sir_filter = PpSIRFilter.query.all()
    
    if rb_filter:
        rb_filter_exist = 'Yes'
        rb_filter = PpRemainingBenefits.query.all()
        
    if gender_filter:
        gender_filter_exist = 'Yes'
        gender_filter = PpGenderFilter.query.all()
                
    if status_filter:
        status_filter_exist = 'Yes'
        status_filter = PpStatusFilter.query.all()
    
    if sched_filter:
        sched_filter_exist = 'Yes'
        sched_filter = PpScheduleFilter.query.all()
        
    if uninsured_filter:
        uninsured_filter_exist = 'Yes'
        uninsured_filter = PpUninsuredFilter.query.all()
   
    if firstseen_filter:
        firstseen_filter_exist = 'Yes'   
        firstseen_filter = PpFirstseenFilter.query.all()
        
    if lastseen_filter:
        lastseen_filter_exist = 'Yes'
        lastseen_filter =  PpLastSeenFilter.query.all()
        
    if fhv_filter:
        fhv_filter_exist = 'Yes'
        fhv_filter = PpFutureHygVisitFilter.query.all()
        
    if fv_filter:
        fv_filter_exist = 'Yes'
        fv_filter = PpFutureVisitFilter.query.all()
        
    if lhv_filter:
        lhv_filter_exist = 'Yes'
        lhv_filter = PpLastHygVisitFilter.query.all()
        
    if perio_care_filter:
        perio_care_exist = 'Yes'
        perio_care_filter = PpPerioCareFilter.query.all()
        
    if visit_filter:
        visit_filter_exist = 'Yes'
        visit_filter = PpVisitFilter.query.all() 
        
         
    return render_template('PP_Template/PP_index.html', 
        all_test = all_test,
        latest_test = latest_test,
        age_filter_exist = age_filter_exist, age_filter = age_filter, 
        pir_filter_exist = pir_filter_exist, pir_filter = pir_filter,
        balance_filter_exist = balance_filter_exist, balance_filter = balance_filter,
        sir_filter_exist = sir_filter_exist, sir_filter = sir_filter,
        rb_filter_exist = rb_filter_exist, rb_filter = rb_filter,
        gender_filter_exist = gender_filter_exist, gender_filter = gender_filter,
        status_filter_exist = status_filter_exist, status_filter = status_filter,
        sched_filter_exist = sched_filter_exist, sched_filter = sched_filter,
        uninsured_filter_exist = uninsured_filter_exist, uninsured_filter = uninsured_filter,
        firstseen_filter_exist = firstseen_filter_exist, firstseen_filter = firstseen_filter,
        lastseen_filter_exist = lastseen_filter_exist, lastseen_filter = lastseen_filter, 
        fhv_filter_exist = fhv_filter_exist, fhv_filter = fhv_filter,
        fv_filter_exist = fv_filter_exist, fv_filter = fv_filter,
        lhv_filter_exist = lhv_filter_exist, lhv_filter = lhv_filter,
        perio_care_exist = perio_care_exist, perio_care_filter = perio_care_filter,
        visit_filter_exist = visit_filter_exist, visit_filter = visit_filter,
    )
    
    
@pp.route("/patient-portal/all_test", methods=['POST','GET'])
def patient_portal_alltest():
    all_test = PpTestcodeLogs.query.all()
    return render_template('PP_Template/Modals/all_test_modal.html', all_test=all_test)
