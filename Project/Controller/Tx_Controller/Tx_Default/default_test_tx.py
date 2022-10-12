from decimal import Decimal
from selenium import webdriver
from selenium.webdriver.common.by import By
from flask_login import login_required, current_user
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time 
from datetime import datetime
from ....models import TxMinerDefaultTest
from .... import db
import sqlite3
import re


def defaultTestTx(driver, test_code, test_month):
    driver.implicitly_wait(1000000000)

    checkIfTableAlreadyLoad = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[3]/div/div/div/div[2]/div/div/table/tbody/tr[1]/td[1]")
    checkIfColorCodingAlreadyShown = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[3]/div/div/div/div[1]/div[1]/div/ul")
    
    getAllDataInTable = driver.find_elements(By.XPATH, "/html/body/div[1]/main/div[3]/div/div/div/div[2]/div/div/table/tbody/tr")
    countAllDataInTable = len(getAllDataInTable)
    print(countAllDataInTable)


    totalAllPendingScheduled = 0
    totalAllPendingUnScheduled = 0
    totalAllActiveProduction = 0
    for i in range(countAllDataInTable):
        getMonth = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[3]/div/div/div/div[2]/div/div/table/tbody/tr["+str(i+1)+"]/td[1]").text
        getPendingSchedPerMonth = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[3]/div/div/div/div[2]/div/div/table/tbody/tr["+str(i+1)+"]/td[3]").text.replace(',' , '').replace('$ ','')
        mainViewPendingSchedPerMonth = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[3]/div/div/div/div[2]/div/div/table/tbody/tr["+str(i+1)+"]/td[3]").text
        getPendingUnschedPerMonth = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[3]/div/div/div/div[2]/div/div/table/tbody/tr["+str(i+1)+"]/td[4]").text.replace(',' , '').replace('$ ','')
        mainViewPendingUnschedPerMonth = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[3]/div/div/div/div[2]/div/div/table/tbody/tr["+str(i+1)+"]/td[4]").text
        getActiveProductionPerMonth = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[3]/div/div/div/div[2]/div/div/table/tbody/tr["+str(i+1)+"]/td[5]").text.replace(',' , '').replace('$ ','')
        mainViewActiveProduction = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[3]/div/div/div/div[2]/div/div/table/tbody/tr["+str(i+1)+"]/td[5]").text

        clickMonthBreakdown = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[3]/div/div/div/div[2]/div/div/table/tbody/tr["+str(i+1)+"]/td[1]/span/span[2]/a")
        driver.execute_script("arguments[0].click();", clickMonthBreakdown)
        # clickMonthBreakdown.click()

        waitUntilDataInTableWillLoad = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[5]/div/div/div/div[2]/div/div/div/div[2]/div[1]/table/tbody/tr[1]/td[2]").text

        getBreakdownPendingSchedPerMonth = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[5]/div/div/div/div[2]/div/div/div/div[2]/div[1]/table/tr/td[9]").text.replace(',' , '').replace('$ ','')
        breakdownPendingSchedPerMonth = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[5]/div/div/div/div[2]/div/div/div/div[2]/div[1]/table/tr/td[9]").text
        getBreakdownPendingUnschedPerMonth = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[5]/div/div/div/div[2]/div/div/div/div[2]/div[1]/table/tr/td[10]").text.replace(',' , '').replace('$ ','')
        breakdownPendingUnschedPerMonth = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[5]/div/div/div/div[2]/div/div/div/div[2]/div[1]/table/tr/td[10]").text
        getBreakdownActiveProductionPerMonth = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[5]/div/div/div/div[2]/div/div/div/div[2]/div[1]/table/tr/td[11]").text.replace(',' , '').replace('$ ','')
        breakdownActiveProductionPerMonth = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[5]/div/div/div/div[2]/div/div/div/div[2]/div[1]/table/tr/td[11]").text

        

        pendingSchedPerMonthStatus = ""
        pendingUnschedPerMonthStatus = ""
        activeProductionPerMonth = ""

        if getPendingSchedPerMonth == getBreakdownPendingSchedPerMonth:
            pendingSchedPerMonthStatus = "Pass"
        else: 
            pendingSchedPerMonthStatus = "Fail"

        if getPendingUnschedPerMonth == getBreakdownPendingUnschedPerMonth:
            pendingUnschedPerMonthStatus = "Pass"
        else: 
            pendingUnschedPerMonthStatus = "Fail"

        if getActiveProductionPerMonth == getBreakdownActiveProductionPerMonth:
            activeProductionPerMonth = "Pass"
        else: 
            activeProductionPerMonth = "Fail"

        print(getMonth)
        print(pendingSchedPerMonthStatus)
        print(pendingUnschedPerMonthStatus)
        print(activeProductionPerMonth)

        print(mainViewPendingSchedPerMonth)
        print(mainViewPendingUnschedPerMonth)
        print(mainViewActiveProduction)

        print(breakdownPendingSchedPerMonth)
        print(breakdownPendingUnschedPerMonth)
        print(breakdownActiveProductionPerMonth)

        new_txminer_default = TxMinerDefaultTest(user_id = current_user.id,
            test_code = test_code,
            month = getMonth,
            mv_pending_sched = mainViewPendingSchedPerMonth,
            mv_pending_unsched = mainViewPendingUnschedPerMonth,
            mv_active_production = mainViewActiveProduction,
            breakdown_pending_sched = breakdownPendingSchedPerMonth,
            breakdown_pending_unsched = breakdownPendingUnschedPerMonth, 
            breakdown_active_production = mainViewActiveProduction,
            pending_sched_status = pendingSchedPerMonthStatus,
            pending_unsched_status = pendingUnschedPerMonthStatus,
            pending_active_production = activeProductionPerMonth,
            created_at = datetime.now(),
            updated_at = datetime.now())

        db.session.add(new_txminer_default)
        db.session.commit()

        closeBreakdown = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[5]/div/div/div/div[1]/button")
        driver.execute_script("arguments[0].click();", closeBreakdown)
        

        

        totalAllPendingScheduled = totalAllPendingScheduled + Decimal(getPendingSchedPerMonth)
        totalAllPendingUnScheduled = totalAllPendingUnScheduled + Decimal(getPendingUnschedPerMonth)
        totalAllActiveProduction = totalAllActiveProduction + Decimal(getActiveProductionPerMonth)
        
    # print(totalAllPendingScheduled)
    # print(totalAllPendingUnScheduled)
    # print(totalAllActiveProduction)
    return driver