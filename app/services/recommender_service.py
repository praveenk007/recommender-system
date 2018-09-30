import pandas
from app.dao import HDF5Dao
from app.algo import Recommenders

from app.dao import Dao
from bson.json_util import loads
from sklearn.model_selection import train_test_split


def visualize_data():
    all_data = pandas.read_csv('dataset/user_activity.txt')

    all_data_grouped = all_data.groupby(['plan', 'state']).agg({'count': 'count'}).reset_index()
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
    print reco_meta
    user_id = reco_meta['user_field']
    item_id = reco_meta['item_field']
    feature = item_id
    feature_weight = 1

    if 'features' in reco_meta:
        feature = reco_meta['features'][0]['id']
        feature_weight = reco_meta['features'][0]['weight']
        train_data['feature'] = train_data[feature]
        train_data_grouped = train_data.groupby([user_id, item_id, 'feature']).agg({feature: 'count'}).reset_index()
        if not reco_meta['isScored']:
            feature_count = feature + '_count'
            train_data_grouped.rename(columns={feature: feature_count}, inplace=True)
            train_data_grouped[feature + '_score'] = calculate_score(train_data_grouped, feature_count)
        else:
            train_data_grouped.rename(columns={reco_meta['scoreField']: feature + '_score'}, inplace=True)
    else:
        train_data['feature'] = train_data[feature]
        train_data_grouped = train_data
        if not reco_meta['isScored']:
            feature_count = feature + '_count'
            train_data_grouped.rename(columns={'feature': feature_count}, inplace=True)
            train_data_grouped[feature + '_score'] = calculate_score(train_data_grouped, feature_count)
        else:
            train_data_grouped.rename(columns={reco_meta['score_field']: feature + '_score'}, inplace=True)

    print train_data_grouped.columns.values

    reco_system = get_system(reco_meta['algo'])
    unique_users = [s for s in get_unique_objects(train_data_grouped, user_id)]
    print 'calculated unique users'
    unique_items = [s for s in get_unique_objects(train_data_grouped, item_id)]
    print 'calculated unique items'
    user_item_matrix = reco_system.get_user_item_matrix(train_data_grouped, unique_users, unique_items, user_id, item_id, feature, feature_weight)
    print user_item_matrix.dtypes
    path = 'dataset/' + reco_meta['_id'] + '.h5'
    HDF5Dao.save(path, 'user_item_matrix', user_item_matrix)

    matrix = reco_system.build_correlation(user_item_matrix, unique_users, unique_items)
    print 'saving corr matrix'
    HDF5Dao.save(path, 'correlation_matrix', matrix)


def recommend(mongo, _id, user, k=10):
    reco_meta = Dao.mongo_reco_meta_dao().getOne(mongo, _id)
    reco_system = get_system(reco_meta['algo'])
    hdf5path = 'dataset/' + reco_meta['_id'] + '.h5'
    corr_matrix = HDF5Dao.get(hdf5path, 'correlation_matrix')
    user_item_matrix = HDF5Dao.get(hdf5path, 'user_item_matrix')
    return reco_system.recommend(user, user_item_matrix, corr_matrix, k)


def get_system(algo):
    if algo == 'colab_user_based':
        collab_ubased = Recommenders.CollaborativeUserBased()
    # if algo == 'colab_item_based':
    return collab_ubased


def get_trained_aggregated_data(mongo):
    return Dao.mongo_model_dao().find_all(mongo)


def drop_then_persist_model(mongo, train_data_grouped):
    Dao.mongo_model_dao().drop(mongo)
    Dao.mongo_model_dao().persist_many(mongo, loads(train_data_grouped.to_json(orient='records')))


def calculate_score(train_data_grouped, feature_count):
    print 'Calculating score'
    return train_data_grouped[feature_count].div(train_data_grouped[feature_count].sum())


def get_unique_objects(data, ids):
    return data[ids].unique()




