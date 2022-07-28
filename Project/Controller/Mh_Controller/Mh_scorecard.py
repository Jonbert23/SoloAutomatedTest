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
from Project.models import MhScorecard
from Project import db


class MornigHuddleScorecard:
    
    def Main_test(driver, test_code):
        
        wait = WebDriverWait(driver, 60)
        loader = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/main/div[1]/div/div/div/div[4]/button')))
        driver.implicitly_wait(10)
        action =  ActionChains(driver)
        
        #Yesterday Scorecard------------------------------------------------------------------------------------------------
        yrt_scorecard_open = driver.find_element(By.XPATH, '/html/body/div[1]/main/div[2]/div[1]/div[1]/div/h5/a')
        yrt_scorecard_open.click()
        
        ytr_prod = driver.find_element(By.XPATH, MHXpath.ytr_sc_prod).text
        ytr_goal = driver.find_element(By.XPATH, MHXpath.ytr_sc_goal).text
        ytr_collection = driver.find_element(By.XPATH, MHXpath.ytr_sc_collection).text
        ytr_npt_actual = driver.find_element(By.XPATH, MHXpath.ytr_sc_npt).text
        yrt_broken_appt = driver.find_element(By.XPATH, MHXpath.ytr_sc_broken_visst).text
        
        print('--------------------------------------------------------------------')
        print('Scorecard Production : '+ytr_prod)
        print('--------------------------------------------------------------------')
        print('Scorecard Goal : '+ytr_goal)
        print('--------------------------------------------------------------------')
        print('Scorecard Collection : '+ytr_collection)
        print('--------------------------------------------------------------------')
        print('Scorecard NPT Actual: '+ytr_npt_actual)
        print('--------------------------------------------------------------------')
        print('Scorecard Broken Appt: '+yrt_broken_appt)
        
        
        yrt_scorecard_close = driver.find_element(By.XPATH, '/html/body/div[1]/main/div[4]/div/div/div/div[1]/button')
        yrt_scorecard_close.click()
        
        #Today Scorecard------------------------------------------------------------------------------------------------
        tdy_scorecard_open = driver.find_element(By.XPATH, '/html/body/div[1]/main/div[2]/div[1]/div[2]/h5/a')
        tdy_scorecard_open.click()
        
        tdy_sched_prod = driver.find_element(By.XPATH, MHXpath.tdy_sc_sched_prod).text
        tdy_goal = driver.find_element(By.XPATH, MHXpath.tdy_sc_goal).text
        tdy_npt_actual = driver.find_element(By.XPATH, MHXpath.tdy_sc_npt_actual).text
        tdy_npt_sched =  driver.find_element(By.XPATH, MHXpath.tdy_sc_npt_sched).text
        
        print('--------------------------------------------------------------------')
        print('Scorecard Sched Production : '+tdy_sched_prod)
        print('--------------------------------------------------------------------')
        print('Scorecard Goal : '+tdy_goal)
        print('--------------------------------------------------------------------')
        print('Scorecard NPT Actual: '+tdy_npt_actual)
        print('--------------------------------------------------------------------')
        print('Scorecard NPT Sched: '+tdy_npt_sched)
        
        tdy_scorecard_close = driver.find_element(By.XPATH, '/html/body/div[1]/main/div[4]/div/div/div/div[1]/button')
        tdy_scorecard_close.click()
        
        #Today Scorecard------------------------------------------------------------------------------------------------
        tmw_scorecard_open = driver.find_element(By.XPATH, '/html/body/div[1]/main/div[2]/div[1]/div[3]/div/h5/a')
        tmw_scorecard_open.click()
        
        tmw_sched_prod = driver.find_element(By.XPATH, MHXpath.tmw_sc_sched_prod).text
        tmw_goal = driver.find_element(By.XPATH, MHXpath.tmw_sc_goal).text
        tmw_npt = driver.find_element(By.XPATH, MHXpath.tmw_sc_npt).text
        
        print('--------------------------------------------------------------------')
        print('Scorecard Sched Production : '+tmw_sched_prod)
        print('--------------------------------------------------------------------')
        print('Scorecard Goal : '+tmw_goal)
        print('--------------------------------------------------------------------')
        print('Scorecard NPT Sched: '+tmw_npt)
        
        tmw_scorecard_close = driver.find_element(By.XPATH, '/html/body/div[1]/main/div[4]/div/div/div/div[1]/button')
        tmw_scorecard_close.click()
        
        mh_sc = MhScorecard(
            user_id = current_user.id,
            test_code = test_code,
            ytr_prod  = ytr_prod ,
            ytr_goal  = ytr_goal ,
            ytr_collection = ytr_collection,
            ytr_npt_actual = ytr_npt_actual ,
            yrt_broken_appt = yrt_broken_appt,
            tdy_sched_prod = tdy_sched_prod,
            tdy_goal = tdy_goal,
            tdy_npt_actual = tdy_npt_actual,
            tdy_npt_sched = tdy_npt_sched,
            tmw_sched_prod = tmw_sched_prod,
            tmw_goal = tmw_goal,
            tmw_npt = tmw_npt 
        )
        db.session.add(mh_sc)
        db.session.commit()