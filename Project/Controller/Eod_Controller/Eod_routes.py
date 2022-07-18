from flask import Blueprint, render_template, url_for, request, redirect
from flask_login import login_required, current_user
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from Project.Controller.Global_Controller.Global_test import Login
from Project.Controller.Global_Controller.One_date_picker import SpecificDateSelector
from .Eod_xpath import EodBreakdown, EodSetupXpath, ClickableElement, GmailXpath, EmailData, EodData
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
import re
from ...models import TestCodes, User, EodBreakdownTest
from ... import db
from werkzeug.security import generate_password_hash

eod = Blueprint('eod', __name__)

@eod.route("/eod-form", methods=["POST", "GET"])
def eodForm():
    testcode = None
    testcode_info = None
    last_test = None

    if request.method == 'POST':
        testcode = request.form['testcode'].lower()
        testcode_info = TestCodes.query.filter_by(test_code=testcode).first()
        testcode_date = testcode_info.test_date.split('-')
        test_url = f"{testcode_info.client_link}end-of-day" if testcode_info.client_link.endswith("/") else f"{testcode_info.client_link}/end-of-day"

        d = DesiredCapabilities.CHROME
        d['loggingPrefs'] = {'browser': 'ERROR'}
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), desired_capabilities=d)
        login = Login.login(driver, f"{testcode_info.client_link}end-of-day", testcode_info.client_username, testcode_info.client_password)
        
        if login and driver:

            date = {
                "month": testcode_date[1],
                "day": testcode_date[2],
                "year": testcode_date[0]
            }

            # SET DATE IN EOD
            setDate(driver, date['month'], date['day'], date['year'])
            refresh_btn = ClickableElement('refresh_btn', EodSetupXpath.refresh_btn)
            refresh_btn.findElement(driver)
            refresh_btn.click(driver)

            # TEST EOD METRICS
            # bd_result = breakdownTest(driver)
            email_result = emailTest(driver)

            driver.quit()

            # storeTest(bd_result, testcode)
    else:
        testcode = request.args.get('testcode').lower() if request.args.get('testcode') else None

    if testcode and not testcode_info:
        testcode_info = TestCodes.query.filter_by(test_code=testcode).first()
        last_test = EodBreakdownTest.query.filter_by(test_code=testcode).order_by(EodBreakdownTest.id.desc()).first()
    else:
        last_test = EodBreakdownTest.query.order_by(EodBreakdownTest.id.desc()).first()
        testcode_info = TestCodes.query.filter_by(test_code=last_test.test_code).first()

    return render_template('Eod_Template/Eod_index.html', last_test=last_test, testcode_info=testcode_info)

def storeTest(result, testcode):
    test_result = EodBreakdownTest(
        user_id = current_user.id,
        test_code = testcode,
        collection_main = result["collection"]["main"],
        collection_bd = result["collection"]["breakdown"],
        adjustments_main = result['adjustments']['main'],
        adjustments_bd = result['adjustments']['breakdown'],
        case_accpt_main = result['case_acceptance']['main'],
        case_accpt_bd = result['case_acceptance']['breakdown'],
        miss_ref_main = result['missing_ref']['main'],
        miss_ref_bd = result['missing_ref']['breakdown'],
        no_show_main = result['no_show']['main'],
        no_show_bd = result['no_show']['breakdown'],
        daily_coll_main = result['daily_coll']['main'],
        daily_coll_bd = result['daily_coll']['breakdown'],
        hyg_reapp_main = result['hyg_reapp']['main'],
        hyg_reapp_bd = result['hyg_reapp']['breakdown'],
        new_patient_main = result['new_patients']['main'],
        new_patient_bd = result['new_patients']['breakdown'],
        sd_treat_main = result['same_day_treat']['main'],
        sd_treat_bd = result['same_day_treat']['breakdown'],
        pt_portion_main = result['pt_portion']['main'],
        pt_portion_bd = result['pt_portion']['breakdown'],
    )
    db.session.add(test_result)
    db.session.commit()

def breakdownTest(driver):
    try:
        modal_metrics = EodBreakdown.getModalMetrics()
        bd_metric_collection = EodData.getBdMetricCollection()
        bd_metric_collection.findElement(driver)

        num_of_bd_metric = bd_metric_collection.getValue()

        bd_result = {}

        for i in range(1, num_of_bd_metric+1):
            metric = EodData.getMetricWithBreakdown(i)
            close_modal = EodBreakdown.getCloseModal()
            metric['name'].findElement(driver)
            metric['value'].findElement(driver)
            metric['open_bd'].findElement(driver)
            name = metric['name'].getValue()

            bd_result[name] = {}
            
            value = metric['value'].getValue()
            bd_result[name]['main'] = value

            metric['open_bd'].click(driver)

            modal_metrics[name].findElement(driver)

            bd_result[name]['breakdown'] = '0'
            if modal_metrics[name].element != None and modal_metrics[name].instantiated:
                breakdown_value = modal_metrics[name].getValue()

                if modal_metrics[name].type == 'collection' and breakdown_value == 1 and "Nothing to show" in modal_metrics[name].element[0].text:
                    bd_result[name]['breakdown'] = '0'
                else:
                    bd_result[name]['breakdown'] = str(breakdown_value)    

            close_modal.findElement(driver)
            close_modal.click(driver)
        
        bd_result = cleanValues(bd_result)
        print(bd_result)
    except Exception as e:
        print(e)
        raise Exception(f"Exception while testing: {e}")
    finally:
        return bd_result

def emailTest(driver):
    try:
        metrics_collection = EodData.getMetricsCollection()
        metrics_collection.findElement(driver)

        num_of_metrics = metrics_collection.getValue()

        main_test_result = {}
        for i in range(1, num_of_metrics + 1):

            # Get metric name from EOD
            metric = EodData.getMetric(i)
            metric['name'].findElement(driver)
            name = metric['name'].getValue()

            # Set dictionary for metric with key indicated by the name variable aforementioned.
            main_test_result[name] = {}

            # Get value from input element
            metric['value'].findElement(driver)
            value = metric['value'].getValue()
            main_test_result[name]['main'] = value

        send_eod = getSubmitEod()

        send_eod["submit_btn"].findElement(driver)
        send_eod["submit_btn"].click(driver)

        send_eod["recipients"].findElement(driver)
        send_eod["sndeod_email"].findElement(driver)
        send_eod["sndeod_email"].element.send_keys("eod.test.jap@gmail.com\n")

        send_eod["send_summary"].findElement(driver)
        send_eod["send_summary"].click(driver)

        driver.get("https://mail.google.com/")
        gmail_elements = getGmailXpath()

        gmail_elements['email'].findElement(driver)
        gmail_elements['email'].element.send_keys('eod.test.jap@gmail.com\n')

        gmail_elements['password'].findElement(driver)
        gmail_elements['password'].element.send_keys('ZsRL3Yk3crboXq\n')

        gmail_elements['first_email'].findElement(driver)
        gmail_elements['first_email'].click(driver)

        metric_collection = EmailData.getMetricsCollection()
        metric_collection.findElement(driver)

        num_of_metrics = metric_collection.getValue()

        for i in range(1, num_of_metrics+1):
            email_metric = EmailData.getMetric(i)

            email_metric['name'].findElement(driver)
            name = email_metric['name'].getValue()

            email_metric['value'].findElement(driver)
            value = email_metric['value'].getValue()
            main_test_result[name]['email'] = value

        print(main_test_result)
        return main_test_result
    except Exception as e:
        print(e)

def setDate(driver, month, day, year):
    calendar_xpath = {
        "date_picker": EodSetupXpath.date_picker,
        "prev_month": EodSetupXpath.prev_month,
        "next_month": EodSetupXpath.next_month,
        "curr_month_year": EodSetupXpath.curr_month_year,
        "date_table": EodSetupXpath.date_table
    }

    date = {
        "month": month,
        "day": day,
        "year": year
    }

    date_selector = SpecificDateSelector(calendar_xpath)
    date_selector.initializeCalendar(driver)
    date_selector.selectDate(driver, date)

def cleanValues(dict):
    for metric in dict:
        dict[metric]['main'] = round(float(re.sub("[^0-9.]", "", dict[metric]['main'])))
        dict[metric]['breakdown'] = round(float(re.sub("[^0-9.]", "", dict[metric]['breakdown'])))
    
    return dict

def getGmailXpath():
    return {
        'email': GmailXpath.getEmail(),
        'password': GmailXpath.getPasswd(),
        'submit_btn': GmailXpath.getSubmitBtn(),
        'email_list': GmailXpath.getEmailList(),
        'first_email': GmailXpath.getFirstEmail()
    }

def getSubmitEod():
    return {
        "submit_btn": EodSetupXpath.getSubmitBtn(),
        "sndeod_email": EodSetupXpath.getSendEodEmail(),
        "send_summary": EodSetupXpath.getSendEmail(),
        "recipients": EodSetupXpath.getEmailList()
    }