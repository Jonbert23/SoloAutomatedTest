# from __main__ import app
from flask import Blueprint, render_template, url_for, request, redirect, flash
from flask_login import login_required, current_user
import random
import uuid
from ...models import TestCodes
from ... import db
from datetime import datetime


tcc = Blueprint('tcc', __name__)

@tcc.route("/")
@login_required
def testcode():
    test_codes = TestCodes.query.all()
    print(test_codes)
    return render_template('Testcode_Template/Testcode_index.html', name=current_user.name, test_code=test_codes)

@tcc.route("/add_testcode", methods=['POST'])
@login_required
def add_testcode():
    if request.method == 'POST':
        client_name = request.form.get('client_name')
        client_link = request.form.get('client_link')
        client_username = request.form.get('client_username')
        client_password = request.form.get('client_password')
        test_date_from = request.form.get('test_date_from')
        test_date_to = request.form.get('test_date_to')
        test_month = request.form.get('test_month')
        test_date = request.form.get('test_date')
        test_code = uuid.uuid4().hex
        user_id = current_user.id
        test_modules = "0"
        created_at = datetime.now()
        updated_at = datetime.now()

        if(test_date_from < test_date_to):
            new_test_code = TestCodes(client_name=client_name, 
                client_link=client_link,
                client_username=client_username,
                client_password=client_password,
                test_date_from=test_date_from,
                test_date_to=test_date_to,
                test_month=test_month,
                test_date=test_date,
                test_code=test_code,
                user_id=user_id,
                test_modules=test_modules,
                created_at=created_at,
                updated_at=updated_at,)

            db.session.add(new_test_code)
            db.session.commit()

            flash('Your Test Code is '+test_code, 'success')
            return redirect(url_for('tcc.testcode'))
        else:
            flash('Date-From cannot be less than Date-To', 'fail')
            return redirect(url_for('tcc.testcode'))
