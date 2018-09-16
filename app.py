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


@app.route('/api/recommender/model/create', methods=['GET'])
def create_model():
    _id = request.args.get('id')
    recommender_service.create_model(mongo, _id)
    return jsonify({"status": 200})


@app.route('/api/recommender/recommend', methods=['GET'])
def recommend():
    _id = request.args.get('id')
    user = request.args.get('user')
    k = request.args.get('k')
    recommender_service.recommend(mongo, _id, user, k)
    return jsonify({"status": 200})


if __name__ == '__main__':
    app.run(debug=True)
