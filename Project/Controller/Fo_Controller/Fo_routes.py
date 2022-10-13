from flask_login import login_required, current_user
from flask import Blueprint, render_template, url_for, request, redirect
from array import *
from ..Fo_Controller import Fo_selenium

fo = Blueprint('fo', __name__)

@fo.route("/front-office")
@login_required
def frontOffice():
    return render_template('Fo_Template/Fo_index.html')