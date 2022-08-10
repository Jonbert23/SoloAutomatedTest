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
from .... import db
import sqlite3
import re


def providerTestTx(driver, test_code, test_month):

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

    
    
    clickProviderFilter = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div[1]/div/button")
    clickProviderFilter.click()

    getAllProviderInProviderFilter = driver.find_elements(By.XPATH, '/html/body/div[1]/main/div[2]/div[1]/div/div/div[2]/ul/li')
    countAllProvider = len(getAllProviderInProviderFilter)

    # print(countAllProvider)

    clickCancelButton = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div[1]/div/div/div[3]/button[1]")
    clickCancelButton.click()

    numberOfProviderItHasData = 0
    providerArray = []

    checkIfTheresDataInTables = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[3]/div/div/div/div[1]/div[1]/ul")

    stopper = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[1]/div/div/div/div[3]/button[contains(text(), 'Refresh')]")



    for i in range(countAllProvider):
        if numberOfProviderItHasData < 3:
            checkIfTheresDataInTables = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[3]/div/div/div/div[1]/div[1]/ul")
            stopper = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[1]/div/div/div/div[3]/button[contains(text(), 'Refresh')]")
            clickProviderFilters = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div[1]/div/button")
            clickProviderFilters.click()

            getProviderTextInProviderFilter = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div[1]/div/div/div[2]/ul/li["+str(i+1)+"]/span/span[1]").text
            print(getProviderTextInProviderFilter)
            clickSelectedProvider = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div[1]/div/div/div[2]/ul/li["+str(i+1)+"]/span/span[1]")
            clickSelectedProvider.click()

            clickApplyButton = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div[1]/div/div/div[3]/button[2]")
            clickApplyButton.click()

            checkIfTheresDataInTable = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[3]/div/div/div/div[1]/div[1]/ul")
            stopper = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[1]/div/div/div/div[3]/button[contains(text(), 'Refresh')]")

            checkIfDataExistInTables = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[3]/div/div/div/div[2]/div/div/table/tbody").text
            countCheckedData = len(checkIfDataExistInTables)

            if countCheckedData != 0:
                getAllDataInTable = driver.find_elements(By.XPATH, "/html/body/div[1]/main/div[3]/div/div/div/div[2]/div/div/table/tbody/tr/td[1]")
                countAllDataInTable = len(getAllDataInTable)
            else:
                countAllDataInTable = 0

            # print(countAllDataInTable)
            if countAllDataInTable != 0:
                numberOfProviderItHasData = numberOfProviderItHasData + 1
                # providerArray.append(getProviderTextInProviderFilter)
                countDataInTable = driver.find_elements(By.XPATH, "/html/body/div[1]/main/div[3]/div/div/div/div[2]/div/div/table/tbody/tr/td[1]")
                countData = len(countDataInTable)

                
                if countData >= 3:
                    iteratorMonth = 3
                if countData < 3:
                    iteratorMonth = countData
                
                # print(iteratorMonth)
                numberOfMonthToTest = 0

                for j in range(iteratorMonth):
                    
                    getMonth = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[3]/div/div/div/div[2]/div/div/table/tbody/tr["+str(j+1)+"]/td[1]").text
                    # print(getMonth)

                    clickMonthBreakdown = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[3]/div/div/div/div[2]/div/div/table/tbody/tr["+str(j+1)+"]/td[1]/span/span[2]/a")
                    clickMonthBreakdown.click()
                    
                    wait = WebDriverWait(driver, 100000)
                    element = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/main/div[5]/div/div/div/div[2]/div/div/div/div[1]/div/button[2]')))
                    
                    checkIfAlreadyLoad = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[5]/div/div/div/div[2]/div/div/div/div[2]/div[1]/table/tbody").text
                    countDataText = len(checkIfAlreadyLoad)
                    
                    # print(countDataText)
                    if countDataText > 0:
                        countDataInTable = driver.find_elements(By.XPATH, "/html/body/div[1]/main/div[5]/div/div/div/div[2]/div/div/div/div[2]/div[1]/table/tbody/tr/td[2]")
                        countDataInTableLenght = len(countDataInTable)
                        # print(countDataInTableLenght)
                        if countDataInTableLenght >= 3: 
                            iteratorPatient = 3
                        if countDataInTableLenght < 3:
                            iteratorPatient = countDataInTableLenght
                        
                        for t in range(iteratorPatient):
                            getPatientName = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[5]/div/div/div/div[2]/div/div/div/div[2]/div[1]/table/tbody/tr["+str(t+1)+"]/td[2]").text
                            
                            
                            clickPatientBreakdown = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[5]/div/div/div/div[2]/div/div/div/div[2]/div[1]/table/tbody/tr["+str(t+1)+"]/td[2]/span/span/a")
                            clickPatientBreakdown.click()
                            checkIfPatientInfoAlreadyLoad = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[5]/div[2]/div/div/div[2]/div[2]/div/div/div[1]/div[1]/div[1]/div/h5").text
                            checkIfOverviewAlreadyLoad = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[5]/div[2]/div/div/div[2]/div[2]/div/div/div[2]/div[1]/div[1]/div/div[2]/h5[1]").text 
                            clickARSummary = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[5]/div[2]/div/div/div[2]/div[1]/ul/li[6]/a")
                            clickARSummary.click()
                            
                            checkIfTotalAlreadyLoaded = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[5]/div[2]/div/div/div[2]/div[2]/div/div/div[1]/div/div[1]/div/div/div[1]/h5").text 
                            # checkIfTableAlreadyLoaded = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[5]/div[2]/div/div/div[2]/div[2]/div/div/div[2]/div/div/table/tbody/tr[1]/td[1]").text 
                            time.sleep(3)
                            
                            countDataInTableARSummary = driver.find_elements(By.XPATH, "/html/body/div[1]/main/div[5]/div[2]/div/div/div[2]/div[2]/div/div/div[2]/div/div/table/tbody/tr/td[1]")
                            countARSummaryData = len(countDataInTableARSummary)
                            
                            # print(countARSummaryData)
                            status = ""
                            for w in range(countARSummaryData):
                                getArSummaryDate = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[5]/div[2]/div/div/div[2]/div[2]/div/div/div[2]/div/div/table/tbody/tr["+str(w+1)+"]/td[5]").text
                                month_ar_summary = datetime.strptime(getArSummaryDate, '%b %d, %Y')
                                month_ar_summary = month_ar_summary.strftime("%Y-%m")
                                
                                if month_ar_summary == test_month:
                                    getProviderNameArSummary = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[5]/div[2]/div/div/div[2]/div[2]/div/div/div[2]/div/div/table/tbody/tr["+str(w+1)+"]/td[4]").text
                                    print(getProviderNameArSummary);
                                    print("-----------------------------------")

                                    
                            # print("Month Breakdown: "+getMonth)
                            # print("Month Filtered: "+month_test)
                            # print("Patient Name: "+getPatientName)   
                            # print("Status: "+ status)
                            
                            clickClosePatientInfoButton = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[5]/div[2]/div/div/div[2]/div[1]/div[1]/button")
                            clickClosePatientInfoButton.click()
                            
                        clickCloseBreakdownButton = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[5]/div/div/div/div[1]/button")
                        clickCloseBreakdownButton.click()
                    else:
                        clickCloseBreakdownButton = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[5]/div/div/div/div[1]/button")
                        clickCloseBreakdownButton.click()
                    
                    
                   
                    
                    

                checkIfTheresDataInTable = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[3]/div/div/div/div[1]/div[1]/ul")
                
                clickPrvdrFilter = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div[1]/div/button")
                clickPrvdrFilter.click()

                unclickSelectedProvider = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div[1]/div/div/div[2]/ul/li["+str(i+1)+"]/span/span[1]")
                unclickSelectedProvider.click()

                clickApplyButtons = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div[1]/div/div/div[3]/button[2]")
                clickApplyButtons.click()

                checkIfTheresDataInTable = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[3]/div/div/div/div[1]/div[1]/ul")
                stopper = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[1]/div/div/div/div[3]/button[contains(text(), 'Refresh')]")
            if countAllDataInTable == 0:
                checkIfTheresDataInTable = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[3]/div/div/div/div[1]/div[1]/ul")
                
                clickPrvdrFilter = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div[1]/div/button")
                clickPrvdrFilter.click()

                unclickSelectedProvider = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div[1]/div/div/div[2]/ul/li["+str(i+1)+"]/span/span[1]")
                unclickSelectedProvider.click()

                clickApplyButtons = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div[1]/div/div/div[3]/button[2]")
                clickApplyButtons.click()


                checkIfTheresDataInTable = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[3]/div/div/div/div[1]/div[1]/ul")
                stopper = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[1]/div/div/div/div[3]/button[contains(text(), 'Refresh')]")
        else:
            break
        
    return driver

    # print(numberOfProviderItHasData)
    # print(providerArray)

    