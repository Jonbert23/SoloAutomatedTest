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

            getProviderTextInProviderFilter = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div[1]/div/div/div[2]/ul/li["+str(i+1)+"]/span/span[2]").text
            splitGetProviderTextInProviderFilter = getProviderTextInProviderFilter.split(" - ")
            providerInFilter = splitGetProviderTextInProviderFilter[0]
            # print(splitGetProviderTextInProviderFilter[0])
            clickSelectedProvider = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div[1]/div/div/div[2]/ul/li["+str(i+1)+"]/span/span[1]")
            clickSelectedProvider.click()

            clickApplyButton = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div[1]/div/div/div[3]/button[2]")
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
                            clickLedger = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[5]/div[2]/div/div/div[2]/div[1]/ul/li[4]/a")
                            clickLedger.click()
                            
                            # checkIfTotalAlreadyLoaded = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[5]/div[2]/div/div/div[2]/div[2]/div/div/div[1]/div/div[1]/div/div/div[1]/h5").text 
                            time.sleep(3)
                            checkIfTableAlreadyLoaded = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[5]/div[2]/div/div/div[2]/div[2]/div/div/div/div/table/tbody/tr[1]/td[1]").text 
                            
                            
                            # countDataInTableTXPlans = driver.find_elements(By.XPATH, "/html/body/div[1]/main/div[5]/div[2]/div/div/div[2]/div[2]/div/div/div/div/table/tbody/tr/td[1]")
                            # countTXPlanData = len(countDataInTableTXPlans)

                            checkIfItsNoData = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[5]/div[2]/div/div/div[2]/div[2]/div/div/div/div/table/tbody/tr/td").text
                            # print(checkIfItsNoData)
                            statusBreaker = 0; 

                            if checkIfItsNoData == "No Data":
                                clickTxPlans = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[5]/div[2]/div/div/div[2]/div[1]/ul/li[5]/a")
                                clickTxPlans.click()
                                time.sleep(3)

                                checkIfItsNoDataTXplan = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[5]/div[2]/div/div/div[2]/div[2]/div/div/div/div/table/tbody/tr/td").text
                                # print(checkIfItsNoData)
                                statusBreaker = 0; 

                                if checkIfItsNoDataTXplan == "No Data":
                                    print("FAILLLLLLLLLLLL")
                                    new_txminer_provider = TxMinerProviderTest(user_id = current_user.id,
                                        test_code = test_code,
                                        month_breakdown = getMonth,
                                        pt_name = "No Data",
                                        provider_filtered = providerInFilter,
                                        provider_pt_table = "No Data",
                                        status = "Fail",
                                        created_at = datetime.now(),
                                        updated_at = datetime.now())
                                    
                                    db.session.add(new_txminer_provider)
                                    db.session.commit()
                                else:
                                    countTXPlanData = driver.find_elements(By.XPATH, "/html/body/div[1]/main/div[5]/div[2]/div/div/div[2]/div[2]/div/div/div/div/table/tbody/tr/td[1]")
                                    lengthOfCountTXPlanData = len(countTXPlanData)
                                    txPlanProvider = "NONEEE"
                                    for b in range(lengthOfCountTXPlanData):
                                        getTXPlanDate = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[5]/div[2]/div/div/div[2]/div[2]/div/div/div/div/table/tbody/tr["+str(b+1)+"]/td[8]").text
                                        month_txplan = datetime.strptime(getTXPlanDate, '%b %d, %Y')
                                        month_txplan = month_txplan.strftime("%Y-%m")

                                        table_month = datetime.strptime(getMonth, '%B %Y')
                                        table_month = table_month.strftime("%Y-%m")
                                        if month_txplan == table_month:
                                            getProviderTXPlan = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[5]/div[2]/div/div/div[2]/div[2]/div/div/div/div/table/tbody/tr["+str(b+1)+"]/td[6]").text
                                            if providerInFilter == getProviderTXPlan:
                                                txPlanProvider = getProviderTXPlan
                                                statusBreaker = 1
                                                break
                                    if statusBreaker == 1: 
                                        print("Month Breakdown: "+getMonth)
                                        print("Patient Name: "+getPatientName)   
                                        print("Provider Name Filtered: "+providerInFilter)
                                        print("Provider Name Ledger: "+txPlanProvider)
                                        print("Status: "+ str(statusBreaker))
                                        new_txminer_provider = TxMinerProviderTest(user_id = current_user.id,
                                            test_code = test_code,
                                            month_breakdown = getMonth,
                                            pt_name = getPatientName,
                                            provider_filtered = providerInFilter,
                                            provider_pt_table = txPlanProvider,
                                            status = "Pass",
                                            created_at = datetime.now(),
                                            updated_at = datetime.now())
                                        
                                        db.session.add(new_txminer_provider)
                                        db.session.commit()
                                    else: 
                                        print("FAIIIIIIIIIIIIIIIIIIIIIIIL")
                                        new_txminer_provider = TxMinerProviderTest(user_id = current_user.id,
                                            test_code = test_code,
                                            month_breakdown = getMonth,
                                            pt_name = "No Data",
                                            provider_filtered = providerInFilter,
                                            provider_pt_table = "No Data",
                                            status = "Fail",
                                            created_at = datetime.now(),
                                            updated_at = datetime.now())
                                        
                                        db.session.add(new_txminer_provider)
                                        db.session.commit()
                            else:
                                countLedgerData = driver.find_elements(By.XPATH, "/html/body/div[1]/main/div[5]/div[2]/div/div/div[2]/div[2]/div/div/div/div/table/tbody/tr/td[1]")
                                lengthOfCountLedgerData = len(countLedgerData)
                                ledgerProvider = "NONEEE"
                                for w in range(lengthOfCountLedgerData):
                                    getLedgerDate = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[5]/div[2]/div/div/div[2]/div[2]/div/div/div/div/table/tbody/tr["+str(w+1)+"]/td[7]").text
                                    month_ledger = datetime.strptime(getLedgerDate, '%b %d, %Y')
                                    month_ledger = month_ledger.strftime("%Y-%m")

                                    table_month = datetime.strptime(getMonth, '%B %Y')
                                    table_month = table_month.strftime("%Y-%m")

                                    if table_month == month_ledger:
                                        getLedgerProviderName = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[5]/div[2]/div/div/div[2]/div[2]/div/div/div/div/table/tbody/tr["+str(w+1)+"]/td[6]").text
                                        # print(table_month + ' CONDTION ' + providerInFilter)
                                        # print(month_ledger + ' and ' + getLedgerProviderName)
                                        if providerInFilter == getLedgerProviderName:
                                            ledgerProvider = getLedgerProviderName
                                            statusBreaker = 1
                                            break

                                if statusBreaker != 1: 
                                    print("------------ Checking in TX Plan ------------")
                                    clickTxPlans = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[5]/div[2]/div/div/div[2]/div[1]/ul/li[5]/a")
                                    clickTxPlans.click()
                                    time.sleep(3)

                                    checkIfItsNoData = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[5]/div[2]/div/div/div[2]/div[2]/div/div/div/div/table/tbody/tr/td").text
                                    # print(checkIfItsNoData)
                                    # statusBreaker = 0; 

                                    if checkIfItsNoData == "No Data":
                                        print("FAILLLLLLLLLLLL")
                                        new_txminer_provider = TxMinerProviderTest(user_id = current_user.id,
                                            test_code = test_code,
                                            month_breakdown = getMonth,
                                            pt_name = "No Data",
                                            provider_filtered = providerInFilter,
                                            provider_pt_table = "No Data",
                                            status = "Fail",
                                            created_at = datetime.now(),
                                            updated_at = datetime.now())
                                        
                                        db.session.add(new_txminer_provider)
                                        db.session.commit()
                                    else:
                                        countTXPlanData = driver.find_elements(By.XPATH, "/html/body/div[1]/main/div[5]/div[2]/div/div/div[2]/div[2]/div/div/div/div/table/tbody/tr/td[1]")
                                        lengthOfCountTXPlanData = len(countTXPlanData)
                                        txPlanProvider = "NONEEE"
                                        for b in range(lengthOfCountTXPlanData):
                                            getTXPlanDate = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[5]/div[2]/div/div/div[2]/div[2]/div/div/div/div/table/tbody/tr["+str(b+1)+"]/td[8]").text
                                            month_txplan = datetime.strptime(getTXPlanDate, '%b %d, %Y')
                                            month_txplan = month_txplan.strftime("%Y-%m")

                                            table_month = datetime.strptime(getMonth, '%B %Y')
                                            table_month = table_month.strftime("%Y-%m")
                                            if month_txplan == table_month:
                                                getProviderTXPlan = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[5]/div[2]/div/div/div[2]/div[2]/div/div/div/div/table/tbody/tr["+str(b+1)+"]/td[6]").text
                                                if providerInFilter == getProviderTXPlan:
                                                    txPlanProvider = getProviderTXPlan
                                                    statusBreaker = 1
                                                    break
                                        if statusBreaker == 1: 
                                            print("Month Breakdown: "+getMonth)
                                            print("Patient Name: "+getPatientName)   
                                            print("Provider Name Filtered: "+providerInFilter)
                                            print("Provider Name Ledger: "+txPlanProvider)
                                            print("Status: "+ str(statusBreaker))
                                            new_txminer_provider = TxMinerProviderTest(user_id = current_user.id,
                                                test_code = test_code,
                                                month_breakdown = getMonth,
                                                pt_name = getPatientName,
                                                provider_filtered = providerInFilter,
                                                provider_pt_table = txPlanProvider,
                                                status = "Pass",
                                                created_at = datetime.now(),
                                                updated_at = datetime.now())
                                            
                                            db.session.add(new_txminer_provider)
                                            db.session.commit()
                                        else: 
                                            print("FAILLLLLLLLLLLL")
                                            new_txminer_provider = TxMinerProviderTest(user_id = current_user.id,
                                                test_code = test_code,
                                                month_breakdown = getMonth,
                                                pt_name = "No Data",
                                                provider_filtered = providerInFilter,
                                                provider_pt_table = "No Data",
                                                status = "Fail",
                                                created_at = datetime.now(),
                                                updated_at = datetime.now())
                                            
                                            db.session.add(new_txminer_provider)
                                            db.session.commit()
                                else:
                                    print("Month Breakdown: "+getMonth)
                                    print("Patient Name: "+getPatientName)   
                                    print("Provider Name Filtered: "+providerInFilter)
                                    print("Provider Name Ledger: "+ledgerProvider)
                                    print("Status: "+ str(statusBreaker))
                                    new_txminer_provider = TxMinerProviderTest(user_id = current_user.id,
                                        test_code = test_code,
                                        month_breakdown = getMonth,
                                        pt_name = getPatientName,
                                        provider_filtered = providerInFilter,
                                        provider_pt_table = ledgerProvider,
                                        status = "Pass",
                                        created_at = datetime.now(),
                                        updated_at = datetime.now())
                                    
                                    db.session.add(new_txminer_provider)
                                    db.session.commit()
                            
                            
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

    driver.quit()
    # return driver

    # print(numberOfProviderItHasData)
    # print(providerArray)

    