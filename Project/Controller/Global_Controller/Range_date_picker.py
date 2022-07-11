import time
import datetime
from selenium.webdriver.common.by import By
from Project.Controller.Global_Controller.Global_xpath import DatePicker

class DateFilter:
    
    def rangePicker(driver, start_date, end_date):
        time.sleep(3)
        driver.implicitly_wait(1000000)
        
        start_date = datetime.datetime.strptime(start_date,'%Y-%m-%d')
        end_date = datetime.datetime.strptime(end_date,'%Y-%m-%d')
        
        driver.find_element(By.XPATH, DatePicker.date_filter_button).click()
        
        DateFilter.startYearMonth(driver, start_date.month, start_date.year )
        driver.find_element(By.XPATH, DateFilter.start_day(driver, start_date.day)).click()
        
        DateFilter.endYearMonth(driver, end_date.month, end_date.year)
        driver.find_element(By.XPATH, DateFilter.end_day(driver, end_date.day)).click()
        
        # driver.find_element(By.XPATH, DatePicker.update_button).click()
        
        
    def start_day(driver, start_date):
        see_start_date = 'false'
        have_selected = 'false'
        start_date_xpath = 'null'
        
        for row in range(8):
            for column in range(8):
                if row > 1 and column > 0:
                    date = driver.find_element(By.XPATH, DatePicker.start_date_xpath(row, column)).text

                    if date == '1':
                        see_start_date = 'true'
                    
                    if see_start_date == 'true':
                        if str(start_date) == date:
                            start_date_xpath = DatePicker.start_date_xpath(row, column)
                            have_selected = 'true' 
            
            if have_selected == 'true':
                break
        return start_date_xpath
    
    def end_day(driver, end_date):
        see_start_date = 'false'
        have_selected = 'false'
        end_date_xpath = 'null'
        
        for row in range(8):
            for column in range(8):
                if row > 1 and column > 0:
                    date = driver.find_element(By.XPATH, DatePicker.end_date_xpath(row, column)).text

                    if date == '1':
                        see_start_date = 'true'
                    
                    if see_start_date == 'true':
                        if str(end_date) == date:
                            end_date_xpath = DatePicker.end_date_xpath(row, column)
                            have_selected = 'true' 
            
            if have_selected == 'true':
                break
        
        return end_date_xpath
    
    
    def startYearMonth(driver, start_month, startyear):
        done = 'false'
        
        for i in range(5000):
            year = driver.find_element(By.XPATH, DatePicker.start_year).get_attribute('value')
            if int(startyear) < int(year):
                arrow_back = driver.find_element(By.XPATH, DatePicker.start_arrow_back)
                arrow_back.click()
                
            if int(startyear) > int(year):
                arrow_next = driver.find_element(By.XPATH, DatePicker.start_arrow_next)
                arrow_next.click()
                
            if int(startyear) == int(year):
                for i in range(13):
                    month = driver.find_element(By.XPATH, DatePicker.start_month).get_attribute('value')
                    if int(start_month) < int(month):
                        arrow_back = driver.find_element(By.XPATH, DatePicker.start_arrow_back)
                        arrow_back.click()

                    
                    if int(start_month) > int(month):
                        arrow_next = driver.find_element(By.XPATH, DatePicker.start_arrow_next)
                        arrow_next.click()
                    
                    if int(start_month) == int(month): 
                        done = 'true'
                        
                    if done == 'true':
                        break
                        
            if done == 'true':
                break
            
    def endYearMonth(driver, end_month, end_year):
        done = 'false'
        
        for i in range(5000):
            year = driver.find_element(By.XPATH, DatePicker.end_year).get_attribute('value')
            if int(end_year) < int(year):
                arrow_back = driver.find_element(By.XPATH, DatePicker.end_arrow_back)
                arrow_back.click()
                
            if int(end_year) > int(year):
                arrow_next = driver.find_element(By.XPATH, DatePicker.end_arrow_next)
                arrow_next.click()
                
            if int(end_year) == int(year):
                for i in range(13):
                    month = driver.find_element(By.XPATH, DatePicker.end_month).get_attribute('value')
                    if int(end_month) < int(month):
                        arrow_back = driver.find_element(By.XPATH, DatePicker.end_arrow_back)
                        arrow_back.click()
                    
                    if int(end_month) > int(month):
                        arrow_next = driver.find_element(By.XPATH, DatePicker.end_arrow_next)
                        arrow_next.click()
                    
                    if int(end_month) == int(month): 
                        done = 'true'
                        
                    if done == 'true':
                        break
                        
            if done == 'true':
                break 
                    
    def monthConverter(month):
        month_value = 0
        if month == 'Janunary':
            month_value = 1
        if month == 'Febuary':
            month_value = 2
        if month == 'March':
            month_value = 3
        if month == 'April':
            month_value == 4
        if month == 'May':
            month_value = 5
        if month == 'June':
            month_value = 6
        if month == 'July':
            month_value = 7
        if month == 'August':
            month_value = 8
        if month == 'September':
            month_value = 9
        if month == 'October':
            month_value = 10
        if month == 'November':
            month_value = 11
        if month == 'December':
            month_value = 12
            
        return month_value
        
        
        
        
           
    
               
                    
                    
