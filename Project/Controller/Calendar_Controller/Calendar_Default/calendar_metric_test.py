from selenium import webdriver
from selenium.webdriver.common.by import By
from flask_login import login_required, current_user
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time 
from datetime import datetime
from ....models import CalendarFilterUse
from ....models import CalendarFilterTesting
from ....models import CalendarMetricTesting
from .... import db
import sqlite3
import re


def metricTest(driver, test_code, test_month):
    driver.implicitly_wait(1000000000)
    clickMonth = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div/div/div[2]/div[1]/ul/li[1]/a")
    clickMonth.click()

    stopperGetTbodyInTable = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div/span/div[2]/div[3]/div/div/table/tbody/tr/td/div/div/div/table/tbody")
    time.sleep(5)
    month_test = datetime.strptime(test_month, '%Y-%m')
    month_test = month_test.strftime("%B %Y")
    value = 1
    

    while(value):
        getMonth = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div/span/div[2]/div[2]/div/div/h4").text
        if getMonth == str(month_test):
            break
        else:
            clickPrevMonth = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div/span/div[2]/div[2]/div/button[1]")
            clickPrevMonth.click()
    
    stopperGetTbodyInTables = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div/span/div[2]/div[3]/div/div/table/tbody/tr/td/div/div/div/table/tbody")
    time.sleep(5)

    bd_sched_amount = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div/span/div[1]/div[2]/div/div[1]/div/div[2]/h4/span").text
    bd_goal = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div/span/div[1]/div[2]/div/div[3]/div/div[2]/h4/span").text
    bd_production = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div/span/div[1]/div[2]/div/div[6]/div/div[2]/h4/span").text
    bd_appt = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div/span/div[1]/div[2]/div/div[4]/div/div[2]/h4/span").text
    bd_npts = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div/span/div[1]/div[2]/div/div[5]/div/div[2]/h4/span").text


    start = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div/span/div[2]/div[3]/div/div/table/tbody/tr/td/div/div/div/table/tbody/tr[1]/td[1]")

    getAllColumnsInCalendar = driver.find_elements(By.XPATH, "/html/body/div[1]/main/div[2]/div/span/div[2]/div[3]/div/div/table/tbody/tr/td/div/div/div/table/tbody/tr")
    countColumnsInCalendar = len(getAllColumnsInCalendar)
    # print(countColumnsInCalendar)

    end = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div/span/div[2]/div[3]/div/div/table/tbody/tr/td/div/div/div/table/tbody/tr["+str(countColumnsInCalendar)+"]/td[7]")

    performClickAndHold = ActionChains(driver).click_and_hold(start).move_to_element(end).click(end).perform()
    time.sleep(5)

    # getMonths = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div/span/div[2]/div[2]/div/div/h4").text

    sd_sched_amount = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div/span/div[1]/div[2]/div/div[1]/div/div[2]/h4/span").text
    sd_goal = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div/span/div[1]/div[2]/div/div[3]/div/div[2]/h4/span").text
    sd_production = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div/span/div[1]/div[2]/div/div[6]/div/div[2]/h4/span").text
    sd_appt = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div/span/div[1]/div[2]/div/div[4]/div/div[2]/h4/span").text
    sd_npts = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div/span/div[1]/div[2]/div/div[5]/div/div[2]/h4/span").text

    #STATUS FOR SCHEDULE AMOUNT
    if bd_sched_amount == sd_sched_amount:
        status_sched_amount = "Pass"
    else: 
        status_sched_amount = "Fail"
    #STATUS FOR Goal
    if bd_goal == sd_goal:
        status_goal = "Pass"
    else: 
        status_goal = "Fail"
    #STATUS FOR Production
    if bd_production == sd_production:
        status_production = "Pass"
    else: 
        status_production = "Fail"
    #STATUS FOR Appointments
    if bd_appt == sd_appt:
        status_appt = "Pass"
    else: 
        status_appt = "Fail"
    #STATUS FOR New Patients
    if bd_npts == sd_npts:
        status_npts = "Pass"
    else: 
        status_npts = "Fail"

    print("Schedule Amount "+bd_sched_amount+"/"+sd_sched_amount+"/"+status_sched_amount)
    print("Goal "+bd_goal+"/"+sd_goal+"/"+status_goal)
    print("Production: "+bd_production+"/"+sd_production+"/"+status_production)
    print("Appointments: "+bd_appt+"/"+sd_appt+"/"+status_appt)
    print("new Patients: "+bd_npts+"/"+sd_npts+"/"+status_npts)

    new_calendar_metric_testing = CalendarMetricTesting(user_id = current_user.id,
        test_code = test_code,
        bd_sched_amount = bd_sched_amount,
        sd_sched_amount = sd_sched_amount,
        bd_goal = bd_goal,
        sd_goal = sd_goal,
        bd_production = bd_production,
        sd_production = sd_production,
        bd_appt = bd_appt,
        sd_appt = sd_appt,
        bd_npts = bd_npts,
        sd_npts = bd_npts,
        status_sched_amount = status_sched_amount,
        status_npts = status_npts,
        status_goal = status_goal,
        status_production = status_production,
        status_appt = status_appt,
        created_at = datetime.now(),
        updated_at = datetime.now())

    db.session.add(new_calendar_metric_testing)
    db.session.commit()


    # print(getMonths)
