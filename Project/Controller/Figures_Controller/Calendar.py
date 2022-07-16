import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from Project.Controller.Figures_Controller.Figures_xpath import CalendarXpath
from Project.Controller.Global_Controller.Calendar_monthDatePicker import MonthPicker

from Project.models import FiguresMatching
from Project import db


class Calendar:
    
    def main(driver, metrics, client_url , month, param, test_code):
        driver.get(client_url+'/calendar/appointments/month')
        print('Calendar Data--------------------------------------------------------------------------')
        driver.implicitly_wait(1000000)
        
        net_prod = 'N/A'
        gross_prod = 'N/A'
        collection = 'N/A'
        adj = 'N/A'
        npt = 'N/A'
        pts = 'N/A'
        
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

        cal = FiguresMatching.query.filter_by(test_code=test_code).first()
        cal.cal_netProd = net_prod
        cal.cal_grossProd  = gross_prod
        cal.cal_npt  = npt
        db.session.commit()
        
    def prod(driver):
        prod = driver.find_element(By.XPATH, CalendarXpath.prod).text
        return prod
    
    def npt(driver):
        npt = driver.find_element(By.XPATH, CalendarXpath.npt).text
        return npt
        