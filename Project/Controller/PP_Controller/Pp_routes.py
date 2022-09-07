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

from Project.models import PpTestcodeLogs
from Project.models import PpAgeFilter
from Project.models import PpPIRFilter
from Project.models import PpBalanceFilter
from Project.models import PpSIRFilter
from Project.models import PpRemainingBenefits
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
        
        print('naako diri')
        #Saving Test Logs
        save_test_logs = PpTestcodeLogs(
            user_id = current_user.id,
            test_code = test_code 
        )
        db.session.add(save_test_logs)
        db.session.commit()
        
        driver.get(client_url+'/patient-portal')
        
        for pp_filter in filters:
            if pp_filter == 'age':
                greater = request.form['greater']
                less = request.form['less']
                equal = request.form['equal']
                between_first = request.form['between_first']
                between_second = request.form['between_second']

                AgeFilter.Age_filter(driver, greater, less, equal, between_first, between_second, test_code)
                
            if pp_filter == 'balance':
                greater = request.form['greater']
                less = request.form['less']
                equal = request.form['equal']
                between_first = request.form['between_first']
                between_second = request.form['between_second']

                BalanceFilter.Balance_filter(driver, greater, less, equal, between_first, between_second, test_code)
                
            if pp_filter == 'primary_insurance_remaining':
                greater = request.form['greater']
                less = request.form['less']
                equal = request.form['equal']
                between_first = request.form['between_first']
                between_second = request.form['between_second']

                PIRFilter.PIR_filter(driver, greater, less, equal, between_first, between_second, test_code)
                
            if pp_filter == 'secondary_insurance_remaining':
                greater = request.form['greater']
                less = request.form['less']
                equal = request.form['equal']
                between_first = request.form['between_first']
                between_second = request.form['between_second']

                SIRFilter.SIR_filter(driver, greater, less, equal, between_first, between_second, test_code)
                
            if pp_filter == 'remaining_benefits':
                greater = request.form['greater']
                less = request.form['less']
                equal = request.form['equal']
                between_first = request.form['between_first']
                between_second = request.form['between_second']

                RemainingBenefitsFilter.RB_filter(driver, greater, less, equal, between_first, between_second, test_code)
    
        flash('Your Test Code: '+test_code, 'info')
        
    latest_test = PpTestcodeLogs.query.order_by(PpTestcodeLogs.id.desc()).first()
    print(latest_test.test_code)
    
    age_filter_exist = 'No'
    age_filter = PpAgeFilter.query.filter_by(test_code=latest_test.test_code).first()
    
    pir_filter_exist = 'No'
    pir_filter = PpPIRFilter.query.filter_by(test_code=latest_test.test_code).first()
    
    balance_filter_exist = 'No'
    balance_filter = PpBalanceFilter.query.filter_by(test_code=latest_test.test_code).first()
    
    sir_filter_exist = 'No'
    sir_filter = PpSIRFilter.query.filter_by(test_code=latest_test.test_code).first()
    
    rb_filter_exist = 'No'
    rb_filter = PpRemainingBenefits.query.filter_by(test_code=latest_test.test_code).first()
    
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
        
        
    return render_template('PP_Template/PP_index.html', 
        latest_test = latest_test,
        age_filter_exist = age_filter_exist, age_filter = age_filter, 
        pir_filter_exist = pir_filter_exist, pir_filter = pir_filter,
        balance_filter_exist = balance_filter_exist, balance_filter = balance_filter,
        sir_filter_exist = sir_filter_exist, sir_filter = sir_filter,
        rb_filter_exist = rb_filter_exist, rb_filter = rb_filter,
    )
