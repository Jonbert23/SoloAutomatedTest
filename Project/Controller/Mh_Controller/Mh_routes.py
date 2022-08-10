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

from Project.Controller.Global_Controller.Global_test import Login
from Project.Controller.Mh_Controller.Mh_xpath import MHXpath
from Project.Controller.Mh_Controller.Mh_braakdown import MornigHuddleBreakdown
from Project.Controller.Mh_Controller.Mh_scorecard import MornigHuddleScorecard
from Project.Controller.Mh_Controller.Mh_result import MhResult
from Project.Controller.Mh_Controller.Mh_mail import MornigHuddleMail
from Project.Controller.Global_Controller.Single_date_picker import SinglePicker

from Project.models import TestCodes
from Project import db
from Project.models import MhBreakdown
from Project.models import MhMain
from Project.models import MhScorecard

mh = Blueprint('mh', __name__)

@mh.route("/morning-huddle", methods=['POST','GET'])
def morning_huddle():
    
    #credentials = TestCodes.query.filter_by(test_code='1dbb30da4b964850a6ddcc6d6f1c0088').first()
    test = TestCodes.query.order_by(TestCodes.id.desc()).first()
    
    if request.method == 'POST':
        test_code = request.form['test_code']
        tests = request.form.getlist('Test[]')   
        email_username = request.form['email_username']
        mail_password = request.form['mail_password']
        
        check_testcode_in_mh_main = MhMain.query.filter_by(test_code=test_code).first()
        check_testcode_exist = TestCodes.query.filter_by(test_code=test_code).first()
        
        if not check_testcode_exist:
            flash("The test code does not exist", 'error')
            return redirect('/morning-huddle')
        
        if check_testcode_in_mh_main:
            flash("The test code have already been used in this module", 'info')
            return redirect('/morning-huddle')
        
        test = TestCodes.query.filter_by(test_code=test_code).first()
        
        options = Options()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
        
        Login.login(driver, test.client_link, test.client_username, test.client_password)
        
        driver.get(test.client_link+'/morning-huddle')
        
        SinglePicker.MH_DatePicker(driver, test.test_date)
        update = driver.find_element(By.XPATH, MHXpath.update_btn).click()
        
        #MornigHuddleBreakdown.Main_test(driver, test.test_date, test_code) 
        #MornigHuddleScorecard.Main_test(driver, test_code) 
        
        for test in tests:
            if test == 'mail':
                MornigHuddleMail.main_test(driver, email_username, mail_password, test_code)
                
        
    #Test Queries   
    mh_main = MhMain.query.order_by(MhMain.id.desc()).first()
    mh_brk = MhBreakdown.query.order_by(MhBreakdown.id.desc()).first()
    mh_sc = MhScorecard.query.order_by(MhScorecard.id.desc()).first()
    mh_main_len = MhMain.query.order_by(MhMain.id.desc()).count()
    
    #Test Results
    if mh_main_len != 0:
        brk_ytr_result = MhResult.brk_ytr_result(mh_main, mh_brk)
        brk_tdy_result = MhResult.brk_tdy_result(mh_main, mh_brk)
        brk_tmw_result = MhResult.brk_tmw_result(mh_main, mh_brk)
        sc_result = MhResult.sc_result(mh_main, mh_sc)
    else:
        brk_ytr_result = 0
        brk_tdy_result = 0
        brk_tmw_result = 0
        sc_result = 0
    
    #Graph Data
    if mh_main_len != 0:
        brk_ytr_chart = Graph.brk_chart(brk_ytr_result)
        brk_tdy_chart = Graph.brk_chart(brk_tdy_result)
        brk_tmw_chart = Graph.brk_chart(brk_tmw_result)
        sc_chart = Graph.brk_chart(sc_result)
        sc_goal_prod_graph = Graph.sc_goal_prod_chart(mh_main, mh_sc)
    else:
        brk_ytr_chart = 0
        brk_tdy_chart = 0
        brk_tmw_chart = 0
        sc_chart = 0
        sc_goal_prod_graph =0
    
    if mh_main_len != 0: 
        test = TestCodes.query.filter_by(test_code=mh_main.test_code).first()
    else:
        test = {
            'client_name': 'No Performed Test',
            'client_link': 'No Test',
            'test_date': '--/--/--'
        }

    return render_template('Mh_Template/Mh_index.html',
                           test = test,
                           mh_main = mh_main,
                           mh_brk = mh_brk,
                           mh_sc = mh_sc,
                           brk_ytr_result = brk_ytr_result,
                           brk_tdy_result = brk_tdy_result,
                           brk_tmw_result = brk_tmw_result,
                           sc_result = sc_result,
                           brk_ytr_chart = brk_ytr_chart,
                           brk_tdy_chart = brk_tdy_chart,
                           brk_tmw_chart = brk_tmw_chart,
                           sc_chart = sc_chart,
                           sc_goal_prod_graph = sc_goal_prod_graph)
    
    
class Graph:

    def brk_chart(results):
        fail_test = 0
        pass_test = 0
        
        for key in results:
            if results[key] == 'Pass':
                pass_test = pass_test + 1
            else:
                fail_test = fail_test + 1
        
        total_test = fail_test + pass_test
        total_fail = (fail_test / total_test) * 100
        total_pass = (pass_test / total_test) * 100
        
        total_fail = "{:.2f}".format(total_fail)
        total_pass = "{:.2f}".format(total_pass)
        
        chart_data = {
            'pass': total_pass,
            'fail': total_fail
        }
        
        return chart_data
    
    def sc_goal_prod_chart(mh_main, mh_sc):
        chart = {
            'mh_ytr_prod' : mh_main.ytr_net_prod.replace("$","").replace(",","").replace(" ","").replace("%","").replace("N/A","0"),
            'mh_ytr_goal': mh_main.ytr_goal.replace("$","").replace(",","").replace(" ","").replace("%","").replace("N/A","0"),
            'sc_ytr_prod': mh_sc.ytr_prod.replace("$","").replace(",","").replace(" ","").replace("%","").replace("N/A","0"),
            'sc_ytr_sc': mh_sc.ytr_goal.replace("$","").replace(",","").replace(" ","").replace("%","").replace("N/A","0"),
            
            'mh_tdy_prod': mh_main.tdy_sched_prod.replace("$","").replace(",","").replace(" ","").replace("%","").replace("N/A","0"),
            'mh_tdy_goal': mh_main.tdy_goal.replace("$","").replace(",","").replace(" ","").replace("%","").replace("N/A","0"),
            'sc_tdy_prod': mh_sc.tdy_sched_prod.replace("$","").replace(",","").replace(" ","").replace("%","").replace("N/A","0"),
            'sc_tdy_goal': mh_sc.tdy_goal.replace("$","").replace(",","").replace(" ","").replace("%","").replace("N/A","0"),
            
            'mh_tmw_prod': mh_main.tmw_sched_prod.replace("$","").replace(",","").replace(" ","").replace("%","").replace("N/A","0"),
            'mh_tmw_goal': mh_main.tmw_goal.replace("$","").replace(",","").replace(" ","").replace("%","").replace("N/A","0"),
            'sc_tmw_prod': mh_sc.tmw_sched_prod.replace("$","").replace(",","").replace(" ","").replace("%","").replace("N/A","0"),
            'sc_tmw_goal': mh_sc.tmw_goal.replace("$","").replace(",","").replace(" ","").replace("%","").replace("N/A","0"),
        }
        return chart
            
 
 
