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
    
    
    
    