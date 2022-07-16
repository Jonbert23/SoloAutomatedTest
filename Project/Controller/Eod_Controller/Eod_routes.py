# from crypt import methods
#from crypt import methods
from flask import Blueprint, render_template, url_for, request, redirect
from flask_login import login_required, current_user
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from Project.Controller.Global_Controller.Global_test import Login
from Project.Controller.Global_Controller.One_date_picker import SpecificDateSelector
from .Eod_xpath import EodXpath, BreakdownXpath, EodSetupXpath, ModalMetricXpath, ModalCloseBtnXpath, ClickableElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
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
        Login.login(driver, f"{testcode_info.client_link}end-of-day", testcode_info.client_username, testcode_info.client_password)
        
        if not driver:
            return False

        date = {
            "month": testcode_date[1],
            "day": testcode_date[2],
            "year": testcode_date[0]
        }

        result = testEod(driver, date)
        storeTest(result, testcode)

    else:
        testcode = request.args.get('testcode')

    last_test = EodBreakdownTest.query.order_by(EodBreakdownTest.id.desc()).first()
    if testcode and not testcode_info:
        testcode_info = TestCodes.query.filter_by(test_code=testcode).first()
    else:
        if last_test:
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

def testEod(driver, date):
    result = {}

    try:
        month = date['month']
        day = date['day']
        year = date['year']

        setDate(driver, month, day, year)

        refresh_btn = ClickableElement('refresh_btn', EodSetupXpath.refresh_btn)
        refresh_btn.findElement(driver)
        refresh_btn.click(driver)

        xpaths = getXpath()

        for metric in xpaths:
            
            result[metric] = {
                "main": None,
                "breakdown": "0"
            }

            # Get main view metric value
            xpaths[metric]["main"].findElement(driver)
            result[metric]["main"] = xpaths[metric]["main"].getValue()

            # Open breakdown modal
            xpaths[metric]["breakdown"]["open_modal"].findElement(driver)
            xpaths[metric]["breakdown"]["open_modal"].click(driver)

            # Get modal metric value
            xpaths[metric]["breakdown"]["metric"].findElement(driver)

            if xpaths[metric]["breakdown"]["metric"].element != None and xpaths[metric]["breakdown"]["metric"].instantiated:
                temp = xpaths[metric]["breakdown"]["metric"].getValue()

                if xpaths[metric]["breakdown"]["metric"].type == 'collection' and temp == 1 and "Nothing to show" in xpaths[metric]["breakdown"]["metric"].element[0].text:
                    result[metric]['breakdown'] = "0"
                else:
                    result[metric]['breakdown'] = str(temp)

            # Close breakdown modal
            xpaths[metric]["breakdown"]["close_modal"].findElement(driver)
            xpaths[metric]["breakdown"]["close_modal"].click(driver)

        print(result)
        result = cleanValues(result)
        print(result)
        
    except Exception as e:
        print(f"Some error in here {e}")
    finally:
        driver.quit()
        return result

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


def getXpath():
    return {
        "collection": getMainBreakdown(EodXpath.collection, BreakdownXpath.collection, ModalMetricXpath.collection, ModalCloseBtnXpath.collection),
        "adjustments": getMainBreakdown(EodXpath.adjustments, BreakdownXpath.adjustments, ModalMetricXpath.adjustments, ModalCloseBtnXpath.adjustments),
        "case_acceptance": getMainBreakdown(EodXpath.case_acceptance, BreakdownXpath.case_acceptance, ModalMetricXpath.case_acceptance, ModalCloseBtnXpath.case_acceptance),
        "missing_ref": getMainBreakdown(EodXpath.missing_ref, BreakdownXpath.missing_ref, ModalMetricXpath.missing_ref, ModalCloseBtnXpath.missing_ref),
        "no_show": getMainBreakdown(EodXpath.no_show, BreakdownXpath.no_show, ModalMetricXpath.no_show, ModalCloseBtnXpath.no_show),
        "daily_coll": getMainBreakdown(EodXpath.daily_coll, BreakdownXpath.daily_coll, ModalMetricXpath.daily_coll, ModalCloseBtnXpath.daily_coll),
        "hyg_reapp": getMainBreakdown(EodXpath.hyg_reapp, BreakdownXpath.hyg_reapp, ModalMetricXpath.hyg_reapp, ModalCloseBtnXpath.hyg_reapp),
        "new_patients": getMainBreakdown(EodXpath.new_patients, BreakdownXpath.new_patients, ModalMetricXpath.new_patients, ModalCloseBtnXpath.new_patients),
        "same_day_treat": getMainBreakdown(EodXpath.same_day_treat, BreakdownXpath.same_day_treat, ModalMetricXpath.same_day_treat, ModalCloseBtnXpath.same_day_treat),
        "pt_portion": getMainBreakdown(EodXpath.pt_portion, BreakdownXpath.pt_portion, ModalMetricXpath.pt_portion, ModalCloseBtnXpath.pt_portion)
    }

def getMainBreakdown(main, open_brkdn, breakdown, close_btn):
    return {
        "main": main,
        "breakdown": {
            "open_modal": open_brkdn,
            "metric": breakdown,
            "close_modal": close_btn
        }
    }

def cleanValues(dict):
    for metric in dict:
        dict[metric]['main'] = round(float(re.sub("[^0-9.]", "", dict[metric]['main'])))
        dict[metric]['breakdown'] = round(float(re.sub("[^0-9.]", "", dict[metric]['breakdown'])))
    
    return dict