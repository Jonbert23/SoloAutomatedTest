import time
import datetime
from selenium.webdriver.common.by import By
from Project.Controller.Figures_Controller.Figures_xpath import EodXpath
from Project.Controller.Global_Controller.Single_date_picker import SinglePicker

class Eod:
    
    def main(driver, metrics, client_url, test_type, test_month, test_day):
        print('EOD Data -------------------------------------------------------------------------')
        driver.get(client_url+'/end-of-day')
        driver.implicitly_wait(1000000)
        net_prod = 'null'
        gross_prod = 'null'
        collection = 'null'
        adj = 'null'
        npt = 'null'
        pts = 'null'
        
        loader = driver.find_element(By.XPATH, '/html/body/div[1]/main/div[2]/div[3]/div[1]/div/form/div/div[2]/div[2]/div[2]/input').get_attribute('value')
        
        if test_type == 'daily':
            SinglePicker.EOD_DatePicker(driver, test_day)
        if test_type == 'monthly':
            end_test_month = datetime.datetime.strptime(test_month,'%Y-%m')
            end_date = test_month+'-'+Eod.end_day(end_test_month.month)
            SinglePicker.EOD_DatePicker(driver, end_date)
            
        driver.find_element(By.XPATH, EodXpath.update_btn).click()

        for metric in metrics:
            if metric == "net_prod":
                if test_type == 'daily':
                    net_prod = Eod.getDailyValue(driver, 'Daily Net Production')
                    print(net_prod)
                if test_type == 'monthly':
                    net_prod = Eod.netProd(driver)
                    print(net_prod)
                
            if metric == "gross_prod":
                if test_type == 'daily':
                    gross_prod = Eod.getDailyValue(driver, 'Daily Gross Production')
                    print(gross_prod)
                if test_type == 'monthly':    
                    gross_prod = Eod.grossProd(driver)
                    print(gross_prod)
                    
            if metric == "collection":
                if test_type == 'daily':
                    collection = Eod.getDailyValue(driver, 'Daily Collection')
                    print(collection)
                if test_type == 'monthly':
                    collection = Eod.collection(driver)
                    print(collection)
                
            if metric == "adj":
                if test_type == 'daily':
                    adj = Eod.getDailyValue(driver, 'Adjustments')
                    print(adj)
                if test_type == 'monthly':
                    adj = Eod.adjustment(driver)
                    print(adj)
                
            if metric == "npt":
                if test_type == 'daily':
                    npt = Eod.getDailyValue(driver, 'New Patients')
                    print(npt)
                if test_type == 'monthly':
                    npt = Eod.npt(driver)
                    print(npt)
                
            if metric == "pts":
                if test_type == 'daily':
                    pts = Eod.getDailyValue(driver, 'Total Pts Seen')
                    print(pts)
                if test_type == 'monthly':
                    pts = Eod.pts(driver)
                    print(pts)
                
        data = []
        data.append(gross_prod)
        data.append(net_prod)
        data.append(collection)
        data.append(adj)
        data.append(npt)
        data.append(pts)
        return data

    def netProd(driver):
        net_prod = driver.find_element(By.XPATH, EodXpath.net_prod).get_attribute('value')
        return net_prod
    
    def grossProd(driver):
        gross_prod = driver.find_element(By.XPATH, EodXpath.gross_prod).get_attribute('value')
        return gross_prod
    
    def collection(driver):
        collection = driver.find_element(By.XPATH, EodXpath.collection).get_attribute('value')
        return collection
    
    def adjustment(driver):
        adj = driver.find_element(By.XPATH, EodXpath.adj).get_attribute('value')
        return adj
    
    def npt(driver):
        npt = driver.find_element(By.XPATH, EodXpath.npt).get_attribute('value')
        return npt
    
    def pts(driver):
        pts = driver.find_element(By.XPATH, EodXpath.pts).get_attribute('value')
        return pts
    
    def getDailyValue(driver, metric_name):
        value = 'null'
        done = 'false'
        rows = driver.find_elements(By.XPATH, EodXpath.metric_counter)
        rows = len(rows)

        for row in range(rows + 1):
            if row > 0:
                metric_row = driver.find_element(By.XPATH, EodXpath.metric_name(row)).text
                #print(metric_row)
                if metric_row == metric_name:
                    value = driver.find_element(By.XPATH, EodXpath.metric_value(row)).get_attribute('value')
                    done = 'true'
            if done == 'true':
                break
        return value
        
    
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
    
    
        

        
