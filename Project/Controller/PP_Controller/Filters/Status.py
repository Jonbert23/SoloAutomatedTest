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

from Project.models import PpStatusFilter
from Project import db



class StatusFilter:
    
    def Status_filter(driver, test_code):
        driver.implicitly_wait(5)
        
        wait = WebDriverWait(driver, 60)
        element = wait.until(EC.element_to_be_clickable((By.XPATH, Xpath.loader)))
        print('Gender: Male ------------------------------------------------------------------------------------')
        StatusFilter.add_filter(driver, 'Active')
        time.sleep(3)
        StatusFilter.collect_data(driver, test_code, 'Active')
        driver.refresh()
        
        print('Gender: Female ----------------------------------------------------------------------------------')
        StatusFilter.add_filter(driver, 'InActive')
        time.sleep(3)
        StatusFilter.collect_data(driver, test_code, 'InActive')
        driver.refresh()
        
       
    def add_filter(driver, selected_condition):
        
        add_fiter_button = driver.find_element(By.XPATH, Xpath.add_filter)
        add_fiter_button.click()
        
        search_filter = driver.find_element(By.XPATH, Xpath.search)
        search_filter.send_keys('status')
        
        find_filter = driver.find_element(By.XPATH, Xpath.find_filter)
        find_filter.click()
        
        if selected_condition == 'Active':
            driver.find_element(By.XPATH, Xpath.active).click()
        
        if selected_condition == 'InActive':
            driver.find_element(By.XPATH, Xpath.inactive).click()
            
        driver.find_element(By.XPATH, Xpath.add_condition).click()
            
        
        
    def collect_data(driver, test_code, selected_condition):
        
        for row in range(10):
            xpath_exist = driver.find_elements(By.XPATH, Xpath.patient_name(row+1))
            xpath_exist = len(xpath_exist)
            #print('Xpath Exist: '+str(xpath_exist))
            
            if xpath_exist != 0:
                
                patient_name = driver.find_element(By.XPATH, Xpath.patient_name(row+1)).text
                patient_id = driver.find_element(By.XPATH, Xpath.patient_id(row+1)).text
                patient_gender = driver.find_element(By.XPATH, Xpath.patient_gender(row+1)).text
                patient_email = driver.find_element(By.XPATH, Xpath.patient_email(row+1)).text
                
                open_modal = driver.find_element(By.XPATH, Xpath.patient_modal(row+1)).click()
                patient_status = driver.find_element(By.XPATH, Xpath.status).text
                close_modal = driver.find_element(By.XPATH, Xpath.close_modal).click()
                
                print(str(row)+'. '+patient_name+' : '+patient_status)
                StatusFilter.store_date(selected_condition, test_code, patient_name, patient_id, patient_gender, patient_email, patient_status)
            else:
                break 
            
            xpath_exist = 0
            
    def store_date(selected_condition, test_code, patient_name, patient_id, patient_gender, patient_email, patient_status):
        patient_status = patient_status.replace(" ","")
        condition_text ='N/A'
        status = 'N/A'
        
        if selected_condition == 'Active':
            condition_text = 'Patient status should be active'
            if patient_status == 'Active':
                status = 'Pass'
            else:
                status = 'Fail'
                
        if selected_condition == 'InActive':
            condition_text = 'Patient status should be inactive'
            if patient_status == 'InActive':
                status = 'Pass'
            else:
                status = 'Fail'
        
        data = PpStatusFilter(
            user_id = current_user.id,
            test_code = test_code,
            patient_name = patient_name,
            patient_id = patient_id,
            patient_status = patient_status,
            patient_gender = patient_gender,
            patient_email = patient_email,
            Condition = condition_text,
            status = status   
        )
        db.session.add(data)
        db.session.commit()
            
class Xpath:
    loader = '/html/body/div[1]/main/div[1]/div/div/div/div[2]/button'
    add_filter = '/html/body/div[1]/main/div[2]/div/div[1]/div/div/div/div/div[1]/div[1]/button'
    search = '/html/body/div[1]/main/div[2]/div/div[1]/div/div/div/div/div[2]/div[1]/input'
    find_filter = '/html/body/div[1]/main/div[2]/div/div[1]/div/div/div/div/div[2]/div[2]/ol/span[1]/li'
    
    exit_filter = '/html/body/div[1]/main/div[2]/div/div[1]/div/div/div/span/svg'
    edit_filter = '/html/body/div[1]/main/div[2]/div/div[1]/div/div/div/span/div/button'
    
    active = '/html/body/div[1]/main/div[4]/div/div/div/fieldset/label[1]/input'
    inactive = '/html/body/div[1]/main/div[4]/div/div/div/fieldset/label[2]/input'
    
    add_condition = '/html/body/div[1]/main/div[4]/div/div/div/div[2]/button[2]'
    status = '/html/body/div[1]/main/div[4]/div/div/div/div[2]/div[2]/div/div/div[1]/div[1]/div[4]/div/h5'
    close_modal = '/html/body/div[1]/main/div[4]/div/div/div/div[2]/div[1]/div[1]/button'
    
    def patient_name(row):
        xpath = '/html/body/div[1]/main/div[2]/div/div[2]/div/div/div/div/div[2]/div[1]/table/tbody/tr['+str(row)+']/td[2]'
        return xpath
    
    def patient_id(row):
        xpath = '/html/body/div[1]/main/div[2]/div/div[2]/div/div/div/div/div[2]/div[1]/table/tbody/tr['+str(row)+']/td[3]'
        return xpath
    
    def patient_age(row):
        xpath = '/html/body/div[1]/main/div[2]/div/div[2]/div/div/div/div/div[2]/div[1]/table/tbody/tr['+str(row)+']/td[4]'
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
    
    
    
                 
    
    
        
        
        
        