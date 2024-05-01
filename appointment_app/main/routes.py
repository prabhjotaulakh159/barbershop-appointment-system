'''import flask and its methods'''
from flask import Blueprint, render_template
from flask_login import current_user
main = Blueprint('main', __name__, template_folder="templates")


@main.route("/")
def home():
    ''' Renders the homepage '''
    return render_template("home.html", current_user=current_user)
