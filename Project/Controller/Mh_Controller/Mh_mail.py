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
from selenium.webdriver.common.keys import Keys
# from Project.models import MhMail

from Project.Controller.Mh_Controller.Mh_xpath import MailTestXpath

from Project import db

class MornigHuddleMail:
    
    def main_test(driver, email_username, mail_password, test_code):
        wait = WebDriverWait(driver, 60)
        loader = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/main/div[1]/div/div/div/div[4]/button')))
        driver.implicitly_wait(5)
        action =  ActionChains(driver)
        
        footer = driver.find_element(By.XPATH, '/html/body/div[1]/footer/div') 
        action.move_to_element(footer).perform()
        time.sleep(3)
        
        wait = WebDriverWait(driver, 60)
        loader = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/main/div[1]/div/div/div/div[4]/button')))
        
        #Steps For Sending Emails---------------------------------------------------------------------------------------------------------------------------
        driver.find_element(By.XPATH, MailTestXpath.open_mail_btn).click()
        driver.find_element(By.XPATH, MailTestXpath.mail_input).send_keys(email_username)
        action.send_keys(Keys.ENTER).perform()
        mail_subject = driver.find_element(By.XPATH, MailTestXpath.mail_subject).get_attribute('value')
        driver.find_element(By.XPATH, MailTestXpath.mail_note).send_keys('Send by Jarvis Analytics Automated QA Test')
        driver.find_element(By.XPATH, MailTestXpath.send_mail_btn).click()
        
        #Steps for Logging In in Gmail-----------------------------------------------------------------------------------------------------------------------
        driver.get('https://mail.google.com/')
        driver.find_element(By.XPATH, MailTestXpath.username_field).send_keys(email_username)
        action.send_keys(Keys.ENTER).perform()
        driver.find_element(By.XPATH, MailTestXpath.password_field).send_keys(mail_password)
        action.send_keys(Keys.ENTER).perform()
        
        
        #Steps for Opening Jarvis Mail-----------------------------------------------------------------------------------------------------------------------
        wait = WebDriverWait(driver, 60)
        loader = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[7]/div[3]/div/div[2]/div[3]/div[1]/div/div[1]/div[1]/div/div[1]/div[3]')))
        
        mail_inbox_counter = driver.find_elements(By.XPATH, MailTestXpath.mail_inbox_counter)
        mail_inbox_counter = len(mail_inbox_counter)
        print(mail_inbox_counter)
        time.sleep(5)
        
        for row in range(mail_inbox_counter):
            inbox = driver.find_element(By.XPATH, MailTestXpath.mail_inbox(row+1)).text
             
            if mail_subject == inbox:
                driver.find_element(By.XPATH, MailTestXpath.mail_inbox(row+1)).click()
                break
            else:
                print('No Inbox')
        
        time.sleep(5)
        
        mh_main = MhMail(
            user_id = current_user.id,
            test_code = test_code,
        )
        db.session.add(mh_main)
        db.session.commit()
        
        ytr_mail_counter = driver.find_elements(By.XPATH, MailTestXpath.ytr_mail_counter)
        ytr_mail_counter = len(ytr_mail_counter)
        
        print('Yesterday Mail----------------------------------------------------------------------------------------------------------------')
        for row in range(ytr_mail_counter):
            metric_name = driver.find_element(By.XPATH, MailTestXpath.ytr_mail_metric_name(row+1)).text
            
            if metric_name == "Yesterday's Production (gross)":
                value = driver.find_element(By.XPATH, MailTestXpath.ytr_mail_metric_value(row+1)).text
                print(metric_name+": "+value)
                
                mh_mail = MhMail.query.filter_by(test_code=test_code).first()
                mh_mail.ytr_gross_prod = value
                db.session.commit()
                print(metric_name+": "+value)
            
            if metric_name == "Goal":
                value = driver.find_element(By.XPATH, MailTestXpath.ytr_mail_metric_value(row+1)).text
                
                mh_mail = MhMail.query.filter_by(test_code=test_code).first()
                mh_mail.ytr_goal = value
                db.session.commit()
                print(metric_name+": "+value)
                
            if metric_name == "Yesterday's Production (net)":
                value = driver.find_element(By.XPATH, MailTestXpath.ytr_mail_metric_value(row+1)).text
                
                mh_mail = MhMail.query.filter_by(test_code=test_code).first()
                mh_mail.ytr_net_prod = value
                db.session.commit()
                print(metric_name+": "+value)
                
            if metric_name == "Yesterday's Collection":
                value = driver.find_element(By.XPATH, MailTestXpath.ytr_mail_metric_value(row+1)).text
                
                mh_mail = MhMail.query.filter_by(test_code=test_code).first()
                mh_mail.ytr_collection = value
                db.session.commit()
                print(metric_name+": "+value)
                
            if metric_name == "Collection (%)":
                value = driver.find_element(By.XPATH, MailTestXpath.ytr_mail_metric_value(row+1)).text
                
                mh_mail = MhMail.query.filter_by(test_code=test_code).first()
                mh_mail.ytr_collection_percent = value
                db.session.commit()
                print(metric_name+": "+value)
            
            if metric_name == "Patient Co-pay Collection (%)":
                value = driver.find_element(By.XPATH, MailTestXpath.ytr_mail_metric_value(row+1)).text
                
                mh_mail = MhMail.query.filter_by(test_code=test_code).first()
                mh_mail.ytr_copay = value
                db.session.commit()
                print(metric_name+": "+value)
                
            if metric_name == "Production Per Patient":
                value = driver.find_element(By.XPATH, MailTestXpath.ytr_mail_metric_value(row+1)).text
                
                mh_mail = MhMail.query.filter_by(test_code=test_code).first()
                mh_mail.ytr_prod_per_patient = value
                db.session.commit()
                print(metric_name+": "+value)
            
            if metric_name == "New Patients (Actual)":
                value = driver.find_element(By.XPATH, MailTestXpath.ytr_mail_metric_value(row+1)).text
                
                mh_mail = MhMail.query.filter_by(test_code=test_code).first()
                mh_mail.ytr_npt = value
                db.session.commit()
                print(metric_name+": "+value)
                
            if metric_name == "Care Progress Rate (%)":
                value = driver.find_element(By.XPATH, MailTestXpath.ytr_mail_metric_value(row+1)).text
                
                mh_mail = MhMail.query.filter_by(test_code=test_code).first()
                mh_mail.ytr_care_progress = value
                db.session.commit()
                print(metric_name+": "+value)
                
            if metric_name == "Treatment acceptance (%)":
                value = driver.find_element(By.XPATH, MailTestXpath.ytr_mail_metric_value(row+1)).text
                
                mh_mail = MhMail.query.filter_by(test_code=test_code).first()
                mh_mail.ytr_tx_acceptance = value
                db.session.commit()
                print(metric_name+": "+value)
                
            if metric_name == "Presented":
                value = driver.find_element(By.XPATH, MailTestXpath.ytr_mail_metric_value(row+1)).text
                
                mh_mail = MhMail.query.filter_by(test_code=test_code).first()
                mh_mail.ytr_tx_presented = value
                db.session.commit()
                print(metric_name+": "+value)
                
            if metric_name == "Completed":
                value = driver.find_element(By.XPATH, MailTestXpath.ytr_mail_metric_value(row+1)).text
                
                mh_mail = MhMail.query.filter_by(test_code=test_code).first()
                mh_mail.ytr_tx_completed = value
                db.session.commit()
                print(metric_name+": "+value)
                
            if metric_name == "Scheduled":
                value = driver.find_element(By.XPATH, MailTestXpath.ytr_mail_metric_value(row+1)).text
                
                mh_mail = MhMail.query.filter_by(test_code=test_code).first()
                mh_mail.ytr_tx_sched = value
                db.session.commit()
                print(metric_name+": "+value)
                
            if metric_name == "Unscheduled":
                value = driver.find_element(By.XPATH, MailTestXpath.ytr_mail_metric_value(row+1)).text
                
                mh_mail = MhMail.query.filter_by(test_code=test_code).first()
                mh_mail.ytr_tx_unsched = value
                db.session.commit()
                print(metric_name+": "+value)
                
            if metric_name == "Hygiene Production":
                value = driver.find_element(By.XPATH, MailTestXpath.ytr_mail_metric_value(row+1)).text
                
                mh_mail = MhMail.query.filter_by(test_code=test_code).first()
                mh_mail.ytr_hyg_prod = value
                db.session.commit()
                print(metric_name+": "+value)
                
            if metric_name == "Hygiene Reappoint (%)":
                value = driver.find_element(By.XPATH, MailTestXpath.ytr_mail_metric_value(row+1)).text
                
                mh_mail = MhMail.query.filter_by(test_code=test_code).first()
                mh_mail.ytr_hyg_reappt = value
                db.session.commit()
                print(metric_name+": "+value)
                
            if metric_name == "Scheduled":
                value = driver.find_element(By.XPATH, MailTestXpath.ytr_mail_metric_value(row+1)).text
                
                mh_mail = MhMail.query.filter_by(test_code=test_code).first()
                mh_mail.ytr_hyg_sched = value
                db.session.commit()
                print(metric_name+": "+value)
                
            if metric_name == "Not Scheduled":
                value = driver.find_element(By.XPATH, MailTestXpath.ytr_mail_metric_value(row+1)).text
                
                mh_mail = MhMail.query.filter_by(test_code=test_code).first()
                mh_mail.ytr_not_sched = value
                db.session.commit()
                print(metric_name+": "+value)
                
            if metric_name == "Broken appointments":
                value = driver.find_element(By.XPATH, MailTestXpath.ytr_mail_metric_value(row+1)).text
                
                mh_mail = MhMail.query.filter_by(test_code=test_code).first()
                mh_mail.ytr_broken_appt = value
                db.session.commit()
                print(metric_name+": "+value)
                
            if metric_name == "Unscheduled Broken Appointments":
                value = driver.find_element(By.XPATH, MailTestXpath.ytr_mail_metric_value(row+1)).text
                
                mh_mail = MhMail.query.filter_by(test_code=test_code).first()
                mh_mail.ytr_unshed_broken_appt = value
                db.session.commit()
                print(metric_name+": "+value)
                
            if metric_name == "New Pts not rescheduled":
                value = driver.find_element(By.XPATH, MailTestXpath.ytr_mail_metric_value(row+1)).text
                
                mh_mail = MhMail.query.filter_by(test_code=test_code).first()
                mh_mail.ytr_npt_not_resched = value
                db.session.commit()
                print(metric_name+": "+value)
                
            if metric_name == "Existing Pts not rescheduled":
                value = driver.find_element(By.XPATH, MailTestXpath.ytr_mail_metric_value(row+1)).text
                
                mh_mail = MhMail.query.filter_by(test_code=test_code).first()
                mh_mail.ytr_pts_not_resched = value
                db.session.commit()
                print(metric_name+": "+value)
            
        tdy_mail_counter = driver.find_elements(By.XPATH, MailTestXpath.tdy_mail_counter)
        tdy_mail_counter = len(tdy_mail_counter)
        
        
        print('Today Mail--------------------------------------------------------------------------------------------------------------------')
        for row in range(tdy_mail_counter):
            metric_name = driver.find_element(By.XPATH, MailTestXpath.tdy_mail_metric_name(row+1)).text
            
            if metric_name == "Today's Scheduled Production":
                value = driver.find_element(By.XPATH, MailTestXpath.tdy_mail_metric_value(row+1)).text
                
                mh_mail = MhMail.query.filter_by(test_code=test_code).first()
                mh_mail.tdy_sched_prod = value
                db.session.commit()
                print(metric_name+": "+value)
                
            if metric_name == "Goal":
                value = driver.find_element(By.XPATH, MailTestXpath.tdy_mail_metric_value(row+1)).text
                
                mh_mail = MhMail.query.filter_by(test_code=test_code).first()
                mh_mail.tdy_goal = value
                db.session.commit()
                print(metric_name+": "+value)
                
            if metric_name == "New Patients (Actual)":
                value = driver.find_element(By.XPATH, MailTestXpath.tdy_mail_metric_value(row+1)).text
                
                mh_mail = MhMail.query.filter_by(test_code=test_code).first()
                mh_mail.tdy_npt_actual = value
                db.session.commit()
                print(metric_name+": "+value)
                
            if metric_name == "New Patients (Scheduled)":
                value = driver.find_element(By.XPATH, MailTestXpath.tdy_mail_metric_value(row+1)).text
                
                mh_mail = MhMail.query.filter_by(test_code=test_code).first()
                mh_mail.tdy_npt_sched = value
                db.session.commit()
                print(metric_name+": "+value)
                
            if metric_name == "Hygiene Production (Scheduled)":
                value = driver.find_element(By.XPATH, MailTestXpath.tdy_mail_metric_value(row+1)).text
                
                mh_mail = MhMail.query.filter_by(test_code=test_code).first()
                mh_mail.tdy_hyg_prod_sched = value
                db.session.commit()
                print(metric_name+": "+value)
                
            if metric_name == "Hygiene Production (Actual)":
                value = driver.find_element(By.XPATH, MailTestXpath.tdy_mail_metric_value(row+1)).text
                
                mh_mail = MhMail.query.filter_by(test_code=test_code).first()
                mh_mail.tdy_hyg_prod_actual = value
                db.session.commit()
                print(metric_name+": "+value)
                
            if metric_name == "Unscheduled Treatment":
                value = driver.find_element(By.XPATH, MailTestXpath.tdy_mail_metric_value(row+1)).text
                
                mh_mail = MhMail.query.filter_by(test_code=test_code).first()
                mh_mail.tdy_unsched_tx = value
                db.session.commit()
                print(metric_name+": "+value)
                
            if metric_name == "Unscheduled Family Members":
                value = driver.find_element(By.XPATH, MailTestXpath.tdy_mail_metric_value(row+1)).text
                
                mh_mail = MhMail.query.filter_by(test_code=test_code).first()
                mh_mail.tdy_unsched_family_members = value
                db.session.commit()
                print(metric_name+": "+value)
                
            if metric_name == "Unscheduled Hygiene":
                value = driver.find_element(By.XPATH, MailTestXpath.tdy_mail_metric_value(row+1)).text
                
                mh_mail = MhMail.query.filter_by(test_code=test_code).first()
                mh_mail.tdy_unsched_hyg = value
                db.session.commit()
                print(metric_name+": "+value)
                
            if metric_name == "Patient Birthdays":
                value = driver.find_element(By.XPATH, MailTestXpath.tdy_mail_metric_value(row+1)).text
                
                mh_mail = MhMail.query.filter_by(test_code=test_code).first()
                mh_mail.tdy_patient_bday = value
                db.session.commit()
                print(metric_name+": "+value)
                
            if metric_name == "Past Due AR":
                value = driver.find_element(By.XPATH, MailTestXpath.tdy_mail_metric_value(row+1)).text
                
                mh_mail = MhMail.query.filter_by(test_code=test_code).first()
                mh_mail.tdy_past_due_ar = value
                db.session.commit()
                print(metric_name+": "+value)
                
            if metric_name == "Due for BWX":
                value = driver.find_element(By.XPATH, MailTestXpath.tdy_mail_metric_value(row+1)).text
                
                mh_mail = MhMail.query.filter_by(test_code=test_code).first()
                mh_mail.tdy_due_bwx = value
                db.session.commit()
                print(metric_name+": "+value)
                
            if metric_name == "Due for FMX":
                value = driver.find_element(By.XPATH, MailTestXpath.tdy_mail_metric_value(row+1)).text
                
                mh_mail = MhMail.query.filter_by(test_code=test_code).first()
                mh_mail.tdy_due_fmx = value
                db.session.commit()
                print(metric_name+": "+value)
            
            
        tmw_mail_counter = driver.find_elements(By.XPATH, MailTestXpath.tmw_mail_counter)
        tmw_mail_counter = len(tmw_mail_counter)
        print(tmw_mail_counter)
        
        print('Tomorrow Mail-----------------------------------------------------------------------------------------------------------------')
        for row in range(tmw_mail_counter):
            metric_name = driver.find_element(By.XPATH, MailTestXpath.tmw_mail_metric_name(row+1)).text
            
            if metric_name == "Tomorrow's Scheduled Production":
                value = driver.find_element(By.XPATH, MailTestXpath.tmw_mail_metric_value(row+1)).text
                
                mh_mail = MhMail.query.filter_by(test_code=test_code).first()
                mh_mail.tmw_sched_prod = value
                db.session.commit()
                print(metric_name+": "+value)
                
            if metric_name == "Goal":
                value = driver.find_element(By.XPATH, MailTestXpath.tmw_mail_metric_value(row+1)).text
                
                mh_mail = MhMail.query.filter_by(test_code=test_code).first()
                mh_mail.tmw_goal = value
                db.session.commit()
                print(metric_name+": "+value)
                
            if metric_name == "New Patients (Scheduled)":
                value = driver.find_element(By.XPATH, MailTestXpath.tmw_mail_metric_value(row+1)).text
                
                mh_mail = MhMail.query.filter_by(test_code=test_code).first()
                mh_mail.tmw_npt_sched = value
                db.session.commit()
                print(metric_name+": "+value)
                
            if metric_name == "Hygiene Production (Scheduled)":
                value = driver.find_element(By.XPATH, MailTestXpath.tmw_mail_metric_value(row+1)).text
                
                mh_mail = MhMail.query.filter_by(test_code=test_code).first()
                mh_mail.tmw_hyg_prod_sched = value
                db.session.commit()
                print(metric_name+": "+value)
                
            if metric_name == "Unscheduled Treatment":
                value = driver.find_element(By.XPATH, MailTestXpath.tmw_mail_metric_value(row+1)).text
                
                mh_mail = MhMail.query.filter_by(test_code=test_code).first()
                mh_mail.tmw_unsched_tx = value
                db.session.commit()
                print(metric_name+": "+value)
                
            if metric_name == "Unscheduled Family Members":
                value = driver.find_element(By.XPATH, MailTestXpath.tmw_mail_metric_value(row+1)).text
                
                mh_mail = MhMail.query.filter_by(test_code=test_code).first()
                mh_mail.tmw_unsched_family_members = value
                db.session.commit()
                print(metric_name+": "+value)
                
            if metric_name == "Unscheduled Hygiene":
                value = driver.find_element(By.XPATH, MailTestXpath.tmw_mail_metric_value(row+1)).text
                
                mh_mail = MhMail.query.filter_by(test_code=test_code).first()
                mh_mail.tmw_unsched_hyg = value
                db.session.commit()
                print(metric_name+": "+value)
                
            if metric_name == "Past Due AR":
                value = driver.find_element(By.XPATH, MailTestXpath.tmw_mail_metric_value(row+1)).text
                
                mh_mail = MhMail.query.filter_by(test_code=test_code).first()
                mh_mail.tmw_past_due_ar = value
                db.session.commit()
                print(metric_name+": "+value)
                
            if metric_name == "Due for BWX":
                value = driver.find_element(By.XPATH, MailTestXpath.tmw_mail_metric_value(row+1)).text
                
                mh_mail = MhMail.query.filter_by(test_code=test_code).first()
                mh_mail.tmw_due_bwx = value
                db.session.commit()
                print(metric_name+": "+value)
                
            if metric_name == "Due for FMX":
                value = driver.find_element(By.XPATH, MailTestXpath.tmw_mail_metric_value(row+1)).text
                
                mh_mail = MhMail.query.filter_by(test_code=test_code).first()
                mh_mail.twm_due_fmx = value
                db.session.commit()
                print(metric_name+": "+value)
            
            
        
        
        
        
    
    
        
        
        
        
        
        
        
        
        
        
        
        