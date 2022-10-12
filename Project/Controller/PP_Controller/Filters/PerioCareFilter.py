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

from Project.models import PpPerioCareFilter
from Project import db



class PerioCareFilter:
    
    def PerioCare_filter(driver, test_code):
        driver.implicitly_wait(60)
        
        wait = WebDriverWait(driver, 60)
        element = wait.until(EC.element_to_be_clickable((By.XPATH, Xpath.loader)))
        print('Uninsured ------------------------------------------------------------------------------------')
        PerioCareFilter.add_filter(driver, 'In_Perio')
        time.sleep(3)
        PerioCareFilter.collect_data(driver, test_code, 'In_Perio')
        driver.refresh()
        
        print('Insured ----------------------------------------------------------------------------------')
        PerioCareFilter.add_filter(driver, 'Not_Perio')
        time.sleep(3)
        PerioCareFilter.collect_data(driver, test_code, 'Not_Perio')
        driver.refresh()
        
       
    def add_filter(driver, selected_condition):
        
        add_fiter_button = driver.find_element(By.XPATH, Xpath.add_filter)
        add_fiter_button.click()
        
        search_filter = driver.find_element(By.XPATH, Xpath.search)
        search_filter.send_keys('perio')
        
        find_filter = driver.find_element(By.XPATH, Xpath.find_filter)
        find_filter.click()
        
        if selected_condition == 'In_Perio':
            driver.find_element(By.XPATH, Xpath.active).click()
        
        if selected_condition == 'Not_Perio':
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
                
                
                open_modal = driver.find_element(By.XPATH, Xpath.patient_modal(row+1)).click()
                
                insurance = driver.find_element(By.XPATH, Xpath.insurance).text
                age = driver.find_element(By.XPATH, Xpath.age).text
                p_status = driver.find_element(By.XPATH, Xpath.p_status).text
                
                ar_tab = driver.find_element(By.XPATH, Xpath.ar_tab).click()
                time.sleep(2)
                pc_procedure = ['D4341','D4342','D4910','D4346','D4355']
                ar_counter = driver.find_elements(By.XPATH, Xpath.ar_counter)
                ar_counter = len(ar_counter)
                print(ar_counter)
                patient_pc = ''
                
                if ar_counter > 1:
                    for row_i in range(len(pc_procedure)):
                        for row_j in range(ar_counter):
                            procedure = driver.find_element(By.XPATH, Xpath.ar_procedure(row_j+1)).text
                            
                            if pc_procedure[row_i] == procedure:
                                patient_pc = patient_pc + " " +procedure
                                break
                
                ar_counter = 0      
                close_modal = driver.find_element(By.XPATH, Xpath.close_modal).click()
                print('---------------------------------------------------------------')
                print('Name: '+patient_name)
                print('Age: '+age)
                print('Status: '+p_status)
                print('Perio Care Procedure: '+ patient_pc)
               
                PerioCareFilter.store_date(selected_condition, test_code, patient_name, patient_id, age, p_status, patient_pc)
            else:
                break 
            
            
            xpath_exist = 0
            
    def store_date(selected_condition, test_code, patient_name, patient_id, age, p_status, patient_pc):
            
        condition_text ='N/A'
        status = 'N/A'
        
        if selected_condition == 'In_Perio':
            condition_text = 'Perio Care: In'
            if patient_pc != '' and int(age) >= 30 and p_status == 'Active':
                status = 'Pass'
            else:
                status = 'Fail'
                
        if selected_condition == 'Not_Perio':
            condition_text = 'Perio Care: Not'
            if patient_pc == '' or int(age) <= 30 or p_status == 'InActive':
                status = 'Pass'
            else:
                status = 'Fail'
                
        if patient_pc == '':
            patient_pc = 'No Perio Care Procedure'
        
        if patient_name != "":
            data = PpPerioCareFilter(
                user_id = current_user.id,
                test_code = test_code,
                patient_name = patient_name,
                patient_id = patient_id,
                age = age,
                p_status = p_status,
                patient_pc = patient_pc,
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
    age = '/html/body/div[1]/main/div[4]/div/div/div/div[2]/div[2]/div/div/div[1]/div[1]/div[1]/div/h5'
    p_status = '/html/body/div[1]/main/div[4]/div/div/div/div[2]/div[2]/div/div/div[1]/div[1]/div[4]/div/h5'
    close_modal = '/html/body/div[1]/main/div[4]/div/div/div/div[2]/div[1]/div[1]/button'
    ar_tab = '/html/body/div[1]/main/div[4]/div/div/div/div[2]/div[1]/ul/li[6]/a'
    ar_counter = '/html/body/div[1]/main/div[4]/div/div/div/div[2]/div[2]/div/div/div[2]/div/div/table/tbody/tr'
    
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
    
    def ar_procedure(row):
        xpath = '/html/body/div[1]/main/div[4]/div/div/div/div[2]/div[2]/div/div/div[2]/div/div/table/tbody/tr['+str(row)+']/td[2]'
        return xpath
    
    
    
                 
    
    
        
        
        
        