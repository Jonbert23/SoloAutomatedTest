#Importing Flask Dependecies
from flask import Blueprint, render_template, url_for, request, redirect
from flask_login import login_required, current_user
import time
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
from Project.Controller.Figures_Controller.Figures_xpath import DatePicker
from Project.Controller.Global_Controller.Range_date_picker import DateFilter
fm = Blueprint('fm', __name__)

@fm.route("/figures-matching",methods=['GET', 'POST'])
def figuresMatching():
    
    if request.method == 'POST':
        #Request-------------------------------------------------------------------------------------
        modules = request.form.getlist('Module[]')
        metrics = request.form.getlist('Metric[]')
        
        #Declaring Selenium driver--------------------------------------------------------------------
        options = Options()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
        driver.fullscreen_window()
        
        #Calling Login Global Test -----------------------------------------------------------------
        Login.login(driver, "https://solo.next.jarvisanalytics.com", "testryan", "Jarvis.123")
        driver.implicitly_wait(1000000)
        
        DateFilter.rangePicker(driver)
        
       
        # for module in modules:
        #     if module == "eod":
        #         driver.get('https://solo.next.jarvisanalytics.com/end-of-day')
        #         Eod.main(driver, metrics)
                
        #     if module == "dashboard":
        #         driver.get('https://solo.next.jarvisanalytics.com/solo/results')
        #         Dashboard.main(driver, metrics)
                
        #     if module == "calendar":
        #         driver.get('https://solo.next.jarvisanalytics.com/calendar/appointments')
        #         Calendar.main(driver, metrics)
        
        # driver.quit()
        
        return render_template('Figures_Template/Figures_index.html')
    
    return render_template('Figures_Template/Figures_index.html')
