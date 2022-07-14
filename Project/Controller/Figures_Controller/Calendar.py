import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from Project.Controller.Figures_Controller.Figures_xpath import CalendarXpath
from Project.Controller.Global_Controller.Calendar_monthDatePicker import MonthPicker


class Calendar:
    
    def main(driver, metrics, client_url , month, param):
        driver.get(client_url+'/calendar/appointments/month')
        print('Calendar Data--------------------------------------------------------------------------')
        driver.implicitly_wait(1000000)
        net_prod = 'null'
        gross_prod = 'null'
        collection = 'null'
        adj = 'null'
        npt = 'null'
        pts = 'null'
        
        wait = WebDriverWait(driver, 60)
        element = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/main/div[1]/div/div/div/div[2]/button')))
        
        #Finding Test month
        MonthPicker.Cal_monthPicker(driver, month)
        time.sleep(3)
        
        for metric in metrics:
            
            if metric == 'net_prod':
                if param == 'net_true':
                    net_prod = Calendar.prod(driver)
                print('Net production: '+net_prod)
            
           
            if metric == "gross_prod":
                if param == 'net_false':
                    gross_prod = Calendar.prod(driver)
                print('Gross Production: '+gross_prod)
                
            if metric == "collection":
                print(collection)
                
            if metric == "adj":
                print(adj)
            
            if metric == "npt":
                npt = Calendar.npt(driver)
                print(npt)
            
            if metric == "pts":
                print(pts)
                
        data = []
        data.append(gross_prod)
        data.append(net_prod)
        data.append(collection)
        data.append(adj)
        data.append(npt)
        data.append(pts)
        return data
    
    def prod(driver):
        prod = driver.find_element(By.XPATH, CalendarXpath.prod).text
        return prod
    
    def npt(driver):
        npt = driver.find_element(By.XPATH, CalendarXpath.npt).text
        return npt
        