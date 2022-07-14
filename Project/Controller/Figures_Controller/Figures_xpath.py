class DashboardXpath:
    net_prod = '/html/body/div[1]/main/div[2]/section[1]/div[1]/div[1]/div/div/div[2]/h3'
    gross_prod = '/html/body/div[1]/main/div[2]/section[1]/div[1]/div[2]/div/div/div[2]/h3'
    collection = '/html/body/div[1]/main/div[2]/section[1]/div[1]/div[3]/div/div/div[2]/h3'
    adj = '/html/body/div[1]/main/div[2]/section[1]/div[1]/div[4]/div/div/div[2]/h3'
    npt = "/html/body/div[1]/main/div[2]/section[2]/div/div[1]/div/div[1]/div/div/div[2]/h3"
    pts = "/html/body/div[1]/main/div[2]/section[2]/div/div[1]/div/div[2]/div/div/div[2]/h3"
    
    metric_counter = '/html/body/div[1]/main/div[2]/section[1]/div[1]/div/div/div/div[1]/h6'
    
    def metric_name(row):
        name = '/html/body/div[1]/main/div[2]/section[1]/div[1]/div['+str(row)+']/div/div/div[1]/h6'
        return name
    
    def metric_value(row):
        value = '/html/body/div[1]/main/div[2]/section[1]/div[1]/div['+str(row)+']/div/div/div[2]/h3'
        return value
    
    
class EodXpath:
    net_prod = '/html/body/div[1]/main/div[2]/div[3]/div[1]/div/form/div/div[2]/div[8]/div[2]/input'
    gross_prod = '/html/body/div[1]/main/div[2]/div[3]/div[1]/div/form/div/div[2]/div[9]/div[2]/input'
    collection = '/html/body/div[1]/main/div[2]/div[3]/div[1]/div/form/div/div[2]/div[11]/div[2]/input'
    adj = '/html/body/div[1]/main/div[2]/div[3]/div[1]/div/form/div/div[2]/div[10]/div[2]/input'
    npt = '/html/body/div[1]/main/div[2]/div[3]/div[1]/div/form/div/div[2]/div[12]/div[2]/input'
    pts = '/html/body/div[1]/main/div[2]/div[3]/div[1]/div/form/div/div[2]/div[14]/div[2]/input'
    update_btn = '/html/body/div[1]/main/div[1]/div/div/div/div[3]/button'
    metric_counter = '/html/body/div[1]/main/div[2]/div[3]/div[1]/div/form/div/div[1]/div[1]/div/div/div[1]'
    
    def metric_name(row):
        name = '/html/body/div[1]/main/div[2]/div[3]/div[1]/div/form/div/div[1]/div[1]/div/div['+str(row)+']/div[1]'
        return name
    
    def metric_value(row):
        value = '/html/body/div[1]/main/div[2]/div[3]/div[1]/div/form/div/div[1]/div[1]/div/div['+str(row)+']/div[2]/input'
        return value
    
class CalendarXpath:
    prod = '/html/body/div[1]/main/div[2]/div/span/div[1]/div[2]/div/div[6]/div/div[2]/h4/span'
    npt = '/html/body/div[1]/main/div[2]/div/span/div[1]/div[2]/div/div[5]/div/div[2]/h4/span'
    month_button = '/html/body/div[1]/main/div[2]/div/div/div[2]/div[1]/ul/li[1]/a'
    

class DatePicker:
    date_filter_button = '/html/body/div[1]/main/div[1]/div/div/div/div[1]/div'
    
    def date_xpath(row, column):
        date = '/html/body/div[1]/main/div[1]/div/div/div/div[1]/div/div[2]/div/div[2]/div[1]/div/table/tbody/tr['+str(row)+']/td['+str(column)+']'
        return date
    
class MhXpath:
    metric_counter = '/html/body/div[1]/main/div[2]/div[1]/div[1]/div/div/div/div/strong'
    
    def metric_name(row):
        name = '/html/body/div[1]/main/div[2]/div[1]/div[1]/div/div/div['+str(row)+']/div/strong'
        return name
    
    def metric_value(row):
        value = '/html/body/div[1]/main/div[2]/div[1]/div[1]/div/div/div['+str(row)+']/input'
        return value
    prod = '/html/body/div[1]/main/div[4]/div/div/div/div[2]/div/div[2]/div[2]/div[3]/div/div[2]/h4/div/span'
    collection = '/html/body/div[1]/main/div[4]/div/div/div/div[2]/div/div[2]/div[2]/div[4]/div/div[2]/h4/span'
    npt = '/html/body/div[1]/main/div[4]/div/div/div/div[2]/div/div[2]/div[3]/div[2]/div[2]/div[2]/div/div/div[1]/div[2]/h4/span'
    pts = '/html/body/div[1]/main/div[4]/div/div/div/div[2]/div/div[2]/div[3]/div[2]/div[2]/div[2]/div/div/div[2]/div[2]/h4/span'
    scorecard = '/html/body/div[1]/main/div[2]/div[1]/div[2]/h5/a'
    
    