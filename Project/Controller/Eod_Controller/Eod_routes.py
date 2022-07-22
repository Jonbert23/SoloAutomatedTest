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
from ...models import TestCodes, User, EodTestResults
from ... import db
from werkzeug.security import generate_password_hash
from datetime import datetime

eod = Blueprint('eod', __name__)

@eod.route("/eod-form", methods=["POST", "GET"])
def eodForm():
    testcode = None
    testcode_info = None
    last_test = None
    succ_vs_fail = None 

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

            # BREAKDOWN AND EMAIL TESTS
            bd_result = breakdownTest(driver)
            email_result = emailTest(driver)
            bundled_result = bundleResults(bd_result, email_result)
            clean_result = cleanValues(bundled_result)

            driver.quit()

            storeTest(clean_result, testcode)
    else:
        testcode = request.args.get('testcode').lower() if request.args.get('testcode') else None

    last_test = getLastTest(testcode)
    if last_test:
        testcode_info = getTestCodeInfo(last_test.test_code)
        succ_vs_fail = getGraphData(last_test)

    return render_template('Eod_Template/Eod_index.html', last_test=last_test, testcode_info=testcode_info, graph_vals=succ_vs_fail)

def storeTest(result, testcode):

    if result.get('Collection'):
        collection_main = result["Collection"]["main"]
        collection_bd = result["Collection"]["breakdown"]
        collection_email = result["Collection"]["email"]
    else:
        collection_main = 'Not found'
        collection_bd = 'Not found'
        collection_email = 'Not found'

    if result.get('Adjustments'):
        adjustments_main = result["Adjustments"]["main"]
        adjustments_bd = result["Adjustments"]["breakdown"]
        adjustments_email = result["Adjustments"]["email"]
    else:
        adjustments_main = 'Not found'
        adjustments_bd = 'Not found'
        adjustments_email = 'Not found'

    if result.get('Case acceptance (%)'):
        case_accpt_main = result["Case acceptance (%)"]["main"]
        case_accpt_bd = result["Case acceptance (%)"]["breakdown"]
        case_accpt_email = result["Case acceptance (%)"]["email"]
    else:
        case_accpt_main = 'Not found'
        case_accpt_bd = 'Not found'
        case_accpt_email = 'Not found'

    if result.get('Patients w/ Missing Referral'):
        miss_ref_main = result["Patients w/ Missing Referral"]["main"]
        miss_ref_bd = result["Patients w/ Missing Referral"]["breakdown"]
        miss_ref_email = result["Patients w/ Missing Referral"]["email"]
    else:
        miss_ref_main = 'Not found'
        miss_ref_bd = 'Not found'
        miss_ref_email = 'Not found'

    if result.get('No Show'):
        no_show_main = result["No Show"]["main"]
        no_show_bd = result["No Show"]["breakdown"]
        no_show_email = result["No Show"]["email"]
    else:
        no_show_main = 'Not found'
        no_show_bd = 'Not found'
        no_show_email = 'Not found'

    if result.get('Daily Collection'):
        daily_coll_main = result["Daily Collection"]["main"]
        daily_coll_bd = result["Daily Collection"]["breakdown"]
        daily_coll_email = result["Daily Collection"]["email"]
    else:
        daily_coll_main = 'Not found'
        daily_coll_bd = 'Not found'
        daily_coll_email = 'Not found'

    if result.get('Hyg Reappointment'):
        hyg_reapp_main = result["Hyg Reappointment"]["main"]
        hyg_reapp_bd = result["Hyg Reappointment"]["breakdown"]
        hyg_reapp_email =result["Hyg Reappointment"]["email"]
    else:
        hyg_reapp_main = 'Not found'
        hyg_reapp_bd = 'Not found'
        hyg_reapp_email = 'Not found'

    if result.get('New Patients'):
        new_patient_main = result["New Patients"]["main"]
        new_patient_bd = result["New Patients"]["breakdown"]
        new_patient_email = result["New Patients"]["email"]
    else:
        new_patient_main = 'Not found'
        new_patient_bd = 'Not found'
        new_patient_email = 'Not found'

    if result.get('Same Day Treatment'):
        sd_treat_main = result["Same Day Treatment"]["main"]
        sd_treat_bd = result["Same Day Treatment"]["breakdown"]
        sd_treat_email = result["Same Day Treatment"]["email"]
    else:
        sd_treat_main = 'Not found'
        sd_treat_bd = 'Not found'
        sd_treat_email = 'Not found'

    if result.get('PT Portion Collections % Today Collected'):
        pt_portion_main = result["PT Portion Collections % Today Collected"]["main"]
        pt_portion_bd = result["PT Portion Collections % Today Collected"]["breakdown"]
        pt_portion_email = result["PT Portion Collections % Today Collected"]["email"]
    else:
        pt_portion_main = 'Not found'
        pt_portion_bd = 'Not found'
        pt_portion_email = 'Not found'

    if result.get('Booked production'):
        booked_prod_main = result["Booked production"]["main"]
        booked_prod_email = result["Booked production"]["email"]
    else:
        booked_prod_main = 'Not found'
        booked_prod_email = 'Not found'

    if result.get('Daily Net Production'):
        daily_net_main = result["Daily Net Production"]["main"]
        daily_net_email = result["Daily Net Production"]["email"]
    else:
        daily_net_main = 'Not found'
        daily_net_email = 'Not found'

    if result.get('Daily Gross Production'):
        daily_gross_main = result["Daily Gross Production"]["main"]
        daily_gross_email = result["Daily Gross Production"]["email"]
    else:
        daily_gross_main = 'Not found'
        daily_gross_email = 'Not found'

    if result.get('Office Scheduled VS Goal (monthly)'):
        sched_vs_goal_main = result["Office Scheduled VS Goal (monthly)"]["main"]
        sched_vs_goal_email = result["Office Scheduled VS Goal (monthly)"]["email"]
    else:
        sched_vs_goal_main = 'Not found'
        sched_vs_goal_email = 'Not found'
    
    if result.get('General'):
        general_main = result["General"]["main"]
        general_email = result["General"]["email"]
    else:
        general_main = 'Not found'
        general_email = 'Not found'

    if result.get('Ortho Production'):
        ortho_prod_main = result["Ortho Production"]["main"]
        ortho_prod_email = result["Ortho Production"]["email"]
    else:
        ortho_prod_main = 'Not found'
        ortho_prod_email = 'Not found'

    if result.get('Perio Production'):
        perio_prod_main = result["Perio Production"]["main"]
        perio_prod_email = result["Perio Production"]["email"]
    else:
        perio_prod_main = 'Not found'
        perio_prod_email = 'Not found'

    if result.get('Oral Surgery Production'):
        oral_surgery_main = result["Oral Surgery Production"]["main"]
        oral_surgery_email = result["Oral Surgery Production"]["email"]
    else:
        oral_surgery_main = 'Not found'
        oral_surgery_email = 'Not found'

    if result.get('Number of Providers'):
        num_prod_main = result["Number of Providers"]["main"]
        num_prod_email = result["Number of Providers"]["email"]
    else:
        num_prod_main = 'Not found'
        num_prod_email = 'Not found'

    if result.get('Office Adjusted Daily Production (ADP)'):
        adp_main = result["Office Adjusted Daily Production (ADP)"]["main"]
        adp_email = result["Office Adjusted Daily Production (ADP)"]["email"]
    else:
        adp_main = 'Not found'
        adp_email = 'Not found'

    if result.get('Specialty'):
        specialty_main = result["Specialty"]["main"]
        specialty_email = result["Specialty"]["email"]
    else:
        specialty_main = 'Not found'
        specialty_email = 'Not found'

    if result.get('Total Pts Seen'):
        total_pts_main = result["Total Pts Seen"]["main"]
        total_pts_email = result["Total Pts Seen"]["email"]
    else:
        total_pts_main = 'Not found'
        total_pts_email = 'Not found'

    if result.get('Total Office Visits'):
        total_office_main = result["Total Office Visits"]["main"]
        total_office_email = result["Total Office Visits"]["email"]
    else:
        total_office_main = 'Not found'
        total_office_email = 'Not found'

    if result.get('Total Appointments Changed'):
        appts_changed_main = result["Total Appointments Changed"]["main"]
        appts_changed_email = result["Total Appointments Changed"]["email"]
    else:
        appts_changed_main = 'Not found'
        appts_changed_email = 'Not found'

    if result.get('Total Appts Cancelled w/o Rescheduling'):
        appts_cancel_main = result["Total Appts Cancelled w/o Rescheduling"]["main"]
        appts_cancel_email = result["Total Appts Cancelled w/o Rescheduling"]["email"]
    else:
        appts_cancel_main = 'Not found'
        appts_cancel_email = 'Not found'

    if result.get('Hyg Reservation (Next 7 Days)'):
        hyg_reserve_main = result["Hyg Reservation (Next 7 Days)"]["main"]
        hyg_reserve_email = result["Hyg Reservation (Next 7 Days)"]["email"]
    else:
        hyg_reserve_main = 'Not found'
        hyg_reserve_email = 'Not found'

    if result.get('Hygiene Appointment Capacity'):
        hyg_cap_main = result["Hygiene Appointment Capacity"]["main"]
        hyg_cap_email = result["Hygiene Appointment Capacity"]["email"]
    else:
        hyg_cap_main = 'Not found'
        hyg_cap_email = 'Not found'

    if result.get('Reactivation Calls Made'):
        react_calls_main = result["Reactivation Calls Made"]["main"]
        react_calls_email = result["Reactivation Calls Made"]["email"]
    else:
        react_calls_main = 'Not found'
        react_calls_email = 'Not found'

    if result.get('Total $ Amount Of Restorative Appts Made Today'):
        res_apps_main = result["Total $ Amount Of Restorative Appts Made Today"]["main"]
        res_apps_email = result["Total $ Amount Of Restorative Appts Made Today"]["email"]
    else:
        res_apps_main = 'Not found'
        res_apps_email = 'Not found'

    if result.get('Endo'):
        endo_main = result["Endo"]["main"]
        endo_email = result["Endo"]["email"]
    else:
        endo_main = 'Not found'
        endo_email = 'Not found'
    
    if result.get('Clear Aligners'):
        clear_aligners_main = result["Clear Aligners"]["main"]
        clear_aligners_email = result["Clear Aligners"]["email"]
    else:
        clear_aligners_main = 'Not found'
        clear_aligners_email = 'Not found'

    if result.get('Total Guests From Today With Future Hyg Appt'):
        guest_appt_main = result["Total Guests From Today With Future Hyg Appt"]["main"]
        guest_appt_email = result["Total Guests From Today With Future Hyg Appt"]["email"]
    else:
        guest_appt_main = 'Not found'
        guest_appt_email = 'Not found'

    if result.get('Number of unscheduled treatment calls made today'):
        unsched_treat_main = result["Number of unscheduled treatment calls made today"]["main"]
        unsched_treat_email = result["Number of unscheduled treatment calls made today"]["email"]
    else:
        unsched_treat_main = 'Not found'
        unsched_treat_email = 'Not found'

    if result.get('# of Recalls Made'):
        recalls_main = result["# of Recalls Made"]["main"]
        recalls_email = result["# of Recalls Made"]["email"]
    else:
        recalls_main = 'Not found'
        recalls_email = 'Not found'

    
    created_at = datetime.now()
    updated_at = datetime.now()

    test_result = EodTestResults(
        user_id = current_user.id,
        test_code = testcode,
        collection_main = collection_main,
        collection_bd = collection_bd,
        collection_email = collection_email,
        adjustments_main = adjustments_main,
        adjustments_bd = adjustments_bd,
        adjustments_email = adjustments_email,
        case_accpt_main = case_accpt_main,
        case_accpt_bd = case_accpt_bd,
        case_accpt_email = case_accpt_email,
        miss_ref_main = miss_ref_main,
        miss_ref_bd = miss_ref_bd,
        miss_ref_email = miss_ref_email,
        no_show_main = no_show_main,
        no_show_bd = no_show_bd,
        no_show_email = no_show_email,
        daily_coll_main = daily_coll_main,
        daily_coll_bd = daily_coll_bd,
        daily_coll_email = daily_coll_email,
        hyg_reapp_main = hyg_reapp_main,
        hyg_reapp_bd = hyg_reapp_bd,
        hyg_reapp_email = hyg_reapp_email,
        new_patient_main = new_patient_main,
        new_patient_bd = new_patient_bd,
        new_patient_email = new_patient_email,
        sd_treat_main = sd_treat_main,
        sd_treat_bd = sd_treat_bd,
        sd_treat_email = sd_treat_email,
        pt_portion_main = pt_portion_main,
        pt_portion_bd = pt_portion_bd,
        pt_portion_email = pt_portion_email,
        booked_prod_main = booked_prod_main,
        booked_prod_email = booked_prod_email,
        daily_net_main = daily_net_main,
        daily_net_email = daily_net_email,
        daily_gross_main = daily_gross_main,
        daily_gross_email = daily_gross_email,
        sched_vs_goal_main = sched_vs_goal_main,
        sched_vs_goal_email = sched_vs_goal_email,
        general_main = general_main,
        general_email = general_email,
        ortho_prod_main = ortho_prod_main,
        ortho_prod_email = ortho_prod_email,
        perio_prod_main = perio_prod_main,
        perio_prod_email = perio_prod_email,
        oral_surgery_main = oral_surgery_main,
        oral_surgery_email = oral_surgery_email,
        num_prod_main = num_prod_main,
        num_prod_email = num_prod_email,
        adp_main = adp_main,
        adp_email = adp_email,
        specialty_main = specialty_main,
        specialty_email = specialty_email,
        total_pts_main = total_pts_main,
        total_pts_email = total_pts_email,
        total_office_main = total_pts_email,
        total_office_email = total_office_email,
        appts_changed_main = appts_changed_main,
        appts_changed_email = appts_changed_email,
        appts_cancel_main = appts_cancel_main,
        appts_cancel_email = appts_cancel_email,
        hyg_reserve_main = hyg_reserve_main,
        hyg_reserve_email = hyg_reserve_email,
        hyg_cap_main = hyg_cap_main,
        hyg_cap_email = hyg_cap_email,
        react_calls_main = react_calls_main,
        react_calls_email = react_calls_email,
        res_apps_main = res_apps_main,
        res_apps_email = res_apps_email,
        endo_main = endo_main,
        endo_email = endo_email,
        clear_aligners_main = clear_aligners_main,
        clear_aligners_email = clear_aligners_email,
        guest_appt_main = guest_appt_main,
        guest_appt_email = guest_appt_email,
        unsched_treat_main = unsched_treat_main,
        unsched_treat_email = unsched_treat_email,
        recalls_main = recalls_main,
        recalls_email = recalls_email,
        created_at = created_at,
        updated_at = updated_at
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
        
        # bd_result = cleanValues(bd_result)
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

        # GET MAIN PAGE VALUES
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

        # SEND EMAIL
        send_eod["submit_btn"].findElement(driver)
        send_eod["submit_btn"].click(driver)

        send_eod["recipients"].findElement(driver)
        send_eod["sndeod_email"].findElement(driver)
        send_eod["sndeod_email"].element.send_keys("eod.test.jap@gmail.com\n")

        send_eod["send_summary"].findElement(driver)
        send_eod["send_summary"].click(driver)

        # OPEN GMAIL THEN LOGIN
        # Some cases may occur when google has some dialog. In this case, the test would fail.
        driver.get("https://mail.google.com/")
        gmail_elements = getGmailXpath()

        gmail_elements['email'].findElement(driver)
        gmail_elements['email'].element.send_keys('eod.test.jap@gmail.com\n')

        gmail_elements['password'].findElement(driver)
        gmail_elements['password'].element.send_keys('ZsRL3Yk3crboXq\n')

        # OPEN FIRST EMAIL RECEIVED.
        gmail_elements['first_email'].findElement(driver)
        gmail_elements['first_email'].click(driver)

        metric_collection = EmailData.getMetricsCollection()
        metric_collection.findElement(driver)

        num_of_metrics = metric_collection.getValue()

        # GET EMAIL METRIC VALUES
        for i in range(1, num_of_metrics+1):
            email_metric = EmailData.getMetric(i)

            email_metric['name'].findElement(driver)
            name = email_metric['name'].getValue()

            email_metric['value'].findElement(driver)
            value = email_metric['value'].getValue()
            main_test_result[name]['email'] = value

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
        dict[metric]['main'] = re.sub("[^-0-9.a-zA-Z/\s()]", "", dict[metric]['main']).strip()
        dict[metric]['breakdown'] = re.sub("[^-0-9.a-zA-Z/\s()]", "", dict[metric]['breakdown']).strip()
        dict[metric]['email'] = re.sub("[^-0-9.a-zA-Z/\s()]", "", dict[metric]['email']).strip()
        if re.search("\(.*\)", dict[metric]['main']):
            dict[metric]['main'] = re.sub('[()]', "", dict[metric]['main'])
            dict[metric]['main'] = "-" + dict[metric]['main']
        if re.search("\(.*\)", dict[metric]['breakdown']):
            dict[metric]['breakdown'] = re.sub('[()]', "", dict[metric]['breakdown'])
            print(dict[metric]['breakdown'])
            dict[metric]['breakdown'] = "-" + dict[metric]['breakdown']
        if re.search("\(.*\)", dict[metric]['email']):
            dict[metric]['email'] = re.sub('[()]', "", dict[metric]['email'])
            dict[metric]['email'] = "-" + dict[metric]['email']
    
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

def bundleResults(bd_result, email_result):
    keys = { *bd_result.keys(), *email_result.keys() }
    
    bundled_result = {}
    for key in keys:
        bundled_result[key] = {}
        bundled_result[key]["main"] = (email_result[key]['main'] if email_result[key]['main'] != "-" else "0") if email_result[key].get('main') else bd_result[key]['main']
        bundled_result[key]["breakdown"] = (bd_result[key]['breakdown'] if email_result[key]['main'] != "-" else "0") if bd_result.get(key) and bd_result[key].get('breakdown') else "No breakdown for this metric."
        bundled_result[key]["email"] = (email_result[key]['email'] if email_result[key]['email'] != "-" else "0") if email_result[key].get('email') else "Not in email."

    return bundled_result

def getLastTest(testcode=None):
    last_test = None
    if testcode:
        last_test = EodTestResults.query.filter_by(test_code=testcode).order_by(EodTestResults.id.desc()).first()
    else: 
        last_test = EodTestResults.query.order_by(EodTestResults.id.desc()).first()

    try:
        last_test.collection_main = float(last_test.collection_main)
        last_test.collection_bd = float(last_test.collection_bd)
        last_test.collection_email = float(last_test.collection_email)
    except:
        pass

    try:
        last_test.booked_prod_main = float(last_test.booked_prod_main)
        last_test.booked_prod_email = float(last_test.booked_prod_email)
    except:
        pass

    try:
        last_test.adjustments_main = float(last_test.adjustments_main)
        last_test.adjustments_bd = float(last_test.adjustments_bd)
        last_test.adjustments_email = float(last_test.adjustments_email)
    except:
        pass

    try:
        last_test.case_accpt_main = float(last_test.case_accpt_main)
        last_test.case_accpt_bd = float(last_test.case_accpt_bd)
        last_test.case_accpt_email = float(last_test.case_accpt_email)
    except:
        pass

    try:
        last_test.miss_ref_main = float(last_test.miss_ref_main)
        last_test.miss_ref_bd = float(last_test.miss_ref_bd)
        last_test.miss_ref_email = float(last_test.miss_ref_email)
    except:
        pass

    try:
        last_test.no_show_main = float(last_test.no_show_main)
        last_test.no_show_bd = float(last_test.no_show_bd)
        last_test.no_show_email = float(last_test.no_show_email)
    except:
        pass

    try:
        last_test.daily_coll_main = float(last_test.daily_coll_main)
        last_test.daily_coll_bd = float(last_test.daily_coll_bd)
        last_test.daily_coll_email = float(last_test.email)
    except:
        pass

    try:
        last_test.hyg_reapp_main = float(last_test.hyg_reapp_main)
        last_test.hyg_reapp_bd = float(last_test.hyg_reapp_bd)
        last_test.hyg_reapp_email = float(last_test.hyg_reapp_email)
    except:
        pass

    try:
        last_test.new_patient_main = float(last_test.new_patient_main)
        last_test.new_patient_bd = float(last_test.new_patient_bd)
        last_test.new_patient_email = float(last_test.new_patient_email)
    except:
        pass

    try:
        last_test.sd_treat_main = float(last_test.sd_treat_main)
        last_test.sd_treat_bd = float(last_test.sd_treat_bd)
        last_test.sd_treat_email = float(last_test.sd_treat_email)
    except:
        pass

    try:
        last_test.pt_portion_main = float(last_test.pt_portion_main)
        last_test.pt_portion_bd = float(last_test.pt_portion_bd)
        last_test.pt_portion_email = float(last_test.pt_portion_email)
    except:
        pass
    
    try:
        last_test.daily_net_main = float(last_test.daily_net_main)
        last_test.daily_net_email = float(last_test.daily_net_email)
    except:
        pass

    try:
        last_test.daily_gross_main = float(last_test.daily_gross_main)
        last_test.daily_gross_email = float(last_test.daily_gross_email)
    except:
        pass

    try:
        last_test.sched_vs_goal_main = float(last_test.sched_vs_goal_main)
        last_test.sched_vs_goal_email = float(last_test.sched_vs_goal_email)
    except:
        pass

    try:
        last_test.general_main = float(last_test.general_main)
        last_test.general_email = float(last_test.general_email)
    except:
        pass

    try:
        last_test.ortho_prod_main = float(last_test.ortho_prod_main)
        last_test.ortho_prod_email = float(last_test.ortho_prod_email)
    except:
        pass
    
    try:
        last_test.perio_prod_main = float(last_test.perio_prod_main)
        last_test.perio_prod_email = float(last_test.perio_prod_email)
    except:
        pass

    try:
        last_test.oral_surgery_main = float(last_test.oral_surgery_main)
        last_test.oral_surgery_email = float(last_test.oral_surgery_email)
    except:
        pass

    try:
        last_test.num_prod_main = float(last_test.num_prod_main)
        last_test.num_prod_email = float(last_test.num_prod_email)
    except:
        pass

    try:
        last_test.adp_main = float(last_test.adp_main)
        last_test.adp_email = float(last_test.adp_email)
    except:
        pass

    try:
        last_test.specialty_main = float(last_test.specialty_main)
        last_test.specialty_email = float(last_test.specialty_email)
    except:
        pass
    
    try:
        last_test.total_pts_main = float(last_test.total_pts_main)
        last_test.total_pts_email = float(last_test.total_pts_email)
    except:
        pass

    try:
        last_test.total_office_main = float(last_test.total_office_main)
        last_test.total_office_email = float(last_test.total_office_email)
    except:
        pass

    try:
        last_test.appts_changed_main = float(last_test.appts_changed_main)
        last_test.appts_changed_email = float(last_test.appts_changed_email)
    except:
        pass

    try:
        last_test.appts_cancel_main = float(last_test.appts_cancel_main)
        last_test.appts_cancel_email = float(last_test.appts_cancel_email)
    except:
        pass

    try:
        last_test.hyg_reserve_main = float(last_test.hyg_reserve_main)
        last_test.hyg_reserve_email = float(last_test.hyg_reserve_email)
    except:
        pass

    try:
        last_test.hyg_cap_main = float(last_test.hyg_cap_main)
        last_test.hyg_cap_email = float(last_test.hyg_cap_email)
    except:
        pass

    try:
        last_test.react_calls_main = float(last_test.react_calls_main)
        last_test.react_calls_email = float(last_test.react_calls_email)
    except:
        pass

    try:
        last_test.res_apps_main = float(last_test.res_apps_main)
        last_test.res_apps_email = float(last_test.res_apps_email)
    except:
        pass

    try:
        last_test.endo_main = float(last_test.endo_main)
        last_test.endo_email = float(last_test.endo_email)
    except:
        pass

    try:
        last_test.clear_aligners_main = float(last_test.clear_aligners_main)
        last_test.clear_aligners_email = float(last_test.clear_aligners_email)
    except:
        pass

    try:
        last_test.guest_appt_main = float(last_test.guest_appt_main)
        last_test.guest_appt_email = float(last_test.guest_appt_email)
    except:
        pass

    try:
        last_test.unsched_treat_main = float(last_test.unsched_treat_main)
        last_test.unsched_treat_email = float(last_test.unsched_treat_email)
    except:
        pass

    try:
        last_test.recalls_main = float(last_test.recalls_main)
        last_test.recalls_email = float(last_test.recalls_email)
    except:
        pass

    return last_test

def getTestCodeInfo(testcode):
    return TestCodes.query.filter_by(test_code=testcode).first()

def getGraphData(last_test):
    bd_success = 0
    bd_fail = 0
    email_success = 0
    email_fail = 0

    if (last_test.collection_main == last_test.collection_bd):
        bd_success += 1
    else:
        bd_fail += 1

    if (last_test.adjustments_main == last_test.adjustments_bd):
        bd_success += 1
    else:
        bd_fail += 1

    if (last_test.case_accpt_main == last_test.case_accpt_bd):
        bd_success += 1
    else:
        bd_fail += 1

    if (last_test.miss_ref_main == last_test.miss_ref_bd):
        bd_success += 1
    else:
        bd_fail += 1

    if (last_test.no_show_main == last_test.no_show_bd):
        bd_success += 1
    else:
        bd_fail += 1
    
    if (last_test.daily_coll_main == last_test.daily_coll_bd):
        bd_success += 1
    else:
        bd_fail += 1

    if (last_test.hyg_reapp_main == last_test.hyg_reapp_bd):
        bd_success += 1
    else:
        bd_fail += 1

    if (last_test.new_patient_main == last_test.new_patient_bd):
        bd_success += 1
    else:
        bd_fail += 1

    if (last_test.sd_treat_main == last_test.sd_treat_bd):
        bd_success += 1
    else:
        bd_fail += 1

    if (last_test.pt_portion_main == last_test.pt_portion_bd):
        bd_success += 1
    else:
        bd_fail += 1    

    if (last_test.collection_main == last_test.collection_email):
        email_success += 1
    else:
        email_fail += 1

    if (last_test.adjustments_main == last_test.adjustments_email):
        email_success += 1
    else:
        email_fail += 1

    if (last_test.case_accpt_main == last_test.case_accpt_email):
        email_success += 1
    else:
        email_fail += 1

    if (last_test.miss_ref_main == last_test.miss_ref_email):
        email_success += 1
    else:
        email_fail += 1

    if (last_test.no_show_main == last_test.no_show_email):
        email_success += 1
    else:
        email_fail += 1

    if (last_test.daily_coll_main == last_test.daily_coll_email):
        email_success += 1
    else:
        email_fail += 1

    if (last_test.hyg_reapp_main == last_test.hyg_reapp_email):
        email_success += 1
    else:
        email_fail += 1

    if (last_test.new_patient_main == last_test.new_patient_email):
        email_success += 1
    else:
        email_fail += 1

    if (last_test.sd_treat_main == last_test.sd_treat_email):
        email_success += 1
    else:
        email_fail += 1

    if (last_test.pt_portion_main == last_test.pt_portion_email):
        email_success += 1
    else:
        email_fail += 1
    
    if (last_test.booked_prod_main == last_test.booked_prod_email):
        email_success += 1
    else:
        email_fail += 1

    if (last_test.daily_net_main == last_test.daily_net_email):
        email_success += 1
    else:
        email_fail += 1

    if (last_test.daily_gross_main == last_test.daily_gross_email):
        email_success += 1
    else:
        email_fail += 1

    if (last_test.sched_vs_goal_main == last_test.sched_vs_goal_email):
        email_success += 1
    else:
        email_fail += 1

    if (last_test.general_main == last_test.general_email):
        email_success += 1
    else:
        email_fail += 1

    if (last_test.ortho_prod_main == last_test.ortho_prod_email):
        email_success += 1
    else:
        email_fail += 1

    if (last_test.perio_prod_main == last_test.perio_prod_email):
        email_success += 1
    else:
        email_fail += 1

    if (last_test.oral_surgery_main == last_test.oral_surgery_email):
        email_success += 1
    else:
        email_fail += 1

    if (last_test.num_prod_main == last_test.num_prod_email):
        email_success += 1
    else:
        email_fail += 1

    if (last_test.adp_main == last_test.adp_email):
        email_success += 1
    else:
        email_fail += 1

    if (last_test.specialty_main == last_test.specialty_email):
        email_success += 1
    else:
        email_fail += 1

    if (last_test.total_pts_main == last_test.total_pts_email):
        email_success += 1
    else:
        email_fail += 1

    if (last_test.total_office_main == last_test.total_office_email):
        email_success += 1
    else:
        email_fail += 1
    
    if (last_test.appts_changed_main == last_test.appts_changed_email):
        email_success += 1
    else:
        email_fail += 1

    if (last_test.appts_cancel_main == last_test.appts_cancel_email):
        email_success += 1
    else:
        email_fail += 1

    if (last_test.hyg_reserve_main == last_test.hyg_reserve_email):
        email_success += 1
    else:
        email_fail += 1

    if (last_test.hyg_cap_main == last_test.hyg_cap_email):
        email_success += 1
    else:
        email_fail += 1

    if (last_test.react_calls_main == last_test.react_calls_email):
        email_success += 1
    else:
        email_fail += 1

    if (last_test.res_apps_main == last_test.res_apps_email):
        email_success += 1
    else:
        email_fail += 1

    if (last_test.endo_main == last_test.endo_email):
        email_success += 1
    else:
        email_fail += 1

    if (last_test.clear_aligners_main == last_test.clear_aligners_email):
        email_success += 1
    else:
        email_fail += 1

    if (last_test.guest_appt_main == last_test.guest_appt_email):
        email_success += 1
    else:
        email_fail += 1

    if (last_test.unsched_treat_main == last_test.unsched_treat_email):
        email_success += 1
    else:
        email_fail += 1

    if (last_test.recalls_main == last_test.recalls_email):
        email_success += 1
    else:
        email_fail += 1

    return {
        'bd_success': bd_success,
        'bd_fail': bd_fail,
        'email_success': email_success,
        'email_fail': email_fail
    }