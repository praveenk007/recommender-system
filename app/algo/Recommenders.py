import pandas as pd

class popularity_recommender():

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

class similar_recommender():

    def __init__(self):
        self.train_data = None
        self.user_id = None
        self.item_id = None
        self.similarity_model = None

    def create_model_v1(self, train_data, user_id, item_id, group_by):
        self.train_data = train_data
        self.user_id = user_id
        self.item_id = item_id

        train_data['state_count'] = train_data['state']

        train_data_grouped = train_data.groupby(group_by).agg({'state_count': 'count'}).reset_index()
        print(train_data_grouped)
        train_data_grouped.rename(columns={'state_count': 'count'}, inplace=True)
        train_data_grouped['score'] = self.calculate_score(train_data_grouped)
        self.similarity_model = train_data_grouped.sort_values(['score', self.item_id], ascending=[0, 1])
        return self.similarity_model

    def create_model_v2(self, train_data, user_id, item_id, feature):
        print(train_data)
        self.user_id = user_id
        self.item_id = item_id
        train_data['feature'] = train_data[feature]
        train_data_grouped = train_data.groupby([self.user_id, item_id, 'feature']).agg({feature: 'count'}).reset_index()
        feature_count = feature+'_count'
        train_data_grouped.rename(columns={feature: feature_count}, inplace=True)
        train_data_grouped[feature + '_score'] = self.calculate_score(train_data_grouped, feature_count)
        return train_data_grouped

    def calculate_score(self, train_data_grouped, feature_count):
        return train_data_grouped[feature_count].div(train_data_grouped[feature_count].sum())

    def find_similar_users(self):


        return [];

    def correlate(self, train_data_grouped, user_id, item_id, feature):
        """
        finds correlation between users
        :param item_id:
        :param train_data_grouped:
        :return:
        """
        unique_users = self.get_unique_objects(train_data_grouped, user_id)
        unique_items = self.get_unique_objects(train_data_grouped, item_id)

        user_item_matrix = pd.DataFrame(index=unique_items, columns=unique_users)

        for user in unique_users:
            for item in unique_items:
                temp_df = train_data_grouped.query(user_id + ' == @user and ' + item_id + '== @item').reset_index()
                if temp_df.empty:
                    user_item_matrix[user][item] = 0
                else:
                    user_item_matrix[user][item] = temp_df[feature + '_score'].iloc[0]
        print(user_item_matrix)



    def get_unique_objects(self, data, ids):
        return data[ids].unique()
