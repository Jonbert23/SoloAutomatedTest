from flask_login import login_required, current_user
from flask import Blueprint, render_template, url_for, request, redirect
from array import *
from ..DashboardV2_Controller import d_selenium
from ...models import TestCodes
from ...models import DashboardV2DefaultBreakdownTest
from ...models import DashboardV2DefaultProductionTest
from ...models import DashboardV2DefaultSearchProcedure
from ...models import DashboardV2DefaultLOBTest 
from ...models import DashboardV2DefaultCountTest

dboard = Blueprint('dboard', __name__)

@dboard.route("/dashboardv2")
@login_required
def dashboardv2():

    getDefault = DashboardV2DefaultBreakdownTest.query.order_by(DashboardV2DefaultBreakdownTest.id.desc()).first()

    if getDefault:
        getTheLatestTestCode = DashboardV2DefaultBreakdownTest.query.order_by(DashboardV2DefaultBreakdownTest.id.desc()).first()
        useTestCode = getTheLatestTestCode.test_code
        getTestCodeInfo = TestCodes.query.filter_by(test_code=useTestCode).first()

        getBreakdown = DashboardV2DefaultBreakdownTest.query.filter_by(test_code=useTestCode).order_by(DashboardV2DefaultBreakdownTest.id.desc()).all()
        
        getNetProduction = DashboardV2DefaultBreakdownTest.query.filter_by(test_code=useTestCode).filter_by(main_view_label="Net Production").first()
        getMainNetProductionValue = getNetProduction.main_view_value.replace(',' , '').replace('$ ','')
        getBreakdownNetProductionValue = getNetProduction.breakdown_view_value.replace(',' , '').replace('$ ','')

        getGrossProduction = DashboardV2DefaultBreakdownTest.query.filter_by(test_code=useTestCode).filter_by(main_view_label="Gross Production").first()
        getMainGrossProductionValue = getGrossProduction.main_view_value.replace(',' , '').replace('$ ','')
        getBreakdownGrossProductionValue = getGrossProduction.breakdown_view_value.replace(',' , '').replace('$ ','')

        getCollection = DashboardV2DefaultBreakdownTest.query.filter_by(test_code=useTestCode).filter_by(main_view_label="Collection").first()
        getMainCollectionValue = getCollection.main_view_value.replace(',' , '').replace('$ ','')
        getBreakdownCollectionValue = getCollection.breakdown_view_value.replace(',' , '').replace('$ ','')

        getAdjustment = DashboardV2DefaultBreakdownTest.query.filter_by(test_code=useTestCode).filter_by(main_view_label="Adjustment").first()
        getMainAdjustmentValue = getAdjustment.main_view_value.replace(',' , '').replace('$ ','')
        getBreakdownAdjustmentValue = getAdjustment.breakdown_view_value.replace(',' , '').replace('$ ','')

        getNpt = DashboardV2DefaultBreakdownTest.query.filter_by(test_code=useTestCode).filter_by(main_view_label="New Patients Visits").first()
        getMainNptValue = getNpt.main_view_value.replace(',' , '').replace('$ ','')
        getBreakdownNptValue = getNpt.breakdown_view_value.replace(',' , '').replace('$ ','')

        getEnpt = DashboardV2DefaultBreakdownTest.query.filter_by(test_code=useTestCode).filter_by(main_view_label="Existing Patients Visits").first()
        getMainEnptValue = getEnpt.main_view_value.replace(',' , '').replace('$ ','')
        getBreakdownEnptValue = getEnpt.breakdown_view_value.replace(',' , '').replace('$ ','')
       

        getProductionTest = DashboardV2DefaultProductionTest.query.filter_by(test_code=useTestCode).first()
        baseValue = getProductionTest.base_value.replace(',' , '').replace('$ ','')
        providerValue = getProductionTest.production_by_provider.replace(',' , '').replace('$ ','')
        tableValue = getProductionTest.table_production.replace(',' , '').replace('$ ','')
        payorsValue = getProductionTest.payors_production.replace(',' , '').replace('$ ','')

        providerStatus = ""
        tableStatus = ""
        payorsStatus = ""

        if baseValue == providerValue:
            providerStatus = "Pass"
        else:
            providerStatus = "Fail"

        if baseValue == tableValue:
            tableStatus = "Pass"
        else:
            tableStatus = "Fail"

        if baseValue == payorsValue:
            payorsStatus = "Pass"
        else:
            payorsStatus = "Fail"

        getSearchTest = DashboardV2DefaultSearchProcedure.query.filter_by(test_code=useTestCode).all()
        pendingSearchStatus = ""

        for getSearchTest in getSearchTest:
            if getSearchTest.status == 'Fail':
                pendingSearchStatus = "Fail"
                break
            else:
                pendingSearchStatus = "Pass"

        getCountTest = DashboardV2DefaultCountTest.query.filter_by(test_code=useTestCode).all()
        pendingCountStatus = ""

        for getCountTest in getCountTest:
            if getCountTest.status == 'Fail':
                pendingCountStatus = "Fail"
                break
            else:
                pendingCountStatus = "Pass"

        getSearchPassTest = DashboardV2DefaultSearchProcedure.query.filter_by(test_code=useTestCode).filter_by(status="Pass").all()
        countPassSearchTest = len(getSearchPassTest)
        getSearchFailTest = DashboardV2DefaultSearchProcedure.query.filter_by(test_code=useTestCode).filter_by(status="Fail").all()
        countFailSearchTest = len(getSearchFailTest)

        getCountPassTest = DashboardV2DefaultCountTest.query.filter_by(test_code=useTestCode).filter_by(status="Pass").all()
        countPassCountTest = len(getCountPassTest)
        getCountFailTest = DashboardV2DefaultCountTest.query.filter_by(test_code=useTestCode).filter_by(status="Fail").all()
        countFailCountTest = len(getCountFailTest)

        #LOB OPTIONS QUERY
        #DOCTOR
        getDoctor = DashboardV2DefaultLOBTest.query.filter_by(test_code=useTestCode).filter_by(lob_options="Doctor").all()
        doctorStatus = ""

        for getDoctor in getDoctor:
            if getDoctor.status == 'Fail':
                doctorStatus = "Fail"
                break
            else:
                doctorStatus = "Pass"
        #ORAL SURGERY
        getOralSurgery = DashboardV2DefaultLOBTest.query.filter_by(test_code=useTestCode).filter_by(lob_options="Oral Surgery").all()
        oralSurgeryStatus = ""

        for getOralSurgery in getOralSurgery:
            if getOralSurgery.status == 'Fail':
                oralSurgeryStatus = "Fail"
                break
            else:
                oralSurgeryStatus = "Pass"
        # PERIO
        getPerio = DashboardV2DefaultLOBTest.query.filter_by(test_code=useTestCode).filter_by(lob_options="Oral Surgery").all()
        perioStatus = ""

        for getPerio in getPerio:
            if getPerio.status == 'Fail':
                perioStatus = "Fail"
                break
            else:
                perioStatus = "Pass"
        # ENDO
        getEndo = DashboardV2DefaultLOBTest.query.filter_by(test_code=useTestCode).filter_by(lob_options="Endo").all()
        endoStatus = ""

        for getEndo in getEndo:
            if getEndo.status == 'Fail':
                endoStatus = "Fail"
                break
            else:
                endoStatus = "Pass"
        # ORTHO
        getOrtho = DashboardV2DefaultLOBTest.query.filter_by(test_code=useTestCode).filter_by(lob_options="Ortho").all()
        orthoStatus = ""

        for getOrtho in getOrtho:
            if getOrtho.status == 'Fail':
                orthoStatus = "Fail"
                break
            else:
                orthoStatus = "Pass"
        # PROSTHE
        getProsthe = DashboardV2DefaultLOBTest.query.filter_by(test_code=useTestCode).filter_by(lob_options="Prosthe").all()
        prostheStatus = ""

        for getProsthe in getProsthe:
            if getProsthe.status == 'Fail':
                prostheStatus = "Fail"
                break
            else:
                prostheStatus = "Pass"

        # HYGIENE
        getHygiene = DashboardV2DefaultLOBTest.query.filter_by(test_code=useTestCode).filter_by(lob_options="Hygiene").all()
        hygieneStatus = ""

        for getHygiene in getHygiene:
            if getHygiene.status == 'Fail':
                hygieneStatus = "Fail"
                break
            else:
                hygieneStatus = "Pass"

        # PEDO
        getPedo = DashboardV2DefaultLOBTest.query.filter_by(test_code=useTestCode).filter_by(lob_options="Pedo").all()
        pedoStatus = ""

        for getPedo in getPedo:
            if getPedo.status == 'Fail':
                pedoStatus = "Fail"
                break
            else:
                pedoStatus = "Pass"

        # OTHERS
        getOthers = DashboardV2DefaultLOBTest.query.filter_by(test_code=useTestCode).filter_by(lob_options="Others").all()
        othersStatus = ""

        for getOthers in getOthers:
            if getOthers.status == 'Fail':
                othersStatus = "Fail"
                break
            else:
                othersStatus = "Pass"

        # INVISALIGN
        getInvisalign = DashboardV2DefaultLOBTest.query.filter_by(test_code=useTestCode).filter_by(lob_options="Invisalign").all()
        invisalignStatus = ""

        for getInvisalign in getInvisalign:
            if getInvisalign.status == 'Fail':
                invisalignStatus = "Fail"
                break
            else:
                invisalignStatus = "Pass"

        getAllPassLob = DashboardV2DefaultLOBTest.query.filter_by(test_code=useTestCode).filter_by(status="Pass").all()
        countPassLob = len(getAllPassLob)
        getAllFailLob = DashboardV2DefaultLOBTest.query.filter_by(test_code=useTestCode).filter_by(status="Fail").all()
        countFailLob = len(getAllFailLob)

        print(countFailLob)
        
        return render_template('DashboardV2_Template/DashboardV2_index.html', trigger="On",
            getBreakdown=getBreakdown,
            getMainNetProductionValue=getMainNetProductionValue,
            getBreakdownNetProductionValue=getBreakdownNetProductionValue,
            getMainGrossProductionValue=getMainGrossProductionValue,
            getBreakdownGrossProductionValue=getBreakdownGrossProductionValue,
            getMainCollectionValue=getMainCollectionValue,
            getBreakdownCollectionValue=getBreakdownCollectionValue,
            getMainAdjustmentValue=getMainAdjustmentValue,
            getBreakdownAdjustmentValue=getBreakdownAdjustmentValue,
            getMainNptValue=getMainNptValue,
            getBreakdownNptValue=getBreakdownNptValue,
            getMainEnptValue=getMainEnptValue,
            getBreakdownEnptValue=getBreakdownEnptValue,
            baseValue=baseValue,
            providerValue=providerValue,
            tableValue=tableValue,
            payorsValue=payorsValue,
            providerStatus=providerStatus,
            tableStatus=tableStatus,
            payorsStatus=payorsStatus,
            pendingSearchStatus=pendingSearchStatus,
            pendingCountStatus=pendingCountStatus,
            countPassSearchTest=countPassSearchTest,
            countFailSearchTest=countFailSearchTest,
            countPassCountTest=countPassCountTest,
            countFailCountTest=countFailCountTest,
            useTestCode=useTestCode,
            doctorStatus=doctorStatus,
            oralSurgeryStatus=oralSurgeryStatus,
            perioStatus=perioStatus,
            endoStatus=endoStatus,
            orthoStatus=orthoStatus,
            prostheStatus=prostheStatus,
            hygieneStatus=hygieneStatus,
            pedoStatus=pedoStatus,
            othersStatus=othersStatus,
            invisalignStatus=invisalignStatus,
            countPassLob=countPassLob,
            countFailLob=countFailLob,
            getTestCodeInfo=getTestCodeInfo,


        )
    
    if not getDefault:
        return render_template('DashboardV2_Template/DashboardV2_index.html', trigger="Off")

    
@dboard.route("/dashboardV2-test", methods=['POST','GET'])
@login_required
def dashTest():
    defaultTestDash = request.form.getlist('defaultTestDash[]')
    optionalTestDash = request.form.getlist('optionalTestDash[]')
    test_code =  request.form.get('test_code')

    # print(defaultTestDash)
    # print(optionalTestDash)
    # print(test_code)
    get_test_code = TestCodes.query.filter_by(test_code=test_code).first()
    allData = d_selenium.login(get_test_code, optionalTestDash)

    return redirect(url_for('dboard.dashboardv2'))

@dboard.route("/dash-breakdown/<useTestCode>")
@login_required
def dashBreakdown(useTestCode):
    getBreakdown = DashboardV2DefaultBreakdownTest.query.filter_by(test_code=useTestCode).order_by(DashboardV2DefaultBreakdownTest.id.desc()).all()
    return render_template('DashboardV2_Template/Modals/Breakdown_test_modal.html', getBreakdown=getBreakdown)

@dboard.route("/dash-production/<useTestCode>")
@login_required
def productionFigures(useTestCode):
    getProductionTest = DashboardV2DefaultProductionTest.query.filter_by(test_code=useTestCode).first()
    return render_template('DashboardV2_Template/Modals/Production_figures_test_modal.html', getProductionTest=getProductionTest)

@dboard.route("/dash-search-procedure/<useTestCode>")
@login_required
def searchProc(useTestCode):
    getSearchProcedure = DashboardV2DefaultSearchProcedure.query.filter_by(test_code=useTestCode).all()
    return render_template('DashboardV2_Template/Modals/Search_prosedure_modal.html', getSearchProcedure=getSearchProcedure)

@dboard.route("/dash-count-procedure/<useTestCode>")
@login_required
def countProc(useTestCode):
    getCountProcedure = DashboardV2DefaultCountTest.query.filter_by(test_code=useTestCode).all()
    return render_template('DashboardV2_Template/Modals/Count_breakdown_modal.html', getCountProcedure=getCountProcedure)

@dboard.route("/dash-lob-filter/<useTestCode>/<lobFilter>")
@login_required
def lobFilterBrkdwn(useTestCode, lobFilter):
    getLob = DashboardV2DefaultLOBTest.query.filter_by(test_code=useTestCode).filter_by(lob_options=lobFilter).all()
    return render_template('DashboardV2_Template/Modals/Lob_modal.html', getLob=getLob, lobFilter=lobFilter)


@dboard.route("/dash_test_code")
@login_required
def dashAllTestCode():
    getPassPatientFilterTesting = DashboardV2DefaultBreakdownTest.query.join(TestCodes, TestCodes.test_code == DashboardV2DefaultBreakdownTest.test_code).with_entities(DashboardV2DefaultBreakdownTest.test_code, TestCodes.client_name, TestCodes.client_link, TestCodes.test_date).group_by(DashboardV2DefaultBreakdownTest.test_code).all()
    print(getPassPatientFilterTesting) 
    return render_template('DashboardV2_Template/Modals/dash_all_test_modal.html', getPassPatientFilterTesting=getPassPatientFilterTesting)

@dboard.route("/search-dash-test", methods=['POST','GET'])
@login_required
def searchDashTestCode():
    test_code =  request.form.get('test_code')
    # getTheLatestTestCode = DashboardV2DefaultBreakdownTest.query.order_by(DashboardV2DefaultBreakdownTest.id.desc()).first()
    useTestCode = test_code
    getTestCodeInfo = TestCodes.query.filter_by(test_code=useTestCode).first()

    getBreakdown = DashboardV2DefaultBreakdownTest.query.filter_by(test_code=useTestCode).order_by(DashboardV2DefaultBreakdownTest.id.desc()).all()
    
    getNetProduction = DashboardV2DefaultBreakdownTest.query.filter_by(test_code=useTestCode).filter_by(main_view_label="Net Production").first()
    getMainNetProductionValue = getNetProduction.main_view_value.replace(',' , '').replace('$ ','')
    getBreakdownNetProductionValue = getNetProduction.breakdown_view_value.replace(',' , '').replace('$ ','')

    getGrossProduction = DashboardV2DefaultBreakdownTest.query.filter_by(test_code=useTestCode).filter_by(main_view_label="Gross Production").first()
    getMainGrossProductionValue = getGrossProduction.main_view_value.replace(',' , '').replace('$ ','')
    getBreakdownGrossProductionValue = getGrossProduction.breakdown_view_value.replace(',' , '').replace('$ ','')

    getCollection = DashboardV2DefaultBreakdownTest.query.filter_by(test_code=useTestCode).filter_by(main_view_label="Collection").first()
    getMainCollectionValue = getCollection.main_view_value.replace(',' , '').replace('$ ','')
    getBreakdownCollectionValue = getCollection.breakdown_view_value.replace(',' , '').replace('$ ','')

    getAdjustment = DashboardV2DefaultBreakdownTest.query.filter_by(test_code=useTestCode).filter_by(main_view_label="Adjustment").first()
    getMainAdjustmentValue = getAdjustment.main_view_value.replace(',' , '').replace('$ ','')
    getBreakdownAdjustmentValue = getAdjustment.breakdown_view_value.replace(',' , '').replace('$ ','')

    getNpt = DashboardV2DefaultBreakdownTest.query.filter_by(test_code=useTestCode).filter_by(main_view_label="New Patients Visits").first()
    getMainNptValue = getNpt.main_view_value.replace(',' , '').replace('$ ','')
    getBreakdownNptValue = getNpt.breakdown_view_value.replace(',' , '').replace('$ ','')

    getEnpt = DashboardV2DefaultBreakdownTest.query.filter_by(test_code=useTestCode).filter_by(main_view_label="Existing Patients Visits").first()
    getMainEnptValue = getEnpt.main_view_value.replace(',' , '').replace('$ ','')
    getBreakdownEnptValue = getEnpt.breakdown_view_value.replace(',' , '').replace('$ ','')
    

    getProductionTest = DashboardV2DefaultProductionTest.query.filter_by(test_code=useTestCode).first()
    baseValue = getProductionTest.base_value.replace(',' , '').replace('$ ','')
    providerValue = getProductionTest.production_by_provider.replace(',' , '').replace('$ ','')
    tableValue = getProductionTest.table_production.replace(',' , '').replace('$ ','')
    payorsValue = getProductionTest.payors_production.replace(',' , '').replace('$ ','')

    providerStatus = ""
    tableStatus = ""
    payorsStatus = ""

    if baseValue == providerValue:
        providerStatus = "Pass"
    else:
        providerStatus = "Fail"

    if baseValue == tableValue:
        tableStatus = "Pass"
    else:
        tableStatus = "Fail"

    if baseValue == payorsValue:
        payorsStatus = "Pass"
    else:
        payorsStatus = "Fail"

    getSearchTest = DashboardV2DefaultSearchProcedure.query.filter_by(test_code=useTestCode).all()
    pendingSearchStatus = ""

    for getSearchTest in getSearchTest:
        if getSearchTest.status == 'Fail':
            pendingSearchStatus = "Fail"
            break
        else:
            pendingSearchStatus = "Pass"

    getCountTest = DashboardV2DefaultCountTest.query.filter_by(test_code=useTestCode).all()
    pendingCountStatus = ""

    for getCountTest in getCountTest:
        if getCountTest.status == 'Fail':
            pendingCountStatus = "Fail"
            break
        else:
            pendingCountStatus = "Pass"

    getSearchPassTest = DashboardV2DefaultSearchProcedure.query.filter_by(test_code=useTestCode).filter_by(status="Pass").all()
    countPassSearchTest = len(getSearchPassTest)
    getSearchFailTest = DashboardV2DefaultSearchProcedure.query.filter_by(test_code=useTestCode).filter_by(status="Fail").all()
    countFailSearchTest = len(getSearchFailTest)

    getCountPassTest = DashboardV2DefaultCountTest.query.filter_by(test_code=useTestCode).filter_by(status="Pass").all()
    countPassCountTest = len(getCountPassTest)
    getCountFailTest = DashboardV2DefaultCountTest.query.filter_by(test_code=useTestCode).filter_by(status="Fail").all()
    countFailCountTest = len(getCountFailTest)

    #LOB OPTIONS QUERY
    #DOCTOR
    getDoctor = DashboardV2DefaultLOBTest.query.filter_by(test_code=useTestCode).filter_by(lob_options="Doctor").all()
    doctorStatus = ""

    for getDoctor in getDoctor:
        if getDoctor.status == 'Fail':
            doctorStatus = "Fail"
            break
        else:
            doctorStatus = "Pass"
    #ORAL SURGERY
    getOralSurgery = DashboardV2DefaultLOBTest.query.filter_by(test_code=useTestCode).filter_by(lob_options="Oral Surgery").all()
    oralSurgeryStatus = ""

    for getOralSurgery in getOralSurgery:
        if getOralSurgery.status == 'Fail':
            oralSurgeryStatus = "Fail"
            break
        else:
            oralSurgeryStatus = "Pass"
    # PERIO
    getPerio = DashboardV2DefaultLOBTest.query.filter_by(test_code=useTestCode).filter_by(lob_options="Oral Surgery").all()
    perioStatus = ""

    for getPerio in getPerio:
        if getPerio.status == 'Fail':
            perioStatus = "Fail"
            break
        else:
            perioStatus = "Pass"
    # ENDO
    getEndo = DashboardV2DefaultLOBTest.query.filter_by(test_code=useTestCode).filter_by(lob_options="Endo").all()
    endoStatus = ""

    for getEndo in getEndo:
        if getEndo.status == 'Fail':
            endoStatus = "Fail"
            break
        else:
            endoStatus = "Pass"
    # ORTHO
    getOrtho = DashboardV2DefaultLOBTest.query.filter_by(test_code=useTestCode).filter_by(lob_options="Ortho").all()
    orthoStatus = ""

    for getOrtho in getOrtho:
        if getOrtho.status == 'Fail':
            orthoStatus = "Fail"
            break
        else:
            orthoStatus = "Pass"
    # PROSTHE
    getProsthe = DashboardV2DefaultLOBTest.query.filter_by(test_code=useTestCode).filter_by(lob_options="Prosthe").all()
    prostheStatus = ""

    for getProsthe in getProsthe:
        if getProsthe.status == 'Fail':
            prostheStatus = "Fail"
            break
        else:
            prostheStatus = "Pass"

    # HYGIENE
    getHygiene = DashboardV2DefaultLOBTest.query.filter_by(test_code=useTestCode).filter_by(lob_options="Hygiene").all()
    hygieneStatus = ""

    for getHygiene in getHygiene:
        if getHygiene.status == 'Fail':
            hygieneStatus = "Fail"
            break
        else:
            hygieneStatus = "Pass"

    # PEDO
    getPedo = DashboardV2DefaultLOBTest.query.filter_by(test_code=useTestCode).filter_by(lob_options="Pedo").all()
    pedoStatus = ""

    for getPedo in getPedo:
        if getPedo.status == 'Fail':
            pedoStatus = "Fail"
            break
        else:
            pedoStatus = "Pass"

    # OTHERS
    getOthers = DashboardV2DefaultLOBTest.query.filter_by(test_code=useTestCode).filter_by(lob_options="Others").all()
    othersStatus = ""

    for getOthers in getOthers:
        if getOthers.status == 'Fail':
            othersStatus = "Fail"
            break
        else:
            othersStatus = "Pass"

    # INVISALIGN
    getInvisalign = DashboardV2DefaultLOBTest.query.filter_by(test_code=useTestCode).filter_by(lob_options="Invisalign").all()
    invisalignStatus = ""

    for getInvisalign in getInvisalign:
        if getInvisalign.status == 'Fail':
            invisalignStatus = "Fail"
            break
        else:
            invisalignStatus = "Pass"

    getAllPassLob = DashboardV2DefaultLOBTest.query.filter_by(test_code=useTestCode).filter_by(status="Pass").all()
    countPassLob = len(getAllPassLob)
    getAllFailLob = DashboardV2DefaultLOBTest.query.filter_by(test_code=useTestCode).filter_by(status="Fail").all()
    countFailLob = len(getAllFailLob)

    print(countFailLob)
    
    return render_template('DashboardV2_Template/DashboardV2_index.html', trigger="On",
        getBreakdown=getBreakdown,
        getMainNetProductionValue=getMainNetProductionValue,
        getBreakdownNetProductionValue=getBreakdownNetProductionValue,
        getMainGrossProductionValue=getMainGrossProductionValue,
        getBreakdownGrossProductionValue=getBreakdownGrossProductionValue,
        getMainCollectionValue=getMainCollectionValue,
        getBreakdownCollectionValue=getBreakdownCollectionValue,
        getMainAdjustmentValue=getMainAdjustmentValue,
        getBreakdownAdjustmentValue=getBreakdownAdjustmentValue,
        getMainNptValue=getMainNptValue,
        getBreakdownNptValue=getBreakdownNptValue,
        getMainEnptValue=getMainEnptValue,
        getBreakdownEnptValue=getBreakdownEnptValue,
        baseValue=baseValue,
        providerValue=providerValue,
        tableValue=tableValue,
        payorsValue=payorsValue,
        providerStatus=providerStatus,
        tableStatus=tableStatus,
        payorsStatus=payorsStatus,
        pendingSearchStatus=pendingSearchStatus,
        pendingCountStatus=pendingCountStatus,
        countPassSearchTest=countPassSearchTest,
        countFailSearchTest=countFailSearchTest,
        countPassCountTest=countPassCountTest,
        countFailCountTest=countFailCountTest,
        useTestCode=useTestCode,
        doctorStatus=doctorStatus,
        oralSurgeryStatus=oralSurgeryStatus,
        perioStatus=perioStatus,
        endoStatus=endoStatus,
        orthoStatus=orthoStatus,
        prostheStatus=prostheStatus,
        hygieneStatus=hygieneStatus,
        pedoStatus=pedoStatus,
        othersStatus=othersStatus,
        invisalignStatus=invisalignStatus,
        countPassLob=countPassLob,
        countFailLob=countFailLob,
        getTestCodeInfo=getTestCodeInfo,
        

    )
    return test_code