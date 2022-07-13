from flask import Blueprint, render_template, url_for, request, redirect, flash
from flask_login import login_required, current_user
from ..Calendar_Controller import Calendar_selenium
from ...models import CalendarFilterUse
from ...models import TestCodes

cal = Blueprint('cal', __name__)

@cal.route("/calendar")
@login_required
def calendar():
    return render_template('Calendar_Template/Calendar_index.html')


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