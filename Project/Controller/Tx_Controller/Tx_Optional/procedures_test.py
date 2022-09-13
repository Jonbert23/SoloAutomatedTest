from decimal import Decimal
from selenium import webdriver
from selenium.webdriver.common.by import By
from flask_login import login_required, current_user
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import time 
from datetime import datetime
from ....models import TxMinerDefaultTest
from ....models import TxMinerProviderTest
from .... import db
import sqlite3
import re


def procedureTestTx(driver, test_code, test_month):

    driver.implicitly_wait(1000000000)

    checkIfTheresDataInTable = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[3]/div/div/div/div[1]/div[1]/ul")
    stopper = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[1]/div/div/div/div[3]/button[contains(text(), 'Refresh')]")
    
    clickMonthFilter = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[1]/div/div/div/div[1]/div/div[2]")
    clickMonthFilter.click()
    
    countMonthFilter = driver.find_elements(By.XPATH, "/html/body/div[1]/main/div[1]/div/div/div/div[1]/div/div[3]/ul/li/span")
    lengthMonthFilter = len(countMonthFilter)
    
    
    month_test = datetime.strptime(test_month, '%Y-%m')
    month_test = month_test.strftime("%B %Y")

    for q in range(lengthMonthFilter):
        getMonthNameInFilter = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[1]/div/div/div/div[1]/div/div[3]/ul/li["+str(q+1)+"]/span").text
        # print(getMonthNameInFilter)
        if getMonthNameInFilter == month_test:
            clickMonthNameInFilter = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[1]/div/div/div/div[1]/div/div[3]/ul/li["+str(q+1)+"]/span")
            clickMonthNameInFilter.click()
            clickUpdateButton = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[1]/div/div/div/div[3]/button")
            clickUpdateButton.click()
            break
        
        
    checkIfTheresDataInTable = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[3]/div/div/div/div[1]/div[1]/ul")
    stopper = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[1]/div/div/div/div[3]/button[contains(text(), 'Refresh')]")

    # time.sleep(3)
    
    clickProcedureFilter = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div[2]/div/button")
    clickProcedureFilter.click()

    getAllProcedureInProcedureFilter = driver.find_elements(By.XPATH, '/html/body/div[1]/main/div[2]/div[2]/div/div/div[2]/ul/li')
    countAllProcedure = len(getAllProcedureInProcedureFilter)
    

    print(countAllProcedure)

    clickCancelButton = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div[2]/div/div/div[3]/button[1]")
    clickCancelButton.click()

    numberOfProcedureItHasData = 0
    procedureArray = []

    checkIfTheresDataInTables = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[3]/div/div/div/div[1]/div[1]/ul")

    stopper = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[1]/div/div/div/div[3]/button[contains(text(), 'Refresh')]")

    for i in range(countAllProcedure):
        if numberOfProcedureItHasData < 3:
            checkIfTheresDataInTables = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[3]/div/div/div/div[1]/div[1]/ul")
            stopper = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[1]/div/div/div/div[3]/button[contains(text(), 'Refresh')]")
            clickProcedureFilters = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div[2]/div/button")
            clickProcedureFilters.click()

            getProcedureCodeNumber = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div[2]/div/div/div[2]/ul/li["+str(i+1)+"]/span/span[1]").text
            getProcedureCodeDesc = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div[2]/div/div/div[2]/ul/li["+str(i+1)+"]/span/span[2]").text
            # providerInFilter = splitGetProviderTextInProviderFilter[0]
            # print(splitGetProviderTextInProviderFilter[0])
            clickSelectedProcedure = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div[2]/div/div/div[2]/ul/li["+str(i+1)+"]/span/span[1]")
            clickSelectedProcedure.click()

            clickApplyButton = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div[2]/div/div/div[3]/button[2]")
            clickApplyButton.click()


            checkIfTheresDataInTable = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[3]/div/div/div/div[1]/div[1]/ul")
            stopper = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[1]/div/div/div/div[3]/button[contains(text(), 'Refresh')]")
            time.sleep(3)
            checkIfDataExistInTables = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[3]/div/div/div/div[2]/div/div/table/tbody").text
            countCheckedData = len(checkIfDataExistInTables)

            if countCheckedData != 0:
                getAllDataInTable = driver.find_elements(By.XPATH, "/html/body/div[1]/main/div[3]/div/div/div/div[2]/div/div/table/tbody/tr/td[1]")
                countAllDataInTable = len(getAllDataInTable)
            else:
                countAllDataInTable = 0

            if countAllDataInTable != 0:
                numberOfProcedureItHasData = numberOfProcedureItHasData + 1
                # providerArray.append(getProviderTextInProviderFilter)
                countDataInTable = driver.find_elements(By.XPATH, "/html/body/div[1]/main/div[3]/div/div/div/div[2]/div/div/table/tbody/tr/td[1]")
                countData = len(countDataInTable)

                if countData >= 3:
                    iteratorMonth = 3
                if countData < 3:
                    iteratorMonth = countData
                
                numberOfMonthToTest = 0
                for j in range(iteratorMonth):
                    
                    getMonth = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[3]/div/div/div/div[2]/div/div/table/tbody/tr["+str(j+1)+"]/td[1]").text
                    # print(getMonth)

                    clickMonthBreakdown = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[3]/div/div/div/div[2]/div/div/table/tbody/tr["+str(j+1)+"]/td[1]/span/span[2]/a")
                    clickMonthBreakdown.click()

                    wait = WebDriverWait(driver, 100000000)
                    element = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/main/div[5]/div/div/div/div[2]/div/div/div/div[1]/div/button[2]')))
                    
                    checkIfAlreadyLoad = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[5]/div/div/div/div[2]/div/div/div/div[2]/div[1]/table/tbody").text
                    countDataText = len(checkIfAlreadyLoad)

                    if countDataText > 0:
                        countDataInTable = driver.find_elements(By.XPATH, "/html/body/div[1]/main/div[5]/div/div/div/div[2]/div/div/div/div[2]/div[1]/table/tbody/tr/td[2]")
                        countDataInTableLenght = len(countDataInTable)
                        print(countDataInTableLenght)
                        if countDataInTableLenght >= 3: 
                            iteratorPatient = 3
                        if countDataInTableLenght < 3:
                            iteratorPatient = countDataInTableLenght
                    else:
                        clickCloseBreakdownButton = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[5]/div/div/div/div[1]/button")
                        clickCloseBreakdownButton.click()   




            if countAllDataInTable == 0:
                checkIfTheresDataInTable = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[3]/div/div/div/div[1]/div[1]/ul")
                    
                clickProceduresFilters = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div[2]/div/button")
                clickProceduresFilters.click()

                unclickSelectedProcedure = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div[2]/div/div/div[2]/ul/li["+str(i+1)+"]/span/span[1]")
                unclickSelectedProcedure.click()

                clickApplyButtons = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div[2]/div/div/div[3]/button[2]")
                clickApplyButtons.click()

                checkIfTheresDataInTable = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[3]/div/div/div/div[1]/div[1]/ul")
                stopper = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[1]/div/div/div/div[3]/button[contains(text(), 'Refresh')]")
        else:
            break
    driver.quit()