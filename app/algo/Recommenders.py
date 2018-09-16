from app.algo import Correlation, NearestNeightbours
import pandas as pd
import numpy as np


class PopularityBased:

    def __init__(self):
        self.train_data = None
        self.user_id = None
        self.item_id = None
        self.popularity_model = None

    def create_model(self, train_data, user_id, item_id, group_by):
        self.train_data = train_data
        self.user_id = user_id
        self.item_id = item_id

        train_data_grouped = train_data.groupby(group_by).agg({self.user_id: 'count'}).reset_index()
        print(train_data_grouped)
        train_data_grouped.rename(columns={'user': 'count'}, inplace=True)
        train_data_grouped['score'] = self.calculate_score(train_data_grouped)
        self.popularity_model = train_data_grouped.sort_values(['score', self.item_id], ascending=[0, 1])
        return self.popularity_model

    def calculate_score(self, train_data_grouped):
        return train_data_grouped['count'].div(train_data_grouped['count'].sum())

    def recommend(self, user_id):
        user_recommendations = self.popularity_model
        user_recommendations['user'] = user_id
        return user_recommendations


class CollaborativeUserBased:

    def __init__(self):
        print

    def get_user_item_matrix(self, train_data_grouped, unique_users, unique_items, user_id, item_id, feature, weight):
        user_item_matrix = pd.DataFrame(np.nan, index=unique_items, columns=unique_users)

        for user in unique_users:
            for item in unique_items:
                temp_df = train_data_grouped.query(user_id + ' == @user and ' + item_id + '== @item').reset_index()
                if temp_df.empty:
                    user_item_matrix[user][item] = 0.0
                else:
                    user_item_matrix[user][item] = temp_df[feature + '_score'].iloc[0] * weight

        return user_item_matrix

    def build_correlation(self, user_item_matrix, unique_users, unique_items):

        corr_matrix = Correlation.PearsonCorrelation().correlate(user_item_matrix, unique_users)
        print corr_matrix
        return corr_matrix
        # save correlation matrix
        # comment below
        # self.recommend('gh', corr_matrix)

    def recommend(self, user, user_item_matrix, corr_matrix, k=10):
        k_similar_users = NearestNeightbours.KNN(user, corr_matrix, k).find_nearest()
        print k_similar_users









