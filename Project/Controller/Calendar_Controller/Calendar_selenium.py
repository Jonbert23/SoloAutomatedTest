from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from flask import Blueprint, flash, render_template, url_for, request, redirect
from .Calendar_Optional import calendar_provider
from .Calendar_Optional import calendar_patient
from .Calendar_Optional import calendar_procedure
from .Calendar_Default import calendar_metric_test
from .Calendar_Default import calendar_appt_per_day_test
from ...models import CalendarFilterTesting
from ...models import CalendarMetricTesting
from ...models import CalendarFilterUse


def login(get_test_code, optional_test):

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
    test_date = get_test_code.test_date

    checkIfAlreadyTestInMetric = CalendarMetricTesting.query.filter_by(test_code=test_code).first()


    if not checkIfAlreadyTestInMetric:
        driver.implicitly_wait(1000000000)
        driver.get('https://solo.next.jarvisanalytics.com/calendar/appointments')
        optionalData = calendar_metric_test.metricTest(driver, test_code, test_month)


    # driver.implicitly_wait(1000000000)
    # driver.get('https://solo.next.jarvisanalytics.com/calendar/appointments/day')
    # optionalData = calendar_appt_per_day_test.perDayTest(driver, test_code, test_date)

    # for option in optional_test:
    #     print("--- "+option+" ---")
    #     if option == "Provider Filter":
    #         driver.implicitly_wait(1000000000)
    #         driver.get('https://solo.next.jarvisanalytics.com/calendar/appointment-details')

    #         getProvider = CalendarFilterUse.query.filter_by(test_code=test_code).filter_by(filter_name='Provider Filter').order_by(CalendarFilterUse.id.desc()).first()
    #         if getProvider:
    #             driver.quit()
    #             return "fail"
    #         if not getProvider:
    #             optionalData = calendar_provider.providerFilterTest(driver, test_code)
    #     if option == "Procedure Filter":
    #         driver.implicitly_wait(1000000000)
    #         driver.get('https://solo.next.jarvisanalytics.com/calendar/appointment-details')
    #         getProcedureCode = CalendarFilterUse.query.filter_by(test_code=test_code).filter_by(filter_name='Procedure Filter').order_by(CalendarFilterUse.id.desc()).first()
    #         if getProvider:
    #             driver.quit()
    #             return "fail"
    #         if not getProvider:
    #             optionalData = calendar_procedure.procedureFilterTest(driver, test_code)
    #     if option == "Patient Filter":
    #         driver.implicitly_wait(1000000000)
    #         driver.get('https://solo.next.jarvisanalytics.com/calendar/appointment-details')

    #         getPatient = CalendarFilterUse.query.filter_by(test_code=test_code).filter_by(filter_name='Patient Filter').order_by(CalendarFilterUse.id.desc()).first()
    #         if getProvider:
    #             driver.quit()
    #             return "fail"
    #         if not getProvider:
    #             optionalData = calendar_patient.patientFilterTest(driver, test_code)

    driver.quit()