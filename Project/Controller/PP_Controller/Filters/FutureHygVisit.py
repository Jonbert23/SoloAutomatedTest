from flask import Blueprint, render_template, url_for, request, redirect,flash
from flask_login import login_required, current_user
import time
import datetime
import uuid
from datetime import date
#Importing Selenium Dependecies
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from Project.Controller.PP_Controller.Filters.RangeDatePicker import DateFilter
from Project.Controller.PP_Controller.Filters.SingleDatePicker import SinglePicker 

from Project.models import PpFutureHygVisitFilter
from Project import db

class FutureHygVisitFilter:
    
    def FutureHygVisit_filter(driver, test_code, after, before, on, between_first, between_second):
        driver.implicitly_wait(5)
        
        wait = WebDriverWait(driver, 60)
        element = wait.until(EC.element_to_be_clickable((By.XPATH, Xpath.loader)))
        
        
        print('After Condition------------------------------------------------------------------------')
        FutureHygVisitFilter.add_filter(driver, 'After', after, 'none')
        time.sleep(3)
        FutureHygVisitFilter.collect_data(driver, test_code, 'After', after, 'none')
        driver.refresh()
        
        print('Before Condition------------------------------------------------------------------------')
        FutureHygVisitFilter.add_filter(driver, 'Before', before, 'none')
        time.sleep(3)
        FutureHygVisitFilter.collect_data(driver, test_code, 'Before', before, 'none')
        driver.refresh()
        
        print('On Condition------------------------------------------------------------------------')
        FutureHygVisitFilter.add_filter(driver, 'On', on, 'none')
        time.sleep(3)
        FutureHygVisitFilter.collect_data(driver, test_code, 'On', on, 'none')
        driver.refresh()
        
        print('Between Condition------------------------------------------------------------------------')
        FutureHygVisitFilter.add_filter(driver, 'Between', between_first, between_second)
        time.sleep(3)
        FutureHygVisitFilter.collect_data(driver, test_code, 'Between', between_first, between_second)
        driver.refresh()
        
    def add_filter(driver, selected_condition, date1, date2):
        
        add_fiter_button = driver.find_element(By.XPATH, Xpath.add_filter).click()
        search_filter = driver.find_element(By.XPATH, Xpath.search).send_keys('future')
        find_filter = driver.find_element(By.XPATH, Xpath.find_filter).click()
        condition_option = driver.find_element(By.XPATH, Xpath.condition_option).click()
        
        if selected_condition == 'After':
            greater_con = driver.find_element(By.XPATH, Xpath.after_con).click()
            calendar_trigger = driver.find_element(By.XPATH, Xpath.calendar_trigger).click()
            SinglePicker.Single_picker(driver, date1)
        
        if selected_condition == 'Before':
            before_con = driver.find_element(By.XPATH, Xpath.before_con).click()
            calendar_trigger = driver.find_element(By.XPATH, Xpath.calendar_trigger).click()
            SinglePicker.Single_picker(driver, date1) 
            
        if selected_condition == 'Between':
            between_con = driver.find_element(By.XPATH, Xpath.between_con).click()
            calendar_trigger = driver.find_element(By.XPATH, Xpath.calendar_trigger).click()
            DateFilter.rangePicker(driver, date1, date2) 
            
        if selected_condition == 'On':
            on_con = driver.find_element(By.XPATH, Xpath.on_con).click()
            calendar_trigger = driver.find_element(By.XPATH, Xpath.calendar_trigger).click()
            SinglePicker.Single_picker(driver, date1) 
            
        add_condition = driver.find_element(By.XPATH, Xpath.add_condition).click()
        
        
    def collect_data(driver, test_code, selected_condition, condition_value, condition_value2):
        
        for row in range(10):
            xpath_exist = driver.find_elements(By.XPATH, Xpath.patient_name(row+1))
            xpath_exist = len(xpath_exist)
            #print('Xpath Exist: '+str(xpath_exist))
            
            if xpath_exist != 0:
                
                patient_name = driver.find_element(By.XPATH, Xpath.patient_name(row+1)).text
                patient_id = driver.find_element(By.XPATH, Xpath.patient_id(row+1)).text
                patient_gender = driver.find_element(By.XPATH, Xpath.patient_gender(row+1)).text
                patient_email = driver.find_element(By.XPATH, Xpath.patient_email(row+1)).text
                
                patient_modal =  driver.find_element(By.XPATH, Xpath.patient_modal(row+1)).click()
                future_visit = driver.find_element(By.XPATH, Xpath.future_visit).text
                
                close_modal = driver.find_element(By.XPATH, Xpath.close_modal).click()
                print(str(row)+'. '+patient_name+' : '+str(future_visit))
                
                FutureHygVisitFilter.store_date(selected_condition, condition_value, condition_value2, test_code, patient_name, patient_id, patient_gender, patient_email, future_visit)
                
            else:
                break
            xpath_exist = 0
            
    def store_date(selected_condition, condition_value, condition_value2, test_code, patient_name, patient_id, patient_gender, patient_email, future_visit):
        condition_text1 = condition_value
        condition_text2 = condition_value2
        fv_text = future_visit
        condition_text = ''
        status =  ''
        
        condition_value = datetime.datetime.strptime(condition_value,'%Y-%m-%d')
        
        if future_visit != '-':
            future_visit = datetime.datetime.strptime(future_visit, '%b %d, %Y')
        else:
            future_visit = 'N/A'
            fv_text = 'N/A'
        
        
        if selected_condition == 'After':
            condition_text = 'After : '+condition_text1
            if future_visit != 'N/A':
                if condition_value <= future_visit:
                    status = 'Pass'
                else:
                    status = 'Fail'
            else:
                status = 'Fail'
                
        if selected_condition == 'Before': 
            condition_text = 'Before : '+condition_text1
            if future_visit != 'N/A':
                if condition_value >= future_visit:
                    status = 'Pass'
                else:
                    status = 'Fail'
            else:
                status = 'Fail'
                
        if selected_condition == 'On':
            condition_text = 'On : '+condition_text1
            if future_visit != 'N/A':
                if condition_value == future_visit:
                    status = 'Pass'
                else:
                    status = 'Fail'
            else:
                status = 'Fail'
                
        if selected_condition == 'Between':
            condition_value2 = datetime.datetime.strptime(condition_value2,'%Y-%m-%d')
            condition_text = 'Between : '+condition_text1+' and '+condition_text2
            if future_visit != 'N/A':
                if condition_value <= future_visit and condition_value2 >= future_visit:
                    status = 'Pass'
                else:
                    status = 'Fail'
            else:
                status = 'Fail'
                
        if patient_name != "":
            data = PpFutureHygVisitFilter(
                user_id = current_user.id,
                test_code = test_code,
                patient_name = patient_name,
                patient_id = patient_id,
                future_hyg_visit = fv_text,
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
    
    condition_option = '/html/body/div[1]/main/div[4]/div/div/div/div[2]/div/div[2]'
    
    after_con = '/html/body/div[1]/main/div[4]/div/div/div/div[2]/div/div[3]/ul/li[1]'
    before_con = '/html/body/div[1]/main/div[4]/div/div/div/div[2]/div/div[3]/ul/li[2]'
    between_con = '/html/body/div[1]/main/div[4]/div/div/div/div[2]/div/div[3]/ul/li[3]'
    on_con = '/html/body/div[1]/main/div[4]/div/div/div/div[2]/div/div[3]/ul/li[4]'
    
    calendar_trigger = '/html/body/div[1]/main/div[4]/div/div/div/div[3]/div/div/div'
    add_condition = '/html/body/div[1]/main/div[4]/div/div/div/div[4]/button[2]'
    
    future_visit = '/html/body/div[1]/main/div[4]/div/div/div/div[2]/div[2]/div/div/div[2]/div[1]/div[1]/div/div[2]/h5[1]'
    
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