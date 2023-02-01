from flask import Blueprint, render_template, url_for, request, redirect, flash
from flask_login import login_required, current_user
from ..Calendar_Controller import Calendar_selenium
from ...models import CalendarFilterUse
from ...models import TestCodes
from ...models import CalendarFilterTesting
from ...models import CalendarMetricTesting
from ...models import CalendarApptValidation
import json


cal = Blueprint('cal', __name__)

@cal.route("/calendar")
@login_required
def calendar():
    performedTest = CalendarFilterUse.query.all()
    countPerformedTest = len(performedTest)
    getLatestMetricTest = CalendarMetricTesting.query.order_by(CalendarMetricTesting.id.desc()).first()
    getAllPassApptValidation = CalendarApptValidation.query.filter_by(pts_status='Pass').all()
    getAllFailApptValidation = CalendarApptValidation.query.filter_by(pts_status='Fail').all()

    getLatestTestCodeTestedInFilterTesting = CalendarFilterTesting.query.order_by(CalendarFilterTesting.id.desc()).first()

    if getLatestTestCodeTestedInFilterTesting: 
        test_code_use = TestCodes.query.filter_by(test_code=getLatestTestCodeTestedInFilterTesting.test_code).first()
        getProviderFilterTest = CalendarFilterUse.query.filter_by(test_code=getLatestTestCodeTestedInFilterTesting.test_code).filter_by(filter_name='Provider Filter').first()
        getProcedureFilterTest = CalendarFilterUse.query.filter_by(test_code=getLatestTestCodeTestedInFilterTesting.test_code).filter_by(filter_name='Procedure Filter').first()
        getPatientFilterTest = CalendarFilterUse.query.filter_by(test_code=getLatestTestCodeTestedInFilterTesting.test_code).filter_by(filter_name='Patient Filter').first()
        getPassProviderFilterTesting = CalendarFilterTesting.query.filter_by(test_code=getLatestTestCodeTestedInFilterTesting.test_code).filter_by(filter_id=getProviderFilterTest.id).filter_by(status='Pass').all()
        countPassProviderFilterTesting = len(getPassProviderFilterTesting)
        getFailProviderFilterTesting = CalendarFilterTesting.query.filter_by(test_code=getLatestTestCodeTestedInFilterTesting.test_code).filter_by(filter_id=getProviderFilterTest.id).filter_by(status='Fail').all()
        countFailProviderFilterTesting = len(getFailProviderFilterTesting)

        getPassProcedureFilterTesting = CalendarFilterTesting.query.filter_by(test_code=getLatestTestCodeTestedInFilterTesting.test_code).filter_by(filter_id=getProcedureFilterTest.id).filter_by(status='Pass').all()
        countPassProcedureFilterTesting = len(getPassProcedureFilterTesting)
        getFailProcedureFilterTesting = CalendarFilterTesting.query.filter_by(test_code=getLatestTestCodeTestedInFilterTesting.test_code).filter_by(filter_id=getProcedureFilterTest.id).filter_by(status='Fail').all()
        countFailProcedureFilterTesting = len(getFailProcedureFilterTesting)

        getPassPatientFilterTesting = CalendarFilterTesting.query.filter_by(test_code=getLatestTestCodeTestedInFilterTesting.test_code).filter_by(filter_id=getPatientFilterTest.id).filter_by(status='Pass').all()
        countPassPatientFilterTesting = len(getPassPatientFilterTesting)
        getFailPatientFilterTesting = CalendarFilterTesting.query.filter_by(test_code=getLatestTestCodeTestedInFilterTesting.test_code).filter_by(filter_id=getPatientFilterTest.id).filter_by(status='Fail').all()
        countFailPatientFilterTesting = len(getFailPatientFilterTesting)

        testCodeLatestTestInFilterTesting = getLatestTestCodeTestedInFilterTesting.test_code
        providerFilterTest = getProviderFilterTest.id
        procedureFilterTest = getProcedureFilterTest.id
        patientFilterTest = getPatientFilterTest.id


        if countFailProviderFilterTesting == 0:
            providerStatus = 'Pass'
        else:
            providerStatus = 'Fail'

        if countFailProcedureFilterTesting == 0:
            procedureStatus = 'Pass'
        else:
            procedureStatus = 'Fail'

        if countFailPatientFilterTesting == 0:
            patientStatus = 'Pass'
        else:
            patientStatus = 'Fail'

    if not getLatestTestCodeTestedInFilterTesting:
        countPassProviderFilterTesting=0
        countFailProviderFilterTesting=0
        countPassProcedureFilterTesting=0
        countFailProcedureFilterTesting=0
        countPassPatientFilterTesting=0
        countFailPatientFilterTesting=0
        providerStatus=''
        procedureStatus=''
        patientStatus=''
        testCodeLatestTestInFilterTesting=''
        providerFilterTest=0
        procedureFilterTest=0
        patientFilterTest=0

    if not getAllPassApptValidation:
        countPassApptValidation = 0
    if not getAllFailApptValidation:
        countFailApptValidation = 0
    if getAllPassApptValidation:
        countPassApptValidation = len(getAllPassApptValidation)
    if getAllFailApptValidation:
        countFailApptValidation = len(getAllFailApptValidation)


    if not getLatestMetricTest:
        sd_sched_amount = 0
        bd_sched_amounts = 0
        bd_goal = 0
        sd_goal = 0
        bd_production = 0
        sd_production = 0
        bd_appt = 0
        sd_appt = 0
        bd_npts = 0
        sd_npts = 0
        test_code = "Null"
    if getLatestMetricTest:
        sd_sched_amount = getLatestMetricTest.sd_sched_amount.replace(',' , '').replace('$','')
        bd_sched_amounts = getLatestMetricTest.bd_sched_amount.replace(',' , '').replace('$','')
        bd_goal = getLatestMetricTest.bd_goal.replace(',' , '').replace('$','')
        sd_goal = getLatestMetricTest.sd_goal.replace(',' , '').replace('$','')
        bd_production = getLatestMetricTest.bd_production.replace(',' , '').replace('$','')
        sd_production = getLatestMetricTest.sd_production.replace(',' , '').replace('$','')
        bd_appt = getLatestMetricTest.bd_appt.replace(',' , '').replace('$','')
        sd_appt = getLatestMetricTest.sd_appt.replace(',' , '').replace('$','')
        bd_npts = getLatestMetricTest.bd_npts.replace(',' , '').replace('$','')
        sd_npts = getLatestMetricTest.sd_npts.replace(',' , '').replace('$','')

        test_code = getLatestMetricTest.test_code


    return render_template('Calendar_Template/Calendar_index.html', countPerformedTest=countPerformedTest,
        test_code_use=test_code_use,
        getLatestMetricTest=getLatestMetricTest, 
        sd_sched_amount=sd_sched_amount,
        bd_sched_amounts=bd_sched_amounts,
        bd_goal=bd_goal,
        sd_goal=sd_goal,
        bd_production=bd_production,
        sd_production=sd_production,
        bd_appt=bd_appt,
        sd_appt=sd_appt,
        bd_npts=bd_npts,
        sd_npts=sd_npts,
        test_code=test_code,
        countPassApptValidation=countPassApptValidation,
        countFailApptValidation=countFailApptValidation,
        countPassProviderFilterTesting=countPassProviderFilterTesting,
        countFailProviderFilterTesting=countFailProviderFilterTesting,
        countPassProcedureFilterTesting=countPassProcedureFilterTesting,
        countFailProcedureFilterTesting=countFailProcedureFilterTesting,
        countPassPatientFilterTesting=countPassPatientFilterTesting,
        countFailPatientFilterTesting=countFailPatientFilterTesting,
        providerStatus=providerStatus,
        procedureStatus=procedureStatus,
        patientStatus=patientStatus,
        testCodeLatestTestInFilterTesting=testCodeLatestTestInFilterTesting,
        providerFilterTest=providerFilterTest,
        procedureFilterTest=procedureFilterTest,
        patientFilterTest=patientFilterTest)


@cal.route("/calendarTest", methods=['POST','GET'])
@login_required
def calendarTest():
    optional_test = request.form.getlist('optionalTest[]')
    default_test = request.form.getlist('defaultTest[]')
    test_code =  request.form.get('test_code')

    get_test_code = TestCodes.query.filter_by(test_code=test_code).first()

    countOptionalTest = len(optional_test)

    if countOptionalTest == 0:
        flash('Please select a optional filter, thank you!.', 'info')
        return redirect(url_for('cal.calendar')) 

    countAlreadyTestFilter = 0
    listOfFilterALreadyTested = ""
    for i in range(countOptionalTest):
        getProvider = CalendarFilterUse.query.filter_by(test_code=get_test_code.test_code).filter_by(filter_name=optional_test[i]).first()
        if getProvider:
            countAlreadyTestFilter = countAlreadyTestFilter + 1
            listOfFilterALreadyTested = listOfFilterALreadyTested + ", " + optional_test[i]


    print(countAlreadyTestFilter)
    if countAlreadyTestFilter == 0:
        allData = Calendar_selenium.login(get_test_code, optional_test)
    elif countAlreadyTestFilter != 0:
        flash('This list of filter is already tested ('+listOfFilterALreadyTested+').', 'info')
        return redirect(url_for('cal.calendar'))    
    
    return redirect(url_for('cal.calendar'))

@cal.route("/showMetricTestModal/<test_code>")
@login_required
def showMetricTestModal(test_code):
    getMetricTest = CalendarMetricTesting.query.filter_by(test_code=test_code).first()
    return render_template('Calendar_Template/Modals/Figures_test_modal.html', getMetricTest=getMetricTest)

@cal.route("/showApptValidationModal/<test_code>")
@login_required
def showApptValidationModal(test_code):
    getApptValidation = CalendarApptValidation.query.filter_by(test_code=test_code).all()
    return render_template('Calendar_Template/Modals/Appt_validation_test_modal.html', getApptValidation=getApptValidation)

@cal.route("/showProviderFilterModal/<testCodeLatestTestInFilterTesting>/<providerFilterTest>")
@login_required
def showProviderFilterModal(testCodeLatestTestInFilterTesting, providerFilterTest):
    getPassProviderFilterTesting = CalendarFilterTesting.query.filter_by(test_code=testCodeLatestTestInFilterTesting).filter_by(filter_id=providerFilterTest).all()
    return render_template('Calendar_Template/Modals/Provider_filter_modal.html', getPassProviderFilterTesting=getPassProviderFilterTesting)

@cal.route("/showProcedureFilterModal/<testCodeLatestTestInFilterTesting>/<procedureFilterTest>")
@login_required
def showProcedureFilterModal(testCodeLatestTestInFilterTesting, procedureFilterTest):
    getPassProcedureFilterTesting = CalendarFilterTesting.query.filter_by(test_code=testCodeLatestTestInFilterTesting).filter_by(filter_id=procedureFilterTest).all()
    return render_template('Calendar_Template/Modals/Procedure_filter_modal.html', getPassProcedureFilterTesting=getPassProcedureFilterTesting)

@cal.route("/showPatientFilterModal/<testCodeLatestTestInFilterTesting>/<patientFilterTest>")
@login_required
def showPatientFilterModal(testCodeLatestTestInFilterTesting, patientFilterTest):
    getPassPatientFilterTesting = CalendarFilterTesting.query.filter_by(test_code=testCodeLatestTestInFilterTesting).filter_by(filter_id=patientFilterTest).all()
    return render_template('Calendar_Template/Modals/Patient_filter_modal.html', getPassPatientFilterTesting=getPassPatientFilterTesting)

@cal.route("/all_test_code")
@login_required
def all_test_code():
    getPassPatientFilterTesting = CalendarFilterUse.query.join(TestCodes, TestCodes.test_code == CalendarFilterUse.test_code).with_entities(CalendarFilterUse.test_code, TestCodes.client_name, TestCodes.client_link, TestCodes.test_date).group_by(CalendarFilterUse.test_code).all()
    print(getPassPatientFilterTesting) 
    return render_template('Calendar_Template/Modals/all_test_modal.html', getPassPatientFilterTesting=getPassPatientFilterTesting)

@cal.route("/searchCalTestCode", methods=['POST','GET'])
@login_required
def searchCalTestCode():
    test_code =  request.form.get('test_code')

    performedTest = CalendarFilterUse.query.filter_by(test_code=test_code).all()
    countPerformedTest = len(performedTest)
    getLatestMetricTest = CalendarMetricTesting.query.filter_by(test_code=test_code).order_by(CalendarMetricTesting.id.desc()).first()
    getAllPassApptValidation = CalendarApptValidation.query.filter_by(test_code=test_code).filter_by(pts_status='Pass').all()
    getAllFailApptValidation = CalendarApptValidation.query.filter_by(test_code=test_code).filter_by(pts_status='Fail').all()

    getLatestTestCodeTestedInFilterTesting = CalendarFilterTesting.query.order_by(CalendarFilterTesting.id.desc()).first()

    if getLatestTestCodeTestedInFilterTesting: 
        test_code_use = TestCodes.query.filter_by(test_code=test_code).first()
        getProviderFilterTest = CalendarFilterUse.query.filter_by(test_code=test_code).filter_by(filter_name='Provider Filter').first()
        getProcedureFilterTest = CalendarFilterUse.query.filter_by(test_code=test_code).filter_by(filter_name='Procedure Filter').first()
        getPatientFilterTest = CalendarFilterUse.query.filter_by(test_code=test_code).filter_by(filter_name='Patient Filter').first()
        getPassProviderFilterTesting = CalendarFilterTesting.query.filter_by(test_code=test_code).filter_by(filter_id=getProviderFilterTest.id).filter_by(status='Pass').all()
        countPassProviderFilterTesting = len(getPassProviderFilterTesting)
        getFailProviderFilterTesting = CalendarFilterTesting.query.filter_by(test_code=test_code).filter_by(filter_id=getProviderFilterTest.id).filter_by(status='Fail').all()
        countFailProviderFilterTesting = len(getFailProviderFilterTesting)

        getPassProcedureFilterTesting = CalendarFilterTesting.query.filter_by(test_code=test_code).filter_by(filter_id=getProcedureFilterTest.id).filter_by(status='Pass').all()
        countPassProcedureFilterTesting = len(getPassProcedureFilterTesting)
        getFailProcedureFilterTesting = CalendarFilterTesting.query.filter_by(test_code=test_code).filter_by(filter_id=getProcedureFilterTest.id).filter_by(status='Fail').all()
        countFailProcedureFilterTesting = len(getFailProcedureFilterTesting)

        getPassPatientFilterTesting = CalendarFilterTesting.query.filter_by(test_code=test_code).filter_by(filter_id=getPatientFilterTest.id).filter_by(status='Pass').all()
        countPassPatientFilterTesting = len(getPassPatientFilterTesting)
        getFailPatientFilterTesting = CalendarFilterTesting.query.filter_by(test_code=test_code).filter_by(filter_id=getPatientFilterTest.id).filter_by(status='Fail').all()
        countFailPatientFilterTesting = len(getFailPatientFilterTesting)

        testCodeLatestTestInFilterTesting = test_code
        providerFilterTest = getProviderFilterTest.id
        procedureFilterTest = getProcedureFilterTest.id
        patientFilterTest = getPatientFilterTest.id


        if countFailProviderFilterTesting == 0:
            providerStatus = 'Pass'
        else:
            providerStatus = 'Fail'

        if countFailProcedureFilterTesting == 0:
            procedureStatus = 'Pass'
        else:
            procedureStatus = 'Fail'

        if countFailPatientFilterTesting == 0:
            patientStatus = 'Pass'
        else:
            patientStatus = 'Fail'

    if not getLatestTestCodeTestedInFilterTesting:
        countPassProviderFilterTesting=0
        countFailProviderFilterTesting=0
        countPassProcedureFilterTesting=0
        countFailProcedureFilterTesting=0
        countPassPatientFilterTesting=0
        countFailPatientFilterTesting=0
        providerStatus=''
        procedureStatus=''
        patientStatus=''
        testCodeLatestTestInFilterTesting=''
        providerFilterTest=0
        procedureFilterTest=0
        patientFilterTest=0

    if not getAllPassApptValidation:
        countPassApptValidation = 0
    if not getAllFailApptValidation:
        countFailApptValidation = 0
    if getAllPassApptValidation:
        countPassApptValidation = len(getAllPassApptValidation)
    if getAllFailApptValidation:
        countFailApptValidation = len(getAllFailApptValidation)


    if not getLatestMetricTest:
        sd_sched_amount = 0
        bd_sched_amounts = 0
        bd_goal = 0
        sd_goal = 0
        bd_production = 0
        sd_production = 0
        bd_appt = 0
        sd_appt = 0
        bd_npts = 0
        sd_npts = 0
        test_code = "Null"
    if getLatestMetricTest:
        sd_sched_amount = getLatestMetricTest.sd_sched_amount.replace(',' , '').replace('$','')
        bd_sched_amounts = getLatestMetricTest.bd_sched_amount.replace(',' , '').replace('$','')
        bd_goal = getLatestMetricTest.bd_goal.replace(',' , '').replace('$','')
        sd_goal = getLatestMetricTest.sd_goal.replace(',' , '').replace('$','')
        bd_production = getLatestMetricTest.bd_production.replace(',' , '').replace('$','')
        sd_production = getLatestMetricTest.sd_production.replace(',' , '').replace('$','')
        bd_appt = getLatestMetricTest.bd_appt.replace(',' , '').replace('$','')
        sd_appt = getLatestMetricTest.sd_appt.replace(',' , '').replace('$','')
        bd_npts = getLatestMetricTest.bd_npts.replace(',' , '').replace('$','')
        sd_npts = getLatestMetricTest.sd_npts.replace(',' , '').replace('$','')

        test_code = getLatestMetricTest.test_code


    return render_template('Calendar_Template/Calendar_index.html', countPerformedTest=countPerformedTest,
        test_code_use=test_code_use,
        getLatestMetricTest=getLatestMetricTest, 
        sd_sched_amount=sd_sched_amount,
        bd_sched_amounts=bd_sched_amounts,
        bd_goal=bd_goal,
        sd_goal=sd_goal,
        bd_production=bd_production,
        sd_production=sd_production,
        bd_appt=bd_appt,
        sd_appt=sd_appt,
        bd_npts=bd_npts,
        sd_npts=sd_npts,
        test_code=test_code,
        countPassApptValidation=countPassApptValidation,
        countFailApptValidation=countFailApptValidation,
        countPassProviderFilterTesting=countPassProviderFilterTesting,
        countFailProviderFilterTesting=countFailProviderFilterTesting,
        countPassProcedureFilterTesting=countPassProcedureFilterTesting,
        countFailProcedureFilterTesting=countFailProcedureFilterTesting,
        countPassPatientFilterTesting=countPassPatientFilterTesting,
        countFailPatientFilterTesting=countFailPatientFilterTesting,
        providerStatus=providerStatus,
        procedureStatus=procedureStatus,
        patientStatus=patientStatus,
        testCodeLatestTestInFilterTesting=testCodeLatestTestInFilterTesting,
        providerFilterTest=providerFilterTest,
        procedureFilterTest=procedureFilterTest,
        patientFilterTest=patientFilterTest)

    