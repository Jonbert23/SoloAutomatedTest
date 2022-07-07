from flask import Blueprint, render_template, url_for, request, redirect
from flask_login import login_required, current_user

tx = Blueprint('tx', __name__)

@tx.route("/tx-miner")
@login_required
def txMiner():
    return render_template('Tx_Template/Tx_index.html')