'''import flask and its methods'''
from flask import Blueprint, render_template
from project.qdb.database import Database

main = Blueprint('main', __name__, template_folder="templates",
                 static_folder="static")


@main.route("/")
@main.route("/home")
def home_view():
    '''function rendering for the route / and /home'''
    context_data = {"page_title": "home"}
    return render_template("home.html", context=context_data)

