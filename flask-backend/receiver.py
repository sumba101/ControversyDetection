from flask import Flask 
from flask_restful import Resource, Api
app=Flask(__name__)
api=Api(app)

class Contro(Resource):
	def get(self,url):
		# Here url will have the twitter url, utilise this for the rest of the code
		print(url)
		return {'result':'hello'+url}

api.add_resource(Contro,'/<string:url>')

if __name__=='__main__':
	app.run(debug=True)
