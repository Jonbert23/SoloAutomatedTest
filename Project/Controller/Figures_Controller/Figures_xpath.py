class DashboardXpath:
    net_prod = '/html/body/div[1]/main/div[2]/section[1]/div[1]/div[1]/div/div/div[2]/h3'
    gross_prod = '/html/body/div[1]/main/div[2]/section[1]/div[1]/div[2]/div/div/div[2]/h3'
    collection = '/html/body/div[1]/main/div[2]/section[1]/div[1]/div[3]/div/div/div[2]/h3'
    adj = '/html/body/div[1]/main/div[2]/section[1]/div[1]/div[4]/div/div/div[2]/h3'
    npt = "/html/body/div[1]/main/div[2]/section[2]/div/div[1]/div/div[1]/div/div/div[2]/h3"
    pts = "/html/body/div[1]/main/div[2]/section[2]/div/div[1]/div/div[2]/div/div/div[2]/h3"
    
class EodXpath:
    net_prod = '/html/body/div[1]/main/div[2]/div[3]/div[1]/div/form/div/div[2]/div[8]/div[2]/input'
    gross_prod = '/html/body/div[1]/main/div[2]/div[3]/div[1]/div/form/div/div[2]/div[9]/div[2]/input'
    collection = '/html/body/div[1]/main/div[2]/div[3]/div[1]/div/form/div/div[2]/div[11]/div[2]/input'
    adj = '/html/body/div[1]/main/div[2]/div[3]/div[1]/div/form/div/div[2]/div[11]/div[2]/input'
    npt = '/html/body/div[1]/main/div[2]/div[3]/div[1]/div/form/div/div[2]/div[12]/div[2]/input'
    pts = '/html/body/div[1]/main/div[2]/div[3]/div[1]/div/form/div/div[2]/div[14]/div[2]/input'
    
class CalendarXpath:
    prod = '/html/body/div[1]/main/div[2]/div/span/div[1]/div[2]/div/div[6]/div/div[2]/h4/span'
    npt = '/html/body/div[1]/main/div[2]/div/span/div[1]/div[2]/div/div[5]/div/div[2]/h4/span'
    month_button = '/html/body/div[1]/main/div[2]/div/div/div[2]/div[1]/ul/li[1]/a'
    

class DatePicker:
    date_filter_button = '/html/body/div[1]/main/div[1]/div/div/div/div[1]/div'
    
    def date_xpath(row, column):
        date = '/html/body/div[1]/main/div[1]/div/div/div/div[1]/div/div[2]/div/div[2]/div[1]/div/table/tbody/tr['+str(row)+']/td['+str(column)+']'
        return date
    
    