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
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from Project.Controller.Mh_Controller.Mh_xpath import MHXpath
from Project.Controller.Global_Controller.Single_date_picker import SinglePicker
from Project.models import MhBreakdown
from Project.models import MhMain
from Project import db


class MornigHuddleBreakdown:
    
    def Main_test(driver, test_date, test_code):
        
        wait = WebDriverWait(driver, 60)
        loader = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/main/div[1]/div/div/div/div[4]/button')))
        driver.implicitly_wait(3)
        action =  ActionChains(driver)
        
        # SinglePicker.MH_DatePicker(driver, test_date)
        # update = driver.find_element(By.XPATH, MHXpath.update_btn).click()
        time.sleep(3)
        
        ytr_counter = driver.find_elements(By.XPATH, MHXpath.ytr_counter)
        ytr_counter = len(ytr_counter)
        tdy_counter = driver.find_elements(By.XPATH, MHXpath.tdy_counter)
        tdy_counter = len(tdy_counter)
        tmw_counter = driver.find_elements(By.XPATH, MHXpath.tmw_counter)
        tmw_counter = len(tmw_counter)
        
        value = ''
        
        #Inializing Database
        mh_main = MhMain(
            user_id = current_user.id,
            test_code = test_code,
        )
        db.session.add(mh_main)
        db.session.commit()
        
        mh_brk = MhBreakdown(
            user_id = current_user.id,
            test_code = test_code,
        )
        db.session.add(mh_brk)
        db.session.commit()
        
        for row in range(ytr_counter):
            metric_name = driver.find_element(By.XPATH, MHXpath.ytr_name(row+1)).text
            
            if metric_name == "Yesterday's Production (gross)":
                value = driver.find_element(By.XPATH, MHXpath.ytr_value(row+1)).get_attribute('value')
                brk = MornigHuddleBreakdown.ytr_brk(driver, row)
                
                mh_main = MhMain.query.filter_by(test_code=test_code).first()
                mh_brk = MhBreakdown.query.filter_by(test_code=test_code).first()
                mh_main.ytr_gross_prod = value
                mh_brk.ytr_gross_prod = value
                db.session.commit()
                
                print('--------------------------------------------------------------------')
                print(metric_name+': '+value)
                print('Breakdown: '+str(brk))
                print('--------------------------------------------------------------------')
            
                
            if metric_name == "Goal":
                value = driver.find_element(By.XPATH, MHXpath.ytr_value(row+1)).get_attribute('value')
                
                mh_main = MhMain.query.filter_by(test_code=test_code).first()
                mh_main.ytr_goal = value
                db.session.commit()
                
                print(metric_name+': '+value)
                
            if metric_name == "Yesterday's Production (net)":
                value = driver.find_element(By.XPATH, MHXpath.ytr_value(row+1)).get_attribute('value')
                brk = MornigHuddleBreakdown.ytr_brk(driver, row)
                
                mh_main = MhMain.query.filter_by(test_code=test_code).first()
                mh_brk = MhBreakdown.query.filter_by(test_code=test_code).first()
                mh_main.ytr_net_prod = value
                mh_brk.ytr_net_prod = value
                db.session.commit()
                
                print('--------------------------------------------------------------------')
                print(metric_name+': '+value)
                print('Breakdown: '+str(brk))
                print('--------------------------------------------------------------------')
            
            if metric_name == "Yesterday's Collection":
                value = driver.find_element(By.XPATH, MHXpath.ytr_value(row+1)).get_attribute('value')
                brk = MornigHuddleBreakdown.ytr_brk(driver, row)
                
                mh_main = MhMain.query.filter_by(test_code=test_code).first()
                mh_brk = MhBreakdown.query.filter_by(test_code=test_code).first()
                mh_main.ytr_collection = value
                mh_brk.ytr_collection = value
                db.session.commit()
                
                print(metric_name+': '+value)
                print('Breakdown: '+str(brk))
                print('--------------------------------------------------------------------')
            
                
            if metric_name == "Collection (%)":
                value = driver.find_element(By.XPATH, MHXpath.ytr_value(row+1)).get_attribute('value')
                brk = MornigHuddleBreakdown.ytr_brk(driver, row)
                
                mh_main = MhMain.query.filter_by(test_code=test_code).first()
                mh_brk = MhBreakdown.query.filter_by(test_code=test_code).first()
                mh_main.ytr_collection = value
                mh_brk.ytr_collection = value
                db.session.commit()
                
                print(metric_name+': '+value)
                print('Breakdown: '+str(brk))
                print('--------------------------------------------------------------------')
            
                
            if metric_name == "Patient Co-pay Collection (%)":
                value = driver.find_element(By.XPATH, MHXpath.ytr_value(row+1)).get_attribute('value')
                brk = MornigHuddleBreakdown.ytr_brk(driver, row)
                
                mh_main = MhMain.query.filter_by(test_code=test_code).first()
                mh_brk = MhBreakdown.query.filter_by(test_code=test_code).first()
                mh_main.ytr_copay = value
                mh_brk.ytr_copay = value
                db.session.commit()
                
                print(metric_name+': '+value)
                print('Breakdown: '+str(brk))
                print('--------------------------------------------------------------------')
            
                
            if metric_name == "Production Per Patient":
                value = driver.find_element(By.XPATH, MHXpath.ytr_value(row+1)).get_attribute('value')
                brk = MornigHuddleBreakdown.ytr_brk(driver, row)
                
                mh_main = MhMain.query.filter_by(test_code=test_code).first()
                mh_brk = MhBreakdown.query.filter_by(test_code=test_code).first()
                mh_main.ytr_prod_per_patient = value
                mh_brk.ytr_prod_per_patient = value
                db.session.commit()
                
                print(metric_name+': '+value)
                print('Breakdown: '+str(brk))
                print('--------------------------------------------------------------------')
                
            if metric_name == "New Patients (Actual)":
                value = driver.find_element(By.XPATH, MHXpath.ytr_value(row+1)).get_attribute('value')
                brk = MornigHuddleBreakdown.ytr_brk(driver, row)
                
                mh_main = MhMain.query.filter_by(test_code=test_code).first()
                mh_brk = MhBreakdown.query.filter_by(test_code=test_code).first()
                mh_main.ytr_npt = value
                mh_brk.ytr_npt = value
                db.session.commit()
                
                print(metric_name+': '+value)
                print('Breakdown: '+str(brk))
                print('--------------------------------------------------------------------')
                
            if metric_name == "Care Progress Rate (%)":
                value = driver.find_element(By.XPATH, MHXpath.ytr_value(row+1)).get_attribute('value')
                print(metric_name+': '+value)
                
                mh_main = MhMain.query.filter_by(test_code=test_code).first()
                mh_brk = MhBreakdown.query.filter_by(test_code=test_code).first()
                mh_main.ytr_care_progress = value
                mh_brk.ytr_care_progress = value
                db.session.commit()
                
                print('Breakdown: ')
                print('--------------------------------------------------------------------')
                
            if metric_name == "Treatment acceptance (%)":
                value = driver.find_element(By.XPATH, MHXpath.ytr_value(row+1)).get_attribute('value')
                brk = MornigHuddleBreakdown.ytr_brk(driver, row)
                
                mh_main = MhMain.query.filter_by(test_code=test_code).first()
                mh_brk = MhBreakdown.query.filter_by(test_code=test_code).first()
                mh_main.ytr_tx_acceptance = value
                mh_brk.ytr_tx_acceptance = value
                db.session.commit()
                
                print(metric_name+': '+value)
                print('Breakdown: '+str(brk))
                print('--------------------------------------------------------------------')
            
            if metric_name == "Presented":
                value = driver.find_element(By.XPATH, MHXpath.ytr_value(row+1)).get_attribute('value')
                brk = MornigHuddleBreakdown.ytr_brk(driver, row)
                
                mh_main = MhMain.query.filter_by(test_code=test_code).first()
                mh_brk = MhBreakdown.query.filter_by(test_code=test_code).first()
                mh_main.ytr_tx_presented = value
                mh_brk.ytr_tx_presented = value
                db.session.commit()
                
                print(metric_name+': '+value)
                print('Breakdown: '+str(brk))
                print('--------------------------------------------------------------------')
                
            if metric_name == "Completed":
                value = driver.find_element(By.XPATH, MHXpath.ytr_value(row+1)).get_attribute('value')
                brk = MornigHuddleBreakdown.ytr_brk(driver, row)
                
                mh_main = MhMain.query.filter_by(test_code=test_code).first()
                mh_brk = MhBreakdown.query.filter_by(test_code=test_code).first()
                mh_main.ytr_tx_completed = value
                mh_brk.ytr_tx_completed = value
                db.session.commit()
                
                print(metric_name+': '+value)
                print('Breakdown: '+str(brk))
                print('--------------------------------------------------------------------')
                
            if metric_name == "Scheduled":
                value = driver.find_element(By.XPATH, MHXpath.ytr_value(row+1)).get_attribute('value')
                brk = MornigHuddleBreakdown.ytr_brk(driver, row)
                
                mh_main = MhMain.query.filter_by(test_code=test_code).first()
                mh_brk = MhBreakdown.query.filter_by(test_code=test_code).first()
                mh_main.ytr_tx_sched = value
                mh_brk.ytr_tx_sched = value
                db.session.commit()
                
                print(metric_name+': '+value)
                print('Breakdown: '+str(brk))
                print('--------------------------------------------------------------------')
                
            if metric_name == "Unscheduled":
                value = driver.find_element(By.XPATH, MHXpath.ytr_value(row+1)).get_attribute('value')
                brk = MornigHuddleBreakdown.ytr_brk(driver, row)
                
                mh_main = MhMain.query.filter_by(test_code=test_code).first()
                mh_brk = MhBreakdown.query.filter_by(test_code=test_code).first()
                mh_main.ytr_tx_unsched = value
                mh_brk.ytr_tx_unsched = value
                db.session.commit()
                
                print(metric_name+': '+value)
                print('Breakdown: '+str(brk))
                print('--------------------------------------------------------------------')
                
            if metric_name == "Hygiene Production":
                value = driver.find_element(By.XPATH, MHXpath.ytr_value(row+1)).get_attribute('value')
                brk = MornigHuddleBreakdown.ytr_brk(driver, row)
                
                mh_main = MhMain.query.filter_by(test_code=test_code).first()
                mh_brk = MhBreakdown.query.filter_by(test_code=test_code).first()
                mh_main.ytr_hyg_prod = value
                mh_brk.ytr_hyg_prod = value
                db.session.commit()
                
                print(metric_name+': '+value)
                print('Breakdown: '+str(brk))
                print('--------------------------------------------------------------------')
                
            if metric_name == "Hygiene Reappoint (%)":
                value = driver.find_element(By.XPATH, MHXpath.ytr_value(row+1)).get_attribute('value')
                brk = MornigHuddleBreakdown.ytr_brk(driver, row)
                
                mh_main = MhMain.query.filter_by(test_code=test_code).first()
                mh_brk = MhBreakdown.query.filter_by(test_code=test_code).first()
                mh_main.ytr_hyg_reappt = value
                mh_brk.ytr_hyg_reappt = value
                db.session.commit()
                
                print(metric_name+': '+value)
                print('Breakdown: '+str(brk))
                print('--------------------------------------------------------------------')
                
            if metric_name == "Scheduled":
                value = driver.find_element(By.XPATH, MHXpath.ytr_value(row+1)).get_attribute('value')
                brk = MornigHuddleBreakdown.ytr_brk(driver, row)
                
                mh_main = MhMain.query.filter_by(test_code=test_code).first()
                mh_brk = MhBreakdown.query.filter_by(test_code=test_code).first()
                mh_main.ytr_hyg_sched = value
                mh_brk.ytr_hyg_sched = value
                db.session.commit()
                
                print(metric_name+': '+value)
                print('Breakdown: '+str(brk))
                print('--------------------------------------------------------------------')
                
            if metric_name == "Not Scheduled":
                value = driver.find_element(By.XPATH, MHXpath.ytr_value(row+1)).get_attribute('value')
                brk = MornigHuddleBreakdown.ytr_brk(driver, row)
                
                mh_main = MhMain.query.filter_by(test_code=test_code).first()
                mh_brk = MhBreakdown.query.filter_by(test_code=test_code).first()
                mh_main.ytr_not_sched = value
                mh_brk.ytr_not_sched = value
                db.session.commit()
                
                print(metric_name+': '+value)
                print('Breakdown: '+str(brk))
                print('--------------------------------------------------------------------')
                
            if metric_name == "Broken appointments":
                value = driver.find_element(By.XPATH, MHXpath.ytr_value(row+1)).get_attribute('value')
                brk = MornigHuddleBreakdown.ytr_brk(driver, row)
                
                mh_main = MhMain.query.filter_by(test_code=test_code).first()
                mh_brk = MhBreakdown.query.filter_by(test_code=test_code).first()
                mh_main.ytr_broken_appt = value
                mh_brk.ytr_broken_appt = value
                db.session.commit()
                
                print(metric_name+': '+value)
                print('Breakdown: '+str(brk))
                print('--------------------------------------------------------------------')
                
            if metric_name == "Unscheduled Broken Appointments":
                value = driver.find_element(By.XPATH, MHXpath.ytr_value(row+1)).get_attribute('value')
                brk = MornigHuddleBreakdown.ytr_brk(driver, row)
                
                mh_main = MhMain.query.filter_by(test_code=test_code).first()
                mh_brk = MhBreakdown.query.filter_by(test_code=test_code).first()
                mh_main.ytr_unshed_broken_appt = value
                mh_brk.ytr_unshed_broken_appt = value
                db.session.commit()
                
                print(metric_name+': '+value)
                print('Breakdown: '+str(brk))
                print('--------------------------------------------------------------------')
                
            if metric_name == "New Pts not rescheduled":
                value = driver.find_element(By.XPATH, MHXpath.ytr_value(row+1)).get_attribute('value')
                brk = MornigHuddleBreakdown.ytr_brk(driver, row)
                
                mh_main = MhMain.query.filter_by(test_code=test_code).first()
                mh_brk = MhBreakdown.query.filter_by(test_code=test_code).first()
                mh_main.ytr_npt_not_resched = value
                mh_brk.ytr_npt_not_resched = value
                db.session.commit()
                
                print(metric_name+': '+value)
                print('Breakdown: '+str(brk))
                print('--------------------------------------------------------------------')
                
            if metric_name == "Existing Pts not rescheduled":
                value = driver.find_element(By.XPATH, MHXpath.ytr_value(row+1)).get_attribute('value')
                brk = MornigHuddleBreakdown.ytr_brk(driver, row)
                
                mh_main = MhMain.query.filter_by(test_code=test_code).first()
                mh_brk = MhBreakdown.query.filter_by(test_code=test_code).first()
                mh_main.ytr_pts_not_resched = value
                mh_brk.ytr_pts_not_resched = value
                db.session.commit()
                
                print(metric_name+': '+value)
                print('Breakdown: '+str(brk))
                print('--------------------------------------------------------------------')
                
        title = driver.find_element(By.XPATH, '/html/body/div[1]/main/div[1]/div/h2') 
        action.move_to_element(title).perform()  
                   
        for row in range(tdy_counter):
            metric_name = driver.find_element(By.XPATH, MHXpath.tdy_name(row+1)).text
            
            if metric_name == "Today's Scheduled Production":
                value = driver.find_element(By.XPATH, MHXpath.tdy_value(row+1)).get_attribute('value')
                
                mh_main = MhMain.query.filter_by(test_code=test_code).first()
                mh_main.tdy_sched_prod = value
                db.session.commit()
                
                print(metric_name+': '+value)
                print('--------------------------------------------------------------------')
                
            if metric_name == "Goal":
                value = driver.find_element(By.XPATH, MHXpath.tdy_value(row+1)).get_attribute('value')
                
                mh_main = MhMain.query.filter_by(test_code=test_code).first()
                mh_main.tdy_goal = value
                db.session.commit()
                
                print(metric_name+': '+value)
                print('--------------------------------------------------------------------')
                
            if metric_name == "New Patients (Actual)":
                value = driver.find_element(By.XPATH, MHXpath.tdy_value(row+1)).get_attribute('value')
                brk = MornigHuddleBreakdown.tdy_brk(driver, row)
                
                mh_main = MhMain.query.filter_by(test_code=test_code).first()
                mh_brk = MhBreakdown.query.filter_by(test_code=test_code).first()
                mh_main.tdy_npt_actual = value
                mh_brk.tdy_npt_actual = value
                db.session.commit()
                
                print(metric_name+': '+value)
                print('Breakdown: '+str(brk))
                print('--------------------------------------------------------------------')
                
                 
            if metric_name == "New Patients (Scheduled)":
                value = driver.find_element(By.XPATH, MHXpath.tdy_value(row+1)).get_attribute('value')
                brk = MornigHuddleBreakdown.tdy_brk(driver, row)
                
                mh_main = MhMain.query.filter_by(test_code=test_code).first()
                mh_brk = MhBreakdown.query.filter_by(test_code=test_code).first()
                mh_main.tdy_npt_sched = value
                mh_brk.tdy_npt_sched = value
                db.session.commit()
                
                print(metric_name+': '+value)
                print('Breakdown: '+str(brk))
                print('--------------------------------------------------------------------')
                
                 
            if metric_name == "Hygiene Production (Scheduled)":
                value = driver.find_element(By.XPATH, MHXpath.tdy_value(row+1)).get_attribute('value')
                brk = MornigHuddleBreakdown.tdy_brk(driver, row)
                
                mh_main = MhMain.query.filter_by(test_code=test_code).first()
                mh_brk = MhBreakdown.query.filter_by(test_code=test_code).first()
                mh_main.tdy_hyg_prod_sched = value
                mh_brk.tdy_hyg_prod_sched = value
                db.session.commit()
                
                print(metric_name+': '+value)
                print('Breakdown: '+str(brk))
                print('--------------------------------------------------------------------')
                
                 
            if metric_name == "Hygiene Production (Actual)":
                value = driver.find_element(By.XPATH, MHXpath.tdy_value(row+1)).get_attribute('value')
                brk = MornigHuddleBreakdown.tdy_brk(driver, row)
                
                mh_main = MhMain.query.filter_by(test_code=test_code).first()
                mh_brk = MhBreakdown.query.filter_by(test_code=test_code).first()
                mh_main.tdy_hyg_prod_actual = value
                mh_brk.tdy_hyg_prod_actual = value
                db.session.commit()
                
                print(metric_name+': '+value)
                print('Breakdown: '+str(brk))
                print('--------------------------------------------------------------------')
                
                 
            if metric_name == "Unscheduled Treatment":
                value = driver.find_element(By.XPATH, MHXpath.tdy_value(row+1)).get_attribute('value')
                brk = MornigHuddleBreakdown.tdy_brk(driver, row)
                
                mh_main = MhMain.query.filter_by(test_code=test_code).first()
                mh_brk = MhBreakdown.query.filter_by(test_code=test_code).first()
                mh_main.tdy_unsched_tx = value
                mh_brk.tdy_unsched_tx = value
                db.session.commit()
                
                print(metric_name+': '+value)
                print('Breakdown: '+str(brk))
                print('--------------------------------------------------------------------')
                
                 
            if metric_name == "Unscheduled Family Members":
                value = driver.find_element(By.XPATH, MHXpath.tdy_value(row+1)).get_attribute('value')
                brk = MornigHuddleBreakdown.tdy_brk(driver, row)
                
                mh_main = MhMain.query.filter_by(test_code=test_code).first()
                mh_brk = MhBreakdown.query.filter_by(test_code=test_code).first()
                mh_main.tdy_unsched_family_members = value
                mh_brk.tdy_unsched_family_members = value
                db.session.commit()
                
                print(metric_name+': '+value)
                print('Breakdown: '+str(brk))
                print('--------------------------------------------------------------------')
                
                 
            if metric_name == "Unscheduled Hygiene":
                value = driver.find_element(By.XPATH, MHXpath.tdy_value(row+1)).get_attribute('value')
                brk = MornigHuddleBreakdown.tdy_brk(driver, row)
                
                mh_main = MhMain.query.filter_by(test_code=test_code).first()
                mh_brk = MhBreakdown.query.filter_by(test_code=test_code).first()
                mh_main.tdy_unsched_hyg = value
                mh_brk.tdy_unsched_hyg = value
                db.session.commit()
                
                print(metric_name+': '+value)
                print('Breakdown: '+str(brk))  
                print('--------------------------------------------------------------------')
                
                 
            if metric_name == "Patient Birthdays":
                value = driver.find_element(By.XPATH, MHXpath.tdy_value(row+1)).get_attribute('value')
                brk = MornigHuddleBreakdown.tdy_brk(driver, row)
                
                mh_main = MhMain.query.filter_by(test_code=test_code).first()
                mh_brk = MhBreakdown.query.filter_by(test_code=test_code).first()
                mh_main.tdy_patient_bday = value
                mh_brk.tdy_patient_bday = value
                db.session.commit()
                
                print(metric_name+': '+value)
                print('Breakdown: '+str(brk))  
                print('--------------------------------------------------------------------')
                
                 
            if metric_name == "Past Due AR":
                value = driver.find_element(By.XPATH, MHXpath.tdy_value(row+1)).get_attribute('value')
                brk = MornigHuddleBreakdown.tdy_brk(driver, row)
                
                mh_main = MhMain.query.filter_by(test_code=test_code).first()
                mh_brk = MhBreakdown.query.filter_by(test_code=test_code).first()
                mh_main.tdy_past_due_ar = value
                mh_brk.tdy_past_due_ar = value
                db.session.commit()
                
                print(metric_name+': '+value)
                print('Breakdown: '+str(brk))  
                print('--------------------------------------------------------------------')
                 
            if metric_name == "Due for BWX":
                value = driver.find_element(By.XPATH, MHXpath.tdy_value(row+1)).get_attribute('value')
                brk = MornigHuddleBreakdown.tdy_brk(driver, row)
                
                mh_main = MhMain.query.filter_by(test_code=test_code).first()
                mh_brk = MhBreakdown.query.filter_by(test_code=test_code).first()
                mh_main.tdy_due_bwx = value
                mh_brk.tdy_due_bwx = value
                db.session.commit()
                
                print(metric_name+': '+value)
                print('Breakdown: '+str(brk))  
                print('--------------------------------------------------------------------')
            
            if metric_name == "Due for FMX":
                value = driver.find_element(By.XPATH, MHXpath.tdy_value(row+1)).get_attribute('value')
                brk = MornigHuddleBreakdown.tdy_brk(driver, row)
                
                mh_main = MhMain.query.filter_by(test_code=test_code).first()
                mh_brk = MhBreakdown.query.filter_by(test_code=test_code).first()
                mh_main.tdy_due_fmx = value
                mh_brk.tdy_due_fmx = value
                db.session.commit()
                
                print(metric_name+': '+value)
                print('Breakdown: '+str(brk))  
                print('--------------------------------------------------------------------')
         
        title = driver.find_element(By.XPATH, '/html/body/div[1]/main/div[1]/div/h2') 
        action.move_to_element(title).perform()  
        
        for row in range(tmw_counter):
            metric_name = driver.find_element(By.XPATH, MHXpath.tmw_name(row+1)).text  
            
            if metric_name == "Tomorrow's Scheduled Production":
                value = driver.find_element(By.XPATH, MHXpath.tmw_value(row+1)).get_attribute('value')
                
                mh_main = MhMain.query.filter_by(test_code=test_code).first()
                mh_main.tmw_sched_prod = value
                db.session.commit()
                
                print(metric_name+': '+value)
                print('--------------------------------------------------------------------')
                
            if metric_name == "Goal":
                value = driver.find_element(By.XPATH, MHXpath.tmw_value(row+1)).get_attribute('value')
                
                mh_main = MhMain.query.filter_by(test_code=test_code).first()
                mh_main.tmw_goal = value
                db.session.commit()
                
                print(metric_name+': '+value)
                print('--------------------------------------------------------------------')
                
            if metric_name == "New Patients (Scheduled)":
                value = driver.find_element(By.XPATH, MHXpath.tmw_value(row+1)).get_attribute('value')
                brk = MornigHuddleBreakdown.tmw_brk(driver, row)
                
                mh_main = MhMain.query.filter_by(test_code=test_code).first()
                mh_brk = MhBreakdown.query.filter_by(test_code=test_code).first()
                mh_main.tmw_npt_sched = value
                mh_brk.tmw_npt_sched = value
                db.session.commit()
                
                print(metric_name+': '+value)
                print('Breakdown: '+str(brk))
                print('--------------------------------------------------------------------')
        
            if metric_name == "Hygiene Production (Scheduled)":
                value = driver.find_element(By.XPATH, MHXpath.tmw_value(row+1)).get_attribute('value')
                brk = MornigHuddleBreakdown.tmw_brk(driver, row)
                
                mh_main = MhMain.query.filter_by(test_code=test_code).first()
                mh_brk = MhBreakdown.query.filter_by(test_code=test_code).first()
                mh_main.tmw_hyg_prod_sched = value
                mh_brk.tmw_hyg_prod_sched = value
                db.session.commit()
                
                print(metric_name+': '+value)
                print('Breakdown: '+str(brk))
                print('--------------------------------------------------------------------')
                
            if metric_name == "Unscheduled Treatment":
                value = driver.find_element(By.XPATH, MHXpath.tmw_value(row+1)).get_attribute('value')
                brk = MornigHuddleBreakdown.tmw_brk(driver, row)
                
                mh_main = MhMain.query.filter_by(test_code=test_code).first()
                mh_brk = MhBreakdown.query.filter_by(test_code=test_code).first()
                mh_main.tmw_unsched_tx = value
                mh_brk.tmw_unsched_tx = value
                db.session.commit()
                
                print(metric_name+': '+value)
                print('Breakdown: '+str(brk))
                print('--------------------------------------------------------------------')
            
            if metric_name == "Unscheduled Family Members":
                value = driver.find_element(By.XPATH, MHXpath.tmw_value(row+1)).get_attribute('value')
                brk = MornigHuddleBreakdown.tmw_brk(driver, row)
                
                mh_main = MhMain.query.filter_by(test_code=test_code).first()
                mh_brk = MhBreakdown.query.filter_by(test_code=test_code).first()
                mh_main.tmw_unsched_family_members = value
                mh_brk.tmw_unsched_family_members = value
                db.session.commit()
                
                print(metric_name+': '+value)
                print('Breakdown: '+str(brk))
                print('--------------------------------------------------------------------')
            
            if metric_name == "Unscheduled Hygiene":
                value = driver.find_element(By.XPATH, MHXpath.tmw_value(row+1)).get_attribute('value')
                brk = MornigHuddleBreakdown.tmw_brk(driver, row)
                
                mh_main = MhMain.query.filter_by(test_code=test_code).first()
                mh_brk = MhBreakdown.query.filter_by(test_code=test_code).first()
                mh_main.tmw_unsched_hyg = value
                mh_brk.tmw_unsched_hyg = value
                db.session.commit()
                
                print(metric_name+': '+value)
                print('Breakdown: '+str(brk))
                print('--------------------------------------------------------------------')
                
            if metric_name == "Due for BWX":
                value = driver.find_element(By.XPATH, MHXpath.tmw_value(row+1)).get_attribute('value')
                brk = MornigHuddleBreakdown.tmw_brk(driver, row)
                
                mh_main = MhMain.query.filter_by(test_code=test_code).first()
                mh_brk = MhBreakdown.query.filter_by(test_code=test_code).first()
                mh_main.tmw_due_bwx = value
                mh_brk.tmw_due_bwx = value
                db.session.commit()
                
                print(metric_name+': '+value)
                print('Breakdown: '+str(brk))
                print('--------------------------------------------------------------------')
                
            if metric_name == "Due for FMX":
                value = driver.find_element(By.XPATH, MHXpath.tmw_value(row+1)).get_attribute('value')
                brk = MornigHuddleBreakdown.tmw_brk(driver, row)
                
                mh_main = MhMain.query.filter_by(test_code=test_code).first()
                mh_brk = MhBreakdown.query.filter_by(test_code=test_code).first()
                mh_main.twm_due_fmx = value
                mh_brk.twm_due_fmx = value
                db.session.commit()
                
                print(metric_name+': '+value)
                print('Breakdown: '+str(brk))
                print('--------------------------------------------------------------------')
        
        
    def ytr_brk(driver, row):
        brk = driver.find_element(By.XPATH, MHXpath.yrt_breakdown(row+1))
        brk.click()
        
        brk_data = driver.find_elements(By.XPATH, '/html/body/div[1]/main/div[4]/div/div/div/div[2]/section/div/div/div[2]/div/div[1]/table/tr/td')
        brk_data = len(brk_data)
        value = 'N\A'
        
        if brk_data != 0:
            column = driver.find_elements(By.XPATH, MHXpath.brk_column_counter)
            column = len(column)
            value = driver.find_element(By.XPATH, MHXpath.brk_value(column)).text
        else:
            value = 0
        
        driver.find_element(By.XPATH, MHXpath.modal_exit).click()
        return value
    
    def tdy_brk(driver, row):
        brk = driver.find_element(By.XPATH, MHXpath.tdy_brk_btn(row+1))
        brk.click()
        
        brk_data = driver.find_elements(By.XPATH, '/html/body/div[1]/main/div[4]/div/div/div/div[2]/section/div/div/div[2]/div/div[1]/table/tr/td')
        brk_data = len(brk_data)
        value = 'N\A'
        
        if brk_data != 0:
            column = driver.find_elements(By.XPATH, MHXpath.brk_column_counter)
            column = len(column)
            value = driver.find_element(By.XPATH, MHXpath.brk_value(column)).text
        else:
            value = 0
        
        driver.find_element(By.XPATH, MHXpath.modal_exit).click()
        return value
    
    def tmw_brk(driver, row):
        brk = driver.find_element(By.XPATH, MHXpath.tmw_brk_btn(row+1))
        brk.click()
        
        brk_data = driver.find_elements(By.XPATH, '/html/body/div[1]/main/div[4]/div/div/div/div[2]/section/div/div/div[2]/div/div[1]/table/tr/td')
        brk_data = len(brk_data)
        value = 'N\A'
        
        if brk_data != 0:
            column = driver.find_elements(By.XPATH, MHXpath.brk_column_counter)
            column = len(column)
            value = driver.find_element(By.XPATH, MHXpath.brk_value(column)).text
        else:
            value = 0
        
        driver.find_element(By.XPATH, MHXpath.modal_exit).click()
        return value
    
    
        
        