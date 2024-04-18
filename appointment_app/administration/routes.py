'''import flask and its methods'''
from flask import Blueprint, render_template
from appointment_app.qdb.database import Database

administration = Blueprint('administration', __name__, template_folder="templates",
                 static_folder="static")

