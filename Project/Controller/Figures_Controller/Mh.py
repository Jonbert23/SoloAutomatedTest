import time
import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Project.Controller.Figures_Controller.Figures_xpath import MhXpath
from Project.Controller.Global_Controller.Single_date_picker import SinglePicker


class MorningHuddle:
    
    def main(driver, metrics, client_url, test_day, param):
        print('Morning Huddle Data -------------------------------------------------------------------------')
        driver.get(client_url+'/morning-huddle')
        driver.implicitly_wait(1000000)
        
        wait = WebDriverWait(driver, 60)
        loader = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/main/div[1]/div/div/div/div[4]/button')))
        
        # test_day = datetime.datetime.strptime(test_day, "%Y-%m-%d")
        # test_day = test_day + datetime.timedelta(days=1)
        # test_day = test_day.strftime("%Y-%m-%d")
        
        SinglePicker.MH_DatePicker(driver, test_day)
        update_btn = driver.find_element(By.XPATH, '/html/body/div[1]/main/div[1]/div/div/div/div[4]/button').click()
        time.sleep(5)
        scorecard = driver.find_element(By.XPATH, MhXpath.scorecard).click()
        
        net_prod = 'null'
        gross_prod = 'null'
        collection = 'null'
        adj = 'null'
        npt = 'null'
        pts = 'null'
        
        for metric in metrics:
            if metric == "net_prod":
                #net_prod = MorningHuddle.getValue(driver, "Yesterday's Production (net)")
                if param == 'net_true':
                    net_prod = driver.find_element(By.XPATH, MhXpath.prod).text
                print('Net Production: '+net_prod)
                
            if metric == "gross_prod":
                #gross_prod = MorningHuddle.getValue(driver, "Yesterday's Production (gross)")
                if param == 'net_false':
                    gross_prod = driver.find_element(By.XPATH, MhXpath.prod).text
                print('Gorss Production: '+gross_prod)
                
            if metric == "collection":
                #collection = MorningHuddle.getValue(driver, "Yesterday's Collection")
                collection = driver.find_element(By.XPATH, MhXpath.collection).text
                print(collection)
                
            if metric == "adj":
                print(adj)
                
            if metric == "npt":
                #npt = MorningHuddle.getValue(driver, "New Patients (Actual)")
                npt = driver.find_element(By.XPATH, MhXpath.npt).text
                print(npt)
                
            if metric == "pts":
                npt = driver.find_element(By.XPATH, MhXpath.pts).text
                print(pts)

        data = []
        data.append(gross_prod)
        data.append(net_prod)
        data.append(collection)
        data.append(adj)
        data.append(npt)
        data.append(pts)
        return data
                
    
    def getValue(driver, metric_name):
        value = 'null'
        done = 'false'
        rows = driver.find_elements(By.XPATH, MhXpath.metric_counter)
        rows = len(rows)

        for row in range(rows + 1):
            if row > 0:
                metric_row = driver.find_element(By.XPATH, MhXpath.metric_name(row)).text
                #print(metric_row)
                if metric_row == metric_name:
                    value = driver.find_element(By.XPATH, MhXpath.metric_value(row)).get_attribute('value')
                    done = 'true'
            if done == 'true':
                break
        return value