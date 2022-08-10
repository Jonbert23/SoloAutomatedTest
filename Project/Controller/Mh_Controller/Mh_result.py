class MhResult:
    
    def brk_ytr_result(mh_main, mh_brk):
        ytr_gross_prod = MhResult.result(mh_main.ytr_gross_prod, mh_brk.ytr_gross_prod)
        ytr_net_prod = MhResult.result(mh_main.ytr_net_prod, mh_brk.ytr_net_prod)
        ytr_collection  = MhResult.result(mh_main.ytr_collection, mh_brk.ytr_collection)
        ytr_collection_percent = MhResult.result(mh_main.ytr_collection_percent, mh_brk.ytr_collection_percent)
        ytr_prod_per_patient  = MhResult.result(mh_main.ytr_prod_per_patient , mh_brk.ytr_prod_per_patient )
        ytr_npt = MhResult.result(mh_main.ytr_npt, mh_brk.ytr_npt)
        ytr_care_progress = MhResult.result(mh_main.ytr_care_progress, mh_brk.ytr_care_progress)
        ytr_copay = MhResult.result(mh_main.ytr_copay , mh_brk.ytr_copay)
        ytr_tx_acceptance = MhResult.result(mh_main.ytr_tx_acceptance, mh_brk.ytr_tx_acceptance)
        ytr_tx_presented = MhResult.result(mh_main.ytr_tx_presented, mh_brk.ytr_tx_presented)
        ytr_tx_completed = MhResult.result(mh_main.ytr_tx_completed, mh_brk.ytr_tx_completed)
        ytr_tx_sched = MhResult.result(mh_main.ytr_tx_sched , mh_brk.ytr_tx_sched )
        ytr_tx_unsched = MhResult.result(mh_main.ytr_tx_unsched , mh_brk.ytr_tx_unsched )
        ytr_hyg_prod = MhResult.result(mh_main.ytr_hyg_prod , mh_brk.ytr_hyg_prod )
        ytr_hyg_reappt = MhResult.result(mh_main.ytr_hyg_reappt , mh_brk.ytr_hyg_reappt )
        ytr_hyg_sched = MhResult.result(mh_main.ytr_hyg_sched , mh_brk.ytr_hyg_sched )
        ytr_not_sched = MhResult.result(mh_main.ytr_not_sched , mh_brk.ytr_not_sched )
        ytr_broken_appt = MhResult.result(mh_main.ytr_broken_appt, mh_brk.ytr_broken_appt)
        ytr_unshed_broken_appt = MhResult.result(mh_main.ytr_unshed_broken_appt  , mh_brk.ytr_unshed_broken_appt  )
        ytr_npt_not_resched = MhResult.result(mh_main.ytr_npt_not_resched, mh_brk.ytr_npt_not_resched  )
        ytr_pts_not_resched = MhResult.result(mh_main.ytr_pts_not_resched , mh_brk.ytr_pts_not_resched )
        
        result = {
           'ytr_gross_prod' : ytr_gross_prod,
           'ytr_net_prod': ytr_net_prod,
           'ytr_collection': ytr_collection,
           'ytr_collection_percent': ytr_collection_percent,
           'ytr_prod_per_patient': ytr_prod_per_patient,
           'ytr_npt': ytr_npt,
           'ytr_care_progress': ytr_care_progress,
           'ytr_copay': ytr_copay,
           'ytr_tx_acceptance': ytr_tx_acceptance,
           'ytr_tx_presented': ytr_tx_presented,
           'ytr_tx_completed': ytr_tx_completed,
           'ytr_tx_sched': ytr_tx_sched,
           'ytr_tx_unsched': ytr_tx_unsched,
           'ytr_hyg_prod': ytr_hyg_prod,
           'ytr_hyg_reappt': ytr_hyg_reappt,
           'ytr_hyg_sched': ytr_hyg_sched,
           'ytr_not_sched': ytr_not_sched,  
           'ytr_broken_appt': ytr_broken_appt,
           'ytr_unshed_broken_appt': ytr_unshed_broken_appt ,
           'ytr_npt_not_resched': ytr_npt_not_resched,
           'ytr_pts_not_resched': ytr_pts_not_resched,
            
        }
        
        return result 
    
    def brk_tdy_result(mh_main, mh_brk):
        tdy_npt_actual = MhResult.result(mh_main.tdy_npt_actual, mh_brk.tdy_npt_actual)
        tdy_npt_sched = MhResult.result(mh_main.tdy_npt_sched , mh_brk.tdy_npt_sched)
        tdy_hyg_prod_sched = MhResult.result(mh_main.tdy_hyg_prod_sched , mh_brk.tdy_hyg_prod_sched )
        tdy_hyg_prod_actual = MhResult.result(mh_main.tdy_hyg_prod_actual, mh_brk.tdy_hyg_prod_actual)
        tdy_unsched_tx = MhResult.result(mh_main.tdy_unsched_tx , mh_brk.tdy_unsched_tx )
        tdy_unsched_family_members = MhResult.result(mh_main.tdy_unsched_family_members, mh_brk.tdy_unsched_family_members)
        tdy_unsched_hyg = MhResult.result(mh_main.tdy_unsched_hyg, mh_brk.tdy_unsched_hyg)
        tdy_patient_bday = MhResult.result(mh_main.tdy_patient_bday , mh_brk.tdy_patient_bday )
        tdy_past_due_ar = MhResult.result(mh_main.tdy_past_due_ar, mh_brk.tdy_past_due_ar)
        tdy_due_bwx = MhResult.result(mh_main.tdy_due_bwx, mh_brk.tdy_due_bwx)
        tdy_due_fmx = MhResult.result(mh_main.tdy_due_fmx, mh_brk.tdy_due_fmx)
        
        result = {
            'tdy_npt_actual': tdy_npt_actual,
            'tdy_npt_sched': tdy_npt_sched,
            'tdy_hyg_prod_sched': tdy_hyg_prod_sched,
            'tdy_hyg_prod_actual': tdy_hyg_prod_actual,
            'tdy_unsched_tx': tdy_unsched_tx,
            'tdy_unsched_family_members':tdy_unsched_family_members,
            'tdy_unsched_hyg': tdy_unsched_hyg,
            'tdy_patient_bday': tdy_patient_bday,
            'tdy_past_due_ar': tdy_past_due_ar,
            'tdy_due_bwx': tdy_due_bwx,
            'tdy_due_fmx': tdy_due_fmx,
        }
        
        return result
    
    def brk_tmw_result(mh_main, mh_brk):
        tmw_npt_sched = MhResult.result(mh_main.tmw_npt_sched, mh_brk.tmw_npt_sched)
        tmw_hyg_prod_sched = MhResult.result(mh_main.tmw_hyg_prod_sched, mh_brk.tmw_hyg_prod_sched)
        tmw_unsched_tx = MhResult.result(mh_main.tmw_unsched_tx, mh_brk.tmw_unsched_tx)
        tmw_unsched_family_members = MhResult.result(mh_main.tmw_unsched_family_members, mh_brk.tmw_unsched_family_members)
        tmw_unsched_hyg = MhResult.result(mh_main.tmw_unsched_hyg, mh_brk.tmw_unsched_hyg)
        tmw_past_due_ar = MhResult.result(mh_main.tmw_past_due_ar, mh_brk.tmw_past_due_ar)
        tmw_due_bwx = MhResult.result(mh_main.tmw_due_bwx, mh_brk.tmw_due_bwx)
        twm_due_fmx = MhResult.result(mh_main.twm_due_fmx, mh_brk.twm_due_fmx)
        
        result = {
            'tmw_npt_sched': tmw_npt_sched,
            'tmw_hyg_prod_sched': tmw_hyg_prod_sched,
            'tmw_unsched_tx': tmw_unsched_tx,
            'tmw_unsched_family_members': tmw_unsched_family_members,
            'tmw_unsched_hyg': tmw_unsched_hyg,
            'tmw_past_due_ar': tmw_past_due_ar,
            'tmw_due_bwx': tmw_due_bwx,
            'twm_due_fmx': twm_due_fmx,
        }
        
        return result
    
    def sc_result(mh_main, mh_sc):
        ytr_prod = MhResult.result(mh_main.ytr_net_prod, mh_sc.ytr_prod)
        ytr_goal = MhResult.result(mh_main.ytr_goal, mh_sc.ytr_goal)
        ytr_collection = MhResult.result(mh_main.ytr_collection, mh_sc.ytr_collection)
        ytr_npt_actual = MhResult.result(mh_main.ytr_npt, mh_sc.ytr_npt_actual)
        yrt_broken_appt = MhResult.result(mh_main.ytr_broken_appt, mh_sc.yrt_broken_appt)
        
        tdy_sched_prod = MhResult.result(mh_main.tdy_sched_prod, mh_sc.tdy_sched_prod)
        tdy_goal = MhResult.result(mh_main.tdy_goal, mh_sc.tdy_goal)
        tdy_npt_actual = MhResult.result(mh_main.tdy_npt_actual, mh_sc.tdy_npt_actual)
        tdy_npt_sched = MhResult.result(mh_main.tdy_npt_sched, mh_sc.tdy_npt_sched)
        
        tmw_sched_prod = MhResult.result(mh_main.tmw_sched_prod, mh_sc.tmw_sched_prod) 
        tmw_goal = MhResult.result(mh_main.tmw_goal, mh_sc.tmw_goal) 
        tmw_npt = MhResult.result(mh_main.tmw_npt_sched, mh_sc.tmw_npt)
        
        result = {
            'ytr_prod': ytr_prod,
            'ytr_goal': ytr_goal,
            'ytr_collection': ytr_collection,
            'ytr_npt_actual': ytr_npt_actual,
            'yrt_broken_appt': yrt_broken_appt,
            'tdy_sched_prod': tdy_sched_prod,
            'tdy_goal': tdy_goal,
            'tdy_npt_actual': tdy_npt_actual,
            'tdy_npt_sched': tdy_npt_sched,
            'tmw_sched_prod': tmw_sched_prod,
            'tmw_goal': tmw_goal,
            'tmw_npt': tmw_npt,
        }
        
        return result
    
    def result(main, brk):
        main = main.replace("$","").replace(",","").replace(" ","").replace("%","").replace("N/A","0").replace("(","-").replace(")","")
        brk = brk.replace("$","").replace(",","").replace(" ","").replace("%","").replace("N/A","0").replace("(","-").replace(")","")
        result = ''
        
        if float(main) == float(brk):
            result = 'Pass'
        else:
            result = 'Fail'
            
        return result