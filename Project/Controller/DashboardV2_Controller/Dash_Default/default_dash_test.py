from decimal import Decimal
from selenium import webdriver
from selenium.webdriver.common.by import By
from flask_login import login_required, current_user
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from ...Global_Controller import Range_date_picker
import time 
from datetime import datetime
from .... import db
from ....models import DashboardV2DefaultBreakdownTest
import sqlite3
import re



def defaultDashTest(driver, test_code, test_month, test_date_from, test_date_to):
    start_date = test_date_from
    end_date = test_date_to
    driver.implicitly_wait(1000000)
    # stopperNetProd = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/section[1]/div[1]/div[1]/div/div/div[2]/h3").text
    # stopperGrossProd = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/section[1]/div[1]/div[2]/div/div/div[2]/h3").text
    # stopperColl = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/section[1]/div[1]/div[3]/div/div/div[2]/h3").text
    # stopperAdjustment = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/section[1]/div[1]/div[4]/div/div/div[2]/h3").text

    # stopperAdjustment = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/section[3]/div[2]/div/div[1]/div[1]/div/ul").text

    stopper = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/section[1]/div[1]").text
    stopper2nd = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/section[3]/div[2]/div/div[2]/div/table/tbody").text

    Range_date_picker.DateFilter.rangePicker(driver, start_date, end_date)
    
    clickUpdateButton = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[1]/div/div/div/div[4]/button")
    clickUpdateButton.click()
    time.sleep(3)

    stopper = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/section[1]/div[1]").text
    stopper2nd = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/section[3]/div[2]/div/div[2]/div/table/tbody").text

    # stopperNetProd = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/section[1]/div[1]/div[1]/div/div/div[2]/h3").text
    # stopperGrossProd = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/section[1]/div[1]/div[2]/div/div/div[2]/h3").text
    # stopperColl = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/section[1]/div[1]/div[3]/div/div/div[2]/h3").text
    # stopperAdjustment = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/section[1]/div[1]/div[4]/div/div/div[2]/h3").text

    # stopperAdjustment = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/section[3]/div[2]/div/div[1]/div[1]/div/ul").text

    #Function Starts Here!
    countTiles = driver.find_elements(By.XPATH, "/html/body/div[1]/main/div[2]/section[1]/div[1]/div")
    lenghtTiles = len(countTiles)

    for x in range(lenghtTiles):
        getLabelTiles = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/section[1]/div[1]/div["+str(x+1)+"]/div/div/div[1]/h6").text
        getValueTiles = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/section[1]/div[1]/div["+str(x+1)+"]/div/div/div[2]/h3").text

        clickTileBreakdown = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/section[1]/div[1]/div["+str(x+1)+"]/div/div/div[3]/a")
        clickTileBreakdown.click()

        checkBreakdownIfItHasData = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/section[1]/div[1]/div["+str(x+1)+"]/div/div/div[3]/div/div/div/div[2]/div[2]/table/tbody").text
        countData = len(checkBreakdownIfItHasData)
        
        getBreakdownLabel = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/section[1]/div[1]/div["+str(x+1)+"]/div/div/div[3]/div/div/div/div[1]/h2/span").text
        getBreakdownTotal = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/section[1]/div[1]/div["+str(x+1)+"]/div/div/div[3]/div/div/div/div[2]/div[2]/table/tr/td[3]/span").text


        clickCloseBreakdownButton = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/section[1]/div[1]/div["+str(x+1)+"]/div/div/div[3]/div/div/div/div[1]/button")
        clickCloseBreakdownButton.click()
        
        status = ""
        if getValueTiles == getBreakdownTotal:
            status = "Pass"
        else:
            status = "Fail"

        print("Main View Label: " + getLabelTiles)
        print("Main View Value: " + getValueTiles)
        print("Breakdown Label: " + getBreakdownLabel)
        print("Breakdown Value: " + getBreakdownTotal)
        print("Status: " + status)

        new_dash_default = DashboardV2DefaultBreakdownTest(user_id = current_user.id,
            test_code = test_code,
            main_view_label = getLabelTiles,
            main_view_value = getValueTiles,
            breakdown_view_label = getBreakdownLabel,
            breakdown_view_value = getBreakdownTotal,
            status = status,
            created_at = datetime.now(),
            updated_at = datetime.now())

        db.session.add(new_dash_default)
        db.session.commit()

    print("-------------------------")
    print("-------------------------")
    print("-------------------------")

    #Patient Data Test 
    countPtTiles = driver.find_elements(By.XPATH, "/html/body/div[1]/main/div[2]/section[2]/div/div[1]/div/div")
    lengthPtTiles = len(countPtTiles)

    for y in range(lengthPtTiles):
        getPtLabel = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/section[2]/div/div[1]/div/div["+str(y+1)+"]/div/div/div[1]/h6").text
        getPtValue = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/section[2]/div/div[1]/div/div["+str(y+1)+"]/div/div/div[2]/h3").text

        clickPtBreakdown = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/section[2]/div/div[1]/div/div["+str(y+1)+"]/div/div/div[3]/a")
        clickPtBreakdown.click()
        
        time.sleep(3)
        countPtTbodyTable = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/section[2]/div/div[1]/div/div["+str(y+1)+"]/div/div/div[3]/div/div/div/div[2]/div[2]/table/tbody").text
        lengthPtTbodyTable = len(countPtTbodyTable)
        

        getBreakdownLabel = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/section[2]/div/div[1]/div/div["+str(y+1)+"]/div/div/div[3]/div/div/div/div[1]/h2/span").text
        breakdownPtValue = "";
        
        if getBreakdownLabel == "New Patients Visits Breakdown":
            if lengthPtTbodyTable != 0:
                getDataInTable = driver.find_elements(By.XPATH, "/html/body/div[1]/main/div[2]/section[2]/div/div[1]/div/div[1]/div/div/div[3]/div/div/div/div[2]/div[2]/table/tbody/tr")
                breakdownPtValue = len(getDataInTable)
                breakdownPtValue = str(breakdownPtValue)
            else:
                breakdownPtValue = "0"
        if getBreakdownLabel == "Existing Patients Visits Breakdown":
            if lengthPtTbodyTable != 0:
                getDataInTable = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/section[2]/div/div[1]/div/div[2]/div/div/div[3]/div/div/div/div[2]/div[2]/table/tr/td[5]/span").text
                breakdownPtValue = getDataInTable
            else:
                breakdownPtValue = "0"

        statusPt = ""
        if getPtValue == breakdownPtValue:
            statusPt = "Pass"
        else:
            statusPt = "Fail"

        clickPtCloseButton = driver.find_element(By.XPATH, " /html/body/div[1]/main/div[2]/section[2]/div/div[1]/div/div["+str(y+1)+"]/div/div/div[3]/div/div/div/div[1]/button")
        clickPtCloseButton.click()
       

        print("Main View PT Label: " + getPtLabel)
        print("Main View PT Value: " + getPtValue)
        print("Breakdown PT Label: " + getBreakdownLabel)
        print(breakdownPtValue )
        print("Status PT: " + statusPt)

        new_dash_default = DashboardV2DefaultBreakdownTest(user_id = current_user.id,
            test_code = test_code,
            main_view_label = getPtLabel,
            main_view_value = getPtValue,
            breakdown_view_label = getBreakdownLabel,
            breakdown_view_value = breakdownPtValue,
            status = statusPt,
            created_at = datetime.now(),
            updated_at = datetime.now())

        db.session.add(new_dash_default)
        db.session.commit()

    return driver
        

