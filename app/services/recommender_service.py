import pandas
from app.dao import HDF5Dao
from app.algo import Recommenders

from app.dao import Dao
from bson.json_util import loads
from sklearn.model_selection import train_test_split


def visualize_data():
    all_data = pandas.read_csv('dataset/user_activity.txt')

    all_data_grouped = all_data.groupby(['plan','state']).agg({'count' : 'count'}).reset_index()
    grouped_count = all_data_grouped['count'].sum()
    all_data_grouped['percentage'] = all_data_grouped['count'].div(grouped_count) * 100


"""
def create_model_v1(mongo):
    all_data = pandas.DataFrame.from_dict(Dao.mongo_data_dao().find_all(mongo))
    train_data, test_data = train_test_split(all_data, test_size=0.10, random_state=0)
    similarity_reco = Recommenders.SimilarRecommend()
    op = similarity_reco.recommend(train_data, 'user', 'plan', ['plan', 'state'])
    Dao.mongo_model_dao().drop(mongo)
    Dao.mongo_model_dao().persist_many(mongo, loads(op.to_json(orient='records')))
    print(op)
"""

def create_model(mongo, _id):
    all_data = pandas.DataFrame.from_dict(Dao.mongo_data_dao().find_all(mongo))
    train_data, test_data = train_test_split(all_data, test_size=0.10, random_state=0)

    reco_meta = Dao.mongo_reco_meta_dao().getOne(mongo, _id)
    user_id = reco_meta['user_field']
    item_id = reco_meta['item_field']
    feature = reco_meta['features'][0]['id']
    feature_weight = reco_meta['features'][0]['weight']
    train_data['feature'] = train_data[feature]
    train_data_grouped = train_data.groupby([user_id, item_id, 'feature']).agg({feature: 'count'}).reset_index()
    feature_count = feature + '_count'
    train_data_grouped.rename(columns={feature: feature_count}, inplace=True)
    train_data_grouped[feature + '_score'] = calculate_score(train_data_grouped, feature_count)
    print train_data_grouped

    # make this async
    drop_then_persist_model(mongo, train_data_grouped)

    reco_system = get_system(reco_meta['algo'])

    matrix = reco_system.build_correlation(train_data_grouped, user_id, item_id, feature, feature_weight)
    path = 'dataset/' + reco_meta['_id'] + '_corr_matrix.h5'
    HDF5Dao.save(path, 'correlation_matrix', matrix)


def get_system(algo):
    if algo == 'colab_user_based':
        collab_ubased = Recommenders.CollaborativeUserBased()
    return collab_ubased


def drop_then_persist_model(mongo, train_data_grouped):
    Dao.mongo_model_dao().drop(mongo)
    Dao.mongo_model_dao().persist_many(mongo, loads(train_data_grouped.to_json(orient='records')))


def calculate_score(train_data_grouped, feature_count):
    return train_data_grouped[feature_count].div(train_data_grouped[feature_count].sum())




