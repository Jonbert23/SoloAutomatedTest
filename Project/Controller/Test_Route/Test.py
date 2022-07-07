from flask import Blueprint, render_template, url_for, request, redirect, flash

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
    
    message = 'Two way to run the figures matching Test '
    
    return render_template("test.html", data=data, financial=financial, dash=dash, ops=ops)
