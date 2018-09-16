import pandas as pd
import math
import numpy as np


class PearsonCorrelation:

    def __init__(self):
        print

    def correlate(self, user_item_matrix, unique_objects):

        corr_matrix = pd.DataFrame(np.nan, index=unique_objects, columns=unique_objects)

        for user1 in unique_objects:
            user1_df = user_item_matrix[user1]
            user1_nonzero_count = (user1_df != 0).sum()
            if user1_nonzero_count <= 1:
                continue
            user1_nonzero_plans = user1_df.loc[user1_df != 0].index.tolist()
            user1_mean = user1_df.sum() / user1_nonzero_count
            for user2 in unique_objects:
                if user1 == user2:
                    corr_matrix[user1][user2] = 0
                    continue
                user2_df = user_item_matrix[user2]
                user2_nonzero_count = (user2_df != 0).sum()
                if user2_nonzero_count <= 1:
                    corr_matrix[user1][user2] = 0
                    continue
                user2_mean = user2_df.sum() / user2_nonzero_count
                user2_nonzero_plans = user2_df.loc[user2_df != 0].index.tolist()
                common_plans = self.find_common_items(user1_nonzero_plans, user2_nonzero_plans)
                if len(common_plans) <= 1:
                    corr_matrix[user1][user2] = 0
                    continue
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
                    sqr = math.sqrt(user1item_minus_mean_sqr_summation * user2item_minus_mean_sqr_summation)
                    corr_matrix[user1][user2] = num_summation / (
                        sqr
                    )
        return corr_matrix

    @staticmethod
    def find_common_items(user1_nonzero_plans, user2_nonzero_plans):
        if len(user1_nonzero_plans) > len(user2_nonzero_plans):
            return [plan for plan in user1_nonzero_plans if plan in user2_nonzero_plans]
        return [plan for plan in user2_nonzero_plans if plan in user1_nonzero_plans]



