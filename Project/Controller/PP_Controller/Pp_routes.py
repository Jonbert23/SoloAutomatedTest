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


pp = Blueprint('pp', __name__)

@pp.route("/patient-portal", methods=['POST','GET'])
def patient_portal():
    
    if request.method == 'POST':
        filters = request.form.getlist('Filter[]')
        client_url = request.form['client_url']
        client_username = request.form['client_username']
        client_password = request.form['client_password']
            
        #Declaring Selenium driver--------------------------------------------------------------------
        options = Options()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
        
        #Calling Login Global Test -----------------------------------------------------------------
        GlobalLogin.Login(driver, client_url, client_username, client_password)
        
        
        driver.get(client_url+'/patient-portal')
        
        for pp_filter in filters:
            print(pp_filter)
            if pp_filter == 'age':
                greater = request.form['greater']
                less = request.form['less']
                equal = request.form['equal']
                between_first = request.form['between_first']
                between_second = request.form['between_second']

                AgeFilter.Age_filter(driver, greater, less, equal, between_first, between_second)
        
    return render_template('PP_Template/PP_index.html')
