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
from ....models import TxMinerProcedureTest
from ....models import TxMinerPatientTest
from .... import db
import sqlite3
import re


def patientTestTx(driver, test_code, test_month):
    driver.implicitly_wait(1000000000)

    checkIfTheresDataInTable = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[3]/div/div/div/div[1]/div[1]/div/ul")
    stopper = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[1]/div/div/div/div[3]/button[contains(text(), 'Refresh')]")
    
    clickMonthFilter = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[1]/div/div/div/div[1]/div/div[2]")
    clickMonthFilter.click()
    
    countMonthFilter = driver.find_elements(By.XPATH, "/html/body/div[1]/main/div[1]/div/div/div/div[1]/div/div[3]/ul/li/span")
    lengthMonthFilter = len(countMonthFilter)
    
    
    month_test = datetime.strptime(test_month, '%Y-%m')
    month_test = month_test.strftime("%B %Y")

    # print(month_test)

    for q in range(lengthMonthFilter):
        getMonthNameInFilter = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[1]/div/div/div/div[1]/div/div[3]/ul/li["+str(q+1)+"]/span").text
        # print(getMonthNameInFilter)
        if getMonthNameInFilter == month_test:
            clickMonthNameInFilter = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[1]/div/div/div/div[1]/div/div[3]/ul/li["+str(q+1)+"]/span")
            clickMonthNameInFilter.click()
            clickUpdateButton = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[1]/div/div/div/div[3]/button")
            clickUpdateButton.click()
            break
        
        
    checkIfTheresDataInTable = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[3]/div/div/div/div[1]/div[1]/div/ul")
    stopper = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[1]/div/div/div/div[3]/button[contains(text(), 'Refresh')]")

    clickPatientFilter = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div[3]/div/button")
    clickPatientFilter.click()

    countPatientFilter = driver.find_elements(By.XPATH, "/html/body/div[1]/main/div[2]/div[3]/div/div/div[2]/ul/li")
    lengthPatientFilter = len(countPatientFilter)

    clickCancelButton = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div[3]/div/div/div[3]/button[1]")
    clickCancelButton.click()

    checkIfTheresDataInTable = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[3]/div/div/div/div[1]/div[1]/div/ul")
    stopper = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[1]/div/div/div/div[3]/button[contains(text(), 'Refresh')]")

    print(lengthPatientFilter)

    numberOfPatientThatHasData = 0


    for x in range(lengthPatientFilter):
        if(numberOfPatientThatHasData != 3):
            checkIfTheresDataInTable = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[3]/div/div/div/div[1]/div[1]/div/ul")
            stopper = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[1]/div/div/div/div[3]/button[contains(text(), 'Refresh')]")

            clickPatientFilters = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div[3]/div/button")
            clickPatientFilters.click()

            clickPatient = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div[3]/div/div/div[2]/ul/li["+str(x+1)+"]")
            clickPatient.click()

            getPatientName = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div[3]/div/div/div[2]/ul/li["+str(x+1)+"]/span/span[2]").text

            print("PATIENT NAME: " + getPatientName)

            clickApply = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div[3]/div/div/div[3]/button[2]")
            clickApply.click()

            checkIfTheresDataInTable = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[3]/div/div/div/div[1]/div[1]/div/ul")
            stopper = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[1]/div/div/div/div[3]/button[contains(text(), 'Refresh')]")

            countDataInTable = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[3]/div/div/div/div[2]/div/div/table/tbody").text
            lenghtOfDataInTable = len(countDataInTable)

            # print(lenghtOfDataInTable)

            if lenghtOfDataInTable != 0:
                countDataInTablePatient = driver.find_elements(By.XPATH, "/html/body/div[1]/main/div[3]/div/div/div/div[2]/div/div/table/tbody/tr/td[1]")
                lengthOfTable = len(countDataInTablePatient)
                # print(lengthOfTable)
                for y in range(lengthOfTable):
                    getMonthBreakdown = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[3]/div/div/div/div[2]/div/div/table/tbody/tr["+str(y+1)+"]/td[1]").text
                    print(getMonthBreakdown)
                    clickMonthBreakdown = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[3]/div/div/div/div[2]/div/div/table/tbody/tr["+str(y+1)+"]/td[1]/span/span[2]/a")
                    clickMonthBreakdown.click()

                    wait = WebDriverWait(driver, 100000000)
                    element = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/main/div[5]/div/div/div/div[2]/div/div/div/div[1]/div/button[2]')))

                    checkIfAlreadyLoad = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[5]/div/div/div/div[2]/div/div/div/div[2]/div[1]/table/tbody").text
                    countDataText = len(checkIfAlreadyLoad)

                    if countDataText != 0:
                        countColumnBreakdownData = driver.find_elements(By.XPATH, "/html/body/div[1]/main/div[5]/div/div/div/div[2]/div/div/div/div[2]/div[1]/table/tbody/tr/td[2]")
                        lenghtColumnBreakdownData = len(countColumnBreakdownData)
                        # print(lenghtColumnBreakdownData)

                        for m in range(lenghtColumnBreakdownData):
                            wait = WebDriverWait(driver, 100000000)
                            element = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/main/div[5]/div/div/div/div[2]/div/div/div/div[1]/div/button[2]')))

                            getBreakdownPatientName = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[5]/div/div/div/div[2]/div/div/div/div[2]/div[1]/table/tbody/tr["+str(m+1)+"]/td[2]").text

                            print("Breakdown Patient Name: " + getBreakdownPatientName) 

                            # print("Patient Filter: " + getPatientName)
                            # print("Patient Breakdown: " + getBreakdownPatientName)
                            # print("Status: ")

                            if getPatientName == getBreakdownPatientName:
                                status = "Pass"
                                new_txminer_patient = TxMinerPatientTest(user_id = current_user.id,
                                    test_code = test_code,
                                    month_breakdown = getMonthBreakdown,
                                    patient_name_filtered = getPatientName,
                                    patient_name_breakdown = getBreakdownPatientName,
                                    status = status,
                                    created_at = datetime.now(),
                                    updated_at = datetime.now())
                                
                                db.session.add(new_txminer_patient)
                                db.session.commit()
                            else:
                                status = "Fail"
                                new_txminer_patient = TxMinerPatientTest(user_id = current_user.id,
                                    test_code = test_code,
                                    month_breakdown = getMonthBreakdown,
                                    patient_name_filtered = getPatientName,
                                    patient_name_breakdown = getBreakdownPatientName,
                                    status = status,
                                    created_at = datetime.now(),
                                    updated_at = datetime.now())
                                
                                db.session.add(new_txminer_patient)
                                db.session.commit()
                                print(status)

                        clickCloseBreakdownButton = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[5]/div/div/div/div[1]/button")
                        clickCloseBreakdownButton.click()
                    else:
                        clickCloseBreakdownButton = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[5]/div/div/div/div[1]/button")
                        clickCloseBreakdownButton.click()

                numberOfPatientThatHasData = numberOfPatientThatHasData + 1
                    

            clickPtFilters = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div[3]/div/button")
            clickPtFilters.click()

            unclickPatient = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div[3]/div/div/div[2]/ul/li["+str(x+1)+"]")
            unclickPatient.click()

            clickApplyPatient = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div[3]/div/div/div[3]/button[2]")
            clickApplyPatient.click()

            checkIfTheresDataInTable = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[3]/div/div/div/div[1]/div[1]/div/ul")
            stopper = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[1]/div/div/div/div[3]/button[contains(text(), 'Refresh')]")

    return driver


