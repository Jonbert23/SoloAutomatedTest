from flask import Blueprint, render_template, url_for, request, redirect
from flask_login import login_required, current_user
from array import *
# import numpy as np
from ..Tx_Controller import Tx_selenium
from ...models import TestCodes
from ...models import TxMinerDefaultTest
from ...models import TxMinerProviderTest
from ...models import TxMinerProcedureTest
from ...models import TxMinerPatientTest

tx = Blueprint('tx', __name__)

@tx.route("/tx-miner")
@login_required
def txMiner():

    getDefault = TxMinerDefaultTest.query.order_by(TxMinerDefaultTest.id.desc()).first()
    getProvider = TxMinerProviderTest.query.order_by(TxMinerProviderTest.id.desc()).first()
    getProcedure = TxMinerProcedureTest.query.order_by(TxMinerProcedureTest.id.desc()).first()
    getPatient = TxMinerPatientTest.query.order_by(TxMinerPatientTest.id.desc()).first()
    
    print(getPatient)
    if getDefault:
        getTheLatestTestCode = TxMinerDefaultTest.query.order_by(TxMinerDefaultTest.id.desc()).first()
        useTestCode = getTheLatestTestCode.test_code

        getTestCode = TestCodes.query.filter_by(test_code=useTestCode).first()

        getTxMinerDefault = TxMinerDefaultTest.query.filter_by(test_code=useTestCode).all()
        getTxMinerDefaultSched = TxMinerDefaultTest.query.filter_by(test_code=useTestCode).all()
        getTxMinerDefaultActive = TxMinerDefaultTest.query.filter_by(test_code=useTestCode).all()
        pendingSchedStatus = ""
        pendingUnschedStatus = ""
        activeProductionStatus = ""
        for getTxMinerDefault in getTxMinerDefault:
            if getTxMinerDefault.pending_sched_status == 'Fail':
                pendingSchedStatus = "Fail"
            else:
                pendingSchedStatus = "Pass"

        for getTxMinerDefaultSched in getTxMinerDefaultSched:
            if getTxMinerDefaultSched.pending_unsched_status == 'Fail':
                pendingUnschedStatus = "Fail"
            else:
                pendingUnschedStatus = "Pass"
        
        for getTxMinerDefaultActive in getTxMinerDefaultActive:
            if getTxMinerDefaultActive.pending_active_production == 'Fail':
                activeProductionStatus = "Fail"
            else:
                activeProductionStatus = "Pass"
        
        getTxMinderDefaultGraph = TxMinerDefaultTest.query.filter_by(test_code=useTestCode).all()
        lenghtDefaultGraphQuery = len(getTxMinderDefaultGraph)
        months = []
        for x in range(lenghtDefaultGraphQuery):
            monthsBreakdown = getTxMinderDefaultGraph[x].month
            months.insert(1, monthsBreakdown)
        # months = np.array(months)


        getTxMinderMvPendingSched = TxMinerDefaultTest.query.filter_by(test_code=useTestCode).all()
        lenghtMvPendingSched = len(getTxMinderMvPendingSched)
        mvPendingSched = []
        for y in range(lenghtMvPendingSched):
            mvPendingSchedBreaks = getTxMinderMvPendingSched[y].mv_pending_sched.replace(',' , '').replace('$ ','')
            mvPendingSched.insert(1, mvPendingSchedBreaks)
        # mvPendingSched = np.array(mvPendingSched)

        getTxMinderBrPendingSched = TxMinerDefaultTest.query.filter_by(test_code=useTestCode).all()
        lenghtBrPendingSched = len(getTxMinderBrPendingSched)
        brPendingSched = []
        for y in range(lenghtBrPendingSched):
            brPendingSchedBreaks = getTxMinderBrPendingSched[y].breakdown_pending_sched.replace(',' , '').replace('$ ','')
            brPendingSched.insert(1, brPendingSchedBreaks)
        # mvPendingSched = np.array(mvPendingSched)

        getTxMinderMvPendingUnSched = TxMinerDefaultTest.query.filter_by(test_code=useTestCode).all()
        lenghtMvPendingUnSched = len(getTxMinderMvPendingUnSched)
        mvPendingUnSched = []
        for y in range(lenghtMvPendingUnSched):
            mvPendingUnSchedBreaks = getTxMinderMvPendingSched[y].mv_pending_unsched.replace(',' , '').replace('$ ','')
            mvPendingUnSched.insert(1, mvPendingUnSchedBreaks)
        # mvPendingSched = np.array(mvPendingSched)

        getTxMinderBrPendingUnSched = TxMinerDefaultTest.query.filter_by(test_code=useTestCode).all()
        lenghtBrPendingUnSched = len(getTxMinderBrPendingUnSched)
        brPendingUnSched = []
        for y in range(lenghtBrPendingUnSched):
            brPendingUnSchedBreaks = getTxMinderMvPendingSched[y].breakdown_pending_unsched.replace(',' , '').replace('$ ','')
            brPendingUnSched.insert(1, brPendingUnSchedBreaks)
        # mvPendingSched = np.array(mvPendingSched)

        getTxMinderMvActiveProduction = TxMinerDefaultTest.query.filter_by(test_code=useTestCode).all()
        lenghtMvActiveProduction = len(getTxMinderMvActiveProduction)
        mvActiveProduction = []
        for y in range(lenghtMvActiveProduction):
            mvPendingActiveProduction = getTxMinderMvPendingSched[y].mv_active_production.replace(',' , '').replace('$ ','')
            mvActiveProduction.insert(1, mvPendingActiveProduction)
        # mvPendingSched = np.array(mvPendingSched)

        getTxMinderBrActiveProduction = TxMinerDefaultTest.query.filter_by(test_code=useTestCode).all()
        lenghtBrActiveProduction = len(getTxMinderBrActiveProduction)
        brActiveProduction = []
        for y in range(lenghtBrActiveProduction):
            brPendingActiveProduction = getTxMinderMvPendingSched[y].breakdown_active_production.replace(',' , '').replace('$ ','')
            brActiveProduction.insert(1, brPendingActiveProduction)
        # mvPendingSched = np.array(mvPendingSched)

        getTxMinerProviderFilterPass = TxMinerProviderTest.query.filter_by(test_code=useTestCode).filter_by(status="Pass").all()
        lengthProviderFilterPass = len(getTxMinerProviderFilterPass)
        getTxMinerProviderFilterFail = TxMinerProviderTest.query.filter_by(test_code=useTestCode).filter_by(status="Fail").all()
        lengthProviderFilterFail = len(getTxMinerProviderFilterFail)

        
        getTxMinerProcedureFilterPass = TxMinerProcedureTest.query.filter_by(test_code=useTestCode).filter_by(status="Pass").all()
        lengthProcedureFilterPass = len(getTxMinerProcedureFilterPass)
        getTxMinerProcedureFilterFail = TxMinerProcedureTest.query.filter_by(test_code=useTestCode).filter_by(status="Fail").all()
        lengthProcedureFilterFail = len(getTxMinerProcedureFilterFail)

        getTxMinerPatientFilterPass = TxMinerPatientTest.query.filter_by(test_code=useTestCode).filter_by(status="Pass").all()
        lengthPatientFilterPass = len(getTxMinerPatientFilterPass)
        getTxMinerPatientFilterFail = TxMinerPatientTest.query.filter_by(test_code=useTestCode).filter_by(status="Fail").all()
        lengthPatientFilterFail = len(getTxMinerPatientFilterFail)



        
        print(lengthPatientFilterFail)
        return render_template('Tx_Template/Tx_index.html', trigger="On",
            useTestCode=useTestCode,
            pendingSchedStatus=pendingSchedStatus,
            pendingUnschedStatus=pendingUnschedStatus,
            activeProductionStatus=activeProductionStatus,
            months=months,
            mvPendingSched=mvPendingSched,
            brPendingSched=brPendingSched,
            mvPendingUnSched=mvPendingUnSched,
            brPendingUnSched=brPendingUnSched,
            mvActiveProduction=mvActiveProduction,
            brActiveProduction=brActiveProduction,
            lengthProviderFilterPass=lengthProviderFilterPass,
            lengthProviderFilterFail=lengthProviderFilterFail,
            lengthProcedureFilterPass=lengthProcedureFilterPass,
            lengthProcedureFilterFail=lengthProcedureFilterFail,
            lengthPatientFilterPass=lengthPatientFilterPass,
            lengthPatientFilterFail=lengthPatientFilterFail,
            getTestCode=getTestCode

        )
        
    if not getDefault:
        return render_template('Tx_Template/Tx_index.html', trigger="Off")

@tx.route("/showTxPendingSchedModal/<useTestCode>")
@login_required
def showTxPendingSchedModal(useTestCode):
    fetchTxMinerPendingSched = TxMinerDefaultTest.query.filter_by(test_code=useTestCode).all()
    return render_template('Tx_Template/Modal/Pending_sched_modal.html', fetchTxMinerPendingSched=fetchTxMinerPendingSched)

@tx.route("/showTxPendingUnschedModal/<useTestCode>")
@login_required
def showTxPendingUnschedModal(useTestCode):
    fetchTxMinerPendingUnsched = TxMinerDefaultTest.query.filter_by(test_code=useTestCode).all()
    return render_template('Tx_Template/Modal/Pending_unsched_modal.html', fetchTxMinerPendingUnsched=fetchTxMinerPendingUnsched)

@tx.route("/showTxActiveProductionModal/<useTestCode>")
@login_required
def showTxActiveProductionModal(useTestCode):
    fetchTxMinerActiveProductionFilter = TxMinerDefaultTest.query.filter_by(test_code=useTestCode).all()
    return render_template('Tx_Template/Modal/Active_production_modal.html', fetchTxMinerActiveProductionFilter=fetchTxMinerActiveProductionFilter)

@tx.route("/showTxProviderFilterModal/<useTestCode>")
@login_required
def showTxProviderFilterModal(useTestCode):
    fetchTxMinerProviderFilter = TxMinerProviderTest.query.filter_by(test_code=useTestCode).all()
    return render_template('Tx_Template/Modal/Provider_filter_test.html', fetchTxMinerProviderFilter=fetchTxMinerProviderFilter)

@tx.route("/showTxProcedureFilterModal/<useTestCode>")
@login_required
def showTxProcedureFilterModal(useTestCode):
    fetchTxMinerProcedureFilter = TxMinerProcedureTest.query.filter_by(test_code=useTestCode).all()
    return render_template('Tx_Template/Modal/Procedure_filter_test.html', fetchTxMinerProcedureFilter=fetchTxMinerProcedureFilter)

@tx.route("/showTxPatientFilterModal/<useTestCode>")
@login_required
def showTxPatientFilterModal(useTestCode):
    fetchTxMinerPatientFilter = TxMinerPatientTest.query.filter_by(test_code=useTestCode).all()
    return render_template('Tx_Template/Modal/Patient_filter_modal.html', fetchTxMinerPatientFilter=fetchTxMinerPatientFilter)
        
    

@tx.route("/tx-miner-test", methods=['POST','GET'])
@login_required
def txminerTest():
    defaultTestTx = request.form.getlist('defaultTestTx[]')
    optionalTestTx = request.form.getlist('optionalTestTx[]')
    test_code =  request.form.get('test_code')


    get_test_code = TestCodes.query.filter_by(test_code=test_code).first()
    allData = Tx_selenium.login(get_test_code, optionalTestTx)

    return redirect(url_for('tx.txMiner'))