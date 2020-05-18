"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

import os
from app import app, db
import datetime
from flask import render_template, request, redirect, url_for, flash, session, abort
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename

from .forms import UploadForm, LoginForm, GramForm
from .models import Users


###
# Routing for your application.
###


# Please create all new routes and view functions above this route.
# This route is now our catch all route for our VueJS single page
# application.
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    """
    Because we use HTML5 history mode in vue-router we need to configure our
    web server to redirect all routes to index.html. Hence the additional route
    "/<path:path".

    Also we will render the initial webpage and then let VueJS take control.
    """
    return render_template('index.html')


@app.route('/api/upload', methods=['POST'])
def upload():
    photoform = UploadForm()

    if request.method == 'POST':
        if photoform.validate_on_submit():
            photo = photoform.photo.data  # we could also use request.files['photo']
            description = photoform.description.data

            filename = secure_filename(photo.filename)
            photo.save(os.path.join(
                app.config['UPLOAD_FOLDER'], filename
            ))

            data = {
                "message": "File Upload Successful",
                "filename": filename,
                "description": description
            }

            return data

    return {"errors": [{"error 1": "You must fill out the description and select a photo"},
                       {"error 2": "You must fill out the description and select a photo"}]}


@app.route('/api/login', methods=['POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME'] or request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid username or password'
        else:
            session['logged_in'] = True

            flash('You were logged in', 'success')
            return 'success'
    return error


@app.route("/api/users/register", methods=['POST'])
def register():
    registerform = GramForm()

    if request.method == 'POST':
        if registerform.validate_on_submit():
            username = registerform.username.data
            password = registerform.password.data
            first_name = registerform.firstname.data
            last_name = registerform.lastname.data
            email = registerform.email.data
            location = registerform.location.data
            bio = registerform.biography.data
            photo = registerform.photo.data
            filename = secure_filename(photo.filename)
            photo.save(os.path.join(
                app.config['UPLOAD_FOLDER'], filename
            ))

            d = datetime.datetime.today()
            joined_on = d.strftime("%d-%B-%Y")

            user = Users(username=username, password=password, first_name=first_name, last_name=last_name, email=email,
                         location=location, bio=bio,
                         joined_on=joined_on, photo=filename)

            db.session.add(user)
            db.session.commit()

            users = Users.query.all()

            data = {
                "message": "File Upload Successful",
                "filename": filename,
                "description": "Have a good day"
            }

            return data

        return {"errors": [{"error 1": "Closer"},
                           {"error 2": "Not close enough"}]}

    return {"errors": [{"error 1": "You must fill out the entire form"},
                       {"error 2": "Please fill out the entire form"}]}


# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            )
            error_messages.append(message)

    return error_messages


###
# The functions below should be applicable to all Flask apps.
###


@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")
