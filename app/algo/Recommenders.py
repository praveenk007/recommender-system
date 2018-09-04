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

    def create_model(self, train_data, user_id, item_id, group_by):
        self.train_data = train_data
        self.user_id = user_id
        self.item_id = item_id

        train_data['state_count'] = train_data['state']
        print(train_data)

        train_data_grouped = train_data.groupby(group_by).agg({'state_count': 'count'}).reset_index()
        print(train_data_grouped)
        train_data_grouped.rename(columns={'state_count': 'count'}, inplace=True)
        train_data_grouped['score'] = self.calculate_score(train_data_grouped)
        self.similarity_model = train_data_grouped.sort_values(['score', self.item_id], ascending=[0, 1])
        return self.similarity_model

    def calculate_score(self, train_data_grouped):
        return train_data_grouped['count'].div(train_data_grouped['count'].sum())

    def find_similar_users(self):


        return [];
