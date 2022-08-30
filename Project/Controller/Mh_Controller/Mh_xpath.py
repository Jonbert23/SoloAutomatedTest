class MHXpath:
    ytr_counter = '/html/body/div[1]/main/div[2]/div[1]/div[1]/div/div/div/div/strong'
    tdy_counter = '/html/body/div[1]/main/div[2]/div[1]/div[2]/div/div/div/strong'
    tmw_counter = '/html/body/div[1]/main/div[2]/div[1]/div[3]/div/div/div/div/strong'
    update_btn = '/html/body/div[1]/main/div[1]/div/div/div/div[4]/button'
    brk_column_counter = '/html/body/div[1]/main/div[4]/div/div/div/div[2]/section/div/div/div[2]/div/div[1]/table/tr/td'
    modal_exit = '/html/body/div[1]/main/div[4]/div/div/div/div[2]/div/button'
    
    ytr_sc_goal = '/html/body/div[1]/main/div[4]/div/div/div/div[2]/div/div[2]/div[2]/div[1]/div/div[2]/h4/span'
    ytr_sc_prod = '/html/body/div[1]/main/div[4]/div/div/div/div[2]/div/div[2]/div[2]/div[3]/div/div[2]/h4/div/span'
    ytr_sc_collection = '/html/body/div[1]/main/div[4]/div/div/div/div[2]/div/div[2]/div[2]/div[4]/div/div[2]/h4/span'
    ytr_sc_npt = '/html/body/div[1]/main/div[4]/div/div/div/div[2]/div/div[2]/div[3]/div[2]/div[2]/div[2]/div/div/div[1]/div[2]/h4/span'
    ytr_sc_broken_visst = '/html/body/div[1]/main/div[4]/div/div/div/div[2]/div/div[2]/div[3]/div[2]/div[2]/div[3]/div/div[2]/h4/span'
    
    tdy_sc_sched_prod = '/html/body/div[1]/main/div[4]/div/div/div/div[2]/div/div[2]/div[2]/div[2]/div/div[2]/h4/div/span'
    tdy_sc_goal = '/html/body/div[1]/main/div[4]/div/div/div/div[2]/div/div[2]/div[2]/div[1]/div/div[2]/h4/span'
    tdy_sc_npt_actual = '/html/body/div[1]/main/div[4]/div/div/div/div[2]/div/div[2]/div[3]/div[2]/div[2]/div[2]/div/div/div[1]/div[2]/h4/span'
    tdy_sc_npt_sched = '/html/body/div[1]/main/div[4]/div/div/div/div[2]/div/div[2]/div[3]/div[1]/div[2]/div[3]/div/div[2]/h4/span'
    
    tmw_sc_sched_prod = '/html/body/div[1]/main/div[4]/div/div/div/div[2]/div/div[2]/div[2]/div[2]/div/div[2]/h4/div/span'
    tmw_sc_goal = '/html/body/div[1]/main/div[4]/div/div/div/div[2]/div/div[2]/div[2]/div[1]/div/div[2]/h4/span'
    tmw_sc_npt = '/html/body/div[1]/main/div[4]/div/div/div/div[2]/div/div[2]/div[3]/div[1]/div[2]/div[3]/div/div[2]/h4/span'
   
    
    def ytr_name(row):
        name = '/html/body/div[1]/main/div[2]/div[1]/div[1]/div/div/div['+str(row)+']/div/strong'
        return name
    
    def ytr_value(row):
        value = '/html/body/div[1]/main/div[2]/div[1]/div[1]/div/div/div['+str(row)+']/input'
        return value
    
    def yrt_breakdown(row):
        brk = '/html/body/div[1]/main/div[2]/div[1]/div[1]/div/div/div['+str(row)+']/div/button'
        return brk
    
    def brk_value(column):
        value = '/html/body/div[1]/main/div[4]/div/div/div/div[2]/section/div/div/div[2]/div/div[1]/table/tr/td['+str(column)+']/strong/span'
        return value
    
    def tdy_name(row):
        name = '/html/body/div[1]/main/div[2]/div[1]/div[2]/div/div['+str(row)+']/div/strong'
        return name
    
    def tdy_value(row):
        value = '/html/body/div[1]/main/div[2]/div[1]/div[2]/div/div['+str(row)+']/input'
        return value
    
    def tdy_brk_btn(row):
        btn = '/html/body/div[1]/main/div[2]/div[1]/div[2]/div/div['+str(row)+']/div/button'
        return btn 
    
    def tmw_name(row):
        name = '/html/body/div[1]/main/div[2]/div[1]/div[3]/div/div/div['+str(row)+']/div/strong'
        return name
    
    def tmw_value(row):
        value = '/html/body/div[1]/main/div[2]/div[1]/div[3]/div/div/div['+str(row)+']/input'
        return value
    
    def tmw_brk_btn(row):
        btn = '/html/body/div[1]/main/div[2]/div[1]/div[3]/div/div/div['+str(row)+']/div/button'
        return btn
    
    
class MailTestXpath:
    open_mail_btn = '/html/body/div[1]/main/div[2]/div[2]/button'
    mail_input = '/html/body/div[1]/main/div[5]/div/div/div/form/div[1]/input'
    mail_subject = '/html/body/div[1]/main/div[5]/div/div/div/form/div[3]/input'
    mail_note = '/html/body/div[1]/main/div[5]/div/div/div/form/div[4]/textarea'
    send_mail_btn = '/html/body/div[1]/main/div[5]/div/div/div/form/div[5]/button'
    
    username_field = '//div[1]/div/div[1]/div/div/input'
    password_field = '/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[1]/input'
    
    mail_inbox_counter = '/html/body/div[7]/div[3]/div/div[2]/div[2]/div/div/div/div/div[2]/div/div[1]/div/div/div[8]/div/div[1]/div[3]/div/table/tbody/tr'
    ytr_mail_counter = '/html/body/div[7]/div[3]/div/div[2]/div[2]/div/div/div/div/div[2]/div/div[1]/div/div[2]/div/table/tr/td[1]/div[2]/div[2]/div/div[3]/div/div/div/div/div/div[1]/div[2]/div[3]/div[3]/div[1]/div[1]/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[1]/td/table/tbody/tr/td/table/tbody/tr'
    tmw_mail_counter = '/html/body/div[7]/div[3]/div/div[2]/div[2]/div/div/div/div/div[2]/div/div[1]/div/div[2]/div/table/tr/td[1]/div[2]/div[2]/div/div[3]/div/div/div/div/div/div[1]/div[2]/div[3]/div[3]/div/div[1]/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[4]/td/table/tbody/tr/td/table/tbody/tr'
    tdy_mail_counter = '/html/body/div[7]/div[3]/div/div[2]/div[2]/div/div/div/div/div[2]/div/div[1]/div/div[2]/div/table/tr/td[1]/div[2]/div[2]/div/div[3]/div/div/div/div/div/div[1]/div[2]/div[3]/div[3]/div[1]/div[1]/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[3]/td/table/tbody/tr/td/table/tbody/tr'
    
    
    def mail_inbox(row):
        inbox = '/html/body/div[7]/div[3]/div/div[2]/div[2]/div/div/div/div/div[2]/div/div[1]/div/div/div[8]/div/div[1]/div[3]/div/table/tbody/tr['+str(row)+']/td[5]/div/div/div'
        return inbox
    
    
    def ytr_mail_metric_name(row):
        name = '/html/body/div[7]/div[3]/div/div[2]/div[2]/div/div/div/div/div[2]/div/div[1]/div/div[2]/div/table/tr/td[1]/div[2]/div[2]/div/div[3]/div/div/div/div/div/div[1]/div[2]/div[3]/div[3]/div[1]/div[1]/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[1]/td/table/tbody/tr/td/table/tbody/tr['+str(row)+']/td[1]'
        return name
    
    def ytr_mail_metric_value(row):
        value = '/html/body/div[7]/div[3]/div/div[2]/div[2]/div/div/div/div/div[2]/div/div[1]/div/div[2]/div/table/tr/td[1]/div[2]/div[2]/div/div[3]/div/div/div/div/div/div[1]/div[2]/div[3]/div[3]/div[1]/div[1]/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[1]/td/table/tbody/tr/td/table/tbody/tr['+str(row)+']/td[2]'
        return value
    
    def tdy_mail_metric_name(row):
        name = '/html/body/div[7]/div[3]/div/div[2]/div[2]/div/div/div/div/div[2]/div/div[1]/div/div[2]/div/table/tr/td[1]/div[2]/div[2]/div/div[3]/div/div/div/div/div/div[1]/div[2]/div[3]/div[3]/div[1]/div[1]/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[3]/td/table/tbody/tr/td/table/tbody/tr['+str(row)+']/td[1]'
        return name
    
    def tdy_mail_metric_value(row):
        value = '/html/body/div[7]/div[3]/div/div[2]/div[2]/div/div/div/div/div[2]/div/div[1]/div/div[2]/div/table/tr/td[1]/div[2]/div[2]/div/div[3]/div/div/div/div/div/div[1]/div[2]/div[3]/div[3]/div[1]/div[1]/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[3]/td/table/tbody/tr/td/table/tbody/tr['+str(row)+']/td[2]'
        return value
    
    def tmw_mail_metric_name(row):
        name = '/html/body/div[7]/div[3]/div/div[2]/div[2]/div/div/div/div/div[2]/div/div[1]/div/div[2]/div/table/tr/td[1]/div[2]/div[2]/div/div[3]/div/div/div/div/div/div[1]/div[2]/div[3]/div[3]/div/div[1]/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[4]/td/table/tbody/tr/td/table/tbody/tr['+str(row)+']/td[1]'
        return name
    
    def tmw_mail_metric_value(row):
        value = '/html/body/div[7]/div[3]/div/div[2]/div[2]/div/div/div/div/div[2]/div/div[1]/div/div[2]/div/table/tr/td[1]/div[2]/div[2]/div/div[3]/div/div/div/div/div/div[1]/div[2]/div[3]/div[3]/div/div[1]/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[4]/td/table/tbody/tr/td/table/tbody/tr['+str(row)+']/td[2]'
        return value