from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from flask import Blueprint, flash, render_template, url_for, request, redirect
from ...models import TxMinerDefaultTest
from .Tx_Default import default_test_tx
from .Tx_Optional import providers_test

def login(get_test_code, optionalTestTx):
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.implicitly_wait(1000000000) 
    driver.get(get_test_code.client_link)

    usernameXpath = driver.find_element(By.XPATH, '/html/body/div/div/div/div/div[1]/div/form/div[1]/div/input')
    usernameXpath.send_keys(get_test_code.client_username)
    passwordXpath = driver.find_element(By.XPATH, '/html/body/div/div/div/div/div[1]/div/form/div[2]/div[2]/input')
    passwordXpath.send_keys(get_test_code.client_password)
    loginButton = driver.find_element(By.XPATH, '/html/body/div/div/div/div/div[1]/div/form/button')
    loginButton.click()

    test_code = get_test_code.test_code
    test_month = get_test_code.test_month
    
    checkIfAlreadyTestInDefaultTest = TxMinerDefaultTest.query.filter_by(test_code=test_code).first()

    # if not checkIfAlreadyTestInDefaultTest:
    #     driver.implicitly_wait(1000000000)
    #     driver.get('https://solo.next.jarvisanalytics.com/tx-miner')
    #     optionalData = default_test_tx.defaultTestTx(driver, test_code, test_month)

    for option in optionalTestTx:
        # print("--- "+option+" ---")
        if option == "Provider Filter":
            driver.implicitly_wait(1000000000)
            driver.get(get_test_code.client_link+'/tx-miner')

            optionalData = providers_test.providerTestTx(driver, test_code)
            print("Provider Filter")
        if option == "Procedure Filter":
            print("Procedure Filter")
        if option == "Patient Filter":
            print("Patient Filter")



    driver.quit()