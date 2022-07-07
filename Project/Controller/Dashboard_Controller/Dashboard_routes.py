from flask import Blueprint, render_template, url_for, request, redirect
from flask_login import login_required, current_user

dash = Blueprint('dash', __name__)

@dash.route("/dashboard")
def dashboard():
    return render_template('Dashboard_Template/Dashboard_index.html')
