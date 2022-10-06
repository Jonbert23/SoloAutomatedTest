from flask import Blueprint, render_template, url_for, request, redirect,flash
from flask_login import login_required, current_user
import time
import datetime
import uuid
#Importing Selenium Dependecies
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SinglePicker:
    
    def Single_picker(driver, date):
        time.sleep(1)
        date = datetime.datetime.strptime(date,'%Y-%m-%d')
        
        SinglePicker.EOD_monthYearPicker(driver, date.month, date.year)
        SinglePicker.dayPicker(driver, date.day)
        apply_btn = driver.find_element(By.XPATH, Xpath.apply_btn).click()
        
    def EOD_monthYearPicker(driver, month, year):
        done = 'false'
        month_year = driver.find_element(By.XPATH, Xpath.month_year).text
        for i in range(5000):
            scrip_year = driver.find_element(By.XPATH, Xpath.month_year).text
            cal_year = scrip_year[4:10]
            # print('row:'+str(i)+' - '+cal_year)

            if int(year) < int(cal_year):
                arrow_back = driver.find_element(By.XPATH, Xpath.back_btn)
                arrow_back.click()
                #print('(year) < (cal_year):' +str(year)+' '+str(cal_year))
                
            if int(year) > int(cal_year):
                arrow_next = driver.find_element(By.XPATH,Xpath.next_btn)
                arrow_next.click()
                #print('(year) > (cal_year):' +str(year)+' '+str(cal_year))
                
            if int(year) == int(cal_year):
                #print('(year) < (cal_year):' +str(year)+' '+str(cal_year))
                for i in range(13):
                    scrip_month = driver.find_element(By.XPATH, Xpath.month_year).text
                    cal_month = SinglePicker.monthConverter(scrip_month[0:3])
                    if int(month) < int(cal_month):
                        arrow_back = driver.find_element(By.XPATH, Xpath.back_btn)
                        arrow_back.click()
                        #print('(month) < (cal_month):' +str(month)+' '+str(cal_month))
                        
                    if int(month) > int(cal_month):
                        arrow_next = driver.find_element(By.XPATH, Xpath.next_next)
                        arrow_next.click()
                        #print('(month) > (cal_month):' +str(month)+' '+str(cal_month))
                        
                    if int(month) == int(cal_month):
                        #print('(month) == (cal_month):' +str(month)+' '+str(cal_month))
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
                    date = driver.find_element(By.XPATH, Xpath.single_date_xpath(row, column)).text

                    if date == '1':
                        see_start_date = 'true'
                    
                    if see_start_date == 'true':
                        if str(day) == date:
                            driver.find_element(By.XPATH, Xpath.single_date_xpath(row, column)).click()
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
    
    
class Xpath:
    loader = '/html/body/div[1]/main/div[1]/div/div/div/div[2]/button'
    add_filter = '/html/body/div[1]/main/div[2]/div/div[1]/div/div/div/div/div[1]/div[1]/button'
    search = '/html/body/div[1]/main/div[2]/div/div[1]/div/div/div/div/div[2]/div[1]/input'
    find_filter = '/html/body/div[1]/main/div[2]/div/div[1]/div/div/div/div/div[2]/div[2]/ol/span/li'
    
    month_year = '/html/body/div[1]/main/div[4]/div/div/div/div[3]/div/div/div[2]/div[1]/div/div/div/table/thead/tr/th[2]'
    back_btn = '/html/body/div[1]/main/div[4]/div/div/div/div[3]/div/div/div[2]/div[1]/div/div/div/table/thead/tr/th[1]'
    next_btn = '/html/body/div[1]/main/div[4]/div/div/div/div[3]/div/div/div[2]/div[1]/div/div/div/table/thead/tr/th[3]'
    apply_btn = '/html/body/div[1]/main/div[4]/div/div/div/div[3]/div/div/div[2]/div[2]/button[2]'
    
    def single_date_xpath(row, column):
        date = '/html/body/div[1]/main/div[4]/div/div/div/div[3]/div/div/div[2]/div[1]/div/div/div/table/tbody/tr['+str(row)+']/td['+str(column)+']'
        return date
    