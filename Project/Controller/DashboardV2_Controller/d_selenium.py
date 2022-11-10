from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .Dash_Default import default_dash_test
from .Dash_Default import default_production_figures
from .Dash_Default import default_services_test
from .Dash_Default import default_lob_test
from .Dash_Optional import services_filter
from .Dash_Optional import lob_filter
from ...models import DashboardV2DefaultBreakdownTest
from ...models import DashboardV2DefaultProductionTest
from ...models import DashboardV2DefaultSearchProcedure
from ...models import DashboardV2DefaultLOBTest
from flask import Blueprint, flash, render_template, url_for, request, redirect

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
    test_date_from = get_test_code.test_date_from
    test_date_to = get_test_code.test_date_to

    checkIfAlreadyTestInBreakdownTest = DashboardV2DefaultBreakdownTest.query.filter_by(test_code=test_code).first()

    #DONE Breakdown Test
    if not checkIfAlreadyTestInBreakdownTest:
        driver.implicitly_wait(1000000000)
        driver.get(get_test_code.client_link+'/solo/results')
        optionalData = default_dash_test.defaultDashTest(driver, test_code, test_month, test_date_from, test_date_to)

    checkIfAlreadyTestInProductionTest = DashboardV2DefaultProductionTest.query.filter_by(test_code=test_code).first()
    #DONE PRODUCTION FIGURES TESTING
    if not checkIfAlreadyTestInProductionTest:
        driver.implicitly_wait(1000000000)
        driver.get(get_test_code.client_link+'/solo/results')
        productionFiguresTest = default_production_figures.defaultProductionFiguresTest(driver, test_code, test_month, test_date_from, test_date_to)

    #DONE PRODUCTION SERVICES TESTING
    # driver.implicitly_wait(1000000000)
    # driver.get(get_test_code.client_link+'/solo/metrics')
    # servicesTest = default_services_test.defaultServicesTest(driver, test_code, test_month, test_date_from, test_date_to)

    

    for option in optionalTestTx:
        # print("--- "+option+" ---")
        if option == "Services Filter":
            checkIfAlreadyTestInServiceTest = DashboardV2DefaultSearchProcedure.query.filter_by(test_code=test_code).first()
            driver.implicitly_wait(1000000000)
            if not checkIfAlreadyTestInServiceTest:
                driver.get(get_test_code.client_link+'/solo/metrics')
                servicesTest = default_services_test.defaultServicesTest(driver, test_code, test_month, test_date_from, test_date_to)
                print("Services Filter")
        if option == "LOB Filter":
            checkIfAlreadyTestInLOBTest = DashboardV2DefaultLOBTest.query.filter_by(test_code=test_code).first()
            driver.implicitly_wait(1000000000)
            if not checkIfAlreadyTestInLOBTest:
                driver.get(get_test_code.client_link+'/solo/results')
                servicesTest = default_lob_test.defaultLobTest(driver, test_code, test_month, test_date_from, test_date_to)
                print("LOB Filter")

    driver.quit()
            