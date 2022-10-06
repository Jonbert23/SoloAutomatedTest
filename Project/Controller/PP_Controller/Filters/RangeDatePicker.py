import time
import datetime
from datetime import date
from selenium.webdriver.common.by import By

class DateFilter:
    
    def rangePicker(driver, start_date, end_date):
        time.sleep(1)
        date_now = date.today()
        start_date = datetime.datetime.strptime(start_date,'%Y-%m-%d')
        end_date = datetime.datetime.strptime(end_date,'%Y-%m-%d')
        
        #driver.find_element(By.XPATH, DatePicker.date_filter_button).click()
        
        if int(date_now.month) == int(end_date.month):
            DateFilter.startYearMonth(driver, start_date.month, start_date.year )
            select_start_day = driver.find_element(By.XPATH, DateFilter.start_day(driver, start_date.day)).click()
            select_end_day = driver.find_element(By.XPATH, DateFilter.start_day(driver, end_date.day)).click()
         
        else:
            DateFilter.startYearMonth(driver, start_date.month, start_date.year )
            select_start_day = driver.find_element(By.XPATH, DateFilter.start_day(driver, start_date.day)).click()
        
            DateFilter.endYearMonth(driver, end_date.month, end_date.year)
            select_end_day = driver.find_element(By.XPATH, DateFilter.end_day(driver, end_date.day)).click()
        
        apply_btn = driver.find_element(By.XPATH, DatePicker.apply_btn).click()
        
        
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
            year = driver.find_element(By.XPATH, DatePicker.start_month_year).text
            year = year[4:10]
            #print('Selectiny year: '+year[4:10])
            
            if int(startyear) < int(year):
                arrow_back = driver.find_element(By.XPATH, DatePicker.start_arrow_back)
                arrow_back.click()
                
            if int(startyear) > int(year):
                arrow_next = driver.find_element(By.XPATH, DatePicker.start_arrow_next)
                arrow_next.click()
                
            if int(startyear) == int(year):
                for i in range(13):
                    month = driver.find_element(By.XPATH, DatePicker.start_month_year).text
                    month = DateFilter.monthConverter(month[0:3])
                    #print('selecting month: '+month[0:3])
                    
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
        
        for i in range(100):
            year = driver.find_element(By.XPATH, DatePicker.end_month_year).text
            # print('Selectiny year: '+year[4:10])
            year = year[4:10]
            
            if int(end_year) < int(year):
                arrow_back = driver.find_element(By.XPATH, DatePicker.end_arrow_back)
                arrow_back.click()
                
            if int(end_year) > int(year):
                arrow_next = driver.find_element(By.XPATH, DatePicker.end_arrow_next)
                arrow_next.click()
                
            if int(end_year) == int(year):
                for i in range(13):
                    month = driver.find_element(By.XPATH, DatePicker.end_month_year).text
                    month = DateFilter.monthConverter(month[0:3])
                   
                    
                    if int(end_month) < int(month):
                        # print('selecting month <: '+str(month))
                        # print('selecting month <: '+str(end_month))
                        arrow_back = driver.find_element(By.XPATH, DatePicker.end_arrow_back)
                        arrow_back.click()
                    
                    if int(end_month) > int(month):
                        # print('selecting month >: '+str(month))
                        # print('selecting month >: '+str(end_month))
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
        
class DatePicker:
    apply_btn = '/html/body/div[1]/main/div[4]/div/div/div/div[3]/div/div/div[2]/div[2]/button[2]'
    
    start_arrow_back = '/html/body/div[1]/main/div[4]/div/div/div/div[3]/div/div/div[2]/div[1]/div[2]/div[1]/div/table/thead/tr/th[1]'
    start_arrow_next = '/html/body/div[1]/main/div[4]/div/div/div/div[3]/div/div/div[2]/div[1]/div[2]/div[1]/div/table/thead/tr/th[3]'
    start_month_year = '/html/body/div[1]/main/div[4]/div/div/div/div[3]/div/div/div[2]/div[1]/div[2]/div[1]/div/table/thead/tr/th[2]'
                  
    
    end_arrow_back = '/html/body/div[1]/main/div[4]/div/div/div/div[3]/div/div/div[2]/div[1]/div[2]/div[2]/div/table/thead/tr/th[1]'
    end_arrow_next = '/html/body/div[1]/main/div[4]/div/div/div/div[3]/div/div/div[2]/div[1]/div[2]/div[2]/div/table/thead/tr/th[3]'
    end_month_year = '/html/body/div[1]/main/div[4]/div/div/div/div[3]/div/div/div[2]/div[1]/div[2]/div[2]/div/table/thead/tr/th[2]'
    
    
    def start_date_xpath(row, column):
        date = '/html/body/div[1]/main/div[4]/div/div/div/div[3]/div/div/div[2]/div[1]/div[2]/div[1]/div/table/tbody/tr['+str(row)+']/td['+str(column)+']'
        return date
    
    def end_date_xpath(row, column):
        date = '/html/body/div[1]/main/div[4]/div/div/div/div[3]/div/div/div[2]/div[1]/div[2]/div[2]/div/table/tbody/tr['+str(row)+']/td['+str(column)+']'
        return date       
        
        
           
    
               
                    
                    
