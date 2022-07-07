from flask import Blueprint, render_template, url_for, request, redirect
from flask_login import login_required, current_user
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from Project.Controller.Global_Controller.Global_test import Login
from Project.Controller.Figures_Controller.Dashboard import Dashboard

fm = Blueprint('fm', __name__)

@fm.route("/figures-matching",methods=['GET', 'POST'])
def figuresMatching():
    
    if request.method == 'POST':
        modules = request.form.getlist('Module[]')
        metrics = request.form.getlist('Metric[]')
            
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        Login.login(driver, "https://solo.next.jarvisanalytics.com", "testryan", "Jarvis.123")
        driver.implicitly_wait(1000000)
       
        dash_data = 'null'
        for module in modules:
            if module == "dashboard":
                driver.get('https://solo.next.jarvisanalytics.com/solo/results')
                dash_data = Dashboard.main(driver, metrics)
            
            if module == "calendar":
                driver.get('https://solo.next.jarvisanalytics.com/calendar/appointments')
                
                
            if module == "eod":
                driver.get('https://solo.next.jarvisanalytics.com/end-of-day')
        
        driver.quit()
        
        return render_template('Figures_Template/Figures_index.html', dash_data=dash_data)
    
    return render_template('Figures_Template/Figures_index.html')
