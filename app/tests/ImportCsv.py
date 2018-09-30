import pandas

movies_df = pandas.read_csv('../../dataset/movies.csv')
ratings_df = pandas.read_csv('../../dataset/ratings.csv')
result = ratings_df.merge(movies_df, on='movieId')
result.to_csv('../../dataset/ml_result.csv')