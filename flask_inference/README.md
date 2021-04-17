This folder contains the files related to inference i.e. the files needed to predict a tweet. 

- `inference.pynb`: This notebook is used predict if a tweet is controversial or not from a pretrained model. A tweet like object consists of a root tweet and a list of comments
- `flask_inference.py`: This files consists of the flask app which is used to create the REST API. This file exposes a REST API at port 3000(if it is not occupied already). For exposing it out of local machine, you can use ngrok,
