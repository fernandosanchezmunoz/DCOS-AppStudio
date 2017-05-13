from flask import Flask, redirect, url_for, request
from flask.ext.pymongo import PyMongo

app = Flask(__name__)

# read application



# connect to MongoDB server
app.config['MONGO3_HOST'] = 'mongodb.marathon.l4lb.thisdcos.directory'
app.config['MONGO3_PORT'] = 28017
app.config['MONGO3_DBNAME'] = 'dbname_three'	#from APPDEF
mongo3 = PyMongo(app, config_prefix='MONGO3')
