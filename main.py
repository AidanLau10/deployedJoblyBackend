# imports from flask
from flask import redirect, render_template, request, url_for  # import render_template from "public" flask libraries
from flask_login import current_user, login_user, logout_user
from flask.cli import AppGroup

# import "objects" from "this" project
from __init__ import app, db, login_manager, cors  # Key Flask objects 

# API endpoints

from api.user import user_api 
from api.jobuser import jobuser_api
from api.job import job_api
# database Initialization functions
from model.users import User, initUsers 
from model.jobs import initJobs
from model.jobuser import initJobsUsers
from model.applications import initApplications
# server only Views

from views.projects.projects import project_views



# Initialize the SQLAlchemy object to work with the Flask app instance
db.init_app(app)

# register URIs for api endpoints

app.register_blueprint(user_api) 
app.register_blueprint(job_api)
app.register_blueprint(jobuser_api)

# register URIs for server pages
app.register_blueprint(algorithm_views) 
app.register_blueprint(recipe_views) 
app.register_blueprint(project_views) 


@app.before_request
def before_request():
    # Check if the request came from a specific origin
    allowed_origin = request.headers.get('Origin')
    if allowed_origin in ['http://127.0.0.1:4100/joblyFrontend/', 'http://localhost:4100/joblyFrontend/', 'https://aidanlau10.github.io/joblyFrontend/', 
                          'https://aidanlau10.github.io/', 'http://127.0.0.1:4100/joblyFrontend/jobs/', 'http://localhost:4100/joblyFrontend/jobs/',
                          'https://aidanlau10.github.io/joblyFrontend/jobs/', 'http://127.0.0.1:4100']:
        cors._origins = allowed_origin
        
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.context_processor
def inject_user():
    return dict(current_user=current_user)

@app.errorhandler(404)  # catch for URL not found
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

@app.route('/')  # connects default URL to index() function
def index():
    print("Home:", current_user)
    return render_template("index.html")

@app.route('/table/')  # connects /table/ URL
def table():
    return render_template("table.html")

@app.route('/login/')  # connects /table/ URL
def login_page():
    return render_template("login.html")

@app.route('/login', methods=['POST'])
def login():
    # authenticate user
    user = User.query.filter_by(_uid=request.form['username']).first()
    if user and user.is_password(request.form['password']):
        login_user(user)
        print("Logged in:", current_user)
        return redirect(url_for('index'))
    else:
        return 'Invalid username or password'
    
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# Create an AppGroup for custom commands
custom_cli = AppGroup('custom', help='Custom commands')

# Define a command to run the data generation functions
@custom_cli.command('generate_data')
def generate_data():
    initUsers()
    initJobs()
    initJobsUsers()
    initApplications()

# Register the custom command group with the Flask application
app.cli.add_command(custom_cli)
        
# this runs the flask application on the development server
if __name__ == "__main__":
    # change name for testing
    app.run(debug=True, host="0.0.0.0", port="8046")
