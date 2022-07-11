import time
import datetime
from selenium.webdriver.common.by import By
from Project.Controller.Global_Controller.Global_xpath import SinglePickerXpath

class SingePicker:
    
    def singleDatePicker(driver):
        driver.get('https://solo.next.jarvisanalytics.com/end-of-day')
        driver.implicitly_wait(1000000)
        time.sleep(5)
        
        driver.find_element(By.XPATH, SinglePickerXpath.picker).click()
        SingePicker.monthYearPicker(driver, 7, 2017)
        SingePicker.dayPicker(driver, 15)
        
        
        time.sleep(10)
        
    def monthYearPicker(driver, month, year):
        done = 'false'
        
        for i in range(5000):
            scrip_year = driver.find_element(By.XPATH, SinglePickerXpath.month_year_xpath).text
            cal_year = scrip_year[4:10]
            
            if int(year) < int(cal_year):
                arrow_back = driver.find_element(By.XPATH, SinglePickerXpath.back_arrow)
                arrow_back.click()
                
            if int(year) > int(cal_year):
                arrow_next = driver.find_element(By.XPATH,SinglePickerXpath.next_arrow)
                arrow_next.click()
                
            if int(year) == int(cal_year):
                for i in range(13):
                    scrip_month = driver.find_element(By.XPATH, SinglePickerXpath.month_year_xpath).text
                    cal_month = SingePicker.monthConverter(scrip_month[0:3])
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
            month_value == 4
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