from flask_login import login_required, current_user
from flask import Blueprint, render_template, url_for, request, redirect
from array import *
from ..Fo_Controller import Fo_selenium
from ...models import TestCodes
from ...models import FrontOfficeKpisTest

fo = Blueprint('fo', __name__)

@fo.route("/front-office")
@login_required
def frontOffice():
    getDefault = FrontOfficeKpisTest.query.order_by(FrontOfficeKpisTest.id.desc()).first()

    if getDefault:
        getTheLatestTestCode = FrontOfficeKpisTest.query.order_by(FrontOfficeKpisTest.id.desc()).first()
        useTestCode = getTheLatestTestCode.test_code

        getTestCode = TestCodes.query.filter_by(test_code=useTestCode).first()

        getAllKpisTestInTestCode = FrontOfficeKpisTest.query.filter_by(test_code=useTestCode).all()
        
        getPassBreakdownTest = FrontOfficeKpisTest.query.filter_by(test_code=useTestCode).filter_by(match_brkdwn_status="Pass").all()
        countPassBreakdownTest = len(getPassBreakdownTest)

        getFailBreakdownTest = FrontOfficeKpisTest.query.filter_by(test_code=useTestCode).filter_by(match_brkdwn_status="Fail").all()
        countFailBreakdownTest = len(getFailBreakdownTest)

        getPassCalculationTest = FrontOfficeKpisTest.query.filter_by(test_code=useTestCode).filter_by(cal_status="Pass").all()
        countPassCalculationTest = len(getPassCalculationTest)

        getFailCalculationTest = FrontOfficeKpisTest.query.filter_by(test_code=useTestCode).filter_by(cal_status="Fail").all()
        countFailCalculationTest = len(getFailCalculationTest)


        return render_template('Fo_Template/Fo_index.html', trigger="On",
            countPassBreakdownTest=countPassBreakdownTest,
            countFailBreakdownTest=countFailBreakdownTest,
            countPassCalculationTest=countPassCalculationTest,
            countFailCalculationTest=countFailCalculationTest,
            getAllKpisTestInTestCode=getAllKpisTestInTestCode,
            getTestCode=getTestCode

        )
    if not getDefault:
        return render_template('Fo_Template/Fo_index.html', trigger="Off")

@fo.route("/front-office-test", methods=['POST','GET'])
@login_required
def foTest():
    test_code =  request.form.get('test_code')
    # print(test_code)

    get_test_code = TestCodes.query.filter_by(test_code=test_code).first()
    print(get_test_code)
    allData = Fo_selenium.login(get_test_code)

    return redirect(url_for('fo.frontOffice'))