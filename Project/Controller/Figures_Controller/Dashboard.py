from flask import Blueprint, render_template, url_for, request, redirect
from flask_login import login_required, current_user
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By

from Project.Controller.Figures_Controller.Figures_xpath import DashboardXpath

class Dashboard:
    
    def main(driver, metrics):
        
        driver.implicitly_wait(1000000)
        net_prod = 'null'
        gross_prod = 'null'
        collection = 'null'
        adj = 'null'
        npt = 'null'
        pts = 'null'
        
        for metric in metrics:
            if metric == "net_prod":
                net_prod = Dashboard.netProd(driver)
                print(net_prod)
                
            if metric == "gross_prod":
                gross_prod = Dashboard.grossProd(driver)
                print(gross_prod)
                
            if metric == "collection":
                collection = Dashboard.collection(driver)
                print(collection)
                
            if metric == "adj":
                adj = Dashboard.adjustment(driver)
                print(adj)
                
            if metric == "npt":
                npt = Dashboard.npt(driver)
                print(npt)
                
            if metric == "pts":
                pts = Dashboard.pts(driver)
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
        net_prod = driver.find_element(By.XPATH, DashboardXpath.net_prod).text
        return net_prod
    
    def grossProd(driver):
        gross_prod = driver.find_element(By.XPATH, DashboardXpath.gross_prod).text
        return gross_prod
    
    def collection(driver):
        collection = driver.find_element(By.XPATH, DashboardXpath.collection).text
        return collection
    
    def adjustment(driver):
        adj = driver.find_element(By.XPATH, DashboardXpath.adj).text
        return adj
    
    def npt(driver):
        npt = driver.find_element(By.XPATH, DashboardXpath.npt).text
        return npt
    
    def pts(driver):
        pts = driver.find_element(By.XPATH, DashboardXpath.pts).text
        return pts
    
    
        

        
