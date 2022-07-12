import time
from selenium.webdriver.common.by import By
from Project.Controller.Figures_Controller.Figures_xpath import EodXpath
from Project.Controller.Global_Controller.Single_date_picker import SinglePicker

class Eod:
    
    def main(driver, metrics, test_day):
        print('EOD Data -------------------------------------------------------------------------')
        driver.implicitly_wait(1000000)
        net_prod = 'null'
        gross_prod = 'null'
        collection = 'null'
        adj = 'null'
        npt = 'null'
        pts = 'null'
        
        SinglePicker.EOD_DatePicker(driver, test_day)

        for metric in metrics:
            if metric == "net_prod":
                net_prod = Eod.netProd(driver)
                print(net_prod)
                
            if metric == "gross_prod":
                gross_prod = Eod.grossProd(driver)
                print(gross_prod)
                
            if metric == "collection":
                collection = Eod.collection(driver)
                print(collection)
                
            if metric == "adj":
                adj = Eod.adjustment(driver)
                print(adj)
                
            if metric == "npt":
                npt = Eod.npt(driver)
                print(npt)
                
            if metric == "pts":
                pts = Eod.pts(driver)
                print(pts)
                
        data = {
            'GrossProd': gross_prod,
            'NetProd': net_prod,
            'Collection': collection,
            'Adjustment': adj,
            'Npt': npt,
            'Pts': pts
        }
        print(data)
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
    
    
        

        
