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
        login = Login.login(driver, f"{testcode_info.client_link}end-of-day", testcode_info.client_username, testcode_info.client_password)
        
        if login and driver:

            date = {
                "month": testcode_date[1],
                "day": testcode_date[2],
                "year": testcode_date[0]
            }

            # SET DATE IN EOD
            setDate(driver, date['month'], date['day'], date['year'])

            # TEST EOD METRICS
            bd_result = breakdownTest(driver)
            email_result = emailTest(driver)

            driver.quit()

            storeTest(bd_result, testcode)
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
    result = {}

    try:
        # month = date['month']
        # day = date['day']
        # year = date['year']

        # setDate(driver, month, day, year)

        refresh_btn = ClickableElement('refresh_btn', EodSetupXpath.refresh_btn)
        refresh_btn.findElement(driver)
        refresh_btn.click(driver)

        xpaths = getBreakdownTestXpath()

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

        # print(result)
        result = cleanValues(result)
        # print(result)
        
    except Exception as e:
        driver.quit()
        raise Exception(f"Exception while testing: {e}")
    finally:
        return result

def emailTest(driver):
    main_xpath = getMainEmailTestXpath()

    main_test_result = {}
    for metric in main_xpath:
        main_test_result[metric] = {}

        main_xpath[metric].findElement(driver);
        main_test_result[metric]['main'] = main_xpath[metric].getValue()

    print(main_test_result)

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

def getBreakdownTestXpath():
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

def getMainEmailTestXpath():
    return {
        'booked_prod': EodXpath.booked_prod,
        'daily_net_prod': EodXpath.daily_net_prod,
        'daily_gross_prod': EodXpath.daily_gross_prod,
        'ofc_sched_vs_goal': EodXpath.ofc_sched_vs_goal,
        'general': EodXpath.general,
        'ortho_prod': EodXpath.ortho_prod,
        'perio_prod': EodXpath.perio_prod,
        'endo': EodXpath.endo,
        'oral_surgery_prod': EodXpath.oral_surgery_prod,
        'clear_aligners': EodXpath.clear_aligners,
        'num_providers': EodXpath.num_providers,
        'adp': EodXpath.adp,
        'specialty': EodXpath.specialty,
        'total_pts_seen': EodXpath.total_pts_seen,
        'total_office_visits': EodXpath.total_office_visits,
        'total_appts_changed': EodXpath.total_appts_changed,
        'total_appts_cancel': EodXpath.total_appts_cancel,
        'guest_with_appt': EodXpath.guest_with_appt,
        'hyg_reserve': EodXpath.hyg_reserve,
        'hyg_cap': EodXpath.hyg_cap,
        'react_made': EodXpath.react_made,
        'unsched_treat': EodXpath.unsched_treat,
        'restore_appts': EodXpath.restore_appts,
        'recalls_made': EodXpath.recalls_made,
        "collection": EodXpath.collection,
        'adjustments': EodXpath.adjustments,
        'case_acceptance': EodXpath.case_acceptance,
        'missing_ref': EodXpath.missing_ref,
        'no_show': EodXpath.no_show,
        'daily_coll': EodXpath.daily_coll,
        'hyg_reapp': EodXpath.hyg_reapp,
        'new_patients': EodXpath.new_patients,
        'same_day_treat': EodXpath.same_day_treat,
        'pt_portion': EodXpath.pt_portion
    }