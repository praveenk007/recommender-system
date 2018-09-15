import pandas as pd
import math


class PearsonCorrelation:

    def __init__(self):
        print

    def correlate(self, train_data_grouped, user_id, item_id, feature, weight):

        """
        :param self:
        :param train_data_grouped:
        :param user_id:
        :param item_id:
        :param feature:
        :param weight:
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
                    user_item_matrix[user][item] = temp_df[feature + '_score'].iloc[0] * weight
        print(user_item_matrix)

        corr_matrix = pd.DataFrame(index=unique_users, columns=unique_users)

        for user1 in unique_users:
            user1_df = user_item_matrix[user1].astype(str).astype(float)
            user1_nonzero_count = (user1_df != 0).sum()
            user1_nonzero_plans = user1_df.loc[user1_df != 0].index.tolist()
            user1_mean = user1_df.sum() / user1_nonzero_count
            for user2 in unique_users:
                if user1 == user2:
                    corr_matrix[user1][user2] = 1
                    if user1_nonzero_count <= 1:
                        break
                    else:
                        continue
                user2_df = user_item_matrix[user2]
                user2_nonzero_count = (user2_df != 0).sum()
                if user2_nonzero_count <= 1:
                    continue
                user2_mean = user2_df.sum() / user2_nonzero_count
                user2_nonzero_plans = user2_df.loc[user2_df != 0].index.tolist()
                common_plans = self.find_common_plans(user1_nonzero_plans, user2_nonzero_plans)
                if len(common_plans) <= 1:
                    continue
                print user1, user2
                print common_plans
                num_summation = 0
                user1item_minus_mean_sqr_summation = 0
                user2item_minus_mean_sqr_summation = 0
                for item in common_plans:
                    if user_item_matrix[user1][item] != 0 and user_item_matrix[user2][item] != 0:
                        user1_score = user_item_matrix[user1][item]
                        user2_score = user_item_matrix[user2][item]

                        user1item_minus_mean = user1_score - user1_mean
                        user2item_minus_mean = user2_score - user2_mean

                        user1item_minus_mean_sqr_summation = user1item_minus_mean_sqr_summation + (
                                    user1item_minus_mean * user1item_minus_mean)
                        user2item_minus_mean_sqr_summation = user2item_minus_mean_sqr_summation + (
                                    user2item_minus_mean * user2item_minus_mean)

                        num_summation = num_summation + (user1item_minus_mean * user2item_minus_mean)
                if num_summation == 0:
                    corr_matrix[user1][user2] = 0
                else:
                    corr_matrix[user1][user2] = num_summation / (
                        math.sqrt(user1item_minus_mean_sqr_summation * user2item_minus_mean_sqr_summation)
                    )
        print corr_matrix

    def find_common_plans(self, user1_nonzero_plans, user2_nonzero_plans):
        if len(user1_nonzero_plans) > len(user2_nonzero_plans):
            return [plan for plan in user1_nonzero_plans if plan in user2_nonzero_plans]
        return [plan for plan in user2_nonzero_plans if plan in user1_nonzero_plans]

    def get_unique_objects(self, data, ids):
        return data[ids].unique()

