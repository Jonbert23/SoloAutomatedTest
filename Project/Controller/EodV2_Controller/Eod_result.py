class EodResult:
    
    def Brk_result(eod_main, eod_brk):
        pt_portion_col = EodResult.Eod_result(eod_main.pt_portion_col, eod_brk.pt_portion_col)
        adjustments  = EodResult.Eod_result(eod_main.adjustments, eod_brk.adjustments)
        total_collection = EodResult.Eod_result(eod_main.total_collection, eod_brk.total_collection)
        daily_collection = EodResult.Eod_result(eod_main.daily_collection, eod_brk.daily_collection)
        no_show = EodResult.Eod_result(eod_main.no_show, eod_brk.no_show)
        same_day_tx = EodResult.Eod_result(eod_main.same_day_tx, eod_brk.same_day_tx)
        new_patient = EodResult.Eod_result(eod_main.new_patient, eod_brk.new_patient)
        pts_miss_referral = EodResult.Eod_result(eod_main.pts_miss_referral, eod_brk.pts_miss_referral)
        hyg_reappt = EodResult.Eod_result(eod_main.hyg_reappt, eod_brk.hyg_reappt)
        case_acceptance = EodResult.Eod_result(eod_main.case_acceptance, eod_brk.hyg_reappt)
        
        result = {
            'pt_portion_col'  : pt_portion_col,
            'adjustments'  : adjustments,
            'total_collection'  : total_collection,
            'daily_collection'  : daily_collection,
            'no_show'  : no_show,
            'same_day_tx'  : same_day_tx,
            'new_patient'  : new_patient,
            'pts_miss_referral'  : pts_miss_referral,
            'hyg_reappt'  : hyg_reappt,
            'case_acceptance'  : case_acceptance,
        }
        
        return result
    
    def eod_graph_result(eod_result):
        Pass = 0
        Fail = 0
        Total = 0
        
        for x in eod_result:
            # print(eod_result[x])
            if eod_result[x] == 'Pass':
                Pass = Pass + 1
            else:
                Fail = Fail + 1
                
        Total = Pass + Fail
        Fail = (Fail / Total) * 100
        Pass = (Pass / Total) * 100
        
        # print(Total)
        # print(Fail)
        # print(Pass)
        result = {
            'Pass': Pass,
            'Fail': Fail
        }
        
        return result
                
    
    def Eod_result(main, brk):
        main = main.replace("$","").replace(",","").replace(" ","").replace("%","").replace("N/A","0").replace("(","-").replace(")","")
        brk = brk.replace("$","").replace(",","").replace(" ","").replace("%","").replace("N/A","0").replace("(","-").replace(")","")
        result = ''
        
        if float(main) == float(brk):
            result = 'Pass'
        else:
            result = 'Fail'
            
        return result