from decimal import Decimal
from selenium import webdriver
from selenium.webdriver.common.by import By
from flask_login import login_required, current_user
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from ...Global_Controller import Range_date_picker
import time 
from datetime import datetime
from .... import db
from ....models import DashboardV2DefaultSearchProcedure
from ....models import DashboardV2DefaultCountTest
import sqlite3
import re


def defaultServicesTest(driver, test_code, test_month, test_date_from, test_date_to):
    start_date = test_date_from
    end_date = test_date_to
    driver.implicitly_wait(1000000)

    time.sleep(3)
    
    getIfItHasData = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/section[4]/div/div[2]/div/div/table/tbody/tr[1]/td[1]").text

    Range_date_picker.DateFilter.rangePicker(driver, start_date, end_date)
    
    clickUpdateButton = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[1]/div/div/div/div[3]/button")
    clickUpdateButton.click()
    time.sleep(3)


    getIfItHasData = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/section[4]/div/div[2]/div/div/table/tbody/tr[1]/td[1]").text

    if getIfItHasData == "No data":
        # new_dash_search_test = DashboardV2DefaultSearchProcedure(user_id = current_user.id,
        #     test_code = test_code,
        #     main_proc_code = "No data",
        #     breakdown_proc_code = "No data",
        #     status = "Pass",
        #     created_at = datetime.now(),
        #     updated_at = datetime.now())

        # db.session.add(new_dash_search_test)
        # db.session.commit()
        print("NO DATA NIIII !!")
    else:
        countDataInTableServices = driver.find_elements(By.XPATH, "/html/body/div[1]/main/div[2]/section[4]/div/div[2]/div/div/table/tbody/tr/td[3]")
        lengthInTableServices = len(countDataInTableServices)
        print(lengthInTableServices)

        for m in range(lengthInTableServices):
            if lengthInTableServices > 10:
                if m != 10:
                    getProcCode = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/section[4]/div/div[2]/div/div/table/tbody/tr["+str(m+1)+"]/td[3]").text
                    clickSearchBar = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/section[4]/div/div[1]/div[2]/div[1]/input")
                    clickSearchBar.send_keys(getProcCode)

                    time.sleep(2)

                    countTableServices = driver.find_elements(By.XPATH, "/html/body/div[1]/main/div[2]/section[4]/div/div[2]/div/div/table/tbody/tr/td[3]")
                    lengthTableServices = len(countTableServices)

                    status = ""
                    breakdownProcCode = ""
                    for n in range(lengthTableServices):
                        getProdCodeTable = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/section[4]/div/div[2]/div/div/table/tbody/tr["+str(n+1)+"]/td[3]").text
                        
                        if getProcCode == getProdCodeTable:
                            breakdownProcCode = getProdCodeTable
                            status = "Pass"
                        else: 
                            print(getProcCode)
                            print(getProdCodeTable)
                            getProdCodeTable = getProdCodeTable
                            status = "Fail"
                            break
                    

                    new_dash_search_test = DashboardV2DefaultSearchProcedure(user_id = current_user.id,
                        test_code = test_code,
                        main_proc_code = getProcCode,
                        breakdown_proc_code = getProdCodeTable,
                        status = status,
                        created_at = datetime.now(),
                        updated_at = datetime.now())

                    db.session.add(new_dash_search_test)
                    db.session.commit()

                    print(getProcCode)
                    print(getProdCodeTable)
                    print(status)


                    ActionChains(driver) \
                        .key_down(Keys.CONTROL) \
                        .click(clickSearchBar) \
                        .key_up(Keys.CONTROL) \
                        .perform()
                    clickSearchBar.send_keys(Keys.DELETE)

                    
                        
                else:
                    break
            else:
                getProcCode = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/section[4]/div/div[2]/div/div/table/tbody/tr["+str(m+1)+"]/td[3]").text
                clickSearchBar = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/section[4]/div/div[1]/div[2]/div[1]/input")
                clickSearchBar.send_keys(getProcCode)

                time.sleep(2)

                countTableServices = driver.find_elements(By.XPATH, "/html/body/div[1]/main/div[2]/section[4]/div/div[2]/div/div/table/tbody/tr/td[3]")
                lengthTableServices = len(countTableServices)

                status = ""
                breakdownProcCode = ""
                for n in range(lengthTableServices):
                    getProdCodeTable = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/section[4]/div/div[2]/div/div/table/tbody/tr["+str(n+1)+"]/td[3]").text
                    
                    if getProcCode == getProdCodeTable:
                        breakdownProcCode = getProdCodeTable
                        status = "Pass"
                    else: 
                        print(getProcCode)
                        print(getProdCodeTable)
                        breakdownProcCode = getProdCodeTable
                        status = "Fail"
                        break

                new_dash_search_test = DashboardV2DefaultSearchProcedure(user_id = current_user.id,
                    test_code = test_code,
                    main_proc_code = getProcCode,
                    breakdown_proc_code = getProdCodeTable,
                    status = status,
                    created_at = datetime.now(),
                    updated_at = datetime.now())

                db.session.add(new_dash_search_test)
                db.session.commit()

                print(getProcCode)
                print(getProdCodeTable)
                print(status)


                ActionChains(driver) \
                    .key_down(Keys.CONTROL) \
                    .click(clickSearchBar) \
                    .key_up(Keys.CONTROL) \
                    .perform()
                clickSearchBar.send_keys(Keys.DELETE)

        time.sleep(3)    


    checkIfItHasData = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/section[4]/div/div[2]/div/div/table/tbody/tr[1]/td[1]").text

    if checkIfItHasData == "No data":
        print("NO DATAAAA COUNT!!!!")
    else:
        countingDataInTableServices = driver.find_elements(By.XPATH, "/html/body/div[1]/main/div[2]/section[4]/div/div[2]/div/div/table/tbody/tr/td[3]")
        lengthDataTableServices = len(countingDataInTableServices)
        print(lengthDataTableServices)

        for y in range(lengthDataTableServices):
            if lengthDataTableServices > 10:
                if y != 10:
                    getMainProcCode = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/section[4]/div/div[2]/div/div/table/tbody/tr["+str(y+1)+"]/td[3]").text
                    getMainCount = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/section[4]/div/div[2]/div/div/table/tbody/tr["+str(y+1)+"]/td[5]/span/span[1]/span").text

                    
                    clickCountBreakdown = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/section[4]/div/div[2]/div/div/table/tbody/tr["+str(y+1)+"]/td[5]/span/span[2]/a")
                    clickCountBreakdown.click()

                    checkIfBreakdownAlreadyLoad = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[3]/div/div/div/div[2]/section/div/div/div[2]/div/div[1]/table/tbody/tr[1]/td[1]").text

                    getBreakdownTotalCount = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[3]/div/div/div/div[2]/section/div/div/div[2]/div/div[1]/table/tr/td[5]").text

                    

                    status = ""
                    if getMainCount == getBreakdownTotalCount:
                        status = "Pass"
                    else:
                        status = "Fail"

                    print("MAIN PROCEDURE CODE AND COUNT: " + getMainProcCode + " " + getMainCount)
                    print("BREAKDOWN COUNT: " + getBreakdownTotalCount)
                    print("Status: " + status)

                    new_dash_count_test = DashboardV2DefaultCountTest(user_id = current_user.id,
                        test_code = test_code,
                        main_proc_code = getMainProcCode,
                        main_count = getMainCount,
                        breakdown_count = getBreakdownTotalCount,
                        status = status,
                        created_at = datetime.now(),
                        updated_at = datetime.now())

                    db.session.add(new_dash_count_test)
                    db.session.commit()

                    closeBreakdown = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[3]/div/div/div/div[2]/div/button")
                    closeBreakdown.click()

                else:
                    break
            else:
                getMainProcCode = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/section[4]/div/div[2]/div/div/table/tbody/tr["+str(y+1)+"]/td[3]").text
                getMainCount = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/section[4]/div/div[2]/div/div/table/tbody/tr["+str(y+1)+"]/td[5]/span/span[1]/span").text
                clickCountBreakdown = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/section[4]/div/div[2]/div/div/table/tbody/tr["+str(y+1)+"]/td[5]/span/span[2]/a")
                clickCountBreakdown.click()

                checkIfBreakdownAlreadyLoad = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[3]/div/div/div/div[2]/section/div/div/div[2]/div/div[1]/table/tbody/tr[1]/td[1]").text

                getBreakdownTotalCount = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[3]/div/div/div/div[2]/section/div/div/div[2]/div/div[1]/table/tr/td[5]").text

                

                status = ""
                if getMainCount == getBreakdownTotalCount:
                    status = "Pass"
                else:
                    status = "Fail"

                print("MAIN PROCEDURE CODE AND COUNT: " + getMainProcCode + " " + getMainCount)
                print("BREAKDOWN COUNT: " + getBreakdownTotalCount)
                print("Status: " + status)

                new_dash_count_test = DashboardV2DefaultCountTest(user_id = current_user.id,
                    test_code = test_code,
                    main_proc_code = getMainProcCode,
                    main_count = getMainCount,
                    breakdown_count = getBreakdownTotalCount,
                    status = status,
                    created_at = datetime.now(),
                    updated_at = datetime.now())

                db.session.add(new_dash_count_test)
                db.session.commit()

                closeBreakdown = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[3]/div/div/div/div[2]/div/button")
                closeBreakdown.click()
                

    return driver




    