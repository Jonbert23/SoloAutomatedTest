import time
import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from Project.Controller.Global_Controller.Global_xpath import SinglePickerXpath

class SinglePicker:
    
    def MH_DatePicker(driver, date):
        date = datetime.datetime.strptime(date,'%Y-%m-%d')
        driver.implicitly_wait(1000000)
        wait = WebDriverWait(driver, 60)
        element = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/main/div[1]/div/div/div/div[4]/button')))
        time.sleep(3)
        
        stoper = value = driver.find_element(By.XPATH, '/html/body/div[1]/main/div[2]/div[1]/div[1]/div/div/div[1]/input').get_attribute('value')
        
        driver.find_element(By.XPATH, SinglePickerXpath.picker).click()
        SinglePicker.MH_monthYearPicker(driver, date.month, date.year)
        SinglePicker.dayPicker(driver, date.day)
    
    def EOD_DatePicker(driver, date):
        date = datetime.datetime.strptime(date,'%Y-%m-%d')
        driver.implicitly_wait(1000000)
        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.visibility_of_element_located((By.XPATH, SinglePickerXpath.eod_loader)))
        time.sleep(3)
        
        driver.find_element(By.XPATH, SinglePickerXpath.picker).click()
        SinglePicker.EOD_monthYearPicker(driver, date.month, date.year)
        SinglePicker.dayPicker(driver, date.day)
        
        
    def EOD_monthYearPicker(driver, month, year):
        done = 'false'
        month_year = driver.find_element(By.XPATH, SinglePickerXpath.month_year_xpath).text
        for i in range(5000):
            scrip_year = driver.find_element(By.XPATH, SinglePickerXpath.month_year_xpath).text
            cal_year = scrip_year[4:10]

            if int(year) < int(cal_year):
                arrow_back = driver.find_element(By.XPATH, SinglePickerXpath.back_arrow)
                arrow_back.click()
                #print('(year) < (cal_year):' +str(year)+' '+str(cal_year))
                
            if int(year) > int(cal_year):
                arrow_next = driver.find_element(By.XPATH,SinglePickerXpath.next_arrow)
                arrow_next.click()
                #print('(year) > (cal_year):' +str(year)+' '+str(cal_year))
                
            if int(year) == int(cal_year):
                #print('(year) < (cal_year):' +str(year)+' '+str(cal_year))
                for i in range(13):
                    scrip_month = driver.find_element(By.XPATH, SinglePickerXpath.month_year_xpath).text
                    cal_month = SinglePicker.monthConverter(scrip_month[0:3])
                    if int(month) < int(cal_month):
                        arrow_back = driver.find_element(By.XPATH, SinglePickerXpath.back_arrow)
                        arrow_back.click()
                        #print('(month) < (cal_month):' +str(month)+' '+str(cal_month))
                        
                    if int(month) > int(cal_month):
                        arrow_next = driver.find_element(By.XPATH,SinglePickerXpath.next_arrow)
                        arrow_next.click()
                        #print('(month) > (cal_month):' +str(month)+' '+str(cal_month))
                        
                    if int(month) == int(cal_month):
                        #print('(month) == (cal_month):' +str(month)+' '+str(cal_month))
                        done = 'true'
                    
                    if done == 'true':
                        break 
                
            if done == 'true':
                break 
            
    def MH_monthYearPicker(driver, month, year):
        done = 'false'
        
        for i in range(5000):
            cal_year = driver.find_element(By.XPATH, SinglePickerXpath.year).get_attribute('value')
            if int(year) < int(cal_year):
                arrow_back = driver.find_element(By.XPATH, SinglePickerXpath.back_arrow)
                arrow_back.click()
                
            if int(year) > int(cal_year):
                arrow_next = driver.find_element(By.XPATH,SinglePickerXpath.next_arrow)
                arrow_next.click()
                
            if int(year) == int(cal_year):
                for i in range(13):
                    cal_month = driver.find_element(By.XPATH, SinglePickerXpath.month).get_attribute('value')
                    if int(month) < int(cal_month):
                        arrow_back = driver.find_element(By.XPATH, SinglePickerXpath.back_arrow)
                        arrow_back.click()
                        
                    if int(month) > int(cal_month):
                        arrow_next = driver.find_element(By.XPATH,SinglePickerXpath.next_arrow)
                        arrow_next.click()
                        
                    if int(month) == int(cal_month):
                        done = 'true'
                    
                    if done == 'true':
                        break 
                
            if done == 'true':
                break
            
    def dayPicker(driver, day):
        see_start_date = 'false'
        have_selected = 'false'
        
        for row in range(8):
            for column in range(8):
                if row > 1 and column > 0:
                    date = driver.find_element(By.XPATH, SinglePickerXpath.single_date_xpath(row, column)).text

                    if date == '1':
                        see_start_date = 'true'
                    
                    if see_start_date == 'true':
                        if str(day) == date:
                            driver.find_element(By.XPATH, SinglePickerXpath.single_date_xpath(row, column)).click()
                            have_selected = 'true' 
                
                if have_selected == 'true':
                    break
            
            if have_selected == 'true':
                break
     
    def monthConverter(month):
        month_value = 0
        if month == 'Jan':
            month_value = 1
        if month == 'Feb':
            month_value = 2
        if month == 'Mar':
            month_value = 3
        if month == 'Apr':
            month_value = 4
        if month == 'May':
            month_value = 5
        if month == 'Jun':
            month_value = 6
        if month == 'Jul':
            month_value = 7
        if month == 'Aug':
            month_value = 8
        if month == 'Sep':
            month_value = 9
        if month == 'Oct':
            month_value = 10
        if month == 'Nov':
            month_value = 11
        if month == 'Dec':
            month_value = 12
            
        return month_value