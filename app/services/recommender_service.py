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

def create_model_v1(mongo):
    all_data = pandas.DataFrame.from_dict(Dao.mongo_data_dao().find_all(mongo))
    train_data, test_data = train_test_split(all_data, test_size=0.10, random_state=0)
    similarity_reco = Recommenders.similar_recommender()
    op = similarity_reco.create_model_v2(train_data, 'user', 'plan', ['plan', 'state'])
    Dao.mongo_model_dao().drop(mongo)
    Dao.mongo_model_dao().persist_many(mongo, loads(op.to_json(orient='records')))
    print(op)

def create_model_v2(mongo, request_json):
    all_data = pandas.DataFrame.from_dict(Dao.mongo_data_dao().find_all(mongo))
    train_data, test_data = train_test_split(all_data, test_size=0.10, random_state=0)
    similarity_reco = Recommenders.similar_recommender()
    reco_meta = Dao.mongo_reco_meta_dao().getOne(mongo, request_json['id'])
    train_data_grouped = similarity_reco.create_model_v2(train_data, reco_meta['user_field'], reco_meta['item_field'], reco_meta['features'][0]['id'])
    similarity_reco.correlate(train_data_grouped, reco_meta['user_field'], reco_meta['item_field'], reco_meta['features'][0]['id'])


def recommend_popular(mongo):
    return []

def recommend_similar(mongo):
    all_data = pandas.read_json('dataset/user_activity.json')
    train_data, test_data = train_test_split(all_data, test_size = 0.10, random_state=0)
    popularity_reco = Recommenders.popularity_recommender()
    popularity_reco.create_model(train_data, 'user', 'plan', ['plan', 'state'])
    users = test_data['user'].unique()
    return popularity_reco.recommend(users[0])


