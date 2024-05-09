""" Contains routes for all main global pages """
from flask import Blueprint, render_template
from flask_login import current_user


main = Blueprint('main', __name__, template_folder="templates", static_folder='static', static_url_path='/static/main')


@main.route("/")
def home():
    ''' Renders the homepage '''
    return render_template("home.html", current_user=current_user)

@main.route("/about")
def about():
    ''' Renders the about page'''
    return render_template("about.html")