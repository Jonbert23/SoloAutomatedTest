class LoginXpath:
    username = '/html/body/div/div/div/div/div[1]/div/form/div[1]/div/input'
    password = '/html/body/div/div/div/div/div[1]/div/form/div[2]/div[2]/input'
    login_btn = '/html/body/div/div/div/div/div[1]/div/form/button'
    main_header = '/html/body/div[1]/main/header'
    login_error = '/html/body/div/div/div/div/div[1]/div/form/p'
    logo_xpath = '/html/body/div/div/div/div/div[1]/div/div/a/img'
    no_vpn = '/html/body/div/div/div[1]'
    
    
class DatePicker:
    date_filter_button = '/html/body/div[1]/main/div[1]/div/div/div/div[1]/div'
    update_button = '/html/body/div[1]/main/div[1]/div/div/div/div[4]/button'
    start_arrow_back = '/html/body/div[1]/main/div[1]/div/div/div/div[1]/div/div[2]/div/div[2]/div[1]/div/table/thead/tr/th[1]'
    start_arrow_next = '/html/body/div[1]/main/div[1]/div/div/div/div[1]/div/div[2]/div/div[2]/div[1]/div/table/thead/tr/th[3]'
    start_year = '/html/body/div[1]/main/div[1]/div/div/div/div[1]/div/div[2]/div/div[2]/div[1]/div/table/thead/tr/th[2]/div/input'
    start_month = '/html/body/div[1]/main/div[1]/div/div/div/div[1]/div/div[2]/div/div[2]/div[1]/div/table/thead/tr/th[2]/div/select'
    
    end_arrow_back = '/html/body/div[1]/main/div[1]/div/div/div/div[1]/div/div[2]/div/div[2]/div[2]/div/table/thead/tr/th[1]'
    end_arrow_next = '/html/body/div[1]/main/div[1]/div/div/div/div[1]/div/div[2]/div/div[2]/div[2]/div/table/thead/tr/th[3]'
    end_year = '/html/body/div[1]/main/div[1]/div/div/div/div[1]/div/div[2]/div/div[2]/div[2]/div/table/thead/tr/th[2]/div/input'
    end_month = '/html/body/div[1]/main/div[1]/div/div/div/div[1]/div/div[2]/div/div[2]/div[2]/div/table/thead/tr/th[2]/div/select'
    
    def start_date_xpath(row, column):
        date = '/html/body/div[1]/main/div[1]/div/div/div/div[1]/div/div[2]/div/div[2]/div[1]/div/table/tbody/tr['+str(row)+']/td['+str(column)+']'
        return date
    
    def end_date_xpath(row, column):
        date = '/html/body/div[1]/main/div[1]/div/div/div/div[1]/div/div[2]/div/div[2]/div[2]/div/table/tbody/tr['+str(row)+']/td['+ str(column)+']'
        return date