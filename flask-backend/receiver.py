from flask import Flask 
from flask_restful import Resource, Api
from scraper import driverFunction
app=Flask(__name__)
api=Api(app)

class Contro(Resource):
	def get(self,url):
		# Here url will have the twitter url, utilise this for the rest of the code
		return {'result':driverFunction(url)}

api.add_resource(Contro,'/<string:url>')

if __name__=='__main__':
	app.run(debug=True)
