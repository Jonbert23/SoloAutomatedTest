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

from Project.models import PpGenderFilter
from Project import db



class GenderFilter:
    
    def Gender_filter(driver, test_code):
        driver.implicitly_wait(5)
        
        wait = WebDriverWait(driver, 60)
        element = wait.until(EC.element_to_be_clickable((By.XPATH, AgeFilterXpath.loader)))
        
        print('Gender: Male ------------------------------------------------------------------------------------')
        GenderFilter.add_filter(driver, 'Male')
        time.sleep(3)
        GenderFilter.collect_data(driver, test_code, 'Male')
        driver.refresh()
        
        print('Gender: Female ----------------------------------------------------------------------------------')
        GenderFilter.add_filter(driver, 'Female')
        time.sleep(3)
        GenderFilter.collect_data(driver, test_code, 'Female')
        driver.refresh()
        
       
    def add_filter(driver, selected_condition):
        
        add_fiter_button = driver.find_element(By.XPATH, AgeFilterXpath.add_filter)
        add_fiter_button.click()
        
        search_filter = driver.find_element(By.XPATH, AgeFilterXpath.search)
        search_filter.send_keys('gender')
        
        find_filter = driver.find_element(By.XPATH, AgeFilterXpath.find_filter)
        find_filter.click()
        
        if selected_condition == 'Male':
            driver.find_element(By.XPATH, AgeFilterXpath.male).click()
        
        if selected_condition == 'Female':
            driver.find_element(By.XPATH, AgeFilterXpath.female).click()
            
        driver.find_element(By.XPATH, AgeFilterXpath.add_condition).click()
            
        
        
    def collect_data(driver, test_code, selected_condition):
        
        for row in range(10):
            xpath_exist = driver.find_elements(By.XPATH, AgeFilterXpath.patient_name(row+1))
            xpath_exist = len(xpath_exist)
            #print('Xpath Exist: '+str(xpath_exist))
            
            if xpath_exist != 0:
                
                patient_name = driver.find_element(By.XPATH, AgeFilterXpath.patient_name(row+1)).text
                patient_id = driver.find_element(By.XPATH, AgeFilterXpath.patient_id(row+1)).text
                patient_age = driver.find_element(By.XPATH, AgeFilterXpath.patient_age(row+1)).text
                patient_gender = driver.find_element(By.XPATH, AgeFilterXpath.patient_gender(row+1)).text
                patient_email = driver.find_element(By.XPATH, AgeFilterXpath.patient_email(row+1)).text
                
                
                print(str(row)+'. '+patient_name+' : '+patient_gender)
                GenderFilter.store_date(selected_condition, test_code, patient_name, patient_id, patient_gender, patient_email, patient_age)
            else:
                break 
            
            xpath_exist = 0
            
    def store_date(selected_condition, test_code, patient_name, patient_id, patient_gender, patient_email, patient_age):
        condition_text =''
        status = ''
        
        if selected_condition == 'Male':
            condition_text = 'Gender should be male'
            if patient_gender == 'Male':
                status = 'Pass'
            else:
                status = 'Fail'
                
        if selected_condition == 'Female':
            condition_text = 'Gender should be female'
            if patient_gender == 'Female':
                status = 'Pass'
            else:
                status = 'Fail'
        
        data = PpGenderFilter(
            user_id = current_user.id,
            test_code = test_code,
            patient_name = patient_name,
            patient_id = patient_id,
            patient_age = patient_age,
            patient_gender = patient_gender,
            patient_email = patient_email,
            Condition = condition_text,
            status = status   
        )
        db.session.add(data)
        db.session.commit()
            
class AgeFilterXpath:
    loader = '/html/body/div[1]/main/div[1]/div/div/div/div[2]/button'
    add_filter = '/html/body/div[1]/main/div[2]/div/div[1]/div/div/div/div/div[1]/div[1]/button'
    search = '/html/body/div[1]/main/div[2]/div/div[1]/div/div/div/div/div[2]/div[1]/input'
    find_filter = '/html/body/div[1]/main/div[2]/div/div[1]/div/div/div/div/div[2]/div[2]/ol/span[1]/li'
    
    exit_filter = '/html/body/div[1]/main/div[2]/div/div[1]/div/div/div/span/svg'
    edit_filter = '/html/body/div[1]/main/div[2]/div/div[1]/div/div/div/span/div/button'
    
    male = '/html/body/div[1]/main/div[4]/div/div/div/fieldset/label[1]/input'
    female = '/html/body/div[1]/main/div[4]/div/div/div/fieldset/label[2]/input'
    
    add_condition = '/html/body/div[1]/main/div[4]/div/div/div/div[2]/button[2]'
    
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
    
    
    
                 
    
    
        
        
        
        