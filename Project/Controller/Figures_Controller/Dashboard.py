import time
import datetime
from selenium.webdriver.common.by import By
from sqlalchemy import null
from Project.Controller.Figures_Controller.Figures_xpath import DashboardXpath
from Project.Controller.Global_Controller.Range_date_picker import DateFilter
from Project.Controller.Global_Controller.Global_xpath import DatePicker
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Project.models import FiguresMatching
from Project import db

class Dashboard:
    
    def main(driver, metrics, client_url, test_type, test_month, test_day, test_code): 
        print('Dashboard Data -------------------------------------------------------------------------')
        driver.get(client_url+'/solo/results')
        #driver.implicitly_wait(1000000)
        
        wait = WebDriverWait(driver, 60)
        element = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/main/div[1]/div/div/div/div[4]/button')))
        
        net_prod = 'N/A'
        gross_prod = 'N/A'
        collection = 'N/A'
        adj = 'N/A'
        npt = 'N/A'
        pts = 'N/A'
        
        if test_type == 'daily':
            DateFilter.rangePicker(driver, test_day, test_day)
        if test_type == 'monthly':
            end_test_month = datetime.datetime.strptime(test_month,'%Y-%m')
            start_date = test_month+'-1'
            end_date = test_month+'-'+Dashboard.end_day(end_test_month.month)
            DateFilter.rangePicker(driver, start_date, end_date)
        
        driver.find_element(By.XPATH, DatePicker.update_button).click()
        
        for metric in metrics:
            if metric == "net_prod":
                net_prod = Dashboard.getValue(driver, 'Net Production')
                #net_prod = Dashboard.netProd(driver)
                print(net_prod)
                
            if metric == "gross_prod":
                gross_prod = Dashboard.getValue(driver, 'Gross Production')
                #gross_prod = Dashboard.grossProd(driver)
                print(gross_prod)
                
            if metric == "collection":
                collection = Dashboard.getValue(driver, 'Collection')
                #collection = Dashboard.collection(driver)
                print(collection)
                
            if metric == "adj":
                adj = Dashboard.getValue(driver, 'Adjustment')
                #adj = Dashboard.adjustment(driver)
                print(adj)
                
            if metric == "npt":
                npt = Dashboard.npt(driver)
                print(npt)
                
            if metric == "pts":
                pts = Dashboard.pts(driver)
                print(pts)
                
        dashboard = FiguresMatching.query.filter_by(test_code=test_code).first()
        dashboard.dash_netProd = net_prod
        dashboard.dash_grossProd  = gross_prod
        dashboard.dash_collection = collection  
        dashboard.dash_adjusment = adj 
        dashboard.dash_npt = npt
        dashboard.dash_pts = pts
        db.session.commit()
    
    def getValue(driver, metric_name):
        value = 'N/A'
        done = 'false'
        rows = driver.find_elements(By.XPATH, DashboardXpath.metric_counter)
        rows = len(rows)

        for row in range(rows + 1):
            if row > 0:
                metric_row = driver.find_element(By.XPATH, DashboardXpath.metric_name(row)).text
                #print(metric_row)
                if metric_row == metric_name:
                    value = driver.find_element(By.XPATH, DashboardXpath.metric_value(row)).text
                    done = 'true'
            if done == 'true':
                break
        return value
    

    def netProd(driver):
        net_prod = driver.find_element(By.XPATH, DashboardXpath.net_prod).text
        return net_prod
    
    def grossProd(driver):
        gross_prod = driver.find_element(By.XPATH, DashboardXpath.gross_prod).text
        return gross_prod
    
    def collection(driver):
        collection = driver.find_element(By.XPATH, DashboardXpath.collection).text
        return collection
    
    def adjustment(driver):
        adj = driver.find_element(By.XPATH, DashboardXpath.adj).text
        return adj
    
    def npt(driver):
        npt = driver.find_element(By.XPATH, DashboardXpath.npt).text
        return npt
    
    def pts(driver):
        pts = driver.find_element(By.XPATH, DashboardXpath.pts).text
        return pts
    
    def end_day(month):
        end_date = 'null'
        
        if month == 1:
            end_date = '31'
        if month == 2:
            end_date = '28'
        if month == 3:
            end_date = '31'
        if month == 4:
            end_date = '30'
        if month == 5:
            end_date = '31'
        if month == 6:
            end_date = '30'
        if month == 7:
            end_date = '31'
        if month == 8:
            end_date = '31'
        if month == 8:
            end_date = '31'
        if month == 9:
            end_date = '30'
        if month == 10:
            end_date = '31'
        if month == 11:
            end_date = '30'
        if month == 12:
            end_date = '31'
        return end_date
    
    
        

        
