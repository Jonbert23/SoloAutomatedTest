from selenium import webdriver
from selenium.webdriver.common.by import By
from flask_login import login_required, current_user
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time 
from datetime import datetime
from .... import db
import sqlite3
import re


def defaultTestTx(driver, test_code, test_month):
    driver.implicitly_wait(1000000000)

    checkIfTableAlreadyLoad = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[3]/div/div/div/div[2]/div/div/table/tbody/tr[1]/td[1]")
    checkIfColorCodingAlreadyShown = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[3]/div/div/div/div[1]/div[1]/ul")

    getAllDataInTable = driver.find_elements(By.XPATH, "/html/body/div[1]/main/div[3]/div/div/div/div[2]/div/div/table/tbody/tr")
    countAllDataInTable = len(getAllDataInTable)
    print(countAllDataInTable)

    for i in range(countAllDataInTable):
        getMonth = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[3]/div/div/div/div[2]/div/div/table/tbody/tr["+str(i+1)+"]/td[1]").text
        print(getMonth)

    return driver