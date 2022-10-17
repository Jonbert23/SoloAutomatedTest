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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from Project.models import PpVisitFilter
from Project import db



class VisitFilter:
    
    def Visit_filter(driver, greater, less, equal, between_first, between_second, test_code):
        driver.implicitly_wait(60)
        
        wait = WebDriverWait(driver, 60)
        element = wait.until(EC.element_to_be_clickable((By.XPATH, Xpaths.loader)))
        
        greater_xpath = Xpaths.greater_con
        less_xpath = Xpaths.less_con
        equal_xpath = Xpaths.equal_con
        between_xpath = Xpaths.between_con
        # (driver, condition_xpath, condition_type, condition_value1, condition_value2):
        print("Greater Condition--------------------------------------------------------------------------")
        VisitFilter.add_filter(driver, greater_xpath, "Greater", greater, 0)
        time.sleep(3)
        VisitFilter.collect_data(driver, "Greater", greater, 0, test_code)
        driver.refresh()
        
        print("Less Condition--------------------------------------------------------------------------")
        VisitFilter.add_filter(driver, less_xpath, "Less", less, 0)
        time.sleep(3)
        VisitFilter.collect_data(driver, "Less", less, 0, test_code)
        driver.refresh()
        
        print("Equal Condition--------------------------------------------------------------------------")
        VisitFilter.add_filter(driver, equal_xpath, "Equal", equal, 0)
        time.sleep(3)
        VisitFilter.collect_data(driver, "Equal", equal, 0, test_code)
        driver.refresh()
        
        print("Between Condition--------------------------------------------------------------------------")
        VisitFilter.add_filter(driver, between_xpath, "Between", between_first, between_second)
        time.sleep(3)
        VisitFilter.collect_data(driver, "Between", between_first, between_second, test_code)
        driver.refresh()
        
       
    def add_filter(driver, condition_xpath, condition_type, condition_value1, condition_value2):
        
        add_fiter_button = driver.find_element(By.XPATH, Xpaths.add_filter)
        add_fiter_button.click()
        
        search_filter = driver.find_element(By.XPATH, Xpaths.search)
        search_filter.send_keys('visit')
        
        find_filter = driver.find_element(By.XPATH, Xpaths.find_filter)
        find_filter.click()
        
        conditons_btn = driver.find_element(By.XPATH, Xpaths.conditons_btn)
        conditons_btn.click()
        
        select_condition = driver.find_element(By.XPATH, condition_xpath)
        select_condition.click()
        
        if condition_type == 'Between':
            input_con = driver.find_element(By.XPATH, Xpaths.between_input1)
            input_con.send_keys(condition_value1)
            
            input_con = driver.find_element(By.XPATH, Xpaths.between_input2)
            input_con.send_keys(condition_value2)
            
            add_filter_btn = driver.find_element(By.XPATH, Xpaths.add_filter_btn)
            add_filter_btn.click()
            
        else: 
            input_con = driver.find_element(By.XPATH, Xpaths.input_con)
            input_con.send_keys(condition_value1)
            
            add_filter_btn = driver.find_element(By.XPATH, Xpaths.add_filter_btn)
            add_filter_btn.click()
        
        
        
    def collect_data(driver, condition, condition_value, condition_value2, test_code):
        
        for row in range(10):
            xpath_exist = driver.find_elements(By.XPATH, Xpaths.patient_name(row+1))
            xpath_exist = len(xpath_exist)
            #print('Xpath Exist: '+str(xpath_exist))
            
            if xpath_exist != 0:
                
                patient_name = driver.find_element(By.XPATH, Xpaths.patient_name(row+1)).text
                patient_id = driver.find_element(By.XPATH, Xpaths.patient_id(row+1)).text
                patient_gender = driver.find_element(By.XPATH, Xpaths.patient_gender(row+1)).text
                patient_email = driver.find_element(By.XPATH, Xpaths.patient_email(row+1)).text
                
                patient_modal =  driver.find_element(By.XPATH, Xpaths.patient_modal(row+1)).click()
                ledger_tab = driver.find_element(By.XPATH, Xpaths.ledger_tab).click()
                time.sleep(3)
                ledger_conuter = driver.find_elements(By.XPATH, Xpaths.ledger_counter)
                ledger_conuter = len(ledger_conuter)
                current_date = ''
                date_holder = ''
                date_counter = 0
                
                for row in range(ledger_conuter):
                    visit_date = driver.find_element(By.XPATH, Xpaths.visit_dates(row+1)).text
                    # print(visit_date)
                    
                    if current_date != visit_date:
                        date_counter = date_counter + 1
                        date_holder = date_holder+ ' '+ visit_date
                        current_date = visit_date
                        
                close_modal = driver.find_element(By.XPATH, Xpaths.close_modal).click()
               
                print('Patient Name: '+patient_name)
                print('Number Of Visit: '+str(date_counter))
                print('Visit Dates: '+date_holder)
                print('')
                print('')
                
                VisitFilter.store_date(condition, condition_value, condition_value2, test_code, patient_name, patient_id, patient_gender, patient_email, date_counter)
                
            else:
                break
            
            xpath_exist = 0
            
    def store_date(condition, condition_value, condition_value2, test_code, patient_name, patient_id, patient_gender, patient_email, date_counter):
        
        condition_text = ''
        status = ''
        
        if condition == 'Greater':
            condition_text = 'Greater than '+str(condition_value)
            if float(condition_value) < float(date_counter):
                status = 'Pass'
            else:
                status = 'Fail'
                
        if condition == 'Less': 
            condition_text = 'Less than '+str(condition_value)
            if float(condition_value) > float(date_counter):
                status = 'Pass'
            else:
                status = 'Fail'
                
        if condition == 'Equal':
            condition_text = 'Equal to '+str(condition_value)
            if float(condition_value) == float(date_counter):
                status = 'Pass'
            else:
                status = 'Fail'
                
        if condition == 'Between':
            condition_text = 'Between '+str(condition_value)+' and '+str(condition_value2)
            if float(condition_value) <= float(date_counter) and float(condition_value2) >= float(date_counter):
                status = 'Pass'
            else:
                status = 'Fail'
        
        data = PpVisitFilter(
            user_id = current_user.id,
            test_code = test_code,
            patient_name = patient_name,
            patient_id = patient_id,
            number_of_visit = date_counter,
            patient_gender = patient_gender,
            patient_email = patient_email,
            Condition = condition_text,
            status = status   
        )
        db.session.add(data)
        db.session.commit()
            
class Xpaths:
    loader = '/html/body/div[1]/main/div[1]/div/div/div/div[2]/button'
    add_filter = '/html/body/div[1]/main/div[2]/div/div[1]/div/div/div/div/div[1]/div[1]/button'
    search = '/html/body/div[1]/main/div[2]/div/div[1]/div/div/div/div/div[2]/div[1]/input'
    find_filter = '/html/body/div[1]/main/div[2]/div/div[1]/div/div/div/div/div[2]/div[2]/ol/span[5]/li'
    
    conditons_btn = '/html/body/div[1]/main/div[4]/div/div/div/div[2]/div/div[2]'
    greater_con = '/html/body/div[1]/main/div[4]/div/div/div/div[2]/div/div[3]/ul/li[1]'
    less_con = '/html/body/div[1]/main/div[4]/div/div/div/div[2]/div/div[3]/ul/li[2]'
    between_con = '/html/body/div[1]/main/div[4]/div/div/div/div[2]/div/div[3]/ul/li[3]'
    equal_con = '/html/body/div[1]/main/div[4]/div/div/div/div[2]/div/div[3]/ul/li[4]'
    input_con = '/html/body/div[1]/main/div[4]/div/div/div/div[3]/div/div/input'
    add_filter_btn = '/html/body/div[1]/main/div[4]/div/div/div/div[4]/button[2]'
    exit_filter = '/html/body/div[1]/main/div[2]/div/div[1]/div/div/div/span/svg'
    edit_filter = '/html/body/div[1]/main/div[2]/div/div[1]/div/div/div/span/div/button'
    
    between_input1 = '/html/body/div[1]/main/div[4]/div/div/div/div[3]/div/div[1]/div/input'
    between_input2 = '/html/body/div[1]/main/div[4]/div/div/div/div[3]/div/div[2]/div/input'
    
    ledger_tab = '/html/body/div[1]/main/div[4]/div/div/div/div[2]/div[1]/ul/li[4]/a'
    ledger_counter = '/html/body/div[1]/main/div[4]/div/div/div/div[2]/div[2]/div/div/div/div/table/tbody/tr'
    close_modal = '/html/body/div[1]/main/div[4]/div/div/div/div[2]/div[1]/div[1]/button'
    
    
    def patient_name(row):
        xpath = '/html/body/div[1]/main/div[2]/div/div[2]/div/div/div/div/div[2]/div[1]/table/tbody/tr['+str(row)+']/td[2]'
        return xpath
    
    def patient_id(row):
        xpath = '/html/body/div[1]/main/div[2]/div/div[2]/div/div/div/div/div[2]/div[1]/table/tbody/tr['+str(row)+']/td[3]'
        return xpath
    
    def patient_gender(row):
        xpath = '/html/body/div[1]/main/div[2]/div/div[2]/div/div/div/div/div[2]/div[1]/table/tbody/tr['+str(row)+']/td[5]'
        return xpath
    
    def patient_email(row):
        xpath = '/html/body/div[1]/main/div[2]/div/div[2]/div/div/div/div/div[2]/div[1]/table/tbody/tr['+str(row)+']/td[13]'
        return xpath
    
    def patient_modal(row):
        xpath = '/html/body/div[1]/main/div[2]/div/div[2]/div/div/div/div/div[2]/div[1]/table/tbody/tr['+str(row)+']/td[2]/span/span'
        return xpath
    
    def visit_dates(row):
        xpath = '/html/body/div[1]/main/div[4]/div/div/div/div[2]/div[2]/div/div/div/div/table/tbody/tr['+str(row)+']/td[7]'
        return xpath
    
    
    
                 
    
    
        
        
        
        