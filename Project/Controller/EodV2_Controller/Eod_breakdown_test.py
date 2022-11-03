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
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from Project.Controller.EodV2_Controller.Eod_xpath import EodXpath
from Project.Controller.Global_Controller.Single_date_picker import SinglePicker
from Project.models import EodMain
from Project.models import EodBrk
from Project import db

class EodBreakdown:
    
    def Main_test(driver, test_code, test_date):
        
        time.sleep(5)
        driver.implicitly_wait(1)
        wait = WebDriverWait(driver, 60)
        loader = wait.until(EC.element_to_be_clickable((By.XPATH, EodXpath.update_btn)))
        action =  ActionChains(driver)
        
       
       
        
        metric_counter = driver.find_elements(By.XPATH, EodXpath.metric_counter) 
        metric_counter = len(metric_counter)
        # print(metric_counter)
        
        eod_main = EodMain(
            user_id = current_user.id,
            test_code = test_code,
        )
        db.session.add(eod_main)
        db.session.commit()
        
        eod_brk = EodBrk(
            user_id = current_user.id,
            test_code = test_code,
        )
        db.session.add(eod_brk)
        db.session.commit()
        
        eod_main = EodMain.query.filter_by(test_code=test_code).first()
        eod_brk = EodBrk.query.filter_by(test_code=test_code).first()
        
        for row in range(metric_counter):
            metric_name = driver.find_element(By.XPATH, EodXpath.metric_name(row+1)).text
            #print(metric_name)
            # print(metric_value)
            
            if metric_name == 'PT portion collections % today collected':
                metric_data = driver.find_element(By.XPATH, EodXpath.metric_data(row+1)).get_attribute('value')
                brk_data = EodBreakdown.collect_brk_data(driver, row, metric_name, action)
                
                eod_main.pt_portion_col = metric_data
                eod_brk.pt_portion_col = brk_data
                db.session.commit()
                
                print(metric_name)
                print(metric_data)
                print(brk_data)
                print()
                
            if metric_name == 'Adjustments' or metric_name == 'Total adjustment':
                metric_data = driver.find_element(By.XPATH, EodXpath.metric_data(row+1)).get_attribute('value')
                brk_data = EodBreakdown.collect_brk_data(driver, row, metric_name, action)
                
                eod_main.adjustments = metric_data
                eod_brk.adjustments = brk_data
                db.session.commit()
                
                print(metric_name)
                print(metric_data)
                print(brk_data)
                print()
                
            if metric_name == 'Collection' or metric_name == 'Total collection':
                metric_data = driver.find_element(By.XPATH, EodXpath.metric_data(row+1)).get_attribute('value')
                brk_data = EodBreakdown.collect_brk_data(driver, row, metric_name, action)
                
                eod_main.total_collection = metric_data
                eod_brk.total_collection = brk_data
                db.session.commit()
                
                print(metric_name)
                print(metric_data)
                print(brk_data)
                print()
                
            if metric_name == 'Daily collections':
                metric_data = driver.find_element(By.XPATH, EodXpath.metric_data(row+1)).get_attribute('value')
                brk_data = EodBreakdown.collect_brk_data(driver, row, metric_name, action)
                
                eod_main.daily_collection = metric_data
                eod_brk.daily_collection = brk_data
                db.session.commit()
                
                print(metric_name)
                print(metric_data)
                print(brk_data)
                print()
                
            if metric_name == 'No show #':
                metric_data = driver.find_element(By.XPATH, EodXpath.metric_data(row+1)).get_attribute('value')
                brk_data = EodBreakdown.collect_brk_data(driver, row, metric_name, action)
                
                eod_main.no_show = metric_data
                eod_brk.no_show = brk_data
                db.session.commit()
                
                print(metric_name)
                print(metric_data)
                print(brk_data)
                print()
            
            if metric_name == 'Same day treatment':
                metric_data = driver.find_element(By.XPATH, EodXpath.metric_data(row+1)).get_attribute('value')
                brk_data = EodBreakdown.collect_brk_data(driver, row, metric_name, action)
                
                eod_main.same_day_tx = metric_data
                eod_brk.same_day_tx = brk_data
                db.session.commit()
                
                print(metric_name)
                print(metric_data)
                print(brk_data)
                print()
            
            if metric_name == 'Case acceptance (%)':
                metric_data = driver.find_element(By.XPATH, EodXpath.metric_data(row+1)).get_attribute('value')
                brk_data = EodBreakdown.collect_brk_data(driver, row, metric_name, action)
                
                eod_main.case_acceptance = metric_data
                eod_brk.case_acceptance = brk_data
                db.session.commit()
                
                print(metric_name)
                print(metric_data)
                print(brk_data)
                print()
                
            if metric_name == 'New Patients':
                metric_data = driver.find_element(By.XPATH, EodXpath.metric_data(row+1)).get_attribute('value')
                brk_data = EodBreakdown.collect_brk_data(driver, row, metric_name, action)
                
                eod_main.new_patient = metric_data
                eod_brk.new_patient = brk_data
                db.session.commit()
                
                print(metric_name)
                print(metric_data)
                print(brk_data)
                print()
                
            if metric_name == 'Patients w/ Missing Referral':
                metric_data = driver.find_element(By.XPATH, EodXpath.metric_data(row+1)).get_attribute('value')
                brk_data = EodBreakdown.collect_brk_data(driver, row, metric_name, action)
                
                eod_main.pts_miss_referral = metric_data
                eod_brk.pts_miss_referral = brk_data
                db.session.commit()
                
                print(metric_name)
                print(metric_data)
                print(brk_data)
                print()
                
            if metric_name == 'Hygiene reappointment':
                metric_data = driver.find_element(By.XPATH, EodXpath.metric_data(row+1)).get_attribute('value')
                brk_data = EodBreakdown.collect_brk_data(driver, row, metric_name, action)
                
                eod_main.hyg_reappt = metric_data
                eod_brk.hyg_reappt = brk_data
                db.session.commit()
                
                print(metric_name)
                print(metric_data)
                print(brk_data)
                print()

                
                
    def collect_brk_data(driver, row, metric_name, action):
        #Move to Metric location
        move_to_metric = driver.find_element(By.XPATH, EodXpath.metric_name(row+1))
        action.move_to_element(move_to_metric).perform()
        
        open_modal = driver.find_element(By.XPATH, EodXpath.modal(row+1, metric_name)).click()
        brk = ''
        time.sleep(1)
        if metric_name == 'PT portion collections % today collected':
            brk_data = driver.find_element(By.XPATH, EodXpath.pt_portion_col_brk(driver)).text
        
        if metric_name == 'Adjustments' or metric_name == 'Total adjustment':
            brk_data = driver.find_element(By.XPATH, EodXpath.adjustments_brk(driver)).text
            
        if metric_name == 'Collection' or metric_name == 'Total collection':
            brk_data = driver.find_element(By.XPATH, EodXpath.total_collection_brk(driver)).text
            
        if metric_name == 'Daily collections':
            brk_data = driver.find_element(By.XPATH, EodXpath.daily_collection_brk(driver)).text
            
        if metric_name == 'No show #':
            brk_data = driver.find_element(By.XPATH, EodXpath.no_show_brk(driver)).text
        
        if metric_name == 'Same day treatment':
            brk_data = driver.find_element(By.XPATH, EodXpath.same_day_tx(driver)).text
            
        if metric_name == 'Case acceptance (%)':
            brk_data = driver.find_element(By.XPATH, EodXpath.case_acceptance(driver)).text
            
        if metric_name == 'New Patients':
           brk_data = EodXpath.new_patient(driver)
            
        if metric_name == 'Patients w/ Missing Referral':
            brk_data = EodXpath.pts_miss_referral(driver)
            
        if metric_name == 'Hygiene reappointment':
            brk_data = driver.find_element(By.XPATH, EodXpath.hyg_reappt(driver)).text
        
        close_modal = driver.find_element(By.XPATH, EodXpath.close_modal(driver)).click()
        
        return brk_data
            
            
            
        
        

