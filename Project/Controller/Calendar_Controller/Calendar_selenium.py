from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from flask import Blueprint, flash, render_template, url_for, request, redirect
from .Calendar_Optional import calendar_optional
from ...models import CalendarFilterTesting
from ...models import CalendarFilterUse


def login(get_test_code, optional_test):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.implicitly_wait(1000000000) 
    driver.get(get_test_code.client_link)

    usernameXpath = driver.find_element(By.XPATH, '/html/body/div/div/div/div/div[1]/div/form/div[1]/div/input')
    usernameXpath.send_keys(get_test_code.client_username)
    passwordXpath = driver.find_element(By.XPATH, '/html/body/div/div/div/div/div[1]/div/form/div[2]/div[2]/input')
    passwordXpath.send_keys(get_test_code.client_password)
    loginButton = driver.find_element(By.XPATH, '/html/body/div/div/div/div/div[1]/div/form/button')
    loginButton.click()
    
    test_code = get_test_code.test_code

    for option in optional_test:
        print("--- "+option+" ---")
        if option == "Provider Filter Test":
            driver.implicitly_wait(1000000000)
            driver.get('https://solo.next.jarvisanalytics.com/calendar/appointment-details')

            getProvider = CalendarFilterUse.query.filter_by(test_code=test_code).filter_by(filter_name='Provider Filter').order_by(CalendarFilterUse.id.desc()).first()
            if getProvider:
                print('Provider Filter already exist')
                driver.quit()
                return "fail"
            if not getProvider:
                optionalData = calendar_optional.providerFilterTest(driver, test_code)
        if option == "Procedure Filter Test":
            driver.implicitly_wait(1000000000)
            driver.get('https://solo.next.jarvisanalytics.com/calendar/appointment-details')
            optionalData = calendar_optional.procedureFilterTest(driver, test_code)
        if option == "Patient Filter Test":
            driver.implicitly_wait(1000000000)
            driver.get('https://solo.next.jarvisanalytics.com/calendar/appointment-details')
            optionalData = calendar_optional.patientFilterTest(driver, test_code)

    # driver.quit()