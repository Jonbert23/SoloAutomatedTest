from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from .Dashboard_xpath import BreakdownXpath, GlobalXpath, ProductionTest, ServiceTest, BusinessTest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from Project.Controller.Global_Controller.Global_test import Login
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from Project.Controller.Global_Controller.Global_test import calendarDateRange
from ...models import TestCodes, DashboardBreakdownTest, DashboardProductionTest, DashboardServiceCountTest, DashboardServiceProcedureTest, DashboardLOBProductionTest, DashboardLOBSpecialityTest
from ... import db
from collections import Counter

# --Blueprint
dash = Blueprint('dash', __name__)

@login_required
@dash.route("/dashboard", methods=['POST', 'GET'])
def dashboard():
    testcode_info = None
    breakdown_value = None
    production_value = None
    count_value = [None]
    count_status = None
    count_status_pass = None
    count_status_fail = None
    proced_value = [None]
    proced_status = None
    proced_status_pass = None
    proced_status_fail = None
    lobs_status_pass = None
    lobs_status_fail = None
    lob_result = {'Doctor': [[], []], 'Endo': [[], []], 'Hygiene': [[], []], 'Invisalign': [[], []], 'Oral Surgery': [[], []],
                  'Ortho': [[], []], 'Pedo': [[], []], 'Perio': [[], []], 'Prosthe': [[], []], 'Others': [[], []]}
    if request.method == 'POST':
        test_code = request.form['testcode']
        dash_testcodes = [stat_c[0] for stat_c in DashboardBreakdownTest.query.with_entities(DashboardBreakdownTest.test_code).all()]
        if test_code not in dash_testcodes:
            testcode_info = TestCodes.query.filter_by(test_code=test_code).first()
            if testcode_info:
                optional_test = request.form.getlist('Optional')
                d = DesiredCapabilities.CHROME
                d['loggingPrefs'] = {'browser': 'ERROR'}
                driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), desired_capabilities=d)
                Login.login(driver, f"{testcode_info.client_link}/solo/results", testcode_info.client_username, testcode_info.client_password)

                if not driver:
                    return False

                date_from = testcode_info.test_date_from
                date_to = testcode_info.test_date_to

                automationTest(driver, date_from, date_to, optional_test, test_code)
                # Count Performed Test
                per_test = int(testcode_info.test_modules)
                testcode_info.test_modules = str(per_test + 1)
                db.session.commit()
                # Breakdown Test Value
                breakdown_value = DashboardBreakdownTest.query.filter_by(test_code=test_code).first()
                #Production Test Value
                production_value = DashboardProductionTest.query.filter_by(test_code=test_code).first()
                #Service Count Test Value
                count_value = DashboardServiceCountTest.query.filter_by(test_code=test_code).all()
                count_status = [stat_c[0] for stat_c in DashboardServiceCountTest.query.filter_by(test_code=test_code).with_entities(DashboardServiceCountTest.count_status).all()]
                count_status_pass = Counter(count_status)['Pass']
                count_status_fail = Counter(count_status)['Fail']

                # Service Procedure Test Value
                proced_value = DashboardServiceProcedureTest.query.filter_by(test_code=test_code).all()
                proced_status = [stat_c[0] for stat_c in DashboardServiceProcedureTest.query.filter_by(test_code=test_code).with_entities(DashboardServiceProcedureTest.proced_status).all()]
                proced_status_pass = Counter(proced_status)['Pass']
                proced_status_fail = Counter(proced_status)['Fail']

                # LOB
                lob_valid = DashboardLOBProductionTest.query.filter_by(test_code=test_code).first()
                if lob_valid:
                    lobs = ['Doctor', 'Endo', 'Hygiene', 'Invisalign', 'Oral Surgery', 'Ortho', 'Pedo', 'Perio', 'Prosthe',
                            'Others']
                    lob_result = {}
                    for lob in lobs:
                        lob_result[lob] = []
                        spec_value = []
                        prod_lob = DashboardLOBProductionTest.query.filter_by(test_code=test_code).filter_by(
                            line_bussiness=lob).first()
                        provd_name = [n[0] for n in
                                      DashboardLOBSpecialityTest.query.filter_by(production_id=prod_lob.id).with_entities(
                                          DashboardLOBSpecialityTest.providers_name).all()]
                        provd_spec = [s[0] for s in
                                      DashboardLOBSpecialityTest.query.filter_by(production_id=prod_lob.id).with_entities(
                                          DashboardLOBSpecialityTest.providers_speciality).all()]
                        spec_status = [doc[0] for doc in
                                       DashboardLOBSpecialityTest.query.filter_by(production_id=prod_lob.id).with_entities(
                                           DashboardLOBSpecialityTest.speciality_status).all()]
                        prod_status = [prod_lob.production_status]
                        prod_status.extend(spec_status)
                        lob_result[lob].append(prod_status)
                        lob_result[lob].append(
                            [prod_lob.netprod_base, prod_lob.providers_data, prod_lob.table_total, prod_lob.production_status])
                        for (name, spec, stat) in zip(provd_name, provd_spec, spec_status):
                            if provd_name:
                                spec_value.append([name, spec, stat])
                            else:
                                spec_value.append(None)

                        lob_result[lob].append(spec_value)

                    # all LOB status for chart
                    lobs_list = []
                    for status in lobs:
                        global_status = lob_result[status][0]
                        lobs_list.append(global_status)

                    lobs_status = sum(lobs_list, [])
                    lobs_status_pass = Counter(lobs_status)['Pass']
                    lobs_status_fail = Counter(lobs_status)['Fail']
            else:
                flash(f'Test Code [{test_code}] Does Not Exist!','info')
        else:
            flash(f'This Test Code already Tested in this Module, you can search the Test Result! [{test_code}].', 'info')

    return render_template('Dashboard_Template/Dashboard_index.html', testcode_info=testcode_info, breakdown_value=breakdown_value, production_value=production_value,
                           count_value=count_value, count_status=count_status, count_status_pass=count_status_pass, count_status_fail=count_status_fail,
                           proced_value=proced_value, proced_status=proced_status, proced_status_pass=proced_status_pass, proced_status_fail=proced_status_fail,
                           lob_result=lob_result, lobs_status_pass=lobs_status_pass, lobs_status_fail=lobs_status_fail)

@login_required
@dash.route("/dashboard/search", methods=['POST', 'GET'])
def searchTest():
    testcode_info = None
    breakdown_value = None
    production_value = None
    count_value = [None]
    count_status = None
    count_status_pass = None
    count_status_fail = None
    proced_value = [None]
    proced_status = None
    proced_status_pass = None
    proced_status_fail = None
    lobs_status_pass = None
    lobs_status_fail = None
    lob_result = {'Doctor': [[], []], 'Endo': [[], []], 'Hygiene': [[], []], 'Invisalign': [[], []], 'Oral Surgery': [[], []],
                  'Ortho': [[], []], 'Pedo': [[], []], 'Perio': [[], []], 'Prosthe': [[], []], 'Others': [[], []]}
    if request.method == 'POST':
        test_code = request.form['searchtestcode']
        testcode_info = TestCodes.query.filter_by(test_code=test_code).first()
        if testcode_info:
            dash_testcodes = [stat_c[0] for stat_c in DashboardBreakdownTest.query.with_entities(DashboardBreakdownTest.test_code).all()]
            if test_code in dash_testcodes:
                # Breakdown Test Value
                breakdown_value = DashboardBreakdownTest.query.filter_by(test_code=test_code).first()
                # Production Test Value
                production_value = DashboardProductionTest.query.filter_by(test_code=test_code).first()
                # Service Count Test Value
                count_value = DashboardServiceCountTest.query.filter_by(test_code=test_code).all()
                count_status = [stat_c[0] for stat_c in DashboardServiceCountTest.query.filter_by(test_code=test_code).with_entities(DashboardServiceCountTest.count_status).all()]
                count_status_pass = Counter(count_status)['Pass']
                count_status_fail = Counter(count_status)['Fail']
                # Service Procedure Test Value
                proced_value = DashboardServiceProcedureTest.query.filter_by(test_code=test_code).all()
                proced_status = [stat_c[0] for stat_c in DashboardServiceProcedureTest.query.filter_by(test_code=test_code).with_entities(DashboardServiceProcedureTest.proced_status).all()]
                proced_status_pass = Counter(proced_status)['Pass']
                proced_status_fail = Counter(proced_status)['Fail']

                # LOB
                lob_valid = DashboardLOBProductionTest.query.filter_by(test_code=test_code).first()
                if lob_valid:
                    lobs= ['Doctor', 'Endo', 'Hygiene', 'Invisalign', 'Oral Surgery', 'Ortho', 'Pedo', 'Perio', 'Prosthe', 'Others']
                    lob_result = {}
                    for lob in lobs:
                        lob_result[lob]=[]
                        spec_value = []
                        prod_lob = DashboardLOBProductionTest.query.filter_by(test_code=test_code).filter_by(line_bussiness=lob).first()
                        provd_name = [n[0] for n in DashboardLOBSpecialityTest.query.filter_by(production_id=prod_lob.id).with_entities(DashboardLOBSpecialityTest.providers_name).all()]
                        provd_spec = [s[0] for s in DashboardLOBSpecialityTest.query.filter_by(production_id=prod_lob.id).with_entities(DashboardLOBSpecialityTest.providers_speciality).all()]
                        spec_status = [doc[0] for doc in DashboardLOBSpecialityTest.query.filter_by(production_id=prod_lob.id).with_entities(DashboardLOBSpecialityTest.speciality_status).all()]
                        prod_status = [prod_lob.production_status]
                        prod_status.extend(spec_status)
                        lob_result[lob].append(prod_status)
                        lob_result[lob].append([prod_lob.netprod_base, prod_lob.providers_data, prod_lob.table_total, prod_lob.production_status])
                        for (name, spec, stat) in zip(provd_name, provd_spec, spec_status):
                            if provd_name:
                                spec_value.append([name, spec, stat])
                            else:
                                spec_value.append(None)

                        lob_result[lob].append(spec_value)

                    # all LOB status for chart
                    lobs_list = []
                    for status in lobs:
                        global_status = lob_result[status][0]
                        lobs_list.append(global_status)

                    lobs_status = sum(lobs_list, [])
                    lobs_status_pass = Counter(lobs_status)['Pass']
                    lobs_status_fail = Counter(lobs_status)['Fail']
            else:
                flash(f'Please Run This Test Code First [{test_code}].', 'info')
        else:
            flash(f'Test Code [{test_code}] does not Exist.', 'info')

    return render_template('Dashboard_Template/Dashboard_index.html', testcode_info=testcode_info, breakdown_value=breakdown_value, production_value=production_value,
                               count_value=count_value, count_status=count_status, count_status_pass=count_status_pass, count_status_fail=count_status_fail,
                               proced_value=proced_value, proced_status=proced_status, proced_status_pass=proced_status_pass, proced_status_fail=proced_status_fail,
                               lob_result=lob_result, lobs_status_pass=lobs_status_pass, lobs_status_fail=lobs_status_fail)

def getmetricsXpath(metrics, test):
    metric = {}
    if test == "brkTest":
        for x in metrics:
            metric[x] = BreakdownXpath.financial_dataxpath[x]

        return metric

    if test == "prodTest":
        for x in metrics:
            metric[x] = ProductionTest.production_testxpath[x]

        return metric

# BreakDown Test
def breakdownTest(driver):
    metrics = ["net_prod", "gross_prod", "collection", "adjustment", "newpatient_visit", "existingpatient_visit"]
    metricsXpath = getmetricsXpath(metrics, "brkTest")
    values = {}

    if metrics:
        for metric in metricsXpath:
            values[metric] = []
            metric_base = metricsXpath[metric][0]
            metric_brk = metricsXpath[metric][1]
            metric_brktotal = metricsXpath[metric][2]
            metric_brkclose = metricsXpath[metric][3]

            values[metric].append(WebDriverWait(driver, 120).until(
                EC.visibility_of_element_located((By.XPATH, f"{metric_base}"))).text.replace('$ ','').replace('(', '-').replace(')','').replace(',',''))
            breakdown_btn = driver.find_element(by=By.XPATH, value=f'{metric_brk}')
            breakdown_btn.click()
            if metric == "newpatient_visit":
                npv_base = WebDriverWait(driver, 120).until(
                    EC.visibility_of_element_located((By.XPATH, f"{metric_base}"))).text.replace('$ ', '').replace('(','-').replace(')', '').replace(',', '')


                if npv_base != '0':
                    npv_count = WebDriverWait(driver, 10).until(
                        EC.presence_of_all_elements_located((By.XPATH, f"{metric_brktotal}"))
                    )
                    print(str(len(npv_count)))
                    values[metric].append(str(len(npv_count)))
                else:
                    print("No Value")
                    values[metric].append(str(0))
            else:
                values[metric].append(WebDriverWait(driver, 120).until(
                    EC.visibility_of_element_located((By.XPATH, f"{metric_brktotal}"))).text.replace('$ ','').replace('(', '-').replace(')','').replace(',',''))

            breakdown_close = driver.find_element(by=By.XPATH, value=f'{metric_brkclose}')
            breakdown_close.click()

            status = testValue(values[metric])
            values[metric].append(status)

    return values



# Production Test
def productionTest(driver):
    metrics = ["providers_data", "table_total", "payor_score"]
    metricsXpath = getmetricsXpath(metrics, "prodTest")
    values = {}

    if metrics:
        net_prod = WebDriverWait(driver, 120).until(
            EC.visibility_of_element_located((By.XPATH, f"{ProductionTest.netprod_base}"))).text.replace('$ ','').replace('(', '-').replace(')','').replace(',','')

        for metric in metricsXpath:
            values[metric] = []
            metric_base = metricsXpath[metric][0]
            if metric != "payor_score":
                values[metric].append(WebDriverWait(driver, 120).until(
                    EC.visibility_of_element_located((By.XPATH, f"{metric_base}"))).text.replace('$ ','').replace('(', '-').replace(')','').replace(',',''))
                values[metric].append(net_prod)
            else:
                metric_view = WebDriverWait(driver, 120).until(
                        EC.visibility_of_element_located((By.XPATH, f"{GlobalXpath.metric_view}")))
                actions = ActionChains(driver)
                actions.move_to_element(metric_view).click().perform()

                values[metric].append(WebDriverWait(driver, 120).until(
                    EC.visibility_of_element_located((By.XPATH, f"{metric_base}"))).text.replace('$ ','').replace('(', '-').replace(')','').replace(',',''))
                values[metric].append(net_prod)

            status = testValue(values[metric])
            values[metric].append(status)

    return values

def testValue(values):
    if values[0] != values[1]:
        status = "Fail"

    if values[0] == values[1]:
        status = "Pass"

    return status

# Service Test
def countTest(driver):
    service_code = driver.find_elements(By.XPATH, f"{ServiceTest.service_code}")
    service_provider = driver.find_elements(By.XPATH, f"{ServiceTest.service_provider}")
    service_count = driver.find_elements(By.XPATH, f"{ServiceTest.service_count}")
    if service_code:
        values = {}
        for c, (codes, providers, counts) in enumerate(zip(service_code, service_provider, service_count)):
            code = codes.text
            provd = providers.text
            count = counts.text
            if c == 10:
                break

            else:
                values[c] = []
                service = []
                count_basebrk = []
                service.append(code)
                service.append(provd)

                # Count Base Table
                count_basebrk.append(count)

                # Count Breakdown Total
                count_breaktotal = countBreak(driver, c)
                count_basebrk.append(count_breaktotal)

                if count == count_breaktotal:
                    count_basebrk.append("Pass")
                else:
                    count_basebrk.append("Fail")

                # Append all to values list
                values[c].append(service)
                values[c].append(count_basebrk)

        return values

def procedureTest(driver):
    service_type = driver.find_elements(By.XPATH, f"{ServiceTest.service_type}")
    service_code = driver.find_elements(By.XPATH, f"{ServiceTest.service_code}")

    search_input = WebDriverWait(driver, 120).until(
        EC.visibility_of_element_located((By.XPATH, f"{ServiceTest.search_input}"))
    )
    val_codes = []
    values = {}
    for c, (codes, types) in enumerate(zip(service_code, service_type)):
        code = codes.text
        type = types.text
        if c == 10:
            break

        else:
            values[c] = []
            service = []
            val_codes.append(code)
            service.append(code)
            service.append(type)
            values[c].append(service)

    # Search Procedure Test
    for index, val_code in enumerate(val_codes):
        # Select All Search Input
        search_input.send_keys(Keys.CONTROL + "a")
        # Clear Search
        search_input.send_keys(Keys.DELETE)
        # Input Code
        search_input.send_keys(val_code)
        # Enter Search
        search_input.send_keys(Keys.ENTER)

        search_code = searchCodes(val_code, driver)

        if len(search_code) == 0:
            search_proc = []
            search_proc.append("None")
            search_proc.append("Pass")
            values[index].append(search_proc)
        else:
            search_proc = []
            search_proc.append(search_code)
            search_proc.append("Fail")
            values[index].append(search_proc)

    return values

def searchCodes(value_code, driver):
    list_code = []
    search_code = driver.find_elements(By.XPATH, f"{ServiceTest.service_code}")
    for codes in search_code:
        code = codes.text
        if code != value_code and code not in list_code:
            list_code.append(code)

    return list_code

def countBreak(driver, count):
    breakdownbtn = driver.find_element(by=By.XPATH,
                                       value=f'//main/div[2]/section[4]/div/div[2]/div/div/table/tbody/tr[{count + 1}]/td[5]/span/span[2]/a[@class="hover:text-ja-green-200 text-xs text-gray-400 cursor-pointer dark:text-white"]')
    breakdownbtn.click()

    count_brktotal = WebDriverWait(driver, 120).until(
        EC.visibility_of_element_located((By.XPATH, f"{ServiceTest.count_brktotal}")))
    count_breaktotal = count_brktotal.text

    brk_close = WebDriverWait(driver, 120).until(
        EC.visibility_of_element_located((By.XPATH, f"{ServiceTest.brk_close}")))
    brk_close.click()

    return count_breaktotal

# LINE OF BUSINESS Test
def businessTest(driver):
    result_view = WebDriverWait(driver, 120).until(
        EC.visibility_of_element_located((By.XPATH, f"{GlobalXpath.result_view}")))
    actions = ActionChains(driver)
    actions.move_to_element(result_view).click().perform()
    clear_btn = WebDriverWait(driver, 120).until(
        EC.presence_of_element_located((By.XPATH, f"{BusinessTest.clear_btn}")))
    update_btn = WebDriverWait(driver, 120).until(
        EC.presence_of_element_located((By.XPATH, f"{GlobalXpath.update_btn}")))
    business_options = driver.find_elements(By.XPATH, f"{BusinessTest.business_options}")

    values={}
    for business in business_options:
        prod_test = []

        lineof_business = WebDriverWait(driver, 120).until(
            EC.element_to_be_clickable((By.XPATH, f"{BusinessTest.lineof_business}")))
        actions = ActionChains(driver)
        actions.move_to_element(lineof_business).click().perform()

        clear_btn.click()
        base_business = business.text
        values[base_business] = []
        business.click()
        update_btn.click()

        # Production Test
        fin_data = WebDriverWait(driver, 120).until(
            EC.visibility_of_element_located((By.XPATH, f"{ProductionTest.netprod_base}"))).text.replace('$ ', '').replace('(', '-').replace(')', '').replace(',','')
        prod_test.append(fin_data)
        prod_data = WebDriverWait(driver, 120).until(
            EC.visibility_of_element_located((By.XPATH, f"{ProductionTest.providers_data}"))).text.replace('$ ', '').replace('(', '-').replace(')', '').replace(',','')
        prod_test.append(prod_data)
        tabletotal_data = WebDriverWait(driver, 120).until(
            EC.visibility_of_element_located((By.XPATH, f"{ProductionTest.table_total}"))).text.replace('$ ', '').replace('(', '-').replace(')', '').replace(',','')
        prod_test.append(tabletotal_data)

        if prod_test[0] == prod_test[1] == prod_test[2]:
            status = "Pass"
        else:
            status = "Fail"
        prod_test.append(status)

        # Business Speciality Test
        provider_name = driver.find_elements(By.XPATH, f"{BusinessTest.provider_name}")
        business_brk = driver.find_elements(By.XPATH, f"{BusinessTest.business_brk}")
        spec_test = []
        for count, (providers, breakdown) in enumerate(zip(provider_name, business_brk)):
            if count == 5:
                break

            else:
                provd = []
                provider = providers.text
                provd.append(provider)

                breakdownbtn = driver.find_element(by=By.XPATH,
                                                   value=f'/html/body/div[1]/main/div[2]/section[3]/div[2]/div/div[2]/div/table/tbody/tr[{count+1}]/td[1]/span/span/a')
                breakdownbtn.click()

                speciality = WebDriverWait(driver, 120).until(
                    EC.presence_of_element_located((By.XPATH, f"{BusinessTest.speciality}")))
                spec = speciality.text
                provd.append(spec)

                close_btn = WebDriverWait(driver, 120).until(
                    EC.presence_of_element_located((By.XPATH, f"{BusinessTest.close_btn}")))
                close_btn.click()

                if base_business == spec:
                    status = "Pass"
                else:
                    status = "Fail"
                provd.append(status)

                spec_test.append(provd)

        values[base_business].append(prod_test)
        values[base_business].append(spec_test)

    return values

test_dict = {"breakdown_test": breakdownTest, "production_test": productionTest, "count_test": countTest,
             "procedure_test": procedureTest, "lob": businessTest,}

def automationTest(driver, date_from, date_to, optional_test, test_code):
    # Calendar Date Range
    calendarDateRange(driver, date_from, date_to)
    results = {}
    # Update Button
    update_btn = WebDriverWait(driver, 120).until(
        EC.visibility_of_element_located((By.XPATH, f"{GlobalXpath.update_btn}")))
    update_btn.click()

    # Testing
    default_test = ["breakdown_test", "production_test", "count_test"]
    default_test.extend(optional_test)

    for test in default_test:
        results[test] = []
        results[test].append(test_dict[test](driver))

    storeValueTest(results, test_code, default_test)

    return default_test

def storeValueTest(results, currtest_code, default_test):
    
    # Breakdown Test
    breakdown_result = DashboardBreakdownTest(user_id=current_user.id, test_code=currtest_code,
                       base_netprod=results['breakdown_test'][0]['net_prod'][0], bd_netprod=results['breakdown_test'][0]['net_prod'][1], status_netprod=results['breakdown_test'][0]['net_prod'][2],
                       base_grossprod=results['breakdown_test'][0]['gross_prod'][0], bd_grossprod=results['breakdown_test'][0]['gross_prod'][1], status_grossprod=results['breakdown_test'][0]['gross_prod'][2],
                       base_coll=results['breakdown_test'][0]['collection'][0], bd_coll=results['breakdown_test'][0]['collection'][1], status_coll=results['breakdown_test'][0]['collection'][2],
                       base_adjust=results['breakdown_test'][0]['adjustment'][0], bd_adjust=results['breakdown_test'][0]['adjustment'][1], status_adjust=results['breakdown_test'][0]['adjustment'][2],
                       base_npv=results['breakdown_test'][0]['newpatient_visit'][0], bd_npv=results['breakdown_test'][0]['newpatient_visit'][1], status_npv=results['breakdown_test'][0]['newpatient_visit'][2],
                       base_epv=results['breakdown_test'][0]['existingpatient_visit'][0], bd_epv=results['breakdown_test'][0]['existingpatient_visit'][1], status_epv=results['breakdown_test'][0]['existingpatient_visit'][2])
    db.session.add(breakdown_result)

    # Production Test
    production_result = DashboardProductionTest(user_id=current_user.id, test_code=currtest_code,
                                                base_netprod=results['production_test'][0]['providers_data'][1],
                                                provider_data=results['production_test'][0]['providers_data'][0], providerdata_status=results['production_test'][0]['providers_data'][2],
                                                table_total=results['production_test'][0]['table_total'][0], tabletotal_status=results['production_test'][0]['table_total'][2],
                                                payor_score=results['production_test'][0]['payor_score'][0], payorscore_status=results['production_test'][0]['payor_score'][2])

    db.session.add(production_result)

    # Service Count Test
    result = results['count_test'][0]
    for indexc in result:
        value = result[indexc]
        count_result = DashboardServiceCountTest(user_id=current_user.id, test_code=currtest_code,
                                                 provider_name=value[0][1],
                                                 proced_code=value[0][0], count_data=value[1][0],
                                                 bd_data=value[1][1], count_status=value[1][2])
        db.session.add(count_result)

    # Service Count Test
    if 'procedure_test' in default_test:
        result = results['procedure_test'][0]
        for indexp in result:
            value = result[indexp]
            proced_result = DashboardServiceProcedureTest(user_id=current_user.id, test_code=currtest_code,
                                                     proced_code=value[0][0], provider_type=value[0][1],
                                                     unsearch_result=value[1][0], proced_status=value[1][1])
            db.session.add(proced_result)

    # LOB Test
    if 'lob' in default_test:
        result = results['lob'][0]
        for line_bussiness in result:
            production_value = result[line_bussiness]
            print(f"Production---{line_bussiness} {production_value[0][0]} {production_value[0][1]} {production_value[0][2]} {production_value[0][3]}")
            lob_production = DashboardLOBProductionTest(user_id=current_user.id, test_code=currtest_code,
                                                        line_bussiness=line_bussiness, netprod_base=production_value[0][0],
                                                        providers_data=production_value[0][1], table_total=production_value[0][2],
                                                        production_status=production_value[0][3])
            db.session.add(lob_production)
            db.session.commit()

            production_id = DashboardLOBProductionTest.query.filter_by(test_code=currtest_code).filter_by(line_bussiness=line_bussiness).with_entities(DashboardLOBProductionTest.id).first()
            lob_values = result[line_bussiness][1]
            for value in lob_values:
                if value:
                   print(f"LOB---{value[0]} {value[1]} {value[2]}")
                   lob_speciality = DashboardLOBSpecialityTest(production_id=production_id[0], providers_name=value[0],
                                                               providers_speciality=value[1], speciality_status=value[2])
                   db.session.add(lob_speciality)

            print("")

    db.session.commit()
    print("DONE STORING DATA")

