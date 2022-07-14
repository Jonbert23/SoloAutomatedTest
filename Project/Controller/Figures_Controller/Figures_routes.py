#Importing Flask Dependecies
from flask import Blueprint, render_template, url_for, request, redirect,flash
from flask_login import login_required, current_user
import time
import datetime
#Importing Selenium Dependecies
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
#Importing  File Classes 
from Project.Controller.Global_Controller.Global_test import Login
from Project.Controller.Figures_Controller.Dashboard import Dashboard
from Project.Controller.Figures_Controller.Eod import Eod
from Project.Controller.Figures_Controller.Calendar import Calendar
from Project.Controller.Figures_Controller.Mh import MorningHuddle
from Project.Controller.Global_Controller.Single_date_picker import SinglePicker
from Project.Controller.Global_Controller.Range_date_picker import DateFilter


fm = Blueprint('fm', __name__)

@fm.route("/figures-matching",methods=['GET', 'POST'])
def figuresMatching():
    
    if request.method == 'POST':
        #Request-------------------------------------------------------------------------------------
        modules = request.form.getlist('Module[]')
        metrics = request.form.getlist('Metric[]')
        client_url = request.form['client_url']
        client_username = request.form['client_username']
        client_password = request.form['client_password']
        test_type = request.form['test_type'] 
        test_month = request.form['test_month']
        test_day = request.form['test_day']
        param = request.form['param']
        
        print(param)
        # Declaring Selenium driver--------------------------------------------------------------------
        options = Options()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
        
        # Calling Login Global Test -----------------------------------------------------------------
        Login.login(driver, client_url, client_username, client_password)
        
        for module in modules:
            if module == "eod":
                eod_data = Eod.main(driver, metrics, client_url, test_type, test_month, test_day)
                
            if module == "dashboard":
                dash_data = Dashboard.main(driver, metrics, client_url, test_type, test_month, test_day)
                print(dash_data[0])
                
            if module == "calendar":
                calendar_data = Calendar.main(driver, metrics, client_url , test_month, param)
                
            if module == 'morning_huddle':
                mh_data = MorningHuddle.main(driver, metrics, client_url, test_day, param)
        
        driver.quit()
        
        return render_template('Figures_Template/Figures_index.html')
    
    return render_template('Figures_Template/Figures_index.html')
