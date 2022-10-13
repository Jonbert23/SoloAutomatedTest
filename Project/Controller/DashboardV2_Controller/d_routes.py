from flask_login import login_required, current_user
from flask import Blueprint, render_template, url_for, request, redirect
from array import *
from ..Fo_Controller import Fo_selenium

dboard = Blueprint('dboard', __name__)

@dboard.route("/dashboardv2")
@login_required
def dashboardv2():
    return render_template('DashboardV2_Template/DashboardV2_index.html')