from flask import Flask, redirect, url_for, request
from pymongo import MongoClient

app = Flask(__name__)

def mongo_type_for_my_type( type ):
	"""
	Transforms the types received in the app definition for the Mongo equivalents.
	https://docs.mongodb.com/manual/reference/bson-types/
	"""

	if my_type == "String": return "string"
	if my_type == "Integer": return "int"
	if my_type == "Long": return "long"
	if my_type == "Double": return "double"
	if my_type == "Boolean": return "boolean"
	if my_type == "String": return "String"
	if ( my_type == "Date/time" or my_type == "Date/Time" ): 
		return "timestamp"  #or maybe "date"
	if my_type == "Location": return "string"

	return None

# Main Loop
############

# AppStudio: read AppDef "fields"
appdef_env = os.getenv('APPDEF', {} )
if appdef_env:
	appdef_clean = appdef_env.replace( "'", '"' )	#need double quotes
	print('**INFO: Application Definition is: {0}'.format( appdef_clean ) )
	appdef = json.loads(appdef_clean)
	appdef_fields = appdef['fields']
else:	
	appdef_clean = ""
	appdef_fields = []

#TODO: what do I need the APPDEF for in the ingester????

# connect to MongoDB server
mongo_location = os.getenv('MONGO_SERVICE','mongodb.marathon.l4lb.thisdcos.directory:27017' )
print('**DEBUG: mongo_location is {}'.format(mongo_location))
mongo_db_name = fields['path']
print('**DEBUG: mongo_db_name is {}'.format(mongo_db_name))
client = MongoClient('mongodb://'+mongo_location)
mongo_db = client[ mongo_db_name ]
collection = mongo_db.fields['path'] #the collection in mongo that will hold this app's messages

@app.route('/')
def home_page():
    return render_template('index.html', location=mongo_location)

@app.route('/data', methods = [ 'POST', 'PUT' ])
def post_to_mongo():
	if request.json:
		#initialize the values and keys
		vals = ""
		keys = ""
		#read the request and cycle through fields -- correct types
		request = json.loads(request.json)
		for req_field in request:
			print("**DEBUG: about to adapt the type {0} of field {1}".format( \
				req_field['type'],req_field['name']))
			req_field['type'] = mongo_type_for_my_type( req_field['type'] )
			print("**DEBUG: new type is {0} for field {1}".format(req_field['type'],req_field['name']))
		#post it to Mongo and catch the error
		try:
			msg_id = collection.insert_one(request).inserted_id
			print("**INFO: inserted msg with id {0} and content {1}".format( \
				msg_id, request))
	else
		print("**ERROR: empty JSON data received")
		abort(400)	#bad request

if __name__ == '__main__':
	app.run(host = ’0.0.0.0’)