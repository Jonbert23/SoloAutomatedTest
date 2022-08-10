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
        
        ytr_mail_counter = driver.find_elements(By.XPATH, MailTestXpath.ytr_mail_counter)
        ytr_mail_counter = len(ytr_mail_counter)
        print(ytr_mail_counter)
        
        print('Yesterday Mail----------------------------------------------------------------------------------------------------------------')
        for row in range(ytr_mail_counter):
            metric_name = driver.find_element(By.XPATH, MailTestXpath.ytr_mail_metric_name(row+1)).text
            metric_value = driver.find_element(By.XPATH, MailTestXpath.ytr_mail_metric_value(row+1)).text
            print(metric_name+': '+metric_value)
            
        tdy_mail_counter = driver.find_elements(By.XPATH, MailTestXpath.tdy_mail_counter)
        tdy_mail_counter = len(tdy_mail_counter)
        
        
        print('Today Mail--------------------------------------------------------------------------------------------------------------------')
        for row in range(tdy_mail_counter):
            metric_name = driver.find_element(By.XPATH, MailTestXpath.tdy_mail_metric_name(row+1)).text
            metric_value = driver.find_element(By.XPATH, MailTestXpath.tdy_mail_metric_value(row+1)).text
            print(metric_name+': '+metric_value)
            
        tmw_mail_counter = driver.find_elements(By.XPATH, MailTestXpath.tmw_mail_counter)
        tmw_mail_counter = len(tmw_mail_counter)
        
        print('Tomorrow Mail-----------------------------------------------------------------------------------------------------------------')
        for row in range(tmw_mail_counter):
            metric_name = driver.find_element(By.XPATH, MailTestXpath.tmw_mail_metric_name(row+1)).text
            metric_value = driver.find_element(By.XPATH, MailTestXpath.tmw_mail_metric_value(row+1)).text
            print(metric_name+': '+metric_value)
        
        
        
        
    
    
        
        
        
        
        
        
        
        
        
        
        
        