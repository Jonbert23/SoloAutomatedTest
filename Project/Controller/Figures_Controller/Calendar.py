import time
from selenium.webdriver.common.by import By
from Project.Controller.Figures_Controller.Figures_xpath import CalendarXpath

class Calendar:
    
    def main(driver, metrics):
        print('Calendar Data--------------------------------------------------------------------------')
        driver.implicitly_wait(1000000)
        net_prod = 'null'
        gross_prod = 'null'
        collection = 'null'
        adj = 'null'
        npt = 'null'
        pts = 'null'
        driver.find_element(By.XPATH, CalendarXpath.month_button).click()
        time.sleep(3)
        for metric in metrics:
            if metric == 'net_prod':
                net_prod = Calendar.prod(driver)
                print(net_prod)
            
            if metric == "gross_prod":
                gross_prod = Calendar.prod(driver)
                print(gross_prod)
                
            if metric == "collection":
                print(collection)
                
            if metric == "adj":
                print(adj)
            
            if metric == "npt":
                npt = Calendar.npt(driver)
                print(npt)
            
            if metric == "pts":
                print(pts)
    
    def prod(driver):
        prod = driver.find_element(By.XPATH, CalendarXpath.prod).text
        return prod
    
    def npt(driver):
        npt = driver.find_element(By.XPATH, CalendarXpath.npt).text
        return npt
        