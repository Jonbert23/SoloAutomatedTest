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
from ....models import DashboardV2DefaultProductionTest
import sqlite3
import re



def defaultProductionFiguresTest(driver, test_code, test_month, test_date_from, test_date_to):
    scrollToTop = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[1]/div/h1")
    driver.execute_script("return arguments[0].scrollIntoView(true);", scrollToTop)
    time.sleep(2)
    start_date = test_date_from
    end_date = test_date_to
    driver.implicitly_wait(1000000)

    stopper = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/section[1]/div[1]").text
    stopper2nd = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/section[3]/div[2]/div/div[2]/div/table/tbody").text

    Range_date_picker.DateFilter.rangePicker(driver, start_date, end_date)
    
    clickUpdateButton = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[1]/div/div/div/div[4]/button")
    clickUpdateButton.click()
    time.sleep(3)


    stopper = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/section[1]/div[1]").text
    stopper2nd = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/section[3]/div[2]/div/div[2]/div/table/tbody").text


    #FUNCTION STARTS HERE
    getFinancialTiles = driver.find_elements(By.XPATH, "/html/body/div[1]/main/div[2]/section[1]/div[1]/div")
    countTiles = len(getFinancialTiles)
    baseData = ""
    baseValue = ""
    for x in range(countTiles):
        getTileLabel = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/section[1]/div[1]/div["+str(x+1)+"]/div/div/div[1]/h6").text
        # print(getTileLabel)

        if getTileLabel == "Net Production":
            baseValue = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/section[1]/div[1]/div["+str(x+1)+"]/div/div/div[2]/h3").text
            baseData = "Net Production"

    if baseData == "Net Production":
        print("IT HAS A BASE DATA!!!!!!!")
        getProviderDataProduction = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/section[3]/div[1]/div/div[2]/div[1]/h3").text
        getProductionInTable = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/section[3]/div[2]/div/div[2]/div/table/tr[2]/td[3]").text

        #go to metric tab
        clickMetric = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[1]/div/nav/ul/li[2]/a")
        clickMetric.click()
        time.sleep(3)
        stopper4th = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/section[2]/div/div[1]/div[2]/div[2]/button").text
        getIfItHasData = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/section[3]/div/div[2]/div/div/table/tbody/tr[1]/td[1]").text
        
        payorProductionValue = ""
        if getIfItHasData == "No data":
            payorProductionValue == driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/section[3]/div/div[2]/div/div/table/tr/td[2]").text
        else:
            payorProductionValue = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/section[3]/div/div[2]/div/div/table/tr/td[2]").text
        
        status = ""
        if baseValue == getProviderDataProduction and baseValue == getProductionInTable and baseValue == payorProductionValue:
            status = "Pass"
        if baseValue != getProviderDataProduction or baseValue != getProductionInTable or baseValue != payorProductionValue:
            status = "Fail"

        print(getProviderDataProduction)
        print(baseValue)
        print(getProductionInTable)
        print(payorProductionValue)
        print(status)

        new_dash_production_test = DashboardV2DefaultProductionTest(user_id = current_user.id,
            test_code = test_code,
            base_value = baseValue,
            production_by_provider = getProviderDataProduction,
            table_production = getProductionInTable,
            payors_production = payorProductionValue,
            status = status,
            created_at = datetime.now(),
            updated_at = datetime.now())

        db.session.add(new_dash_production_test)
        db.session.commit()

        return driver
        

    if baseData == "":
        print("IT DONT HAVE A BASE DATA!!!!!!!")
        getProviderDataProduction = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/section[3]/div[1]/div/div[2]/div[1]/h3").text
        baseValue = getProviderDataProduction
        getProductionInTable = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/section[3]/div[2]/div/div[2]/div/table/tr[2]/td[3]").text

        #go to metric tab
        clickMetric = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[1]/div/nav/ul/li[2]/a")
        clickMetric.click()
        stopper4th = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/section[2]/div/div[1]/div[2]/div[2]/button").text
        getIfItHasData = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/section[3]/div/div[2]/div/div/table/tbody/tr[1]/td[1]").text
        time.sleep(3)
        payorProductionValue = ""
        if getIfItHasData == "No data":
            payorProductionValue == driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/section[3]/div/div[2]/div/div/table/tr/td[2]").text
        else:
            payorProductionValue = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/section[3]/div/div[2]/div/div/table/tr/td[2]").text

        status = ""
        if baseValue == getProviderDataProduction and baseValue == getProductionInTable and baseValue == payorProductionValue:
            status = "Pass"
        if baseValue != getProviderDataProduction or baseValue != getProductionInTable or baseValue != payorProductionValue:
            status = "Fail"

        print(getProviderDataProduction)
        print(baseValue + " FROM TILE")
        print(getProductionInTable)
        print(payorProductionValue)
        print(status)

        new_dash_production_test = DashboardV2DefaultProductionTest(user_id = current_user.id,
            test_code = test_code,
            base_value = baseValue,
            production_by_provider = getProviderDataProduction,
            table_production = getProductionInTable,
            payors_production = payorProductionValue,
            status = status,
            created_at = datetime.now(),
            updated_at = datetime.now())

        db.session.add(new_dash_production_test)
        db.session.commit()

        return driver
        
        