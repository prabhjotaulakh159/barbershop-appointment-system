""" Contains database configuration """
import os
import dotenv as env

env.load_dotenv()

host = os.environ.get('ORA_HOST')
usr = os.environ.get('ORA_USER')
SN = "pdbora19c.dawsoncollege.qc.ca"
pw = os.environ.get('ORA_PASSWD')
