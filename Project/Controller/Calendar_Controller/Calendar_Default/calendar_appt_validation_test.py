from selenium import webdriver
from selenium.webdriver.common.by import By
from flask_login import login_required, current_user
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time 
from datetime import datetime
from ...Global_Controller import Range_date_picker
from ....models import CalendarFilterUse
from ....models import CalendarFilterTesting
from ....models import CalendarMetricTesting
from ....models import CalendarApptValidation
from .... import db
import sqlite3
import re


def apptValidationTest(driver, test_code, test_date_from, test_date_to):
    start_date = test_date_from
    end_date = test_date_to
    driver.implicitly_wait(1000000)
    stopperGetLoc = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[2]/div/div[2]/div[1]/table/tbody/tr[1]/td[1]/span/span").text

    Range_date_picker.DateFilter.rangePicker(driver, start_date, end_date)

    clickUpdateButton = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[1]/div/div/div/div[3]/button")
    clickUpdateButton.click()

    stopperGetLoc = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[2]/div/div[2]/div[1]/table/tbody/tr[1]/td[1]/span/span").text

    checkIfTheresData = driver.find_elements(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[2]/div/div[2]/div[1]/table/tbody/tr")
    countDataInTable = len(checkIfTheresData)

    if countDataInTable == 0:
        return "No Data in selected date range"
    if countDataInTable != 0:
        getText = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[2]/div/div[2]/div[2]/div[1]/div[2]/span").text
        splitNumberOfItems = getText.split("-")
        countData = splitNumberOfItems[-1]

        # print(countData)

        if int(countData) > 10:
            for i in range(5):
                getPatientName = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[2]/div/div[2]/div[1]/table/tbody/tr["+str(i+1)+"]/td[2]").text
                clickPatientBreakdown = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[2]/div/div[2]/div[1]/table/tbody/tr["+str(i+1)+"]/td[2]/span/span[2]/span/a")
                clickPatientBreakdown.click()
                stopperPatientAgeBreakdown = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[4]/div/div/div/div[2]/div[2]/div/div/div[1]/div[1]/div[1]/div/h5").text
                stopperPatientBreakdown = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[4]/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div[1]/h5").text

                clickApptBreakdown = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[4]/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div[3]/div/div[2]/a/span/span[2]")
                clickApptBreakdown.click()

                stopperApptTableTab = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[4]/div/div/div/div[2]/div[2]/div/div/div[3]/div/div/table/tbody/tr[1]/td[1]/span").text

                checkIfTheresDataInApptTable = driver.find_elements(By.XPATH, "/html/body/div[1]/main/div[4]/div/div/div/div[2]/div[2]/div/div/div[3]/div/div/table/tbody/tr")
                countApptInTable = len(checkIfTheresDataInApptTable)

                totalFail = 0

                pts_procedure = ""
                pts_providers = ""
                pts_appt_status = ""
                pts_amount = ""
                pts_date = ""

                for j in range(countApptInTable):
                    getDateAppt = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[4]/div/div/div/div[2]/div[2]/div/div/div[3]/div/div/table/tbody/tr["+str(j+1)+"]/td[6]/span").text
                    date_test = datetime.strptime(getDateAppt, '%b %d, %Y')
                    date_test = date_test.strftime("%Y-%m-%d")

                    if date_test >= start_date and date_test <= end_date:
                        pts_procedure = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[4]/div/div/div/div[2]/div[2]/div/div/div[3]/div/div/table/tbody/tr["+str(j+1)+"]/td[1]/span").text
                        pts_providers = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[4]/div/div/div/div[2]/div[2]/div/div/div[3]/div/div/table/tbody/tr["+str(j+1)+"]/td[3]/span").text
                        pts_appt_status = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[4]/div/div/div/div[2]/div[2]/div/div/div[3]/div/div/table/tbody/tr["+str(j+1)+"]/td[4]/span").text
                        pts_amount = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[4]/div/div/div/div[2]/div[2]/div/div/div[3]/div/div/table/tbody/tr["+str(j+1)+"]/td[5]/span").text
                        pts_date = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[4]/div/div/div/div[2]/div[2]/div/div/div[3]/div/div/table/tbody/tr["+str(j+1)+"]/td[6]/span").text
                        print(date_test)
                    else:
                        totalFail = totalFail + 1

                if totalFail == countApptInTable:
                    patientStatus = "Fail"
                else:
                    patientStatus = "Pass"
                
                print(patientStatus)

                new_calendar_appt_validation_testing = CalendarApptValidation(user_id = current_user.id,
                    test_code = test_code,
                    test_date_from = start_date,
                    test_date_to = end_date,
                    pts_name = getPatientName, 
                    pts_procedure = pts_procedure,
                    pts_providers = pts_providers,
                    pts_appt_status = pts_appt_status,
                    pts_amount = pts_amount,
                    pts_date = pts_date,
                    pts_status = patientStatus,
                    created_at = datetime.now(),
                    updated_at = datetime.now())

                db.session.add(new_calendar_appt_validation_testing)
                db.session.commit()


                clickClosePatientBreakdown = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[4]/div/div/div/div[2]/div[1]/div[1]/button")
                clickClosePatientBreakdown.click()



        if int(countData) < 10:
            for i in range(int(countData)):
                getPatientName = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[2]/div/div[2]/div[1]/table/tbody/tr["+str(i+1)+"]/td[2]").text
                clickPatientBreakdown = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[2]/div/div[2]/div[1]/table/tbody/tr["+str(i+1)+"]/td[2]/span/span[2]/span/a")
                clickPatientBreakdown.click()
                stopperPatientAgeBreakdown = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[4]/div/div/div/div[2]/div[2]/div/div/div[1]/div[1]/div[1]/div/h5").text
                stopperPatientBreakdown = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[4]/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div[1]/h5").text

                clickApptBreakdown = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[4]/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div[3]/div/div[2]/a/span/span[2]")
                clickApptBreakdown.click()

                stopperApptTableTab = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[4]/div/div/div/div[2]/div[2]/div/div/div[3]/div/div/table/tbody/tr[1]/td[1]/span").text

                checkIfTheresDataInApptTable = driver.find_elements(By.XPATH, "/html/body/div[1]/main/div[4]/div/div/div/div[2]/div[2]/div/div/div[3]/div/div/table/tbody/tr")
                countApptInTable = len(checkIfTheresDataInApptTable)

                totalFail = 0

                pts_procedure = ""
                pts_providers = ""
                pts_appt_status = ""
                pts_amount = ""
                pts_date = ""

                for j in range(countApptInTable):
                    getDateAppt = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[4]/div/div/div/div[2]/div[2]/div/div/div[3]/div/div/table/tbody/tr["+str(j+1)+"]/td[6]/span").text
                    date_test = datetime.strptime(getDateAppt, '%b %d, %Y')
                    date_test = date_test.strftime("%Y-%m-%d")

                    if date_test >= start_date and date_test <= end_date:
                        pts_procedure = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[4]/div/div/div/div[2]/div[2]/div/div/div[3]/div/div/table/tbody/tr["+str(j+1)+"]/td[1]/span").text
                        pts_providers = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[4]/div/div/div/div[2]/div[2]/div/div/div[3]/div/div/table/tbody/tr["+str(j+1)+"]/td[3]/span").text
                        pts_appt_status = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[4]/div/div/div/div[2]/div[2]/div/div/div[3]/div/div/table/tbody/tr["+str(j+1)+"]/td[4]/span").text
                        pts_amount = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[4]/div/div/div/div[2]/div[2]/div/div/div[3]/div/div/table/tbody/tr["+str(j+1)+"]/td[5]/span").text
                        pts_date = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[4]/div/div/div/div[2]/div[2]/div/div/div[3]/div/div/table/tbody/tr["+str(j+1)+"]/td[6]/span").text
                        print(date_test)
                    else:
                        totalFail = totalFail + 1

                if totalFail == countApptInTable:
                    patientStatus = "Fail"
                else:
                    patientStatus = "Pass"
                
                print(patientStatus)

                new_calendar_appt_validation_testing = CalendarApptValidation(user_id = current_user.id,
                    test_code = test_code,
                    test_date_from = start_date,
                    test_date_to = end_date,
                    pts_name = getPatientName, 
                    pts_procedure = pts_procedure,
                    pts_providers = pts_providers,
                    pts_appt_status = pts_appt_status,
                    pts_amount = pts_amount,
                    pts_date = pts_date,
                    pts_status = patientStatus,
                    created_at = datetime.now(),
                    updated_at = datetime.now())

                db.session.add(new_calendar_appt_validation_testing)
                db.session.commit()


                clickClosePatientBreakdown = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[4]/div/div/div/div[2]/div[1]/div[1]/button")
                clickClosePatientBreakdown.click()

        
    return driver