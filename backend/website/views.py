from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route('/')
def homePage():
    # html that is being run on the page
    return render_template("homepage.html")

@views.route('/sign-up/')
def sign_up():
    # html that is being run on the page
    return render_template("sign-up.html")

@views.route('/login/')
def login():
    # html that is being run on the page
    return render_template("login.html")

"""
# decorator sets this as root in website
@app.route("/")

    
    """