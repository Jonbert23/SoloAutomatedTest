from decimal import Decimal
from selenium import webdriver
from selenium.webdriver.common.by import By
from flask_login import login_required, current_user
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from ...Global_Controller import Range_date_picker
import time 
from datetime import datetime
from .... import db
from ....models import DashboardV2DefaultLOBTest
import sqlite3
import re



def defaultLobTest(driver, test_code, test_month, test_date_from, test_date_to):
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

    checkIfTableAlreadyLoad = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/section[3]/div[2]/div/div[2]/div/table/tbody/tr[1]/td[1]").text

    clickLobFilterButton = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[1]/div/div/div/div[3]/div/button")
    clickLobFilterButton.click()

    countLobOptions = driver.find_elements(By.XPATH, "/html/body/div[1]/main/div[1]/div/div/div/div[3]/div/div/div[2]/ul/li")
    lengthLobOptions = len(countLobOptions)

    clickTitle = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[1]/div/h1")
    clickTitle.click()

    for i in range(lengthLobOptions):

        scrollToTop = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[1]/div/h1")
        driver.execute_script("return arguments[0].scrollIntoView(true);", scrollToTop)

        clickLobFilterButtons = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[1]/div/div/div/div[3]/div/button")
        clickLobFilterButtons.click()

        clickClearButton = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[1]/div/div/div/div[3]/div/div/div[2]/div[1]/div/button[2]")
        clickClearButton.click()

        clickLobOptions = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[1]/div/div/div/div[3]/div/div/div[2]/ul/li["+str(i+1)+"]")
        clickLobOptions.click()

        getLabelOptions = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[1]/div/div/div/div[3]/div/div/div[2]/ul/li["+str(i+1)+"]").text
        # print(getLabelOptions)

        clickUpdateButton = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[1]/div/div/div/div[4]/button")
        clickUpdateButton.click()

        time.sleep(3)

        stopper = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/section[1]/div[1]").text
        stopper2nd = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/section[3]/div[2]/div/div[2]/div/table/tbody").text

        #HERES THE CROSSMATCHING STARTS
       

        ifIHasData = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/section[3]/div[2]/div/div[2]/div/table/tbody")

        driver.implicitly_wait(2)
        # ifIHasData = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/section[3]/div[2]/div/div[2]/div/table/tbody/tr")
        # print(lengthData)
        status = 1
        try:
            driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/section[3]/div[2]/div/div[2]/div/table/tbody/tr")
        except NoSuchElementException:
            status = 0

        driver.implicitly_wait(1000000)

        # print(status)
        if status == 1:
            countDataInTable = driver.find_elements(By.XPATH, "/html/body/div[1]/main/div[2]/section[3]/div[2]/div/div[2]/div/table/tbody/tr/td[1]")
            lengthDataInTable = len(countDataInTable)

            stopperLoop = 0
            for y in range(lengthDataInTable):
                if stopperLoop != 5:
                    getProviderName = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/section[3]/div[2]/div/div[2]/div/table/tbody/tr["+str(y+1)+"]/td[1]/span").text
                    clickProviderBr = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/section[3]/div[2]/div/div[2]/div/table/tbody/tr["+str(y+1)+"]/td[1]/span/span/a")
                    clickProviderBr.click()

                    time.sleep(2)
                    waitOpenBreakdownGender = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[3]/div/div/div/div[2]/div[2]/div/div/div[1]/div[1]/div[1]/h5").text
                    waitOpenBreakdownSpecialty = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[3]/div/div/div/div[2]/div[2]/div/div/div[1]/div[1]/div[2]/h5").text
                    waitOpenBreakdownProduction = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[3]/div/div/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[2]/h5").text

                    getSpecialty = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[3]/div/div/div/div[2]/div[2]/div/div/div[1]/div[1]/div[2]/h5").text
                    status = ""
                    if getLabelOptions == getSpecialty:
                        status = "Pass"
                    else:
                        status = "Fail"

                    #Need Database
                    print("LOB Options: " + getLabelOptions)
                    print("Provider Name in Table: " + getProviderName)
                    print("Provider Specialty: " + getSpecialty)
                    print("Status: " + status)
                    print("--------------------------------------------")

                    new_dash_lob_test = DashboardV2DefaultLOBTest(user_id = current_user.id,
                        test_code = test_code,
                        lob_options = getLabelOptions,
                        tbl_provider_name = getProviderName,
                        brkdwn_provider_specialty = getSpecialty,
                        status = status,
                        created_at = datetime.now(),
                        updated_at = datetime.now())

                    db.session.add(new_dash_lob_test)
                    db.session.commit()

                    closeBreakdown = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[3]/div/div/div/div[2]/div[1]/div[1]/button")
                    closeBreakdown.click()
                    stopperLoop = stopperLoop + 1
                else:
                    break
        else:
            print("LOB Options: " + getLabelOptions)
            print("Provider Name in Table: NO DATA")
            print("Provider Specialty: NO DATA")
            print("Status: NO DATA")
            print("--------------------------------------------")

            new_dash_lob_test = DashboardV2DefaultLOBTest(user_id = current_user.id,
                test_code = test_code,
                lob_options = getLabelOptions,
                tbl_provider_name = "No Data",
                brkdwn_provider_specialty = "No Data",
                status = "No Data",
                created_at = datetime.now(),
                updated_at = datetime.now())

            db.session.add(new_dash_lob_test)
            db.session.commit()

        #HERES THE CROSSMATCHING ENDS
    return driver