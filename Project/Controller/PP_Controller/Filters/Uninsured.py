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

from Project.models import PpUninsuredFilter
from Project import db



class UninsuredFilter:
    
    def Uninsured_filter(driver, test_code):
        driver.implicitly_wait(5)
        
        wait = WebDriverWait(driver, 60)
        element = wait.until(EC.element_to_be_clickable((By.XPATH, Xpath.loader)))
        print('Uninsured ------------------------------------------------------------------------------------')
        UninsuredFilter.add_filter(driver, 'Uninsured')
        time.sleep(3)
        UninsuredFilter.collect_data(driver, test_code, 'Uninsured')
        driver.refresh()
        
        print('Insured ----------------------------------------------------------------------------------')
        UninsuredFilter.add_filter(driver, 'Insured')
        time.sleep(3)
        UninsuredFilter.collect_data(driver, test_code, 'Insured')
        driver.refresh()
        
       
    def add_filter(driver, selected_condition):
        
        add_fiter_button = driver.find_element(By.XPATH, Xpath.add_filter)
        add_fiter_button.click()
        
        search_filter = driver.find_element(By.XPATH, Xpath.search)
        search_filter.send_keys('uninsured')
        
        find_filter = driver.find_element(By.XPATH, Xpath.find_filter)
        find_filter.click()
        
        if selected_condition == 'Uninsured':
            driver.find_element(By.XPATH, Xpath.active).click()
        
        if selected_condition == 'Insured':
            driver.find_element(By.XPATH, Xpath.inactive).click()
            
        driver.find_element(By.XPATH, Xpath.add_condition).click()
            
        
    def collect_data(driver, test_code, selected_condition):
        for row in range(100):
            xpath_exist = driver.find_elements(By.XPATH, Xpath.patient_name(row+1))
            xpath_exist = len(xpath_exist)
            #print('Xpath Exist: '+str(xpath_exist))
        
            if xpath_exist != 0:
                loop_counter = loop_counter + 1
                patient_name = driver.find_element(By.XPATH, Xpath.patient_name(row+1)).text
                patient_id = driver.find_element(By.XPATH, Xpath.patient_id(row+1)).text
                patient_gender = driver.find_element(By.XPATH, Xpath.patient_gender(row+1)).text
                patient_email = driver.find_element(By.XPATH, Xpath.patient_email(row+1)).text
                
                open_modal = driver.find_element(By.XPATH, Xpath.patient_modal(row+1)).click()
                insurance = driver.find_element(By.XPATH, Xpath.insurance).text
                close_modal = driver.find_element(By.XPATH, Xpath.close_modal).click()
                
                print(str(row)+'. '+patient_name+' : '+insurance)
                UninsuredFilter.store_date(selected_condition, test_code, patient_name, patient_id, patient_gender, patient_email, insurance)
            else:
                break 
            
            
            xpath_exist = 0
            
    def store_date(selected_condition, test_code, patient_name, patient_id, patient_gender, patient_email, insurance):
        insurance_in_text = insurance
        insurance = insurance.replace("$","").replace(" ","").replace(",","")
            
        condition_text ='N/A'
        status = 'N/A'
        
        if selected_condition == 'Uninsured':
            condition_text = 'Should be uninsured'
            if float(insurance) <= 0:
                status = 'Pass'
            else:
                status = 'Fail'
                
        if selected_condition == 'Insured':
            condition_text = 'Should be insured'
            if float(insurance) > 0:
                status = 'Pass'
            else:
                status = 'Fail'
                
        if float(insurance) == 0:
            insurance_in_text = 'N/A'
        
        if patient_name != "":
            data = PpUninsuredFilter(
                user_id = current_user.id,
                test_code = test_code,
                patient_name = patient_name,
                patient_id = patient_id,
                insurance = insurance_in_text,
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
    find_filter = '/html/body/div[1]/main/div[2]/div/div[1]/div/div/div/div/div[2]/div[2]/ol/span/li'
    
    exit_filter = '/html/body/div[1]/main/div[2]/div/div[1]/div/div/div/span/svg'
    edit_filter = '/html/body/div[1]/main/div[2]/div/div[1]/div/div/div/span/div/button'
    
    active = '/html/body/div[1]/main/div[4]/div/div/div/fieldset/label[1]/input'
    inactive = '/html/body/div[1]/main/div[4]/div/div/div/fieldset/label[2]/input'
    
    add_condition = '/html/body/div[1]/main/div[4]/div/div/div/div[2]/button[2]'
    insurance = '/html/body/div[1]/main/div[4]/div/div/div/div[2]/div[2]/div/div/div[2]/div[1]/div[3]/div/div[2]/h5'
    close_modal = '/html/body/div[1]/main/div[4]/div/div/div/div[2]/div[1]/div[1]/button'
    next_page = '/html/body/div[1]/main/div[2]/div/div[2]/div/div/div/div/div[2]/div[2]/div[2]/div[2]/button[2]'
    
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
    
    
    
                 
    
    
        
        
        
        