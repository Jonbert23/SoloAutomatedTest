from flask import Blueprint, render_template, url_for, request, redirect, flash
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

class GlobalLogin:
    
    def Login(driver, client_url, client_username, client_password):
        driver.implicitly_wait(5)
        
        driver.get(client_url)
        
        logo = driver.find_elements(By.XPATH,LoginXpath.logo)
        logo = len(logo)
        
        if logo == 1:
            print('Entered Correct URL')
            driver.find_element(By.XPATH, LoginXpath.username).send_keys(client_username)
            driver.find_element(By.XPATH, LoginXpath.password).send_keys(client_password)
            driver.find_element(By.XPATH, LoginXpath.login_btn).click()
            
            welcome = driver.find_elements(By.XPATH,LoginXpath.welcome)
            welcome = len(welcome)
            module_title = driver.find_elements(By.XPATH,LoginXpath.module_title)
            module_title = len(module_title)
            
            if welcome == 1 or module_title == 1:
                print('Successfully Login')
            else:
                driver.quit()
                flash('Incorrect Login credentials', 'error')
                return redirect('/')
            
        else:
            driver.quit()
            flash('Url does not exist in Jarvis. Kindly check your internet connection or VPN', 'error')
            return redirect('/')
        
class LoginXpath:
    username = '/html/body/div/div/div/div/div[1]/div/form/div[1]/div/input'
    password = '/html/body/div/div/div/div/div[1]/div/form/div[2]/div[2]/input'
    login_btn = '/html/body/div/div/div/div/div[1]/div/form/button'
    logo = '/html/body/div/div/div/div/div[1]/div/div/a/img'
    welcome = '/html/body/div[1]/main/div[1]/div[1]/h1'
    module_title = '/html/body/div[1]/main/div[1]/div/h2'