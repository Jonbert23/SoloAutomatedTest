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


def providerTestTx(driver, test_code):

    driver.implicitly_wait(1000000000)

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
        if numberOfProviderItHasData < 5:
            checkIfTheresDataInTables = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[3]/div/div/div/div[1]/div[1]/ul")
            stopper = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[1]/div/div/div/div[3]/button[contains(text(), 'Refresh')]")
            clickProviderFilters = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div[1]/div/button")
            clickProviderFilters.click()

            getProviderTextInProviderFilter = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div[1]/div/div/div[2]/ul/li["+str(i+1)+"]/span/span[1]").text
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

                

                print(countData)

                for j in range(countData):
                    getMonth = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[3]/div/div/div/div[2]/div/div/table/tbody/tr["+str(j+1)+"]/td[1]").text
                    print(getMonth)

                    clickMonthBreakdown = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[3]/div/div/div/div[2]/div/div/table/tbody/tr["+str(j+1)+"]/td[1]/span/span[2]/a")
                    clickMonthBreakdown.click()

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

    # print(numberOfProviderItHasData)
    # print(providerArray)

    