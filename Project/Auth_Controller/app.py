from flask import Blueprint, render_template, url_for, request, redirect
from flask_login import login_required, current_user
from .. import db

app = Blueprint('app', __name__)

# @app.route("/")
# @login_required
# def testcode():
#     return render_template('Testcode_Template/Testcode_index.html')

# @app.route("/calendar")
# @login_required
# def calendar():
#     return render_template('Calendar_Template/Calendar_index.html')

# @app.route("/dashboard")
# @login_required
# def dashboard():
#     return render_template('Dashboard_Template/Dashboard_index.html')


# from project.Testcode_Controller.Testcode_routes import Testcode_routes
# from project.Calendar_Controller.Calendar_routes import Calendar_routes
# from project.Dashboard_Controller.Dashboard_routes import Dashboard_routes

# import project.Testcode_Controller.Testcode_routes
# import project.Calendar_Controller.Calendar_routes
# import project.Dashboard_Controller.Dashboard_routes

# @app.route('/')
# @login_required
# def index():
#     return render_template('index.html', name=current_user.name)



# @app.route('/figuresmatching', methods=['POST', 'GET'])
# @login_required
# def figuresMatching():
#     modules = request.form.getlist('modules[]')
#     metrics = request.form.getlist('metrics[]')
#     allData = figuresmatchingmain.login(modules, metrics)

#     return render_template('index.html', allData=allData) 