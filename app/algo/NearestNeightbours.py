class KNN:

    def __init__(self, obj, corr_matrix, k=5):
        self.object = obj
        self.corr_matrix = corr_matrix
        self.k = k

    def find_nearest(self):
        return self.corr_matrix.sort_values([self.object], ascending=[0]).head(self.k).index.tolist()

