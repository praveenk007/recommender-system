class mongo_data_dao():

    def find_all(self, mongo):
        arr = []
        for doc in mongo.db.ml_result.find({}):
            arr.append(doc)
        return arr

class mongo_model_dao():

    def drop(self, mongo):
        mongo.db.RecommenderModel.drop()

    def persist_many(self, mongo, docs):
        for doc in docs:
            mongo.db.RecommenderModel.save(doc)
        print('model saved successfully!')

    def persist(self, mongo, doc):
        mongo.db.RecommenderModel.save(doc)
        print('model saved successfully!')

    def find_all(self, mongo):
        arr = []
        for doc in mongo.db.RecommenderModel.find({}):
            arr.append(doc)
        return arr

class mongo_reco_meta_dao():

    def getOne(self, mongo, id):
        for doc in mongo.db.RecommenderMeta.find({'_id' : id}):
            return doc

