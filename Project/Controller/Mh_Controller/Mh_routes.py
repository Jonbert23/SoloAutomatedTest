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
from Project.Controller.Global_Controller.Single_date_picker import SinglePicker

from Project.models import TestCodes
from Project import db

mh = Blueprint('mh', __name__)

@mh.route("/morning-huddle", methods=['POST','GET'])
def morning_huddle():
    
    #credentials = TestCodes.query.filter_by(test_code='1dbb30da4b964850a6ddcc6d6f1c0088').first()
    test = TestCodes.query.order_by(TestCodes.id.desc()).first()
    
    if request.method == 'POST':
        test_code = request.form['test_code']
        tests = request.form.getlist('Test[]')
            
        test = TestCodes.query.filter_by(test_code=test_code).first()
        
        options = Options()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
        
        Login.login(driver, test.client_link, test.client_username, test.client_password)
        
        driver.get(test.client_link+'/morning-huddle')
        
        
        SinglePicker.MH_DatePicker(driver, test.test_date)
        update = driver.find_element(By.XPATH, MHXpath.update_btn).click()
        
        MornigHuddleBreakdown.Main_test(driver, test.test_date, test_code)
        MornigHuddleScorecard.Main_test(driver, test_code) 

    return render_template('Mh_Template/Mh_index.html',test=test)