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

from Project.Controller.EodV2_Controller.Eod_xpath import EodXpath
from Project.Controller.Global_Controller.Single_date_picker import SinglePicker
from Project.Controller.Global_Controller.Login import GlobalLogin
from Project.Controller.EodV2_Controller.Eod_breakdown_test import EodBreakdown
from Project.Controller.EodV2_Controller.Eod_result import EodResult

from Project.models import TestCodes
from Project.models import EodMain
from Project.models import EodBrk
from Project import db

eod_v2 = Blueprint('eod_v2', __name__)

@eod_v2.route("/eod-form-v2", methods=["POST", "GET"])
@login_required
def eodForm():
    
    if request.method == 'POST':
        test_code = request.form['test_code']
        check_testcode_exist = TestCodes.query.filter_by(test_code=test_code).first()
        
        if not check_testcode_exist:
            flash("The test code does not exist", 'error')
            return redirect('/eod-form-v2')
        
        test = TestCodes.query.filter_by(test_code=test_code).first()
        
        options = Options()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
        
        GlobalLogin.Login(driver, test.client_link, test.client_username, test.client_password)
        
        driver.get(test.client_link+'/end-of-day')
        
        SinglePicker.EOD_DatePicker(driver, test.test_date)
        # print('Im here')
        update = driver.find_element(By.XPATH, EodXpath.update_btn).click()
        
        EodBreakdown.Main_test(driver, test_code,test.test_date)
        
    eod_main = EodMain.query.order_by(EodMain.id.desc()).first()
    eod_brk = EodBrk.query.order_by(EodBrk.id.desc()).first()
    
    empty_test = 'Yes'
    if eod_main:
        empty_test = 'No'
        latest_test = TestCodes.query.filter_by(test_code=eod_main.test_code).first()
        eod_result = EodResult.Brk_result(eod_main, eod_brk)
        eod_graph = EodResult.eod_graph_result(eod_result)  

        return render_template("EodV2_template/Eod_index.html",
                               eod_main = eod_main,
                               eod_brk = eod_brk,
                               eod_result = eod_result,
                               eod_graph = eod_graph,
                               latest_test = latest_test,
                               empty_test = empty_test)
    else:
        return render_template("EodV2_template/Eod_index.html", 
                               empty_test = empty_test)
        
        
@eod_v2.route("/eod-form-v2/search", methods=["POST", "GET"])
@login_required
def eodForm_search():
    test_code = ''
    if request.method == 'POST':
        test_code = request.form['testcode']
        
    eod_main = EodMain.query.filter_by(test_code=test_code).first()
    eod_brk = EodBrk.query.filter_by(test_code=test_code).first()
    
    empty_test = 'Yes'
    if eod_main:
        empty_test = 'No'
        latest_test = TestCodes.query.filter_by(test_code=eod_main.test_code).first()
        eod_result = EodResult.Brk_result(eod_main, eod_brk)
        eod_graph = EodResult.eod_graph_result(eod_result)  

        return render_template("EodV2_template/Eod_index.html",
                               eod_main = eod_main,
                               eod_brk = eod_brk,
                               eod_result = eod_result,
                               eod_graph = eod_graph,
                               latest_test = latest_test,
                               empty_test = empty_test)
    else:
        flash('Searched test code not exist', 'info')
        return redirect('/eod-form-v2')
    
    
@eod_v2.route("/eod-form-v2/all_test", methods=["POST", "GET"])
@login_required
def all_test_codes():
    eod_data = EodMain.query.all()
    eod_all_test = []
    
    if eod_data:
        for data in eod_data:
            all_test = TestCodes.query.filter_by(test_code=data.test_code).first()
            
            data_dictionary = {
                'url': all_test.client_link,
                'client': all_test.client_name,
                'date': all_test.test_date,
                'test_code': all_test.test_code
            }
            eod_all_test.append(data_dictionary)
    
    data_len = len(eod_all_test)
              
    return render_template('EodV2_template/Modal/Eod_all_test_modal.html', eod_all_test=eod_all_test, data_len=data_len)
    