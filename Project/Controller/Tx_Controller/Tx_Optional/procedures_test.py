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
from .... import db
import sqlite3
import re


def procedureTestTx(driver, test_code, test_month):

    driver.implicitly_wait(1000000000)

    checkIfTheresDataInTable = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[3]/div/div/div/div[1]/div[1]/div/ul")
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
        
        
    checkIfTheresDataInTable = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[3]/div/div/div/div[1]/div[1]/div/ul")
    stopper = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[1]/div/div/div/div[3]/button[contains(text(), 'Refresh')]")

    # time.sleep(3)
    
    clickProcedureFilter = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div[2]/div/button")
    clickProcedureFilter.click()

    getAllProcedureInProcedureFilter = driver.find_elements(By.XPATH, '/html/body/div[1]/main/div[2]/div[2]/div/div/div[2]/ul/li')
    countAllProcedure = len(getAllProcedureInProcedureFilter)
    

    # print(countAllProcedure)

    clickCancelButton = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div[2]/div/div/div[3]/button[1]")
    clickCancelButton.click()

    numberOfProcedureItHasData = 0
    procedureArray = []

    checkIfTheresDataInTable = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[3]/div/div/div/div[1]/div[1]/div/ul")

    stopper = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[1]/div/div/div/div[3]/button[contains(text(), 'Refresh')]")

    for i in range(countAllProcedure):
        if numberOfProcedureItHasData < 3:
            checkIfTheresDataInTable = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[3]/div/div/div/div[1]/div[1]/div/ul")
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


            checkIfTheresDataInTable = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[3]/div/div/div/div[1]/div[1]/div/ul")
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

                            time.sleep(3)
                            checkIfTableAlreadyLoaded = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[5]/div[2]/div/div/div[2]/div[2]/div/div/div/div/table/tbody/tr[1]/td[1]").text 


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
                                txPlanProcedureCode = "NONEEE"
                                txPlanProcedureDesc = "NONEEE"

                                if checkIfItsNoDataTXplan == "No Data":
                                    print("FAILLLLLLLLLLLL")
                                    new_txminer_procedure = TxMinerProcedureTest(user_id = current_user.id,
                                        test_code = test_code,
                                        month_breakdown = getMonth,
                                        procedure_code_filtered = getProcedureCodeNumber,
                                        procedure_desc_filtered = getProcedureCodeDesc,
                                        procedure_code_table = "No Data",
                                        procedure_desc_table = "No Data",
                                        status = "Fail",
                                        created_at = datetime.now(),
                                        updated_at = datetime.now())
                                    
                                    db.session.add(new_txminer_procedure)
                                    db.session.commit()
                                else:
                                    for b in range(lengthOfCountTXPlanData):
                                        getTXPlanDate = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[5]/div[2]/div/div/div[2]/div[2]/div/div/div/div/table/tbody/tr["+str(b+1)+"]/td[8]").text
                                        month_txplan = datetime.strptime(getTXPlanDate, '%b %d, %Y')
                                        month_txplan = month_txplan.strftime("%Y-%m")

                                        table_month = datetime.strptime(getMonth, '%B %Y')
                                        table_month = table_month.strftime("%Y-%m")
                                        if month_txplan == table_month:
                                            getProcedureCodeTXPlan = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[5]/div[2]/div/div/div[2]/div[2]/div/div/div/div/table/tbody/tr["+str(b+1)+"]/td[1]").text
                                            getProcedureDescTXPlan = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[5]/div[2]/div/div/div[2]/div[2]/div/div/div/div/table/tbody/tr["+str(b+1)+"]/td[2]").text
                                            if getProcedureCodeNumber == getProcedureCodeTXPlan and getProcedureCodeDesc == getProcedureDescTXPlan:
                                                txPlanProcedureCode = getProcedureCodeTXPlan
                                                txPlanProcedureDesc = getProcedureDescTXPlan
                                                statusBreaker = 1
                                                break
                                    if statusBreaker == 1: 
                                        print("Pass")
                                        
                                        new_txminer_procedure = TxMinerProcedureTest(user_id = current_user.id,
                                            test_code = test_code,
                                            month_breakdown = getMonth,
                                            procedure_code_filtered = getProcedureCodeNumber,
                                            procedure_desc_filtered = getProcedureCodeDesc,
                                            procedure_code_table = txPlanProcedureCode,
                                            procedure_desc_table = txPlanProcedureDesc,
                                            status = "Pass",
                                            created_at = datetime.now(),
                                            updated_at = datetime.now())
                                        
                                        db.session.add(new_txminer_procedure)
                                        db.session.commit()
                                    else: 
                                        print("FAIIIIIIIIIIIIIIIIIIIIIIIL")
                                        new_txminer_procedure = TxMinerProcedureTest(user_id = current_user.id,
                                            test_code = test_code,
                                            month_breakdown = getMonth,
                                            procedure_code_filtered = getProcedureCodeNumber,
                                            procedure_desc_filtered = getProcedureCodeDesc,
                                            procedure_code_table = "No Data",
                                            procedure_desc_table = "No Data",
                                            status = "Fail",
                                            created_at = datetime.now(),
                                            updated_at = datetime.now())
                                        
                                        db.session.add(new_txminer_procedure)
                                        db.session.commit()
                            else:
                                time.sleep(3)
                                countLedgerData = driver.find_elements(By.XPATH, "/html/body/div[1]/main/div[5]/div[2]/div/div/div[2]/div[2]/div/div/div/div/table/tbody/tr/td[1]")
                                lengthOfCountLedgerData = len(countLedgerData)
                                ledgerProcedureCode = "NONEEE"
                                ledgerProcedureDesc = "NONEEE"
                                

                                for w in range(lengthOfCountLedgerData):
                                    getLedgerDates = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[5]/div[2]/div/div/div[2]/div[2]/div/div/div/div/table/tbody/tr["+str(w+1)+"]/td[7]").text
                                    month_ledger = datetime.strptime(getLedgerDates, '%b %d, %Y')
                                    month_ledger = month_ledger.strftime("%Y-%m")

                                    table_month = datetime.strptime(getMonth, '%B %Y')
                                    table_month = table_month.strftime("%Y-%m")
                                    # print(month_ledger + ' and ' + table_month)
                                    if table_month == month_ledger:
                                        getLedgerProcedureCode = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[5]/div[2]/div/div/div[2]/div[2]/div/div/div/div/table/tbody/tr["+str(w+1)+"]/td[1]").text
                                        getLedgerProcedureDesc = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[5]/div[2]/div/div/div[2]/div[2]/div/div/div/div/table/tbody/tr["+str(w+1)+"]/td[2]").text
                                        
                                        if getProcedureCodeNumber == getLedgerProcedureCode and getProcedureCodeDesc == getLedgerProcedureDesc:
                                            print('From Filter::' + getProcedureCodeNumber + ' and ' + getProcedureCodeDesc)
                                            print('From Ledger::' + getLedgerProcedureCode + ' and ' + getLedgerProcedureDesc)
                                            ledgerProcedureCode = getLedgerProcedureCode
                                            ledgerProcedureDesc = getLedgerProcedureDesc
                                            statusBreaker = 1
                                            break
                                if statusBreaker != 1: 
                                    print("------------ Checking in TX Plan ------------")
                                    clickTxPlans = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[5]/div[2]/div/div/div[2]/div[1]/ul/li[5]/a")
                                    clickTxPlans.click()
                                    time.sleep(3)
                                    
                                    checkIfItsNoData = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[5]/div[2]/div/div/div[2]/div[2]/div/div/div/div/table/tbody/tr/td").text
                                    if checkIfItsNoData == "No Data":
                                        print("FAILLLLLLLLLLLL")
                                        new_txminer_procedure = TxMinerProcedureTest(user_id = current_user.id,
                                            test_code = test_code,
                                            month_breakdown = getMonth,
                                            procedure_code_filtered = getProcedureCodeNumber,
                                            procedure_desc_filtered = getProcedureCodeDesc,
                                            procedure_code_table = "No Data",
                                            procedure_desc_table = "No Data",
                                            status = "Fail",
                                            created_at = datetime.now(),
                                            updated_at = datetime.now())
                                        
                                        db.session.add(new_txminer_procedure)
                                        db.session.commit()
                                    else:
                                        countTXPlanData = driver.find_elements(By.XPATH, "/html/body/div[1]/main/div[5]/div[2]/div/div/div[2]/div[2]/div/div/div/div/table/tbody/tr/td[1]")
                                        lengthOfCountTXPlanData = len(countTXPlanData)
                                        txPlanProcedureCode = "NONEEE"
                                        txPlanProcedureDesc = "NONEEE"

                                        for b in range(lengthOfCountTXPlanData):
                                            getTXPlanDate = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[5]/div[2]/div/div/div[2]/div[2]/div/div/div/div/table/tbody/tr["+str(b+1)+"]/td[8]").text
                                            month_txplan = datetime.strptime(getTXPlanDate, '%b %d, %Y')
                                            month_txplan = month_txplan.strftime("%Y-%m")

                                            table_month = datetime.strptime(getMonth, '%B %Y')
                                            table_month = table_month.strftime("%Y-%m")
                                            if month_txplan == table_month:
                                                getProcedureCodeTXPlan = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[5]/div[2]/div/div/div[2]/div[2]/div/div/div/div/table/tbody/tr["+str(b+1)+"]/td[1]").text
                                                getProcedureDescTXPlan = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[5]/div[2]/div/div/div[2]/div[2]/div/div/div/div/table/tbody/tr["+str(b+1)+"]/td[2]").text
                                                if getProcedureCodeNumber == getProcedureCodeTXPlan and getProcedureCodeDesc == getProcedureDescTXPlan:
                                                    txPlanProcedureCode = getProcedureCodeTXPlan
                                                    txPlanProcedureDesc = getProcedureDescTXPlan
                                                    statusBreaker = 1
                                                    break
                                        if statusBreaker == 1: 
                                            print("Pass")
                                            new_txminer_procedure = TxMinerProcedureTest(user_id = current_user.id,
                                                test_code = test_code,
                                                month_breakdown = getMonth,
                                                procedure_code_filtered = getProcedureCodeNumber,
                                                procedure_desc_filtered = getProcedureCodeDesc,
                                                procedure_code_table = txPlanProcedureCode,
                                                procedure_desc_table = txPlanProcedureDesc,
                                                status = "Pass",
                                                created_at = datetime.now(),
                                                updated_at = datetime.now())
                                            
                                            db.session.add(new_txminer_procedure)
                                            db.session.commit()
                                        else: 
                                            print("FAILLLLLLLLLLLL")
                                            new_txminer_procedure = TxMinerProcedureTest(user_id = current_user.id,
                                                test_code = test_code,
                                                month_breakdown = getMonth,
                                                procedure_code_filtered = getProcedureCodeNumber,
                                                procedure_desc_filtered = getProcedureCodeDesc,
                                                procedure_code_table = "No Data",
                                                procedure_desc_table = "No Data",
                                                status = "Fail",
                                                created_at = datetime.now(),
                                                updated_at = datetime.now())
                                            
                                            db.session.add(new_txminer_procedure)
                                            db.session.commit()  
                                else:
                                    print("PASS")
                                    new_txminer_procedure = TxMinerProcedureTest(user_id = current_user.id,
                                        test_code = test_code,
                                        month_breakdown = getMonth,
                                        procedure_code_filtered = getProcedureCodeNumber,
                                        procedure_desc_filtered = getProcedureCodeDesc,
                                        procedure_code_table = ledgerProcedureCode,
                                        procedure_desc_table = ledgerProcedureDesc,
                                        status = "Pass",
                                        created_at = datetime.now(),
                                        updated_at = datetime.now())
                                    
                                    db.session.add(new_txminer_procedure)
                                    db.session.commit()         
                                        

                            clickClosePatientInfoButton = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[5]/div[2]/div/div/div[2]/div[1]/div[1]/button")
                            clickClosePatientInfoButton.click()

                        clickCloseBreakdownButton = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[5]/div/div/div/div[1]/button")
                        clickCloseBreakdownButton.click()  
                    else:
                        clickCloseBreakdownButton = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[5]/div/div/div/div[1]/button")
                        clickCloseBreakdownButton.click()   

                checkIfTheresDataInTable = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[3]/div/div/div/div[1]/div[1]/div/ul")
                    
                clickProceduresFilters = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div[2]/div/button")
                clickProceduresFilters.click()

                unclickSelectedProcedure = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div[2]/div/div/div[2]/ul/li["+str(i+1)+"]/span/span[1]")
                unclickSelectedProcedure.click()

                clickApplyButtons = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div[2]/div/div/div[3]/button[2]")
                clickApplyButtons.click()

                checkIfTheresDataInTable = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[3]/div/div/div/div[1]/div[1]/div/ul")
                stopper = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[1]/div/div/div/div[3]/button[contains(text(), 'Refresh')]")


            if countAllDataInTable == 0:
                checkIfTheresDataInTable = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[3]/div/div/div/div[1]/div[1]/div/ul")
                    
                clickProceduresFilters = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div[2]/div/button")
                clickProceduresFilters.click()

                unclickSelectedProcedure = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div[2]/div/div/div[2]/ul/li["+str(i+1)+"]/span/span[1]")
                unclickSelectedProcedure.click()

                clickApplyButtons = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div[2]/div/div/div[3]/button[2]")
                clickApplyButtons.click()

                checkIfTheresDataInTable = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[3]/div/div/div/div[1]/div[1]/div/ul")
                stopper = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[1]/div/div/div/div[3]/button[contains(text(), 'Refresh')]")
        else:
            break
    return driver