"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

import os
import jwt
from flask import _request_ctx_stack
from functools import wraps
import base64
from app import app, db, login_manager
import datetime
from flask import render_template, request, redirect, url_for, flash, session, abort, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash

from .forms import UploadForm, LoginForm, GramForm
from .models import Users


###
# Routing for your application.
###

# This denotes that a specific route should check for a valid JWT token
# before displaying the contents of that route 
def requires_auth(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    auth = request.headers.get('Authorization', None)
    if not auth:
      return jsonify({'code': 'authorization_header_missing', 'description': 'Authorization header is expected'}), 401

    parts = auth.split()

    if parts[0].lower() != 'bearer':
      return jsonify({'code': 'invalid_header', 'description': 'Authorization header must start with Bearer'}), 401
    elif len(parts) == 1:
      return jsonify({'code': 'invalid_header', 'description': 'Token not found'}), 401
    elif len(parts) > 2:
      return jsonify({'code': 'invalid_header', 'description': 'Authorization header must be Bearer + \s + token'}), 401

    token = parts[1]
    try:
         payload = jwt.decode(token, 'some-secret')

    except jwt.ExpiredSignature:
        return jsonify({'code': 'token_expired', 'description': 'token is expired'}), 401
    except jwt.DecodeError:
        return jsonify({'code': 'token_invalid_signature', 'description': 'Token signature is invalid'}), 401

    g.current_user = user = payload
    return f(*args, **kwargs)

  return decorated


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

            # users = Users.query.all()

            data = {
                "message": "User successfully registered",
                "filename": filename,
                "description": "Have a good day"
            }

            return jsonify(message=data), 201

        return jsonify({"errors": [{"error 1": "Closer"},
                           {"error 2": "Not close enough tho"}]})

    return jsonify({"errors": [{"error 1": "You must fill out the entire form"},
                       {"error 2": "Please fill out the entire form"}]})


@app.route("/api/auth/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST" and form.validate_on_submit():
        # change this to actually validate the entire form submission
        # and not just one field
        if form.username.data:
            # Get the username and password values from the form.
            password = form.password.data
            username = form.username.data

            user = Users.query.filter_by(username=username).first()

            if user is not None and check_password_hash(user.password, password):

                login_user(user)

                # Token generation
                payload = {'username': user.username}
                jwtToken = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')


                return jsonify({'message': "User successfully logged in"}, {'token': jwtToken}) 
    return jsonify({"message": "Try again"})


@app.route("/api/auth/logout")
@login_required
def logout():

    logout_user()
    return jsonify({"message": "The user has logged out"})


# Please create all new routes and view functions above this route.
# This route is now our catch all route for our VueJS single page
# application.
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    return render_template('index.html')


@app.route('/api/upload', methods=['POST'])
@requires_auth
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

            return jsonify(data)

    return jsonify({"errors": [{"error 1": "You must fill out the description and select a photo"},
                       {"error 2": "You must fill out the description and select a photo"}]})


@app.route("/api/posts")
@login_required
@requires_auth
def explore():

    return jsonify({"message": "Welcome to the explore pages"})



@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))


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
