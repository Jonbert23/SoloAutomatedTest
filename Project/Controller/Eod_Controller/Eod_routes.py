from flask import Blueprint, render_template, url_for, request, redirect
from flask_login import login_required, current_user
from Project.Controller.Eod_Controller.Eod_tester import testEod
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from Project.Controller.Global_Controller.Global_test import Login

eod = Blueprint('eod', __name__)

@eod.route("/eod-form")
def eodForm():
    d = DesiredCapabilities.CHROME
    d['loggingPrefs'] = {'browser': 'ERROR'}
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), desired_capabilities=d)
    Login.login(driver, "https://solo.next.jarvisanalytics.com/end-of-day", "testryan", "Jarvis.123")
    
    if not driver:
        return False

    testEod(driver)
    return render_template('Eod_Template/Eod_index.html')