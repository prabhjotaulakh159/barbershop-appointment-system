'''import flask and its methods'''
from flask import Blueprint, render_template
from project.qdb.database import Database

user = Blueprint('user', __name__, template_folder="templates",
                 static_folder="static")
