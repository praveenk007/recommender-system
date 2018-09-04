import pandas
from app.algo import Recommenders
from app.dao import Dao
from bson.json_util import loads
from sklearn.model_selection import train_test_split

def visualize_data():
    all_data = pandas.read_csv('dataset/user_activity.txt')

    all_data_grouped = all_data.groupby(['plan','state']).agg({'count' : 'count'}).reset_index()
    gropued_count = all_data_grouped['count'].sum()
    print(gropued_count)
    all_data_grouped['percentage'] = all_data_grouped['count'].div(gropued_count) * 100


    print(all_data_grouped)

def create_model(mongo):
    all_data = pandas.DataFrame.from_dict(Dao.mongo_data_dao().find_all(mongo))
    train_data, test_data = train_test_split(all_data, test_size=0.10, random_state=0)
    popularity_reco = Recommenders.similar_recommender()
    op = popularity_reco.create_model(train_data, 'user', 'plan', ['user', 'plan', 'state'])
    Dao.mongo_model_dao().drop(mongo)
    Dao.mongo_model_dao().persist_many(mongo, loads(op.to_json(orient='records')))
    print('===== Inserted ====')
    print(op)

def recommend_popular(mongo):
    return []

def recommend_similar(mongo):
    all_data = pandas.read_json('dataset/user_activity.json')
    train_data, test_data = train_test_split(all_data, test_size = 0.10, random_state=0)
    popularity_reco = Recommenders.popularity_recommender()
    popularity_reco.create_model(train_data, 'user', 'plan', ['plan', 'state'])
    users = test_data['user'].unique()
    return popularity_reco.recommend(users[0])


