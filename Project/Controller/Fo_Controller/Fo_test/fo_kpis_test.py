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
from ....models import FrontOfficeKpisTest
import sqlite3
import re



def foKpisTesting(driver, test_code, test_month, test_date_from, test_date_to):
    start_date = test_date_from
    end_date = test_date_to
    driver.implicitly_wait(1000000)

    checkIfDataAlreadyLoad = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div/div/div/div/div/div/div/div/div/div/div/div/div/div/span/span").text
    time.sleep(3)
    
    clickMonthFilter = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[1]/div/div/div/div[1]/div/div[2]")
    clickMonthFilter.click()
    
    countMonthFilter = driver.find_elements(By.XPATH, "/html/body/div[1]/main/div[1]/div/div/div/div[1]/div/div[3]/ul/li/span")
    lengthMonthFilter = len(countMonthFilter)
    
    
    month_test = datetime.strptime(test_month, '%Y-%m')
    month_test = month_test.strftime("%B %Y")

    # print(lengthMonthFilter)

    for q in range(lengthMonthFilter):
        getMonthNameInFilter = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[1]/div/div/div/div[1]/div/div[3]/ul/li["+str(q+1)+"]/span").text
        # print(getMonthNameInFilter)
        if getMonthNameInFilter == month_test:
            clickMonthNameInFilter = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[1]/div/div/div/div[1]/div/div[3]/ul/li["+str(q+1)+"]/span")
            clickMonthNameInFilter.click()
            clickUpdateButton = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[1]/div/div/div/div[3]/button")
            clickUpdateButton.click()
            break

    checkIfDataAlreadyLoad = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div/div/div/div/div/div/div/div/div/div/div/div/div/div/span/span").text
    time.sleep(3)

    print("--------- OFFICE KPIS ---------")
    ## START OFFICE KPIS LOOP CHECK DATA ##
    countOfficeKpiTiles = driver.find_elements(By.XPATH, "/html/body/div[1]/main/div[2]/div/div/div[1]/div/div[2]/div/div/div/div")
    lengthOfficeKpiTiles = len(countOfficeKpiTiles)

    for i in range(lengthOfficeKpiTiles):
        getTileTitle = driver.find_element(By.XPATH, "html/body/div[1]/main/div[2]/div/div/div[1]/div/div[2]/div["+str(i+1)+"]/div/div/div/div[1]/h4").text
        getCurrentWithPercentage = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div/div/div[1]/div/div[2]/div["+str(i+1)+"]/div/div/div/div[2]/div[1]/div[1]/div/div[1]/span[2]/span").text
        getCurrentPercentage = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div/div/div[1]/div/div[2]/div["+str(i+1)+"]/div/div/div/div[2]/div[1]/div[1]/div/div[1]/span[2]/span").text.replace('%' , '')
        getGoalPercentage = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div/div/div[1]/div/div[2]/div["+str(i+1)+"]/div/div/div/div[2]/div[1]/div[1]/div/div[2]/span[2]").text.replace('%' , '')
        totalPercentage = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div/div/div[1]/div/div[2]/div["+str(i+1)+"]/div/div/div/div[2]/div[1]/div[2]/div/div/div[2]").text.replace('%' , '')
        
        total = float(getCurrentPercentage) / float(getGoalPercentage)
        total = float(total) * 100

        calculationStatus = ""
        if str(round(total)) == totalPercentage:
            calculationStatus = "Pass"
        else:
            calculationStatus = "Fail"

        clickBreakdown = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div/div/div[1]/div/div[2]/div["+str(i+1)+"]/div/div/div/div[2]/div[2]/div/a")
        clickBreakdown.click()

        checkIfItAlreadyLoad = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div/div/div[1]/div/div[2]/div["+str(i+1)+"]/div/div/div/div[2]/div[2]/div/div/div/div/div[2]/div[3]/div/table/thead/tr/th[1]").text
        time.sleep(2)

        ## START FUNCTION HERE
        countFooterSection = driver.find_elements(By.XPATH, "/html/body/div[1]/main/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div[2]/div/div/div/div/div[2]/div[3]/div/table/tr")
        lengthFooterSection = len(countFooterSection)

        matchBreakdownStatus = "Fail"
        for j in range(lengthFooterSection):
            countFooterTiles = driver.find_elements(By.XPATH, "/html/body/div[1]/main/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div[2]/div/div/div/div/div[2]/div[3]/div/table/tr["+str(j+1)+"]/td")
            lengthFooterTiles = len(countFooterTiles)
            if matchBreakdownStatus == "Fail":
                for y in range(lengthFooterTiles):
                    getTilesValue = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div[2]/div/div/div/div/div[2]/div[3]/div/table/tr["+str(j+1)+"]/td["+str(y+1)+"]").text
                    
                    if getCurrentWithPercentage == getTilesValue:
                        matchBreakdownStatus = "Pass"
                        break
            else: 
                break
        ## END FUNCTION HERE
        print("TITLE: " + getTileTitle)
        print(getCurrentWithPercentage + " AND " + getTilesValue + " --- STATUS --- " + matchBreakdownStatus)

        # tile name = getTileTitle
        # tile current = getCurrentWithPercentage
        # tile goal = getCurrentWithPercentage
        # breakdown current = getTilesValue
        # calculation status = calculationStatus
        # matching breakdown status = matchBreakdownStatus

        new_kpis_default = FrontOfficeKpisTest(user_id = current_user.id,
            test_code = test_code,
            section_name = "Office KPIs",
            tile_name = getTileTitle,
            main_tile_current = getCurrentWithPercentage,
            main_tile_goal = getGoalPercentage,
            breakdown_tile_current = getTilesValue,
            cal_status = calculationStatus,
            match_brkdwn_status = matchBreakdownStatus,
            created_at = datetime.now(),
            updated_at = datetime.now())

        db.session.add(new_kpis_default)
        db.session.commit()

        clickCloseButton = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div/div/div[1]/div/div[2]/div["+str(i+1)+"]/div/div/div/div[2]/div[2]/div/div/div/div/div[1]/button")
        clickCloseButton.click()

    ## END OFFICE KPIS LOOP CHECK DATA ##

    print("--------- DOCTOR KPIS ---------")
    ## START DOCTOR KPIS LOOP CHECK DATA ##
    countDoctorKpiTiles = driver.find_elements(By.XPATH, "/html/body/div[1]/main/div[2]/div/div/div[2]/div/div[2]/div/div/div/div")

    
    lengthDoctorKpiTiles = len(countDoctorKpiTiles)

    for x in range(lengthDoctorKpiTiles):
        getDoctorTileTitle = driver.find_element(By.XPATH, "html/body/div[1]/main/div[2]/div/div/div[2]/div/div[2]/div["+str(x+1)+"]/div/div/div/div[1]/h4").text
        getDoctorCurrentWithPercentage = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div/div/div[2]/div/div[2]/div["+str(x+1)+"]/div/div/div/div[2]/div[1]/div[1]/div/div[1]/span[2]/span").text
        getDoctorCurrentPercentage = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div/div/div[2]/div/div[2]/div["+str(x+1)+"]/div/div/div/div[2]/div[1]/div[1]/div/div[1]/span[2]/span").text.replace('%' , '').replace('$ ' , '').replace(',' , '')
        getDoctorGoalPercentage = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div/div/div[2]/div/div[2]/div["+str(x+1)+"]/div/div/div/div[2]/div[1]/div[1]/div/div[2]/span[2]").text.replace('%' , '').replace('$' , '').replace(',' , '')
        totalDoctorPercentage = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div/div/div[2]/div/div[2]/div["+str(x+1)+"]/div/div/div/div[2]/div[1]/div[2]/div/div/div[2]").text.replace('%' , '')
        
        total = float(getDoctorCurrentPercentage) / float(getDoctorGoalPercentage)
        total = float(total) * 100

        calculationStatus = ""
        if str(round(total)) == totalDoctorPercentage:
            calculationStatus = "Pass"
        else:
            calculationStatus = "Fail"

        clickBreakdown = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div/div/div[2]/div/div[2]/div["+str(x+1)+"]/div/div/div/div[2]/div[2]/div/a")
        clickBreakdown.click()

        checkIfItAlreadyLoad = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div/div/div[2]/div/div[2]/div["+str(x+1)+"]/div/div/div/div[2]/div[2]/div/div/div/div/div[2]/div[3]/div/table/thead/tr/th[1]").text
        time.sleep(2)

        ## START FUNCTION HERE
        countFooterSection = driver.find_elements(By.XPATH, "/html/body/div[1]/main/div[2]/div/div/div[2]/div/div[2]/div/div/div/div/div[2]/div[2]/div/div/div/div/div[2]/div[3]/div/table/tr")
        lengthFooterSection = len(countFooterSection)

        matchBreakdownStatus = "Fail"
        for n in range(lengthFooterSection):
            countFooterTiles = driver.find_elements(By.XPATH, "/html/body/div[1]/main/div[2]/div/div/div[2]/div/div[2]/div/div/div/div/div[2]/div[2]/div/div/div/div/div[2]/div[3]/div/table/tr["+str(n+1)+"]/td")
            lengthFooterTiles = len(countFooterTiles)
            if matchBreakdownStatus == "Fail":
                for m in range(lengthFooterTiles):
                    getTilesValue = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div/div/div[2]/div/div[2]/div/div/div/div/div[2]/div[2]/div/div/div/div/div[2]/div[3]/div/table/tr["+str(n+1)+"]/td["+str(m+1)+"]").text.replace('$' , '$ ')
                    # print(getTilesValue)
                    if getDoctorCurrentWithPercentage == getTilesValue:
                        matchBreakdownStatus = "Pass"
                        break
            else: 
                break
        ## END FUNCTION HERE
        print("TITLE: " + getDoctorTileTitle)
        print(getDoctorCurrentWithPercentage + " AND " + getTilesValue + " --- STATUS --- " + matchBreakdownStatus)

        new_kpis_default = FrontOfficeKpisTest(user_id = current_user.id,
            test_code = test_code,
            section_name = "Doctor KPIs",
            tile_name = getDoctorTileTitle,
            main_tile_current = getDoctorCurrentWithPercentage,
            main_tile_goal = getDoctorGoalPercentage,
            breakdown_tile_current = getTilesValue,
            cal_status = calculationStatus,
            match_brkdwn_status = matchBreakdownStatus,
            created_at = datetime.now(),
            updated_at = datetime.now())

        db.session.add(new_kpis_default)
        db.session.commit()

        clickCloseButton = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div/div/div[2]/div/div[2]/div["+str(x+1)+"]/div/div/div/div[2]/div[2]/div/div/div/div/div[1]/button")
        clickCloseButton.click()

    ## END DOCTOR KPIS LOOP CHECK DATA ##

    print("--------- HYGIENE KPIS ---------")
    ## START DOCTOR KPIS LOOP CHECK DATA ##
    countHygieneKpiTiles = driver.find_elements(By.XPATH, "/html/body/div[1]/main/div[2]/div/div/div[3]/div/div[2]/div/div/div/div")

    
    lengthHygieneKpiTiles = len(countHygieneKpiTiles)

    for x in range(lengthHygieneKpiTiles):
        getHygieneTileTitle = driver.find_element(By.XPATH, "html/body/div[1]/main/div[2]/div/div/div[3]/div/div[2]/div["+str(x+1)+"]/div/div/div/div[1]/h4").text
        getHygieneCurrentWithPercentage = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div/div/div[3]/div/div[2]/div["+str(x+1)+"]/div/div/div/div[2]/div[1]/div[1]/div/div[1]/span[2]/span").text
        getHygieneCurrentPercentage = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div/div/div[3]/div/div[2]/div["+str(x+1)+"]/div/div/div/div[2]/div[1]/div[1]/div/div[1]/span[2]/span").text.replace('%' , '').replace('$ ' , '').replace(',' , '')
        getHygieneGoalPercentage = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div/div/div[3]/div/div[2]/div["+str(x+1)+"]/div/div/div/div[2]/div[1]/div[1]/div/div[2]/span[2]").text.replace('%' , '').replace('$' , '').replace(',' , '')
        totalHygienePercentage = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div/div/div[3]/div/div[2]/div["+str(x+1)+"]/div/div/div/div[2]/div[1]/div[2]/div/div/div[2]").text.replace('%' , '')
        
        total = float(getHygieneCurrentPercentage) / float(getHygieneGoalPercentage)
        total = float(total) * 100

        calculationStatus = ""
        if str(round(total)) == totalHygienePercentage:
            calculationStatus = "Pass"
        else:
            calculationStatus = "Fail"

        clickBreakdown = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div/div/div[3]/div/div[2]/div["+str(x+1)+"]/div/div/div/div[2]/div[2]/div/a")
        clickBreakdown.click()

        checkIfItAlreadyLoad = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div/div/div[3]/div/div[2]/div["+str(x+1)+"]/div/div/div/div[2]/div[2]/div/div/div/div/div[2]/div[3]/div/table/thead/tr/th[1]").text
        time.sleep(2)

        ## START FUNCTION HERE
        countFooterSection = driver.find_elements(By.XPATH, "/html/body/div[1]/main/div[2]/div/div/div[3]/div/div[2]/div/div/div/div/div[2]/div[2]/div/div/div/div/div[2]/div[3]/div/table/tr")
        lengthFooterSection = len(countFooterSection)

        matchBreakdownStatus = "Fail"
        for n in range(lengthFooterSection):
            countFooterTiles = driver.find_elements(By.XPATH, "/html/body/div[1]/main/div[2]/div/div/div[3]/div/div[2]/div/div/div/div/div[2]/div[2]/div/div/div/div/div[2]/div[3]/div/table/tr["+str(n+1)+"]/td")
            lengthFooterTiles = len(countFooterTiles)
            if matchBreakdownStatus == "Fail":
                for m in range(lengthFooterTiles):
                    getTilesValue = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div/div/div[3]/div/div[2]/div/div/div/div/div[2]/div[2]/div/div/div/div/div[2]/div[3]/div/table/tr["+str(n+1)+"]/td["+str(m+1)+"]").text.replace('$' , '$ ')
                    # print(getTilesValue)
                    if getHygieneCurrentWithPercentage == getTilesValue:
                        matchBreakdownStatus = "Pass"
                        break
            else: 
                break
        ## END FUNCTION HERE
        print("TITLE: " + getHygieneTileTitle)
        print(getHygieneCurrentWithPercentage + " AND " + getTilesValue + " --- STATUS --- " + matchBreakdownStatus)

        new_kpis_default = FrontOfficeKpisTest(user_id = current_user.id,
            test_code = test_code,
            section_name = "Hygiene KPIs",
            tile_name = getHygieneTileTitle,
            main_tile_current = getHygieneCurrentWithPercentage,
            main_tile_goal = getHygieneGoalPercentage,
            breakdown_tile_current = getTilesValue,
            cal_status = calculationStatus,
            match_brkdwn_status = matchBreakdownStatus,
            created_at = datetime.now(),
            updated_at = datetime.now())

        db.session.add(new_kpis_default)
        db.session.commit()

        clickCloseButton = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div/div/div[3]/div/div[2]/div["+str(x+1)+"]/div/div/div/div[2]/div[2]/div/div/div/div/div[1]/button")
        clickCloseButton.click()

    ## END DOCTOR KPIS LOOP CHECK DATA ##

    

      

    


    return driver