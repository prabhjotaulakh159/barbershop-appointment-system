'''import flask and its methods'''
from flask import Blueprint, render_template
from project.qdb.database import Database

appointment = Blueprint('appointment', __name__, template_folder="templates",
                 static_folder="static")


