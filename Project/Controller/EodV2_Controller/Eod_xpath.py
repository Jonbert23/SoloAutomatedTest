from selenium.webdriver.common.by import By

class EodXpath:
    
    update_btn = '/html/body/div[1]/main/div[1]/div/div/div/div[3]/button'
    metric_counter = '/html/body/div[1]/main/div[2]/div[3]/div[1]/div/form/div/div[1]/div[1]/div/div/div[1]'
    close_icon = '/html/body/div[1]/main/div[3]/div/div/div/div[1]/button'
    
    def metric_name(row):
        xpath = '/html/body/div[1]/main/div[2]/div[3]/div[1]/div/form/div/div[1]/div[1]/div/div['+str(row)+']/div[1]'
        return xpath
    
    def metric_data(row):
        xpath = '/html/body/div[1]/main/div[2]/div[3]/div[1]/div/form/div/div[1]/div[1]/div/div['+str(row)+']/div[2]/input'
        return xpath
    
    def modal(row, metric_name):
        xpath = ''
        
        if metric_name == 'Adjustments' or metric_name == 'Collection' or metric_name == 'Total adjustment' or metric_name == 'Total collection':
            xpath = '/html/body/div[1]/main/div[2]/div[3]/div[1]/div/form/div/div[1]/div[1]/div/div['+str(row)+']/div[1]/div/span'
        
        elif metric_name == 'Case acceptance (%)':
            xpath = '/html/body/div[1]/main/div[2]/div[3]/div[1]/div/form/div/div[1]/div[1]/div/div['+str(row)+']/div[1]/label/span'
            
        else:
            xpath = '/html/body/div[1]/main/div[2]/div[3]/div[1]/div/form/div/div[1]/div[1]/div/div['+str(row)+']/div[1]/label/div'
            
        return xpath
    
    
    def close_modal(driver):
        xpath = ''
        
        for row in range(10):
            cm_xpath = '/html/body/div[1]/main/div[3]/div['+str(row+1)+']/div/div/div[1]/button'
            is_displayed = driver.find_element(By.XPATH, cm_xpath).is_displayed()
            
            if is_displayed:
                xpath = cm_xpath
                break
            
        return xpath
    
    def pt_portion_col_brk(driver):
        xpath = ''
        
        for row in range(10):
            cm_xpath = '/html/body/div[1]/main/div[3]/div['+str(row+1)+']/div/div/div[2]/div[2]/div/table/tr[1]/td[2]'
            count = driver.find_elements(By.XPATH, cm_xpath)
            count = len(count)
            div_number = ''
            
            if count != 0:
                is_displayed = driver.find_element(By.XPATH, cm_xpath).is_displayed()
                
                if is_displayed:
                    xpath = cm_xpath
                    div_number = row+1
                    break
            else:
                xpath = '/html/body/div[1]/main/div[3]/div['+str(div_number)+']/div/div/div[2]/div[2]/div/table/tbody/tr/td'
            
        return xpath
    
    def adjustments_brk(driver):
        xpath = ''
        
        for row in range(10):
            cm_xpath = '/html/body/div[1]/main/div[3]/div['+str(row+1)+']/div/div/div[3]/div[1]/div/table/tfoot/tr/td[6]'
            count = driver.find_elements(By.XPATH, cm_xpath)
            count = len(count)
            
            if count != 0:
                is_displayed = driver.find_element(By.XPATH, cm_xpath).is_displayed()
                
                if is_displayed:
                    xpath = cm_xpath
                    break
            
        return xpath
    
    def total_collection_brk(driver):
        xpath = ''
        
        for row in range(10):
            cm_xpath = '/html/body/div[1]/main/div[3]/div['+str(row+1)+']/div/div/div[3]/div[1]/div/table/tfoot/tr/td[6]'
            count = driver.find_elements(By.XPATH, cm_xpath)
            count = len(count)
            
            if count != 0:
                is_displayed = driver.find_element(By.XPATH, cm_xpath).is_displayed()
                
                if is_displayed:
                    xpath = cm_xpath
                    break
            
        return xpath
    
    
    def daily_collection_brk(driver):
        xpath = ''
        
        for row in range(10):
            cm_xpath = '/html/body/div[1]/main/div[3]/div['+str(row+1)+']/div/div/div[2]/div[2]/div/table/tr/td[4]'
            count = driver.find_elements(By.XPATH, cm_xpath)
            count = len(count)
            div_number = ''
            
            if count != 0:
                is_displayed = driver.find_element(By.XPATH, cm_xpath).is_displayed()
                
                if is_displayed:
                    xpath = cm_xpath
                    div_number = row+1
                    break
            else:
                xpath = '/html/body/div[1]/main/div[3]/div['+str(div_number)+']/div/div/div[2]/div[2]/div/table/tbody/tr/td'
            
        return xpath
    
    def no_show_brk(driver):
        xpath = ''
        
        for row in range(10):
            cm_xpath = '/html/body/div[1]/main/div[3]/div['+str(row+1)+']/div/div/div[2]/div[2]/div/table/tr/td[2]'
            count = driver.find_elements(By.XPATH, cm_xpath)
            count = len(count)
            div_number = ''
            
            if count != 0:
                is_displayed = driver.find_element(By.XPATH, cm_xpath).is_displayed()
                
                if is_displayed:
                    xpath = cm_xpath
                    div_number = row+1
                    break
            else:
                xpath = '/html/body/div[1]/main/div[3]/div['+str(div_number)+']/div/div/div[2]/div[2]/div/table/tbody/tr/td'
            
        return xpath
    
    def case_acceptance(driver):
        xpath = ''
        
        for row in range(10):
            cm_xpath = '/html/body/div[1]/main/div[3]/div['+str(row+1)+']/div/div/div[2]/div[1]/div/table/tfoot/tr[1]/td[6]'
            count = driver.find_elements(By.XPATH, cm_xpath)
            count = len(count)
            
            if count != 0:
                is_displayed = driver.find_element(By.XPATH, cm_xpath).is_displayed()
                
                if is_displayed:
                    xpath = cm_xpath
                    break
            
        return xpath
    
    
    def same_day_tx(driver):
        xpath = ''
        
        for row in range(10):
            cm_xpath = '/html/body/div[1]/main/div[3]/div['+str(row+1)+']/div/div/div[2]/div[2]/div/table/tr[2]/td[5]'
            count = driver.find_elements(By.XPATH, cm_xpath)
            count = len(count)
            div_number = ''
            
            if count != 0:
                is_displayed = driver.find_element(By.XPATH, cm_xpath).is_displayed()
                
                if is_displayed:
                    xpath = cm_xpath
                    div_number = row+1
                    break
            else:
                xpath = '/html/body/div[1]/main/div[3]/div['+str(div_number)+']/div/div/div[2]/div[2]/div/table/tbody/tr/td'
            
        return xpath
    
    
    def pts_miss_referral(driver):
        value = 0

        for row in range(10):
            cm_xpath = '/html/body/div[1]/main/div[3]/div['+str(row+1)+']/div/div/div[2]/div[2]/div/table/tbody/tr'
            count = driver.find_elements(By.XPATH, cm_xpath)
            count = len(count)
            
            if count != 0:
                is_displayed = driver.find_element(By.XPATH, cm_xpath).is_displayed()
                
                if count == 1:
                    check_text = driver.find_element(By.XPATH, cm_xpath).text
                    
                    if check_text == 'Nothing to show.':
                        value = 0
                    else:
                        value = 1
                else:
                    value = count  
                        
                if is_displayed:
                    break
                
        return value
    
    def hyg_reappt(driver):
        xpath = ''
        
        for row in range(10):
            cm_xpath = '/html/body/div[1]/main/div[3]/div['+str(row+1)+']/div/div/div[2]/div[2]/div/table/tr/td[3]'
            count = driver.find_elements(By.XPATH, cm_xpath)
            count = len(count)
            div_number = ''
            
            if count != 0:
                is_displayed = driver.find_element(By.XPATH, cm_xpath).is_displayed()
                
                if is_displayed:
                    xpath = cm_xpath
                    div_number = row+1
                    break
            else:
                xpath = '/html/body/div[1]/main/div[3]/div['+str(div_number)+']/div/div/div[2]/div[2]/div/table/tbody/tr/td'
            
        return xpath
    
    def new_patient(driver):
        value = 0

        for row in range(10):
            cm_xpath = '/html/body/div[1]/main/div[3]/div['+str(row+1)+']/div/div/div[2]/table/tbody/tr'
            count = driver.find_elements(By.XPATH, cm_xpath)
            count = len(count)
            
            if count != 0:
                value = count
                break
                
        return value
    
    
    
    
    
    