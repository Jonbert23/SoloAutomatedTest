#Importing Flask Dependecies
from flask import Blueprint, render_template, url_for, request, redirect,flash
from flask_login import login_required, current_user
import time
import datetime
import uuid
#Importing Selenium Dependecies
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
#Importing  File Classes 
from Project.Controller.Global_Controller.Login import GlobalLogin
from Project.Controller.Figures_Controller.Dashboard import Dashboard
from Project.Controller.Figures_Controller.Eod import Eod
from Project.Controller.Figures_Controller.Calendar import Calendar
from Project.Controller.Figures_Controller.Mh import MorningHuddle
from Project.Controller.Global_Controller.Single_date_picker import SinglePicker
from Project.Controller.Global_Controller.Range_date_picker import DateFilter
from Project.models import FiguresMatching
from Project import db



fm = Blueprint('fm', __name__)

@fm.route("/figures-matching",methods=['GET', 'POST'])
def figuresMatching():
    if request.method == 'POST':
        #Request-------------------------------------------------------------------------------------
        modules = request.form.getlist('Module[]')
        metrics = request.form.getlist('Metric[]')
        client_url = request.form['client_url']
        client_username = request.form['client_username']
        client_password = request.form['client_password']
        test_type = request.form['test_type'] 
        test_month = request.form['test_month']
        test_day = request.form['test_day']
        param = request.form['param']
        
        test_date = ''
        if test_type == 'daily':
            test_date = test_day
        else:
            test_date = test_month
        
        test_code = uuid.uuid4().hex
        new_figures_matching = FiguresMatching(
            user_id = current_user.id,
            test_code = test_code,
            client_url = client_url,
            test_type  = test_type,
            query_param  = param,
            test_date  = test_date
        )
        db.session.add(new_figures_matching)
        db.session.commit()
        
        #Declaring Selenium driver--------------------------------------------------------------------
        options = Options()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
        
        #Calling Login Global Test -----------------------------------------------------------------
        GlobalLogin.Login(driver, client_url, client_username, client_password)
        
        for module in modules:
            if module == "eod":
                eod_data = Eod.main(driver, metrics, client_url, test_type, test_month, test_day, test_code)
                
            if module == "dashboard":
                dash_data = Dashboard.main(driver, metrics, client_url, test_type, test_month, test_day, test_code)
                
            if module == "calendar":
                calendar_data = Calendar.main(driver, metrics, client_url , test_month, param, test_code)
                
            if module == 'morning_huddle':
                mh_data = MorningHuddle.main(driver, metrics, client_url, test_day, param, test_code)
        
        driver.quit()
        flash('Your Test Code: '+test_code, 'info')
    
    
    data = FiguresMatching.query.order_by(FiguresMatching.id.desc()).first()
    fm_test = FiguresMatching.query.all()
    has_data = 'No'
    
    if data:
        has_data = 'Yes'
        net_prod_data = [data.dash_netProd, data.cal_netProd, data.eod_netProd, data.mh_netProd]
        net_prod_result = Result.result(net_prod_data)
        
        gross_prod_data = [data.dash_grossProd, data.cal_grossProd, data.eod_grossProd, data.mh_grossProd ]
        gross_prod_result = Result.result(gross_prod_data)
        
        collection_data = [data.dash_collection, data.eod_collection, data.mh_collection]
        collection_result = Result.result(collection_data)
        
        adjustment_data = [data.dash_adjusment, data.eod_adjusment]
        adjustment_result = Result.result(adjustment_data)
        
        pts_data = [data.dash_pts, data.eod_pts]
        pts_result = Result.result(pts_data)
        
        npt_data = [data.dash_npt, data.cal_npt, data.eod_npt, data.mh_npt]
        npt_result = Result.result(npt_data)
    
    
        return render_template('Figures_Template/Figures_index.html', 
                            data = data, 
                            fm_test = fm_test,
                            net_prod_result = net_prod_result,
                            gross_prod_result = gross_prod_result,
                            collection_result = collection_result,
                            adjustment_result = adjustment_result,
                            pts_result = pts_result,
                            npt_result = npt_result,
                            has_data = has_data)
    else:
        return render_template('Figures_Template/Figures_index.html',has_data = has_data)
    
    


@fm.route("/figures-matching/search",methods=['GET', 'POST'])
def figures_matching_search():
    
    test_code = ''
    if request.method == 'POST':
        #Request-------------------------------------------------------------------------------------
        test_code = request.form['test_code']
        print("My Test Code: "+test_code)
        
    # fm_test = FiguresMatching.query.all()
    
    # for fm_tests in fm_test:
    #     print(fm_tests.test_code)
        
    data = FiguresMatching.query.filter_by(test_code=test_code).first()
    has_data = 'No'
    
    if data:
        has_data = 'Yes'
        net_prod_data = [data.dash_netProd, data.cal_netProd, data.eod_netProd, data.mh_netProd]
        net_prod_result = Result.result(net_prod_data)
        
        gross_prod_data = [data.dash_grossProd, data.cal_grossProd, data.eod_grossProd, data.mh_grossProd ]
        gross_prod_result = Result.result(gross_prod_data)
        
        collection_data = [data.dash_collection, data.eod_collection, data.mh_collection]
        collection_result = Result.result(collection_data)
        
        adjustment_data = [data.dash_adjusment, data.eod_adjusment]
        adjustment_result = Result.result(adjustment_data)
        
        pts_data = [data.dash_pts, data.eod_pts]
        pts_result = Result.result(pts_data)
        
        npt_data = [data.dash_npt, data.cal_npt, data.eod_npt, data.mh_npt]
        npt_result = Result.result(npt_data) 
    
        return render_template('Figures_Template/Figures_index.html', 
                            data = data, 
                            net_prod_result = net_prod_result,
                            gross_prod_result = gross_prod_result,
                            collection_result = collection_result,
                            adjustment_result = adjustment_result,
                            pts_result = pts_result,
                            npt_result = npt_result,
                            has_data = has_data)
    else:
        #return render_template('Figures_Template/Figures_index.html',has_data = has_data)
        flash('Search Test Code Not Exist', 'info')
        return redirect('/figures-matching')
    
    
@fm.route("/figures-matching/all_test")
def all_test_codes():
    fm_test = FiguresMatching.query.all()
    return render_template('Figures_Template/Modal/Test_codes_modal.html', fm_test=fm_test)


class Result:

    def result(data_arary):
        done = 'false'
        test_result = 'N/A'       
        for i in range(len(data_arary)):
            for j in range(len(data_arary)):
                if data_arary[i] != 'N/A' and data_arary[j] != 'N/A':
                    data_arary[i] = data_arary[i].replace("$","").replace(",","").replace(" ","").replace("(","-").replace(")","")
                    data_arary[j] = data_arary[j].replace("$","").replace(",","").replace(" ","").replace("(","-").replace(")","")
                    
                    if data_arary[i] ==  data_arary[j]:
                        test_result = 'Pass'
                    else:
                        test_result = 'Fail'
                        done = 'true'
                if done == 'true':
                    break
            if done == 'true':
                break
        return test_result