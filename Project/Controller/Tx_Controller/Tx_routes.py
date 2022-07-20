from flask import Blueprint, render_template, url_for, request, redirect
from flask_login import login_required, current_user
from ..Tx_Controller import Tx_selenium
from ...models import TestCodes

tx = Blueprint('tx', __name__)

@tx.route("/tx-miner")
@login_required
def txMiner():
    hello = "Helloooooo"
    return render_template('Tx_Template/Tx_index.html', hello=hello)

@tx.route("/tx-miner-test", methods=['POST','GET'])
@login_required
def txminerTest():
    defaultTestTx = request.form.getlist('defaultTestTx[]')
    optionalTestTx = request.form.getlist('optionalTestTx[]')
    test_code =  request.form.get('test_code')


    get_test_code = TestCodes.query.filter_by(test_code=test_code).first()
    allData = Tx_selenium.login(get_test_code, optionalTestTx)

    return redirect(url_for('tx.txMiner'))