from flask import Blueprint, render_template, url_for, request, redirect, flash
from Project.models import TestCodes
from Project.models import MhBreakdown
from Project.models import MhMain
from Project import db

test2 = Blueprint('test2', __name__)
test3 = Blueprint('test3', __name__)

@test2.route('/test')
def test():
    return "Hello World"
    

@test2.route('/testing')
def testing():
    gross = 123890
    d_gross = 123891
    financial = {
        'gross': gross,
        'net': '321,789',
        'adj': '243,765'
    }
    dash = {
        'gross': d_gross,
        'net': '234,123',
        'adj': '243,765'
    }
    ops = {
        'gross': '324,890',
        'net': '234,123',
        'adj': '243,765'
    }
    data = [financial, dash, ops]
    
    test = TestCodes.query.filter_by(test_code='c24af578ba8a4798b7bf5baaaf7711cb').first()
    test.client_password = 'Jarvis.123'
    test.client_link = 'https://solo.next.jarvisanalytics.com'
    db.session.commit()
    
     
    
    for i in range(3):
        flash('Hello fuckers!!')
    
    return render_template("test.html", data=data, financial=financial, dash=dash, ops=ops)
