'''import flask and its methods'''
from flask import Blueprint, render_template
from project.qdb.database import Database

report = Blueprint('report', __name__, template_folder="templates",
                 static_folder="static")
