from flask import Flask, jsonify, request
from app.services import recommender_service
import ConfigParser
from flask_pymongo import PyMongo

app = Flask(__name__)

config = ConfigParser.ConfigParser()
config.read('app/configs/local.env')


app.config['MONGO_DBNAME'] = config.get('MONGO', 'db.db')
app.config['MONGO_URI'] = config.get('MONGO', 'db.uri')

mongo = PyMongo(app)

@app.route('/api/recommender/test', methods=['GET'])
def test1():
    op = recommender_service.recommend_popular(mongo)
    return op.to_json(orient='records')

@app.route('/api/recommender/model/create', methods=['POST'])
def create_model():
    request_json = request.get_json()
    recommender_service.create_model_v2(mongo, request_json)
    return jsonify({"status" : 200})


if __name__ == '__main__':
    app.run(debug=True)