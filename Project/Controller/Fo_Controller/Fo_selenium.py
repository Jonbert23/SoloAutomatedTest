from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .Fo_test import fo_kpis_test
from flask import Blueprint, flash, render_template, url_for, request, redirect

def login(get_test_code):
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


    driver.implicitly_wait(1000000000)
    driver.get(get_test_code.client_link+'/front-office/kpis')
    optionalData = fo_kpis_test.foKpisTesting(driver, test_code, test_month, test_date_from, test_date_to)

    driver.quit()