from selenium import webdriver
from selenium.webdriver.common.by import By
from flask_login import login_required, current_user
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time 
from datetime import datetime
from ....models import CalendarFilterUse
from ....models import CalendarFilterTesting
from .... import db
import sqlite3
import re


def procedureFilterTest(driver, test_code):
    driver.implicitly_wait(1000000000)
    new_provider = CalendarFilterUse(user_id = current_user.id,
        test_code = test_code,
        filter_name = "Procedure Filter",
        created_at = datetime.now(),
        updated_at = datetime.now())
    
    db.session.add(new_provider)  
    db.session.commit()

    getProvider = CalendarFilterUse.query.filter_by(test_code=test_code).filter_by(filter_name='Procedure Filter').order_by(CalendarFilterUse.id.desc()).first()

    stopperGetLoc = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[2]/div/div[2]/div[1]/table/tbody/tr[1]/td[1]/span/span").text
    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/main/div[2]/span/div[1]/div/div[3]/div/button'))) 
    
    getAllDataInsideTbody = driver.find_elements(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[2]/div/div[2]/div[1]/table/tbody/tr")
    checkIfTheresData = len(getAllDataInsideTbody)


    if checkIfTheresData != 0:
        clickProcedureSort = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[2]/div/div[2]/div[1]/table/thead/tr/th[14]")
        clickProcedureSort.click()
        getText = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[2]/div/div[2]/div[2]/div[1]/div[2]/span").text
        splitNumberOfItems = getText.split("-")
        countData = splitNumberOfItems[-1]

        if int(countData) > 10:
            arrayOfProcedureCodeToTest = []
            splittingProcedureCode = ''
            for x in range(10):
                getProcedureCode = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[2]/div/div[2]/div[1]/table/tbody/tr["+str(x+1)+"]/td[14]").text
                if getProcedureCode != 'N/A':
                    splittingProcedureCode = getProcedureCode.split(', ')
                    # print(splittingProcedureCode)
                    
                    for y in range(len(splittingProcedureCode)):
                        temp = 0
                        # if len(arrayOfProcedureCodeToTest) == 0:
                        #     arrayOfProcedureCodeToTest.append(splittingProcedureCode[y])
                        # else:    
                        for z in range(len(arrayOfProcedureCodeToTest)):
                            if splittingProcedureCode[y] == arrayOfProcedureCodeToTest[z]:
                                temp = temp+1

                        if temp == 0:
                            if len(arrayOfProcedureCodeToTest) != 10:
                                arrayOfProcedureCodeToTest.append(splittingProcedureCode[y])

            countProcedure = len(arrayOfProcedureCodeToTest)
            print(arrayOfProcedureCodeToTest)
            for i in range(countProcedure):
                driver.implicitly_wait(1000000000)
                totalPass = 0
                totalFail = 0

                clickProcedureFilter = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[1]/div/div[2]/div/button")
                clickProcedureFilter.click()

                searchProcedures = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[1]/div/div[2]/div/div/div[1]/input").clear()   

                searchProcedure = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[1]/div/div[2]/div/div/div[1]/input")
                searchProcedure.send_keys(arrayOfProcedureCodeToTest[i])
                procedureCodeSearch = arrayOfProcedureCodeToTest[i]

                getProcShowInProcFitler = driver.find_elements(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[1]/div/div[2]/div/div/div[2]/ul/li/span/span[1]")
                countProcShowInProcFilter = len(getProcShowInProcFitler)

                # print(procedureCodeSearch)

                rangeProcLoc = 0
                for l in range(countProcShowInProcFilter):
                    getProcInProcFilterName = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[1]/div/div[2]/div/div/div[2]/ul/li["+str(l+1)+"]/span/span[1]").text
                    procInProcFilter = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[1]/div/div[2]/div/div/div[2]/ul/li["+str(l+1)+"]/span/span[1]")
                    if getProcInProcFilterName == procedureCodeSearch:
                        # print("LLLLLLLLL :"+str(l))
                        rangeProcLoc = l
                        procInProcFilter.click()
                        break
                        

                # clickPatient = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[1]/div/div[2]/div/div/div[2]/ul/li")
                # clickPatient.click()

                clickApplyButton = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[1]/div/div[2]/div/div/div[3]/button[2]")
                clickApplyButton.click()

                stopperGetLoc = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[2]/div/div[2]/div[1]/table/tbody/tr[1]/td[1]/span/span").text

                getText = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[2]/div/div[2]/div[2]/div[1]/div[2]/span").text
                splitNumberOfItems = getText.split("-")
                countDatas = splitNumberOfItems[-1]

                patient_name_pass = ''
                provider_pass = ''
                patient_name_fail = ''
                provider_fail = ''
                unsearch_proc_code = ''

                print(procedureCodeSearch)

                for j in range(int(countDatas)):  
                    getProcTextTables = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[2]/div/div[2]/div[1]/table/tbody/tr["+str(j+1)+"]/td[14]").text
                    
                    if procedureCodeSearch == getProcTextTables:
                        patient_name_pass = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[2]/div/div[2]/div[1]/table/tbody/tr["+str(j+1)+"]/td[2]/span/span[1]/span").text
                        provider_pass = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[2]/div/div[2]/div[1]/table/tbody/tr["+str(j+1)+"]/td[13]/span/span[1]/span").text
                        totalPass = totalPass + 1
                    else:
                        patient_name_fail = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[2]/div/div[2]/div[1]/table/tbody/tr["+str(j+1)+"]/td[2]/span/span[1]/span").text
                        provider_fail = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[2]/div/div[2]/div[1]/table/tbody/tr["+str(j+1)+"]/td[13]/span/span[1]/span").text
                        unsearch_proc_code = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[2]/div/div[2]/div[1]/table/tbody/tr["+str(j+1)+"]/td[14]").text
                        totalFail = totalFail + 1


                print("Total Pass: "+ str(totalPass))
                print("Total Fail: "+ str(totalFail))

                if totalFail == 0:
                    new_calendar_testing = CalendarFilterTesting(user_id = current_user.id,
                        test_code = test_code,
                        filter_id = getProvider.id,
                        search_provider = procedureCodeSearch,
                        patient_name = patient_name_pass,
                        procedure_code = provider_pass,
                        unsearch_provider = 'None',
                        status = 'Pass',
                        created_at = datetime.now(),
                        updated_at = datetime.now())

                    db.session.add(new_calendar_testing)
                    db.session.commit()
                else:
                    new_calendar_testing = CalendarFilterTesting(user_id = current_user.id,
                        test_code = test_code,
                        filter_id = getProvider.id,
                        search_provider = procedureCodeSearch,
                        patient_name = patient_name_fail,
                        procedure_code = provider_fail,
                        unsearch_provider = unsearch_proc_code,
                        status = 'Fail',
                        created_at = datetime.now(),
                        updated_at = datetime.now())
                    
                    db.session.add(new_calendar_testing)
                    db.session.commit()

                
                clickProcFilter = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[1]/div/div[2]/div/button")
                clickProcFilter.click()

                unclickProc = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[1]/div/div[2]/div/div/div[2]/ul/li["+str(rangeProcLoc+1)+"]/span/span[1]")
                unclickProc.click()

                searchPatient = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[1]/div/div[2]/div/div/div[1]/input").clear()

                clickApply= driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[1]/div/div[2]/div/div/div[3]/button[2]")
                clickApply.click()

                stopperGetLoc = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[2]/div/div[2]/div[1]/table/tbody/tr[1]/td[1]/span/span").text
                


            # countPatient = len(arrayOfProcedureCodeToTest)
        if int(countData) < 10:
            arrayOfProcedureCodeToTest = []
            splittingProcedureCode = ''
            for x in range(10):
                getProcedureCode = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[2]/div/div[2]/div[1]/table/tbody/tr["+str(x+1)+"]/td[14]").text
                if getProcedureCode != 'N/A':
                    splittingProcedureCode = getProcedureCode.split(', ')
                    # print(splittingProcedureCode)
                    
                    for y in range(len(splittingProcedureCode)):
                        temp = 0
                        # if len(arrayOfProcedureCodeToTest) == 0:
                        #     arrayOfProcedureCodeToTest.append(splittingProcedureCode[y])
                        # else:    
                        for z in range(len(arrayOfProcedureCodeToTest)):
                            if splittingProcedureCode[y] == arrayOfProcedureCodeToTest[z]:
                                temp = temp+1

                        if temp == 0:
                            if len(arrayOfProcedureCodeToTest) != 10:
                                arrayOfProcedureCodeToTest.append(splittingProcedureCode[y])

            countProcedure = len(arrayOfProcedureCodeToTest)
            print(arrayOfProcedureCodeToTest)
            for i in range(countProcedure):
                driver.implicitly_wait(1000000000)
                totalPass = 0
                totalFail = 0

                clickProcedureFilter = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[1]/div/div[2]/div/button")
                clickProcedureFilter.click()

                searchProcedures = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[1]/div/div[2]/div/div/div[1]/input").clear()   

                searchProcedure = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[1]/div/div[2]/div/div/div[1]/input")
                searchProcedure.send_keys(arrayOfProcedureCodeToTest[i])
                procedureCodeSearch = arrayOfProcedureCodeToTest[i]

                getProcShowInProcFitler = driver.find_elements(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[1]/div/div[2]/div/div/div[2]/ul/li/span/span[1]")
                countProcShowInProcFilter = len(getProcShowInProcFitler)

                # print(procedureCodeSearch)

                rangeProcLoc = 0
                for l in range(countProcShowInProcFilter):
                    getProcInProcFilterName = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[1]/div/div[2]/div/div/div[2]/ul/li["+str(l+1)+"]/span/span[1]").text
                    procInProcFilter = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[1]/div/div[2]/div/div/div[2]/ul/li["+str(l+1)+"]/span/span[1]")
                    if getProcInProcFilterName == procedureCodeSearch:
                        # print("LLLLLLLLL :"+str(l))
                        rangeProcLoc = l
                        procInProcFilter.click()
                        break
                        

                # clickPatient = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[1]/div/div[2]/div/div/div[2]/ul/li")
                # clickPatient.click()

                clickApplyButton = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[1]/div/div[2]/div/div/div[3]/button[2]")
                clickApplyButton.click()

                stopperGetLoc = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[2]/div/div[2]/div[1]/table/tbody/tr[1]/td[1]/span/span").text

                getText = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[2]/div/div[2]/div[2]/div[1]/div[2]/span").text
                splitNumberOfItems = getText.split("-")
                countDatas = splitNumberOfItems[-1]

                patient_name_pass = ''
                provider_pass = ''
                patient_name_fail = ''
                provider_fail = ''
                unsearch_proc_code = ''

                print(procedureCodeSearch)

                for j in range(int(countDatas)):  
                    getProcTextTables = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[2]/div/div[2]/div[1]/table/tbody/tr["+str(j+1)+"]/td[14]").text
                    
                    if procedureCodeSearch == getProcTextTables:
                        patient_name_pass = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[2]/div/div[2]/div[1]/table/tbody/tr["+str(j+1)+"]/td[2]/span/span[1]/span").text
                        provider_pass = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[2]/div/div[2]/div[1]/table/tbody/tr["+str(j+1)+"]/td[13]/span/span[1]/span").text
                        totalPass = totalPass + 1
                    else:
                        patient_name_fail = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[2]/div/div[2]/div[1]/table/tbody/tr["+str(j+1)+"]/td[2]/span/span[1]/span").text
                        provider_fail = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[2]/div/div[2]/div[1]/table/tbody/tr["+str(j+1)+"]/td[13]/span/span[1]/span").text
                        unsearch_proc_code = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[2]/div/div[2]/div[1]/table/tbody/tr["+str(j+1)+"]/td[14]").text
                        totalFail = totalFail + 1


                print("Total Pass: "+ str(totalPass))
                print("Total Fail: "+ str(totalFail))

                if totalFail == 0:
                    new_calendar_testing = CalendarFilterTesting(user_id = current_user.id,
                        test_code = test_code,
                        filter_id = getProvider.id,
                        search_provider = procedureCodeSearch,
                        patient_name = patient_name_pass,
                        procedure_code = provider_pass,
                        unsearch_provider = 'None',
                        status = 'Pass',
                        created_at = datetime.now(),
                        updated_at = datetime.now())

                    db.session.add(new_calendar_testing)
                    db.session.commit()
                else:
                    new_calendar_testing = CalendarFilterTesting(user_id = current_user.id,
                        test_code = test_code,
                        filter_id = getProvider.id,
                        search_provider = procedureCodeSearch,
                        patient_name = patient_name_fail,
                        procedure_code = provider_fail,
                        unsearch_provider = unsearch_proc_code,
                        status = 'Fail',
                        created_at = datetime.now(),
                        updated_at = datetime.now())
                    
                    db.session.add(new_calendar_testing)
                    db.session.commit()

                
                clickProcFilter = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[1]/div/div[2]/div/button")
                clickProcFilter.click()

                unclickProc = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[1]/div/div[2]/div/div/div[2]/ul/li["+str(rangeProcLoc+1)+"]/span/span[1]")
                unclickProc.click()

                searchPatient = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[1]/div/div[2]/div/div/div[1]/input").clear()

                clickApply= driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[1]/div/div[2]/div/div/div[3]/button[2]")
                clickApply.click()

                stopperGetLoc = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[2]/div/div[2]/div[1]/table/tbody/tr[1]/td[1]/span/span").text
    
    return driver