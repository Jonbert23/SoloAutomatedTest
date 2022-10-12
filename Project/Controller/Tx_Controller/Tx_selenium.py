from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from flask import Blueprint, flash, render_template, url_for, request, redirect
from ...models import TxMinerDefaultTest
from ...models import TxMinerProviderTest
from ...models import TxMinerProcedureTest
from ...models import TxMinerPatientTest
from .Tx_Default import default_test_tx
from .Tx_Optional import providers_test
from .Tx_Optional import procedures_test
from .Tx_Optional import patient_test

def login(get_test_code, optionalTestTx):
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument('--start-maximized')
    options.add_argument('--disable-blink-features=AutomationControlled')
     

    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver = webdriver.Chrome('/usr/local/bin/chromedriver', options=options)
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

    if not checkIfAlreadyTestInDefaultTest:
        driver.implicitly_wait(1000000000)
        driver.get(get_test_code.client_link+'/tx-miner')
        optionalData = default_test_tx.defaultTestTx(driver, test_code, test_month)

    for option in optionalTestTx:
        # print("--- "+option+" ---")
        if option == "Provider Filter":
            driver.implicitly_wait(1000000000)
            driver.get(get_test_code.client_link+'/tx-miner')
            # This is DONE!!

            getProvider = TxMinerProviderTest.query.filter_by(test_code=test_code).order_by(TxMinerProviderTest.id.desc()).first()
            if getProvider:
                driver.quit()
                return "fail"
            if not getProvider:
                optionalData = providers_test.providerTestTx(driver, test_code, test_month)
            # print("Provider Filter")
            print(getProvider)
        if option == "Procedure Filter":
            driver.implicitly_wait(1000000000)
            driver.get(get_test_code.client_link+'/tx-miner')
            # This is DONE!!
            
            getProcedure = TxMinerProcedureTest.query.filter_by(test_code=test_code).order_by(TxMinerProcedureTest.id.desc()).first()
            if getProcedure:
                driver.quit()
                return "fail"
            if not getProcedure:
                procedureFilter = procedures_test.procedureTestTx(driver, test_code, test_month)
            # print("Procedure Filter")
            print(getProcedure)
        if option == "Patient Filter":
            driver.implicitly_wait(1000000000)
            driver.get(get_test_code.client_link+'/tx-miner')

            getPatient = TxMinerPatientTest.query.filter_by(test_code=test_code).order_by(TxMinerPatientTest.id.desc()).first()
            if getPatient:
                driver.quit()
                return "fail"
            if not getPatient:
                patientFilter = patient_test.patientTestTx(driver, test_code, test_month)
            # print("Patient Filter")
            print(getPatient)



    driver.quit()