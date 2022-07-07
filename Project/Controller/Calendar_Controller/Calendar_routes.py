from flask import Blueprint, render_template, url_for, request, redirect
from flask_login import login_required, current_user
from ..Calendar_Controller import Calendar_selenium
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

    allData = Calendar_selenium.login(get_test_code, optional_test)
    
    
    return render_template('Calendar_Template/Calendar_index.html')